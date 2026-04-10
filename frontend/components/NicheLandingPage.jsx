export default function NicheLandingPage({ niche }) {
  return (
    <div className="niche-landing">
      <section className="hero bg-blue-50 p-8 text-center">
        <h1 className="text-4xl font-bold">{niche?.name || 'Niche Name'}</h1>
        <p className="mt-4 text-gray-600">{niche?.description || 'Niche description goes here.'}</p>
      </section>
      <section className="highlights p-8">
        <h2 className="text-2xl font-bold mb-4">Highlights</h2>
        {/* Neighborhood and Property Highlights */}
      </section>
    </div>
  );
}
