"use client";

import { useState, useEffect } from "react";
import BrandList from "@/components/BrandList";
import BrandForm from "@/components/BrandForm";

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

export default function Portal() {
  const [brands, setBrands] = useState<Brand[]>([]);
  const [editingBrand, setEditingBrand] = useState<Brand | null>(null);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchBrands();
  }, []);

  const fetchBrands = async () => {
    try {
      const response = await fetch("/api/brands");
      const data = await response.json();
      setBrands(data);
    } catch (error) {
      console.error("Failed to fetch brands:", error);
    }
  };

  const handleSave = async (brand: Omit<Brand, "id"> | Brand) => {
    try {
      const isEdit = "id" in brand && brand.id;
      const url = isEdit ? `/api/brands/${brand.id}` : "/api/brands";
      const method = isEdit ? "PUT" : "POST";

      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(brand),
      });

      if (response.ok) {
        fetchBrands();
        setShowForm(false);
        setEditingBrand(null);
      }
    } catch (error) {
      console.error("Failed to save brand:", error);
    }
  };

  const handleEdit = (brand: Brand) => {
    setEditingBrand(brand);
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this brand?")) return;

    try {
      const response = await fetch(`/api/brands/${id}`, {
        method: "DELETE",
      });

      if (response.ok) {
        fetchBrands();
      }
    } catch (error) {
      console.error("Failed to delete brand:", error);
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingBrand(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-slate-900 text-white py-6 px-4 shadow-lg">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold">Urban Matter</h1>
          <p className="text-gray-300 mt-1">Brand Management Portal</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-6 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-900">Your Brands</h2>
          <button
            onClick={() => setShowForm(true)}
            className="bg-slate-900 text-white px-6 py-3 rounded-lg hover:bg-slate-800 transition font-semibold"
          >
            + Add New Brand
          </button>
        </div>

        {showForm && (
          <div className="mb-8">
            <BrandForm
              brand={editingBrand}
              onSave={handleSave}
              onCancel={handleCancel}
            />
          </div>
        )}

        <BrandList
          brands={brands}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      </main>
    </div>
  );
}
