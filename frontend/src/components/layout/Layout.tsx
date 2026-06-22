import { type ReactNode } from 'react';
import { Navbar } from './Navbar';
import { Footer } from './Footer';
import { BackgroundOrnaments } from './BackgroundOrnaments';

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  return (
    <>
      <BackgroundOrnaments />
      <Navbar />
      <main>{children}</main>
      <Footer />
    </>
  );
}
