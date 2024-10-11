document.addEventListener('DOMContentLoaded', function() {
     
    let rows = document.querySelectorAll('table tbody tr');
    rows.forEach(row => {
        row.addEventListener('mouseover', function() {
            this.style.backgroundColor = '#f1f1f1';
        });

        row.addEventListener('mouseout', function() {
            this.style.backgroundColor = '';
        });
    });

     
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

     
    let headers = document.querySelectorAll('th');
    headers.forEach((header, index) => {
        let ascending = true;
        header.addEventListener('click', function() {
            let table = header.closest('table');
            sortTable(table, index, ascending);
            ascending = !ascending;   
        });
    });
});


 
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


 
function fetchResults() {
     
    let results = getResultsFromSearch();  

     
    const resultsArea = document.getElementById('resultsArea');
    results.forEach(result => {
         
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

 
function getResultsFromSearch() {
     
    let query = getQueryFromSearch();  
    let results = query ? query : [];  
    return results;
}
