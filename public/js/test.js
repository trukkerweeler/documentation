import { loadHeaderFooter, getDocType } from "./utils.mjs";
loadHeaderFooter();
const url = 'http://localhost:3000/sysdocs';
const url2 = 'http://localhost:3000/docsavail';

// Console log the value from the inputFile element
const inputElement = document.querySelector("#getfilename");

// inputElement.addEventListener("change", function(event) {
//     event.preventDefault();
//     console.log('clicked');
//     const fileInput = document.querySelector(".inputFile");
//     console.log(fileInput.files[0].name);
//     console.log(fileInput.files[0].size);
//     console.log(fileInput.files[0].type);
//     console.log(fileInput.files[0].lastModifiedDate);
//     // console.log the file path
//     console.log(fileInput.value);   
    
// });


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
            let docid = data.get(field);
            dataJson['DOCUMENT_TYPE'] = getDocType(docid);

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
