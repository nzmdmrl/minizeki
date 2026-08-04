'use client';

import { useEffect, useState, useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { activeProfile } from '@/lib/api';
import { Zeki, Spinner, ErrorBox, ProgressBar } from '@/components/Zeki';

/**
 * OKUMA VE ANLAMA EKRANI
 *
 * AKIS:
 *   hazir -> okuma (sure sayilir) -> sorular -> sonuc
 *
 * NEDEN MIKROFON YOK:
 *   Okuma hizi = kelime / sure. Bunun icin ses tanimaya gerek yok.
 *   Ses tanima cocuk sesinde guvenilmez, sesi ucuncu tarafa gonderir,
 *   iOS Safari'de calismaz. Sure olcumu ise kesindir ve izin istemez.
 *
 * TASARIM KURALLARI (dokumandan):
 *   - Geri sayim YOK. Sure sayilir ama cocuga gosterilmez —
 *     gorunen sayac baski yaratir, okuma hizini bozar.
 *   - Sorularda metin gizli. "Tekrar bak" butonu var ama not dusulur.
 *   - Yanlis cevapta ceza yok, dogrusu gosterilir.
 */

const API = process.env.NEXT_PUBLIC_API_URL || '';

type Soru = { token: string; text: string; options: string[]; type: string };
type Metin = { id: string; title: string; text: string; word_count: number };

export default function OkumaPage() {
  const router = useRouter();
  const [asama, setAsama] = useState<'yukleniyor' | 'hazir' | 'okuma' |
                                     'sorular' | 'sonuc'>('yukleniyor');
  const [metin, setMetin] = useState<Metin | null>(null);
  const [sorular, setSorular] = useState<Soru[]>([]);
  const [sonuc, setSonuc] = useState<any>(null);
  const [err, setErr] = useState('');
  const [sessiz, setSessiz] = useState(false);
  const [tekrar, setTekrar] = useState(false);

  const basRef = useRef<number>(0);
  const sureRef = useRef<number>(0);
  const pid = typeof window !== 'undefined' ? activeProfile.get() : null;

  const yukle = async (yeniMetin = true) => {
    if (!pid) { router.replace('/'); return; }
    setErr('');
    setAsama('yukleniyor');
    try {
      const t = localStorage.getItem('mz_token');
      const h = { Authorization: `Bearer ${t}`, 'Content-Type': 'application/json' };

      let m = metin;
      if (yeniMetin || !m) {
        const r = await fetch(`${API}/api/reading/story?profile_id=${pid}`, { headers: h });
        if (!r.ok) throw new Error((await r.json()).detail || 'Metin alınamadı');
        m = await r.json();
        setMetin(m);
      }

      const rq = await fetch(
        `${API}/api/reading/questions?story_id=${m!.id}&profile_id=${pid}`,
        { headers: h });
      if (!rq.ok) throw new Error('Sorular alınamadı');
      setSorular((await rq.json()).questions);
      setAsama('hazir');
    } catch (e: any) {
      setErr(e.message);
      setAsama('hazir');
    }
  };

  useEffect(() => { yukle(); }, []); // eslint-disable-line

  const basla = () => {
    basRef.current = Date.now();
    setAsama('okuma');
  };

  const okudum = () => {
    sureRef.current = Date.now() - basRef.current;
    setAsama('sorular');
  };

  const bitir = async (cevaplar: number[], baktiMi: boolean) => {
    try {
      const t = localStorage.getItem('mz_token');
      const r = await fetch(`${API}/api/reading/complete`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${t}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          profile_id: pid, story_id: metin!.id,
          mode: sessiz ? 'silent' : 'timed',
          duration_ms: sessiz ? 0 : sureRef.current,
          answers: cevaplar, peeked: baktiMi, reread: tekrar,
        }),
      });
      setSonuc(await r.json());
      setAsama('sonuc');
    } catch (e: any) {
      setErr(e.message);
    }
  };

  // Cikis: sorulara baslanmissa onay sor (diger kategorilerdeki gibi),
  // yoksa sessizce cik.
  const cik = () => {
    if (asama === 'sorular' || asama === 'okuma') {
      if (!confirm('Okumayı bırakmak istiyor musun? İlerlemen kaydedilmeyecek.')) {
        return;
      }
    }
    router.push('/kategoriler');
  };

  const tekrarOku = () => {
    setTekrar(true);
    setSonuc(null);
    setAsama('hazir');
  };

  if (err && asama !== 'sonuc') {
    return (
      <main className="mx-auto max-w-lg px-4 py-12">
        <ErrorBox message={err} onRetry={() => yukle()} />
      </main>
    );
  }
  if (asama === 'yukleniyor' || !metin) return <Spinner label="Hikâye hazırlanıyor…" />;

  if (asama === 'hazir')
    return <HazirEkrani metin={metin} sessiz={sessiz} setSessiz={setSessiz}
                        tekrar={tekrar} onBasla={basla} />;
  if (asama === 'okuma')
    return <OkumaEkrani metin={metin} sessiz={sessiz} onBitir={okudum}
                        onCik={cik} />;
  if (asama === 'sorular')
    return <SoruEkrani metin={metin} sorular={sorular} onBitir={bitir}
                       onCik={cik} />;
  return <SonucEkrani sonuc={sonuc} metin={metin}
                      onTekrar={tekrarOku} onYeni={() => { setTekrar(false); yukle(true); }} />;
}

