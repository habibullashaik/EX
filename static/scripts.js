document.getElementById('signup-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const password = event.target.password.value;
    const confirmPassword = event.target.confirm_password.value;
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }
    alert("Signed up successfully!");
});

document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    alert("Logged in successfully!");
});
