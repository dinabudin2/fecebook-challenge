 
window.onload = () => {
    gsap.from(".login-container", { duration: 1.5, opacity: 0, y: -50, ease: "power2.out" });
};

 
document.querySelectorAll('.social-btn').forEach(button => {
    button.addEventListener('mouseover', () => {
        gsap.to(button, { duration: 0.3, scale: 1.1 });
    });

    button.addEventListener('mouseout', () => {
        gsap.to(button, { duration: 0.3, scale: 1 });
    });
});

 
document.getElementById('google-btn').addEventListener('click', () => {
    window.location.href = 'https://accounts.google.com/';
});

document.getElementById('facebook-btn').addEventListener('click', () => {
    window.location.href = 'https://www.facebook.com/login/';
});

 
window.onload = () => {
    gsap.from("h2", { duration: 1.5, opacity: 0, scale: 0.8, ease: "elastic.out(1, 0.5)" });
    gsap.to("h2", { duration: 1, textShadow: "0px 0px 10px #00d1ff, 0px 0px 20px #00d1ff", repeat: -1, yoyo: true, ease: "power1.inOut" });
};

