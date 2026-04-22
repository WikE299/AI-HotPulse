import axios from 'axios';
import type { Article, ArticlesResponse, FilterParams, TopicsResponse, TopicDetail, Brief, ModelRelease } from '../types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
});

export async function fetchArticles(params: FilterParams): Promise<ArticlesResponse> {
  const { data } = await api.get<ArticlesResponse>('/articles', { params });
  return data;
}

export async function fetchTopArticles(limit = 10): Promise<Article[]> {
  const { data } = await api.get<Article[]>('/articles/top', { params: { limit } });
  return data;
}

export async function fetchArticle(id: string): Promise<Article> {
  const { data } = await api.get<Article>(`/articles/${id}`);
  return data;
}

export async function fetchPapers(page = 1, pageSize = 20): Promise<ArticlesResponse> {
  const { data } = await api.get<ArticlesResponse>('/articles', {
    params: { source_type: 'academic', page, page_size: pageSize },
  });
  return data;
}

export async function fetchTopics(page = 1, pageSize = 20): Promise<TopicsResponse> {
  const { data } = await api.get<TopicsResponse>('/topics', { params: { page, page_size: pageSize } });
  return data;
}

export async function fetchTopic(id: string): Promise<TopicDetail> {
  const { data } = await api.get<TopicDetail>(`/topics/${id}`);
  return data;
}

export async function fetchLatestBrief(): Promise<Brief> {
  const { data } = await api.get<Brief>('/briefs/latest');
  return data;
}

export async function fetchBrief(date: string): Promise<Brief> {
  const { data } = await api.get<Brief>(`/briefs/${date}`);
  return data;
}

export async function generateBrief(): Promise<Brief> {
  const { data } = await api.post<Brief>('/briefs/generate');
  return data;
}

export async function triggerCrawl() {
  const { data } = await api.post('/crawl/trigger');
  return data;
}

export async function fetchModelReleases(organization?: string): Promise<ModelRelease[]> {
  const { data } = await api.get<ModelRelease[]>('/model-releases', {
    params: organization ? { organization } : {},
  });
  return data;
}
