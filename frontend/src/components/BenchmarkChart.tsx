import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import type { ModelRelease } from '../types';
import './BenchmarkChart.css';

const BENCHMARK_NAMES = ['MMLU', 'HumanEval', 'MATH', 'GSM8K', 'ARC'];

const ORG_COLORS: Record<string, string> = {
  'OpenAI': '#74aa9c',
  'Anthropic': '#d4a574',
  'Google': '#4285f4',
  'Meta': '#0668e1',
  'Mistral AI': '#ff7000',
  'DeepSeek': '#4a90d9',
  'Alibaba': '#ff6a00',
};

function getColor(org: string): string {
  return ORG_COLORS[org] || '#6366F1';
}

interface Props {
  models: ModelRelease[];
}

export function BenchmarkChart({ models }: Props) {
  if (!models.length) return null;

  const chartData = BENCHMARK_NAMES.map((name) => {
    const entry: Record<string, string | number | null> = { benchmark: name };
    for (const m of models) {
      const val = m.benchmarks?.[name];
      entry[m.model_name] = val ?? null;
    }
    return entry;
  }).filter((d) => models.some((m) => d[m.model_name] != null));

  if (!chartData.length) {
    return <div className="bench-empty">暂无 Benchmark 数据</div>;
  }

  return (
    <div className="bench-wrap">
      <div className="bench-label">BENCHMARK COMPARISON</div>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={chartData} margin={{ top: 8, right: 12, left: -8, bottom: 0 }} barGap={2} barCategoryGap="20%">
          <CartesianGrid stroke="#E2E5ED" vertical={false} />
          <XAxis
            dataKey="benchmark"
            tick={{ fill: '#8E95A6', fontSize: 10, fontFamily: 'JetBrains Mono, monospace' }}
            axisLine={{ stroke: '#D0D4DE' }}
            tickLine={false}
          />
          <YAxis
            domain={[0, 100]}
            tick={{ fill: '#8E95A6', fontSize: 10, fontFamily: 'JetBrains Mono, monospace' }}
            axisLine={false}
            tickLine={false}
            width={36}
          />
          <Tooltip
            contentStyle={{
              background: '#FFFFFF',
              border: '1px solid #D0D4DE',
              borderRadius: 10,
              boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
              fontFamily: 'JetBrains Mono, monospace',
              fontSize: 11,
              color: '#1A1D26',
            }}
            cursor={{ fill: 'rgba(99,102,241,0.06)' }}
            formatter={(value: unknown) => (value != null ? Number(value).toFixed(1) : 'N/A')}
          />
          <Legend
            wrapperStyle={{
              fontFamily: 'JetBrains Mono, monospace',
              fontSize: 10,
              letterSpacing: '0.04em',
            }}
          />
          {models.map((m) => (
            <Bar key={m.id} dataKey={m.model_name} fill={getColor(m.organization)} radius={[4, 4, 0, 0]} />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
