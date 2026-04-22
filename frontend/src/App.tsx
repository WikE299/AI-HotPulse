import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Header } from './components/Header';
import { Home } from './pages/Home';
import { ArticleDetail } from './pages/ArticleDetail';
import { Papers } from './pages/Papers';
import { Topics } from './pages/Topics';
import { TopicDetail } from './pages/TopicDetail';
import { BriefPage } from './pages/Brief';
import { Timeline } from './pages/Timeline';
import { Arena } from './pages/Arena';
import './App.css';

export default function App() {
  return (
    <BrowserRouter>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/article/:id" element={<ArticleDetail />} />
          <Route path="/papers" element={<Papers />} />
          <Route path="/topics" element={<Topics />} />
          <Route path="/topics/:id" element={<TopicDetail />} />
          <Route path="/brief" element={<BriefPage />} />
          <Route path="/timeline" element={<Timeline />} />
          <Route path="/arena" element={<Arena />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
