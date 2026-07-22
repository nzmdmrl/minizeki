'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { api, Question } from '@/lib/api';
import QuestionPlayer from '@/components/QuestionPlayer';
import { Zeki, Spinner, ErrorBox } from '@/components/Zeki';

/**
 * Kalibrasyon: 8 soru.
 * "Test" gibi gorunmez, ILK OYUN gibi gorunur.
 * Sonuc ekraninda PUAN GOSTERILMEZ — sadece "Harika! Hazirsin".
 */
export default function TanisalimPage() {
  const router = useRouter();
  const { id } = useParams<{ id: string }>();

  const [stage, setStage] = useState<'intro' | 'play' | 'done'>('intro');
  const [questions, setQuestions] = useState<Question[] | null>(null);
  const [err, setErr] = useState('');

  const load = async () => {
    setErr('');
    try {
      const r = await api.calibrateQuestions(id);
      setQuestions(r.questions);
    } catch (e: any) {
      setErr(e.message);
    }
  };

  useEffect(() => { load(); }, [id]); // eslint-disable-line react-hooks/exhaustive-deps

  const finish = async (correct: number, total: number) => {
    try { await api.submitCalibration(id, correct, total); } catch { /* yut */ }
    setStage('done');
  };

  if (err) return (
    <main className="mx-auto max-w-md px-4 py-12">
      <ErrorBox message={err} onRetry={load} />
    </main>
  );

  if (stage === 'intro') {
    return (
      <main className="mx-auto flex min-h-screen max-w-md flex-col items-center
                       justify-center px-4 text-center">
        <Zeki mood="happy" size={128} />
        <h1 className="mt-4 text-3xl font-black text-brand-600">Tanışalım!</h1>
        <p className="mt-3 text-lg font-bold text-slate-500">
          Birkaç soru soracağım.<br />Bilemezsen hiç sorun değil —
          seni tanımak için soruyorum.
        </p>
        <button onClick={() => setStage('play')} disabled={!questions}
                className="btn-primary mt-8 w-full text-lg">
          {questions ? 'Hadi başlayalım!' : 'Hazırlanıyor…'}
        </button>
      </main>
    );
  }

  if (stage === 'play' && questions) {
    return <QuestionPlayer questions={questions} onFinish={finish} title="Tanışma" />;
  }

  if (stage === 'done') {
    return (
      <main className="mx-auto flex min-h-screen max-w-md flex-col items-center
                       justify-center px-4 text-center">
        <Zeki mood="cheer" size={128} />
        {/* PUAN GOSTERILMEZ - kasitli */}
        <h1 className="mt-4 text-4xl font-black text-mint-600">Harika! 🎉</h1>
        <p className="mt-2 text-xl font-bold text-slate-500">Hazırsın.</p>
        <button onClick={() => router.push('/')} className="btn-primary mt-8 w-full text-lg">
          Oynamaya başla
        </button>
      </main>
    );
  }

  return <Spinner label="Hazırlanıyor…" />;
}
