// Animate login form elements on page load
window.onload = function() {
    gsap.from(".form-box", { opacity: 0, y: 30, duration: 1, ease: "power2.out" });
    gsap.from("input[type='text'], input[type='password']", { opacity: 0, y: 20, duration: 0.8, ease: "power2.out", stagger: 0.1 });
    gsap.from("button", { opacity: 0, scale: 0.8, duration: 0.8, ease: "elastic.out(1, 0.5)", delay: 0.3 });
};
