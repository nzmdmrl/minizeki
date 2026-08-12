'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

/**
 * TEK ÇİZGİ — mola oyunu
 *
 * Kural: 1'den başlayarak sayıları sırayla birleştir, her kareden
 * tam bir kez geç.
 *
 * MOLA OYUNU TASARIM KURALLARI:
 *   - Kaybetme yok, süre baskısı yok, puan yok
 *   - Ses yok (sınıfta/otobüste kullanılabilsin)
 *   - Zorlanınca "Yeni bölüm" ile atlanabilir
 *   - Bölüm numarası sadece bilgi; hedef değil
 */

// Kolaydan zora: küçük tahta + çok nokta = kolay
const PLAN = [
  { n: 4, dots: 6 }, { n: 4, dots: 5 }, { n: 4, dots: 4 },
  { n: 5, dots: 8 }, { n: 5, dots: 6 }, { n: 5, dots: 5 }, { n: 5, dots: 4 },
  { n: 6, dots: 8 }, { n: 6, dots: 6 }, { n: 6, dots: 5 }, { n: 6, dots: 4 },
  { n: 7, dots: 9 }, { n: 7, dots: 8 }, { n: 7, dots: 7 }, { n: 7, dots: 6 },
];

type Level = { n: number; checkpoints: Record<number, number>; solution: number[] };

function komsular(n: number): number[][] {
  const s = n * n, nb: number[][] = [];
  for (let i = 0; i < s; i++) {
    const r = Math.floor(i / n), c = i % n, o: number[] = [];
    if (r > 0) o.push(i - n);
    if (r < n - 1) o.push(i + n);
    if (c > 0) o.push(i - 1);
    if (c < n - 1) o.push(i + 1);
    nb.push(o);
  }
  return nb;
}

/** Kalan kareler hala birbirine bagli mi? (cikmaz sokak kontrolu) */
function bagliMi(start: number, seen: boolean[], nb: number[][], size: number) {
  const st = [start], vis = new Set([start]);
  while (st.length) {
    const cur = st.pop()!;
    for (const x of nb[cur]) if (!seen[x] && !vis.has(x)) { vis.add(x); st.push(x); }
  }
  let left = 0;
  for (let i = 0; i < size; i++) if (!seen[i]) left++;
  return vis.size >= left;
}

/** Tum kareleri bir kez gezen yol uret (Hamilton yolu) */
function hamiltonYolu(n: number): number[] | null {
  const size = n * n, nb = komsular(n);
  for (let deneme = 0; deneme < 60; deneme++) {
    const seen = new Array(size).fill(false), path: number[] = [];
    let butce = 120000, ok = false;

    const dfs = (cur: number): boolean => {
      if (butce-- <= 0) return false;
      seen[cur] = true; path.push(cur);
      if (path.length === size) { ok = true; return true; }
      const opts = nb[cur].filter((x) => !seen[x]);
      // Az secenegi olan komsuya once git (Warnsdorff)
      opts.sort((x, y) =>
        nb[x].filter((z) => !seen[z]).length - nb[y].filter((z) => !seen[z]).length
        || Math.random() - 0.5);
      for (const x of opts) {
        seen[x] = true;
        const uygun = bagliMi(x, seen, nb, size);
        seen[x] = false;
        if (uygun && dfs(x)) return true;
      }
      seen[cur] = false; path.pop(); return false;
    };

    dfs(Math.floor(Math.random() * size));
    if (ok) return path;
  }
  return null;
}

function bolumUret(L: number): Level {
  const spec = PLAN[Math.min(L, PLAN.length) - 1];
  const sol = hamiltonYolu(spec.n);
  if (!sol) {
    // Uretilemezse daha kucuk tahtaya dus
    const yedek = hamiltonYolu(4)!;
    const cp: Record<number, number> = {};
    [0, 5, 10, 15].forEach((p, k) => { cp[yedek[p]] = k + 1; });
    return { n: 4, checkpoints: cp, solution: yedek };
  }
  const size = spec.n * spec.n;
  const gap = (size - 1) / (spec.dots - 1);
  const marks = [0];
  for (let k = 1; k < spec.dots - 1; k++) {
    const jit = Math.floor(Math.random() * 3) - 1;
    marks.push(Math.min(size - 2, Math.max(marks[k - 1] + 2, Math.round(k * gap) + jit)));
  }
  marks.push(size - 1);
  const checkpoints: Record<number, number> = {};
  marks.forEach((p, k) => { checkpoints[sol[p]] = k + 1; });
  return { n: spec.n, checkpoints, solution: sol };
}

