'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api, activeProfile } from '@/lib/api';
import { Zeki, Spinner, ErrorBox } from '@/components/Zeki';
import TekCizgi from '@/components/games/TekCizgi';

/**
 * MOLA EKRANI
 *
 * Cocuk yeterince calisinca mola hakki kazanir. Mola suresince oyun
 * oynar; sure dolunca ekran kendiliginden kapanir.
 *
 * TASARIM KURALLARI:
 *   - Mola bir ODUL degil, dinlenme HAKKI. Yildiz verilmez, seri etkilenmez.
 *   - Sayac gorunur ama KIRMIZI/TITRESIMLI degil: bu bir yaris degil.
 *   - Son bir dakikada nazik uyari, aniden kapanma yok.
 *   - Cocuk istedigi an "Derse dön" diyebilir; kalan sure saklanir.
 */

type Durum = {
  enabled: boolean;
  mode?: 'off' | 'earned' | 'free';
  daily_limit?: number;
  daily_left?: number;
  can_start?: boolean;
  remaining_seconds?: number;
  study_seconds?: number;
  study_required?: number;
  next_break_in?: number;
  used_today?: number;
  break_minutes?: number;
  study_minutes?: number;
  active?: { id: string; started_at: string; game_id: string } | null;
  games?: { id: string; name: string; description: string; icon: string }[];
};

export default function MolaPage() {
  const router = useRouter();
  const [durum, setDurum] = useState<Durum | null>(null);
  const [err, setErr] = useState('');
  const [oturumId, setOturumId] = useState<string | null>(null);
  const [kalan, setKalan] = useState(0);
  const [bitti, setBitti] = useState(false);
  const bolumRef = useRef(0);
  const kapandiRef = useRef(false);

  const pid = typeof window !== 'undefined' ? activeProfile.get() : null;

  const yukle = useCallback(async () => {
    if (!pid) { router.replace('/'); return; }
    try {
      setDurum(await api.breakStatus(pid));
    } catch (e: any) {
      setErr(e.message);
    }
  }, [pid, router]);

  useEffect(() => { yukle(); }, [yukle]);

  // Acik mola varsa dogrudan oyuna don.
  // Tablet ekran koruyucuya duserse veya sekme arka plana alinirsa
  // oturum acik kalir; cocuk geri geldiginde molasi kaldigi yerden
  // surmelidir. Onceki surumde "Bugunluk mola bitti" yaziyordu.
  useEffect(() => {
    if (!durum?.active || oturumId || bitti) return;
    if ((durum.remaining_seconds || 0) <= 0) return;
    setOturumId(durum.active.id);
    setKalan(durum.remaining_seconds || 0);
    kapandiRef.current = false;
  }, [durum, oturumId, bitti]);

  // Molayi bitir. Birden fazla kez cagrilabilir; ilk cagri gecerli.
  const bitirGercek = useCallback(async (yonlendir: boolean) => {
    if (kapandiRef.current || !oturumId || !pid) return;
    kapandiRef.current = true;
    try {
      await api.breakEnd(pid, oturumId, bolumRef.current);
    } catch { /* sessizce gec: sure sunucuda zaten sinirli */ }
    if (yonlendir) router.push('/');
    else setBitti(true);
  }, [oturumId, pid, router]);

  // Geri sayim
  useEffect(() => {
    if (!oturumId || kalan <= 0) return;
    const iv = setInterval(() => {
      setKalan((k) => {
        if (k <= 1) {
          clearInterval(iv);
          bitirGercek(false);
          return 0;
        }
        return k - 1;
      });
    }, 1000);
    return () => clearInterval(iv);
  }, [oturumId, kalan, bitirGercek]);

  // NOT: Sayfa gizlenince molayi BITIRMIYORUZ.
  // Ekran koruyucu, sekme degistirme veya telefon kilidi de "pagehide"
  // tetikler. Molayi kapatirsak cocuk geri geldiginde molasi bitmis olur.
  //
  // Bunun yerine oturum acik birakilir; sunucu tarafinda:
  //   - suresi dolan oturum otomatik kapatilir
  //   - sure her zaman mola hakkiyla sinirlidir (sure sismez)
  //   - cocuk geri gelirse kaldigi yerden devam eder

  const basla = async () => {
    if (!pid) return;
    try {
      const r = await api.breakStart(pid, 'tek_cizgi');
      setOturumId(r.id);
      setKalan(r.seconds);
      kapandiRef.current = false;
    } catch (e: any) {
      setErr(e.message);
    }
  };

  if (err) return (
    <main className="mx-auto max-w-lg px-4 py-12">
      <ErrorBox message={err} onRetry={yukle} />
    </main>
  );
  if (!durum) return <Spinner label="Yükleniyor…" />;

  if (!durum.enabled) return <KapaliEkran />;
  if (bitti) return <BittiEkrani used={durum.used_today || 0} />;
  if (oturumId) return (
    <OyunEkrani kalan={kalan} onBolum={(n) => { bolumRef.current = n; }}
                onCik={() => bitirGercek(true)} />
  );
  return <HazirEkrani d={durum} onBasla={basla} />;
}

