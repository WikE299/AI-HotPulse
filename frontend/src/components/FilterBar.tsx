import './FilterBar.css';

const SOURCE_TYPES = [
  { value: '', label: 'All' },
  { value: 'chinese', label: 'CN' },
  { value: 'english', label: 'EN' },
  { value: 'academic', label: 'Arxiv' },
  { value: 'social', label: 'Social' },
];

const CATEGORIES = [
  { value: '', label: 'All' },
  { value: 'LLM', label: 'LLM' },
  { value: 'CV', label: 'CV' },
  { value: 'Robotics', label: 'Robot' },
  { value: 'Industry', label: 'Biz' },
  { value: 'Research', label: 'Res' },
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
      <div className="filter-section">
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
      <div className="filter-section">
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
