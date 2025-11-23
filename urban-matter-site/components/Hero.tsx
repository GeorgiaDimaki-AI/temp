import { siteConfig } from "@/config/site.config";

export default function Hero() {
  return (
    <section className="relative bg-gradient-to-br from-slate-50 to-slate-100 py-20 md:py-32">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-5xl md:text-7xl font-bold text-slate-900 mb-6">
            {siteConfig.companyName}
          </h1>
          <p className="text-xl md:text-2xl text-slate-700 mb-8 max-w-3xl mx-auto">
            {siteConfig.tagline}
          </p>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto mb-12">
            {siteConfig.description}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="#brands"
              className="inline-block bg-slate-900 text-white px-8 py-3 rounded-lg font-semibold hover:bg-slate-800 transition"
            >
              Explore Our Brands
            </a>
            <a
              href="#contact"
              className="inline-block bg-white text-slate-900 px-8 py-3 rounded-lg font-semibold border-2 border-slate-900 hover:bg-slate-50 transition"
            >
              Get in Touch
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
