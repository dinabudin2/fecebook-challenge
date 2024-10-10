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
        event.preventDefault();  // מניעת שליחת הטופס אם אין דרישות
        errorMessage.classList.remove('hidden');
    } else {
        errorMessage.classList.add('hidden');
    }
});


// הנפשת תיבת החיפוש בעת טעינת הדף
window.onload = () => {
    gsap.from(".search-container", { duration: 1.5, opacity: 0, y: 50, ease: "power2.out" });
};

// טיפול בטופס החיפוש והצגת אנימציית הטעינה
document.getElementById('searchForm').addEventListener('submit', function (e) {
    e.preventDefault(); // ביטול פעולת ברירת המחדל כדי להציג את ההנפשה

    // הצגת אנימציית הטעינה
    const loadingAnimation = document.getElementById('loadingAnimation');
    loadingAnimation.style.display = 'block';

    // הדמיית זמן חיפוש
    setTimeout(() => {
        loadingAnimation.style.display = 'none'; // הסתרת הטעינה לאחר החיפוש
        displayResults(); // הצגת התוצאות
    }, 2000); // זמן לדוגמה של 2 שניות לחיפוש
});

