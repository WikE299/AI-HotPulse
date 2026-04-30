import { useState, useEffect, useRef, useMemo } from 'react';
import { BenchmarkChart } from '../components/BenchmarkChart';
import { orgColor } from '../utils/orgColors';
import type { ModelRelease } from '../types';
import './Timeline.css';

interface TimelineViewProps {
  releases: ModelRelease[];
  loading: boolean;
}

export function TimelineView({ releases, loading }: TimelineViewProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const trackRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (trackRef.current) {
      trackRef.current.scrollLeft = trackRef.current.scrollWidth;
    }
  }, [releases]);

  const selected = releases.find((r) => r.id === selectedId) || null;

  const compareModels = useMemo(() => {
    if (!selected) return [];
    const idx = releases.findIndex((r) => r.id === selected.id);
    const neighbors = releases.filter((_, i) => i !== idx && Math.abs(i - idx) <= 2);
    return [selected, ...neighbors.slice(0, 3)];
  }, [selected, releases]);

  if (loading) return <div className="tl-status">LOADING…</div>;
  if (!releases.length) return <div className="tl-status">NO DATA</div>;

  return (
    <>
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
    </>
  );
}
