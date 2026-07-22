'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { api, Question, AnswerResult } from '@/lib/api';
import { ProgressBar, Zeki } from './Zeki';

type Props = {
  questions: Question[];
  onFinish: (correct: number, total: number) => void;
  title?: string;
  /** Soru basina sure (sn). 0 = sure yok. */
  seconds?: number;
  /** Cikis. Verilmezse cikis butonu gosterilmez (kalibrasyon gibi). */
  onExit?: () => void;
  /** Cikarken sorulacak onay. Bos ise onay sorulmaz. */
  exitConfirm?: string;
};

/** Dogru cevapta otomatik gecise kadar beklenen sure (ms). */
const AUTO_NEXT_MS = 3000;

/**
 * TASARIM KURALLARI (dokumandan):
 *  - Sure bir oyun mekanigi, tehdit degil: kirmizi ekran / tik sesi / titresim YOK
 *  - Sure bitince soru sessizce gecer, ceza yok
 *  - Yanlis cevapta dogrusu gosterilir + kisa aciklama (aninda geri bildirim)
 *  - Etiket yok: "3. sinif sorusu" veya "seviye 4" YAZILMAZ
 *  - Buyume zihniyeti: "Yanlis!" degil "Dogrusu soyleydi"
 *
 * OTOMATIK GECIS:
 *  - Sadece DOGRU cevapta. Yanlista cocuk dogrusunu okumali, kendi gecmeli.
 *  - Butonda gorunur geri sayim var: habersiz gecis cocugu sasirtir.
 *  - Dokunulursa hemen gecer, sayaci beklemez.
 *  - Rozet/terfi mujdesi varsa otomatik gecis IPTAL: cocuk odulu gormeli.
 *
 * CIKIS:
 *  - Sol ustte SESSIZ bir ok. Buyuk "Cikis" butonu cikmayi davet eder.
 *  - Amac kacis kapisi sunmak, kapiyi gostermek degil.
 *  - Buton olmasa cocuk zaten geri tusuna basar / sekmeyi kapatir;
 *    fark su ki o zaman "sikistim" hissiyle cikar.
 */
