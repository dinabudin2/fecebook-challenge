document.querySelector('form').addEventListener('submit', function(e) {
    const query = document.querySelector('input[name="query"]').value;
    if (query.trim() === '') {
        alert("Please enter a search term.");
        e.preventDefault();
    }
});

document.getElementById('job-form').addEventListener('submit', function(event) {
    const requirements = document.getElementById('requirements').value;
    const errorMessage = document.getElementById('error-message');
    
    if (!requirements.trim()) {
        event.preventDefault();   
        errorMessage.classList.remove('hidden');
    } else {
        errorMessage.classList.add('hidden');
    }
});


 
window.onload = () => {
    gsap.from(".search-container", { duration: 1.5, opacity: 0, y: 50, ease: "power2.out" });
};

 
document.getElementById('searchForm').addEventListener('submit', function (e) {
    e.preventDefault();  

     
    const loadingAnimation = document.getElementById('loadingAnimation');
    loadingAnimation.style.display = 'block';

     
    setTimeout(() => {
        loadingAnimation.style.display = 'none';  
        displayResults();  
    }, 2000);  
});

