document.addEventListener('DOMContentLoaded', function() {
    // הוספת הדגשה כאשר עוברים עם העכבר על שורה בטבלה
    let rows = document.querySelectorAll('table tbody tr');
    rows.forEach(row => {
        row.addEventListener('mouseover', function() {
            this.style.backgroundColor = '#f1f1f1';
        });

        row.addEventListener('mouseout', function() {
            this.style.backgroundColor = '';
        });
    });

    // פונקציה למיון טבלה לפי עמודה
    function sortTable(table, column, ascending) {
        let tbody = table.querySelector('tbody');
        let rowsArray = Array.from(tbody.querySelectorAll('tr'));
        
        rowsArray.sort((a, b) => {
            let aText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
            let bText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
            
            return ascending ? aText.localeCompare(bText) : bText.localeCompare(aText);
        });

        rowsArray.forEach(row => tbody.appendChild(row));
    }

    // הפעלת מיון בלחיצה על הכותרת של העמודה
    let headers = document.querySelectorAll('th');
    headers.forEach((header, index) => {
        let ascending = true;
        header.addEventListener('click', function() {
            let table = header.closest('table');
            sortTable(table, index, ascending);
            ascending = !ascending;  // הפוך את הסדר בכל לחיצה
        });
    });
});


// הנפשת תיבת התוצאות בעת טעינת הדף
window.onload = () => {
    const resultsArea = document.getElementById('resultsArea');
    fetchResults().then(data => {
        data.passed.forEach(candidate => {
            const candidateElement = document.createElement('li');
            candidateElement.textContent = `${candidate.name} - ${candidate.position} - ${candidate.skills}`;
            resultsArea.appendChild(candidateElement);
        });
    });
};


// פונקציה שמבצעת את החיפוש ומציגה את התוצאות בעמוד
function fetchResults() {
    // נניח שהפונקציה הזו כבר קיימת בקוד שלך ומשתמשת באוטומציה להחזרת תוצאות
    let results = getResultsFromSearch(); // פונקציה קיימת שאוספת תוצאות

    // נניח שהתוצאות מתקבלות בפורמט JSON
    const resultsArea = document.getElementById('resultsArea');
    results.forEach(result => {
        // יצירת אלמנט דינמי להצגת תוצאה
        const resultRow = document.createElement('div');
        resultRow.className = 'result-row';
        resultRow.innerHTML = `
            <span>${result.name}</span>
            <span>${result.position}</span>
            <span>${result.skills.join(', ')}</span>
            <span>${result.experience} years</span>
            <span>${result.status}</span>
        `;
        resultsArea.appendChild(resultRow);
    });
}

// פונקציה שמבצעת את החיפוש ומציגה את התוצאות בעמוד
function getResultsFromSearch() {
    // נניח שהפונקציה הזו כבר קיימת בקוד שלך ומשתמשת באוטומציה להחזרת תוצאות
    let query = getQueryFromSearch(); // פונקציה קיימת שאוספת תוצאות
    let results = query ? query : []; // נניח שהתוצאות מתקבלות בפונקציה קיימת שאוספת תוצאות
    return results;
}
