'use client';
import { useState } from 'react';
import MatchResultsList from '../../components/MatchResultsList';

export default function MatchPage() {
  const [clientId, setClientId] = useState('');
  const [nicheId, setNicheId] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleMatch = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ client_id: clientId, niche_id: nicheId })
      });
      const data = await response.json();
      setResults(data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-10">
      <div className="max-w-4xl mx-auto p-4 mb-8">
        <h1 className="text-3xl font-bold mb-4">Run Matching Engine</h1>
        <div className="flex gap-4 mb-4">
          <input type="text" placeholder="Client ID" className="border p-2 rounded flex-1" value={clientId} onChange={e => setClientId(e.target.value)} />
          <input type="text" placeholder="Niche ID" className="border p-2 rounded flex-1" value={nicheId} onChange={e => setNicheId(e.target.value)} />
          <button onClick={handleMatch} disabled={loading} className="bg-green-600 text-white px-6 py-2 rounded font-bold hover:bg-green-700 disabled:bg-green-300">
            {loading ? 'Matching...' : 'Find Matches'}
          </button>
        </div>
      </div>

      {results && <MatchResultsList results={results.ranked_results.map((r, i) => ({ property: r, explanation: results.explanations[i] }))} />}
    </div>
  );
}
