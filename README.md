# Urban Matter

A modern, secure, and accessible website for sustainable architecture and urban design.

## 🎯 Project Overview

Urban Matter showcases sustainable architecture and design with a focus on:
- Modern, responsive design
- Security-first implementation
- Full accessibility (WCAG 2.1 AA compliant)
- Performance optimized
- Production-ready code

## ✨ Features

### Design
- Dark theme with vibrant gradient accents
- Smooth animations and micro-interactions
- Responsive grid layouts (mobile-first)
- Typography scale with fluid sizing
- Reduced motion support for accessibility

### Security
- Content Security Policy (CSP)
- XSS protection headers
- Input sanitization
- HTTPS enforcement
- No external dependencies
- Security headers configured

### Accessibility
- WCAG 2.1 AA compliant
- Keyboard navigation support
- Screen reader optimized
- ARIA labels throughout
- Focus indicators
- Skip to main content link
- Semantic HTML5 structure

### Performance
- Minimal dependencies
- Optimized CSS Grid/Flexbox
- Debounced scroll handlers
- Intersection Observer API
- Lazy loading considerations
- Browser caching configured

## 🚀 Quick Start

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd urban-matter
```

2. Serve locally:
```bash
python3 -m http.server 8000
# or
npx serve
```

3. Open browser:
```
http://localhost:8000
```

### Production Deployment

#### Apache

1. Upload all files to web root
2. Ensure `.htaccess` is in place
3. Configure SSL certificate
4. Enable required Apache modules:
```bash
sudo a2enmod headers
sudo a2enmod deflate
sudo a2enmod expires
sudo a2enmod rewrite
```

#### Nginx

1. Copy `nginx.conf` to your Nginx configuration
2. Update paths and domain names
3. Configure SSL certificate
4. Reload Nginx:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

## 📁 Project Structure

```
urban-matter/
├── index.html              # Main HTML file
├── styles.css             # Stylesheet
├── script.js              # JavaScript functionality
├── package.json           # Project configuration
├── .htaccess             # Apache security headers
├── nginx.conf            # Nginx configuration
├── .htmlhintrc           # HTML linting rules
├── .pa11yci.json         # Accessibility test config
├── SECURITY.md           # Security policy
├── README.md             # This file
└── tests/
    ├── security-test.html    # Security test suite
    ├── performance-test.js   # Performance tests
    └── README.md             # Testing documentation
```

## 🧪 Testing

### Run All Tests
```bash
npm install
npm test
```

### Individual Tests

**Accessibility:**
```bash
npm run test:accessibility
```

**HTML Validation:**
```bash
npm run lint:html
```

**Security Tests:**
Open `tests/security-test.html` in browser

**Performance Tests:**
Run `tests/performance-test.js` in browser console

## 🔒 Security

See [SECURITY.md](SECURITY.md) for:
- Security features
- Vulnerability reporting
- Best practices
- Production checklist

## ♿ Accessibility

Features for all users:
- Keyboard navigation (Tab, Enter, Escape)
- Screen reader support (tested with NVDA/JAWS)
- Focus indicators on all interactive elements
- Skip to main content link
- ARIA labels and roles
- Semantic HTML structure
- Color contrast meets WCAG AA
- Respects `prefers-reduced-motion`

### Keyboard Shortcuts
- `Tab` - Navigate forward
- `Shift + Tab` - Navigate backward
- `Enter` - Activate links/buttons
- `Escape` - Close mobile menu

## 🎨 Design System

### Colors
```css
--color-bg-primary: #0a0a0a      /* Main background */
--color-bg-secondary: #1a1a1a    /* Section backgrounds */
--color-accent-primary: #ff6b6b  /* Red/pink accent */
--color-accent-secondary: #ffd93d /* Yellow accent */
--color-accent-tertiary: #6bcf7f  /* Green accent */
```

### Typography
- Primary Font: System font stack
- Heading Font: Helvetica Neue, Arial
- Fluid sizing using clamp()

### Spacing Scale
```css
--space-xs: 0.5rem   /* 8px */
--space-sm: 1rem     /* 16px */
--space-md: 1.5rem   /* 24px */
--space-lg: 2rem     /* 32px */
--space-xl: 3rem     /* 48px */
--space-2xl: 4rem    /* 64px */
--space-3xl: 6rem    /* 96px */
```

## 📱 Responsive Breakpoints

```css
/* Mobile: < 768px (default) */
/* Tablet: 768px - 1024px */
/* Desktop: > 1024px */
```

## ⚡ Performance Targets

- Page Load: < 3 seconds
- First Contentful Paint: < 1.8 seconds
- Time to Interactive: < 3.5 seconds
- DOM Nodes: < 1500
- Total Resources: < 30

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🛠️ Technologies

- HTML5
- CSS3 (Grid, Flexbox, Custom Properties)
- Vanilla JavaScript (ES6+)
- No frameworks or libraries

## 📄 License

MIT License - See LICENSE file for details

## 👥 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Run tests before committing
4. Commit with descriptive messages
5. Push to branch
6. Open Pull Request

## 🐛 Known Issues

None currently. See GitHub Issues for planned enhancements.

## 📞 Contact

For questions or support:
- Email: contact@urbanmatter.com
- Website: https://urbanmatter.com

## 🔄 Changelog

### Version 1.0.0 (2025-01-23)
- Initial release
- Responsive design implementation
- Security headers and CSP
- Accessibility features
- Test suite
- Documentation

## 🙏 Acknowledgments

- Design inspiration from modern architecture websites
- WCAG guidelines from W3C
- Security best practices from OWASP
- Performance patterns from web.dev

---

Built with ❤️ by the Urban Matter team
