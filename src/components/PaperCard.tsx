import type { Article } from '../types';
import './PaperCard.css';

const STARS = [1, 2, 3, 4, 5];

interface Props {
  article: Article;
}

export function PaperCard({ article }: Props) {
  const score = article.readability_score ?? 0;

  return (
    <div className="paper-card">
      <div className="paper-header">
        <span className="paper-badge">论文</span>
        {article.source && <span className="paper-source">{article.source}</span>}
        {article.published_at && (
          <span className="paper-date">
            {new Date(article.published_at).toLocaleDateString('zh-CN')}
          </span>
        )}
      </div>

      <h3 className="paper-title">{article.title}</h3>

      {article.paper_contribution && (
        <div className="paper-contribution">
          <span className="contrib-label">核心贡献</span>
          <p>{article.paper_contribution}</p>
        </div>
      )}

      {article.summary && !article.paper_contribution && (
        <p className="paper-summary">{article.summary}</p>
      )}

      <div className="paper-footer">
        <div className="readability">
          <span className="readability-label">可读性</span>
          <div className="stars">
            {STARS.map((s) => (
              <span key={s} className={s <= score ? 'star filled' : 'star'}>★</span>
            ))}
          </div>
          <span className="readability-hint">
            {score === 0 ? '' : score <= 2 ? '需要专业背景' : score >= 4 ? '人人可读' : '一般读者'}
          </span>
        </div>

        <div className="paper-links">
          {article.original_url && (
            <a href={article.original_url} target="_blank" rel="noopener noreferrer" className="paper-link">
              查看论文
            </a>
          )}
        </div>
      </div>

      {article.keywords.length > 0 && (
        <div className="paper-keywords">
          {article.keywords.slice(0, 6).map((kw) => (
            <span key={kw} className="paper-kw">{kw}</span>
          ))}
        </div>
      )}
    </div>
  );
}
