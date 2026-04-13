const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Tag {
  name: string;
  polarity?: string;
  relevance?: number;
  confidence?: number;
  source?: string;
}

export interface Neighborhood {
  name: string;
  location?: string;
  description?: string;
  relevance_score?: number;
}

export interface Niche {
  niche_id: string;
  name: string;
  description: string;
  tags: Tag[];
  neighborhoods: Neighborhood[];
  sources: string[];
  similarity_score?: number;
}

export async function searchNiches(query: string, limit: number = 10): Promise<Niche[]> {
  const response = await fetch(`${API_URL}/niche/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query, limit }),
  });

  if (!response.ok) {
    throw new Error(`Failed to search niches: ${response.statusText}`);
  }

  return response.json();
}

export async function listNiches(page: number = 1, limit: number = 50): Promise<Niche[]> {
  const response = await fetch(`${API_URL}/niche/list?page=${page}&limit=${limit}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to list niches: ${response.statusText}`);
  }

  return response.json();
}
