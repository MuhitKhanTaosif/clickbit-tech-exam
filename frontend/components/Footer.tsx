import Link from "next/link";
import Image from "next/image";
import {
  Mail,
  Phone,
  MapPin,
  Facebook,
  Twitter,
  Linkedin,
  Instagram,
} from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          {/* Company Info */}
          <div className="md:col-span-1">
            <div className="flex items-center gap-3 mb-6">
              <Image
                src="/white-logo.png"
                alt="Open Path Care"
                width={50}
                height={50}
                className="h-12 w-auto"
              />
              <div>
                <span className="font-bold text-xl">Open Path Care</span>
                <p className="text-sm text-gray-400">NDIS Services</p>
              </div>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed mb-6">
              Supporting Australians with disabilities to live independently and
              with dignity through comprehensive NDIS services.
            </p>
            <div className="flex gap-4">
              <Link
                href="#"
                className="text-gray-400 hover:text-white transition"
              >
                <Facebook size={20} />
              </Link>
              <Link
                href="#"
                className="text-gray-400 hover:text-white transition"
              >
                <Twitter size={20} />
              </Link>
              <Link
                href="#"
                className="text-gray-400 hover:text-white transition"
              >
                <Linkedin size={20} />
              </Link>
              <Link
                href="#"
                className="text-gray-400 hover:text-white transition"
              >
                <Instagram size={20} />
              </Link>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-bold text-lg mb-6">Quick Links</h3>
            <ul className="space-y-3">
              <li>
                <Link
                  href="/"
                  className="text-gray-400 hover:text-white transition text-sm"
                >
                  Home
                </Link>
              </li>
              <li>
                <Link
                  href="/services"
                  className="text-gray-400 hover:text-white transition text-sm"
                >
                  Services
                </Link>
              </li>
              <li>
                <Link
                  href="/about"
                  className="text-gray-400 hover:text-white transition text-sm"
                >
                  About Us
                </Link>
              </li>
              <li>
                <Link
                  href="/contact"
                  className="text-gray-400 hover:text-white transition text-sm"
                >
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Services */}
          <div>
            <h3 className="font-bold text-lg mb-6">Our Services</h3>
            <ul className="space-y-3">
              <li>
                <Link
                  href="/service/assist-access-maintain-employment"
                  className="text-gray-400 hover:text-white transition text-sm"
                >
                  Employment Support
                </Link>
              </li>
              <li>
                <Link
                  href="/service/assist-personal-activities"
                  className="text-gray-400 hover:text-white transition text-sm"
                >
                  Personal Care
                </Link>
              </li>
              <li>
                <Link
                  href="/service/innovative-community-participation"
                  className="text-gray-400 hover:text-white transition text-sm"
                >
                  Community Participation
                </Link>
              </li>
              <li>
                <Link
                  href="/service/assist-travel-and-transport"
                  className="text-gray-400 hover:text-white transition text-sm"
                >
                  Travel & Transport
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="font-bold text-lg mb-6">Contact Us</h3>
            <ul className="space-y-4">
              <li className="flex items-start gap-3">
                <Phone size={18} className="mt-1 flex-shrink-0 text-blue-400" />
                <div>
                  <span className="text-white font-medium block">Phone</span>
                  <span className="text-gray-400 text-sm">1300 123 456</span>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <Mail size={18} className="mt-1 flex-shrink-0 text-blue-400" />
                <div>
                  <span className="text-white font-medium block">Email</span>
                  <span className="text-gray-400 text-sm">
                    info@openpathcare.com.au
                  </span>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <MapPin
                  size={18}
                  className="mt-1 flex-shrink-0 text-blue-400"
                />
                <div>
                  <span className="text-white font-medium block">Location</span>
                  <span className="text-gray-400 text-sm">Australia Wide</span>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-gray-400 text-sm">
              © 2025 Open Path Care. All rights reserved. | NDIS Provider
              Number: 4050001234
            </p>
            <div className="flex gap-6 text-sm">
              <Link
                href="#"
                className="text-gray-400 hover:text-white transition"
              >
                Privacy Policy
              </Link>
              <Link
                href="#"
                className="text-gray-400 hover:text-white transition"
              >
                Terms of Service
              </Link>
              <Link
                href="#"
                className="text-gray-400 hover:text-white transition"
              >
                Accessibility
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
