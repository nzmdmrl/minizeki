'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api, activeProfile, Question } from '@/lib/api';
import QuestionPlayer from '@/components/QuestionPlayer';
import { Zeki, Spinner, ErrorBox } from '@/components/Zeki';

type Result = {
  correct: number; total: number; streak: number;
  shield_used: boolean; streak_broken: boolean; shield_left: number;
  rewards: { star: number; reason: string }[];
  star_balance: number;
  new_badges: { id: string; name: string; icon: string; description: string }[];
  suggestion: { category_id: string; category_name: string;
                icon: string; message: string } | null;
};

export default function GorevPage() {
  const router = useRouter();
  const [questions, setQuestions] = useState<Question[] | null>(null);
  const [questId, setQuestId] = useState('');
  const [result, setResult] = useState<Result | null>(null);
  const [err, setErr] = useState('');

  const pid = activeProfile.get();

  const load = async () => {
    if (!pid) { router.replace('/'); return; }
    setErr('');
    try {
      const r = await api.questToday(pid);
      if (r.completed) { router.replace('/'); return; }
      setQuestId(r.quest_id);
      setQuestions(r.questions);
    } catch (e: any) {
      setErr(e.message);
    }
  };

  useEffect(() => { load(); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const finish = async (correct: number, total: number) => {
    try {
      const r = await api.questComplete(questId, correct, total);
      setResult({ ...r, correct, total });
    } catch (e: any) {
      setErr(e.message);
    }
  };

  if (err) return (
    <main className="mx-auto max-w-md px-4 py-12">
      <ErrorBox message={err} onRetry={load} />
    </main>
  );

  if (result) return <SonucEkrani r={result} />;
  if (!questions) return <Spinner label="Sorular hazırlanıyor…" />;

  return (
    <QuestionPlayer
      questions={questions} onFinish={finish}
      title="Bugünün görevi" seconds={0}
      onExit={() => router.push('/')}
      // Gunluk gorev daily_quest'te kayitli: geri gelince ayni sorularla devam eder.
      // Cocuk "her sey gitti" sanmasin.
      exitConfirm={'Şimdi çıkarsan görevin kaydedilir, sonra devam edebilirsin.\n\nÇıkalım mı?'}
    />
  );
}

/* ------------------------------------------------------------------ */

function SonucEkrani({ r }: { r: Result }) {
  const perfect = r.correct === r.total;
  const oran = Math.round((r.correct / r.total) * 100);

  return (
    <main className="mx-auto max-w-md px-4 py-8 no-select">
      <div className="mb-6 text-center">
        <Zeki mood="cheer" size={112} />
        <h1 className="mt-3 text-4xl font-black text-mint-600">
          {perfect ? 'Mükemmel! 💯' : 'Günlük görev tamam! 🎉'}
        </h1>
      </div>

      {/* Skor */}
      <div className="card mb-4 p-6 text-center">
        <p className="text-5xl font-black text-slate-800">
          {r.correct}<span className="text-2xl text-slate-300">/{r.total}</span>
        </p>
        <p className="mt-1 font-extrabold text-slate-400">doğru · %{oran}</p>
      </div>

      {/* Seri */}
      <div className="card mb-4 p-5">
        {r.shield_used ? (
          <>
            <p className="text-center text-xl font-black text-brand-600">
              🛡️ Kalkan kullanıldı!
            </p>
            <p className="mt-1 text-center font-bold text-slate-500">
              Dün oynayamadın ama serin korundu. Devam edelim!
            </p>
            <p className="mt-2 text-center text-sm font-extrabold text-slate-400">
              Kalan kalkan: {r.shield_left}
            </p>
          </>
        ) : r.streak_broken ? (
          <>
            <p className="text-center text-xl font-black text-slate-700">
              Yeniden başlayalım! 💪
            </p>
            <p className="mt-1 text-center font-bold text-slate-500">
              Serin sıfırlandı ama yıldızların ve rozetlerin duruyor.
            </p>
          </>
        ) : (
          <p className="text-center text-2xl font-black text-slate-800">
            🔥 {r.streak} gün
          </p>
        )}
      </div>

      {/* Oduller */}
      {r.rewards.length > 0 && (
        <div className="card mb-4 divide-y divide-slate-100 p-2">
          {r.rewards.map((rw, i) => (
            <div key={i} className="flex items-center justify-between px-3 py-2.5">
              <span className="font-bold text-slate-600">{rw.reason}</span>
              <span className="font-black text-sun-500">+{rw.star} ★</span>
            </div>
          ))}
          <div className="flex items-center justify-between px-3 py-2.5">
            <span className="font-black text-slate-800">Toplam</span>
            <span className="font-black text-slate-800">{r.star_balance} ★</span>
          </div>
        </div>
      )}

      {/* Yeni rozetler */}
      {r.new_badges?.length > 0 && (
        <div className="card mb-4 p-5">
          <p className="mb-3 text-center font-black text-slate-700">Yeni rozet!</p>
          <div className="grid gap-2">
            {r.new_badges.map((b) => (
              <div key={b.id} className="flex items-center gap-3 rounded-2xl
                                          bg-sun-400/10 px-4 py-3">
                <span className="text-3xl">{b.icon}</span>
                <div>
                  <p className="font-black text-slate-800">{b.name}</p>
                  <p className="text-xs font-bold text-slate-500">{b.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Zeki'nin Onerisi — zorunlu degil, cocugun kendi secimi gibi */}
      {r.suggestion && (
        <div className="card mb-4 p-5">
          <div className="flex items-start gap-3">
            <Zeki mood="thinking" size={52} />
            <div className="flex-1">
              <p className="font-bold text-slate-700">
                Zeki diyor ki: &ldquo;{r.suggestion.message}&rdquo;
              </p>
              <div className="mt-3 flex gap-2">
                <Link href={`/oyna/${r.suggestion.category_id}`}
                      className="btn-mint flex-1 text-sm">
                  Hadi! {r.suggestion.icon}
                </Link>
                <Link href="/" className="btn-ghost flex-1 text-sm">
                  Başka zaman
                </Link>
              </div>
            </div>
          </div>
        </div>
      )}

      {!r.suggestion && (
        <Link href="/" className="btn-primary w-full text-lg">Bitir</Link>
      )}
    </main>
  );
}