/* ------------------------------------------------------------------ */

function dakikaMetni(sn: number) {
  const d = Math.floor(sn / 60), s = sn % 60;
  return `${d}:${String(s).padStart(2, '0')}`;
}

function KapaliEkran() {
  return (
    <main className="mx-auto max-w-sm px-4 py-16 text-center">
      <Zeki mood="calm" size={88} />
      <h1 className="mt-4 text-2xl font-black text-slate-800">Mola kapalı</h1>
      <p className="mt-2 font-bold text-slate-500">
        Mola bölümünü annen veya baban açabilir.
      </p>
      <Link href="/" className="btn-primary mt-6 w-full">Ana ekran</Link>
    </main>
  );
}

function HazirEkrani({ d, onBasla }: { d: Durum; onBasla: () => void }) {
  const hazir = d.can_start;
  const serbest = d.mode === 'free';
  const calisma = Math.round((d.study_seconds || 0) / 60);
  const gerekli = Math.round((d.study_required || 1800) / 60);
  const yuzde = Math.min(100, ((d.study_seconds || 0) % (d.study_required || 1800))
    / (d.study_required || 1800) * 100);

  return (
    <main className="mx-auto max-w-lg px-4 py-8">
      <div className="mb-4 flex items-center gap-3">
        <Link href="/" className="text-2xl font-black text-slate-300
                                   hover:text-slate-500">←</Link>
        <h1 className="text-2xl font-black text-slate-800">Mola</h1>
      </div>

      <div className="mb-5 text-center">
        <Zeki mood={hazir ? 'cheer' : 'thinking'} size={100} />
      </div>

      {hazir ? (
        <div className="card p-6 text-center">
          <p className="text-lg font-black text-mint-600">
            {serbest ? 'Mola yapabilirsin' : 'Mola zamanı!'}
          </p>
          <p className="mt-1 font-bold text-slate-500">
            {Math.round((d.remaining_seconds || 0) / 60)} dakika oyun oynayabilirsin
          </p>
          {serbest && (d.daily_limit || 0) > 0 && (
            <p className="mt-1 text-xs font-bold text-slate-400">
              Bugün {Math.round((d.daily_left || 0) / 60)} dakika hakkın kaldı
            </p>
          )}

          <div className="mt-5 rounded-2xl bg-slate-50 p-4 text-left">
            <div className="flex items-center gap-3">
              <span className="text-3xl">✏️</span>
              <div>
                <p className="font-black text-slate-800">Tek Çizgi</p>
                <p className="text-xs font-bold text-slate-500">
                  Sayıları sırayla birleştir, her kareden bir kez geç
                </p>
              </div>
            </div>
          </div>

          <button onClick={onBasla} className="btn-primary mt-5 w-full text-lg">
            Molaya başla
          </button>
        </div>
      ) : serbest ? (
        // Serbest modda mola hakki yoksa tek sebep gunluk tavan dolmus olmasi.
        // Sinirsiz ayarda bu ekran hic gorunmemelidir.
        <div className="card p-6 text-center">
          <p className="text-lg font-black text-slate-700">
            {(d.daily_limit || 0) > 0
              ? 'Bugünlük mola bitti'
              : 'Şu an mola yapılamıyor'}
          </p>
          <p className="mt-1 font-bold text-slate-500">
            {(d.daily_limit || 0) > 0
              ? `Bugün ${Math.round((d.used_today || 0) / 60)} dakika mola yaptın.
                 Yarın yeniden başlıyor.`
              : 'Biraz sonra tekrar dene.'}
          </p>
          <Link href="/gorev" className="btn-primary mt-5 w-full text-lg">
            Günlük göreve git
          </Link>
        </div>
      ) : (
        <div className="card p-6 text-center">
          <p className="text-lg font-black text-slate-700">Biraz daha çalış</p>
          <p className="mt-1 font-bold text-slate-500">
            {gerekli} dakika çalışınca mola hakkın olur
          </p>

          <div className="mt-5">
            <div className="h-3 overflow-hidden rounded-full bg-slate-100">
              <div className="h-full rounded-full bg-brand-500 transition-all"
                   style={{ width: `${yuzde}%` }} />
            </div>
            <p className="mt-2 text-sm font-extrabold text-slate-400">
              Bugün {calisma} dakika çalıştın
            </p>
          </div>

          <Link href="/gorev" className="btn-primary mt-5 w-full text-lg">
            Günlük göreve git
          </Link>
        </div>
      )}

      {(d.used_today || 0) > 0 && (
        <p className="mt-4 text-center text-xs font-bold text-slate-400">
          Bugün {Math.round((d.used_today || 0) / 60)} dakika mola yaptın
        </p>
      )}
    </main>
  );
}

