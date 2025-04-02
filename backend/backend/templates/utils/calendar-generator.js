import { config } from './config.js';

const headerRow = document.getElementById('month-numbers');
const tableBody = document.getElementById('tableBody');
const numRows = config.numRows;
const numMonths = config.numMonths;

// Add even numbered headers
function generateNumberOfMonths(numMonths) {
    numMonths = numMonths || 12;
    let n = 1;
    if (numMonths === 24) {
        n = 2;
    }

    for (let i = 0; i < 12; i++) {
        const th = document.createElement('th');
        th.textContent = (i + 1) * n;
        headerRow.appendChild(th);
    }
}

// Initialize with 24 months
generateNumberOfMonths(numMonths);

// Generate and insert rows
for (let i = 1; i <= numRows; i++) {
    const tr = document.createElement('tr');
    
    // Add description cell
    const tdDesc = document.createElement('td');
    tdDesc.textContent = `{{table_row${i}}}`;
    tr.appendChild(tdDesc);
    
    // Add 12 month cells
    for (let j = 0; j < 12; j++) {
        const td = document.createElement('td');
        tr.appendChild(td);
    }
    
    tableBody.appendChild(tr);
}