// ---------------------------------------------------------------- Bilesen

export default function TekCizgi({ onLevel }: { onLevel?: (n: number) => void }) {
  const [bolum, setBolum] = useState(1);
  const [level, setLevel] = useState<Level | null>(null);
  const [path, setPath] = useState<number[]>([]);
  const [kazandi, setKazandi] = useState(false);
  const [mesaj, setMesaj] = useState('');
  const cizimRef = useRef(false);
  const boardRef = useRef<HTMLDivElement>(null);

  const yukle = useCallback((no: number) => {
    setLevel(bolumUret(no));
    setPath([]);
    setKazandi(false);
    setMesaj('');
    onLevel?.(no);
  }, [onLevel]);

  useEffect(() => { yukle(1); }, []); // eslint-disable-line

  const n = level?.n ?? 4;
  const nb = useMemo(() => komsular(n), [n]);

  const siradakiSayi = useCallback(() => {
    if (!level) return 1;
    let gorulen = 0;
    for (const i of path) {
      const s = level.checkpoints[i];
      if (s) gorulen = s;
    }
    return gorulen + 1;
  }, [level, path]);

  const girilebilir = useCallback((i: number) => {
    if (!level) return false;
    if (path.includes(i)) return false;
    if (path.length === 0) return level.checkpoints[i] === 1;
    if (!nb[path[path.length - 1]].includes(i)) return false;
    const s = level.checkpoints[i];
    if (s && s !== siradakiSayi()) return false;
    return true;
  }, [level, path, nb, siradakiSayi]);

  const ekle = useCallback((i: number) => {
    if (!level || kazandi) return;
    if (!girilebilir(i)) return;
    const yeni = [...path, i];
    setPath(yeni);
    setMesaj('');
    if (yeni.length === n * n) {
      const sonSayi = Math.max(...Object.values(level.checkpoints));
      const bittiMi = level.checkpoints[i] === sonSayi;
      if (bittiMi) {
        setKazandi(true);
        setMesaj('Tamamladın!');
      }
    }
  }, [level, path, kazandi, girilebilir, n]);

  const kareyiBul = (e: React.PointerEvent | PointerEvent): number | null => {
    const b = boardRef.current?.getBoundingClientRect();
    if (!b) return null;
    const s = b.width / n;
    const cx = ('clientX' in e ? e.clientX : 0) - b.left;
    const cy = ('clientY' in e ? e.clientY : 0) - b.top;
    if (cx < 0 || cy < 0 || cx >= b.width || cy >= b.height) return null;
    return Math.floor(cy / s) * n + Math.floor(cx / s);
  };

  const basla = (e: React.PointerEvent) => {
    const i = kareyiBul(e);
    if (i === null) return;
    cizimRef.current = true;
    (e.target as Element).setPointerCapture?.(e.pointerId);
    // Cizilmis bir kareye dokunulursa oraya kadar geri al
    const idx = path.indexOf(i);
    if (idx >= 0) setPath(path.slice(0, idx + 1));
    else ekle(i);
  };

  const surukle = (e: React.PointerEvent) => {
    if (!cizimRef.current || kazandi) return;
    const i = kareyiBul(e);
    if (i === null) return;
    const idx = path.indexOf(i);
    if (idx >= 0 && idx < path.length - 1) { setPath(path.slice(0, idx + 1)); return; }
    ekle(i);
  };

  const bitir = () => { cizimRef.current = false; };

  const geriAl = () => {
    if (kazandi) return;
    setPath(path.slice(0, -1));
    setMesaj('');
  };

  if (!level) {
    return (
      <div className="grid h-72 place-items-center">
        <p className="font-bold text-slate-400">Bulmaca hazırlanıyor…</p>
      </div>
    );
  }

  const sonSayi = Math.max(...Object.values(level.checkpoints));
  const siradaki = siradakiSayi();

  return (
    <div className="mx-auto w-full max-w-md no-select">
      <div className="mb-3 flex items-center justify-between">
        <span className="text-sm font-black text-slate-500">
          Bölüm {bolum} · {n}×{n}
        </span>
        <span className="text-sm font-bold text-slate-400">
          {path.length}/{n * n} kare
        </span>
      </div>

      {/* Tahta */}
      <div ref={boardRef}
           onPointerDown={basla} onPointerMove={surukle}
           onPointerUp={bitir} onPointerLeave={bitir} onPointerCancel={bitir}
           className="relative aspect-square w-full touch-none overflow-hidden
                      rounded-2xl border-4 border-slate-300 bg-white"
           style={{ display: 'grid',
                    gridTemplateColumns: `repeat(${n}, 1fr)`,
                    gridTemplateRows: `repeat(${n}, 1fr)` }}>
        {/* Cizilen iz: karelerin merkezlerini birlestiren tek cizgi.
            Oyunun asil geri bildirimi budur — cocuk nereden gectigini
            gorebilmeli. Karelerin arka plan rengi tek basina yetmez. */}
        {/* Tahta kare oldugu icin viewBox birim = hucre.
            strokeWidth 0.34 -> cizgi hucre genisliginin ucte biri kadar;
            tahta buyudukce cizgi de oransal buyur. */}
        <svg className="pointer-events-none absolute inset-0 z-[2] h-full w-full"
             viewBox={`0 0 ${n} ${n}`}>
          {path.length > 1 && (
            <polyline
              points={path.map((i) =>
                `${(i % n) + 0.5},${Math.floor(i / n) + 0.5}`).join(' ')}
              fill="none"
              stroke={kazandi ? '#10b981' : '#3b82f6'}
              strokeOpacity="0.5"
              strokeWidth={0.34}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          )}
        </svg>

        {Array.from({ length: n * n }, (_, i) => {
          const sayi = level.checkpoints[i];
          const izde = path.includes(i);
          const sonKare = path[path.length - 1] === i;
          return (
            // Izgara cizgileri: soluk olursa cocuk kareleri ayirt edemiyor.
            // Son sutun/satirda ic cizgi yok (dis cerceve zaten var).
            <div key={i}
                 className={`relative ${
                   (i % n) < n - 1 ? 'border-r-2 border-r-slate-300' : ''} ${
                   Math.floor(i / n) < n - 1 ? 'border-b-2 border-b-slate-300' : ''}`}>
              {izde && (
                <div className={`absolute inset-[22%] rounded-md ${
                  kazandi ? 'bg-mint-400/20' : 'bg-brand-400/15'}`} />
              )}
              {sayi && (
                <div className={`absolute inset-[18%] z-[3] grid place-items-center
                                 rounded-full text-lg font-black transition
                  ${izde
                    ? (kazandi ? 'bg-mint-500 text-white' : 'bg-brand-500 text-white')
                    : 'bg-slate-800 text-white'}
                  ${!izde && sayi === siradaki ? 'ring-4 ring-brand-300' : ''}`}>
                  {sayi}
                </div>
              )}
              {sonKare && !sayi && (
                <div className="absolute inset-[34%] z-[3] rounded-full bg-brand-600
                                ring-4 ring-brand-200" />
              )}
            </div>
          );
        })}
      </div>

      {/* Durum */}
      <p className={`mt-3 min-h-6 text-center text-sm font-extrabold ${
        kazandi ? 'text-mint-600' : 'text-slate-400'}`}>
        {mesaj || (path.length === 0
          ? '1 numaradan başla, parmağını sürükle'
          : `Sırada ${Math.min(siradaki, sonSayi)} numara`)}
      </p>

      {/* Kontroller */}
      <div className="mt-3 grid grid-cols-3 gap-2">
        <button onClick={geriAl} disabled={!path.length || kazandi}
                className="btn-ghost text-sm">Geri</button>
        <button onClick={() => yukle(bolum)} className="btn-ghost text-sm">
          Baştan
        </button>
        {kazandi ? (
          <button onClick={() => { const y = bolum + 1; setBolum(y); yukle(y); }}
                  className="btn-mint text-sm">Sonraki →</button>
        ) : (
          <button onClick={() => { const y = bolum + 1; setBolum(y); yukle(y); }}
                  className="btn-ghost text-sm">Yeni bölüm</button>
        )}
      </div>
    </div>
  );
}
