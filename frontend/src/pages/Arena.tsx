import { useState, useEffect, useMemo } from 'react';
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Legend,
} from 'recharts';
import { fetchModelReleases } from '../api/client';
import type { ModelRelease, Benchmarks } from '../types';
import './Arena.css';

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
  return ORG_COLORS[org] || '#e63946';
}

const BENCHMARKS = ['MMLU', 'HumanEval', 'MATH', 'GSM8K', 'ARC'] as const;
type BenchKey = (typeof BENCHMARKS)[number];
type SortKey = BenchKey | 'composite';

function compositeScore(b: Benchmarks | null | undefined): number | null {
  if (!b) return null;
  const vals = BENCHMARKS.map((k) => b[k]).filter((v): v is number => v != null);
  if (vals.length === 0) return null;
  return vals.reduce((a, c) => a + c, 0) / vals.length;
}

function getScore(m: ModelRelease, key: SortKey): number | null {
  if (key === 'composite') return compositeScore(m.benchmarks);
  return m.benchmarks?.[key] ?? null;
}

export function Arena() {
  const [releases, setReleases] = useState<ModelRelease[]>([]);
  const [loading, setLoading] = useState(true);
  const [orgFilter, setOrgFilter] = useState('');
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [sortKey, setSortKey] = useState<SortKey>('composite');
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('desc');
  const [activeBench, setActiveBench] = useState<BenchKey>('MMLU');

  useEffect(() => {
    setLoading(true);
    fetchModelReleases(orgFilter || undefined)
      .then(setReleases)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [orgFilter]);

  const orgs = useMemo(() => {
    const set = new Set(releases.map((r) => r.organization));
    return Array.from(set).sort();
  }, [releases]);

  const sorted = useMemo(() => {
    const arr = [...releases];
    arr.sort((a, b) => {
      const sa = getScore(a, sortKey);
      const sb = getScore(b, sortKey);
      if (sa == null && sb == null) return 0;
      if (sa == null) return 1;
      if (sb == null) return -1;
      return sortDir === 'desc' ? sb - sa : sa - sb;
    });
    return arr;
  }, [releases, sortKey, sortDir]);

  const selectedModels = useMemo(
    () => releases.filter((r) => selectedIds.has(r.id)),
    [releases, selectedIds],
  );

  function handleSort(key: SortKey) {
    if (key === sortKey) {
      setSortDir((d) => (d === 'desc' ? 'asc' : 'desc'));
    } else {
      setSortKey(key);
      setSortDir('desc');
    }
  }

  function toggleSelect(id: string) {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else if (next.size < 5) next.add(id);
      return next;
    });
  }

  const benchMaxes = useMemo(() => {
    const m: Partial<Record<SortKey, number>> = {};
    for (const key of [...BENCHMARKS, 'composite'] as SortKey[]) {
      let max = -Infinity;
      for (const r of releases) {
        const s = getScore(r, key);
        if (s != null && s > max) max = s;
      }
      if (max > -Infinity) m[key] = max;
    }
    return m;
  }, [releases]);

  // --- Radar data ---
  const radarData = useMemo(() => {
    return BENCHMARKS.map((bk) => {
      const entry: Record<string, string | number | null> = { benchmark: bk };
      for (const m of selectedModels) {
        entry[m.model_name] = m.benchmarks?.[bk] ?? null;
      }
      return entry;
    });
  }, [selectedModels]);

  // --- Bar data ---
  const barData = useMemo(() => {
    return releases
      .map((r) => ({
        name: r.model_name,
        org: r.organization,
        score: r.benchmarks?.[activeBench] ?? null,
      }))
      .filter((d) => d.score != null)
      .sort((a, b) => (b.score as number) - (a.score as number));
  }, [releases, activeBench]);

  function colHeader(key: SortKey, label: string) {
    const active = sortKey === key;
    return (
      <th className={active ? 'sorted' : ''} onClick={() => handleSort(key)}>
        {label}
        {active && <span className="arena-sort-arrow">{sortDir === 'desc' ? '▼' : '▲'}</span>}
      </th>
    );
  }

  return (
    <div className="arena-page">
      <div className="arena-heading">
        <div>
          <h1 className="arena-title">Model Arena</h1>
          <p className="arena-sub">AI 模型 Benchmark 竞技场 · 多维对比分析</p>
        </div>
      </div>

      <div className="arena-filters">
        <button className={`arena-pill ${orgFilter === '' ? 'active' : ''}`} onClick={() => setOrgFilter('')}>ALL</button>
        {orgs.map((org) => (
          <button
            key={org}
            className={`arena-pill ${orgFilter === org ? 'active' : ''}`}
            style={{ '--pill-color': orgColor(org) } as React.CSSProperties}
            onClick={() => setOrgFilter(org === orgFilter ? '' : org)}
          >
            {org}
          </button>
        ))}
      </div>

      {loading && <div className="arena-status">LOADING…</div>}

      {!loading && releases.length === 0 && <div className="arena-status">NO DATA</div>}

      {!loading && releases.length > 0 && (
        <div className="arena-body">
          {/* ── Left: Leaderboard ── */}
          <div className="arena-table-wrap">
            <div className="arena-table-toolbar">
              <span className="arena-table-toolbar-left">
                LEADERBOARD{' '}
                {selectedIds.size > 0 && (
                  <span className="arena-selected-count">· {selectedIds.size} SELECTED</span>
                )}
              </span>
              {selectedIds.size > 0 && (
                <button className="arena-clear-btn" onClick={() => setSelectedIds(new Set())}>CLEAR ALL</button>
              )}
            </div>
            <table className="arena-table">
              <thead>
                <tr>
                  <th style={{ cursor: 'default' }}>#</th>
                  <th style={{ cursor: 'default' }} />
                  <th style={{ cursor: 'default' }}>MODEL</th>
                  {BENCHMARKS.map((bk) => colHeader(bk, bk))}
                  {colHeader('composite', 'AVG')}
                </tr>
              </thead>
              <tbody>
                {sorted.map((r, i) => {
                  const isSelected = selectedIds.has(r.id);
                  const comp = compositeScore(r.benchmarks);
                  return (
                    <tr
                      key={r.id}
                      className={isSelected ? 'arena-row--selected' : ''}
                      onClick={() => toggleSelect(r.id)}
                      style={{ cursor: 'pointer' }}
                    >
                      <td className="arena-cell-rank">{String(i + 1).padStart(2, '0')}</td>
                      <td className="arena-cell-check">
                        <input
                          type="checkbox"
                          className="arena-check"
                          checked={isSelected}
                          readOnly
                        />
                      </td>
                      <td className="arena-cell-model">
                        <span className="arena-org-dot" style={{ background: orgColor(r.organization) }} />
                        {r.model_name}
                      </td>
                      {BENCHMARKS.map((bk) => {
                        const val = r.benchmarks?.[bk];
                        const isTop = val != null && val === benchMaxes[bk];
                        return (
                          <td key={bk} className={`arena-cell-score ${isTop ? 'arena-cell-score--top' : ''} ${val == null ? 'arena-cell-na' : ''}`}>
                            {val != null ? val.toFixed(1) : '—'}
                          </td>
                        );
                      })}
                      <td className={`arena-cell-composite ${comp != null && comp === benchMaxes.composite ? 'arena-cell-score--top' : ''}`}>
                        {comp != null ? comp.toFixed(1) : '—'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* ── Right: Charts ── */}
          <div className="arena-charts">
            {/* Radar */}
            <div className="arena-radar-section">
              <div className="arena-section-label">RADAR COMPARISON</div>
              {selectedModels.length === 0 ? (
                <div className="arena-radar-empty">SELECT MODELS FROM THE TABLE TO COMPARE</div>
              ) : (
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={radarData} cx="50%" cy="50%" outerRadius="72%">
                    <PolarGrid stroke="#2a2a2a" />
                    <PolarAngleAxis
                      dataKey="benchmark"
                      tick={{ fill: '#484848', fontSize: 10, fontFamily: 'JetBrains Mono, monospace' }}
                    />
                    <PolarRadiusAxis
                      domain={[0, 100]}
                      tick={{ fill: '#383838', fontSize: 9 }}
                      axisLine={false}
                    />
                    {selectedModels.map((m) => (
                      <Radar
                        key={m.id}
                        name={m.model_name}
                        dataKey={m.model_name}
                        stroke={orgColor(m.organization)}
                        fill={orgColor(m.organization)}
                        fillOpacity={0.12}
                        strokeWidth={1.5}
                      />
                    ))}
                    <Legend
                      wrapperStyle={{
                        fontFamily: 'JetBrains Mono, monospace',
                        fontSize: 10,
                        letterSpacing: '0.04em',
                      }}
                    />
                    <Tooltip
                      contentStyle={{
                        background: '#161616',
                        border: '1px solid #2a2a2a',
                        borderRadius: 0,
                        fontFamily: 'JetBrains Mono, monospace',
                        fontSize: 11,
                        color: '#f0f0f0',
                      }}
                      formatter={(value: unknown) => (value != null ? Number(value).toFixed(1) : 'N/A')}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              )}
            </div>

            {/* Bar chart */}
            <div className="arena-bar-section">
              <div className="arena-section-label">BENCHMARK RANKING</div>
              <div className="arena-bench-tabs">
                {BENCHMARKS.map((bk) => (
                  <button
                    key={bk}
                    className={`arena-bench-tab ${activeBench === bk ? 'active' : ''}`}
                    onClick={() => setActiveBench(bk)}
                  >
                    {bk}
                  </button>
                ))}
              </div>
              {barData.length === 0 ? (
                <div className="arena-radar-empty">NO DATA FOR {activeBench}</div>
              ) : (
                <ResponsiveContainer width="100%" height={Math.max(280, barData.length * 28)}>
                  <BarChart data={barData} layout="vertical" margin={{ top: 0, right: 16, left: 0, bottom: 0 }} barCategoryGap="16%">
                    <CartesianGrid stroke="#1f1f1f" horizontal={false} />
                    <XAxis
                      type="number"
                      domain={[0, 100]}
                      tick={{ fill: '#484848', fontSize: 10, fontFamily: 'JetBrains Mono, monospace' }}
                      axisLine={{ stroke: '#2a2a2a' }}
                      tickLine={false}
                    />
                    <YAxis
                      type="category"
                      dataKey="name"
                      width={140}
                      tick={{ fill: '#909090', fontSize: 10, fontFamily: 'JetBrains Mono, monospace' }}
                      axisLine={false}
                      tickLine={false}
                    />
                    <Tooltip
                      contentStyle={{
                        background: '#161616',
                        border: '1px solid #2a2a2a',
                        borderRadius: 0,
                        fontFamily: 'JetBrains Mono, monospace',
                        fontSize: 11,
                        color: '#f0f0f0',
                      }}
                      cursor={{ fill: 'rgba(255,255,255,0.03)' }}
                      formatter={(value: unknown) => (value != null ? Number(value).toFixed(1) : 'N/A')}
                    />
                    <Bar
                      dataKey="score"
                      radius={[0, 2, 2, 0]}
                      shape={(props: { x?: number; y?: number; width?: number; height?: number; payload?: { org: string } }) => {
                        const { x = 0, y = 0, width = 0, height = 0, payload } = props;
                        return (
                          <rect
                            x={x}
                            y={y}
                            width={width}
                            height={height}
                            fill={orgColor(payload?.org ?? '')}
                            rx={2}
                          />
                        );
                      }}
                    />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
