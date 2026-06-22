// ── SVG Icon components ported from klasifikasi.js & camera.js ────────────────

import type { CSSProperties } from 'react';

interface IconProps {
  style?: CSSProperties;
  className?: string;
}

const defaultProps: IconProps = {};

export function PlasticIcon({ style, className }: IconProps = defaultProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style={style} className={className}>
      <rect x="8" y="3" width="8" height="3" rx="1" fill="currentColor" opacity="0.5" />
      <path d="M9 6v2.5L7 11v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-9l-2-2.5V6" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" fill="currentColor" fillOpacity="0.12" />
      <line x1="7.5" y1="14" x2="16.5" y2="14" stroke="currentColor" strokeWidth="2" />
    </svg>
  );
}

export function PaperIcon({ style, className }: IconProps = defaultProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style={style} className={className}>
      <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" fill="currentColor" fillOpacity="0.12" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" />
      <path d="M14 2v6h6" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" />
      <line x1="8" y1="13" x2="16" y2="13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      <line x1="8" y1="17" x2="13" y2="17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}

export function GlassIcon({ style, className }: IconProps = defaultProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style={style} className={className}>
      <path d="M7 3h10l-1.2 13.5a3.5 3.5 0 0 1-3.49 3.2h-.62a3.5 3.5 0 0 1-3.49-3.2L7 3z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" fill="currentColor" fillOpacity="0.1" />
      <line x1="7.6" y1="9" x2="16.4" y2="9" stroke="currentColor" strokeWidth="2" />
    </svg>
  );
}

export function MetalIcon({ style, className }: IconProps = defaultProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style={style} className={className}>
      <path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" fill="currentColor" fillOpacity="0.12" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" />
      <path d="m3.3 7 8.7 5 8.7-5M12 22V12" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" />
    </svg>
  );
}

export function OrganicIcon({ style, className }: IconProps = defaultProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style={style} className={className}>
      <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z" fill="currentColor" opacity="0.18" />
      <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 11 13 11 11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function RecycleIcon({ style, className }: IconProps = defaultProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style={style} className={className}>
      <path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M11 19h8.203a1.83 1.83 0 0 0 1.556-.89 1.784 1.784 0 0 0 0-1.775l-1.226-2.12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <path d="m14 16-3 3 3 3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M8.293 13.596 7.196 9.5 3.1 10.598" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <path d="m9.344 5.811 1.093-1.892A1.83 1.83 0 0 1 11.985 3a1.784 1.784 0 0 1 1.546.888l3.943 6.843" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <path d="m13.378 9.633 4.096 1.098 1.097-4.096" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function LightbulbIcon({ style, className }: IconProps = defaultProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style={style} className={className}>
      <path d="M9 18h6M10 22h4M12 2a6 6 0 0 0-4 10.5c.6.5 1 1.3 1 2.1V15h6v-.4c0-.8.4-1.6 1-2.1A6 6 0 0 0 12 2z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="currentColor" fillOpacity="0.12" />
    </svg>
  );
}

// Map icon key to component
const ICON_MAP: Record<string, React.FC<IconProps>> = {
  plastic: PlasticIcon,
  paper: PaperIcon,
  glass: GlassIcon,
  metal: MetalIcon,
  organic: OrganicIcon,
  recycle: RecycleIcon,
};

export function ClassIcon({ name, style, className }: { name: string; style?: CSSProperties; className?: string }) {
  const meta = ICON_MAP[name] || RecycleIcon;
  const Icon = meta;
  return <Icon style={style} className={className} />;
}

// Map emoji from backend to SVG icon component
const EMOJI_MAP: Record<string, React.FC<IconProps>> = {
  '♻️': PlasticIcon,
  '📄': PaperIcon,
  '🪟': GlassIcon,
  '⚙️': MetalIcon,
  '🌿': OrganicIcon,
};

export function EmojiToIcon({ emoji, style, className }: { emoji: string; style?: CSSProperties; className?: string }) {
  const Icon = EMOJI_MAP[emoji] || RecycleIcon;
  return <Icon style={style} className={className} />;
}
