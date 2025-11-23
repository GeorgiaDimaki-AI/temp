# Urban Matter - Public Site

The public-facing portfolio website showcasing your brand collection.

## 🚀 Getting Started

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

Visit http://localhost:3000

## 🎨 Customizing Branding

Edit `config/site.config.ts` to change:
- Company name ("Urban Matter")
- Tagline
- Contact information
- Social media links
- Color scheme

Example:
```typescript
export const siteConfig = {
  companyName: "Your Company Name", // Change this!
  tagline: "Your tagline here",
  // ... more settings
};
```

## 📁 Project Structure

```
app/
  ├── layout.tsx        # Root layout with header/footer
  ├── page.tsx          # Homepage
  └── globals.css       # Global styles

components/
  ├── Header.tsx        # Navigation header
  ├── Footer.tsx        # Site footer
  ├── Hero.tsx          # Hero section
  ├── BrandsGrid.tsx    # Brand showcase grid
  ├── BrandCard.tsx     # Individual brand card
  ├── About.tsx         # About section
  └── Contact.tsx       # Contact section

config/
  └── site.config.ts    # ⭐ Site configuration (edit this!)

data/
  └── brands.json       # Brand data (managed by portal)
```

## 🎯 Features

- Responsive design (mobile, tablet, desktop)
- Dynamic brand loading from JSON
- Featured brand highlighting
- Smooth navigation
- SEO-friendly structure
- Fast page loads with Next.js

## 🔧 Configuration

### Colors

Update Tailwind classes in `config/site.config.ts`:
```typescript
colors: {
  primary: "slate-900",    // Main color
  secondary: "amber-600",  // Accent color
  accent: "emerald-600",   // Highlight color
}
```

### Images

Brand images are loaded from URLs specified in `data/brands.json`. Use:
- Your own image hosting
- Unsplash (e.g., `https://images.unsplash.com/...`)
- CDN service

## 📝 Managing Content

Brand content is managed through the **Urban Matter Portal**.

See the main README for portal setup instructions.

## 🌐 Deployment

### Vercel (Recommended)
1. Push to GitHub
2. Import to Vercel
3. Deploy automatically

### Other Platforms
- Build: `npm run build`
- Start: `npm start`
- Requires Node.js 18+

## 🎨 Customizing Styles

This project uses Tailwind CSS. To customize:

1. Edit `tailwind.config.ts` for theme changes
2. Modify component files for layout changes
3. Update `app/globals.css` for global styles

## 📱 Sections

- **Hero:** Welcome section with company name and CTA
- **Brands:** Grid of brand cards
- **About:** Company information
- **Contact:** Contact details and information

## 🔄 Updates

When brands are added/edited/deleted via the portal:
1. Portal updates `data/brands.json`
2. Refresh the site to see changes
3. In production, consider revalidation strategies

---

For more information, see the main project README.
