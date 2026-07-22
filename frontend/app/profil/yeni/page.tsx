'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api, activeProfile, AVATARS } from '@/lib/api';
import { Zeki } from '@/components/Zeki';

export default function YeniProfilPage() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [avatar, setAvatar] = useState('fox');
  const [grade, setGrade] = useState(2);
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async () => {
    setErr('');
    if (!name.trim()) return setErr('Bir ad yazın');
    setBusy(true);
    try {
      const p = await api.createProfile(name.trim(), avatar, grade);
      activeProfile.set(p.id);
      router.push(`/profil/${p.id}/tanisalim`);
    } catch (e: any) {
      setErr(e.message);
      setBusy(false);
    }
  };

  return (
    <main className="mx-auto max-w-md px-4 py-8">
      <div className="mb-6 text-center">
        <Zeki mood="happy" size={80} />
        <h1 className="mt-2 text-3xl font-black text-brand-600">Çocuk ekle</h1>
      </div>

      <div className="card grid gap-5 p-6">
        <div>
          <label className="mb-2 block font-extrabold text-slate-600">Adı</label>
          <input value={name} maxLength={20}
                 onChange={(e) => setName(e.target.value)}
                 placeholder="Ali" className="input" />
        </div>

        <div>
          <label className="mb-2 block font-extrabold text-slate-600">Avatarı</label>
          <div className="grid grid-cols-6 gap-2">
            {Object.entries(AVATARS).map(([id, emoji]) => (
              <button key={id} onClick={() => setAvatar(id)}
                      className={`aspect-square rounded-2xl border-4 text-3xl transition ${
                        avatar === id ? 'border-brand-500 bg-brand-50 scale-105'
                                      : 'border-slate-100 hover:border-slate-200'}`}>
                {emoji}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="mb-2 block font-extrabold text-slate-600">
            Kaçıncı sınıf?
          </label>
          <div className="grid grid-cols-4 gap-2">
            {[1, 2, 3, 4].map((g) => (
              <button key={g} onClick={() => setGrade(g)}
                      className={`rounded-2xl border-4 py-4 text-2xl font-black
                                  transition ${
                        grade === g ? 'border-brand-500 bg-brand-50 text-brand-600'
                                    : 'border-slate-100 text-slate-400'}`}>
                {g}
              </button>
            ))}
          </div>
          <p className="mt-2 text-xs font-bold leading-relaxed text-slate-400">
            Sistem bir alt sınıfın konularını kendiliğinden tekrar ettirir.
            Çocuğunuz hazır olduğunda üst sınıf soruları otomatik açılır —
            ayar yapmanız gerekmez.
          </p>
        </div>

        {err && (
          <p className="rounded-xl bg-coral-400/10 px-3 py-2 text-sm font-extrabold
                        text-coral-500">{err}</p>
        )}

        <button onClick={submit} disabled={busy} className="btn-primary w-full text-lg">
          {busy ? 'Bekleyin…' : 'Devam'}
        </button>
      </div>
    </main>
  );
}
