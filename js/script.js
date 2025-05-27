// Basic script
console.log("Script loaded from js/script.js!");

// Add some more code to ensure the file is different
function placeholderFunction() {
    console.log("Placeholder function called from js/script.js");
}

document.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed from js/script.js');
    // Example: Add a class to the body after load
    // document.body.classList.add('js-loaded');
});

// More placeholder functions if needed
function anotherPlaceholder(message) {
    console.log("Another placeholder received: " + message);
}
