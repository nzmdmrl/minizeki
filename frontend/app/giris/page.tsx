'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api, token } from '@/lib/api';
import { Zeki } from '@/components/Zeki';

export default function GirisPage() {
  const router = useRouter();
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [pin, setPin] = useState('');
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async () => {
    setErr('');
    if (!email.includes('@')) return setErr('Geçerli bir e-posta girin');
    if (password.length < 6) return setErr('Şifre en az 6 karakter olmalı');
    if (mode === 'register' && !/^\d{4}$/.test(pin))
      return setErr('PIN 4 rakamdan oluşmalı');

    setBusy(true);
    try {
      const r = mode === 'login'
        ? await api.login(email, password)
        : await api.register(email, password, pin);
      token.set(r.access_token);
      router.push('/');
    } catch (e: any) {
      setErr(e.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center px-4 py-8">
      <div className="w-full max-w-md">
        <div className="mb-6 text-center">
          <Zeki mood="happy" size={96} />
          <h1 className="mt-2 text-4xl font-black text-brand-600">Minizeki</h1>
          <p className="mt-1 font-bold text-slate-400">
            İlkokul için zeka oyunları
          </p>
        </div>

        <div className="card p-6">
          <div className="mb-5 grid grid-cols-2 gap-2 rounded-2xl bg-slate-100 p-1">
            {(['login', 'register'] as const).map((m) => (
              <button key={m} onClick={() => { setMode(m); setErr(''); }}
                      className={`rounded-xl py-2.5 font-extrabold transition ${
                        mode === m ? 'bg-white text-brand-600 shadow-sm'
                                   : 'text-slate-400'}`}>
                {m === 'login' ? 'Giriş yap' : 'Kayıt ol'}
              </button>
            ))}
          </div>

          <div className="grid gap-3">
            <div>
              <label className="mb-1 block text-sm font-extrabold text-slate-500">
                E-posta
              </label>
              <input type="email" value={email} autoComplete="email"
                     onChange={(e) => setEmail(e.target.value)}
                     placeholder="ornek@eposta.com" className="input" />
            </div>

            <div>
              <label className="mb-1 block text-sm font-extrabold text-slate-500">
                Şifre
              </label>
              <input type="password" value={password}
                     autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
                     onChange={(e) => setPassword(e.target.value)}
                     onKeyDown={(e) => e.key === 'Enter' && mode === 'login' && submit()}
                     placeholder="En az 6 karakter" className="input" />
            </div>

            {mode === 'register' && (
              <div>
                <label className="mb-1 block text-sm font-extrabold text-slate-500">
                  Ebeveyn PIN'i (4 rakam)
                </label>
                <input inputMode="numeric" maxLength={4} value={pin}
                       onChange={(e) => setPin(e.target.value.replace(/\D/g, ''))}
                       placeholder="••••"
                       className="input tracking-[0.5em] text-center" />
                <p className="mt-1.5 text-xs font-bold text-slate-400">
                  Gelişim raporunu ve ayarları bu PIN korur. Çocuğunuz ayarlara
                  giremez.
                </p>
              </div>
            )}

            {err && (
              <p className="rounded-xl bg-coral-400/10 px-3 py-2 text-sm
                            font-extrabold text-coral-500">{err}</p>
            )}

            <button onClick={submit} disabled={busy}
                    className="btn-primary mt-1 w-full text-lg">
              {busy ? 'Bekleyin…' : mode === 'login' ? 'Giriş yap' : 'Hesap oluştur'}
            </button>
          </div>
        </div>

        <p className="mt-5 text-center text-xs font-bold leading-relaxed text-slate-400">
          Reklamsız. Çocuğunuz hiçbir yerde ödeme ekranı görmez.<br />
          Başka çocuklarla eşleşme ve sohbet yoktur.
        </p>
      </div>
    </main>
  );
}
