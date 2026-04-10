'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import NeighborhoodDetailPage from '../../../components/NeighborhoodDetailPage';

export default function NeighborhoodViewPage() {
  const params = useParams();
  const [neighborhood, setNeighborhood] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const scoutNeighborhood = async () => {
      setLoading(true);
      try {
        const response = await fetch('http://localhost:8000/neighborhood/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ neighborhood_name: decodeURIComponent(params.id), region: "Default Region" })
        });
        const data = await response.json();
        setNeighborhood({
          neighborhood_id: params.id,
          name: decodeURIComponent(params.id),
          region: "Default Region",
          tags: data.tags,
          vibe_summary: data.vibe_summary
        });
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    };

    if (params.id) {
      scoutNeighborhood();
    }
  }, [params.id]);

  if (loading) return <div className="text-center p-20">Scouting latest neighborhood intelligence...</div>;
  if (!neighborhood) return null;

  return <NeighborhoodDetailPage neighborhood={neighborhood} />;
}
