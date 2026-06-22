import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';

const NAV_ITEMS = [
  { path: '/', label: 'Home' },
  { path: '/klasifikasi', label: 'Klasifikasi' },
  { path: '/camera', label: 'Camera' },
  { path: '/about', label: 'About' },
];

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();

  const currentPage = (() => {
    const path = location.pathname;
    if (path === '/') return 'home';
    if (path === '/klasifikasi') return 'klasifikasi';
    if (path === '/camera') return 'camera';
    if (path === '/about') return 'about';
    return '';
  })();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    setMenuOpen(false);
  }, [location]);

  return (
    <>
      <nav className={`navbar${scrolled ? ' scrolled' : ''}`} id="navbar">
        <Link to="/" className="nav-logo">
          <span className="logo-text">
            SmartWaste<span className="logo-accent">AI</span>
          </span>
        </Link>

        <div className="nav-tabs">
          {NAV_ITEMS.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-tab${currentPage === item.label.toLowerCase() ? ' active' : ''}`}
            >
              {item.label}
            </Link>
          ))}
        </div>

        <div className="nav-right">
          <img src="/images/logo-fte.png" alt="Fakultas Teknik Elektro - Telkom University" className="nav-fte-logo nav-cta" />
          <img src="/images/logo-lab.png" alt="Logo Laboratorium" className="nav-lab-logo" />
          <button
            className="nav-toggle"
            id="navToggle"
            aria-label="Buka menu"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            <svg viewBox="0 0 24 24" fill="none">
              <line x1="3" y1="6" x2="21" y2="6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              <line x1="3" y1="12" x2="21" y2="12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              <line x1="3" y1="18" x2="21" y2="18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
          </button>
        </div>
      </nav>

      {/* Mobile menu */}
      <div className={`mobile-menu${menuOpen ? ' open' : ''}`} id="mobileMenu">
        {NAV_ITEMS.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`nav-tab${currentPage === item.label.toLowerCase() ? ' active' : ''}`}
          >
            {item.label}
          </Link>
        ))}
      </div>
    </>
  );
}
