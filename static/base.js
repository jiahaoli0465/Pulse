document.addEventListener('DOMContentLoaded', function() {
    let flashDurationInSeconds = 5;
    let flashContainerId = 'flash-messages';

    function removeFlashMessages() {
        let flashContainer = document.getElementById(flashContainerId);
        if (flashContainer) {
            flashContainer.remove();
        }
    }

    setTimeout(removeFlashMessages, flashDurationInSeconds * 1000);
});

const profile = document.querySelector('#navProfile');
const menu = document.querySelector('#menu');
let menuTimeout;

profile.addEventListener('mouseover', () => {
    clearTimeout(menuTimeout);  // Clear any existing timeout
    menu.classList.remove('hidden');
});

profile.addEventListener('mouseleave', () => {
    // Start a timeout when leaving the profile link
    menuTimeout = setTimeout(() => {
        menu.classList.add('hidden');
    }, 300); // 300 milliseconds delay
});

menu.addEventListener('mouseover', () => {
    clearTimeout(menuTimeout);  // Cancel hiding when over the menu
});

menu.addEventListener('mouseleave', () => {
    // Hide the menu after leaving it
    menuTimeout = setTimeout(() => {
        menu.classList.add('hidden');
    }, 300);
});