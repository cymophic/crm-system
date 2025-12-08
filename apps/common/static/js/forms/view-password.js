document.addEventListener('DOMContentLoaded', () => {
    // Find all password toggle buttons on the page
    const toggleButtons = document.querySelectorAll('.password-toggle-button');

    // Add click handler to each toggle button
    toggleButtons.forEach((button) => {
        button.addEventListener('click', function () {
            togglePasswordVisibility(this);
        });
    });
});

function togglePasswordVisibility(button) {
    // Get the target input ID from button's data attribute
    const targetInputId = button.dataset.targetId;
    const passwordInput = document.getElementById(targetInputId);
    const toggleIcon = button.querySelector('span');

    // Exit if password input and toggleIcon doesn't exist
    if (!passwordInput || !toggleIcon) return;

    // Check current visibility state
    const isPasswordVisible = passwordInput.getAttribute('type') === 'text';

    // Toggle between 'password' and 'text' type
    const newType = isPasswordVisible ? 'password' : 'text';
    passwordInput.setAttribute('type', newType);

    // Update icon to match new state
    toggleIcon.textContent = isPasswordVisible ? 'visibility' : 'visibility_off';
}
