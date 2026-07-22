'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api, token, activeProfile, Profile, AVATARS } from '@/lib/api';
import { Zeki, Stat, Spinner } from '@/components/Zeki';

export default function HomePage() {
  const router = useRouter();
  const [profiles, setProfiles] = useState<Profile[] | null>(null);
  const [active, setActive] = useState<Profile | null>(null);

  useEffect(() => {
    if (!token.get()) { router.replace('/tanitim'); return; }
    load();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const load = async () => {
    try {
      const list = await api.profiles();
      setProfiles(list);
      const saved = activeProfile.get();
      const found = list.find((p) => p.id === saved);
      if (found) setActive(found);
      else if (list.length === 0) router.push('/profil/yeni');
    } catch {
      setProfiles([]);
    }
  };

  const pick = (p: Profile) => {
    activeProfile.set(p.id);
    if (!p.calibrated) router.push(`/profil/${p.id}/tanisalim`);
    else setActive(p);
  };

  if (profiles === null) return <Spinner label="Yükleniyor…" />;

  // --- Profil secimi ---
  if (!active) {
    return (
      <main className="mx-auto max-w-lg px-4 py-10">
        <div className="mb-8 text-center">
          <Zeki mood="happy" size={80} />
          <h1 className="mt-2 text-3xl font-black text-brand-600">Kim oynuyor?</h1>
        </div>

        <div className="grid grid-cols-2 gap-4">
          {profiles.map((p) => (
            <button key={p.id} onClick={() => pick(p)}
                    className="card flex flex-col items-center gap-2 p-6
                               transition hover:-translate-y-1 hover:shadow-lg">
              <span className="text-6xl">{AVATARS[p.avatar_id] || '🦊'}</span>
              <span className="text-xl font-black">{p.name}</span>
              <span className="text-sm font-bold text-slate-400">
                {p.grade}. sınıf
              </span>
              {p.quest_done_today && (
                <span className="rounded-full bg-mint-400/15 px-2 py-0.5 text-xs
                                 font-extrabold text-mint-600">
                  Bugün tamam ✓
                </span>
              )}
            </button>
          ))}

          <Link href="/profil/yeni"
                className="card flex flex-col items-center justify-center gap-2 p-6
                           border-2 border-dashed border-slate-200 text-slate-400
                           transition hover:border-brand-300 hover:text-brand-500">
            <span className="text-4xl">+</span>
            <span className="font-extrabold">Çocuk ekle</span>
          </Link>
        </div>

        <div className="mt-8 flex justify-center gap-3">
          <Link href="/ebeveyn" className="btn-ghost text-sm">
            👤 Ebeveyn
          </Link>
          <button onClick={() => { token.clear(); router.push('/giris'); }}
                  className="btn-ghost text-sm">
            Çıkış
          </button>
        </div>
      </main>
    );
  }

  // --- Cocuk ana ekrani: TEK BUTON ---
  return (
    <main className="mx-auto max-w-lg px-4 py-6 no-select">
      {/* Ust bar */}
      <div className="mb-8 flex items-center justify-between">
        <button onClick={() => { setActive(null); activeProfile.clear(); }}
                className="flex items-center gap-2">
          <span className="text-3xl">{AVATARS[active.avatar_id] || '🦊'}</span>
          <span className="text-lg font-black">{active.name}</span>
        </button>
        <div className="flex gap-2">
          <Stat icon="⭐" value={active.star_balance} />
          <Stat icon="🔥" value={active.streak_days} />
        </div>
      </div>

      {/* Ana kart */}
      <div className="mb-6">
        <div className="mb-4 flex justify-center">
          <Zeki mood={active.quest_done_today ? 'cheer' : 'happy'} size={120} />
        </div>

        {active.quest_done_today ? (
          <div className="card p-8 text-center">
            <p className="text-3xl font-black text-mint-600">Bugün tamam! 🎉</p>
            <p className="mt-2 font-bold text-slate-500">
              Yarın yeni sorular seni bekliyor.
            </p>
            <Link href="/kategoriler" className="btn-mint mt-5 w-full text-lg">
              Daha oynamak istiyorum
            </Link>
          </div>
        ) : (
          <Link href="/gorev"
                className="block rounded-3xl bg-brand-500 p-8 text-center text-white
                           shadow-2xl shadow-brand-500/30 transition
                           hover:bg-brand-600 active:scale-[0.98]">
            <p className="text-sm font-extrabold uppercase tracking-wider
                          text-brand-100">
              Bugünün görevi
            </p>
            <p className="mt-2 text-4xl font-black">BAŞLA</p>
            <p className="mt-2 font-bold text-brand-100">
              {active.grade <= 2 ? 16 : 18} soru · yaklaşık 4 dakika
            </p>
          </Link>
        )}
      </div>

      {/* Alt menu */}
      <div className="grid grid-cols-2 gap-3">
        <Link href="/ev" className="card flex items-center gap-3 p-4
                                    transition hover:-translate-y-0.5">
          <span className="text-3xl">🏠</span>
          <div className="text-left">
            <p className="font-black">Zeki'nin Evi</p>
            <p className="text-xs font-bold text-slate-400">⭐ {active.star_balance}</p>
          </div>
        </Link>
        <Link href="/kategoriler" className="card flex items-center gap-3 p-4
                                             transition hover:-translate-y-0.5">
          <span className="text-3xl">📚</span>
          <div className="text-left">
            <p className="font-black">Kategoriler</p>
            <p className="text-xs font-bold text-slate-400">Madalyalarım</p>
          </div>
        </Link>
      </div>

      <div className="mt-6 text-center">
        <Link href="/ebeveyn" className="text-sm font-extrabold text-slate-300
                                          hover:text-slate-500">
          Ebeveyn paneli
        </Link>
      </div>
    </main>
  );
}
