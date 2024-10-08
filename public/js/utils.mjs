async function loadTemplate(path) {
    const res = await fetch(path);
    const template = await res.text();
    return template;
  }

export function renderWithTemplate(template, parentElement, data, callback, position = "afterbegin"){
    if (parentElement) {
      parentElement.insertAdjacentHTML(position, template);
      if (callback) {
        callback(data);
      }
    } else {
      console.error("Parent element is null or undefined.");
    }
  }

export async function loadHeaderFooter(){
    const headerTemplate = await loadTemplate("/partials/header.html");
    const headerElement = document.querySelector("#header");
    const footerTemplate = await loadTemplate('/partials/footer.html');
    const footerElement = document.querySelector("#footer");
  
    renderWithTemplate(headerTemplate, headerElement);
    renderWithTemplate(footerTemplate, footerElement);
  }

// Determine document type
export function getDocType(docid) {
  let proposedDocType = 'P';
  if (/F[0-9]{4}-[0-9]{1,2}/.test(docid)) {
    proposedDocType = 'F';
  }
  return proposedDocType;
}

  // get user value from config.json file
  export async function getUserValue() {
    const res = await fetch("../js/config.json");
    const data = await res.json();
    return data.user;
  }