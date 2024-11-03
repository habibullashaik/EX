from flask import Flask, render_template, request, redirect, url_for, jsonify,flash, get_flashed_messages
from datetime import datetime, timedelta
import sqlite3
from datetime import datetime, timedelta
import secrets
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Initialize the database
def init_db():
    conn = sqlite3.connect('expenditure.db')
    c = conn.cursor()
    
    # Ensure the table for expenditures is created
    c.execute('''CREATE TABLE IF NOT EXISTS expenditures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
   

    
    # Table for recurring expenses
    c.execute('''CREATE TABLE IF NOT EXISTS recurring_expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        interval TEXT NOT NULL,  -- e.g., 'daily', 'weekly', 'monthly'
        start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Create the incomes table
    c.execute('''
    CREATE TABLE IF NOT EXISTS incomes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect('expenditure.db')
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

@app.route('/')
def signup():
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    conn = get_db_connection()
    query = 'SELECT * FROM expenditures WHERE 1=1'
    filters = []

    # Apply filters from request arguments
    if 'search' in request.args:
        search_term = request.args['search']
        query += ' AND (title LIKE ? OR amount LIKE ? OR date LIKE ?)'
        filters.extend(['%' + search_term + '%'] * 3)
    
    if 'category' in request.args:
        query += ' AND category = ?'
        filters.append(request.args['category'])
    if 'start_date' in request.args and 'end_date' in request.args:
        query += ' AND date BETWEEN ? AND ?'
        filters.extend([request.args['start_date'], request.args['end_date']])
    if 'min_amount' in request.args:
        query += ' AND amount >= ?'
        filters.append(request.args['min_amount'])
    if 'max_amount' in request.args:
        query += ' AND amount <= ?'
        filters.append(request.args['max_amount'])

    expenditures = conn.execute(query, filters).fetchall()
    incomes = conn.execute('SELECT * FROM incomes').fetchall()
    conn.close()
    
    # Calculate total expenses, income, and balance
    total_expenses = sum([expense['amount'] for expense in expenditures])
    total_income = sum([income['amount'] for income in incomes])
    balance = total_income - total_expenses

    return render_template('dashboard.html', expenses=expenditures, incomes=incomes, balance=balance)

@app.route('/filter-data/<period>')
def filter_data(period):
    conn = get_db_connection()
    query = 'SELECT * FROM expenditures WHERE 1=1'
    income_query = 'SELECT * FROM incomes WHERE 1=1'
    filters = []

    # Define date filter based on the period
    if period != 'all':
        days = int(period)
        start_date = datetime.now() - timedelta(days=days)
        query += ' AND date >= ?'
        income_query += ' AND date >= ?'
        filters.append(start_date)

    expenditures = conn.execute(query, filters).fetchall()
    incomes = conn.execute(income_query, filters).fetchall()
    conn.close()

    return render_template('filtered_data.html', expenditures=expenditures, incomes=incomes)
@app.route('/add-expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        category = request.form['category']
        conn = get_db_connection()
        
        # Ensure this line is correct and actually inserts into the expenditures table
        conn.execute('INSERT INTO expenditures (title, amount, category) VALUES (?, ?, ?)',
                     (title, amount, category))
        conn.commit()
        conn.close()
        
        return redirect(url_for('dashboard'))  # Redirect back to the dashboard after submission
    
    return render_template('add_expense.html')  # Render the form if GET request


# Add Recurring Expense
@app.route('/add-recurring-expense', methods=['GET', 'POST'])
def add_recurring_expense():
    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        category = request.form['category']
        interval = request.form['interval']  # daily, weekly, or monthly
        conn = get_db_connection()
        conn.execute('INSERT INTO recurring_expenses (title, amount, category, interval) VALUES (?, ?, ?, ?)',
                     (title, amount, category, interval))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_recurring_expense.html')

# Add Income
@app.route('/add-income', methods=['GET', 'POST'])
def add_income():
    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        category = request.form['category']
        conn = get_db_connection()
        conn.execute('INSERT INTO incomes (title, amount, category) VALUES (?, ?, ?)', 
                     (title, amount, category))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_income.html')

@app.route('/recently-added')
def recently_added():
    conn = get_db_connection()
    expenditures = conn.execute('SELECT * FROM expenditures ORDER BY date DESC LIMIT 10').fetchall()
    conn.close()
    return render_template('recently_added.html', expenditures=expenditures)

@app.route('/overall')
def overall():
    conn = get_db_connection()
    expenditures = conn.execute('SELECT * FROM expenditures').fetchall()
    conn.close()
    
    overall_data = {
        'total_amount': sum(expense['amount'] for expense in expenditures),
        'categories': {}
    }
    
    for expense in expenditures:
        category = expense['category']
        if category in overall_data['categories']:
            overall_data['categories'][category] += expense['amount']
        else:
            overall_data['categories'][category] = expense['amount']
    
    return render_template('overall.html', expenditures=expenditures, overall_data=overall_data)

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

@app.route('/get_graph_data')
def get_graph_data():
    conn = get_db_connection()
    category_expenses = conn.execute('SELECT category, SUM(amount) FROM expenditures GROUP BY category').fetchall()
    labels = [row['category'] for row in category_expenses]
    data = [row['SUM(amount)'] for row in category_expenses]
    conn.close()
    return jsonify(labels=labels, data=data)

@app.route('/get_monthly_expenses')
def get_monthly_expenses():
    conn = get_db_connection()
    monthly_expenses = conn.execute('SELECT strftime("%Y-%m", date) AS month, SUM(amount) FROM expenditures GROUP BY month ORDER BY month').fetchall()
    labels = [row['month'] for row in monthly_expenses]
    data = [row['SUM(amount)'] for row in monthly_expenses]
    conn.close()
    return jsonify(labels=labels, data=data)

@app.route('/get_doughnut_data')
def get_doughnut_data():
    conn = get_db_connection()
    category_expenses = conn.execute('SELECT category, SUM(amount) FROM expenditures GROUP BY category').fetchall()
    labels = [row['category'] for row in category_expenses]
    data = [row['SUM(amount)'] for row in category_expenses]
    conn.close()
    return jsonify(labels=labels, data=data)

@app.route('/delete-data', methods=['GET', 'POST'])
def delete_data():
    conn = get_db_connection()
    if request.method == 'POST':
        data_id = request.form['data_id']
        conn.execute('DELETE FROM expenditures WHERE id = ?', (data_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('overall'))
    
    expenditures = conn.execute('SELECT * FROM expenditures').fetchall()
    conn.close()
    return render_template('delete_data.html', expenditures=expenditures)
@app.route('/delete-income-page')
def delete_income_page():
    conn = get_db_connection()
    incomes = conn.execute("SELECT * FROM incomes").fetchall()
    conn.close()
    return render_template('delete_income_page.html', incomes=incomes)

@app.route('/delete_income/<int:income_id>', methods=['POST'])
def delete_income(income_id):
    conn = get_db_connection()  # Get a database connection
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM incomes WHERE id = ?', (income_id,))
        conn.commit()
        flash('Income entry deleted successfully!')
    except Exception as e:
        flash('An error occurred while trying to delete the income entry.')
        print(e)  # Print the error to the console for debugging
    finally:
        conn.close()  # Ensure the connection is closed
    return redirect(url_for('dashboard'))  # Redirect to the dashboard instead


# Ensure to add flash messages to your HTML templates
@app.route('/flash-example')
def flash_example():
    flash('This is a flash message example.')
    return redirect(url_for('some_page'))


if __name__ == '__main__':
    app.run(debug=True)
