import Image from "next/image";
import { Users, Heart, Shield, Award, CheckCircle } from "lucide-react";

export const metadata = {
  title: "About Us - Open Path Care",
  description:
    "Learn about our mission to support Australians with disabilities",
};

export default function AboutPage() {
  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 text-white py-20 md:py-28">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            About <span className="text-blue-200">Open Path Care</span>
          </h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto leading-relaxed">
            We are passionate about supporting Australians with disabilities to
            live their best lives. Our person-centered approach ensures every
            individual receives the care and support they deserve.
          </p>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 md:py-28 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-6">
              <h2 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight">
                Our <span className="text-blue-600">Mission</span>
              </h2>
              <p className="text-lg text-gray-600 leading-relaxed">
                At Open Path Care, we believe that every individual has the
                right to live independently, confidently, and with dignity. Our
                mission is to provide high-quality, person-centered support
                services that empower people with disabilities to achieve their
                personal goals and participate fully in their communities.
              </p>
              <p className="text-lg text-gray-600 leading-relaxed">
                We are committed to creating meaningful opportunities for
                growth, independence, and community connection. Our experienced
                team works closely with each person to develop personalized
                support plans that reflect their unique needs, preferences, and
                aspirations.
              </p>
            </div>
            <div className="relative">
              <Image
                src="/About_us.png"
                alt="About Open Path Care - Our Mission"
                width={600}
                height={500}
                className="rounded-2xl shadow-xl"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 md:py-28 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Our <span className="text-blue-600">Values</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              These core values guide everything we do and shape how we deliver
              our services.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-white p-8 rounded-2xl shadow-lg text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Users className="text-blue-600" size={32} />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Person-Centered
              </h3>
              <p className="text-gray-600">
                Every individual is unique. We tailor our services to meet your
                specific needs, goals, and preferences.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-lg text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Heart className="text-blue-600" size={32} />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Compassionate
              </h3>
              <p className="text-gray-600">
                We provide caring, respectful support that recognizes your
                dignity and worth as an individual.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-lg text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Shield className="text-blue-600" size={32} />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Reliable</h3>
              <p className="text-gray-600">
                You can count on us to be there when you need us, providing
                consistent, high-quality support.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-lg text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Award className="text-blue-600" size={32} />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Excellence
              </h3>
              <p className="text-gray-600">
                We strive for excellence in everything we do, continuously
                improving our services and outcomes.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 md:py-28 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Meet Our <span className="text-blue-600">Team</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our dedicated professionals are passionate about making a positive
              difference in your life.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-gray-50 rounded-2xl p-8 text-center">
              <div className="relative w-32 h-32 mx-auto mb-6">
                <Image
                  src="/Tony-Osmani.jpg"
                  alt="Tony Osmani - Founder & CEO"
                  width={128}
                  height={128}
                  className="rounded-full object-cover"
                />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Tony Osmani
              </h3>
              <p className="text-blue-600 font-semibold mb-4">Founder & CEO</p>
              <p className="text-gray-600 text-sm">
                With over 15 years of experience in disability support, Tony
                founded Open Path Care to create meaningful opportunities for
                people with disabilities.
              </p>
            </div>

            <div className="bg-gray-50 rounded-2xl p-8 text-center">
              <div className="relative w-32 h-32 mx-auto mb-6">
                <Image
                  src="/placeholder-user.jpg"
                  alt="Sarah Johnson - Operations Manager"
                  width={128}
                  height={128}
                  className="rounded-full object-cover"
                />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Sarah Johnson
              </h3>
              <p className="text-blue-600 font-semibold mb-4">
                Operations Manager
              </p>
              <p className="text-gray-600 text-sm">
                Sarah ensures our services run smoothly and efficiently,
                coordinating support delivery and maintaining the highest
                quality standards.
              </p>
            </div>

            <div className="bg-gray-50 rounded-2xl p-8 text-center">
              <div className="relative w-32 h-32 mx-auto mb-6">
                <Image
                  src="/placeholder-user.jpg"
                  alt="Michael Chen - Senior Support Coordinator"
                  width={128}
                  height={128}
                  className="rounded-full object-cover"
                />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Michael Chen
              </h3>
              <p className="text-blue-600 font-semibold mb-4">
                Senior Support Coordinator
              </p>
              <p className="text-gray-600 text-sm">
                Michael works closely with participants to develop personalized
                support plans and navigate the NDIS system effectively.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* NDIS Registration Section */}
      <section className="py-20 md:py-28 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl p-8 md:p-12 shadow-lg">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              <div>
                <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
                  NDIS{" "}
                  <span className="text-blue-600">Registered Provider</span>
                </h2>
                <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                  Open Path Care is a registered NDIS provider, meeting the
                  highest standards of quality and safety in disability support
                  services. Our registration ensures that you receive
                  professional, reliable support that meets NDIS requirements.
                </p>
                <div className="space-y-4">
                  <div className="flex items-start gap-3">
                    <CheckCircle
                      className="text-blue-600 flex-shrink-0 mt-1"
                      size={20}
                    />
                    <span className="text-gray-700">
                      Fully registered NDIS provider
                    </span>
                  </div>
                  <div className="flex items-start gap-3">
                    <CheckCircle
                      className="text-blue-600 flex-shrink-0 mt-1"
                      size={20}
                    />
                    <span className="text-gray-700">
                      Compliant with NDIS Quality and Safeguards Commission
                    </span>
                  </div>
                  <div className="flex items-start gap-3">
                    <CheckCircle
                      className="text-blue-600 flex-shrink-0 mt-1"
                      size={20}
                    />
                    <span className="text-gray-700">
                      Regular audits and quality assessments
                    </span>
                  </div>
                  <div className="flex items-start gap-3">
                    <CheckCircle
                      className="text-blue-600 flex-shrink-0 mt-1"
                      size={20}
                    />
                    <span className="text-gray-700">
                      Trained and qualified support workers
                    </span>
                  </div>
                </div>
              </div>
              <div className="bg-blue-50 rounded-2xl p-8 text-center">
                <div className="bg-blue-100 w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Award className="text-blue-600" size={48} />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">
                  NDIS Provider Number
                </h3>
                <p className="text-3xl font-bold text-blue-600 mb-4">
                  4050001234
                </p>
                <p className="text-gray-600">
                  Registered since 2010, serving participants across Australia
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
