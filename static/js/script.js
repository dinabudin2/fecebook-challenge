document.addEventListener('mousemove', function(e) {
    let x = e.clientX / window.innerWidth;
    let y = e.clientY / window.innerHeight;
    document.body.style.backgroundPosition = `${x * 50}px ${y * 50}px`;
});
