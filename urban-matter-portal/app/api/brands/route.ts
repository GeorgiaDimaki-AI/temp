import { NextRequest, NextResponse } from "next/server";
import { readBrands, writeBrands, generateId, Brand } from "@/lib/brands";

// GET all brands
export async function GET() {
  try {
    const brands = readBrands();
    return NextResponse.json(brands);
  } catch (error) {
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
    const brands = readBrands();

    const newBrand: Brand = {
      id: generateId(),
      name: body.name,
      tagline: body.tagline,
      description: body.description,
      image: body.image,
      website: body.website,
      category: body.category,
      featured: body.featured || false,
    };

    brands.push(newBrand);
    writeBrands(brands);

    return NextResponse.json(newBrand, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to create brand" },
      { status: 500 }
    );
  }
}