/* ------------------------------------------------------------------ */

function HazirEkrani({ metin, sessiz, setSessiz, tekrar, onBasla }: any) {
  return (
    <main className="mx-auto max-w-lg px-4 py-8 no-select">
      <div className="mb-4 flex items-center gap-3">
        <Link href="/kategoriler" className="text-2xl font-black text-slate-300
                                              hover:text-slate-500">←</Link>
        <h1 className="text-2xl font-black text-slate-800">Okuma</h1>
      </div>

      <div className="mb-5 text-center">
        <Zeki mood="happy" size={96} />
      </div>

      <div className="card p-6 text-center">
        {tekrar && (
          <p className="mb-3 rounded-xl bg-brand-50 px-3 py-2 text-sm
                        font-extrabold text-brand-600">
            Bu sefer daha çok şey fark edeceksin
          </p>
        )}
        <p className="text-sm font-extrabold uppercase tracking-wide text-slate-400">
          Hikâye
        </p>
        <h2 className="mt-1 text-3xl font-black text-slate-800">{metin.title}</h2>
        <p className="mt-2 font-bold text-slate-500">
          {metin.word_count} kelime · sonra 5 soru
        </p>

        <button onClick={onBasla} className="btn-primary mt-6 w-full text-lg">
          Hazırım, okumaya başlıyorum
        </button>

        <label className="mt-4 flex cursor-pointer items-start gap-3 rounded-2xl
                          bg-slate-50 p-4 text-left">
          <input type="checkbox" checked={sessiz} className="mt-1 h-5 w-5"
                 onChange={(e) => setSessiz(e.target.checked)} />
          <div>
            <p className="font-black text-slate-700">İçimden okuyacağım</p>
            <p className="text-xs font-bold text-slate-500">
              Süre ölçülmez, sadece sorular sorulur.
            </p>
          </div>
        </label>
      </div>

      <p className="mt-4 text-center text-xs font-bold text-slate-400">
        Acele etmene gerek yok. Anladığından emin olana kadar oku.
      </p>
    </main>
  );
}

/* ------------------------------------------------------------------ */

function OkumaEkrani({ metin, sessiz, onBitir, onCik }: any) {
  return (
    <main className="mx-auto max-w-2xl px-4 py-6 no-select">
      {/* Cikis: sessiz, sol ustte — diger kategorilerdeki gibi */}
      <button onClick={onCik} aria-label="Çık"
              className="mb-2 -ml-1 rounded-lg px-2 py-1 text-lg leading-none
                         text-slate-300 transition hover:bg-slate-100
                         hover:text-slate-500">
        ←
      </button>

      <div className="card mb-4 p-6 md:p-8">
        <h2 className="mb-4 text-2xl font-black text-slate-800">{metin.title}</h2>
        {/* Okuma metni: buyuk punto, genis satir araligi, kisa satir uzunlugu.
            Bu yas grubunda okunabilirlik icin uc temel ayar. */}
        <div className="whitespace-pre-line text-xl leading-[1.9] text-slate-800"
             style={{ maxWidth: '38ch', fontWeight: 600 }}>
          {metin.text}
        </div>
      </div>

      <button onClick={onBitir} className="btn-mint w-full text-lg">
        {sessiz ? 'Okudum, sorulara geç' : 'Okudum ✓'}
      </button>

      {/* Sayac BILEREK gosterilmiyor: gorunur sayac baski yaratir
          ve cocugun okuma hizini bozar. Sure arka planda olculur. */}
      <p className="mt-3 text-center text-xs font-bold text-slate-400">
        Bitirince dokun
      </p>
    </main>
  );
}

/* ------------------------------------------------------------------ */

// Dogru cevapta otomatik gecis suresi.
// QuestionPlayer ile AYNI olmali; farkli olursa cocuk iki ekranda
// farkli ritim hisseder.
const AUTO_NEXT_MS = 1500;

