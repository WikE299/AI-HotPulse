import { useState, useEffect, useRef, useMemo } from 'react';
import { fetchModelReleases } from '../api/client';
import { BenchmarkChart } from '../components/BenchmarkChart';
import type { ModelRelease } from '../types';
import './Timeline.css';

const ORG_COLORS: Record<string, string> = {
  'OpenAI': '#74aa9c',
  'Anthropic': '#d4a574',
  'Google': '#4285f4',
  'Meta': '#0668e1',
  'Mistral AI': '#ff7000',
  'DeepSeek': '#4a90d9',
  'Alibaba': '#ff6a00',
};

function orgColor(org: string): string {
  return ORG_COLORS[org] || '#6366F1';
}

export function Timeline() {
  const [releases, setReleases] = useState<ModelRelease[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [orgFilter, setOrgFilter] = useState<string>('');
  const trackRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setLoading(true);
    fetchModelReleases(orgFilter || undefined)
      .then(setReleases)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [orgFilter]);

  useEffect(() => {
    if (trackRef.current) {
      trackRef.current.scrollLeft = trackRef.current.scrollWidth;
    }
  }, [releases]);

  const orgs = useMemo(() => {
    const set = new Set(releases.map((r) => r.organization));
    return Array.from(set).sort();
  }, [releases]);

  const selected = releases.find((r) => r.id === selectedId) || null;

  const compareModels = useMemo(() => {
    if (!selected) return [];
    const idx = releases.findIndex((r) => r.id === selected.id);
    const neighbors = releases.filter((_, i) => i !== idx && Math.abs(i - idx) <= 2);
    return [selected, ...neighbors.slice(0, 3)];
  }, [selected, releases]);

  return (
    <div className="tl-page">
      <div className="tl-heading">
        <div>
          <h1 className="tl-page-title">Model Timeline</h1>
          <p className="tl-page-sub">AI 模型发布时间轴 · Benchmark 数据对比</p>
        </div>
      </div>

      <div className="tl-filters">
        <button className={`tl-pill ${orgFilter === '' ? 'active' : ''}`} onClick={() => setOrgFilter('')}>ALL</button>
        {orgs.map((org) => (
          <button
            key={org}
            className={`tl-pill ${orgFilter === org ? 'active' : ''}`}
            style={{ '--pill-color': orgColor(org) } as React.CSSProperties}
            onClick={() => setOrgFilter(org === orgFilter ? '' : org)}
          >
            {org}
          </button>
        ))}
      </div>

      {loading && <div className="tl-status">LOADING…</div>}

      {!loading && releases.length === 0 && (
        <div className="tl-status">NO DATA</div>
      )}

      {!loading && releases.length > 0 && (
        <div className="tl-track-wrap" ref={trackRef}>
          <div className="tl-track">
            <div className="tl-line" />
            {releases.map((r, i) => {
              const above = i % 2 === 0;
              const isSelected = r.id === selectedId;
              return (
                <div
                  key={r.id}
                  className={`tl-node ${above ? 'tl-node--above' : 'tl-node--below'} ${isSelected ? 'tl-node--sel' : ''}`}
                  onClick={() => setSelectedId(isSelected ? null : r.id)}
                >
                  <div className="tl-node-label">
                    <span className="tl-node-name">{r.model_name}</span>
                    <span className="tl-node-date">{r.release_date.slice(0, 7)}</span>
                  </div>
                  <div
                    className="tl-dot"
                    style={{ background: orgColor(r.organization), boxShadow: isSelected ? `0 0 0 3px ${orgColor(r.organization)}44` : 'none' }}
                  />
                  <div className="tl-node-connector" />
                </div>
              );
            })}
          </div>
        </div>
      )}

      {selected && (
        <div className="tl-detail">
          <div className="tl-detail-grid">
            <div className="tl-info-card">
              <div className="tl-info-header">
                <span className="tl-info-org" style={{ color: orgColor(selected.organization) }}>{selected.organization}</span>
                <span className="tl-info-cat">{selected.category.toUpperCase()}</span>
              </div>
              <h2 className="tl-info-name">{selected.model_name}</h2>
              <div className="tl-info-meta">
                <span>{selected.release_date}</span>
                {selected.parameters_size && (
                  <>
                    <span className="tl-sep">·</span>
                    <span>{selected.parameters_size} params</span>
                  </>
                )}
              </div>
              {selected.description && <p className="tl-info-desc">{selected.description}</p>}
              {selected.announcement_url && (
                <a href={selected.announcement_url} target="_blank" rel="noopener noreferrer" className="tl-info-link">
                  公告原文 ↗
                </a>
              )}
            </div>
            <div className="tl-chart-area">
              <BenchmarkChart models={compareModels} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
