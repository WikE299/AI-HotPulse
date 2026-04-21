import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import dayjs from 'dayjs';
import { fetchArticle } from '../api/client';
import type { Article } from '../types';
import './ArticleDetail.css';

const CATEGORY_COLORS: Record<string, string> = {
  LLM: '#6366f1', CV: '#f59e0b', Robotics: '#10b981',
  Industry: '#3b82f6', Research: '#8b5cf6', Other: '#6b7280',
};

export function ArticleDetail() {
  const { id } = useParams<{ id: string }>();
  const [article, setArticle] = useState<Article | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    fetchArticle(id).then(setArticle).finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="detail-loading">加载中...</div>;
  if (!article) return <div className="detail-loading">文章不存在</div>;

  const categoryColor = article.category ? (CATEGORY_COLORS[article.category] ?? '#6b7280') : '#6b7280';

  return (
    <div className="detail-page">
      <Link to="/" className="back-link">← 返回列表</Link>

      {article.image_url && (
        <img className="detail-image" src={article.image_url} alt="" onError={(e) => (e.currentTarget.style.display = 'none')} />
      )}

      <div className="detail-meta">
        <span className="detail-source">{article.source}</span>
        {article.published_at && (
          <span className="detail-time">{dayjs(article.published_at).format('YYYY-MM-DD HH:mm')}</span>
        )}
        {article.heat_score > 0 && <span className="detail-heat">🔥 热度 {article.heat_score}/10</span>}
      </div>

      <h1 className="detail-title">{article.title}</h1>

      <div className="detail-chips">
        {article.category && (
          <span className="detail-category" style={{ backgroundColor: categoryColor }}>{article.category}</span>
        )}
        {article.keywords.map((kw) => (
          <span key={kw} className="detail-keyword">{kw}</span>
        ))}
      </div>

      {article.summary && (
        <section className="detail-section">
          <h2>AI 摘要</h2>
          <p>{article.summary}</p>
        </section>
      )}

      {article.content_snippet && (
        <section className="detail-section">
          <h2>内容片段</h2>
          <p className="detail-snippet">{article.content_snippet}</p>
        </section>
      )}

      <a className="detail-original-btn" href={article.original_url} target="_blank" rel="noopener noreferrer">
        查看原文 ↗
      </a>
    </div>
  );
}
