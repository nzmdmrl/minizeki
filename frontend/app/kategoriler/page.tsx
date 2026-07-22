'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api, activeProfile, CategoryItem, SUBJECT_NAMES } from '@/lib/api';
import { Spinner, ErrorBox, ProgressBar } from '@/components/Zeki';

export default function KategorilerPage() {
  const router = useRouter();
  const [cats, setCats] = useState<CategoryItem[] | null>(null);
  const [err, setErr] = useState('');

  const load = async () => {
    const pid = activeProfile.get();
    if (!pid) { router.replace('/'); return; }
    setErr('');
    try {
      const r = await api.categories(pid);
      setCats(r.categories);
    } catch (e: any) {
      setErr(e.message);
    }
  };

  useEffect(() => { load(); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  if (err) return <main className="mx-auto max-w-lg px-4 py-12">
    <ErrorBox message={err} onRetry={load} />
  </main>;
  if (!cats) return <Spinner label="Yükleniyor…" />;

  // Derse gore grupla
  const gruplar = cats.reduce<Record<string, CategoryItem[]>>((acc, c) => {
    (acc[c.subject] ||= []).push(c);
    return acc;
  }, {});

  return (
    <main className="mx-auto max-w-lg px-4 py-6 no-select">
      <div className="mb-6 flex items-center gap-3">
        <Link href="/" className="text-2xl font-black text-slate-300
                                  hover:text-slate-500">←</Link>
        <h1 className="text-3xl font-black text-slate-800">Kategoriler</h1>
      </div>

      {Object.entries(gruplar).map(([subject, items]) => (
        <section key={subject} className="mb-7">
          <h2 className="mb-3 font-black text-slate-400">
            {SUBJECT_NAMES[subject] || subject}
          </h2>
          <div className="grid gap-2.5">
            {items.map((c) => (
              <CategoryCard key={c.id} c={c} />
            ))}
          </div>
        </section>
      ))}
    </main>
  );
}

function CategoryCard({ c }: { c: CategoryItem }) {
  const inner = (
    <>
      <span className="text-3xl">{c.icon}</span>
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <p className="truncate font-black text-slate-800">{c.name}</p>
          {c.medal_level > 0 && <span className="text-lg">{c.medal_icon}</span>}
          {c.locked && <span className="text-sm">🔒</span>}
        </div>
        <div className="mt-1.5 flex items-center gap-2">
          <ProgressBar value={c.progress} className="h-2 flex-1" />
          <span className="shrink-0 text-xs font-extrabold text-slate-400">
            {c.next_at ? `${c.total_correct}/${c.next_at}` : 'Usta 👑'}
          </span>
        </div>
      </div>
    </>
  );

  if (c.locked) {
    return (
      <div className="card flex items-center gap-3 p-4 opacity-50">
        {inner}
      </div>
    );
  }

  return (
    <Link href={`/oyna/${c.id}`}
          className="card flex items-center gap-3 p-4 transition
                     hover:-translate-y-0.5 hover:shadow-md">
      {inner}
    </Link>
  );
}
