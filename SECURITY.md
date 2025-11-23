# Security Policy

## Overview

Urban Matter takes security seriously. This document outlines our security practices and how to report vulnerabilities.

## Security Features Implemented

### 1. Content Security Policy (CSP)

We implement a strict CSP to prevent XSS attacks:

```
default-src 'self';
script-src 'self' 'unsafe-inline';
style-src 'self' 'unsafe-inline';
img-src 'self' data: https:;
font-src 'self' data:;
connect-src 'self';
frame-ancestors 'self';
base-uri 'self';
form-action 'self';
```

### 2. Security Headers

- **X-Content-Type-Options**: `nosniff` - Prevents MIME type sniffing
- **X-Frame-Options**: `SAMEORIGIN` - Prevents clickjacking
- **X-XSS-Protection**: `1; mode=block` - Enables XSS filtering
- **Referrer-Policy**: `strict-origin-when-cross-origin` - Controls referrer information
- **Strict-Transport-Security**: `max-age=31536000; includeSubDomains; preload` - Forces HTTPS
- **Permissions-Policy**: Restricts browser features (geolocation, camera, etc.)

### 3. Input Validation & Sanitization

All user inputs are:
- Validated on client-side before submission
- Sanitized to prevent XSS attacks
- Checked for proper format (email, required fields, etc.)
- Escaped before any DOM manipulation

Example sanitization function:
```javascript
function sanitizeInput(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}
```

### 4. HTTPS Enforcement

- Production site MUST be served over HTTPS
- HTTP requests automatically redirected to HTTPS
- HSTS headers ensure browser always uses HTTPS

### 5. No External Dependencies

- All scripts and styles are self-hosted
- No third-party CDN dependencies
- No tracking scripts or analytics that could compromise privacy

### 6. Form Security

- CSRF protection considerations for backend implementation
- Client-side validation prevents common injection attempts
- Form submissions require all required fields
- Email validation using regex patterns

## Vulnerability Categories

### High Priority

- XSS (Cross-Site Scripting)
- SQL Injection (if backend is added)
- CSRF (Cross-Site Request Forgery)
- Authentication bypass
- Remote code execution

### Medium Priority

- Information disclosure
- Broken authentication
- Security misconfiguration
- Sensitive data exposure

### Low Priority

- Missing security headers (non-critical)
- Outdated dependencies (with no known exploits)
- Non-security code quality issues

## Reporting a Vulnerability

If you discover a security vulnerability:

1. **DO NOT** create a public GitHub issue
2. Email details to: security@urbanmatter.com (if configured)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Based on severity
  - Critical: 24-48 hours
  - High: 7 days
  - Medium: 30 days
  - Low: 90 days

## Security Best Practices for Deployment

### Apache

1. Place `.htaccess` file in web root
2. Ensure `mod_headers` is enabled
3. Configure SSL certificate
4. Enable HTTPS redirect

### Nginx

1. Use provided `nginx.conf` configuration
2. Configure SSL certificate
3. Enable HTTP/2
4. Set up proper SSL protocols and ciphers

### General

1. Keep server software updated
2. Use strong SSL/TLS configuration
3. Implement rate limiting
4. Monitor access logs
5. Regular security audits
6. Backup regularly
7. Use environment variables for sensitive data
8. Never commit secrets to version control

## Known Limitations

### Current Implementation

1. **No Backend Validation**: Form validation is client-side only. Backend validation MUST be implemented before production use.

2. **Inline Styles in CSP**: Currently allows `'unsafe-inline'` for styles. This should be removed and replaced with nonce-based CSP when possible.

3. **Inline Scripts in CSP**: JavaScript uses inline scripts. Consider moving to external files with nonce-based CSP.

4. **No CAPTCHA**: Contact form has no bot protection. Consider implementing reCAPTCHA or similar.

5. **No Rate Limiting (Client)**: Rate limiting must be implemented server-side.

## Security Checklist for Production

- [ ] SSL/TLS certificate installed and configured
- [ ] HTTPS redirect enabled
- [ ] Security headers configured (via .htaccess or nginx.conf)
- [ ] CSP headers properly set
- [ ] All forms connect to secure backend
- [ ] Backend input validation implemented
- [ ] Rate limiting configured
- [ ] Database secured (if applicable)
- [ ] Error pages don't expose sensitive information
- [ ] Directory listing disabled
- [ ] Unnecessary files removed (.git, tests, etc.)
- [ ] Monitoring and logging enabled
- [ ] Regular backups configured
- [ ] Security audit completed

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Content Security Policy Reference](https://content-security-policy.com/)
- [Mozilla Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
- [Security Headers Check](https://securityheaders.com/)
- [SSL Server Test](https://www.ssllabs.com/ssltest/)

## Updates

This security policy is reviewed and updated quarterly. Last update: 2025-01-23
