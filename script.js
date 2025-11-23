/**
 * Urban Matter - Main JavaScript
 * Security-hardened, accessible, and performant
 */

(function() {
    'use strict';

    // ================================
    // Utility Functions
    // ================================

    /**
     * Sanitize user input to prevent XSS attacks
     * @param {string} str - Input string to sanitize
     * @returns {string} Sanitized string
     */
    function sanitizeInput(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    /**
     * Debounce function to limit function calls
     * @param {Function} func - Function to debounce
     * @param {number} wait - Wait time in milliseconds
     * @returns {Function} Debounced function
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Check if element is in viewport
     * @param {HTMLElement} el - Element to check
     * @returns {boolean} Whether element is in viewport
     */
    function isInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // ================================
    // Mobile Navigation
    // ================================

    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-menu a');

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
            menuToggle.setAttribute('aria-expanded', !isExpanded);
            navMenu.classList.toggle('active');
        });

        // Close menu when clicking a link
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                menuToggle.setAttribute('aria-expanded', 'false');
                navMenu.classList.remove('active');
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!menuToggle.contains(e.target) && !navMenu.contains(e.target)) {
                menuToggle.setAttribute('aria-expanded', 'false');
                navMenu.classList.remove('active');
            }
        });

        // Close menu on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navMenu.classList.contains('active')) {
                menuToggle.setAttribute('aria-expanded', 'false');
                navMenu.classList.remove('active');
                menuToggle.focus();
            }
        });
    }

    // ================================
    // Enhanced Header with Scroll Effects
    // ================================

    const header = document.querySelector('.site-header');
    let lastScrollTop = 0;
    const scrollThreshold = 100;

    const handleScroll = debounce(() => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        // Add 'scrolled' class for enhanced styling
        if (scrollTop > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }

        // Hide on scroll down, show on scroll up
        if (scrollTop > lastScrollTop && scrollTop > scrollThreshold) {
            header.classList.add('hidden');
        } else {
            header.classList.remove('hidden');
        }

        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    }, 100);

    window.addEventListener('scroll', handleScroll, { passive: true });

    // ================================
    // Scroll-Based Animations (Tender Food style)
    // ================================

    const animatedElements = document.querySelectorAll('.preFade, .preScale, .preSlide, .preSlideLeft, .preSlideRight');

    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                // Only animate once
                animationObserver.unobserve(entry.target);
            }
        });
    }, {
        root: null,
        rootMargin: '0px 0px -100px 0px', // Trigger slightly before element enters viewport
        threshold: 0.1
    });

    animatedElements.forEach(el => {
        animationObserver.observe(el);
    });

    // ================================
    // Smooth Scrolling for Anchor Links
    // ================================

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');

            // Ignore empty hrefs and non-id hrefs
            if (href === '#' || !href.startsWith('#')) return;

            const targetId = href.substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                e.preventDefault();

                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });

                // Update focus for accessibility
                targetElement.setAttribute('tabindex', '-1');
                targetElement.focus();
                targetElement.removeAttribute('tabindex');
            }
        });
    });

    // ================================
    // Animated Counter for Stats
    // ================================

    const statNumbers = document.querySelectorAll('.stat-number');
    let hasAnimated = false;

    function animateCounter(element, target, duration = 2000) {
        const start = 0;
        const increment = target / (duration / 16); // 60 FPS
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 16);
    }

    function handleStatsAnimation() {
        const impactSection = document.querySelector('.impact-section');
        if (!impactSection || hasAnimated) return;

        if (isInViewport(impactSection)) {
            hasAnimated = true;
            statNumbers.forEach(stat => {
                const target = parseInt(stat.getAttribute('data-target'), 10);
                if (!isNaN(target)) {
                    animateCounter(stat, target);
                }
            });
        }
    }

    // Use Intersection Observer for better performance
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.3
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !hasAnimated) {
                hasAnimated = true;
                statNumbers.forEach(stat => {
                    const target = parseInt(stat.getAttribute('data-target'), 10);
                    if (!isNaN(target)) {
                        animateCounter(stat, target);
                    }
                });
            }
        });
    }, observerOptions);

    const impactSection = document.querySelector('.impact-section');
    if (impactSection) {
        observer.observe(impactSection);
    }

    // ================================
    // Form Validation and Submission
    // ================================

    const contactForm = document.getElementById('contact-form');

    if (contactForm) {
        const nameInput = contactForm.querySelector('#name');
        const emailInput = contactForm.querySelector('#email');
        const messageInput = contactForm.querySelector('#message');
        const submitButton = contactForm.querySelector('.submit-button');
        const successMessage = contactForm.querySelector('.form-success');

        /**
         * Validate email format
         * @param {string} email - Email to validate
         * @returns {boolean} Whether email is valid
         */
        function validateEmail(email) {
            const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return re.test(email);
        }

        /**
         * Show error message for a field
         * @param {HTMLElement} input - Input element
         * @param {string} message - Error message
         */
        function showError(input, message) {
            const formGroup = input.closest('.form-group');
            const errorMessage = formGroup.querySelector('.error-message');

            input.classList.add('error');
            input.setAttribute('aria-invalid', 'true');

            if (errorMessage) {
                errorMessage.textContent = sanitizeInput(message);
                errorMessage.classList.add('visible');
            }
        }

        /**
         * Clear error message for a field
         * @param {HTMLElement} input - Input element
         */
        function clearError(input) {
            const formGroup = input.closest('.form-group');
            const errorMessage = formGroup.querySelector('.error-message');

            input.classList.remove('error');
            input.setAttribute('aria-invalid', 'false');

            if (errorMessage) {
                errorMessage.textContent = '';
                errorMessage.classList.remove('visible');
            }
        }

        /**
         * Validate single field
         * @param {HTMLElement} input - Input element
         * @returns {boolean} Whether field is valid
         */
        function validateField(input) {
            const value = input.value.trim();
            clearError(input);

            if (!value) {
                showError(input, 'This field is required');
                return false;
            }

            if (input.type === 'email' && !validateEmail(value)) {
                showError(input, 'Please enter a valid email address');
                return false;
            }

            if (input.name === 'message' && value.length < 10) {
                showError(input, 'Message must be at least 10 characters');
                return false;
            }

            return true;
        }

        // Real-time validation
        [nameInput, emailInput, messageInput].forEach(input => {
            if (input) {
                input.addEventListener('blur', () => validateField(input));
                input.addEventListener('input', () => {
                    if (input.classList.contains('error')) {
                        validateField(input);
                    }
                });
            }
        });

        // Form submission
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Validate all fields
            const isNameValid = validateField(nameInput);
            const isEmailValid = validateField(emailInput);
            const isMessageValid = validateField(messageInput);

            if (!isNameValid || !isEmailValid || !isMessageValid) {
                // Focus first invalid field
                const firstInvalid = contactForm.querySelector('.error');
                if (firstInvalid) {
                    firstInvalid.focus();
                }
                return;
            }

            // Sanitize inputs
            const formData = {
                name: sanitizeInput(nameInput.value.trim()),
                email: sanitizeInput(emailInput.value.trim()),
                message: sanitizeInput(messageInput.value.trim())
            };

            // Disable submit button
            submitButton.disabled = true;
            submitButton.textContent = 'Sending...';

            try {
                // Simulate form submission (replace with actual API call)
                await new Promise(resolve => setTimeout(resolve, 1500));

                // Log form data (in production, send to server)
                console.log('Form submitted:', formData);

                // Show success message
                successMessage.textContent = 'Thank you! Your message has been sent successfully.';
                successMessage.classList.add('visible');

                // Reset form
                contactForm.reset();

                // Hide success message after 5 seconds
                setTimeout(() => {
                    successMessage.classList.remove('visible');
                }, 5000);

            } catch (error) {
                console.error('Form submission error:', error);
                successMessage.textContent = 'Sorry, something went wrong. Please try again.';
                successMessage.classList.add('visible');
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = 'Send Message';
            }
        });
    }

    // ================================
    // Update Copyright Year
    // ================================

    const yearElement = document.getElementById('current-year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }

    // ================================
    // Keyboard Navigation Enhancement
    // ================================

    // Add keyboard navigation for project cards
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                card.click();
            }
        });
    });

    // ================================
    // Performance Optimization
    // ================================

    // Lazy load visual elements when they come into view
    const visualElements = document.querySelectorAll('.visual-element, .animated-circle');

    const lazyObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.willChange = 'transform, opacity';
                lazyObserver.unobserve(entry.target);
            }
        });
    }, {
        rootMargin: '50px'
    });

    visualElements.forEach(el => lazyObserver.observe(el));

    // ================================
    // Security: Prevent Console Tampering
    // ================================

    // Freeze critical DOM elements to prevent tampering
    if (Object.freeze) {
        Object.freeze(document.querySelector('.site-header'));
    }

    // ================================
    // Accessibility: Announce Page Load
    // ================================

    // Create a live region for screen readers
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('role', 'status');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    liveRegion.style.cssText = 'position: absolute; left: -10000px; width: 1px; height: 1px; overflow: hidden;';
    document.body.appendChild(liveRegion);

    // Announce page ready
    window.addEventListener('load', () => {
        liveRegion.textContent = 'Urban Matter website loaded. Navigate using tab key or screen reader shortcuts.';
    });

    // ================================
    // Error Handling
    // ================================

    window.addEventListener('error', (e) => {
        console.error('JavaScript error:', e.error);
        // In production, you might want to send this to an error tracking service
    });

    window.addEventListener('unhandledrejection', (e) => {
        console.error('Unhandled promise rejection:', e.reason);
        // In production, you might want to send this to an error tracking service
    });

    // ================================
    // Console Warning
    // ================================

    console.log('%cStop!', 'color: red; font-size: 40px; font-weight: bold;');
    console.log('%cThis is a browser feature intended for developers.', 'font-size: 16px;');
    console.log('%cIf someone told you to copy-paste something here, it is a scam.', 'font-size: 16px;');

})();
