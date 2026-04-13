import Link from 'next/link';
import { Niche } from '@/lib/api';

interface NicheCardProps {
  niche: Niche;
}

export default function NicheCard({ niche }: NicheCardProps) {
  const { niche_id, name, description, similarity_score } = niche;

  return (
    <div className="group relative overflow-hidden rounded-2xl border border-zinc-200 bg-white p-6 transition-all hover:border-blue-300 hover:shadow-xl dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-blue-700">
      <div className="flex flex-col gap-3">
        <div className="flex items-start justify-between">
          <h3 className="text-xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
            {name}
          </h3>
          {similarity_score !== undefined && (
            <div className="flex items-center gap-1 rounded-full bg-blue-50 px-3 py-1 text-sm font-semibold text-blue-600 dark:bg-blue-900/30 dark:text-blue-400">
              <span className="text-xs opacity-70">Match:</span>
              {(similarity_score * 100).toFixed(1)}%
            </div>
          )}
        </div>
        
        <p className="line-clamp-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
          {description}
        </p>

        <div className="mt-4 flex flex-wrap gap-2">
          {niche.tags?.slice(0, 3).map((tag, idx) => (
            <span 
              key={idx} 
              className="rounded-md bg-zinc-100 px-2 py-0.5 text-xs font-medium text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300"
            >
              #{tag.name}
            </span>
          ))}
        </div>

        <Link
          href={`/niche/${niche_id}`}
          className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-blue-600 transition-colors hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300"
        >
          View Details
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="transition-transform group-hover:translate-x-1"
          >
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </Link>
      </div>
    </div>
  );
}