export default function QuestionPlayer({
  questions, onFinish, title, seconds = 0, onExit, exitConfirm,
}: Props) {
  const [i, setI] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [result, setResult] = useState<AnswerResult | null>(null);
  const [correctCount, setCorrectCount] = useState(0);
  const [left, setLeft] = useState(seconds);
  const [busy, setBusy] = useState(false);
  const [autoPct, setAutoPct] = useState(0);       // 0-100 geri sayim dolumu
  const [askExit, setAskExit] = useState(false);   // cikis onay modali

  const startRef = useRef<number>(Date.now());
  const q = questions[i];
  const last = i === questions.length - 1;

  // Soru degisince sifirla
  useEffect(() => {
    setSelected(null);
    setResult(null);
    setLeft(seconds);
    setAutoPct(0);
    startRef.current = Date.now();
  }, [i, seconds]);

  const next = useCallback(() => {
    if (last) onFinish(correctCount, questions.length);
    else setI((n) => n + 1);
  }, [last, correctCount, questions.length, onFinish]);

  const send = useCallback(async (choice: number) => {
    if (result || busy) return;
    setBusy(true);
    setSelected(choice);
    try {
      const r = await api.answer(q.token, choice, Date.now() - startRef.current);
      setResult(r);
      if (r.correct) setCorrectCount((c) => c + 1);
    } catch {
      // Ag hatasi: soruyu atla, cocugu bekletme
      setResult({
        correct: false, answer_index: -1, correct_option: '',
        medal_up: false, advanced: false, total_correct: 0, star_balance: 0,
      });
    } finally {
      setBusy(false);
    }
  }, [q, result, busy]);

  // Sure sayaci — bitince SESSIZCE gecer, ceza yok
  useEffect(() => {
    if (!seconds || result) return;
    if (left <= 0) {
      // -1 = "cevap vermedi". Sunucu yanlis sayar ama ekranda ceza yok.
      send(-1 as number);
      return;
    }
    const t = setTimeout(() => setLeft((s) => s - 1), 1000);
    return () => clearTimeout(t);
  }, [left, seconds, result, send]);

  // Dogru cevapta otomatik gecis.
  // Odul mujdesi (madalya/yeni sorular) varsa cocuk gormeli -> otomatik gecis yok.
  const hasReward = !!(result?.medal_up || result?.advance_message);
  const autoNext = !!result?.correct && !hasReward;

  useEffect(() => {
    if (!autoNext) return;
    const t0 = Date.now();
    const iv = setInterval(() => {
      const p = Math.min(100, ((Date.now() - t0) / AUTO_NEXT_MS) * 100);
      setAutoPct(p);
      if (p >= 100) {
        clearInterval(iv);
        next();
      }
    }, 50);
    return () => clearInterval(iv);
  }, [autoNext, next]);

  const exit = useCallback(() => {
    if (!onExit) return;
    // Ilk soruda henuz bir sey yapmamis -> onay sorma, hemen cikar
    if (exitConfirm && (i > 0 || result)) {
      setAskExit(true);
      return;
    }
    onExit();
  }, [onExit, exitConfirm, i, result]);

  // ESC ile modali kapat
  useEffect(() => {
    if (!askExit) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setAskExit(false); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [askExit]);

  if (!q) return null;

  const pct = ((i + (result ? 1 : 0)) / questions.length) * 100;
  const timePct = seconds ? (left / seconds) * 100 : 0;

  return (
    <div className="mx-auto flex min-h-screen max-w-2xl flex-col px-4 py-4 no-select">
      {/* Ilerleme */}
      <div className="mb-4">
        <div className="mb-2 flex items-center gap-2 text-sm font-extrabold">
          {/* Cikis: sessiz, kucuk, sol ustte. Vurgulu olmamali. */}
          {onExit && (
            <button onClick={exit} aria-label="Çık"
                    className="-ml-1 rounded-lg px-2 py-1 text-lg leading-none
                               text-slate-300 transition hover:bg-slate-100
                               hover:text-slate-500">
              ←
            </button>
          )}
          <span className="text-slate-400">
            {title || 'Soru'} {i + 1}/{questions.length}
          </span>
          <span className="ml-auto text-mint-600">{correctCount} doğru</span>
        </div>
        <ProgressBar value={pct} />

        {/* Sure cubugu: renk kirmizidan gecmez, sadece kisalir */}
        {seconds > 0 && !result && (
          <div className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-slate-100">
            <div
              className="h-full rounded-full bg-sun-400 transition-all duration-1000 ease-linear"
              style={{ width: `${timePct}%` }}
            />
          </div>
        )}
      </div>

      {/* Soru karti */}
      <div className="card mb-4 p-6 animate-pop">
        {q.category_name && (
          <div className="mb-3 inline-flex items-center gap-1.5 rounded-full
                          bg-slate-50 px-3 py-1 text-xs font-extrabold text-slate-500">
            <span>{q.category_icon}</span>
            {q.category_name}
          </div>
        )}

        {q.svg && (
          <div className="clock-wrap mb-4" dangerouslySetInnerHTML={{ __html: q.svg }} />
        )}
        {q.image_url && (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={q.image_url} alt="" className="mx-auto mb-4 max-h-48 rounded-2xl" />
        )}

        <p className="whitespace-pre-line text-2xl font-extrabold leading-snug text-slate-800">
          {q.text}
        </p>
      </div>

      {/* Siklar */}
      <div className="grid gap-3">
        {q.options.map((opt, idx) => {
          let cls = 'opt';
          if (result) {
            if (idx === result.answer_index) cls += ' opt-correct';
            else if (idx === selected) cls += ' opt-wrong';
            else cls += ' opt-muted';
          } else if (selected === idx) {
            cls += ' border-brand-400';
          }
          return (
            <button key={idx} onClick={() => send(idx)} disabled={!!result || busy}
                    className={cls}>
              {opt}
            </button>
          );
        })}
      </div>

      {/* Geri bildirim — aninda, buyume zihniyetiyle */}
      {result && (
        <div className="mt-4 animate-slide-up">
          <div className={`card p-5 ${result.correct
            ? 'border-mint-400 bg-mint-400/10'
            : 'border-slate-200'}`}>
            <div className="flex items-start gap-3">
              <Zeki mood={result.correct ? 'cheer' : 'calm'} size={48} />
              <div className="flex-1">
                <p className={`text-lg font-black ${result.correct
                  ? 'text-mint-600' : 'text-slate-700'}`}>
                  {result.correct ? 'Harika! 🎉' : 'Doğrusu şöyleydi'}
                </p>
                {!result.correct && result.correct_option && (
                  <p className="mt-0.5 font-extrabold text-slate-800">
                    {result.correct_option}
                  </p>
                )}
                {result.advance_message && (
                  <p className="mt-2 font-extrabold text-brand-600">
                    {result.advance_message}
                  </p>
                )}
                {result.medal_up && result.medal && (
                  <p className="mt-2 font-extrabold text-sun-500">
                    {result.medal.icon} {result.medal.name} madalya! +10 ★
                  </p>
                )}
              </div>
            </div>
          </div>

          <button onClick={next}
                  className="relative mt-3 w-full overflow-hidden btn-primary text-lg">
            {/* Otomatik gecis dolgusu: cocuk ne olacagini gorur */}
            {autoNext && (
              <span aria-hidden="true"
                    className="absolute inset-y-0 left-0 bg-white/25"
                    style={{ width: `${autoPct}%` }} />
            )}
            <span className="relative">
              {last ? 'Bitir' : 'Devam et'} →
            </span>
          </button>
        </div>
      )}

      {/* Cikis onayi: tarayici confirm() yerine kendi modalimiz */}
      {askExit && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 px-5"
             onClick={() => setAskExit(false)}>
          <div className="card w-full max-w-sm animate-pop p-7"
               onClick={(e) => e.stopPropagation()}>
            {(exitConfirm ?? '').split('\n\n').map((satir, idx) => (
              <p key={idx}
                 className={idx === 0
                   ? 'text-lg font-bold leading-relaxed text-slate-600'
                   : 'mt-3 text-xl font-black text-slate-800'}>
                {satir}
              </p>
            ))}
            <div className="mt-7 flex gap-3">
              <button className="btn-ghost flex-1 !px-4"
                      onClick={() => setAskExit(false)}>
                Devam et
              </button>
              <button className="btn-primary flex-1 !px-4"
                      onClick={() => { setAskExit(false); onExit?.(); }}>
                Çık
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
