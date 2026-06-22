import { Routes, Route } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { Home } from './pages/Home';
import { Klasifikasi } from './pages/Klasifikasi';
import { Camera } from './pages/Camera';
import { AboutPage } from './pages/About';

export function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/klasifikasi" element={<Klasifikasi />} />
        <Route path="/camera" element={<Camera />} />
        <Route path="/about" element={<AboutPage />} />
      </Routes>
    </Layout>
  );
}
