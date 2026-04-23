import { useState, useEffect } from 'react';
import { Link, NavLink, useLocation } from 'react-router-dom';
import { triggerCrawl } from '../api/client';
import './Sidebar.css';

const today = new Date()
  .toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
  .toUpperCase();

const flame = (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 2c0 0-7 7-7 12a7 7 0 0014 0c0-5-7-12-7-12z" />
    <path d="M12 22c-2 0-3.5-1.5-3.5-3.5 0-2 3.5-5.5 3.5-5.5s3.5 3.5 3.5 5.5c0 2-1.5 3.5-3.5 3.5z" />
  </svg>
);
const chat = (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
  </svg>
);
const doc = (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
    <polyline points="14 2 14 8 20 8" />
    <line x1="16" y1="13" x2="8" y2="13" />
    <line x1="16" y1="17" x2="8" y2="17" />
    <line x1="10" y1="9" x2="8" y2="9" />
  </svg>
);
const cube = (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z" />
    <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
    <line x1="12" y1="22.08" x2="12" y2="12" />
  </svg>
);

const star = (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
  </svg>
);

const NAV_TOP = [
  { to: '/featured', end: false, label: '精选', icon: star },
];

const NAV_GROUPS = [
  {
    label: '信息流',
    items: [
      { to: '/', end: true, label: '热点', icon: flame },
      { to: '/topics', end: false, label: '话题', icon: chat },
      { to: '/papers', end: false, label: '论文', icon: doc },
    ],
  },
  {
    label: '模型',
    items: [
      { to: '/models', end: false, label: '模型', icon: cube },
    ],
  },
];

export function Sidebar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    setMobileOpen(false);
  }, [location.pathname]);

  async function handleTrigger() {
    try {
      await triggerCrawl();
      alert('爬取任务已启动，请稍后刷新页面');
    } catch {
      alert('启动失败，请检查后端服务');
    }
  }

  return (
    <>
      {!mobileOpen && (
        <button className="sidebar-hamburger" onClick={() => setMobileOpen(true)}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <line x1="3" y1="6" x2="21" y2="6" />
            <line x1="3" y1="12" x2="21" y2="12" />
            <line x1="3" y1="18" x2="21" y2="18" />
          </svg>
        </button>
      )}

      {mobileOpen && (
        <div className="sidebar-overlay" onClick={() => setMobileOpen(false)} />
      )}

      <aside className={`sidebar ${mobileOpen ? 'sidebar--open' : ''}`}>
        <div className="sidebar-logo-area">
          <Link to="/" className="sidebar-logo">
            <span className="sidebar-logo-ai">AI</span>
            <span className="sidebar-logo-main">
              <span className="sidebar-logo-hot">HOT</span>
              <span className="sidebar-logo-pulse">PULSE</span>
            </span>
          </Link>
        </div>

        <nav className="sidebar-nav">
          {NAV_TOP.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                'sidebar-nav-item sidebar-nav-item--top' + (isActive ? ' active' : '')
              }
            >
              <span className="sidebar-nav-icon">{item.icon}</span>
              <span className="sidebar-nav-label">{item.label}</span>
            </NavLink>
          ))}
          {NAV_GROUPS.map((group) => (
            <div key={group.label} className="sidebar-group">
              <span className="sidebar-group-label">{group.label}</span>
              {group.items.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.end}
                  className={({ isActive }) =>
                    'sidebar-nav-item' + (isActive ? ' active' : '')
                  }
                >
                  <span className="sidebar-nav-icon">{item.icon}</span>
                  <span className="sidebar-nav-label">{item.label}</span>
                </NavLink>
              ))}
            </div>
          ))}
        </nav>

        <div className="sidebar-spacer" />

        <div className="sidebar-footer">
          <div className="sidebar-meta">
            <span className="sidebar-live-dot" />
            <span className="sidebar-date">{today}</span>
          </div>
          <button className="sidebar-crawl-btn" onClick={handleTrigger}>
            抓取 ▶
          </button>
          <button className="sidebar-brief-btn" disabled title="即将上线：发送 AI 简报到飞书">
            发送简报
          </button>
        </div>
      </aside>
    </>
  );
}
