const darkModeToggled = window.matchMedia('(prefers-color-scheme: dark)');

// Update the favicon based on user's light/dark mode preference
function updateFavicon() {
    const favicon = document.getElementById('favicon');
    const isDark = darkModeToggled.matches;

    const lightIcon = '/static/favicons/favicon-light.ico';
    const darkIcon = '/static/favicons/favicon-dark.ico';

    favicon.href = isDark ? darkIcon : lightIcon;
}

// Run when page first loads
document.addEventListener('DOMContentLoaded', updateFavicon);

// Then run whenever user changes their system theme
darkModeToggled.addEventListener('change', updateFavicon);
