'use client';

import { useState } from 'react';
import { searchNiches, Niche } from '@/lib/api';
import NicheCard from '@/components/NicheCard';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Niche[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setHasSearched(true);
    try {
      const data = await searchNiches(query);
      setResults(data);
    } catch (error) {
      console.error('Search failed:', error);
      // Fallback/error handling could be added here
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-50 px-6 py-12 dark:bg-black">
      <div className="mx-auto max-w-4xl">
        <header className="mb-12 text-center">
          <h1 className="mb-4 text-5xl font-extrabold tracking-tight text-zinc-900 dark:text-zinc-50">
            Find Your <span className="text-blue-600">Niche</span>
          </h1>
          <p className="mx-auto max-w-2xl text-lg text-zinc-600 dark:text-zinc-400">
            Describe your ideal lifestyle, vibe, or specific neighborhood preferences. 
            Our AI will match you with the perfect real estate niche.
          </p>
        </header>

        <section className="mb-16">
          <form onSubmit={handleSearch} className="relative flex gap-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. 'Quiet digital nomad hubs with great coffee and tech scene'..."
              className="w-full rounded-2xl border border-zinc-200 bg-white px-6 py-4 text-base shadow-sm ring-blue-500 transition-all focus:border-blue-500 focus:outline-none focus:ring-2 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-50"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading}
              className="flex items-center justify-center rounded-2xl bg-blue-600 px-8 py-4 font-bold text-white transition-all hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
            >
              {isLoading ? (
                <div className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent" />
              ) : (
                'Search'
              )}
            </button>
          </form>
        </section>

        <main>
          {isLoading ? (
            <div className="grid gap-6 sm:grid-cols-2">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-48 animate-pulse rounded-2xl bg-zinc-200 dark:bg-zinc-800" />
              ))}
            </div>
          ) : results.length > 0 ? (
            <div className="grid gap-6 sm:grid-cols-2">
              {results.map((niche) => (
                <NicheCard key={niche.niche_id} niche={niche} />
              ))}
            </div>
          ) : hasSearched ? (
            <div className="rounded-2xl border border-dashed border-zinc-300 p-12 text-center dark:border-zinc-700">
              <h3 className="text-xl font-semibold text-zinc-900 dark:text-zinc-50">No niches found</h3>
              <p className="mt-2 text-zinc-600 dark:text-zinc-400">Try adjusting your search terms or be more descriptive.</p>
            </div>
          ) : (
             <div className="rounded-2xl bg-white p-8 text-center shadow-sm dark:bg-zinc-900">
                <p className="text-zinc-500 dark:text-zinc-400italic">Type above to explore semantic niches...</p>
             </div>
          )}
        </main>
      </div>
    </div>
  );
}
