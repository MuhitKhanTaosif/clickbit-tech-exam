import Link from "next/link";
import Image from "next/image";
import { CheckCircle, ArrowRight, Users, Heart, Shield } from "lucide-react";
import { servicesData } from "@/lib/services";
import ServiceCard from "@/components/ServiceCard";

export const metadata = {
  title: "Home - Open Path Care",
  description: "Supporting Australians with disabilities through NDIS services",
};

export default function HomePage() {
  const featuredServices = servicesData.slice(0, 6);

  return (
    <div>
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 text-white py-20 md:py-32 overflow-hidden">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="space-y-4">
                <h1 className="text-5xl md:text-6xl font-bold leading-tight">
                  Supporting You,{" "}
                  <span className="text-blue-200">Believing in You</span>
                </h1>
                <p className="text-xl text-blue-100 leading-relaxed">
                  At Open Path Care, we are dedicated to improving the lives of
                  individuals with disabilities. As one of the leading NDIS
                  service providers, we deliver compassionate, person-centered
                  care.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <Link
                  href="/contact"
                  className="inline-flex items-center justify-center bg-white text-blue-600 px-8 py-4 rounded-lg font-bold hover:bg-blue-50 transition text-lg"
                >
                  Get Started Today
                  <ArrowRight className="ml-2" size={20} />
                </Link>
                <Link
                  href="/services"
                  className="inline-flex items-center justify-center border-2 border-white text-white px-8 py-4 rounded-lg font-bold hover:bg-white hover:text-blue-600 transition text-lg"
                >
                  Our Services
                </Link>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-6 pt-8">
                <div className="text-center">
                  <div className="text-3xl font-bold">500+</div>
                  <div className="text-blue-200">Clients Served</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold">15+</div>
                  <div className="text-blue-200">Years Experience</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold">100%</div>
                  <div className="text-blue-200">NDIS Approved</div>
                </div>
              </div>
            </div>

            <div className="relative">
              <Image
                src="/Hero_Open_Path_Care.jpg"
                alt="Open Path Care - Supporting individuals with disabilities"
                width={600}
                height={500}
                className="rounded-2xl shadow-2xl"
                priority
              />
            </div>
          </div>
        </div>
      </section>

      {/* NDIS Section */}
      <section className="py-20 md:py-28 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div className="relative">
              <Image
                src="/Home-Page-2.jpg"
                alt="NDIS Support - Open Path Care"
                width={600}
                height={500}
                className="rounded-2xl shadow-xl"
              />
            </div>
            <div className="space-y-6">
              <div className="space-y-4">
                <h2 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight">
                  How does the <span className="text-blue-600">NDIS work?</span>
                </h2>
                <p className="text-lg text-gray-600 leading-relaxed">
                  The National Disability Insurance Scheme (NDIS) is an
                  Australian government initiative designed to support
                  individuals with permanent and significant disabilities. The
                  NDIS provides funding to assist individuals in achieving their
                  personal goals, increasing independence, and engaging with the
                  community.
                </p>
                <p className="text-lg text-gray-600 leading-relaxed">
                  A key feature of the NDIS is its flexibility, allowing
                  participants to select services that best meet their unique
                  needs and preferences. At Open Path Care, we guide
                  participants through the NDIS, helping them make the most of
                  their funding.
                </p>
              </div>

              <div className="space-y-4">
                <div className="flex items-start gap-4">
                  <div className="bg-blue-100 p-2 rounded-lg">
                    <CheckCircle className="text-blue-600" size={24} />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-1">
                      Personalized Support
                    </h3>
                    <p className="text-gray-600">
                      Tailored to your unique needs and goals
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="bg-blue-100 p-2 rounded-lg">
                    <CheckCircle className="text-blue-600" size={24} />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-1">
                      Expert Guidance
                    </h3>
                    <p className="text-gray-600">
                      Navigate the NDIS system with confidence
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="bg-blue-100 p-2 rounded-lg">
                    <CheckCircle className="text-blue-600" size={24} />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-1">
                      Comprehensive Options
                    </h3>
                    <p className="text-gray-600">
                      Full range of support services available
                    </p>
                  </div>
                </div>
              </div>

              <Link
                href="/services"
                className="inline-flex items-center text-blue-600 font-semibold hover:text-blue-700 transition"
              >
                Learn more about our services
                <ArrowRight className="ml-2" size={16} />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section className="py-20 md:py-28 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              About <span className="text-blue-600">Open Path Care</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
              At Open Path Care, we are dedicated to supporting Australians with
              disabilities in living independently, confidently, and with
              dignity. As an NDIS-approved provider, we focus on delivering
              tailored support to empower each individual.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-2xl shadow-lg text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Users className="text-blue-600" size={32} />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Person-Centered Care
              </h3>
              <p className="text-gray-600">
                Every individual is unique, and our approach reflects that. We
                tailor our services to meet your specific needs and goals.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-lg text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Heart className="text-blue-600" size={32} />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Compassionate Support
              </h3>
              <p className="text-gray-600">
                Our experienced team provides caring, respectful support that
                empowers you to live life on your terms.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-lg text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Shield className="text-blue-600" size={32} />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                NDIS Approved
              </h3>
              <p className="text-gray-600">
                As a registered NDIS provider, we meet the highest standards of
                quality and safety in disability support.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-20 md:py-28 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Our <span className="text-blue-600">Services</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Comprehensive NDIS support services tailored to your individual
              needs and goals
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
            {featuredServices.map((service) => (
              <ServiceCard key={service.id} service={service} />
            ))}
          </div>

          <div className="text-center">
            <Link
              href="/services"
              className="inline-flex items-center justify-center bg-blue-600 text-white px-8 py-4 rounded-lg font-bold hover:bg-blue-700 transition text-lg"
            >
              View All Services
              <ArrowRight className="ml-2" size={20} />
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 text-white py-20 md:py-28">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="max-w-4xl mx-auto space-y-8">
            <h2 className="text-4xl md:text-5xl font-bold leading-tight">
              Ready to Get Started?
            </h2>
            <p className="text-xl text-blue-100 leading-relaxed">
              Let us help you navigate your NDIS journey and achieve your
              personal goals. Our experienced team is here to support you every
              step of the way.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/contact"
                className="inline-flex items-center justify-center bg-white text-blue-600 px-8 py-4 rounded-lg font-bold hover:bg-blue-50 transition text-lg"
              >
                Contact Us Today
                <ArrowRight className="ml-2" size={20} />
              </Link>
              <Link
                href="/services"
                className="inline-flex items-center justify-center border-2 border-white text-white px-8 py-4 rounded-lg font-bold hover:bg-white hover:text-blue-600 transition text-lg"
              >
                Explore Services
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
