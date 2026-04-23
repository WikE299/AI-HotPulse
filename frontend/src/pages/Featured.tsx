import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import dayjs from 'dayjs';
import { fetchTopArticles } from '../api/client';
import type { Article } from '../types';
import './Featured.css';

const TYPE_LABELS: Record<string, string> = {
  chinese: 'CN', english: 'EN', academic: 'ARXIV', social: 'SOCIAL',
};

interface DateGroup {
  date: string;
  articles: Article[];
}

function groupByDate(articles: Article[]): DateGroup[] {
  const map = new Map<string, Article[]>();
  for (const a of articles) {
    const d = a.published_at ? dayjs(a.published_at).format('M月D日') : '未知日期';
    if (!map.has(d)) map.set(d, []);
    map.get(d)!.push(a);
  }
  return Array.from(map.entries()).map(([date, articles]) => ({ date, articles }));
}

export function Featured() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTopArticles(30)
      .then(setArticles)
      .catch(() => setArticles([]))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="ft-status">LOADING...</div>;
  if (!articles.length) return <div className="ft-status">暂无精选内容</div>;

  const groups = groupByDate(articles);

  return (
    <div className="ft-page">
      <div className="ft-header">
        <h1 className="ft-title">精选</h1>
        <p className="ft-sub">AI 自动挑选的高价值内容</p>
      </div>

      <div className="ft-timeline">
        {groups.map((g) => (
          <div key={g.date} className="ft-date-group">
            <div className="ft-date-label">{g.date}</div>
            {g.articles.map((a) => (
              <FeaturedCard key={a.id} article={a} />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

function FeaturedCard({ article }: { article: Article }) {
  const time = article.published_at ? dayjs(article.published_at).format('HH:mm') : '';
  const typeLabel = article.source_type ? (TYPE_LABELS[article.source_type] ?? article.source_type.toUpperCase()) : '';

  return (
    <div className="ft-card-row">
      <div className="ft-time-col">
        <span className="ft-time">{time}</span>
        <span className="ft-dot" />
      </div>
      <Link to={`/article/${article.id}`} className="ft-card">
        <div className="ft-card-head">
          <span className="ft-source">{article.source}</span>
          {typeLabel && <span className="ft-type-badge">{typeLabel}</span>}
          <span className="ft-heat">{article.heat_score}</span>
        </div>
        <h3 className="ft-card-title">{article.title}</h3>
        {article.summary && <p className="ft-card-summary">{article.summary}</p>}
        <div className="ft-card-tags">
          {article.keywords.slice(0, 4).map((kw) => (
            <span key={kw} className="ft-tag">{kw}</span>
          ))}
        </div>
      </Link>
    </div>
  );
}
