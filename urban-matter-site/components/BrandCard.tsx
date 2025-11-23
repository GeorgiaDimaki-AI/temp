interface Brand {
  id: string;
  name: string;
  tagline: string;
  description: string;
  image: string;
  website: string;
  category: string;
  featured: boolean;
}

export default function BrandCard({ brand }: { brand: Brand }) {
  return (
    <div className="group bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100">
      <div className="relative h-64 overflow-hidden bg-gray-100">
        <img
          src={brand.image}
          alt={brand.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />
        {brand.featured && (
          <div className="absolute top-4 right-4 bg-amber-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
            Featured
          </div>
        )}
      </div>

      <div className="p-6">
        <div className="mb-2">
          <span className="text-sm font-semibold text-emerald-600 uppercase tracking-wide">
            {brand.category}
          </span>
        </div>
        <h3 className="text-2xl font-bold text-slate-900 mb-2">
          {brand.name}
        </h3>
        <p className="text-amber-700 font-medium mb-3">{brand.tagline}</p>
        <p className="text-gray-600 mb-4 line-clamp-3">{brand.description}</p>

        <a
          href={brand.website}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center text-slate-900 font-semibold hover:text-amber-600 transition"
        >
          Visit Website
          <svg
            className="w-4 h-4 ml-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
        </a>
      </div>
    </div>
  );
}
