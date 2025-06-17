// a.js - Handles menu toggle and responsive slick for profiles
$(function() {
    // Menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const menuContainer = document.querySelector('.container');
    menuToggle.addEventListener('click', () => {
        menuContainer.classList.toggle('expanded');
    });

    // Make the menu container follow the user's scrolling (fluid and mobile-friendly)
    function updateMenuPosition() {
        // Only apply on desktop (fixed menu), not on mobile where menu is overlay
        if (window.innerWidth < 768) {
            document.querySelector('.container').style.top = '0';
        } else {
            document.querySelector('.container').style.top = window.scrollY + 'px';
        }
    }
    window.addEventListener('scroll', updateMenuPosition);
    window.addEventListener('resize', updateMenuPosition);
    updateMenuPosition();
});
