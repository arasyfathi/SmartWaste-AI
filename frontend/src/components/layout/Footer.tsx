export function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div>
          <span className="logo-text" style={{ fontSize: 14 }}>
            SmartWaste<span className="logo-accent">AI</span>
          </span>
          <div className="footer-brand-sub">Telkom University &middot; 2026</div>
        </div>

        <div className="footer-links">
          <a
            href="https://github.com/arasyfathi/SmartWaste-AI"
            target="_blank"
            rel="noopener noreferrer"
          >
            <svg viewBox="0 0 24 24" fill="none">
              <path
                d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.17 6.84 9.49.5.09.68-.22.68-.48 0-.24-.01-.87-.01-1.7-2.78.6-3.37-1.34-3.37-1.34-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.89 1.52 2.34 1.08 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.95 0-1.1.39-1.99 1.03-2.69-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.03.8-.22 1.65-.33 2.5-.33.85 0 1.7.11 2.5.33 1.91-1.3 2.75-1.03 2.75-1.03.55 1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.69 0 3.85-2.34 4.7-4.57 4.95.36.31.68.92.68 1.85 0 1.34-.01 2.42-.01 2.75 0 .27.18.58.69.48A10.01 10.01 0 0 0 22 12c0-5.523-4.477-10-10-10z"
                fill="currentColor"
              />
            </svg>
            GitHub
          </a>
        </div>

        <div className="footer-right">
          SmartWaste AI &middot; Klasifikasi &amp; Deteksi Sampah Berbasis AI
        </div>
      </div>
    </footer>
  );
}