function OyunEkrani({ kalan, onBolum, onCik }: {
  kalan: number; onBolum: (n: number) => void; onCik: () => void;
}) {
  const azKaldi = kalan <= 60;

  return (
    <main className="mx-auto max-w-lg px-4 py-5">
      <div className="mb-4 flex items-center gap-3">
        <button onClick={onCik} aria-label="Derse dön"
                className="rounded-lg px-2 py-1 text-lg leading-none text-slate-300
                           transition hover:bg-slate-100 hover:text-slate-500">
          ←
        </button>
        <h1 className="text-lg font-black text-slate-800">Tek Çizgi</h1>

        {/* Sayac: bilgi verir ama baski yapmaz.
            Kirmizi/titresimli degil; son dakikada sadece rengi degisir. */}
        <span className={`ml-auto rounded-full px-3 py-1 text-sm font-black
                          tabular-nums ${azKaldi
                            ? 'bg-sun-400/20 text-sun-600'
                            : 'bg-slate-100 text-slate-500'}`}>
          {dakikaMetni(kalan)}
        </span>
      </div>

      {azKaldi && (
        <p className="mb-3 rounded-xl bg-sun-400/10 px-4 py-2 text-center
                      text-sm font-bold text-sun-600">
          Molanın bitmesine az kaldı
        </p>
      )}

      <TekCizgi onLevel={onBolum} />

      <button onClick={onCik} className="btn-ghost mt-5 w-full">
        Derse dön
      </button>
    </main>
  );
}

function BittiEkrani({ used }: { used: number }) {
  return (
    <main className="mx-auto max-w-sm px-4 py-16 text-center">
      <Zeki mood="happy" size={96} />
      <h1 className="mt-4 text-2xl font-black text-slate-800">Mola bitti</h1>
      <p className="mt-2 font-bold text-slate-500">
        Dinlendin, şimdi kaldığın yerden devam edebilirsin.
      </p>
      <div className="mt-6 grid gap-3">
        <Link href="/gorev" className="btn-primary w-full text-lg">
          Günlük göreve dön
        </Link>
        <Link href="/" className="btn-ghost w-full">Ana ekran</Link>
      </div>
    </main>
  );
}
