const categories = [
  { name: 'Plastik', color: '#06b6d4' },
  { name: 'Kertas', color: '#f59e0b' },
  { name: 'Kaca', color: '#8b5cf6' },
  { name: 'Logam', color: '#10d9a0' },
  { name: 'Organik', color: '#4ade80' },
];

export function WasteCategories() {
  return (
    <div className="chips-wrap">
      {categories.map((cat) => (
        <span key={cat.name} className="chip">
          <span className="chip-dot" style={{ '--c': cat.color } as React.CSSProperties}></span>
          {' '}{cat.name}
        </span>
      ))}
    </div>
  );
}
