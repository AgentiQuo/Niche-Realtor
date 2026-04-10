export default function NeighborhoodCard({ neighborhood }) {
  return (
    <div className="border border-green-200 rounded p-4 bg-green-50">
      <h3 className="font-bold text-xl">{neighborhood?.name || 'Neighborhood Name'}</h3>
      <p className="text-sm text-gray-500 mb-2">{neighborhood?.region || 'Region'}</p>
      <p className="text-gray-700 italic">"{neighborhood?.vibe_summary || 'Vibe summary goes here...'}"</p>
    </div>
  );
}
