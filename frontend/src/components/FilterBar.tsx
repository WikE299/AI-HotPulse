import './FilterBar.css';

const SOURCE_TYPES = [
  { value: '', label: '全部来源' },
  { value: 'chinese', label: '中文媒体' },
  { value: 'english', label: '英文媒体' },
  { value: 'academic', label: '学术资讯' },
  { value: 'social', label: '社交热点' },
];

const CATEGORIES = [
  { value: '', label: '全部分类' },
  { value: 'LLM', label: 'LLM' },
  { value: 'CV', label: 'CV' },
  { value: 'Robotics', label: '机器人' },
  { value: 'Industry', label: '行业动态' },
  { value: 'Research', label: '研究' },
  { value: 'Other', label: '其他' },
];

interface Props {
  sourceType: string;
  category: string;
  onSourceTypeChange: (v: string) => void;
  onCategoryChange: (v: string) => void;
}

export function FilterBar({ sourceType, category, onSourceTypeChange, onCategoryChange }: Props) {
  return (
    <div className="filter-bar">
      <div className="filter-group">
        {SOURCE_TYPES.map((t) => (
          <button
            key={t.value}
            className={`filter-btn ${sourceType === t.value ? 'active' : ''}`}
            onClick={() => onSourceTypeChange(t.value)}
          >
            {t.label}
          </button>
        ))}
      </div>
      <div className="filter-group">
        {CATEGORIES.map((c) => (
          <button
            key={c.value}
            className={`filter-btn ${category === c.value ? 'active' : ''}`}
            onClick={() => onCategoryChange(c.value)}
          >
            {c.label}
          </button>
        ))}
      </div>
    </div>
  );
}
