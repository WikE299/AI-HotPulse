import { Link, NavLink } from 'react-router-dom';
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
        <NavLink to="/" end className={({ isActive }) => 'nav-link' + (isActive ? ' active' : '')}>
          热点
        </NavLink>
        <NavLink to="/topics" className={({ isActive }) => 'nav-link' + (isActive ? ' active' : '')}>
          话题
        </NavLink>
        <NavLink to="/papers" className={({ isActive }) => 'nav-link' + (isActive ? ' active' : '')}>
          论文
        </NavLink>
        <NavLink to="/brief" className={({ isActive }) => 'nav-link' + (isActive ? ' active' : '')}>
          简报
        </NavLink>
        <button className="trigger-btn" onClick={handleTrigger}>
          立即抓取
        </button>
      </nav>
    </header>
  );
}
