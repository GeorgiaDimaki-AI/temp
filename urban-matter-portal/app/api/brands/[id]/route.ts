import { NextRequest, NextResponse } from "next/server";
import { readBrands, writeBrands, Brand } from "@/lib/brands";

// GET single brand
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const brands = readBrands();
    const brand = brands.find((b) => b.id === id);

    if (!brand) {
      return NextResponse.json({ error: "Brand not found" }, { status: 404 });
    }

    return NextResponse.json(brand);
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to read brand" },
      { status: 500 }
    );
  }
}

// PUT update brand
export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const body = await request.json();
    const brands = readBrands();
    const index = brands.findIndex((b) => b.id === id);

    if (index === -1) {
      return NextResponse.json({ error: "Brand not found" }, { status: 404 });
    }

    const updatedBrand: Brand = {
      id,
      name: body.name,
      tagline: body.tagline,
      description: body.description,
      image: body.image,
      website: body.website,
      category: body.category,
      featured: body.featured || false,
    };

    brands[index] = updatedBrand;
    writeBrands(brands);

    return NextResponse.json(updatedBrand);
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to update brand" },
      { status: 500 }
    );
  }
}

// DELETE brand
export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const brands = readBrands();
    const filteredBrands = brands.filter((b) => b.id !== id);

    if (filteredBrands.length === brands.length) {
      return NextResponse.json({ error: "Brand not found" }, { status: 404 });
    }

    writeBrands(filteredBrands);
    return NextResponse.json({ message: "Brand deleted successfully" });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to delete brand" },
      { status: 500 }
    );
  }
}
