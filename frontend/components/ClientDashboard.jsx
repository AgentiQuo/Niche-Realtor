import PropertyCard from './PropertyCard';

export default function ClientDashboard({ client, savedProperties, recommendedProperties }) {
  return (
    <div className="p-8 max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Welcome Back</h1>
        <button className="bg-gray-200 px-4 py-2 rounded text-sm hover:bg-gray-300">Adjust Preferences</button>
      </div>

      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-4">Saved Properties</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {savedProperties?.map(prop => <PropertyCard key={prop.property_id} property={prop} />)}
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-bold mb-4">New Recommendations For You</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {recommendedProperties?.map(prop => <PropertyCard key={prop.property_id} property={prop} />)}
        </div>
      </section>
    </div>
  );
}
