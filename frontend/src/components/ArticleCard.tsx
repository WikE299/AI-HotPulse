import { Link } from 'react-router-dom';
import dayjs from 'dayjs';
import type { Article } from '../types';
import './ArticleCard.css';

const SOURCE_TYPE_LABELS: Record<string, string> = {
  chinese: '中文',
  english: 'EN',
  academic: '学术',
  social: '社交',
};

const CATEGORY_COLORS: Record<string, string> = {
  LLM: '#6366f1',
  CV: '#f59e0b',
  Robotics: '#10b981',
  Industry: '#3b82f6',
  Research: '#8b5cf6',
  Other: '#6b7280',
};

export function ArticleCard({ article }: { article: Article }) {
  const typeLabel = article.source_type ? SOURCE_TYPE_LABELS[article.source_type] ?? article.source_type : '';
  const categoryColor = article.category ? (CATEGORY_COLORS[article.category] ?? '#6b7280') : '#6b7280';

  return (
    <Link to={`/article/${article.id}`} className="article-card">
      {article.image_url && (
        <div className="card-image">
          <img src={article.image_url} alt="" loading="lazy" onError={(e) => (e.currentTarget.style.display = 'none')} />
        </div>
      )}
      <div className="card-body">
        <div className="card-meta">
          <span className="source-badge">{typeLabel}</span>
          <span className="source-name">{article.source}</span>
          <span className="publish-time">
            {article.published_at ? dayjs(article.published_at).format('MM-DD HH:mm') : ''}
          </span>
          {article.heat_score > 0 && (
            <span className="heat-score">🔥 {article.heat_score}</span>
          )}
        </div>

        <h3 className="card-title">{article.title}</h3>

        {article.summary && <p className="card-summary">{article.summary}</p>}

        <div className="card-footer">
          <div className="keywords">
            {article.category && (
              <span className="category-chip" style={{ backgroundColor: categoryColor }}>
                {article.category}
              </span>
            )}
            {article.keywords.slice(0, 4).map((kw) => (
              <span key={kw} className="keyword-chip">{kw}</span>
            ))}
          </div>
          <a
            href={article.original_url}
            target="_blank"
            rel="noopener noreferrer"
            className="original-link"
            onClick={(e) => e.stopPropagation()}
          >
            原文 ↗
          </a>
        </div>
      </div>
    </Link>
  );
}
