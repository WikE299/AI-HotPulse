import { useState, useEffect } from 'react';
import { PaperCard } from '../components/PaperCard';
import { fetchPapers } from '../api/client';
import type { Article, ArticlesResponse } from '../types';
import './Papers.css';

export function Papers() {
  const [data, setData] = useState<ArticlesResponse | null>(null);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetchPapers(page)
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [page]);

  return (
    <div className="papers-page">
      <div className="papers-header">
        <h1 className="papers-title">论文速读</h1>
        <p className="papers-subtitle">AI 学术前沿，核心贡献一眼看懂</p>
      </div>

      {loading && <div className="papers-loading">加载中…</div>}

      {!loading && data && data.items.length === 0 && (
        <div className="papers-empty">
          暂无论文数据。触发一次抓取后，ArXiv 论文将自动出现在这里。
        </div>
      )}

      <div className="papers-grid">
        {data?.items.map((article: Article) => (
          <PaperCard key={article.id} article={article} />
        ))}
      </div>

      {data && (
        <div className="papers-pagination">
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1}
            className="page-btn"
          >
            上一页
          </button>
          <span className="page-info">第 {page} 页</span>
          <button
            onClick={() => setPage((p) => p + 1)}
            disabled={!data.items.length || data.items.length < 20}
            className="page-btn"
          >
            下一页
          </button>
        </div>
      )}
    </div>
  );
}
