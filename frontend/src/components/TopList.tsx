import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import dayjs from 'dayjs';
import { fetchTopArticles, fetchTwitterFeed } from '../api/client';
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

function extractHandle(source: string | null): string {
  if (!source) return '';
  const m = source.match(/Twitter @(\w+)/);
  return m ? m[1] : '';
}

const VOICE_PROFILES: Record<string, { name: string; title: string; region: string; color: string }> = {
  sama:          { name: 'Sam Altman',       title: 'CEO, OpenAI',               region: 'US', color: '#10B981' },
  karpathy:      { name: 'Andrej Karpathy',  title: 'Ex-Tesla AI / OpenAI',      region: 'US', color: '#6366F1' },
  ylecun:        { name: 'Yann LeCun',       title: 'Chief AI Scientist, Meta',  region: 'US', color: '#3B82F6' },
  DarioAmodei:   { name: 'Dario Amodei',     title: 'CEO, Anthropic',            region: 'US', color: '#8B5CF6' },
  JeffDean:      { name: 'Jeff Dean',        title: 'Chief Scientist, Google',   region: 'US', color: '#F59E0B' },
  hardmaru:      { name: 'David Ha',         title: 'Research Lead, Sakana AI',  region: 'JP', color: '#EC4899' },
  fchollet:      { name: 'François Chollet', title: 'Creator of Keras, Google',  region: 'US', color: '#14B8A6' },
  iaboredai:     { name: 'Jim Fan',          title: 'Sr. Research Scientist, NVIDIA', region: 'US', color: '#F97316' },
  OpenAI:        { name: 'OpenAI',           title: 'AI Research Lab',           region: 'US', color: '#10B981' },
  AnthropicAI:   { name: 'Anthropic',        title: 'AI Safety Company',         region: 'US', color: '#8B5CF6' },
  GoogleDeepMind:{ name: 'Google DeepMind',  title: 'AI Research Lab',           region: 'UK', color: '#3B82F6' },
  MetaAI:        { name: 'Meta AI',          title: 'AI Research Division',      region: 'US', color: '#3B82F6' },
  huggingface:   { name: 'Hugging Face',     title: 'Open-Source AI Platform',   region: 'US', color: '#F59E0B' },
  MistralAI:     { name: 'Mistral AI',       title: 'AI Startup',                region: 'FR', color: '#EF4444' },
  deepaborshi:   { name: 'DeepSeek',         title: 'AI Research Lab',           region: 'CN', color: '#6366F1' },
};

function getProfile(handle: string) {
  return VOICE_PROFILES[handle] || { name: handle, title: 'Twitter', region: '—', color: '#6B7280' };
}

function getInitial(name: string): string {
  const parts = name.split(/\s+/);
  if (parts.length >= 2) return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  return name.slice(0, 2).toUpperCase();
}

function SignalTab({ articles, loading }: { articles: Article[]; loading: boolean }) {
  if (loading) return <div className="tl-loading">LOADING…</div>;
  if (!articles.length) return null;

  return (
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
  );
}

function VoicesTab({ articles, loading }: { articles: Article[]; loading: boolean }) {
  if (loading) return <div className="tl-loading">LOADING…</div>;
  if (!articles.length) return <div className="tl-empty">暂无 Twitter 动态</div>;

  return (
    <div className="tl-voices-scroll">
      {articles.map((a: Article) => {
        const handle = extractHandle(a.source);
        const profile = getProfile(handle);
        return (
          <a
            key={a.id}
            href={a.original_url}
            target="_blank"
            rel="noopener noreferrer"
            className="tl-card"
          >
            {/* Header: avatar + name + region */}
            <div className="tl-card-header">
              <span className="tl-card-avatar" style={{ background: profile.color }}>
                {getInitial(profile.name)}
              </span>
              <div className="tl-card-who">
                <span className="tl-card-name">{profile.name}</span>
                <span className="tl-card-title">{profile.title}</span>
              </div>
              <span className="tl-card-region">{profile.region}</span>
            </div>

            {/* Image */}
            {a.image_url && (
              <div className="tl-card-img-wrap">
                <img src={a.image_url} alt="" className="tl-card-img" loading="lazy" />
              </div>
            )}

            {/* Body */}
            <p className="tl-card-text">{a.title}</p>

            {/* Footer */}
            <div className="tl-card-footer">
              <span className="tl-card-handle">@{handle}</span>
              {a.published_at && (
                <span className="tl-card-time">{dayjs(a.published_at).format('MM-DD HH:mm')}</span>
              )}
            </div>
          </a>
        );
      })}
    </div>
  );
}

export function TopList() {
  const [activeTab, setActiveTab] = useState<'signal' | 'voices'>('signal');
  const [articles, setArticles] = useState<Article[]>([]);
  const [tweets, setTweets] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [tweetsLoading, setTweetsLoading] = useState(false);

  useEffect(() => {
    fetchTopArticles(10).then(setArticles).finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (activeTab === 'voices' && tweets.length === 0) {
      setTweetsLoading(true);
      fetchTwitterFeed(20).then(setTweets).finally(() => setTweetsLoading(false));
    }
  }, [activeTab, tweets.length]);

  return (
    <div className="tl-wrap">
      <div className="tl-header">
        <div className="tl-header-left">
          <span className="tl-title">SIGNAL RANKING</span>
          <span className="tl-sub">热点 Top 10</span>
        </div>
        <div className="tl-tabs">
          <button
            className={`tl-tab ${activeTab === 'signal' ? 'active' : ''}`}
            onClick={() => setActiveTab('signal')}
          >Signal</button>
          <button
            className={`tl-tab ${activeTab === 'voices' ? 'active' : ''}`}
            onClick={() => setActiveTab('voices')}
          >Voices</button>
        </div>
      </div>
      {activeTab === 'signal'
        ? <SignalTab articles={articles} loading={loading} />
        : <VoicesTab articles={tweets} loading={tweetsLoading} />
      }
    </div>
  );
}
