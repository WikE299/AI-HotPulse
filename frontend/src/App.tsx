import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { OracleCard } from './components/OracleCard';
import { Featured } from './pages/Featured';
import { Home } from './pages/Home';
import { ArticleDetail } from './pages/ArticleDetail';
import { Papers } from './pages/Papers';
import { Topics } from './pages/Topics';
import { TopicDetail } from './pages/TopicDetail';
import { Models } from './pages/Models';
import './App.css';

export default function App() {
  return (
    <BrowserRouter>
      <Sidebar />
      <main>
        <Routes>
          <Route path="/featured" element={<Featured />} />
          <Route path="/" element={<Home />} />
          <Route path="/article/:id" element={<ArticleDetail />} />
          <Route path="/papers" element={<Papers />} />
          <Route path="/topics" element={<Topics />} />
          <Route path="/topics/:id" element={<TopicDetail />} />
          <Route path="/models" element={<Models />} />
        </Routes>
      </main>
      <OracleCard />
    </BrowserRouter>
  );
}
