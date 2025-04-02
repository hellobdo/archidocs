const tableBody = document.getElementById('tableBody');
const rows = generateCalendarRows();
tableBody.innerHTML = rows;

function generateCalendarRows(numRows = 20) {
    let rows = '';
    
    for (let i = 1; i <= numRows; i++) {
        rows += `<tr><td>{{table_row${i}}}</td>`;
        
        // Add 12 month cells
        for (let month = 0; month < 12; month++) {
            rows += '<td></td>';
        }
        
        rows += '</tr>\n';
    }
    
    return rows;
} 