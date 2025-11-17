/**
 * Browser Compatibility Helper
 * Ensures cross-browser support for modern features
 */

(function() {
    'use strict';

    // Browser detection
    const BrowserDetector = {
        isIE: function() {
            return /MSIE|Trident/.test(navigator.userAgent);
        },
        isEdge: function() {
            return /Edg/.test(navigator.userAgent);
        },
        isFirefox: function() {
            return /Firefox/.test(navigator.userAgent);
        },
        isChrome: function() {
            return /Chrome/.test(navigator.userAgent) && !/Edg/.test(navigator.userAgent);
        },
        isSafari: function() {
            return /Safari/.test(navigator.userAgent) && !/Chrome/.test(navigator.userAgent);
        },
        isMobile: function() {
            return /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        }
    };

    // CSS Feature Detection and Polyfills
    const CSSPolyfills = {
        // Check for backdrop-filter support
        supportsBackdropFilter: function() {
            return CSS.supports('backdrop-filter', 'blur(10px)') || 
                   CSS.supports('-webkit-backdrop-filter', 'blur(10px)');
        },

        // Check for CSS Grid support
        supportsGrid: function() {
            return CSS.supports('display', 'grid');
        },

        // Check for Flexbox support
        supportsFlexbox: function() {
            return CSS.supports('display', 'flex');
        },

        // Apply fallbacks for unsupported features
        applyFallbacks: function() {
            // Backdrop filter fallback
            if (!this.supportsBackdropFilter()) {
                const elements = document.querySelectorAll('[style*="backdrop-filter"]');
                elements.forEach(el => {
                    el.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
                    el.style.border = '1px solid rgba(255, 255, 255, 0.2)';
                });
            }

            // Grid fallback
            if (!this.supportsGrid()) {
                const gridElements = document.querySelectorAll('[style*="display: grid"]');
                gridElements.forEach(el => {
                    el.style.display = 'flex';
                    el.style.flexWrap = 'wrap';
                });
            }
        }
    };

    // JavaScript Feature Detection
    const JSPolyfills = {
        // Check for ES6 features
        supportsES6: function() {
            try {
                new Function('(a = 0) => a');
                return true;
            } catch (e) {
                return false;
            }
        },

        // Check for fetch API
        supportsFetch: function() {
            return typeof fetch !== 'undefined';
        },

        // Check for Promise support
        supportsPromise: function() {
            return typeof Promise !== 'undefined';
        },

        // Apply polyfills
        applyPolyfills: function() {
            // Fetch polyfill for older browsers
            if (!this.supportsFetch()) {
                this.loadPolyfill('https://cdn.jsdelivr.net/npm/whatwg-fetch@3.6.2/dist/fetch.umd.js');
            }

            // Promise polyfill for IE
            if (!this.supportsPromise()) {
                this.loadPolyfill('https://cdn.jsdelivr.net/npm/es6-promise@4.2.8/dist/es6-promise.auto.min.js');
            }
        },

        loadPolyfill: function(url) {
            const script = document.createElement('script');
            script.src = url;
            script.async = true;
            document.head.appendChild(script);
        }
    };

    // Performance optimization for older browsers
    const PerformanceOptimizer = {
        // Reduce animations for older browsers
        optimizeAnimations: function() {
            if (BrowserDetector.isIE() || BrowserDetector.isMobile()) {
                const style = document.createElement('style');
                style.textContent = `
                    *, *::before, *::after {
                        animation-duration: 0.01ms !important;
                        animation-iteration-count: 1 !important;
                        transition-duration: 0.01ms !important;
                    }
                `;
                document.head.appendChild(style);
            }
        },

        // Optimize images for mobile
        optimizeImages: function() {
            if (BrowserDetector.isMobile()) {
                const images = document.querySelectorAll('img');
                images.forEach(img => {
                    if (!img.hasAttribute('loading')) {
                        img.setAttribute('loading', 'lazy');
                    }
                });
            }
        }
    };

    // Error handling for cross-browser compatibility
    const ErrorHandler = {
        init: function() {
            window.addEventListener('error', function(e) {
                console.warn('Browser compatibility issue:', e.message);
                
                // Try to recover from common issues
                if (e.message.includes('backdrop-filter')) {
                    CSSPolyfills.applyFallbacks();
                }
            });

            // Handle unhandled promise rejections
            window.addEventListener('unhandledrejection', function(e) {
                console.warn('Unhandled promise rejection:', e.reason);
            });
        }
    };

    // Initialize compatibility features when DOM is ready
    function initCompatibility() {
        // Apply CSS fallbacks
        CSSPolyfills.applyFallbacks();
        
        // Apply JavaScript polyfills
        JSPolyfills.applyPolyfills();
        
        // Optimize performance
        PerformanceOptimizer.optimizeAnimations();
        PerformanceOptimizer.optimizeImages();
        
        // Initialize error handling
        ErrorHandler.init();
        
        // Add browser-specific classes to body
        const body = document.body;
        if (BrowserDetector.isIE()) body.classList.add('browser-ie');
        if (BrowserDetector.isEdge()) body.classList.add('browser-edge');
        if (BrowserDetector.isFirefox()) body.classList.add('browser-firefox');
        if (BrowserDetector.isChrome()) body.classList.add('browser-chrome');
        if (BrowserDetector.isSafari()) body.classList.add('browser-safari');
        if (BrowserDetector.isMobile()) body.classList.add('browser-mobile');
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCompatibility);
    } else {
        initCompatibility();
    }

    // Export for global access
    window.BrowserCompatibility = {
        BrowserDetector: BrowserDetector,
        CSSPolyfills: CSSPolyfills,
        JSPolyfills: JSPolyfills,
        PerformanceOptimizer: PerformanceOptimizer
    };

})();
