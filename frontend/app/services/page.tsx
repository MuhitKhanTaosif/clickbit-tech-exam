import { servicesData } from "@/lib/services";
import ServiceCard from "@/components/ServiceCard";

export const metadata = {
  title: "Services - Open Path Care",
  description: "Explore our comprehensive NDIS services",
};

export default function ServicesPage() {
  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 text-white py-20 md:py-28">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            Our <span className="text-blue-200">Services</span>
          </h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto leading-relaxed">
            Comprehensive NDIS support services designed to empower you and help
            you achieve your personal goals. We offer a wide range of
            person-centered services tailored to your unique needs.
          </p>
        </div>
      </section>

      {/* Services Grid */}
      <section className="py-20 md:py-28 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              NDIS Support Services
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              All our services are delivered by qualified professionals who
              understand the NDIS and are committed to your success.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {servicesData.map((service) => (
              <ServiceCard key={service.id} service={service} />
            ))}
          </div>
        </div>
      </section>

      {/* Why Choose Us Section */}
      <section className="py-20 md:py-28 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
              Why Choose Open Path Care?
            </h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              We're committed to providing exceptional NDIS services that make a
              real difference in your life.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-2xl shadow-lg text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-blue-600">15+</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Years of Experience
              </h3>
              <p className="text-gray-600">
                Over a decade of experience in providing quality disability
                support services across Australia.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-lg text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-blue-600">500+</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Clients Supported
              </h3>
              <p className="text-gray-600">
                We've helped hundreds of individuals achieve their goals and
                live more independently.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-lg text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-blue-600">24/7</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Support Available
              </h3>
              <p className="text-gray-600">
                Round-the-clock support when you need it most, ensuring you're
                never alone in your journey.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
