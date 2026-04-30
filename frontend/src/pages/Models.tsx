import { useState, useEffect, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { fetchModelReleases } from '../api/client';
import { orgColor, ORG_COLORS } from '../utils/orgColors';
import { TimelineView } from './Timeline';
import { ArenaView } from './Arena';
import type { ModelRelease } from '../types';
import './Models.css';

type Tab = 'timeline' | 'arena';

export function Models() {
  const [searchParams, setSearchParams] = useSearchParams();
  const activeTab = (searchParams.get('tab') as Tab) || 'timeline';

  const [releases, setReleases] = useState<ModelRelease[]>([]);
  const [loading, setLoading] = useState(true);
  const [orgFilter, setOrgFilter] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetchModelReleases()
      .then(setReleases)
      .catch(() => setReleases([]))
      .finally(() => setLoading(false));
  }, []);

  const orgs = useMemo(() => {
    const set = new Set(releases.map((r) => r.organization));
    return Array.from(set).sort();
  }, [releases]);

  const filtered = useMemo(
    () => (orgFilter ? releases.filter((r) => r.organization === orgFilter) : releases),
    [releases, orgFilter],
  );

  function switchTab(tab: Tab) {
    setSearchParams({ tab });
  }

  return (
    <div className="models-page">
      <div className="models-heading">
        <div>
          <h1 className="models-title">模型</h1>
          <p className="models-sub">AI MODELS · TIMELINE & BENCHMARK ARENA</p>
        </div>
      </div>

      <div className="models-filters">
        <button
          className={`models-pill ${orgFilter === null ? 'active' : ''}`}
          onClick={() => setOrgFilter(null)}
        >
          ALL
        </button>
        {orgs.map((org) => (
          <button
            key={org}
            className={`models-pill ${orgFilter === org ? 'active' : ''}`}
            style={{ '--pill-color': orgColor(org) } as React.CSSProperties}
            onClick={() => setOrgFilter(orgFilter === org ? null : org)}
          >
            <span className="models-pill-dot" style={{ background: ORG_COLORS[org] || orgColor(org) }} />
            {org.toUpperCase()}
          </button>
        ))}
      </div>

      <div className="models-tabs">
        <button
          className={`models-tab ${activeTab === 'timeline' ? 'active' : ''}`}
          onClick={() => switchTab('timeline')}
        >
          TIMELINE
        </button>
        <button
          className={`models-tab ${activeTab === 'arena' ? 'active' : ''}`}
          onClick={() => switchTab('arena')}
        >
          ARENA
        </button>
      </div>

      {activeTab === 'timeline' ? (
        <TimelineView releases={filtered} loading={loading} />
      ) : (
        <ArenaView releases={filtered} loading={loading} />
      )}
    </div>
  );
}
