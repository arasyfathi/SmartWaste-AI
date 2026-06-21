// ── Navbar scroll effect ──────────────────────────────────────────────────────
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 12);
  });
}

// ── Mobile menu toggle ────────────────────────────────────────────────────────
const navToggle = document.getElementById('navToggle');
const mobileMenu = document.getElementById('mobileMenu');
if (navToggle && mobileMenu) {
  navToggle.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
  });
  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => mobileMenu.classList.remove('open'));
  });
}

// ── Scroll-reveal (fade-up) ──────────────────────────────────────────────────
const revealEls = document.querySelectorAll('.fade-up');
if (revealEls.length) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

  revealEls.forEach(el => observer.observe(el));
}

// ── Stagger reveal untuk grid (feature-card, step-card-3d, team-card, dll) ────
// Memberi setiap item delay kecil berbeda saat masuk viewport, supaya terasa
// "mengalir" satu-satu, bukan muncul serempak datar. Elemen TETAP terlihat
// secara default di HTML/CSS murni (lihat .stagger-in di style.css) — script
// ini hanya menambah animasi kosmetik, jadi kalau observer gagal jalan
// (mis. JS error / browser lama), konten tidak akan hilang.
const staggerGroups = document.querySelectorAll('.feature-grid, .steps-wrap-3d, .team-grid, .chips-wrap');
staggerGroups.forEach(group => {
  const children = Array.from(group.children);
  children.forEach((child, i) => {
    if (child.classList.contains('step-connector-3d')) return;
    child.style.animationDelay = `${Math.min(i * 70, 420)}ms`;
  });
  const groupObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('stagger-in');
        groupObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });
  groupObserver.observe(group);
});

// ── Animated number counters (stats bar) ──────────────────────────────────────
function animateCounter(el) {
  const target = parseFloat(el.dataset.counter);
  const suffix = el.dataset.suffix || '';
  if (isNaN(target)) return;
  const isDecimal = el.dataset.counter.includes('.');
  const duration = 1400;
  const start = performance.now();

  function tick(now) {
    const p = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - p, 3); // ease-out cubic
    const val = target * eased;
    el.textContent = (isDecimal ? val.toFixed(2) : Math.round(val)) + suffix;
    if (p < 1) requestAnimationFrame(tick);
    else el.textContent = (isDecimal ? target.toFixed(2) : target) + suffix;
  }
  requestAnimationFrame(tick);
}

const counterEls = document.querySelectorAll('[data-counter]');
if (counterEls.length) {
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  counterEls.forEach(el => counterObserver.observe(el));
}

// ── 3D mouse-tilt untuk step cards (Cara Kerja) ────────────────────────────────
// Card miring mengikuti posisi kursor (rotateX/rotateY), efek "premium" khas
// produk SaaS modern. Dimatikan otomatis di perangkat sentuh / layar kecil.
const tiltCards = document.querySelectorAll('.step-card-3d-inner');
const supportsHover = window.matchMedia('(hover: hover)').matches;
if (supportsHover && tiltCards.length) {
  tiltCards.forEach(card => {
    const maxTilt = 10;
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const px = (e.clientX - rect.left) / rect.width;  // 0..1
      const py = (e.clientY - rect.top) / rect.height;  // 0..1
      const rotY = (px - 0.5) * maxTilt * 2;
      const rotX = (0.5 - py) * maxTilt * 2;
      card.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg) translateZ(6px)`;
      card.style.setProperty('--mx', `${px * 100}%`);
      card.style.setProperty('--my', `${py * 100}%`);
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'rotateX(0deg) rotateY(0deg) translateZ(0)';
    });
  });
}

// ── Hero orbit parallax mengikuti gerak mouse (efek depth ringan) ────────────
const heroOrbit = document.querySelector('.hero-orbit');
if (supportsHover && heroOrbit) {
  document.addEventListener('mousemove', (e) => {
    const x = (e.clientX / window.innerWidth - 0.5) * 16;
    const y = (e.clientY / window.innerHeight - 0.5) * 16;
    heroOrbit.style.transform = `translate(${x}px, ${y}px)`;
  });
}

// ── Ripple micro-interaction pada tombol utama ────────────────────────────────
const rippleButtons = document.querySelectorAll('.btn-primary, .btn-secondary, .btn-ghost');
rippleButtons.forEach(btn => {
  btn.addEventListener('click', (e) => {
    const rect = btn.getBoundingClientRect();
    const ripple = document.createElement('span');
    ripple.className = 'btn-ripple';
    ripple.style.left = `${e.clientX - rect.left}px`;
    ripple.style.top  = `${e.clientY - rect.top}px`;
    btn.appendChild(ripple);
    ripple.addEventListener('animationend', () => ripple.remove());
  });
});
