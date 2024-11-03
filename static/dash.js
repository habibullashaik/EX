// GSAP Animation for page load
window.onload = function() {
    gsap.from("h1", { opacity: 0, y: -20, duration: 1, ease: "power2.out" });
    gsap.from(".status-bar button, .status-bar select", { 
        opacity: 0, 
        y: 20, 
        duration: 0.8, 
        ease: "power2.out", 
        stagger: 0.1 
    });
    gsap.from(".add-expense-box", { 
        opacity: 0, 
        scale: 0.8, 
        duration: 1, 
        ease: "elastic.out(1, 0.5)" 
    });
    gsap.from(".chart-container", { 
        opacity: 0, 
        scale: 0.9, 
        duration: 1, 
        ease: "bounce.out" 
    });
};

// Function to update the selected timeframe
function updateTimeframe() {
    var timeframe = document.getElementById('timeSelect').value;
    console.log("Selected timeframe: ", timeframe);
    // Additional logic for handling the timeframe can be added here
}

