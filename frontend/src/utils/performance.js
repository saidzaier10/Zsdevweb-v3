/**
 * Performance Utilities
 * Helpers for optimizing application performance
 */

// Check if device is low-end to disable heavy animations
export const isLowEndDevice = () => {
    const hardwareConcurrency = navigator.hardwareConcurrency || 4
    const deviceMemory = navigator.deviceMemory || 4
    return hardwareConcurrency <= 4 || deviceMemory <= 4
}

// Debounce function for scroll/resize events
export const debounce = (fn, delay) => {
    let timeoutId
    return (...args) => {
        clearTimeout(timeoutId)
        timeoutId = setTimeout(() => fn(...args), delay)
    }
}

// Throttle function for scroll events
export const throttle = (fn, limit) => {
    let inThrottle
    return (...args) => {
        if (!inThrottle) {
            fn(...args)
            inThrottle = true
            setTimeout(() => (inThrottle = false), limit)
        }
    }
}

// Lazy load images directive
export const vLazyLoad = {
    mounted: (el) => {
        const loadImage = () => {
            const imageElement = Array.from(el.children).find(
                (el) => el.nodeName === "IMG"
            );
            if (imageElement) {
                imageElement.addEventListener("load", () => {
                    setTimeout(() => el.classList.add("loaded"), 100);
                });
                imageElement.addEventListener("error", () => console.log("error"));
                imageElement.src = imageElement.dataset.url;
            }
        };

        const handleIntersect = (entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    loadImage();
                    observer.unobserve(el);
                }
            });
        };

        const createObserver = () => {
            const options = {
                root: null,
                threshold: 0,
            };
            const observer = new IntersectionObserver(handleIntersect, options);
            observer.observe(el);
        };

        if (window["IntersectionObserver"]) {
            createObserver();
        } else {
            loadImage();
        }
    },
};
