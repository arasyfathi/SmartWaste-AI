export function BackgroundOrnaments() {
  return (
    <div className="page-bg" aria-hidden="true">
      <div className="bg-orb bg-orb-1"></div>
      <div className="bg-orb bg-orb-2"></div>
      <div className="bg-orb bg-orb-3"></div>

      {/* Floating ambient particles */}
      <div className="particle-field">
        {Array.from({ length: 8 }, (_, i) => (
          <span key={i} className={`particle p${i + 1}`}></span>
        ))}
      </div>

      {/* Earth & waste themed ornaments */}
      <div className="page-ornament o-globe">
        <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="1.2"/><ellipse cx="12" cy="12" rx="10" ry="4.2" stroke="currentColor" strokeWidth="1.2"/><ellipse cx="12" cy="12" rx="4.2" ry="10" stroke="currentColor" strokeWidth="1.2"/><line x1="2" y1="12" x2="22" y2="12" stroke="currentColor" strokeWidth="1.2"/></svg>
      </div>
      <div className="page-ornament o-leaf-1">
        <svg viewBox="0 0 24 24" fill="none"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z" fill="currentColor" opacity="0.18"/><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 11 13 11 11" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/></svg>
      </div>
      <div className="page-ornament o-leaf-2">
        <svg viewBox="0 0 24 24" fill="none"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z" fill="currentColor" opacity="0.18"/><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 11 13 11 11" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/></svg>
      </div>
      <div className="page-ornament o-recycle">
        <svg viewBox="0 0 24 24" fill="none"><path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/><path d="M11 19h8.203a1.83 1.83 0 0 0 1.556-.89 1.784 1.784 0 0 0 0-1.775l-1.226-2.12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/><path d="m14 16-3 3 3 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/><path d="M8.293 13.596 7.196 9.5 3.1 10.598" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/><path d="m9.344 5.811 1.093-1.892A1.83 1.83 0 0 1 11.985 3a1.784 1.784 0 0 1 1.546.888l3.943 6.843" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/><path d="m13.378 9.633 4.096 1.098 1.097-4.096" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/></svg>
      </div>
      <div className="page-ornament o-droplet">
        <svg viewBox="0 0 24 24" fill="none"><path d="M12 2.5c3.5 4.5 6 8 6 11.5a6 6 0 0 1-12 0c0-3.5 2.5-7 6-11.5z" fill="currentColor" fillOpacity="0.15" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/></svg>
      </div>
      <div className="page-ornament o-bottle">
        <svg viewBox="0 0 24 24" fill="none"><rect x="8" y="3" width="8" height="3" rx="1" fill="currentColor" opacity="0.5"/><path d="M9 6v2.5L7 11v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-9l-2-2.5V6" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round" fill="currentColor" fillOpacity="0.12"/><line x1="7.5" y1="14" x2="16.5" y2="14" stroke="currentColor" strokeWidth="1.5"/></svg>
      </div>
      <div className="page-ornament o-leaf-3">
        <svg viewBox="0 0 24 24" fill="none"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z" fill="currentColor" opacity="0.18"/><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 11 13 11 11" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/></svg>
      </div>
      <div className="page-ornament o-can">
        <svg viewBox="0 0 24 24" fill="none"><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" fill="currentColor" fillOpacity="0.12" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/></svg>
      </div>
      <div className="page-ornament o-cup">
        <svg viewBox="0 0 24 24" fill="none"><path d="M6 8h12l-1.2 11a2 2 0 0 1-2 1.8H9.2a2 2 0 0 1-2-1.8L6 8z" fill="currentColor" fillOpacity="0.12" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/><path d="M4 8h16M9 8V5a3 3 0 0 1 6 0v3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/></svg>
      </div>
      <div className="page-ornament o-sprout">
        <svg viewBox="0 0 24 24" fill="none"><path d="M12 21V10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/><path d="M12 10C12 6 9 4 5 4c0 4 3 7 7 6z" fill="currentColor" fillOpacity="0.15" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/><path d="M12 13c0-4 3-6 7-6 0 4-3 7-7 6z" fill="currentColor" fillOpacity="0.15" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/></svg>
      </div>
      <div className="page-ornament o-cloud">
        <svg viewBox="0 0 24 24" fill="none"><path d="M6.5 18a4 4 0 0 1-.5-7.97A5 5 0 0 1 15.5 8.5 4.5 4.5 0 0 1 17 18H6.5z" fill="currentColor" fillOpacity="0.13" stroke="currentColor" strokeWidth="1.3" strokeLinejoin="round"/></svg>
      </div>
      <div className="page-ornament o-earth-leaf">
        <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="1.3" fill="currentColor" fillOpacity="0.06"/><path d="M7 12c1-3 3-5 6-5M5.5 9c1.5 0 2.5-1 3-2" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round"/></svg>
      </div>
    </div>
  );
}
