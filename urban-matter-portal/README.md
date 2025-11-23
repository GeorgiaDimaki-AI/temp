# Urban Matter - Management Portal

Private dashboard for managing your brand portfolio.

## 🚀 Getting Started

```bash
# Install dependencies
npm install

# Run development server (port 3001)
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

Visit http://localhost:3001

## 🎯 Features

- **Create** new brands
- **Read** brand list
- **Update** existing brands
- **Delete** brands (with confirmation)
- Real-time updates to public site
- Form validation
- Responsive admin interface

## 📁 Project Structure

```
app/
  ├── api/
  │   └── brands/
  │       ├── route.ts        # GET all, POST new
  │       └── [id]/route.ts   # GET, PUT, DELETE by ID
  ├── layout.tsx              # Root layout
  ├── page.tsx                # Main dashboard
  └── globals.css             # Global styles

components/
  ├── BrandList.tsx           # Brand grid display
  └── BrandForm.tsx           # Add/edit form

lib/
  └── brands.ts               # File operations
```

## 🔑 API Routes

### GET /api/brands
Fetch all brands

### POST /api/brands
Create a new brand

**Body:**
```json
{
  "name": "Brand Name",
  "tagline": "Short tagline",
  "description": "Detailed description",
  "image": "https://example.com/image.jpg",
  "website": "https://brand.com",
  "category": "Artisanal",
  "featured": true
}
```

### GET /api/brands/[id]
Fetch a specific brand

### PUT /api/brands/[id]
Update a brand

### DELETE /api/brands/[id]
Delete a brand

## 💾 Data Storage

Brands are stored in:
```
../urban-matter-site/data/brands.json
```

**Important:** The portal and site must be in the same parent directory.

## 📝 Adding a Brand

1. Click "Add New Brand"
2. Fill in the form:
   - **Name:** Brand name (required)
   - **Tagline:** Short catchphrase (required)
   - **Description:** Detailed info (required)
   - **Image URL:** Direct link to image (required)
   - **Website:** Brand website (required)
   - **Category:** e.g., "Artisanal", "Organic" (required)
   - **Featured:** Check to highlight on homepage
3. Click "Add Brand"

## ✏️ Editing a Brand

1. Find the brand card
2. Click "Edit"
3. Modify fields
4. Click "Update Brand"

## 🗑️ Deleting a Brand

1. Find the brand card
2. Click "Delete"
3. Confirm deletion

**Note:** This action cannot be undone!

## 🖼️ Image URLs

For images, you can use:

**Unsplash (free):**
```
https://images.unsplash.com/photo-XXXXXXXX?w=800&h=600&fit=crop
```

**Your own hosting:**
- Upload to your server
- Use the full URL

**Image CDN:**
- Cloudinary
- ImageKit
- AWS S3

**Requirements:**
- Must be a valid URL
- Publicly accessible
- HTTPS recommended

## 🔒 Security

**⚠️ WARNING:** This portal has NO authentication!

Before production deployment:

### Add Authentication
```bash
npm install next-auth
```

### Protect API Routes
```typescript
// middleware.ts
export { default } from "next-auth/middleware"

export const config = {
  matcher: ["/api/brands/:path*"]
}
```

### Environment Variables
Create `.env.local`:
```
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=http://localhost:3001
```

## 🌐 Production Deployment

### Option 1: Same Server as Site
- Run both applications
- Use reverse proxy (nginx)
- Restrict portal access by IP

### Option 2: Separate Server
- Deploy portal privately
- Use VPN or IP whitelist
- Add authentication

### Option 3: Database Migration
For production, consider migrating from JSON to:
- PostgreSQL with Prisma
- MongoDB with Mongoose
- Supabase
- Firebase

## 🛠 Customization

### Change Port
Edit `package.json`:
```json
{
  "scripts": {
    "dev": "next dev -p 3002"  // Change to any port
  }
}
```

### Add Fields
1. Update `lib/brands.ts` interface
2. Modify `components/BrandForm.tsx`
3. Update API routes
4. Update site components

### Styling
- Uses Tailwind CSS
- Edit components for layout changes
- Modify `tailwind.config.ts` for theme

## 🐛 Troubleshooting

**Can't find brands.json:**
- Ensure directory structure is correct
- Check file exists at `../urban-matter-site/data/brands.json`
- Run portal from correct directory

**Changes not saving:**
- Check browser console for errors
- Verify write permissions on brands.json
- Check API route responses

**Port conflict:**
- Change port in package.json
- Kill process using the port
- Use different port number

## 🔄 Workflow

1. Make changes in portal
2. Portal updates brands.json
3. Public site reads updated data
4. Changes appear on refresh

In production, implement:
- Webhooks for automatic updates
- Incremental Static Regeneration
- Cache invalidation

---

For more information, see the main project README.
