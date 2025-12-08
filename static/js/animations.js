import {
    FADE_DURATION,
    FADE_OUT_DURATION,
    DROPDOWN_DURATION,
    MOBILE_DROPDOWN_DURATION,
    MOBILE_DROPDOWN_ICON_DURATION,
} from './constants.js';

export function fadeIn(element, duration = FADE_DURATION) {
    gsap.fromTo(
        element,
        { opacity: 0, y: -20 },
        { opacity: 1, y: 0, duration, ease: 'power2.inOut' }
    );
}

export function fadeOut(element, onComplete, duration = FADE_OUT_DURATION) {
    gsap.fromTo(
        element,
        { opacity: 1, y: 0 },
        {
            opacity: 0,
            y: -20,
            duration,
            ease: 'power4.inOut',
            onComplete: () => {
                if (onComplete) onComplete();
            },
        }
    );
}

export function dropdownIn(element, duration = DROPDOWN_DURATION) {
    gsap.fromTo(
        element,
        { opacity: 0, y: -10 },
        { opacity: 1, y: 0, duration, ease: 'power2.out' }
    );
}

export function animateDropdown(content, icon, isOpening) {
    if (isOpening) {
        content.classList.remove('hidden');
        gsap.to(content, {
            height: 'auto',
            opacity: 1,
            duration: MOBILE_DROPDOWN_DURATION,
        });
        gsap.to(icon, {
            rotation: 180,
            duration: MOBILE_DROPDOWN_ICON_DURATION,
        });
    } else {
        gsap.to(content, {
            height: 0,
            opacity: 0,
            duration: MOBILE_DROPDOWN_DURATION,
            onComplete: () => {
                content.classList.add('hidden');
            },
        });
        gsap.to(icon, {
            rotation: 0,
            duration: MOBILE_DROPDOWN_ICON_DURATION,
        });
    }
}
