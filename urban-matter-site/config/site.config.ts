/**
 * Site Configuration
 *
 * IMPORTANT: Change the company name and branding here!
 * This configuration is used throughout the site.
 */

export const siteConfig = {
  // Company Information
  companyName: "Urban Matter",
  tagline: "Crafting exceptional food brands",
  description: "A portfolio of carefully curated food brands, each with its own unique story and flavor profile.",

  // Contact Information
  email: "hello@urbanmatter.com",
  phone: "+1 (555) 123-4567",
  address: "123 Main Street, Your City, ST 12345",

  // Social Media (optional - leave empty string if not used)
  social: {
    instagram: "",
    twitter: "",
    linkedin: "",
    facebook: "",
  },

  // Branding Colors (Tailwind classes)
  colors: {
    primary: "slate-900",
    secondary: "amber-600",
    accent: "emerald-600",
  },
};

export type SiteConfig = typeof siteConfig;