function SoruEkrani({ metin, sorular, onBitir, onCik }: any) {
  const [i, setI] = useState(0);
  const [cevaplar, setCevaplar] = useState<number[]>([]);
  const [secili, setSecili] = useState<number | null>(null);
  const [dogruIdx, setDogruIdx] = useState<number | null>(null);
  const [bakti, setBakti] = useState(false);
  const [metinAcik, setMetinAcik] = useState(false);
  const [bekle, setBekle] = useState(false);
  const [autoPct, setAutoPct] = useState(0);

  const q = sorular[i];
  const son = i === sorular.length - 1;
  const cevaplandi = dogruIdx !== null;
  const dogruMu = cevaplandi && secili === dogruIdx;

  // Cift gonderim korumasi: otomatik gecis + elle tiklama ayni anda
  // tetiklenirse onBitir iki kez cagrilir ve cocugun okumasi iki kez
  // kaydedilir. Bu bayrak bunu engeller.
  const bitirildi = useRef(false);

  const ilerle = useCallback(() => {
    const yeni = [...cevaplar, secili as number];
    setCevaplar(yeni);
    setSecili(null);
    setDogruIdx(null);
    setMetinAcik(false);
    setAutoPct(0);

    if (son) {
      if (bitirildi.current) return;
      bitirildi.current = true;
      onBitir(yeni, bakti);
    } else {
      setI((x) => x + 1);
    }
  }, [cevaplar, secili, son, bakti, onBitir]);

  // Dogru cevapta otomatik gecis — diger kategorilerdeki gibi.
  // Yanlista otomatik gecis YOK: cocuk dogru cevabi okuyabilmeli.
  useEffect(() => {
    if (!dogruMu) return;
    const t0 = Date.now();
    const iv = setInterval(() => {
      const p = Math.min(100, ((Date.now() - t0) / AUTO_NEXT_MS) * 100);
      setAutoPct(p);
      if (p >= 100) {
        clearInterval(iv);
        ilerle();
      }
    }, 50);
    return () => clearInterval(iv);
  }, [dogruMu, ilerle]);

  const sec = async (idx: number) => {
    if (cevaplandi || bekle) return;
    setBekle(true);
    setSecili(idx);
    try {
      const t = localStorage.getItem('mz_token');
      const r = await fetch(`${API}/api/answer`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${t}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: q.token, selected: idx, duration_ms: 0 }),
      });
      const d = await r.json();
      setDogruIdx(d.answer_index);
    } catch {
      setDogruIdx(idx);   // ag hatasi: cocugu bekletme
    } finally {
      setBekle(false);
    }
  };

  return (
    <main className="mx-auto max-w-2xl px-4 py-6 no-select">
      <div className="mb-4">
        <div className="mb-2 flex items-center gap-2 text-sm font-extrabold">
          {/* Cikis: sessiz, kucuk, sol ustte — diger kategorilerdeki gibi */}
          <button onClick={onCik} aria-label="Çık"
                  className="-ml-1 rounded-lg px-2 py-1 text-lg leading-none
                             text-slate-300 transition hover:bg-slate-100
                             hover:text-slate-500">
            ←
          </button>
          <span className="text-slate-400">Soru {i + 1}/{sorular.length}</span>
          <button onClick={() => { setMetinAcik(!metinAcik); setBakti(true); }}
                  className="ml-auto rounded-lg px-3 py-1.5 text-xs font-extrabold
                             text-brand-500 hover:bg-brand-50">
            {metinAcik ? 'Hikâyeyi kapat' : 'Hikâyeye tekrar bak'}
          </button>
        </div>
        <ProgressBar value={((i + (cevaplandi ? 1 : 0)) / sorular.length) * 100} />
      </div>

      {metinAcik && (
        <div className="card mb-4 max-h-56 overflow-y-auto p-5 animate-slide-up">
          <p className="whitespace-pre-line text-base font-semibold
                        leading-relaxed text-slate-600">{metin.text}</p>
        </div>
      )}

      <div className="card mb-4 p-6 animate-pop">
        <p className="text-2xl font-black leading-snug text-slate-800">{q.text}</p>
      </div>

      <div className="grid gap-3">
        {q.options.map((o: string, idx: number) => {
          let k = 'opt';
          if (cevaplandi) {
            if (idx === dogruIdx) k += ' opt-correct';
            else if (idx === secili) k += ' opt-wrong';
            else k += ' opt-muted';
          } else if (secili === idx) {
            k += ' opt-secili';
          }
          return (
            <button key={idx} onClick={() => sec(idx)}
                    disabled={cevaplandi || bekle} className={k}>
              {o}
            </button>
          );
        })}
      </div>

      {/* Dogru cevap: kisa mujde + otomatik gecis cubugu */}
      {dogruMu && (
        <div className="mt-4 animate-slide-up">
          <div className="card border-mint-400 bg-mint-400/10 p-4">
            <div className="flex items-center gap-3">
              <Zeki mood="cheer" size={40} />
              <p className="text-lg font-black text-mint-600">Doğru! 🎉</p>
            </div>
            <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-mint-400/20">
              <div className="h-full rounded-full bg-mint-500 transition-none"
                   style={{ width: `${autoPct}%` }} />
            </div>
          </div>
        </div>
      )}

      {/* Yanlis cevap: otomatik gecis YOK, cocuk dogruyu okusun */}
      {cevaplandi && !dogruMu && (
        <div className="mt-4 animate-slide-up">
          <div className="card p-5">
            <div className="flex items-start gap-3">
              <Zeki mood="calm" size={48} />
              <div className="flex-1">
                <p className="text-lg font-black text-slate-700">Doğrusu şöyleydi</p>
                <p className="mt-0.5 font-extrabold text-slate-800">
                  {q.options[dogruIdx as number]}
                </p>
              </div>
            </div>
          </div>
          <button onClick={ilerle} className="btn-primary mt-3 w-full text-lg">
            {son ? 'Bitir' : 'Devam et'} →
          </button>
        </div>
      )}

      {!cevaplandi && (
        <p className="mt-4 text-center text-sm font-bold text-slate-400">
          Cevabını seç
        </p>
      )}
    </main>
  );
}

