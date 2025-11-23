# Implementation Guide: Vercel Migration
## Step-by-Step Technical Instructions

**Prerequisites:**
- Vercel account created
- GitHub repo connected to Vercel
- Node.js 18+ installed locally

---

## Phase 1: Deploy Current Code (30 minutes)

### Step 1.1: Deploy Urban Matter Site

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import the GitHub repository
3. Configure build settings:
   ```
   Framework Preset: Next.js
   Root Directory: urban-matter-site
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   ```
4. Click "Deploy"
5. Note the deployment URL (e.g., `urban-matter-site.vercel.app`)

### Step 1.2: Deploy Urban Matter Portal

1. Create a new Vercel project for the portal
2. Import the same GitHub repository
3. Configure build settings:
   ```
   Framework Preset: Next.js
   Root Directory: urban-matter-portal
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   ```
4. Click "Deploy"
5. Note the deployment URL (e.g., `urban-matter-portal.vercel.app`)

### Step 1.3: Test Deployments

**Expected Results:**
- ✅ Site should load and display
- ⚠️ Portal won't persist data (file system is read-only)
- ⚠️ No authentication on portal

**Action:** This is for testing only. Proceed to Phase 2 for production readiness.

---

## Phase 2: Database Migration (4 hours)

### Step 2.1: Provision Vercel Postgres

1. In Vercel dashboard, go to Storage tab
2. Click "Create Database"
3. Select "Postgres"
4. Choose a region (closest to your users)
5. Click "Create"
6. Note the connection details (auto-added to environment variables)

### Step 2.2: Create Database Schema

```sql
-- Run this in Vercel Postgres SQL Editor or via psql

CREATE TABLE brands (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  tagline TEXT NOT NULL,
  description TEXT NOT NULL,
  image TEXT NOT NULL,
  website TEXT NOT NULL,
  category TEXT NOT NULL,
  featured BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX idx_brands_featured ON brands(featured);
CREATE INDEX idx_brands_category ON brands(category);

-- Insert sample data
INSERT INTO brands (id, name, tagline, description, image, website, category, featured)
VALUES (
  '1',
  'Sample Brand',
  'Premium artisanal foods',
  'Our flagship brand offering premium, handcrafted food products made with locally sourced ingredients.',
  'https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=800&h=600&fit=crop',
  'https://example.com',
  'Artisanal',
  true
);
```

### Step 2.3: Update Portal Dependencies

```bash
cd urban-matter-portal
npm install @vercel/postgres
```

Update `urban-matter-portal/package.json`:
```json
{
  "dependencies": {
    "@vercel/postgres": "^0.5.1",
    // ... existing dependencies
  }
}
```

### Step 2.4: Rewrite Database Layer

Create `urban-matter-portal/lib/db.ts`:
```typescript
import { sql } from '@vercel/postgres';

export interface Brand {
  id: string;
  name: string;
  tagline: string;
  description: string;
  image: string;
  website: string;
  category: string;
  featured: boolean;
  created_at?: Date;
  updated_at?: Date;
}

export async function getAllBrands(): Promise<Brand[]> {
  const { rows } = await sql<Brand>`
    SELECT * FROM brands
    ORDER BY featured DESC, created_at DESC
  `;
  return rows;
}

export async function getBrandById(id: string): Promise<Brand | null> {
  const { rows } = await sql<Brand>`
    SELECT * FROM brands WHERE id = ${id}
  `;
  return rows[0] || null;
}

export async function createBrand(brand: Omit<Brand, 'id' | 'created_at' | 'updated_at'>): Promise<Brand> {
  const id = Date.now().toString(36) + Math.random().toString(36).substr(2);

  const { rows } = await sql<Brand>`
    INSERT INTO brands (id, name, tagline, description, image, website, category, featured)
    VALUES (${id}, ${brand.name}, ${brand.tagline}, ${brand.description},
            ${brand.image}, ${brand.website}, ${brand.category}, ${brand.featured})
    RETURNING *
  `;

  return rows[0];
}

export async function updateBrand(id: string, brand: Partial<Brand>): Promise<Brand | null> {
  const { rows } = await sql<Brand>`
    UPDATE brands
    SET
      name = COALESCE(${brand.name}, name),
      tagline = COALESCE(${brand.tagline}, tagline),
      description = COALESCE(${brand.description}, description),
      image = COALESCE(${brand.image}, image),
      website = COALESCE(${brand.website}, website),
      category = COALESCE(${brand.category}, category),
      featured = COALESCE(${brand.featured}, featured),
      updated_at = CURRENT_TIMESTAMP
    WHERE id = ${id}
    RETURNING *
  `;

  return rows[0] || null;
}

export async function deleteBrand(id: string): Promise<boolean> {
  const { rowCount } = await sql`
    DELETE FROM brands WHERE id = ${id}
  `;

  return (rowCount || 0) > 0;
}
```

