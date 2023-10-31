import { loadHeaderFooter } from "./utils.mjs";
loadHeaderFooter();
const url = 'http://localhost:3000/sysdocs';
const url2 = 'http://localhost:3000/docsavail';

// Send POST request to server
const form = document.querySelector('form');
form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const requestDate = new Date();
    requestDate.setDate(requestDate.getDate())
    let createDate = requestDate.toISOString().slice(0, 19).replace('T', ' ');

    const dataJson = {
        CREATE_DATE: createDate,
        CREATE_BY: 'TKENT',
        AUDIT_RESPONSIBLE: 'I',
        CHECKED_OUT: 'N',
    };
    for (let field of data.keys()) {
        if (field == 'document_id') {
            dataJson[field] = data.get(field);
            let docid = data.get(field)
            const re = new RegExp('[F]#{4}');

            if (re.test(docid)) {
                dataJson['DOCUMENT_TYPE'] = 'F';
            } else {
                    dataJson['DOCUMENT_TYPE'] = 'P';
                }
        } else {
            dataJson[field] = data.get(field);
        }
    }
    console.log(dataJson);

    try {
        await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                },
            body: JSON.stringify(dataJson)
        });
        console.log('Success:', JSON.stringify(dataJson));
        }
        catch (err) {
            console.log('Error:', err);
        }
    
    try {
        await fetch(url2, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                },
            body: JSON.stringify(dataJson)
        });
        console.log('Success:', JSON.stringify(dataJson));
        }
        catch (err) {
            console.log('Error:', err);
        }
    

    form.reset();
});
