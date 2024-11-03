// JavaScript for adding interactive animations

document.addEventListener("DOMContentLoaded", function() {
    // Animate each table row as it loads
    const rows = document.querySelectorAll("tbody tr");
    rows.forEach((row, index) => {
        row.style.animationDelay = `${index * 0.1}s`;
    });

    // Confirmation message before navigating to the dashboard
    const backButton = document.querySelector("button");
    backButton.addEventListener("click", function(event) {
        const confirmed = confirm("Are you sure you want to go back to the dashboard?");
        if (!confirmed) {
            event.preventDefault();
        }
    });
});
