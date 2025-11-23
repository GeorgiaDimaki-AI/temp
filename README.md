# Urban Matter - Brand Portfolio Platform

A complete solution for showcasing and managing your food brand portfolio. This project consists of two applications:

1. **Urban Matter Site** - Public-facing portfolio website
2. **Urban Matter Portal** - Private management dashboard

## 🎯 Features

### Public Site
- Beautiful, responsive portfolio showcase
- Dynamic brand cards with featured highlights
- Configurable company branding
- Hero section with call-to-actions
- About and Contact sections
- Mobile-friendly navigation

### Management Portal
- Add, edit, and delete brands
- Real-time updates to the public site
- Image URL management
- Featured brand toggling
- Category organization
- Responsive admin dashboard

## 📁 Project Structure

```
.
├── urban-matter-site/     # Public-facing website
│   ├── app/               # Next.js app directory
│   ├── components/        # React components
│   ├── config/            # Site configuration (CHANGE BRANDING HERE!)
│   └── data/              # Brand data storage
│
└── urban-matter-portal/   # Management portal
    ├── app/               # Next.js app with API routes
    ├── components/        # Admin UI components
    └── lib/               # Utility functions
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed
- npm or yarn package manager

### Installation

1. **Install dependencies for both applications:**

```bash
# Install site dependencies
cd urban-matter-site
npm install

# Install portal dependencies
cd ../urban-matter-portal
npm install
```

2. **Start development servers:**

Open two terminal windows:

**Terminal 1 - Public Site (Port 3000):**
```bash
cd urban-matter-site
npm run dev
```

**Terminal 2 - Management Portal (Port 3001):**
```bash
cd urban-matter-portal
npm run dev
```

3. **Access the applications:**
- Public Site: http://localhost:3000
- Management Portal: http://localhost:3001

## 🎨 Customizing Your Branding

**IMPORTANT:** To change the company name and branding, edit this file:

```
urban-matter-site/config/site.config.ts
```

This file contains:
- Company name
- Tagline
- Contact information
- Social media links
- Color scheme

Simply update the values and restart the development server!

## 📝 Managing Brands

1. Open the Management Portal at http://localhost:3001
2. Click "Add New Brand"
3. Fill in the brand details:
   - Name
   - Tagline
   - Description
   - Image URL (use Unsplash or your own images)
   - Website URL
   - Category
   - Featured status (appears with special badge)
4. Click "Add Brand"
5. Changes appear immediately on the public site!

## 🌐 Production Deployment

### Site Deployment

```bash
cd urban-matter-site
npm run build
npm run start
```

### Portal Deployment

```bash
cd urban-matter-portal
npm run build
npm run start
```

**Note:** For production, consider:
- Using environment variables for configuration
- Implementing authentication for the portal
- Migrating from JSON file storage to a database (PostgreSQL, MongoDB, etc.)
- Using a CDN for images

## 🔒 Security Considerations

**IMPORTANT:** The management portal currently has no authentication. Before deploying to production:

1. Add authentication (NextAuth.js, Auth0, etc.)
2. Secure API routes with middleware
3. Implement rate limiting
4. Add input validation and sanitization
5. Use environment variables for sensitive data

## 🛠 Tech Stack

- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Storage:** File-based JSON (upgradeable to database)
- **Icons:** SVG-based

## 📄 File Locations

- **Brand Data:** `urban-matter-site/data/brands.json`
- **Site Config:** `urban-matter-site/config/site.config.ts`
- **Portal API:** `urban-matter-portal/app/api/brands/`

## 🐛 Troubleshooting

**Portal can't find brands.json:**
- Ensure both projects are in the same parent directory
- The portal looks for `../urban-matter-site/data/brands.json`

**Changes not appearing:**
- Hard refresh your browser (Ctrl+Shift+R or Cmd+Shift+R)
- Check the browser console for errors
- Verify the brands.json file was updated

**Port already in use:**
- Change the port in package.json scripts
- Site uses port 3000, Portal uses port 3001

## 📚 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [TypeScript](https://www.typescriptlang.org/docs)

## 📜 License

This project is open source and available under the ISC License.

---

**Built with ❤️ for creating beautiful brand portfolios**
