'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';
import { adminApi, adminToken, token } from '@/lib/api';

const NAV = [
  { href: '/admin', label: 'Genel bakış', icon: '📊' },
  { href: '/admin/kalibrasyon', label: 'Kalibrasyon', icon: '🎯' },
  { href: '/admin/sorular', label: 'Sorular', icon: '📝' },
  { href: '/admin/kategoriler', label: 'Kategoriler', icon: '📚' },
  { href: '/admin/uretecler', label: 'Üreteçler', icon: '⚙️' },
  { href: '/admin/hesaplar', label: 'Hesaplar', icon: '👥' },
  { href: '/admin/audit', label: 'İşlem kaydı', icon: '🔍' },
];

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const path = usePathname();
  const [state, setState] = useState<'check' | 'login' | 'ok'>('check');
  const [email, setEmail] = useState('');

  useEffect(() => {
    if (!token.get()) { router.replace('/giris'); return; }
    if (!adminToken.get()) { setState('login'); return; }
    adminApi.me()
      .then((r) => { setEmail(r.email); setState('ok'); })
      .catch(() => { adminToken.clear(); setState('login'); });
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  if (state === 'check') {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-900">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-700
                        border-t-brand-400" />
      </div>
    );
  }

  if (state === 'login') {
    return <AdminLogin onOk={(e) => { setEmail(e); setState('ok'); }} />;
  }

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">
      {/* Ust bar */}
      <header className="sticky top-0 z-20 border-b border-slate-800 bg-slate-900/95
                         backdrop-blur">
        <div className="mx-auto flex max-w-[1400px] items-center justify-between
                        px-5 py-3">
          <div className="flex items-center gap-3">
            <span className="rounded-lg bg-brand-500 px-2 py-1 text-xs font-black">
              ADMIN
            </span>
            <span className="font-black">Minizeki</span>
          </div>
          <div className="flex items-center gap-3 text-sm">
            <span className="font-bold text-slate-400">{email}</span>
            <Link href="/" className="font-bold text-slate-400 hover:text-white">
              Siteye dön
            </Link>
            <button onClick={() => { adminToken.clear(); router.push('/'); }}
                    className="rounded-lg bg-slate-800 px-3 py-1.5 font-bold
                               hover:bg-slate-700">
              Çıkış
            </button>
          </div>
        </div>

        {/* Nav */}
        <nav className="mx-auto max-w-[1400px] overflow-x-auto px-5">
          <div className="flex gap-1 pb-1">
            {NAV.map((n) => {
              const active = path === n.href;
              return (
                <Link key={n.href} href={n.href}
                      className={`shrink-0 rounded-t-lg px-4 py-2.5 text-sm
                                  font-extrabold transition ${
                        active ? 'bg-slate-800 text-white'
                               : 'text-slate-400 hover:text-slate-200'}`}>
                  <span className="mr-1.5">{n.icon}</span>{n.label}
                </Link>
              );
            })}
          </div>
        </nav>
      </header>

      <main className="mx-auto max-w-[1400px] px-5 py-6">{children}</main>
    </div>
  );
}

/* ------------------------------------------------------------------ */

function AdminLogin({ onOk }: { onOk: (email: string) => void }) {
  const [pw, setPw] = useState('');
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async () => {
    setBusy(true); setErr('');
    try {
      const r = await adminApi.login(pw);
      adminToken.set(r.admin_token);
      onOk(r.email);
    } catch (e: any) {
      setErr(e.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-900 px-4">
      <div className="w-full max-w-sm">
        <div className="mb-6 text-center">
          <div className="mx-auto mb-3 flex h-14 w-14 items-center justify-center
                          rounded-2xl bg-brand-500 text-2xl">🔐</div>
          <h1 className="text-2xl font-black text-white">Admin paneli</h1>
          <p className="mt-1 text-sm font-bold text-slate-500">
            Yönetici şifresini girin
          </p>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-800/50 p-6">
          <input type="password" value={pw} autoFocus
                 onChange={(e) => setPw(e.target.value)}
                 onKeyDown={(e) => e.key === 'Enter' && submit()}
                 placeholder="Yönetici şifresi"
                 className="w-full rounded-xl border-2 border-slate-700 bg-slate-900
                            px-4 py-3 font-semibold text-white outline-none
                            focus:border-brand-500" />

          {err && (
            <p className="mt-3 rounded-lg bg-coral-500/15 px-3 py-2 text-sm
                          font-extrabold text-coral-400">{err}</p>
          )}

          <button onClick={submit} disabled={busy || !pw}
                  className="mt-4 w-full rounded-xl bg-brand-500 py-3 font-extrabold
                             text-white transition hover:bg-brand-600
                             disabled:opacity-40">
            {busy ? 'Kontrol ediliyor…' : 'Giriş yap'}
          </button>
        </div>

        <div className="mt-5 rounded-xl border border-slate-800 bg-slate-800/30 p-4
                        text-xs font-bold leading-relaxed text-slate-500">
          Panel iki koşul birden ister:<br />
          1. Hesabınızın admin yetkisi —{' '}
          <code className="text-slate-400">python content/make_admin.py e-posta</code><br />
          2. Sunucunun admin şifresi —{' '}
          <code className="text-slate-400">ADMIN_PASSWORD=... python main.py</code>
        </div>

        <div className="mt-4 text-center">
          <Link href="/" className="text-sm font-bold text-slate-600
                                     hover:text-slate-400">← Siteye dön</Link>
        </div>
      </div>
    </div>
  );
}
