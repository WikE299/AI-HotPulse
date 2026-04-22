import { Link } from 'react-router-dom';
import type { Topic } from '../types';
import './TopicCard.css';

interface Props {
  topic: Topic;
}

export function TopicCard({ topic }: Props) {
  return (
    <Link to={`/topics/${topic.id}`} className="topic-card">
      <div className="topic-header">
        <span className="topic-count">{topic.article_count} 篇报道</span>
        <span className="topic-heat">🔥 {topic.heat_score}</span>
      </div>
      <h3 className="topic-title">{topic.title}</h3>
      {topic.summary && <p className="topic-summary">{topic.summary}</p>}
      <div className="topic-footer">
        <span className="topic-key">{topic.topic_key}</span>
        {topic.latest_at && (
          <span className="topic-time">
            {new Date(topic.latest_at).toLocaleDateString('zh-CN')}
          </span>
        )}
      </div>
    </Link>
  );
}
