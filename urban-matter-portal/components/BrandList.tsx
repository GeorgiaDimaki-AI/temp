import { Brand } from "@/app/page";

interface BrandListProps {
  brands: Brand[];
  onEdit: (brand: Brand) => void;
  onDelete: (id: string) => void;
}

export default function BrandList({ brands, onEdit, onDelete }: BrandListProps) {
  if (brands.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <p className="text-gray-500 text-lg">No brands yet. Add your first brand to get started!</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {brands.map((brand) => (
        <div
          key={brand.id}
          className="bg-white rounded-lg shadow hover:shadow-lg transition overflow-hidden"
        >
          <div className="relative h-48 bg-gray-200">
            <img
              src={brand.image}
              alt={brand.name}
              className="w-full h-full object-cover"
            />
            {brand.featured && (
              <div className="absolute top-3 right-3 bg-amber-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
                Featured
              </div>
            )}
          </div>

          <div className="p-5">
            <div className="mb-2">
              <span className="text-sm font-semibold text-emerald-600 uppercase">
                {brand.category}
              </span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-1">
              {brand.name}
            </h3>
            <p className="text-amber-700 font-medium mb-2">{brand.tagline}</p>
            <p className="text-gray-600 text-sm mb-4 line-clamp-2">
              {brand.description}
            </p>

            <div className="flex gap-2">
              <button
                onClick={() => onEdit(brand)}
                className="flex-1 bg-slate-900 text-white px-4 py-2 rounded hover:bg-slate-800 transition text-sm font-medium"
              >
                Edit
              </button>
              <button
                onClick={() => onDelete(brand.id)}
                className="flex-1 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition text-sm font-medium"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
