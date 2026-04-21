import { useEffect, useState, useCallback } from 'react';
import { ArticleCard } from '../components/ArticleCard';
import { FilterBar } from '../components/FilterBar';
import { TopList } from '../components/TopList';
import { fetchArticles } from '../api/client';
import type { Article } from '../types';
import './Home.css';

export function Home() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [sourceType, setSourceType] = useState('');
  const [category, setCategory] = useState('');

  const load = useCallback(async (p: number, reset: boolean) => {
    setLoading(true);
    try {
      const res = await fetchArticles({ page: p, source_type: sourceType || undefined, category: category || undefined });
      if (reset) {
        setArticles(res.items);
      } else {
        setArticles((prev) => [...prev, ...res.items]);
      }
      setHasMore(res.items.length === res.page_size);
    } finally {
      setLoading(false);
    }
  }, [sourceType, category]);

  useEffect(() => {
    setPage(1);
    load(1, true);
  }, [sourceType, category]);

  const loadMore = () => {
    const next = page + 1;
    setPage(next);
    load(next, false);
  };

  return (
    <div className="home">
      <TopList />

      <FilterBar
        sourceType={sourceType}
        category={category}
        onSourceTypeChange={(v) => setSourceType(v)}
        onCategoryChange={(v) => setCategory(v)}
      />

      {loading && articles.length === 0 ? (
        <div className="loading">加载中...</div>
      ) : articles.length === 0 ? (
        <div className="empty">暂无数据，点击「立即抓取」开始采集</div>
      ) : (
        <>
          <div className="articles-grid">
            {articles.map((a) => (
              <ArticleCard key={a.id} article={a} />
            ))}
          </div>
          {hasMore && (
            <button className="load-more" onClick={loadMore} disabled={loading}>
              {loading ? '加载中...' : '加载更多'}
            </button>
          )}
        </>
      )}
    </div>
  );
}
