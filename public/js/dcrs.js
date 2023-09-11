import { loadHeaderFooter } from "./utils.mjs";
loadHeaderFooter();

const url = 'http://localhost:3000/requests';

function getRecords () {
    const main = document.querySelector('main');
    
    fetch(url, { method: 'GET' })

    .then(response => response.json())
    .then(records => {
        // console.log(records);
        const table = document.createElement('table');
            const thead = document.createElement('thead');
            const tbody = document.createElement('tbody');
            const header = document.createElement('tr');
            const td = document.createElement('td');
            
            for (let key in records[0]) {
                // if (fieldList.includes(key)){
                const th = document.createElement('th');
                th.textContent = key;
                header.appendChild(th);
                // }
            }
            thead.appendChild(header);

            for (let record of records) {
                const tr = document.createElement('tr');
                for (let key in record) {
                    const td = document.createElement('td');
                    switch (key) {
                        case 'DUE_DATE':
                            td.textContent = record[key].slice(0,10);
                            break;
                        case 'DECISION_DATE':
                            if (record[key] !== null) {
                                td.textContent = record[key].slice(0,10);
                            } else {
                                td.textContent = '';
                            }
                            break;
                        case 'REQUEST_DATE':
                            if (record[key] !== null) {
                                td.textContent = record[key].slice(0,10);
                            } else {
                                td.textContent = '';
                            }
                            break;
                        default:
                            td.textContent = record[key];
                    // tr.appendChild(td);
                }
                tr.appendChild(td);
            }
                tbody.appendChild(tr);
            }

            table.appendChild(thead);
            table.appendChild(tbody);
            main.appendChild(table);
    })
}

getRecords();