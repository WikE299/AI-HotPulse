import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchTopic } from '../api/client';
import type { TopicDetail as TopicDetailType } from '../types';
import './TopicDetail.css';

export function TopicDetail() {
  const { id } = useParams<{ id: string }>();
  const [topic, setTopic] = useState<TopicDetailType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    fetchTopic(id)
      .then(setTopic)
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="topic-detail-loading">加载中…</div>;
  if (error || !topic) return <div className="topic-detail-error">话题不存在</div>;

  return (
    <div className="topic-detail-page">
      <Link to="/topics" className="topic-back">← 返回话题列表</Link>

      <div className="topic-detail-header">
        <div className="topic-detail-meta">
          <span className="topic-detail-count">{topic.article_count} 篇报道</span>
          <span className="topic-detail-heat">🔥 热度 {topic.heat_score}</span>
          <span className="topic-detail-key">{topic.topic_key}</span>
        </div>
        <h1 className="topic-detail-title">{topic.title}</h1>
        {topic.summary && <p className="topic-detail-summary">{topic.summary}</p>}
      </div>

      <h2 className="topic-articles-heading">相关报道</h2>
      <div className="topic-articles-list">
        {topic.articles.map((article) => (
          <a
            key={article.id}
            href={article.original_url}
            target="_blank"
            rel="noopener noreferrer"
            className="topic-article-item"
          >
            <div className="ta-meta">
              {article.source && <span className="ta-source">{article.source}</span>}
              {article.published_at && (
                <span className="ta-date">
                  {new Date(article.published_at).toLocaleDateString('zh-CN')}
                </span>
              )}
              <span className="ta-heat">🔥 {article.heat_score}</span>
            </div>
            <h3 className="ta-title">{article.title}</h3>
            {article.summary && <p className="ta-summary">{article.summary}</p>}
          </a>
        ))}
      </div>
    </div>
  );
}
