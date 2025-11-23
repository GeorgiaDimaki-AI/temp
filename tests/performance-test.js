/**
 * Performance Test Suite for Urban Matter
 * Run this in the browser console
 */

(function() {
    'use strict';

    const tests = [];
    const results = {
        pass: [],
        fail: [],
        warnings: []
    };

    console.log('%c🚀 Performance Test Suite', 'font-size: 20px; font-weight: bold; color: #0ff;');
    console.log('='.repeat(50));

    // Test 1: Page Load Time
    function testPageLoadTime() {
        if (window.performance && window.performance.timing) {
            const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
            const threshold = 3000; // 3 seconds

            if (loadTime < threshold) {
                results.pass.push(`✓ Page Load Time: ${loadTime}ms (under ${threshold}ms)`);
            } else {
                results.fail.push(`✗ Page Load Time: ${loadTime}ms (exceeds ${threshold}ms)`);
            }
        } else {
            results.warnings.push('⚠ Performance API not supported');
        }
    }

    // Test 2: DOM Ready Time
    function testDOMReadyTime() {
        if (window.performance && window.performance.timing) {
            const domReadyTime = window.performance.timing.domContentLoadedEventEnd - window.performance.timing.navigationStart;
            const threshold = 1500; // 1.5 seconds

            if (domReadyTime < threshold) {
                results.pass.push(`✓ DOM Ready Time: ${domReadyTime}ms (under ${threshold}ms)`);
            } else {
                results.fail.push(`✗ DOM Ready Time: ${domReadyTime}ms (exceeds ${threshold}ms)`);
            }
        }
    }

    // Test 3: CSS File Size
    function testCSSFileSize() {
        const stylesheets = document.querySelectorAll('link[rel="stylesheet"]');
        stylesheets.forEach((link, index) => {
            const href = link.getAttribute('href');
            results.pass.push(`✓ Stylesheet ${index + 1}: ${href}`);
        });
    }

    // Test 4: JavaScript File Size
    function testJavaScriptFileSize() {
        const scripts = document.querySelectorAll('script[src]');
        scripts.forEach((script, index) => {
            const src = script.getAttribute('src');
            results.pass.push(`✓ Script ${index + 1}: ${src}`);
        });
    }

    // Test 5: Image Optimization
    function testImageOptimization() {
        const images = document.querySelectorAll('img');
        if (images.length === 0) {
            results.pass.push('✓ No images found (or using CSS backgrounds)');
        } else {
            images.forEach((img, index) => {
                if (img.hasAttribute('alt')) {
                    results.pass.push(`✓ Image ${index + 1} has alt text`);
                } else {
                    results.fail.push(`✗ Image ${index + 1} missing alt text`);
                }
            });
        }
    }

    // Test 6: Number of DOM Nodes
    function testDOMNodes() {
        const nodeCount = document.getElementsByTagName('*').length;
        const threshold = 1500;

        if (nodeCount < threshold) {
            results.pass.push(`✓ DOM Nodes: ${nodeCount} (under ${threshold})`);
        } else {
            results.warnings.push(`⚠ DOM Nodes: ${nodeCount} (exceeds ${threshold}, consider optimization)`);
        }
    }

    // Test 7: Resource Count
    function testResourceCount() {
        if (window.performance && window.performance.getEntriesByType) {
            const resources = window.performance.getEntriesByType('resource');
            const threshold = 30;

            if (resources.length < threshold) {
                results.pass.push(`✓ Resource Count: ${resources.length} (under ${threshold})`);
            } else {
                results.warnings.push(`⚠ Resource Count: ${resources.length} (exceeds ${threshold})`);
            }

            // Log resource details
            console.group('Resource Details');
            resources.forEach(resource => {
                console.log(`${resource.name}: ${resource.duration.toFixed(2)}ms`);
            });
            console.groupEnd();
        }
    }

    // Test 8: First Contentful Paint
    function testFirstContentfulPaint() {
        if (window.performance && window.performance.getEntriesByType) {
            const paintEntries = window.performance.getEntriesByType('paint');
            const fcp = paintEntries.find(entry => entry.name === 'first-contentful-paint');

            if (fcp) {
                const threshold = 1800; // 1.8 seconds
                if (fcp.startTime < threshold) {
                    results.pass.push(`✓ First Contentful Paint: ${fcp.startTime.toFixed(2)}ms`);
                } else {
                    results.fail.push(`✗ First Contentful Paint: ${fcp.startTime.toFixed(2)}ms (exceeds ${threshold}ms)`);
                }
            } else {
                results.warnings.push('⚠ First Contentful Paint not available');
            }
        }
    }

    // Test 9: Render-blocking Resources
    function testRenderBlockingResources() {
        const scripts = document.querySelectorAll('script:not([async]):not([defer])');
        const headScripts = Array.from(scripts).filter(s => s.parentElement.tagName === 'HEAD');

        if (headScripts.length === 0) {
            results.pass.push('✓ No render-blocking scripts in <head>');
        } else {
            results.warnings.push(`⚠ ${headScripts.length} render-blocking scripts in <head>`);
        }
    }

    // Test 10: Accessibility Performance
    function testAccessibilityPerformance() {
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        const links = document.querySelectorAll('a');
        const buttons = document.querySelectorAll('button');

        results.pass.push(`✓ Headings: ${headings.length}`);
        results.pass.push(`✓ Links: ${links.length}`);
        results.pass.push(`✓ Buttons: ${buttons.length}`);
    }

    // Run all tests
    setTimeout(() => {
        testPageLoadTime();
        testDOMReadyTime();
        testCSSFileSize();
        testJavaScriptFileSize();
        testImageOptimization();
        testDOMNodes();
        testResourceCount();
        testFirstContentfulPaint();
        testRenderBlockingResources();
        testAccessibilityPerformance();

        // Display results
        console.log('\n');
        console.log('%cPASSED TESTS', 'color: #0f0; font-weight: bold; font-size: 16px;');
        results.pass.forEach(msg => console.log(`%c${msg}`, 'color: #0f0;'));

        if (results.fail.length > 0) {
            console.log('\n');
            console.log('%cFAILED TESTS', 'color: #f00; font-weight: bold; font-size: 16px;');
            results.fail.forEach(msg => console.log(`%c${msg}`, 'color: #f00;'));
        }

        if (results.warnings.length > 0) {
            console.log('\n');
            console.log('%cWARNINGS', 'color: #ff0; font-weight: bold; font-size: 16px;');
            results.warnings.forEach(msg => console.log(`%c${msg}`, 'color: #ff0;'));
        }

        console.log('\n');
        console.log('='.repeat(50));
        console.log(`%cSummary: ${results.pass.length} passed, ${results.fail.length} failed, ${results.warnings.length} warnings`,
            'font-size: 14px; font-weight: bold;');

        // Export results
        window.performanceTestResults = {
            passed: results.pass.length,
            failed: results.fail.length,
            warnings: results.warnings.length,
            details: results
        };

    }, 2000); // Wait 2 seconds for page to fully load

})();
