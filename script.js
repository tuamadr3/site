const hamburgerMenu = document.querySelector('.hamburger-menu');
const navLinks = document.getElementById('nav-links');

hamburgerMenu.addEventListener('click', () => {
    navLinks.classList.toggle('nav-active');
    const isExpanded = navLinks.classList.contains('nav-active');
    hamburgerMenu.setAttribute('aria-expanded', isExpanded);
});
