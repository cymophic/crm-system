import { RESEND_COOLDOWN_DURATION, DISABLED_BUTTON_CLASSES } from '../constants.js';

document.addEventListener('DOMContentLoaded', function () {
    const form = document
        .querySelector('form button[name="action_send"]')
        ?.closest('form');
    const resendButton = document.querySelector('button[name="action_send"]');

    if (!resendButton) return;

    // Constants
    const STORAGE_KEY = 'emailResent';

    // Button visibility management
    function hideResendButton() {
        resendButton.classList.add('hidden');
    }

    function showResendButton() {
        resendButton.classList.remove('hidden');
    }

    // Button state management
    function disableResendButton() {
        resendButton.disabled = true;
        resendButton.classList.add(...DISABLED_BUTTON_CLASSES);
    }

    function enableResendButton() {
        resendButton.disabled = false;
        resendButton.classList.remove(...DISABLED_BUTTON_CLASSES);
        resendButton.textContent = 'Verify';
    }

    // Check if selected email is verified
    function isSelectedEmailVerified() {
        const selectedRadio = document.querySelector('input[name="email"]:checked');
        if (!selectedRadio) return true; // Hide button if nothing selected

        const emailContainer = selectedRadio.closest('div');
        return emailContainer.querySelector('.bg-\\(--alert-success-bg\\)') !== null;
    }

    // Check if in cooldown period
    function isInCooldown() {
        return localStorage.getItem(STORAGE_KEY) !== null;
    }

    // Update button state based on current conditions
    function updateResendButtonState() {
        if (isSelectedEmailVerified()) {
            hideResendButton();
        } else {
            showResendButton();
            if (isInCooldown()) {
                disableResendButton();
            } else {
                enableResendButton();
            }
        }
    }

    // Countdown timer display
    function updateButtonText(timeLeft) {
        const minutes = Math.floor(timeLeft / 60000);
        const seconds = Math.floor((timeLeft % 60000) / 1000);
        resendButton.textContent = `Verify (${minutes}:${seconds.toString().padStart(2, '0')})`;
    }

    // Start cooldown countdown
    function startCooldown(timeLeft) {
        disableResendButton();
        updateButtonText(timeLeft);

        const interval = setInterval(() => {
            timeLeft -= 1000;

            if (timeLeft <= 0) {
                clearInterval(interval);
                localStorage.removeItem(STORAGE_KEY);
                updateResendButtonState();
            } else {
                updateButtonText(timeLeft);
            }
        }, 1000);
    }

    // Initialize
    function init() {
        // Set initial button state
        updateResendButtonState();

        // Check for existing cooldown
        const cooldownEnd = localStorage.getItem(STORAGE_KEY);
        if (cooldownEnd) {
            const timeLeft = parseInt(cooldownEnd) - Date.now();

            if (timeLeft > 0) {
                startCooldown(timeLeft);
            } else {
                localStorage.removeItem(STORAGE_KEY);
            }
        }

        // Handle form submission
        if (form) {
            form.addEventListener('submit', (e) => {
                if (e.submitter?.name === 'action_send') {
                    localStorage.setItem(
                        STORAGE_KEY,
                        Date.now() + RESEND_COOLDOWN_DURATION
                    );
                }
            });
        }

        // Listen for email selection changes
        document.querySelectorAll('input[name="email"]').forEach((radio) => {
            radio.addEventListener('change', updateResendButtonState);
        });
    }

    init();
});