### Step 2.5: Update Portal API Routes

Replace `urban-matter-portal/app/api/brands/route.ts`:
```typescript
import { NextRequest, NextResponse } from "next/server";
import { getAllBrands, createBrand } from "@/lib/db";

export const dynamic = 'force-dynamic';

// GET all brands
export async function GET() {
  try {
    const brands = await getAllBrands();
    return NextResponse.json(brands);
  } catch (error) {
    console.error('Failed to read brands:', error);
    return NextResponse.json(
      { error: "Failed to read brands" },
      { status: 500 }
    );
  }
}

// POST create new brand
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validation
    if (!body.name || !body.tagline || !body.description) {
      return NextResponse.json(
        { error: "Missing required fields" },
        { status: 400 }
      );
    }

    const newBrand = await createBrand({
      name: body.name,
      tagline: body.tagline,
      description: body.description,
      image: body.image || '',
      website: body.website || '',
      category: body.category || 'Uncategorized',
      featured: body.featured || false,
    });

    return NextResponse.json(newBrand, { status: 201 });
  } catch (error) {
    console.error('Failed to create brand:', error);
    return NextResponse.json(
      { error: "Failed to create brand" },
      { status: 500 }
    );
  }
}
```

Replace `urban-matter-portal/app/api/brands/[id]/route.ts`:
```typescript
import { NextRequest, NextResponse } from "next/server";
import { getBrandById, updateBrand, deleteBrand } from "@/lib/db";

export const dynamic = 'force-dynamic';

// GET single brand
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const brand = await getBrandById(params.id);

    if (!brand) {
      return NextResponse.json(
        { error: "Brand not found" },
        { status: 404 }
      );
    }

    return NextResponse.json(brand);
  } catch (error) {
    console.error('Failed to read brand:', error);
    return NextResponse.json(
      { error: "Failed to read brand" },
      { status: 500 }
    );
  }
}

// PUT update brand
export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json();
    const updatedBrand = await updateBrand(params.id, body);

    if (!updatedBrand) {
      return NextResponse.json(
        { error: "Brand not found" },
        { status: 404 }
      );
    }

    return NextResponse.json(updatedBrand);
  } catch (error) {
    console.error('Failed to update brand:', error);
    return NextResponse.json(
      { error: "Failed to update brand" },
      { status: 500 }
    );
  }
}

// DELETE brand
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const deleted = await deleteBrand(params.id);

    if (!deleted) {
      return NextResponse.json(
        { error: "Brand not found" },
        { status: 404 }
      );
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Failed to delete brand:', error);
    return NextResponse.json(
      { error: "Failed to delete brand" },
      { status: 500 }
    );
  }
}
```

### Step 2.6: Update Site to Fetch from API

Update `urban-matter-site/components/BrandsGrid.tsx`:
```typescript
import { Brand } from "@/types/brand";
import BrandCard from "./BrandCard";

async function getBrands(): Promise<Brand[]> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

  try {
    const res = await fetch(`${apiUrl}/api/brands`, {
      next: { revalidate: 60 } // ISR: revalidate every 60 seconds
    });

    if (!res.ok) {
      throw new Error('Failed to fetch brands');
    }

    return res.json();
  } catch (error) {
    console.error('Error fetching brands:', error);
    return [];
  }
}

export default async function BrandsGrid() {
  const brands = await getBrands();

  return (
    <section id="brands" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4">
            Our Brands
          </h2>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            A carefully curated portfolio of exceptional food brands, each with
            its own unique story.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {brands.map((brand) => (
            <BrandCard key={brand.id} brand={brand} />
          ))}
        </div>

        {brands.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">
              No brands yet. Use the management portal to add your first brand!
            </p>
          </div>
        )}
      </div>
    </section>
  );
}
```

Create `urban-matter-site/types/brand.ts`:
```typescript
export interface Brand {
  id: string;
  name: string;
  tagline: string;
  description: string;
  image: string;
  website: string;
  category: string;
  featured: boolean;
  created_at?: string;
  updated_at?: string;
}
```

### Step 2.7: Configure Environment Variables

In Vercel Dashboard → Site Project → Settings → Environment Variables:
```
NEXT_PUBLIC_API_URL=https://urban-matter-portal.vercel.app
```

The Postgres connection string is auto-configured by Vercel.

### Step 2.8: Delete Old Files (No Longer Needed)

```bash
# Portal no longer needs these
rm urban-matter-portal/lib/brands.ts

# Site no longer uses static JSON
rm urban-matter-site/data/brands.json
```

### Step 2.9: Deploy and Test

