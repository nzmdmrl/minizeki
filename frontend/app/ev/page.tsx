'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api, activeProfile } from '@/lib/api';
import { Zeki, Spinner, ErrorBox, Stat } from '@/components/Zeki';

type Item = {
  id: string; name: string; icon: string; category: string;
  category_name: string; price: number; owned: boolean; affordable: boolean;
};
type House = {
  star_balance: number; owned_count: number; total_count: number; items: Item[];
};

export default function EvPage() {
  const router = useRouter();
  const [data, setData] = useState<House | null>(null);
  const [err, setErr] = useState('');
  const [msg, setMsg] = useState('');
  const [busy, setBusy] = useState('');

  const load = async () => {
    const pid = activeProfile.get();
    if (!pid) { router.replace('/'); return; }
    setErr('');
    try { setData(await api.house(pid)); }
    catch (e: any) { setErr(e.message); }
  };

  useEffect(() => { load(); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const buy = async (item: Item) => {
    const pid = activeProfile.get();
    if (!pid) return;
    setBusy(item.id); setMsg('');
    try {
      await api.buyItem(pid, item.id);
      setMsg(`${item.icon} ${item.name} alındı!`);
      await load();
    } catch (e: any) {
      setMsg(e.message);
    } finally {
      setBusy('');
    }
  };

  if (err) return <main className="mx-auto max-w-lg px-4 py-12">
    <ErrorBox message={err} onRetry={load} />
  </main>;
  if (!data) return <Spinner label="Yükleniyor…" />;

  const owned = data.items.filter((i) => i.owned);
  const gruplar = data.items.reduce<Record<string, Item[]>>((acc, i) => {
    (acc[i.category_name] ||= []).push(i);
    return acc;
  }, {});

  return (
    <main className="mx-auto max-w-lg px-4 py-6 no-select">
      <div className="mb-5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link href="/" className="text-2xl font-black text-slate-300
                                    hover:text-slate-500">←</Link>
          <h1 className="text-3xl font-black text-slate-800">Zeki'nin Evi</h1>
        </div>
        <Stat icon="⭐" value={data.star_balance} />
      </div>

      {/* Oda gorunumu */}
      <div className="card mb-5 overflow-hidden">
        <div className="relative flex min-h-[180px] items-end justify-center
                        bg-gradient-to-b from-brand-50 to-sun-400/10 p-6">
          <div className="absolute inset-x-0 bottom-0 h-10 bg-[#d4b896]/40" />
          <div className="relative z-10 flex flex-wrap items-end justify-center gap-2">
            {owned.map((i) => (
              <span key={i.id} className="text-4xl animate-pop" title={i.name}>
                {i.icon}
              </span>
            ))}
            <Zeki mood={owned.length > 3 ? 'cheer' : 'happy'} size={72} />
          </div>
        </div>
        <div className="border-t border-slate-100 px-5 py-3 text-center">
          <p className="font-extrabold text-slate-500">
            {data.owned_count}/{data.total_count} eşya
          </p>
        </div>
      </div>

      {msg && (
        <p className="mb-4 rounded-2xl bg-brand-50 px-4 py-3 text-center
                      font-extrabold text-brand-600 animate-pop">{msg}</p>
      )}

      {/* Magaza */}
      {Object.entries(gruplar).map(([cat, items]) => (
        <section key={cat} className="mb-6">
          <h2 className="mb-2.5 font-black text-slate-400">{cat}</h2>
          <div className="grid grid-cols-2 gap-2.5">
            {items.map((i) => (
              <div key={i.id}
                   className={`card flex items-center gap-3 p-3 ${
                     i.owned ? 'bg-mint-400/8 border-mint-400/40' : ''}`}>
                <span className={`text-3xl ${!i.owned && !i.affordable
                  ? 'grayscale opacity-40' : ''}`}>{i.icon}</span>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-black text-slate-800">{i.name}</p>
                  {i.owned ? (
                    <p className="text-xs font-extrabold text-mint-600">Senin ✓</p>
                  ) : (
                    <button onClick={() => buy(i)}
                            disabled={!i.affordable || busy === i.id}
                            className={`mt-0.5 rounded-full px-2.5 py-1 text-xs
                                        font-black transition ${
                              i.affordable
                                ? 'bg-sun-400 text-white hover:bg-sun-500'
                                : 'bg-slate-100 text-slate-400'}`}>
                      {busy === i.id ? '…' : `${i.price} ★`}
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      ))}
    </main>
  );
}
