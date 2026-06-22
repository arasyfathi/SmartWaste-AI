import { useEffect, type ReactNode } from 'react';
import { Navbar } from './Navbar';
import { Footer } from './Footer';
import { BackgroundOrnaments } from './BackgroundOrnaments';

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  // Global IntersectionObserver: adds .visible to any .fade-up element
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -30px 0px' },
    );

    // Observe all current .fade-up elements
    const elements = document.querySelectorAll('.fade-up');
    elements.forEach((el) => observer.observe(el));

    // Also watch for dynamically added .fade-up elements (route changes)
    const mutationObserver = new MutationObserver((mutations) => {
      mutations.forEach((m) => {
        m.addedNodes.forEach((node) => {
          if (node instanceof HTMLElement) {
            if (node.classList.contains('fade-up')) observer.observe(node);
            node.querySelectorAll?.('.fade-up').forEach((el) => observer.observe(el));
          }
        });
      });
    });

    mutationObserver.observe(document.body, { childList: true, subtree: true });

    return () => {
      observer.disconnect();
      mutationObserver.disconnect();
    };
  }, []);

  return (
    <>
      <BackgroundOrnaments />
      <Navbar />
      <main>{children}</main>
      <Footer />
    </>
  );
}
