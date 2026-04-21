import axios from 'axios';
import type { ArticlesResponse, FilterParams } from '../types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
});

export async function fetchArticles(params: FilterParams): Promise<ArticlesResponse> {
  const { data } = await api.get<ArticlesResponse>('/articles', { params });
  return data;
}

export async function fetchArticle(id: string) {
  const { data } = await api.get(`/articles/${id}`);
  return data;
}

export async function triggerCrawl() {
  const { data } = await api.post('/crawl/trigger');
  return data;
}
