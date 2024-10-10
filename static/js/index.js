// הנפשת הכותרת והכפתור בכניסה לעמוד
window.onload = () => {
    gsap.from(".main-title", { duration: 1.5, opacity: 0, y: -50, ease: "power2.out" });
    gsap.from(".cta-button", { duration: 1.5, opacity: 0, scale: 0.8, ease: "power2.out", delay: 0.5 });
};

// אפקטים לכפתור הקריאה לפעולה
document.querySelector('.cta-button').addEventListener('mouseover', () => {
    gsap.to('.cta-button', { duration: 0.5, scale: 1.1 });
});

document.querySelector('.cta-button').addEventListener('mouseout', () => {
    gsap.to('.cta-button', { duration: 0.5, scale: 1 });
});
