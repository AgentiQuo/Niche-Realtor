import { listNiches, Niche } from '@/lib/api';
import Link from 'next/link';
import { notFound } from 'next/navigation';

interface NicheDetailProps {
  params: Promise<{ id: string }>;
}

export default async function NicheDetailPage({ params }: NicheDetailProps) {
  const { id } = await params;
  
  let niche: Niche | undefined;
  try {
    const allNiches = await listNiches(1, 100); // Fetch up to 100 to be safe
    niche = allNiches.find((n) => n.niche_id === id);
  } catch (error) {
    console.error('Failed to fetch niche details:', error);
  }

  if (!niche) {
    notFound();
  }

  return (
    <div className="min-h-screen bg-zinc-50 px-6 py-12 dark:bg-black">
      <div className="mx-auto max-w-4xl">
        <Link 
          href="/" 
          className="mb-8 inline-flex items-center gap-2 text-sm font-medium text-zinc-600 hover:text-blue-600 dark:text-zinc-400 dark:hover:text-blue-400"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m15 18-6-6 6-6"/></svg>
          Back to Search
        </Link>

        <article className="rounded-3xl border border-zinc-200 bg-white p-8 shadow-sm dark:border-zinc-800 dark:bg-zinc-900 sm:p-12">
          <header className="mb-10">
            <h1 className="mb-4 text-4xl font-extrabold text-zinc-900 dark:text-zinc-50">
              {niche.name}
            </h1>
            <p className="text-xl leading-relaxed text-zinc-600 dark:text-zinc-400">
              {niche.description}
            </p>
          </header>

          <div className="grid gap-12 md:grid-cols-2">
            <section>
              <h2 className="mb-4 flex items-center gap-2 text-lg font-bold text-zinc-900 dark:text-zinc-50">
                <span className="h-2 w-2 rounded-full bg-blue-500"></span>
                Key Attributes
              </h2>
              <div className="flex flex-wrap gap-2 text-xs">
                {niche.tags.map((tag, idx) => (
                  <div 
                    key={idx}
                    className="flex items-center gap-2 rounded-lg bg-zinc-100 px-3 py-2 dark:bg-zinc-800"
                  >
                    <span className="font-semibold text-zinc-800 dark:text-zinc-200">{tag.name}</span>
                    <span className="text-zinc-500 opacity-70">{tag.polarity === 'positive' ? '✓' : '×'}</span>
                  </div>
                ))}
              </div>
            </section>

            <section>
              <h2 className="mb-4 flex items-center gap-2 text-lg font-bold text-zinc-900 dark:text-zinc-50">
                <span className="h-2 w-2 rounded-full bg-green-500"></span>
                Primary Neighborhoods
              </h2>
              <ul className="space-y-3">
                {niche.neighborhoods.length > 0 ? (
                  niche.neighborhoods.map((nh, idx) => (
                    <li key={idx} className="flex flex-col gap-1 rounded-xl border border-zinc-100 p-3 dark:border-zinc-800">
                      <span className="font-bold text-zinc-800 dark:text-zinc-200">{nh.name}</span>
                      {nh.location && <span className="text-sm text-zinc-500">{nh.location}</span>}
                    </li>
                  ))
                ) : (
                  <p className="text-sm italic text-zinc-500">No neighborhood associations mapped yet.</p>
                )}
              </ul>
            </section>
          </div>

          {niche.sources && niche.sources.length > 0 && (
            <footer className="mt-12 border-t border-zinc-100 pt-8 dark:border-zinc-800">
              <h2 className="mb-4 text-sm font-bold uppercase tracking-wider text-zinc-500">
                Sources & Intelligence
              </h2>
              <div className="flex flex-wrap gap-3">
                {niche.sources.map((source, idx) => (
                  <span 
                    key={idx}
                    className="text-sm text-blue-600 underline decoration-blue-200 underline-offset-4 hover:decoration-blue-600 dark:text-blue-400 dark:decoration-blue-900"
                  >
                    {source}
                  </span>
                ))}
              </div>
            </footer>
          )}
        </article>
      </div>
    </div>
  );
}