/* ------------------------------------------------------------------ */

function SonucEkrani({ sonuc, metin, onTekrar, onYeni }: any) {
  if (!sonuc) return <Spinner />;
  const iyi = sonuc.accuracy >= 80;

  const HIZ_ETIKET: Record<string, string> = {
    gelisiyor: 'Gelişiyor',
    beklenen: 'Sınıfın için beklenen hızda',
    hizli: 'Sınıfın için hızlı',
  };

  return (
    <main className="mx-auto max-w-lg px-4 py-8 no-select">
      <div className="mb-5 text-center">
        <Zeki mood={iyi ? 'cheer' : 'happy'} size={104} />
        <h1 className={`mt-3 text-3xl font-black ${
          iyi ? 'text-mint-600' : 'text-slate-800'}`}>
          {sonuc.message}
        </h1>
      </div>

      <div className="card mb-4 p-6 text-center">
        <p className="text-5xl font-black text-slate-800">
          {sonuc.correct}<span className="text-2xl text-slate-300">/{sonuc.total}</span>
        </p>
        <p className="mt-1 font-extrabold text-slate-400">
          doğru · %{sonuc.accuracy} anlama
        </p>
      </div>

      {sonuc.speed && (
        <div className="card mb-4 p-5 text-center">
          <p className="text-xs font-extrabold uppercase tracking-wide text-slate-400">
            Okuma hızın
          </p>
          <p className="mt-1 text-3xl font-black text-brand-600">
            {sonuc.speed.wpm}
            <span className="ml-1 text-base font-bold text-slate-400">kelime/dk</span>
          </p>
          <p className="mt-1 text-sm font-bold text-slate-500">
            {HIZ_ETIKET[sonuc.speed.durum] || ''}
          </p>
        </div>
      )}

      {sonuc.rewards?.length > 0 && (
        <div className="card mb-4 divide-y divide-slate-100 p-2">
          {sonuc.rewards.map((r: any, k: number) => (
            <div key={k} className="flex items-center justify-between px-3 py-2.5">
              <span className="font-bold text-slate-600">{r.reason}</span>
              <span className="font-black text-sun-500">+{r.star} ★</span>
            </div>
          ))}
        </div>
      )}

      {/* Yeni rozetler — okuma kendi rozet setini kullanir */}
      {sonuc.new_badges?.length > 0 && (
        <div className="card mb-4 p-5">
          <p className="mb-3 text-center font-black text-slate-700">Yeni rozet!</p>
          <div className="grid gap-2">
            {sonuc.new_badges.map((b: any) => (
              <div key={b.id} className="flex items-center gap-3 rounded-2xl
                                          bg-sun-400/10 px-4 py-3 animate-pop">
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

      {sonuc.offer_reread && (
        <div className="card mb-4 p-5">
          <div className="flex items-start gap-3">
            <Zeki mood="thinking" size={48} />
            <div className="flex-1">
              <p className="font-bold text-slate-700">
                Zeki diyor ki: &ldquo;Bir daha okusan daha çok şey fark edersin.&rdquo;
              </p>
              <button onClick={onTekrar} className="btn-mint mt-3 w-full text-sm">
                Tekrar okuyayım
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="grid gap-3">
        <button onClick={onYeni} className="btn-primary w-full text-lg">
          Başka hikâye oku
        </button>
        <Link href="/" className="btn-ghost w-full">Ana ekran</Link>
      </div>
    </main>
  );
}
