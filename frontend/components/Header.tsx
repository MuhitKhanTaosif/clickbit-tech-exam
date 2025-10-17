"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { Menu, X, Phone } from "lucide-react";
import { me } from "@/lib/api";

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const [userName, setUserName] = useState<string | null>(null);

  useEffect(() => {
    const t = localStorage.getItem("token");
    if (!t) return;
    setToken(t);
    me(t)
      .then((u) => setUserName(u.firstName))
      .catch(() => setUserName(null));
  }, []);

  return (
    <header className="bg-white shadow-lg sticky top-0 z-50">
      {/* Top Bar */}
      <div className="bg-blue-600 text-white py-2">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center text-sm">
            <div className="flex items-center gap-4">
              <span>Supporting Australians with disabilities</span>
            </div>
            <div className="flex items-center gap-2">
              <Phone size={16} />
              <span>1300 123 456</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Navigation */}
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3">
            <Image
              src="/logo-e1730191504760.png"
              alt="Open Path Care"
              width={60}
              height={60}
              className="h-12 w-auto"
            />
            <div className="hidden sm:block">
              <span className="font-bold text-xl text-gray-900">
                Open Path Care
              </span>
              <p className="text-sm text-gray-600">NDIS Services</p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            <Link
              href="/"
              className="text-gray-700 hover:text-blue-600 transition font-medium"
            >
              Home
            </Link>
            <Link
              href="/services"
              className="text-gray-700 hover:text-blue-600 transition font-medium"
            >
              Services
            </Link>
            <Link
              href="/about"
              className="text-gray-700 hover:text-blue-600 transition font-medium"
            >
              About
            </Link>
            <Link
              href="/contact"
              className="text-gray-700 hover:text-blue-600 transition font-medium"
            >
              Contact
            </Link>
            {userName ? (
              <div className="flex items-center gap-4">
                <span className="text-gray-700">Hi, {userName}!</span>
                <button
                  onClick={() => {
                    localStorage.removeItem("token");
                    location.href = "/";
                  }}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition font-medium"
                >
                  Logout
                </button>
              </div>
            ) : (
              <Link
                href="/auth/login"
                className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition font-medium"
              >
                Login
              </Link>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            aria-label="Toggle menu"
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden mt-4 pb-4 border-t pt-4">
            <Link
              href="/"
              className="block py-2 text-gray-700 hover:text-blue-600 font-medium"
            >
              Home
            </Link>
            <Link
              href="/services"
              className="block py-2 text-gray-700 hover:text-blue-600 font-medium"
            >
              Services
            </Link>
            <Link
              href="/about"
              className="block py-2 text-gray-700 hover:text-blue-600 font-medium"
            >
              About
            </Link>
            <Link
              href="/contact"
              className="block py-2 text-gray-700 hover:text-blue-600 font-medium"
            >
              Contact
            </Link>
            <Link
              href="/contact"
              className="block mt-4 bg-blue-600 text-white px-6 py-3 rounded-lg text-center hover:bg-blue-700 font-medium"
            >
              Get Started
            </Link>
          </div>
        )}
      </nav>
    </header>
  );
}
