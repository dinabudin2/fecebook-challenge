// הנפשת תיבת ההעלאה בעת טעינת הדף
window.onload = () => {
    gsap.from(".upload-container", { duration: 1.5, opacity: 0, y: 50, ease: "power2.out" });
};

// טיפול בטופס העלאת הקבצים
document.querySelector('form[action="/upload"]').addEventListener('submit', function(e) {
    e.preventDefault();
    const fileInput = document.querySelector('#fileUpload');
    
    if (fileInput.files.length === 0) {
        alert("Please select at least one file to upload.");
        return;
    }

    const progressBar = document.querySelector('.progress-fill');
    let progress = 0;
    const totalFiles = fileInput.files.length;
    let totalSize = 0;
    
    // חשב את סך כל גודל הקבצים
    for (let i = 0; i < totalFiles; i++) {
        totalSize += fileInput.files[i].size;
    }

    let uploadedSize = 0;

    // חיווי התקדמות מבוסס על סך גודל הקבצים
    const interval = setInterval(() => {
        uploadedSize += totalSize / 10; 
        progress = Math.min((uploadedSize / totalSize) * 100, 100);
        progressBar.style.width = `${progress}%`;

        if (progress >= 100) {
            clearInterval(interval);
            alert('Files uploaded successfully!');
            document.getElementById('uploadForm').submit(); // המשך העלאה לאחר חיווי ההתקדמות
        }
    }, 200);  // התקדמות כל 200 מילישניות
});

// טיפול בטופס החיפוש
document.querySelector('form[action="/search"]').addEventListener('submit', function(e) {
    e.preventDefault();
    const query = document.querySelector('#query').value;
    const passedTable = document.querySelector('#passed-table');
    const failedTable = document.querySelector('#failed-table');

    // הוספת תוצאות למסמכים שעברו
    mockDataPassed.forEach(file => {
        let row = passedTable.insertRow();
        let cell = row.insertCell();
        cell.textContent = file;
        row.style.backgroundColor = 'green';
    });

    // הוספת תוצאות למסמכים שלא עברו
    mockDataFailed.forEach(file => {
        let row = failedTable.insertRow();
        let cell = row.insertCell();
        cell.textContent = file;
        row.style.backgroundColor = 'red';
    });

    // הצגת תוצאות החיפוש
    const resultsSection = document.querySelector('.results-section');
    resultsSection.style.display = 'block';
});
