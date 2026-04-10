export default function PropertyCard({ property }) {
  return (
    <div className="border rounded-lg overflow-hidden shadow-sm hover:shadow-md transition">
      <div className="h-48 bg-gray-200 object-cover flex items-center justify-center">
        {property?.images?.[0] ? <img src={property.images[0]} alt="Property" className="w-full h-full object-cover"/> : <span className="text-gray-400">Image</span>}
      </div>
      <div className="p-4">
        <h3 className="font-bold text-lg text-blue-900">${property?.price?.toLocaleString() || 'Price'}</h3>
        <p className="text-gray-600 truncate">{property?.location || 'Location'}</p>
        <div className="flex justify-between mt-2 text-sm text-gray-500">
          <span>{property?.beds || 0} Beds</span>
          <span>{property?.baths || 0} Baths</span>
          {property?.match_score && <span className="font-bold text-green-600">{Math.round(property.match_score * 100)}% Match</span>}
        </div>
      </div>
    </div>
  );
}
