// Example function to add an expense list item with fade-in and slide-up effect
function addExpenseItem(title, amount, category) {
    // Create the expense item element
    const expenseItem = document.createElement("div");
    expenseItem.classList.add("expense-item");

    // Add content to the item
    expenseItem.innerHTML = `
        <h3>${title}</h3>
        <p>Amount: ₹${amount}</p>
        <p>Category: ${category}</p>
    `;

    // Style and add fade-in & slide-up animation
    expenseItem.style.opacity = 0;
    expenseItem.style.transform = "translateY(20px)";
    document.body.appendChild(expenseItem);

    // Animation effect
    setTimeout(() => {
        expenseItem.style.transition = "opacity 0.5s ease, transform 0.5s ease";
        expenseItem.style.opacity = 1;
        expenseItem.style.transform = "translateY(0)";
    }, 100);
}
