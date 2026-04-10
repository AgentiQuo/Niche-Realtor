'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import PropertyDetailPage from '../../../components/PropertyDetailPage';

export default function PropertyViewPage() {
  const params = useParams();
  const [property, setProperty] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // In a real application, we would call GET /property/:id.
    // However, the BC-5 spec only provides POST /property/analyze.
    // For demonstration, we'll invoke the analysis endpoint to "retrieve" the property's tags.
    const runAnalysis = async () => {
      setLoading(true);
      try {
        const response = await fetch('http://localhost:8000/property/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ property_id: params.id })
        });
        const data = await response.json();
        setProperty({
          property_id: params.id,
          location: "Downtown Unit " + params.id.substring(0,4),
          images: ["https://via.placeholder.com/800x400"],
          tags: data.tags,
          embedding: data.embedding
        });
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    };
    
    if (params.id) {
      runAnalysis();
    }
  }, [params.id]);

  if (loading) return <div className="text-center p-20">Analyzing property signals...</div>;
  if (!property) return null;

  return <PropertyDetailPage property={property} />;
}
