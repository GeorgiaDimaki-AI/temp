import { siteConfig } from "@/config/site.config";

export default function Contact() {
  return (
    <section id="contact" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4">
              Get in Touch
            </h2>
            <p className="text-xl text-slate-600">
              Interested in our brands or want to explore partnership
              opportunities?
            </p>
          </div>

          <div className="bg-slate-50 rounded-xl p-8 md:p-12">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-lg font-semibold text-slate-900 mb-2">
                  Email
                </h3>
                <a
                  href={`mailto:${siteConfig.email}`}
                  className="text-amber-600 hover:text-amber-700 transition"
                >
                  {siteConfig.email}
                </a>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-slate-900 mb-2">
                  Phone
                </h3>
                <a
                  href={`tel:${siteConfig.phone}`}
                  className="text-amber-600 hover:text-amber-700 transition"
                >
                  {siteConfig.phone}
                </a>
              </div>

              <div className="md:col-span-2">
                <h3 className="text-lg font-semibold text-slate-900 mb-2">
                  Address
                </h3>
                <p className="text-slate-700">{siteConfig.address}</p>
              </div>
            </div>

            <div className="mt-8 pt-8 border-t border-gray-200">
              <p className="text-center text-gray-600">
                We typically respond within 24-48 hours during business days.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
