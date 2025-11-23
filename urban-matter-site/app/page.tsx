import { siteConfig } from "@/config/site.config";
import BrandsGrid from "@/components/BrandsGrid";
import Hero from "@/components/Hero";
import About from "@/components/About";
import Contact from "@/components/Contact";

export default function Home() {
  return (
    <>
      <Hero />
      <BrandsGrid />
      <About />
      <Contact />
    </>
  );
}
