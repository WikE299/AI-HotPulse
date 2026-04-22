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
  paper_contribution: string | null;
  readability_score: number | null;
  topic_id: string | null;
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

export interface Topic {
  id: string;
  topic_key: string;
  title: string;
  summary: string | null;
  article_count: number;
  heat_score: number;
  representative_id: string | null;
  first_seen_at: string | null;
  latest_at: string | null;
}

export interface TopicsResponse {
  items: Topic[];
  page: number;
  page_size: number;
}

export interface TopicDetail extends Topic {
  articles: Article[];
}

export interface Brief {
  id: string;
  date: string;
  content: string;
  article_ids: string;
  generated_at: string | null;
}

export interface Benchmarks {
  MMLU?: number;
  HumanEval?: number;
  MATH?: number;
  GSM8K?: number;
  ARC?: number;
  [key: string]: number | undefined;
}

export interface ModelRelease {
  id: string;
  model_name: string;
  organization: string;
  version: string | null;
  release_date: string;
  parameters_size: string | null;
  description: string | null;
  benchmarks: Benchmarks;
  announcement_url: string | null;
  category: string;
}
