import { fadeIn, fadeOut } from '../../animations.js';
import { AUTO_HIDE_DELAY } from '../../constants.js';

function animateToasts() {
    // Find all toast messages on the page
    const toasts = document.querySelectorAll('[role="alert"]');

    toasts.forEach((toast) => {
        // Remove initial hidden state classes (set in HTML for smooth entry)
        toast.classList.remove('opacity-0', '-translate-y-5');

        // Animate toast entrance
        fadeIn(toast);

        // Schedule toast removal after delay
        setTimeout(() => {
            // Animate toast exit, then remove from DOM
            fadeOut(toast, () => {
                toast.remove();
            });
        }, AUTO_HIDE_DELAY);
    });
}

// Run on initial page load
document.addEventListener('DOMContentLoaded', animateToasts);

// Run after form submissions (handles browser back/forward cache)
window.addEventListener('pageshow', animateToasts);
