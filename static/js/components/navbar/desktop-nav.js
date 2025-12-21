import { dropdownIn, fadeOut } from '../../animations.js';
import { DROPDOWN_DURATION } from '../../constants.js';

document.addEventListener('DOMContentLoaded', function () {
    // Function to close all dropdowns
    function closeAllDropdowns() {
        const allDropdowns = document.querySelectorAll('[data-dropdown-menu]');
        allDropdowns.forEach((dropdown) => {
            if (!dropdown.classList.contains('hidden')) {
                fadeOut(
                    dropdown,
                    () => {
                        dropdown.classList.add('hidden');
                    },
                    DROPDOWN_DURATION
                );
            }
        });
    }

    // Function to toggle a specific dropdown
    function toggleDropdown(menuId) {
        const targetMenu = document.getElementById(menuId);
        if (!targetMenu) return;

        const isCurrentlyHidden = targetMenu.classList.contains('hidden');

        // Close all dropdowns first
        closeAllDropdowns();

        // If the target menu was hidden, show it
        if (isCurrentlyHidden) {
            targetMenu.classList.remove('hidden');
            dropdownIn(targetMenu);
        }
    }

    // Add click event listeners to all dropdown triggers
    document.addEventListener('click', function (event) {
        const trigger = event.target.closest('[data-dropdown-trigger]');

        if (trigger) {
            event.preventDefault();
            const targetMenuId = trigger.getAttribute('data-dropdown-trigger');
            toggleDropdown(targetMenuId);
            return;
        }

        // Close menus when clicking outside any dropdown container
        const isOutsideClick = !event.target.closest('.relative');
        if (isOutsideClick) {
            closeAllDropdowns();
        }
    });
});
