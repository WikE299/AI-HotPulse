import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import dayjs from 'dayjs';
import { fetchTopArticles } from '../api/client';
import type { Article } from '../types';
import './TopList.css';

const TYPE_LABELS: Record<string, string> = {
  chinese: 'CN', english: 'EN', academic: 'ARXIV', social: 'SOCIAL',
};

function HeatBlocks({ score }: { score: number }) {
  const pct = Math.min(score * 10, 100);
  return (
    <span className="tl-heat">
      <span className="tl-heat-track">
        <span className="tl-heat-fill" style={{ width: `${pct}%` }} />
      </span>
      <span className="tl-heat-num">{score}</span>
    </span>
  );
}

export function TopList() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTopArticles(10).then(setArticles).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="tl-loading">LOADING…</div>;
  if (!articles.length) return null;

  return (
    <div className="tl-wrap">
      <div className="tl-header">
        <span className="tl-title">SIGNAL RANKING</span>
        <span className="tl-sub">热度 TOP 10</span>
      </div>
      <ol className="tl-list">
        {articles.map((a: Article, i: number) => (
          <li key={a.id} className={`tl-item ${i === 0 ? 'tl-item--first' : ''} ${i < 3 ? 'tl-item--top' : ''}`}>
            <span className={`tl-rank tl-rank--${i + 1}`}>{String(i + 1).padStart(2, '0')}</span>
            <div className="tl-body">
              <Link to={`/article/${a.id}`} className="tl-title-link">{a.title}</Link>
              <div className="tl-meta">
                {a.source_type && <span className="tl-badge">{TYPE_LABELS[a.source_type] ?? a.source_type}</span>}
                <span className="tl-source">{a.source}</span>
                {a.published_at && <span className="tl-time">{dayjs(a.published_at).format('MM-DD HH:mm')}</span>}
              </div>
            </div>
            {a.heat_score > 0 && <HeatBlocks score={a.heat_score} />}
            <a href={a.original_url} target="_blank" rel="noopener noreferrer"
               className="tl-ext" onClick={(e) => e.stopPropagation()}>↗</a>
          </li>
        ))}
      </ol>
    </div>
  );
}
