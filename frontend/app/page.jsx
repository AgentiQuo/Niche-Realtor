import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] text-center p-8">
      <h1 className="text-5xl font-extrabold text-blue-900 mb-6">Find Your Niche</h1>
      <p className="text-xl text-gray-600 mb-10 max-w-2xl">
        Experience AI-native real estate modeling matching your precise lifestyle vibes, curated properties, and qualitative neighborhood features.
      </p>
      
      <div className="flex gap-4">
        <Link href="/client" className="px-6 py-3 bg-blue-600 text-white font-bold rounded hover:bg-blue-700 transition shadow-lg">
          Onboard Profile
        </Link>
        <Link href="/niche/demo" className="px-6 py-3 bg-gray-200 text-gray-800 font-bold rounded hover:bg-gray-300 transition shadow-lg">
          Explore Niches
        </Link>
      </div>
    </div>
  );
}
