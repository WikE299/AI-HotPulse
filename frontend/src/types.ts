export interface Article {
  id: string;
  title: string;
  source: string | null;
  source_type: 'chinese' | 'english' | 'academic' | 'social' | null;
  original_url: string;
  published_at: string | null;
  image_url: string | null;
  summary: string | null;
  keywords: string[];
  category: string | null;
  heat_score: number;
  content_snippet: string | null;
}

export interface ArticlesResponse {
  items: Article[];
  page: number;
  page_size: number;
}

export interface FilterParams {
  page?: number;
  source_type?: string;
  category?: string;
  date_from?: string;
  date_to?: string;
}
