import { useState, useEffect } from 'react';
import { fetchLatestBrief, generateBrief } from '../api/client';
import type { Brief } from '../types';
import './Brief.css';

export function BriefPage() {
  const [brief, setBrief] = useState<Brief | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    fetchLatestBrief()
      .then(setBrief)
      .catch(() => setNotFound(true))
      .finally(() => setLoading(false));
  }, []);

  async function handleGenerate() {
    setGenerating(true);
    try {
      const b = await generateBrief();
      setBrief(b);
      setNotFound(false);
    } catch {
      alert('生成失败，请确保后端服务正常运行');
    } finally {
      setGenerating(false);
    }
  }

  return (
    <div className="brief-page">
      <div className="brief-heading">
        <div>
          <h1 className="brief-title">每日 AI 简报</h1>
          <p className="brief-subtitle">精选 AI 热点，每日一读</p>
        </div>
        <button className="generate-btn" onClick={handleGenerate} disabled={generating}>
          {generating ? '生成中…' : '生成今日简报'}
        </button>
      </div>

      {loading && <div className="brief-loading">加载中…</div>}

      {!loading && notFound && (
        <div className="brief-empty">
          <p>今日简报尚未生成。</p>
          <p>点击右上角"生成今日简报"按钮，或等待每日 09:05 自动生成。</p>
        </div>
      )}

      {brief && (
        <div className="brief-content-wrap">
          <div className="brief-meta">
            <span className="brief-date">{brief.date}</span>
            {brief.generated_at && (
              <span className="brief-gen-time">
                生成于 {new Date(brief.generated_at).toLocaleString('zh-CN')}
              </span>
            )}
          </div>
          <article className="brief-content">
            <BriefMarkdown content={brief.content} />
          </article>
        </div>
      )}
    </div>
  );
}

function BriefMarkdown({ content }: { content: string }) {
  const lines = content.split('\n');
  const elements: React.ReactNode[] = [];
  let key = 0;

  for (const line of lines) {
    if (line.startsWith('## ')) {
      elements.push(<h2 key={key++}>{line.slice(3)}</h2>);
    } else if (line.startsWith('# ')) {
      elements.push(<h1 key={key++}>{line.slice(2)}</h1>);
    } else if (line.startsWith('- ')) {
      elements.push(<li key={key++}>{renderInline(line.slice(2))}</li>);
    } else if (line.trim() === '') {
      elements.push(<br key={key++} />);
    } else {
      elements.push(<p key={key++}>{renderInline(line)}</p>);
    }
  }
  return <>{elements}</>;
}

function renderInline(text: string): React.ReactNode {
  const parts = text.split(/(\*\*[^*]+\*\*|\[[^\]]+\]\([^)]+\))/g);
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    }
    const linkMatch = part.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
    if (linkMatch) {
      return (
        <a key={i} href={linkMatch[2]} target="_blank" rel="noopener noreferrer">
          {linkMatch[1]}
        </a>
      );
    }
    return part;
  });
}
