import { loadHeaderFooter } from './utils.mjs';
// loadHeaderFooter();

// append the button ncm with an anchor to ncms.html
const ncmButton = document.querySelector('#documents');
ncmButton.addEventListener('click', () => {
  window.location.href = 'documents.html';
});