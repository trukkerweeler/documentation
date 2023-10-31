import { loadHeaderFooter } from "./utils.mjs";
loadHeaderFooter();

const button = document.querySelector('#changedetailsearch');
button.addEventListener('click', async (e) => {
    e.preventDefault();
    const id = document.getElementById('did')
    const did = id.value;
    const url = 'http://localhost:3000/history/' + did;
    // console.log(url);

    // Delete the child nodes of the main element
    while (main.firstChild) {
        main.removeChild(main.firstChild);
    }

    fetch (url, {method: 'GET'})

    .then(response => response.json())
    .then(data => {
        // console.log(data);
        let output = '<tr><th>Request ID</th><th>Request Date</th><th>Change Reason</th><th>Request Text</th><th>Closed Date</th></tr>';
        data.forEach(function (doc) {
            // print each field name and value
            for (let key in doc) {
                // if the last 4 of the key are _DATE, then slice the value to only show the date
                if (key.slice(-4) == 'DATE' && doc[key] != null) {
                    doc[key] = doc[key].slice(0, 10);
                } 
            }

            output += `
            <tr>
                <td>${doc.REQUEST_ID}</td>
                <td>${doc.REQUEST_DATE}</td>
                <td>${doc.CHANGE_REASON}</td>
                <td>${doc.REQUEST_TEXT}</td>
                <td>${doc.CLOSED_DATE}</td>
            </tr>
            `;
        });
        // document.getElementById('output').innerHTML = output;
        // document.getElementById('main').innerHTML = output;
        const main = document.querySelector('#main');
        const table = document.createElement('table');
        table.innerHTML = output;
        main.appendChild(table);
    })
});