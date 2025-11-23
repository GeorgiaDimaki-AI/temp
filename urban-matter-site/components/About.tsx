import { siteConfig } from "@/config/site.config";

export default function About() {
  return (
    <section id="about" className="py-20 bg-slate-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-6">
            About {siteConfig.companyName}
          </h2>
          <div className="text-lg text-slate-700 space-y-4">
            <p>
              We are passionate about creating and nurturing exceptional food
              brands that bring joy and flavor to people's lives. Each brand in
              our portfolio represents our commitment to quality, authenticity,
              and innovation.
            </p>
            <p>
              Our approach combines traditional craftsmanship with modern
              techniques, ensuring that every product we create meets the
              highest standards of excellence.
            </p>
            <p>
              From sourcing the finest ingredients to crafting unique flavor
              profiles, we pay attention to every detail. Our brands are more
              than just products—they're experiences that connect people through
              the universal language of great food.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
