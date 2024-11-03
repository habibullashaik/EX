// JavaScript for adding interactive animations

document.addEventListener("DOMContentLoaded", function() {
    // Animate each table row as it loads
    const rows = document.querySelectorAll("tbody tr");
    rows.forEach((row, index) => {
        row.style.animationDelay = `${index * 0.1}s`;
    });

    // Confirmation before deletion
    const deleteButtons = document.querySelectorAll(".delete-btn");
    deleteButtons.forEach(button => {
        button.addEventListener("click", function(event) {
            const confirmed = confirm("Are you sure you want to delete this expense?");
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
});
