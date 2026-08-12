'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api, pinToken, token, Profile, AVATARS } from '@/lib/api';
import { Spinner, ErrorBox, ProgressBar } from '@/components/Zeki';

export default function EbeveynPage() {
  const router = useRouter();
  const [authed, setAuthed] = useState(false);
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [sel, setSel] = useState<string>('');

  // pinToken.get() suresi dolmus token'i dondurmez ve temizler.
  // Boylece "token var ama gecersiz" durumu olusmaz.
  useEffect(() => {
    if (!token.get()) { router.replace('/giris'); return; }
    if (pinToken.get()) setAuthed(true);
    api.profiles().then((ps) => {
      setProfiles(ps);
      if (ps.length) setSel(ps[0].id);
    }).catch(() => {});
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Sekme arka planda uzun sure kalirsa token suresi dolabilir.
  // Kullanici geri dondugunde kontrol et.
  useEffect(() => {
    const kontrol = () => {
      if (authed && !pinToken.get()) setAuthed(false);
    };
    document.addEventListener('visibilitychange', kontrol);
    const iv = setInterval(kontrol, 60_000);
    return () => {
      document.removeEventListener('visibilitychange', kontrol);
      clearInterval(iv);
    };
  }, [authed]);

  const pinBitti = () => {
    pinToken.clear();
    setAuthed(false);
  };

  if (!authed) return <PinGate onOk={() => setAuthed(true)} />;
  if (!profiles.length) return (
    <main className="mx-auto max-w-md px-4 py-12 text-center">
      <p className="font-bold text-slate-500">Henüz çocuk profili yok.</p>
      <Link href="/profil/yeni" className="btn-primary mt-4">Çocuk ekle</Link>
    </main>
  );

  return (
    <main className="mx-auto max-w-2xl px-4 py-6">
      <div className="mb-5 flex items-center gap-3">
        <Link href="/" className="text-2xl font-black text-slate-300
                                  hover:text-slate-500">←</Link>
        <h1 className="text-3xl font-black text-slate-800">Ebeveyn paneli</h1>
      </div>

      {/* Kimin raporuna bakildigi HER ZAMAN gorunur olmali.
          Tek cocuk varsa secici degil, kimlik karti gosterilir. */}
      {profiles.length > 1 ? (
        <div className="mb-5 flex gap-2 overflow-x-auto pb-1">
          {profiles.map((p) => (
            <button key={p.id} onClick={() => setSel(p.id)}
                    className={`flex shrink-0 items-center gap-2 rounded-2xl border-2
                                px-4 py-2 font-extrabold transition ${
                      sel === p.id ? 'border-brand-500 bg-brand-50 text-brand-600'
                                   : 'border-slate-200 bg-white text-slate-500'}`}>
              <span className="text-xl">{AVATARS[p.avatar_id]}</span>
              <span>{p.name}</span>
              <span className={`text-xs font-bold ${
                sel === p.id ? 'text-brand-400' : 'text-slate-400'}`}>
                {p.grade}. sınıf
              </span>
            </button>
          ))}
        </div>
      ) : (
        <div className="card mb-5 flex items-center gap-3 px-4 py-3">
          <span className="text-3xl">{AVATARS[profiles[0].avatar_id]}</span>
          <div>
            <p className="text-lg font-black text-slate-800">{profiles[0].name}</p>
            <p className="text-xs font-bold text-slate-400">
              {profiles[0].grade}. sınıf
            </p>
          </div>
        </div>
      )}

      {sel && <Dashboard profileId={sel} onPinBitti={pinBitti} />}
    </main>
  );
}

/* ------------------------------------------------------------------ */

function PinGate({ onOk }: { onOk: () => void }) {
  const [pin, setPin] = useState('');
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async (value: string) => {
    setBusy(true); setErr('');
    try {
      const r = await api.verifyPin(value);
      pinToken.set(r.pin_token);
      onOk();
    } catch (e: any) {
      // Sunucudan gelen teknik mesajlar yerine anlasilir metin goster.
      // "Gecersiz PIN oturumu" gibi ifadeler kullaniciya bir sey anlatmaz.
      const kod = e.status;
      if (kod === 401 || kod === 403) {
        setErr('PIN yanlış. Tekrar deneyin.');
      } else if (kod === 429) {
        setErr(e.message || 'Çok fazla deneme yapıldı. Biraz bekleyin.');
      } else if (!kod) {
        setErr('Bağlantı kurulamadı. İnternetinizi kontrol edin.');
      } else {
        setErr(e.message || 'Bir sorun oluştu, tekrar deneyin.');
      }
      setPin('');
    } finally {
      setBusy(false);
    }
  };

  const press = (d: string) => {
    if (busy || pin.length >= 4) return;
    const next = pin + d;
    setPin(next);
    if (next.length === 4) submit(next);
  };

  return (
    <main className="mx-auto flex min-h-screen max-w-xs flex-col items-center
                     justify-center px-4">
      <span className="text-5xl">🔒</span>
      <h1 className="mt-3 text-2xl font-black text-slate-800">Ebeveyn PIN'i</h1>
      <p className="mt-1 text-center text-sm font-bold text-slate-400">
        Gelişim raporu ve ayarlar burada
      </p>

      <div className="my-7 flex gap-3">
        {[0, 1, 2, 3].map((i) => (
          <div key={i} className={`h-4 w-4 rounded-full transition ${
            i < pin.length ? 'bg-brand-500 scale-110' : 'bg-slate-200'}`} />
        ))}
      </div>

      {err && <p className="mb-4 text-center text-sm font-extrabold text-coral-500">
        {err}
      </p>}

      <div className="grid w-full grid-cols-3 gap-3">
        {['1','2','3','4','5','6','7','8','9'].map((d) => (
          <button key={d} onClick={() => press(d)} disabled={busy}
                  className="btn-ghost aspect-square text-2xl">{d}</button>
        ))}
        <div />
        <button onClick={() => press('0')} disabled={busy}
                className="btn-ghost aspect-square text-2xl">0</button>
        <button onClick={() => setPin((p) => p.slice(0, -1))}
                className="btn-ghost aspect-square text-xl">⌫</button>
      </div>

      <Link href="/" className="mt-6 text-sm font-extrabold text-slate-400">
        ← Geri
      </Link>
    </main>
  );
}

/* ------------------------------------------------------------------ */

const GRADE_LABEL: Record<number, string> = {
  0: 'Okul öncesi', 1: '1. sınıf', 2: '2. sınıf', 3: '3. sınıf',
  4: '4. sınıf', 5: '5. sınıf',
};

function Dashboard({ profileId, onPinBitti }:
                   { profileId: string; onPinBitti: () => void }) {
  const [d, setD] = useState<any>(null);
  const [err, setErr] = useState('');
  const [tab, setTab] = useState<'rapor' | 'ayar'>('rapor');

  const load = async () => {
    setErr('');
    try { setD(await api.dashboard(profileId)); }
    catch (e: any) {
      // PIN oturumu bitti: hata gostermek yerine sessizce PIN ekranina don.
      // Ebeveyn "Gecersiz PIN oturumu" gibi teknik bir mesaj gormemeli.
      if (e.status === 401) { onPinBitti(); return; }
      setErr(e.message);
    }
  };

  useEffect(() => { setD(null); load(); }, [profileId]); // eslint-disable-line

  if (err) return <ErrorBox message={err} onRetry={load} />;
  if (!d) return <Spinner />;

  return (
    <>
      {/* Kimlik: sayfa kaydirilinca ustteki secici gozden kaybolur,
          rapor basliginda kimin verisi oldugu tekrar belirtilir. */}
      <div className="mb-3 flex items-baseline gap-2">
        <h2 className="text-xl font-black text-slate-800">{d.profile.name}</h2>
        <span className="text-sm font-bold text-slate-400">
          {d.profile.grade}. sınıf
        </span>
      </div>

      <div className="mb-5 grid grid-cols-2 gap-2 rounded-2xl bg-slate-100 p-1">
        {(['rapor', 'ayar'] as const).map((t) => (
          <button key={t} onClick={() => setTab(t)}
                  className={`rounded-xl py-2.5 font-extrabold transition ${
                    tab === t ? 'bg-white text-brand-600 shadow-sm'
                              : 'text-slate-400'}`}>
            {t === 'rapor' ? 'Gelişim raporu' : 'Ayarlar'}
          </button>
        ))}
      </div>

      {tab === 'rapor' ? <Rapor d={d} /> : <Ayarlar d={d} pid={profileId} reload={load} />}
    </>
  );
}

function Rapor({ d }: { d: any }) {
  return (
    <div className="grid gap-4">
      {/* Okuma ve anlama — ses tanima YOK, sure olcumu ile hesaplanir */}
      {d.reading?.has_data && <OkumaBolumu r={d.reading} />}

      {/* Mola: gunluk calisma/mola dengesi */}
      {d.break && <MolaBolumu m={d.break} />}
      {/* Bugun */}
      <section className="card p-5">
        <h2 className="mb-3 font-black text-slate-700">Bugün</h2>
        <div className="grid grid-cols-3 gap-3 text-center">
          <Box v={`${d.today.minutes}`} l="dakika" />
          <Box v={d.today.questions} l="soru" />
          <Box v={d.today.quest_done ? '✓' : '—'} l="günlük görev" />
        </div>
        <p className="mt-3 text-center text-xs font-bold text-slate-400">
          Günlük süre limiti: {d.today.limit_minutes} dk
        </p>
      </section>

      {/* Ozet */}
      <section className="card p-5">
        <h2 className="mb-3 font-black text-slate-700">Son 8 hafta</h2>
        <div className="grid grid-cols-4 gap-2 text-center">
          <Box v={d.summary.days_played} l="gün" />
          <Box v={d.summary.total_questions} l="soru" />
          <Box v={`%${d.summary.accuracy}`} l="doğruluk" />
          <Box v={`🔥${d.summary.streak}`} l="seri" />
        </div>
        {d.summary.accuracy >= 75 && d.summary.accuracy <= 85 && (
          <p className="mt-3 rounded-xl bg-mint-400/10 px-3 py-2 text-center text-xs
                        font-extrabold text-mint-600">
            Doğruluk hedef bantta (%75–85). Zorluk seviyesi doğru ayarlanmış.
          </p>
        )}
      </section>

      {/* Zayif alan */}
      {d.weak?.length > 0 && (
        <section className="card border-sun-400/40 bg-sun-400/5 p-5">
          <h2 className="mb-3 font-black text-slate-700">⚠️ Dikkat gerektiren</h2>
          {d.weak.map((w: any) => (
            <div key={w.id} className="mb-2 last:mb-0">
              <p className="font-extrabold text-slate-700">
                {w.icon} {w.name} — %{w.accuracy}
              </p>
              <p className="text-xs font-bold text-slate-500">
                Tekrar soruları otomatik artırıldı. Odak moduyla bu haftaya
                alabilirsiniz.
              </p>
            </div>
          ))}
        </section>
      )}

      {/* Kategoriler */}
      <section className="card p-5">
        <h2 className="mb-3 font-black text-slate-700">Kategoriler</h2>
        <div className="grid gap-3">
          {d.categories.map((c: any) => (
            <div key={c.id}>
              <div className="mb-1 flex items-center justify-between text-sm">
                <span className="font-extrabold text-slate-700">
                  {c.icon} {c.name} {c.medal_icon}
                  {c.advanced && (
                    <span className="ml-1.5 rounded-full bg-brand-100 px-1.5 py-0.5
                                     text-[10px] font-black text-brand-600">
                      ⬆️ üst sınıf
                    </span>
                  )}
                </span>
                <span className={`font-black ${
                  c.accuracy >= 75 ? 'text-mint-600'
                  : c.accuracy >= 60 ? 'text-slate-500' : 'text-coral-500'}`}>
                  %{c.accuracy}
                </span>
              </div>
              <ProgressBar value={c.accuracy} className="h-2" />
            </div>
          ))}
          {!d.categories.length && (
            <p className="text-center text-sm font-bold text-slate-400">
              Henüz veri yok. Birkaç tur sonra burada görünecek.
            </p>
          )}
        </div>
      </section>

      {/* Sinif dagilimi */}
      {d.grade_distribution?.length > 0 && (
        <section className="card p-5">
          <h2 className="mb-1 font-black text-slate-700">Bu hafta gelen sorular</h2>
          <p className="mb-3 text-xs font-bold text-slate-400">
            Bu dağılım çocuğunuzun performansına göre otomatik ayarlanır.
          </p>
          <div className="grid gap-2">
            {d.grade_distribution.map((g: any) => (
              <div key={g.grade} className="flex items-center gap-2">
                <span className="w-24 shrink-0 text-sm font-extrabold text-slate-500">
                  {GRADE_LABEL[g.grade] || `${g.grade}. sınıf`}
                </span>
                <ProgressBar value={g.percent} className="h-2.5 flex-1" />
                <span className="w-10 shrink-0 text-right text-xs font-black
                                 text-slate-400">%{g.percent}</span>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Ders dagilimi */}
      {d.subject_distribution?.length > 0 && (
        <section className="card p-5">
          <h2 className="mb-3 font-black text-slate-700">Ders dağılımı</h2>
          <div className="grid gap-2">
            {d.subject_distribution.map((s: any) => (
              <div key={s.subject} className="flex items-center gap-2">
                <span className="w-24 shrink-0 text-sm font-extrabold text-slate-500">
                  {s.name}
                </span>
                <ProgressBar value={s.percent} className="h-2.5 flex-1" />
                <span className="w-10 shrink-0 text-right text-xs font-black
                                 text-slate-400">%{s.percent}</span>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Rozetler */}
      {d.badges?.length > 0 && (
        <section className="card p-5">
          <h2 className="mb-3 font-black text-slate-700">
            Rozetler ({d.badges.length})
          </h2>
          <div className="flex flex-wrap gap-2">
            {d.badges.map((b: any) => (
              <span key={b.id} className="rounded-full bg-slate-50 px-3 py-1.5
                                          text-sm font-extrabold text-slate-600">
                {b.icon} {b.name}
              </span>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

function MolaBolumu({ m }: { m: any }) {
  const enBuyuk = Math.max(
    1, ...m.history.map((h: any) => Math.max(h.study_min, h.break_min)));

  return (
    <section className="card p-5">
      <div className="mb-1 flex items-baseline justify-between">
        <h2 className="font-black text-slate-700">⏱️ Çalışma ve Mola</h2>
        <span className="text-xs font-bold text-slate-400">
          {m.enabled ? `${m.study_minutes} dk → ${m.break_minutes} dk` : 'kapalı'}
        </span>
      </div>
      <p className="mb-4 text-xs font-bold text-slate-400">
        Çalışma süresi, soru cevaplama aralıklarından hesaplanır.
      </p>

      <div className="mb-4 grid grid-cols-2 gap-3">
        <div className="rounded-2xl bg-slate-50 p-4 text-center">
          <p className="text-2xl font-black text-slate-800">
            {m.today.study_min}
            <span className="ml-1 text-xs font-bold text-slate-400">dk</span>
          </p>
          <p className="text-xs font-black text-brand-600">bugün çalışma</p>
        </div>
        <div className="rounded-2xl bg-slate-50 p-4 text-center">
          <p className="text-2xl font-black text-slate-800">
            {m.today.break_min}
            <span className="ml-1 text-xs font-bold text-slate-400">dk</span>
          </p>
          <p className="text-xs font-black text-sun-600">bugün mola</p>
        </div>
      </div>

      {/* 7 gunluk cubuk: calisma ustte, mola altta */}
      <p className="mb-2 text-xs font-black uppercase tracking-wide text-slate-400">
        Son 7 gün
      </p>
      <div className="flex h-24 items-end gap-1.5 rounded-xl bg-slate-50 p-2">
        {m.history.map((h: any, i: number) => (
          <div key={i} className="group relative flex flex-1 flex-col
                                  items-center justify-end gap-0.5">
            <div className="pointer-events-none absolute bottom-full mb-1 hidden
                            whitespace-nowrap rounded bg-slate-800 px-2 py-1
                            text-[10px] font-bold text-white group-hover:block">
              {h.study_min} dk çalışma · {h.break_min} dk mola
            </div>
            {h.break_min > 0 && (
              <div className="w-full rounded-t bg-sun-400"
                   style={{ height: `${(h.break_min / enBuyuk) * 70}%` }} />
            )}
            <div className={`w-full bg-brand-500 ${h.break_min > 0 ? '' : 'rounded-t'}`}
                 style={{ height: `${Math.max((h.study_min / enBuyuk) * 70, 2)}%` }} />
          </div>
        ))}
      </div>
      <div className="mt-2 flex gap-4 text-[11px] font-bold text-slate-400">
        <span className="flex items-center gap-1">
          <i className="h-2 w-2 rounded-sm bg-brand-500" /> çalışma
        </span>
        <span className="flex items-center gap-1">
          <i className="h-2 w-2 rounded-sm bg-sun-400" /> mola
        </span>
      </div>
    </section>
  );
}

const HIZ_DURUM: Record<string, { ad: string; renk: string }> = {
  gelisiyor: { ad: 'Gelişiyor', renk: 'text-sun-500' },
  beklenen: { ad: 'Beklenen aralıkta', renk: 'text-mint-600' },
  hizli: { ad: 'Sınıfın üzerinde', renk: 'text-brand-600' },
  veri_yok: { ad: 'Veri yok', renk: 'text-slate-400' },
};

function OkumaBolumu({ r }: { r: any }) {
  const durum = HIZ_DURUM[r.wpm_status] || HIZ_DURUM.veri_yok;
  const maxWpm = Math.max(r.wpm_norm.max, ...r.speed_history.map((x: any) => x.wpm), 1);

  return (
    <section className="card p-5">
      <div className="mb-1 flex items-baseline justify-between">
        <h2 className="font-black text-slate-700">📖 Okuma ve Anlama</h2>
        <span className="text-xs font-bold text-slate-400">
          {r.stories_read} hikâye · {r.total} tur
        </span>
      </div>
      <p className="mb-4 text-xs font-bold text-slate-400">
        Okuma hızı süre ölçümüyle hesaplanır — mikrofon veya ses kaydı kullanılmaz.
      </p>

      <div className="mb-4 grid grid-cols-2 gap-3">
        <div className="rounded-2xl bg-slate-50 p-4 text-center">
          <p className="text-2xl font-black text-slate-800">
            {r.avg_wpm ?? '—'}
            <span className="ml-1 text-xs font-bold text-slate-400">kelime/dk</span>
          </p>
          <p className={`text-xs font-black ${durum.renk}`}>{durum.ad}</p>
          <p className="mt-0.5 text-[11px] font-bold text-slate-400">
            {r.wpm_norm.min}–{r.wpm_norm.max} beklenir
          </p>
        </div>
        <div className="rounded-2xl bg-slate-50 p-4 text-center">
          <p className="text-2xl font-black text-slate-800">%{r.avg_accuracy}</p>
          <p className="text-xs font-black text-slate-500">anlama</p>
          <p className="mt-0.5 text-[11px] font-bold text-slate-400">
            ortalama doğruluk
          </p>
        </div>
      </div>

      {/* Hiz grafigi — norm bandi gri seritle gosterilir */}
      {r.speed_history.length >= 2 && (
        <div className="mb-4">
          <p className="mb-2 text-xs font-black uppercase tracking-wide text-slate-400">
            Okuma hızı gelişimi
          </p>
          <div className="relative flex h-28 items-end gap-1.5 rounded-xl
                          bg-slate-50 p-2">
            {/* Beklenen aralik bandi */}
            <div className="pointer-events-none absolute inset-x-2 rounded
                            bg-mint-400/15"
                 style={{
                   bottom: `${(r.wpm_norm.min / maxWpm) * 100 * 0.86 + 8}%`,
                   height: `${((r.wpm_norm.max - r.wpm_norm.min) / maxWpm) * 100 * 0.86}%`,
                 }} />
            {r.speed_history.map((h: any, i: number) => (
              <div key={i} className="group relative flex flex-1 flex-col
                                      items-center justify-end">
                <div className="pointer-events-none absolute bottom-full mb-1 hidden
                                whitespace-nowrap rounded bg-slate-800 px-2 py-1
                                text-[10px] font-bold text-white group-hover:block">
                  {h.wpm} kelime/dk
                </div>
                <div className={`w-full rounded-t ${
                  h.wpm < r.wpm_norm.min ? 'bg-sun-400'
                  : h.wpm <= r.wpm_norm.max ? 'bg-mint-500' : 'bg-brand-500'}`}
                     style={{ height: `${Math.max((h.wpm / maxWpm) * 100 * 0.86, 4)}%` }} />
              </div>
            ))}
          </div>
          <p className="mt-1.5 text-[11px] font-bold text-slate-400">
            Yeşil bant: {r.wpm_norm.min}–{r.wpm_norm.max} kelime/dk arası beklenen aralık
          </p>
        </div>
      )}

      {/* Soru turune gore */}
      {r.types?.length > 0 && (
        <div className="mb-4">
          <p className="mb-2 text-xs font-black uppercase tracking-wide text-slate-400">
            Soru türüne göre
          </p>
          <div className="grid gap-2">
            {r.types.map((t: any) => (
              <div key={t.kod} className="flex items-center gap-2">
                <span className="w-32 shrink-0 text-sm font-extrabold text-slate-600">
                  {t.ad}
                </span>
                <ProgressBar value={t.accuracy ?? 0} className="h-2.5 flex-1" />
                <span className={`w-10 shrink-0 text-right text-xs font-black ${
                  (t.accuracy ?? 0) >= 75 ? 'text-mint-600'
                  : (t.accuracy ?? 0) >= 55 ? 'text-slate-500' : 'text-coral-500'}`}>
                  %{t.accuracy}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {r.advice && (
        <div className="rounded-2xl bg-brand-50 px-4 py-3">
          <p className="text-sm font-bold leading-relaxed text-brand-700">
            {r.advice}
          </p>
        </div>
      )}

      {r.suspicious_count > 0 && (
        <p className="mt-3 rounded-xl bg-sun-400/10 px-3 py-2 text-xs
                      font-bold text-sun-600">
          {r.suspicious_count} turda metin okunmadan geçilmiş görünüyor.
        </p>
      )}

      <p className="mt-3 text-[11px] font-bold text-slate-400">
        Son okuma: {r.last.title} · %{r.last.accuracy}
        {r.last.wpm ? ` · ${r.last.wpm} kelime/dk` : ' · içinden okudu'}
      </p>
    </section>
  );
}

function Box({ v, l }: { v: any; l: string }) {
  return (
    <div className="rounded-2xl bg-slate-50 py-3">
      <p className="text-xl font-black text-slate-800">{v}</p>
      <p className="text-[11px] font-bold text-slate-400">{l}</p>
    </div>
  );
}

/* ------------------------------------------------------------------ */

const WEIGHTS = [
  { v: 0.5, l: 'Az' }, { v: 1.0, l: 'Normal' }, { v: 1.5, l: 'Çok' },
];
const REPEATS = [
  { v: 0.10, l: 'Az' }, { v: 0.20, l: 'Orta' }, { v: 0.35, l: 'Çok' },
];
const LIMITS = [15, 30, 45, 180];

function Ayarlar({ d, pid, reload }: { d: any; pid: string; reload: () => void }) {
  const s = d.settings;
  const [weights, setWeights] = useState<Record<string, number>>(
    s.subject_weights || {});
  const [preview, setPreview] = useState<any[]>(d.subject_distribution || []);
  const [msg, setMsg] = useState('');

  const save = async (body: any) => {
    setMsg('');
    try {
      const r = await api.updateSettings(pid, body);
      if (r.preview) setPreview(r.preview);
      setMsg('Kaydedildi ✓');
      setTimeout(() => setMsg(''), 2000);
      reload();
    } catch (e: any) { setMsg(e.message); }
  };

  const setWeight = (subject: string, v: number) => {
    const next = { ...weights, [subject]: v };
    setWeights(next);
    save({ subject_weights: next });
  };

  const setFocus = async (catId: string | null) => {
    try {
      await api.setFocus(pid, catId, 1);
      setMsg(catId ? 'Odak ayarlandı ✓' : 'Odak kaldırıldı');
      setTimeout(() => setMsg(''), 2000);
      reload();
    } catch (e: any) { setMsg(e.message); }
  };

  const subjects = Array.from(
    new Set(d.categories.map((c: any) => c.subject))
  ) as string[];
  const subjName = (s: string) =>
    d.categories.find((c: any) => c.subject === s)?.subject_name || s;

  return (
    <div className="grid gap-4">
      {/* Ayarlar yikici olabilir (sinif degistirme gibi) —
          kimin ayarlarinin degistigi acikca yazilir. */}
      <p className="rounded-xl bg-slate-100 px-4 py-2.5 text-center text-sm
                    font-bold text-slate-500">
        <b className="text-slate-700">{d.profile.name}</b> için ayarlar
      </p>

      {msg && (
        <p className="rounded-2xl bg-brand-50 px-4 py-2.5 text-center
                      font-extrabold text-brand-600">{msg}</p>
      )}

      {/* Ders agirligi */}
      <section className="card p-5">
        <h2 className="font-black text-slate-700">Ders ağırlığı</h2>
        <p className="mb-4 text-xs font-bold leading-relaxed text-slate-400">
          Çocuğunuzun karnesini ve öğretmen geri bildirimini siz bilirsiniz —
          sistem bilemez. Hangi derse ağırlık verileceğini buradan seçin.
          Zorluk seviyesi otomatik ayarlanır, ona dokunmanız gerekmez.
        </p>

        <div className="grid gap-3">
          {subjects.map((sub) => (
            <div key={sub}>
              <div className="mb-1.5 flex items-center justify-between">
                <span className="font-extrabold text-slate-600">{subjName(sub)}</span>
                <span className="text-xs font-black text-slate-400">
                  %{preview.find((p: any) => p.subject === sub)?.percent ?? '—'}
                </span>
              </div>
              <div className="grid grid-cols-3 gap-1.5">
                {WEIGHTS.map((w) => (
                  <button key={w.v} onClick={() => setWeight(sub, w.v)}
                          className={`rounded-xl py-2 text-sm font-extrabold transition ${
                            (weights[sub] ?? 1.0) === w.v
                              ? 'bg-brand-500 text-white'
                              : 'bg-slate-100 text-slate-500'}`}>
                    {w.l}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>

        <p className="mt-3 text-xs font-bold text-slate-400">
          Hiçbir ders %10'un altına inmez, hiçbiri %45'i geçmez —
          müfredat bütünlüğü ve çeşitlilik korunur.
        </p>
      </section>

      {/* Odak modu */}
      <section className="card p-5">
        <h2 className="font-black text-slate-700">🎯 Bu haftanın odağı</h2>
        <p className="mb-3 text-xs font-bold text-slate-400">
          Seçilen kategoriden günlük görevde 2 yerine 6 soru gelir.
          Toplam soru sayısı ve süre değişmez. 1 hafta sonra otomatik biter.
        </p>
        <select value={s.focus_category_id || ''}
                onChange={(e) => setFocus(e.target.value || null)}
                className="input">
          <option value="">Odak yok</option>
          {d.categories.map((c: any) => (
            <option key={c.id} value={c.id}>{c.icon} {c.name}</option>
          ))}
        </select>
        {s.focus_until && (
          <p className="mt-2 text-xs font-extrabold text-brand-600">
            Bitiş: {s.focus_until}
          </p>
        )}
      </section>

      {/* Sinif + tekrar + terfi */}
      <section className="card grid gap-5 p-5">
        <div>
          <h2 className="mb-2 font-black text-slate-700">Sınıf seviyesi</h2>
          <div className="grid grid-cols-4 gap-2">
            {[1, 2, 3, 4].map((g) => (
              <button key={g} onClick={() => save({ grade: g })}
                      className={`rounded-xl py-3 text-lg font-black transition ${
                        d.profile.grade === g ? 'bg-brand-500 text-white'
                                              : 'bg-slate-100 text-slate-500'}`}>
                {g}
              </button>
            ))}
          </div>
        </div>

        <div>
          <h2 className="mb-1 font-black text-slate-700">Tekrar oranı</h2>
          <p className="mb-2 text-xs font-bold text-slate-400">
            Bir alt sınıf sorularının sıklığı. Çocuğunuz bir konuda zorlanırsa
            sistem bu oranı o kategoride kendiliğinden artırır.
          </p>
          <div className="grid grid-cols-3 gap-2">
            {REPEATS.map((r) => (
              <button key={r.v} onClick={() => save({ repeat_ratio: r.v })}
                      className={`rounded-xl py-2.5 font-extrabold transition ${
                        Math.abs((s.repeat_ratio ?? 0.2) - r.v) < 0.01
                          ? 'bg-brand-500 text-white' : 'bg-slate-100 text-slate-500'}`}>
                {r.l}
              </button>
            ))}
          </div>
        </div>

        <div>
          <h2 className="mb-1 font-black text-slate-700">İleri seviye soruları</h2>
          <p className="mb-2 text-xs font-bold text-slate-400">
            Çocuğunuz bir kategoride ustalaştığında üst sınıf soruları otomatik
            açılır. Zorlanırsa sistem oranı kendiliğinden düşürür.
          </p>
          <button onClick={() => save({ allow_advance: !s.allow_advance })}
                  className={`w-full rounded-xl py-2.5 font-extrabold transition ${
                    s.allow_advance ? 'bg-mint-500 text-white'
                                    : 'bg-slate-100 text-slate-500'}`}>
            {s.allow_advance ? 'Açık ✓' : 'Kapalı'}
          </button>
        </div>

        <div>
          <h2 className="mb-2 font-black text-slate-700">Günlük süre limiti</h2>
          <div className="grid grid-cols-4 gap-2">
            {LIMITS.map((m) => (
              <button key={m} onClick={() => save({ daily_limit_min: m })}
                      className={`rounded-xl py-2.5 text-sm font-extrabold transition ${
                        s.daily_limit_min === m ? 'bg-brand-500 text-white'
                                                : 'bg-slate-100 text-slate-500'}`}>
                {m === 180 ? 'Sınırsız' : `${m} dk`}
              </button>
            ))}
          </div>
        </div>

        {/* --- Mola --- */}
        <div className="border-t border-slate-100 pt-5">
          <div className="mb-2 flex items-center justify-between">
            <h2 className="font-black text-slate-700">Mola</h2>
            <button onClick={() => save({ break_enabled: !s.break_enabled })}
                    className={`rounded-xl px-4 py-2 text-sm font-extrabold transition ${
                      s.break_enabled ? 'bg-mint-500 text-white'
                                      : 'bg-slate-100 text-slate-500'}`}>
              {s.break_enabled ? 'Açık ✓' : 'Kapalı'}
            </button>
          </div>
          <p className="mb-4 text-xs font-bold text-slate-400">
            Çocuğunuz belirlediğiniz süre kadar çalışınca oyun molası hakkı
            kazanır. Mola bir ödül değil, dinlenme molasıdır — kullanmazsa
            bir şey kaybetmez.
          </p>

          {s.break_enabled && (
            <div className="grid gap-4">
              <div>
                <p className="mb-2 text-sm font-extrabold text-slate-600">
                  Kaç dakika çalışınca mola?
                </p>
                <div className="grid grid-cols-4 gap-2">
                  {[15, 20, 30, 45].map((m) => (
                    <button key={m} onClick={() => save({ study_minutes: m })}
                            className={`rounded-xl py-2.5 text-sm font-extrabold transition ${
                              s.study_minutes === m ? 'bg-brand-500 text-white'
                                                    : 'bg-slate-100 text-slate-500'}`}>
                      {m} dk
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <p className="mb-2 text-sm font-extrabold text-slate-600">
                  Mola ne kadar sürsün?
                </p>
                <div className="grid grid-cols-4 gap-2">
                  {[5, 10, 15, 20].map((m) => (
                    <button key={m} onClick={() => save({ break_minutes: m })}
                            className={`rounded-xl py-2.5 text-sm font-extrabold transition ${
                              s.break_minutes === m ? 'bg-sun-500 text-white'
                                                    : 'bg-slate-100 text-slate-500'}`}>
                      {m} dk
                    </button>
                  ))}
                </div>
              </div>

              <p className="rounded-xl bg-slate-50 px-4 py-3 text-sm
                            font-bold text-slate-500">
                Şu an: <b className="text-slate-700">{s.study_minutes || 30} dakika</b>{' '}
                çalışınca <b className="text-slate-700">{s.break_minutes || 15} dakika</b>{' '}
                mola hakkı
              </p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
