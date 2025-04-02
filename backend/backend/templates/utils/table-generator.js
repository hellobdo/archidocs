import { config } from './config.js';

const tableBody = document.getElementById('tableBody');
const totalRow = tableBody.querySelector('.total-row');
const numRows = config.numRows;

// Generate and insert rows
for (let i = 1; i <= numRows; i++) {
    const tr = document.createElement('tr');
    const td = document.createElement('td');
    td.textContent = `{{table_row${i}}}`;
    tr.appendChild(td);
    
    // Add the rowspan cells only for the first row
    if (i === 1) {
        const m2 = document.createElement('td');
        m2.setAttribute('rowspan', numRows);
        m2.textContent = 'm²';
        
        const qty = document.createElement('td');
        qty.setAttribute('rowspan', numRows);
        qty.textContent = '{{qty}}';
        
        const costPerUnit = document.createElement('td');
        costPerUnit.setAttribute('rowspan', numRows);
        costPerUnit.textContent = '{{cost_per_unit}}';
        
        const totalCost = document.createElement('td');
        totalCost.setAttribute('rowspan', numRows);
        totalCost.textContent = '{{total_cost}}';
        
        tr.append(m2, qty, costPerUnit, totalCost);
    }
    
    tableBody.insertBefore(tr, totalRow);
}