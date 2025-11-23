import brandsData from "@/data/brands.json";
import BrandCard from "./BrandCard";

export default function BrandsGrid() {
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
          {brandsData.map((brand) => (
            <BrandCard key={brand.id} brand={brand} />
          ))}
        </div>

        {brandsData.length === 0 && (
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
