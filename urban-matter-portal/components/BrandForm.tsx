"use client";

import { useState, useEffect } from "react";
import { Brand } from "@/app/page";

interface BrandFormProps {
  brand: Brand | null;
  onSave: (brand: Omit<Brand, "id"> | Brand) => void;
  onCancel: () => void;
}

export default function BrandForm({ brand, onSave, onCancel }: BrandFormProps) {
  const [formData, setFormData] = useState({
    name: "",
    tagline: "",
    description: "",
    image: "",
    website: "",
    category: "",
    featured: false,
  });

  useEffect(() => {
    if (brand) {
      setFormData(brand);
    }
  }, [brand]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (brand) {
      onSave({ ...formData, id: brand.id });
    } else {
      onSave(formData);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        type === "checkbox" ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-2xl font-bold text-gray-900 mb-6">
        {brand ? "Edit Brand" : "Add New Brand"}
      </h3>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Brand Name *
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-slate-900 focus:border-transparent"
              placeholder="e.g., Artisan Bakery"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Category *
            </label>
            <input
              type="text"
              name="category"
              value={formData.category}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-slate-900 focus:border-transparent"
              placeholder="e.g., Artisanal, Organic, etc."
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Tagline *
          </label>
          <input
            type="text"
            name="tagline"
            value={formData.tagline}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-slate-900 focus:border-transparent"
            placeholder="A short, catchy tagline"
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Description *
          </label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            rows={4}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-slate-900 focus:border-transparent"
            placeholder="Describe your brand..."
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Image URL *
          </label>
          <input
            type="url"
            name="image"
            value={formData.image}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-slate-900 focus:border-transparent"
            placeholder="https://example.com/image.jpg"
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Website URL *
          </label>
          <input
            type="url"
            name="website"
            value={formData.website}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-slate-900 focus:border-transparent"
            placeholder="https://yourbrand.com"
          />
        </div>

        <div className="flex items-center">
          <input
            type="checkbox"
            name="featured"
            id="featured"
            checked={formData.featured}
            onChange={handleChange}
            className="w-4 h-4 text-slate-900 border-gray-300 rounded focus:ring-slate-900"
          />
          <label htmlFor="featured" className="ml-2 text-sm text-gray-700">
            Feature this brand on the homepage
          </label>
        </div>

        <div className="flex gap-3 pt-4">
          <button
            type="submit"
            className="flex-1 bg-slate-900 text-white px-6 py-3 rounded-lg hover:bg-slate-800 transition font-semibold"
          >
            {brand ? "Update Brand" : "Add Brand"}
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300 transition font-semibold"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
