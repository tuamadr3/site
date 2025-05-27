window.addEventListener('DOMContentLoaded', (event) => {
    const header = document.querySelector('header');
    const body = document.body;
    let stickyOffset = 0; // Will be set after header is fully rendered

    if (!header) {
        console.error('Sticky header: Header element not found.');
        return;
    }

    // Function to calculate and set stickyOffset
    // Needs to be callable on resize as well if header height might change
    function calculateStickyOffset() {
        // Temporarily remove sticky to get original offsetHeight if needed
        const wasSticky = header.classList.contains('sticky');
        if (wasSticky) {
            header.classList.remove('sticky');
            body.style.paddingTop = '0px'; // Reset padding for calculation
        }
        stickyOffset = header.offsetHeight;
        if (wasSticky) { // Re-apply if it was sticky before calculation
             // Check width again before re-applying
            if (window.innerWidth >= 769) {
                 header.classList.add('sticky');
                 body.style.paddingTop = stickyOffset + 'px';
            } else {
                // Ensure it's not sticky and padding is zero if now mobile
                header.classList.remove('sticky');
                body.style.paddingTop = '0px';
            }
        }
    }

    // Initial calculation
    // Use a small timeout to ensure header is fully rendered, especially if images affect height
    setTimeout(calculateStickyOffset, 100);


    function handleScroll() {
        if (window.innerWidth < 769) { // Tablet breakpoint
            if (header.classList.contains('sticky')) {
                header.classList.remove('sticky');
                body.style.paddingTop = '0px';
            }
            return; // Don't apply sticky logic on mobile/tablet
        }

        // Ensure stickyOffset is up-to-date (e.g. if images loaded late)
        // This might be excessive to call on every scroll, consider optimizing
        // For now, let's rely on initial and resize calculation mostly.
        // calculateStickyOffset(); // Re-evaluating this. Simpler to use the value from load/resize.

        if (window.pageYOffset > stickyOffset) {
            if (!header.classList.contains('sticky')) {
                header.classList.add('sticky');
                body.style.paddingTop = stickyOffset + 'px';
            }
        } else {
            if (header.classList.contains('sticky')) {
                header.classList.remove('sticky');
                body.style.paddingTop = '0px';
            }
        }
    }

    // Initial check
    handleScroll();

    window.onscroll = handleScroll;

    // Recalculate on resize, especially if header height might change due to responsive CSS
    let resizeTimeout;
    window.onresize = function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            calculateStickyOffset(); // Recalculate offset
            handleScroll(); // Re-apply logic based on new size / offset
        }, 250); // Debounce resize event
    };
});

// Smooth scrolling for same-page anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        // Check if the href is more than just "#"
        if (this.getAttribute('href').length > 1) {
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                e.preventDefault(); // Prevent default anchor click behavior
                
                // Adjust scroll position for sticky header
                let headerHeight = 0;
                const stickyHeader = document.querySelector('header.sticky');
                if (stickyHeader && window.innerWidth >= 769) { // Check if header is sticky and not on mobile
                    headerHeight = stickyHeader.offsetHeight;
                }

                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        }
    });
});
