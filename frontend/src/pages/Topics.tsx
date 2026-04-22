import { useState, useEffect } from 'react';
import { TopicCard } from '../components/TopicCard';
import { fetchTopics } from '../api/client';
import type { TopicsResponse } from '../types';
import './Topics.css';

export function Topics() {
  const [data, setData] = useState<TopicsResponse | null>(null);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetchTopics(page)
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [page]);

  return (
    <div className="topics-page">
      <div className="topics-heading">
        <h1 className="topics-title">话题聚合</h1>
        <p className="topics-subtitle">同一事件多源报道 · 自动归并去噪</p>
      </div>

      {loading && <div className="topics-loading">LOADING…</div>}

      {!loading && data && data.items.length === 0 && (
        <div className="topics-empty">NO TOPICS YET — 触发抓取后话题将自动聚合</div>
      )}

      <div className="topics-grid">
        {data?.items.map((topic) => (
          <TopicCard key={topic.id} topic={topic} />
        ))}
      </div>

      {data && data.items.length > 0 && (
        <div className="topics-pagination">
          <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page === 1} className="page-btn">← 上一页</button>
          <span className="page-info">P.{page}</span>
          <button onClick={() => setPage((p) => p + 1)} disabled={data.items.length < 20} className="page-btn">下一页 →</button>
        </div>
      )}
    </div>
  );
}
