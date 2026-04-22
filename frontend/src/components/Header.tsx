import { Link, NavLink } from 'react-router-dom';
import { triggerCrawl } from '../api/client';
import './Header.css';

const today = new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }).toUpperCase();

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
      <div className="masthead">
        <span className="masthead-meta">
          <span className="live-dot" />
          <span className="masthead-date">{today}</span>
        </span>
        <Link to="/" className="logo">AI HOTPULSE</Link>
        <div className="masthead-right">
          <button className="crawl-btn" onClick={handleTrigger}>抓取 ▶</button>
        </div>
      </div>
      <nav className="nav-strip">
        <NavLink to="/" end className={({ isActive }) => 'nav-item' + (isActive ? ' active' : '')}>热点</NavLink>
        <NavLink to="/topics" className={({ isActive }) => 'nav-item' + (isActive ? ' active' : '')}>话题</NavLink>
        <NavLink to="/papers" className={({ isActive }) => 'nav-item' + (isActive ? ' active' : '')}>论文</NavLink>
        <NavLink to="/brief" className={({ isActive }) => 'nav-item' + (isActive ? ' active' : '')}>简报</NavLink>
      </nav>
    </header>
  );
}
