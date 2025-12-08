import { dropdownIn, fadeOut } from '../../animations.js';
import { DROPDOWN_DURATION } from '../../constants.js';

document.addEventListener('DOMContentLoaded', function () {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileDropdownToggles = document.querySelectorAll('.mobile-dropdown-toggle');

    if (!mobileMenu) {
        return;
    }

    // Close mobile menu with animation
    function closeMobileMenu() {
        fadeOut(
            mobileMenu,
            () => {
                mobileMenu.classList.add('hidden');
            },
            MOBILE_MENU_DURATION
        );

        // Switch icon to menu
        if (mobileMenuButton) {
            const icon = mobileMenuButton.querySelector(
                'span.material-symbols-outlined'
            );
            icon.textContent = 'menu';
        }
    }

    // Open mobile menu with animation
    function openMobileMenu() {
        mobileMenu.classList.remove('hidden');
        fadeIn(mobileMenu, MOBILE_MENU_DURATION);

        // Switch icon to close
        if (mobileMenuButton) {
            const icon = mobileMenuButton.querySelector(
                'span.material-symbols-outlined'
            );
            icon.textContent = 'close';
        }
    }

    // Toggle main mobile menu
    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', function () {
            const isOpen = !mobileMenu.classList.contains('hidden');

            if (isOpen) {
                closeMobileMenu();
            } else {
                openMobileMenu();
            }
        });
    }

    // Close all open mobile dropdowns except the specified one
    function closeOtherDropdowns(currentToggle) {
        mobileDropdownToggles.forEach((toggle) => {
            if (toggle !== currentToggle) {
                const content = toggle.nextElementSibling;
                const icon = toggle.querySelector('.material-symbols-outlined');

                if (!content.classList.contains('hidden')) {
                    animateDropdown(content, icon, false);
                }
            }
        });
    }

    // Initialize and toggle mobile dropdown submenus with animation
    mobileDropdownToggles.forEach((toggle) => {
        const content = toggle.nextElementSibling;
        const icon = toggle.querySelector('.material-symbols-outlined');

        // Set initial state
        gsap.set(content, { height: 0, opacity: 0 });

        toggle.addEventListener('click', () => {
            const isOpening = content.classList.contains('hidden');

            closeOtherDropdowns(toggle);
            animateDropdown(content, icon, isOpening);
        });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', function (event) {
        const isClickInsideMenu = mobileMenu.contains(event.target);
        const isClickOnButton =
            mobileMenuButton && mobileMenuButton.contains(event.target);

        if (
            !isClickInsideMenu &&
            !isClickOnButton &&
            !mobileMenu.classList.contains('hidden')
        ) {
            closeMobileMenu();
        }
    });
});
