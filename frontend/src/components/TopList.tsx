import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import dayjs from 'dayjs';
import { fetchTopArticles } from '../api/client';
import type { Article } from '../types';
import './TopList.css';

const SOURCE_TYPE_LABELS: Record<string, string> = {
  chinese: '中文', english: 'EN', academic: '学术', social: '社交',
};

export function TopList() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTopArticles(10).then(setArticles).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="top-loading">加载中...</div>;
  if (!articles.length) return null;

  return (
    <div className="top-list">
      <div className="top-header">
        <span className="top-title">🔥 今日 AI 热榜</span>
        <span className="top-sub">按热度排序</span>
      </div>
      <ol className="top-items">
        {articles.map((a, i) => (
          <li key={a.id} className={`top-item ${i < 3 ? 'top-item--podium' : ''}`}>
            <span className={`rank rank-${i + 1}`}>{i + 1}</span>
            <div className="top-item-body">
              <Link to={`/article/${a.id}`} className="top-item-title">
                {a.title}
              </Link>
              <div className="top-item-meta">
                {a.source_type && (
                  <span className="top-badge">{SOURCE_TYPE_LABELS[a.source_type] ?? a.source_type}</span>
                )}
                <span className="top-source">{a.source}</span>
                {a.published_at && (
                  <span className="top-time">{dayjs(a.published_at).format('MM-DD HH:mm')}</span>
                )}
                {a.heat_score > 0 && <span className="top-heat">热度 {a.heat_score}</span>}
              </div>
            </div>
            <a
              href={a.original_url}
              target="_blank"
              rel="noopener noreferrer"
              className="top-link"
              onClick={(e) => e.stopPropagation()}
            >
              ↗
            </a>
          </li>
        ))}
      </ol>
    </div>
  );
}
