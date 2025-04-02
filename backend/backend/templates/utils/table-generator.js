const tableBody = document.getElementById('tableBody');
const totalRow = tableBody.querySelector('.total-row');
const rows = generateTableRows();
totalRow.insertAdjacentHTML('beforebegin', rows);

function generateTableRows(numRows = 20) {
    let rows = '';
    
    for (let i = 1; i <= numRows; i++) {
        rows += `<tr><td>{{table_row${i}}}</td>`;
        
        // Add the rowspan cells only for the first row
        if (i === 1) {
            rows += `
                <td rowspan="${numRows}">m²</td>
                <td rowspan="${numRows}">{{qty}}</td>
                <td rowspan="${numRows}">{{cost_per_unit}}</td>
                <td rowspan="${numRows}">{{total_cost}}</td>
            `;
        }
        
        rows += '</tr>\n';
    }
    
    return rows;
}