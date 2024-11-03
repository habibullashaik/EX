// Optional JavaScript if you want to handle specific behaviors or animations
document.addEventListener('DOMContentLoaded', function () {
    // Select all rows with the fade-in-slide-up class
    const rows = document.querySelectorAll('.fade-in-slide-up');
    rows.forEach((row, index) => {
        // Delay the animation for each row
        row.style.animationDelay = `${index * 0.1}s`;
    });
});
