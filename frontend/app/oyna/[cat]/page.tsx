'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { api, activeProfile, Question } from '@/lib/api';
import QuestionPlayer from '@/components/QuestionPlayer';
import { Zeki, Spinner, ErrorBox } from '@/components/Zeki';

export default function OynaPage() {
  const router = useRouter();
  const { cat } = useParams<{ cat: string }>();

  const [questions, setQuestions] = useState<Question[] | null>(null);
  const [info, setInfo] = useState<{ name: string; icon: string } | null>(null);
  const [done, setDone] = useState<{ correct: number; total: number } | null>(null);
  const [err, setErr] = useState('');
  const [locked, setLocked] = useState(false);

  const load = async () => {
    const pid = activeProfile.get();
    if (!pid) { router.replace('/'); return; }
    setErr(''); setLocked(false); setDone(null); setQuestions(null);
    try {
      const r = await api.freePlay(cat, pid, 10);
      setInfo({ name: r.category.name, icon: r.category.icon });
      setQuestions(r.questions);
    } catch (e: any) {
      if (e.status === 402) setLocked(true);
      setErr(e.message);
    }
  };

  useEffect(() => { load(); }, [cat]); // eslint-disable-line react-hooks/exhaustive-deps

  // Ucretsiz plan siniri: cocuga sitem etmeyen, yonlendiren dil
  if (locked) return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col items-center
                     justify-center px-4 text-center">
      <Zeki mood="calm" size={104} />
      <p className="mt-4 text-xl font-black text-slate-700">{err}</p>
      <Link href="/" className="btn-primary mt-6 w-full">Ana ekrana dön</Link>
    </main>
  );

  if (err) return <main className="mx-auto max-w-md px-4 py-12">
    <ErrorBox message={err} onRetry={load} />
  </main>;

  if (done) {
    const oran = Math.round((done.correct / done.total) * 100);
    return (
      <main className="mx-auto flex min-h-screen max-w-md flex-col items-center
                       justify-center px-4 text-center no-select">
        <Zeki mood="cheer" size={112} />
        <h1 className="mt-3 text-3xl font-black text-mint-600">Tur bitti! 🎉</h1>
        <div className="card mt-5 w-full p-6">
          <p className="text-5xl font-black text-slate-800">
            {done.correct}<span className="text-2xl text-slate-300">/{done.total}</span>
          </p>
          <p className="mt-1 font-extrabold text-slate-400">doğru · %{oran}</p>
        </div>
        <div className="mt-5 grid w-full gap-3">
          <button onClick={load} className="btn-mint w-full text-lg">
            Bir tur daha {info?.icon}
          </button>
          <Link href="/kategoriler" className="btn-ghost w-full">
            Başka kategori
          </Link>
          <Link href="/" className="btn-ghost w-full">Ana ekran</Link>
        </div>
      </main>
    );
  }

  if (!questions) return <Spinner label="Sorular hazırlanıyor…" />;

  return (
    <QuestionPlayer
      questions={questions}
      onFinish={(c, t) => setDone({ correct: c, total: t })}
      title={info?.name} seconds={0}
      // Serbest oyunda onay yok: cocuk yanlis kategoriye girmis olabilir,
      // hemen cikabilmeli. Kaybedecek bir sey de yok.
      onExit={() => router.push('/kategoriler')}
    />
  );
}
