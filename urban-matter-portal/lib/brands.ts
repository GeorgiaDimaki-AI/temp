import fs from "fs";
import path from "path";

// Path to the brands.json file in the main site
const BRANDS_FILE = path.join(
  process.cwd(),
  "../urban-matter-site/data/brands.json"
);

export interface Brand {
  id: string;
  name: string;
  tagline: string;
  description: string;
  image: string;
  website: string;
  category: string;
  featured: boolean;
}

export function readBrands(): Brand[] {
  try {
    const data = fs.readFileSync(BRANDS_FILE, "utf-8");
    return JSON.parse(data);
  } catch (error) {
    // If file doesn't exist or is invalid, return empty array
    return [];
  }
}

export function writeBrands(brands: Brand[]): void {
  const dir = path.dirname(BRANDS_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(BRANDS_FILE, JSON.stringify(brands, null, 2));
}

export function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}