```bash
git add .
git commit -m "Migrate to Vercel Postgres database"
git push origin claude/vercel-nextjs-evaluation-012sdoN255sV8woXYmoUBQTW
```

Vercel will auto-deploy. Test:
1. Visit portal URL
2. Add a new brand
3. Visit site URL
4. Verify new brand appears (within 60 seconds due to ISR)

---

## Phase 3: Add Authentication (3 hours)

### Step 3.1: Install NextAuth.js

```bash
cd urban-matter-portal
npm install next-auth@beta
npm install @auth/core
```

### Step 3.2: Create Auth Configuration

Create `urban-matter-portal/auth.ts`:
```typescript
import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";
import Google from "next-auth/providers/google";

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    GitHub({
      clientId: process.env.AUTH_GITHUB_ID,
      clientSecret: process.env.AUTH_GITHUB_SECRET,
    }),
    Google({
      clientId: process.env.AUTH_GOOGLE_ID,
      clientSecret: process.env.AUTH_GOOGLE_SECRET,
    }),
  ],
  pages: {
    signIn: '/auth/signin',
  },
  callbacks: {
    authorized({ auth, request: { nextUrl } }) {
      const isLoggedIn = !!auth?.user;
      const isOnDashboard = nextUrl.pathname.startsWith('/');

      if (isOnDashboard) {
        if (isLoggedIn) return true;
        return false; // Redirect unauthenticated users to login page
      }

      return true;
    },
  },
});
```

### Step 3.3: Add Auth Routes

Create `urban-matter-portal/app/api/auth/[...nextauth]/route.ts`:
```typescript
import { handlers } from "@/auth";

export const { GET, POST } = handlers;
```

### Step 3.4: Create Sign-In Page

Create `urban-matter-portal/app/auth/signin/page.tsx`:
```typescript
import { signIn } from "@/auth";

export default function SignIn() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-center mb-8">
          Urban Matter Portal
        </h1>
        <p className="text-gray-600 text-center mb-8">
          Sign in to manage your brand portfolio
        </p>

        <form
          action={async () => {
            "use server";
            await signIn("github", { redirectTo: "/" });
          }}
          className="mb-4"
        >
          <button
            type="submit"
            className="w-full bg-gray-900 text-white py-3 rounded-lg hover:bg-gray-800 transition"
          >
            Sign in with GitHub
          </button>
        </form>

        <form
          action={async () => {
            "use server";
            await signIn("google", { redirectTo: "/" });
          }}
        >
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition"
          >
            Sign in with Google
          </button>
        </form>
      </div>
    </div>
  );
}
```

### Step 3.5: Add Middleware for Protected Routes

Create `urban-matter-portal/middleware.ts`:
```typescript
export { auth as middleware } from "@/auth";

export const config = {
  matcher: ["/((?!api/auth|auth/signin|_next/static|_next/image|favicon.ico).*)"],
};
```

### Step 3.6: Add Sign-Out Button

Update `urban-matter-portal/app/page.tsx` to add sign-out:
```typescript
import { auth, signOut } from "@/auth";
import BrandList from "@/components/BrandList";
import BrandForm from "@/components/BrandForm";

export default async function Home() {
  const session = await auth();

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex justify-between items-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900">
            Brand Management Portal
          </h1>

          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">
              {session?.user?.email}
            </span>
            <form
              action={async () => {
                "use server";
                await signOut();
              }}
            >
              <button
                type="submit"
                className="px-4 py-2 text-sm text-gray-700 hover:text-gray-900"
              >
                Sign out
              </button>
            </form>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <BrandForm />
          </div>
          <div className="lg:col-span-2">
            <BrandList />
          </div>
        </div>
      </div>
    </main>
  );
}
```

### Step 3.7: Configure OAuth Apps

**For GitHub:**
1. Go to GitHub Settings → Developer settings → OAuth Apps
2. Click "New OAuth App"
3. Set homepage: `https://urban-matter-portal.vercel.app`
4. Set callback URL: `https://urban-matter-portal.vercel.app/api/auth/callback/github`
5. Copy Client ID and Client Secret

**For Google:**
1. Go to Google Cloud Console
2. Create new project or use existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Set authorized redirect URI: `https://urban-matter-portal.vercel.app/api/auth/callback/google`
6. Copy Client ID and Client Secret

### Step 3.8: Add Environment Variables

In Vercel Dashboard → Portal Project → Settings → Environment Variables:
```
AUTH_SECRET=<generate with: openssl rand -base64 32>
AUTH_GITHUB_ID=<from GitHub OAuth app>
AUTH_GITHUB_SECRET=<from GitHub OAuth app>
AUTH_GOOGLE_ID=<from Google OAuth>
AUTH_GOOGLE_SECRET=<from Google OAuth>
```

