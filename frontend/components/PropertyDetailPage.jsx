import ImageCarousel from './ImageCarousel';
import NicheTagCloud from './NicheTagCloud';

export default function PropertyDetailPage({ property }) {
  return (
    <div className="property-detail p-8 max-w-4xl mx-auto">
      <ImageCarousel images={property?.images || []} />
      <div className="mt-8">
        <h1 className="text-3xl font-bold">{property?.location || 'Property Location'}</h1>
        <div className="mt-4">
          <NicheTagCloud tags={property?.tags || []} />
        </div>
        {/* Further Details: Embedding Vis, Neighborhood Context */}
      </div>
    </div>
  );
}
