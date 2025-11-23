# Urban Matter Test Suite

Comprehensive testing suite for security, performance, and accessibility.

## Test Files

### 1. Security Test (`security-test.html`)

Open this file in a browser to run automated security checks:

```bash
# Serve the site locally
python3 -m http.server 8000

# Navigate to:
http://localhost:8000/tests/security-test.html
```

Tests include:
- Content Security Policy validation
- XSS protection headers
- Clickjacking protection
- Input sanitization
- HTTPS protocol enforcement
- Inline event handler detection
- Form validation presence
- External script verification
- ARIA labels for accessibility
- Required meta tags

### 2. Performance Test (`performance-test.js`)

Run in browser console on the main site:

```javascript
// Load the performance test script
const script = document.createElement('script');
script.src = '/tests/performance-test.js';
document.head.appendChild(script);
```

Or copy/paste the contents into the browser console.

Tests include:
- Page load time
- DOM ready time
- CSS/JS file analysis
- Image optimization
- DOM node count
- Resource count
- First Contentful Paint
- Render-blocking resources
- Accessibility performance

### 3. Accessibility Tests

Run with pa11y-ci (requires Node.js):

```bash
npm install
npm run test:accessibility
```

### 4. HTML Validation

```bash
npm run lint:html
```

### 5. CSS Linting

```bash
npm run lint:css
```

## Manual Testing Checklist

### Security
- [ ] All forms validate and sanitize input
- [ ] No XSS vulnerabilities
- [ ] CSP headers properly configured
- [ ] HTTPS enforced (production)
- [ ] No exposed sensitive data in source
- [ ] No console errors or warnings

### Accessibility
- [ ] Keyboard navigation works throughout site
- [ ] All interactive elements are focusable
- [ ] Focus indicators visible
- [ ] Screen reader compatible
- [ ] ARIA labels on all interactive elements
- [ ] Proper heading hierarchy (h1 -> h2 -> h3)
- [ ] Alt text on all images
- [ ] Form labels associated with inputs
- [ ] Color contrast meets WCAG AA standards
- [ ] Reduced motion respected

### Responsive Design
- [ ] Mobile (320px - 480px)
- [ ] Tablet (768px - 1024px)
- [ ] Desktop (1280px+)
- [ ] Touch targets min 44x44px
- [ ] Text readable without zoom
- [ ] No horizontal scroll
- [ ] Images scale properly

### Performance
- [ ] Page loads in under 3 seconds
- [ ] First Contentful Paint under 1.8s
- [ ] No render-blocking resources
- [ ] CSS/JS minified (production)
- [ ] Images optimized
- [ ] Lazy loading implemented where appropriate
- [ ] No console errors

### Browser Compatibility
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari
- [ ] Mobile Chrome

## Automated Testing

Run all tests:

```bash
npm test
```

## Security Audit

Check for known vulnerabilities:

```bash
npm audit
```

## Reporting Issues

When reporting bugs or security issues, include:
1. Browser and version
2. Steps to reproduce
3. Expected vs actual behavior
4. Screenshots if applicable
5. Console errors

## Contributing

Before submitting changes:
1. Run all tests
2. Ensure no new console errors
3. Verify accessibility
4. Test on mobile devices
5. Check browser compatibility