### Step 3.9: Deploy and Test

```bash
git add .
git commit -m "Add NextAuth.js authentication to portal"
git push origin claude/vercel-nextjs-evaluation-012sdoN255sV8woXYmoUBQTW
```

Test:
1. Visit portal URL → should redirect to sign-in
2. Sign in with GitHub or Google
3. Should redirect to dashboard
4. Sign out should work

---

## Phase 4: Image Optimization (2 hours)

### Step 4.1: Configure Image Domains

Update `urban-matter-site/next.config.js`:
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
      },
      {
        protocol: 'https',
        hostname: '**.public.blob.vercel-storage.com',
      },
    ],
  },
};

module.exports = nextConfig;
```

### Step 4.2: Update BrandCard Component

Update `urban-matter-site/components/BrandCard.tsx`:
```typescript
import Image from "next/image";
import { Brand } from "@/types/brand";

interface BrandCardProps {
  brand: Brand;
}

export default function BrandCard({ brand }: BrandCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
      <div className="relative h-64 w-full">
        <Image
          src={brand.image}
          alt={brand.name}
          fill
          className="object-cover"
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        />
        {brand.featured && (
          <div className="absolute top-4 right-4 bg-amber-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
            Featured
          </div>
        )}
      </div>

      <div className="p-6">
        <h3 className="text-2xl font-bold text-slate-900 mb-2">
          {brand.name}
        </h3>
        <p className="text-amber-600 font-medium mb-3">
          {brand.tagline}
        </p>
        <p className="text-slate-600 mb-4 line-clamp-3">
          {brand.description}
        </p>

        <div className="flex items-center justify-between">
          <span className="text-sm text-slate-500 bg-slate-100 px-3 py-1 rounded-full">
            {brand.category}
          </span>
          {brand.website && (
            <a
              href={brand.website}
              target="_blank"
              rel="noopener noreferrer"
              className="text-amber-600 hover:text-amber-700 font-medium text-sm"
            >
              Visit Site →
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
```

### Step 4.3: Add Vercel Blob (Optional - for uploads)

If you want to allow image uploads in the portal:

```bash
cd urban-matter-portal
npm install @vercel/blob
```

Create upload endpoint `urban-matter-portal/app/api/upload/route.ts`:
```typescript
import { put } from '@vercel/blob';
import { NextResponse } from 'next/server';

export async function POST(request: Request): Promise<NextResponse> {
  const { searchParams } = new URL(request.url);
  const filename = searchParams.get('filename');

  if (!filename) {
    return NextResponse.json(
      { error: 'Filename is required' },
      { status: 400 }
    );
  }

  const blob = await put(filename, request.body!, {
    access: 'public',
  });

  return NextResponse.json(blob);
}
```

---

## Phase 5: Production Checklist

### Environment Variables
- [ ] `NEXT_PUBLIC_API_URL` set in site project
- [ ] `AUTH_SECRET` set in portal project
- [ ] OAuth credentials configured
- [ ] Postgres connection (auto-configured)

### DNS Configuration
- [ ] Custom domain for site (e.g., `urbanmatter.com`)
- [ ] Custom domain for portal (e.g., `portal.urbanmatter.com`)
- [ ] SSL certificates (auto-issued by Vercel)

### Security
- [ ] Authentication working
- [ ] API routes protected
- [ ] CORS configured if needed
- [ ] Rate limiting considered

### Performance
- [ ] Image optimization enabled
- [ ] ISR configured (60s revalidation)
- [ ] Database indexes created
- [ ] Analytics enabled

### Monitoring
- [ ] Error tracking (Vercel Analytics or Sentry)
- [ ] Uptime monitoring
- [ ] Database query performance

### Backup
- [ ] Database backup strategy (Vercel Postgres has auto-backups)
- [ ] Export data capability

---

## Troubleshooting

### "Failed to connect to database"
- Check Vercel Postgres is provisioned
- Verify environment variables are set
- Check database is in same region as function

### "Unauthorized" errors
- Check AUTH_SECRET is set
- Verify OAuth credentials are correct
- Check callback URLs match exactly

### Images not loading
- Verify image domain in next.config.js
- Check Next.js Image component props
- Validate image URLs are accessible

### ISR not updating
- Wait full revalidation period (60s)
- Check API is returning new data
- Force refresh with Ctrl+Shift+R

---

## Support Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js App Router](https://nextjs.org/docs/app)
- [NextAuth.js v5](https://authjs.dev/)
- [Vercel Postgres](https://vercel.com/docs/storage/vercel-postgres)
- [Vercel Blob](https://vercel.com/docs/storage/vercel-blob)

---

**Implementation guide complete. Deploy with confidence.**
