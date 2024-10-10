// הנפשה של תיבת ההרשמה
window.onload = () => {
    gsap.from(".register-container", { duration: 1.5, opacity: 0, y: 50, ease: "power2.out" });
    gsap.to("h2", { duration: 1, textShadow: "0px 0px 10px #00ff9f, 0px 0px 20px #00bfff", repeat: -1, yoyo: true, ease: "power1.inOut" });
};

// הנפשת כפתור ההרשמה
document.querySelector('.register-btn').addEventListener('mouseover', () => {
    gsap.to('.register-btn', { duration: 0.5, scale: 1.1 });
});

document.querySelector('.register-btn').addEventListener('mouseout', () => {
    gsap.to('.register-btn', { duration: 0.5, scale: 1 });
});
