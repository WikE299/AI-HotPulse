import { Link } from 'react-router-dom';
import dayjs from 'dayjs';
import type { Article } from '../types';
import './ArticleCard.css';

const TYPE_LABELS: Record<string, string> = {
  chinese: 'CN', english: 'EN', academic: 'ARXIV', social: 'SOCIAL',
};

const CAT_LABELS: Record<string, string> = {
  LLM: 'LLM', CV: 'CV', Robotics: 'ROBOT', Industry: 'BIZ', Research: 'RES', Other: '—',
};

function HeatBar({ score }: { score: number }) {
  const pct = Math.min(score * 10, 100);
  return (
    <span className="heat-bar-wrap">
      <span className="heat-bar-track">
        <span className="heat-bar-fill" style={{ width: `${pct}%` }} />
      </span>
      <span className="heat-num">{score}</span>
    </span>
  );
}

export function ArticleCard({ article }: { article: Article }) {
  const typeLabel = article.source_type ? (TYPE_LABELS[article.source_type] ?? article.source_type.toUpperCase()) : '';
  const catLabel = article.category ? (CAT_LABELS[article.category] ?? article.category) : '';
  const hot = article.heat_score >= 7;

  return (
    <Link to={`/article/${article.id}`} className={`article-card ${hot ? 'article-card--hot' : ''}`}>
      <div className="card-top">
        <span className="card-type">{typeLabel}</span>
        {catLabel && <span className="card-cat">{catLabel}</span>}
        <span className="card-time">
          {article.published_at ? dayjs(article.published_at).format('MM-DD HH:mm') : ''}
        </span>
        {article.heat_score > 0 && <HeatBar score={article.heat_score} />}
      </div>

      <h3 className="card-title">{article.title}</h3>

      {article.summary && <p className="card-summary">{article.summary}</p>}

      <div className="card-bottom">
        <span className="card-source">{article.source}</span>
        <div className="card-kws">
          {article.keywords.slice(0, 3).map((kw) => (
            <span key={kw} className="card-kw">{kw}</span>
          ))}
        </div>
        <a
          href={article.original_url}
          target="_blank"
          rel="noopener noreferrer"
          className="card-link"
          onClick={(e) => e.stopPropagation()}
        >
          原文 ↗
        </a>
      </div>
    </Link>
  );
}
