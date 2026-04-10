import NicheTagCloud from './NicheTagCloud';
import NicheEmbeddingVisualizer from './NicheEmbeddingVisualizer';

export default function NeighborhoodDetailPage({ neighborhood }) {
  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-4xl font-bold">{neighborhood?.name}</h1>
      <p className="text-lg text-gray-600 mt-2">{neighborhood?.region}</p>
      
      <div className="mt-8 bg-blue-50 p-6 rounded italic text-gray-800 border-l-4 border-blue-500">
        {neighborhood?.vibe_summary}
      </div>

      <div className="mt-8">
        <h2 className="text-2xl font-bold mb-4">Vibe Profile</h2>
        <NicheTagCloud tags={neighborhood?.tags} />
      </div>

      <div className="mt-8">
        <h2 className="text-2xl font-bold mb-4">Similar Neighborhoods</h2>
        {/* Grid of similar neighborhoods */}
      </div>
    </div>
  );
}
