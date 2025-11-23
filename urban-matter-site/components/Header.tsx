"use client";

import { siteConfig } from "@/config/site.config";
import { useState } from "react";

export default function Header() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex-shrink-0">
            <a href="/" className="text-2xl font-bold text-slate-900">
              {siteConfig.companyName}
            </a>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex space-x-8">
            <a
              href="#brands"
              className="text-gray-700 hover:text-slate-900 transition"
            >
              Our Brands
            </a>
            <a
              href="#about"
              className="text-gray-700 hover:text-slate-900 transition"
            >
              About
            </a>
            <a
              href="#contact"
              className="text-gray-700 hover:text-slate-900 transition"
            >
              Contact
            </a>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-700 hover:text-slate-900 focus:outline-none"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                {isOpen ? (
                  <path d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden pb-4">
            <a
              href="#brands"
              className="block py-2 text-gray-700 hover:text-slate-900"
              onClick={() => setIsOpen(false)}
            >
              Our Brands
            </a>
            <a
              href="#about"
              className="block py-2 text-gray-700 hover:text-slate-900"
              onClick={() => setIsOpen(false)}
            >
              About
            </a>
            <a
              href="#contact"
              className="block py-2 text-gray-700 hover:text-slate-900"
              onClick={() => setIsOpen(false)}
            >
              Contact
            </a>
          </div>
        )}
      </nav>
    </header>
  );
}
