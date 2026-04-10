import PropertyCard from './PropertyCard';
import MatchExplanationBox from './MatchExplanationBox';

export default function MatchResultsList({ results }) {
  if (!results || results.length === 0) return <div className="p-8 text-center text-gray-500">No matches found.</div>;

  return (
    <div className="flex flex-col gap-8 max-w-5xl mx-auto p-4">
      {results.map((result, index) => (
        <div key={index} className="flex flex-col md:flex-row gap-6 border rounded-lg p-6 bg-white shadow-sm">
          <div className="flex-1">
            <PropertyCard property={result.property} />
          </div>
          <div className="flex-1">
            <MatchExplanationBox explanation={result.explanation} />
          </div>
        </div>
      ))}
    </div>
  );
}
