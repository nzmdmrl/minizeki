import type { Metadata, Viewport } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Minizeki — İlkokul Zeka Oyunları',
  description:
    'İlkokul 1–4. sınıf için MEB müfredatına uygun eğitim oyunları. '
    + 'Her gün 4 dakika, çocuğunuzun seviyesine göre otomatik ayarlanan sorular.',
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  themeColor: '#3392ff',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tr">
      <body className="min-h-screen antialiased text-slate-800">{children}</body>
    </html>
  );
}
