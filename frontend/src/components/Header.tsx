import { Link } from 'react-router-dom';
import { triggerCrawl } from '../api/client';
import './Header.css';

export function Header() {
  async function handleTrigger() {
    try {
      await triggerCrawl();
      alert('爬取任务已启动，请稍后刷新页面');
    } catch {
      alert('启动失败，请检查后端服务');
    }
  }

  return (
    <header className="header">
      <Link to="/" className="logo">
        <span className="logo-icon">⚡</span>
        <span className="logo-text">AI HotPulse</span>
      </Link>
      <nav className="nav">
        <span className="nav-desc">AI 热点资讯聚合</span>
        <button className="trigger-btn" onClick={handleTrigger}>
          立即抓取
        </button>
      </nav>
    </header>
  );
}
