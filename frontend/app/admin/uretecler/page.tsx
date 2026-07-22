'use client';

import { useEffect, useState } from 'react';
import { adminApi } from '@/lib/api';
import {
  Panel, AdminSpinner, AdminBtn, AdminSelect, Badge, Empty,
} from '@/components/admin/UI';

/**
 * PROSEDUREL URETEC ONIZLEME
 *
 * Prosedurel sorularin kalitesi tamamen CELDIRICILERE baglidir.
 * Rastgele celdirici -> cocuk sikki eleyerek bulur, ogrenmez.
 * Bu ekran celdiricilerin gercekten "tipik hata" olup olmadigini
 * gozle kontrol etmek icindir.
 */
export default function UreteclerPage() {
  const [gens, setGens] = useState<any[]>([]);
  const [sel, setSel] = useState('');
  const [grade, setGrade] = useState(2);
  const [band, setBand] = useState(3);
  const [samples, setSamples] = useState<any[]>([]);
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    adminApi.generators().then((r) => {
      setGens(r.generators);
      if (r.generators.length) setSel(r.generators[0].key);
    }).catch((e) => setErr(e.message));
  }, []);

  const uret = async (key = sel, g = grade, b = band) => {
    if (!key) return;
    setBusy(true); setErr('');
    try {
      const r = await adminApi.previewGenerator(key, g, b, 8);
      setSamples(r.samples);
    } catch (e: any) {
      setErr(e.message); setSamples([]);
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => { if (sel) uret(); }, [sel]); // eslint-disable-line

  if (!gens.length && !err) return <AdminSpinner />;

  const aktif = gens.find((g) => g.key === sel);

  return (
    <div className="grid gap-5">
      <div className="rounded-2xl border border-slate-800 bg-slate-800/40 p-5">
        <h2 className="font-black text-white">Prosedürel üreteçler</h2>
        <p className="mt-2 text-sm font-bold leading-relaxed text-slate-400">
          Bu {gens.length} üreteç <b className="text-mint-400">sınırsız soru</b>{' '}
          üretir — soru bankası gerekmez, hiç tekrarlanmaz, üretim maliyeti sıfırdır.
          Günlük görevin yaklaşık yarısını bunlar karşılar.
        </p>
        <p className="mt-2 text-sm font-bold leading-relaxed text-slate-400">
          Kalitenin tamamı <b className="text-slate-200">çeldiricilere</b> bağlıdır:
          çeldiriciler çocuğun gerçekte yaptığı hatalardan üretilmelidir
          (7×8 için 54, 56, 63 gibi — komşu çarpım hataları).
          Absürt bir şık (örn. "3") çocuğun eleyerek bulmasını sağlar, öğrenmez.
          Aşağıdan gözle kontrol edin.
        </p>
      </div>

      <div className="grid gap-5 lg:grid-cols-[280px_1fr]">
        {/* Uretec listesi */}
        <Panel title="Üreteçler" sub={`${gens.length} adet`}>
          <div className="grid max-h-[560px] gap-1 overflow-y-auto">
            {gens.map((g) => (
              <button key={g.key} onClick={() => setSel(g.key)}
                      className={`rounded-lg px-3 py-2.5 text-left transition ${
                        sel === g.key ? 'bg-brand-500 text-white'
                                      : 'text-slate-300 hover:bg-slate-800'}`}>
                <p className="font-black">{g.key}</p>
                <p className={`truncate text-xs font-bold ${
                  sel === g.key ? 'text-brand-100' : 'text-slate-500'}`}>
                  {g.used_by.length ? g.used_by.join(', ') : 'kullanılmıyor'}
                </p>
              </button>
            ))}
          </div>
        </Panel>

        {/* Onizleme */}
        <Panel
          title={aktif ? aktif.key : 'Üreteç seçin'}
          sub={aktif?.used_by.length
            ? `Kullanan kategori: ${aktif.used_by.join(', ')}`
            : 'Hiçbir kategori bu üreteci kullanmıyor'}
          right={
            <div className="flex flex-wrap gap-2">
              <AdminSelect value={grade}
                           onChange={(e) => {
                             const g = +e.target.value;
                             setGrade(g); uret(sel, g, band);
                           }}>
                {[1, 2, 3, 4].map((g) => (
                  <option key={g} value={g}>{g}. sınıf</option>
                ))}
              </AdminSelect>
              <AdminSelect value={band}
                           onChange={(e) => {
                             const b = +e.target.value;
                             setBand(b); uret(sel, grade, b);
                           }}>
                {[[1, 90], [2, 75], [3, 60], [4, 40], [5, 20]].map(([b, t]) => (
                  <option key={b} value={b}>Band {b} — %{t}</option>
                ))}
              </AdminSelect>
              <AdminBtn tone="primary" onClick={() => uret()} disabled={busy}>
                {busy ? '…' : '🎲 Yeniden üret'}
              </AdminBtn>
            </div>
          }>
          {err ? (
            <p className="rounded-lg bg-coral-500/15 px-3 py-2 font-bold
                          text-coral-400">{err}</p>
          ) : samples.length === 0 ? (
            <Empty text="Örnek üretmek için 'Yeniden üret' düğmesine basın." />
          ) : (
            <div className="grid gap-3 md:grid-cols-2">
              {samples.map((s, i) => (
                <div key={i} className="rounded-xl border border-slate-800
                                        bg-slate-900/60 p-4">
                  {s.svg && (
                    <div className="mb-3 flex justify-center rounded-lg bg-white p-2"
                         dangerouslySetInnerHTML={{ __html: s.svg }} />
                  )}
                  <p className="whitespace-pre-line font-black text-white">
                    {s.text}
                  </p>
                  <div className="mt-3 grid grid-cols-2 gap-1.5">
                    {s.options.map((o: string, j: number) => (
                      <div key={j}
                           className={`rounded-lg px-2.5 py-1.5 text-sm font-bold ${
                             o === s.correct
                               ? 'bg-mint-500/20 text-mint-400'
                               : 'bg-slate-800 text-slate-400'}`}>
                        {o === s.correct && '✓ '}{o}
                      </div>
                    ))}
                  </div>
                  {s.explanation && (
                    <p className="mt-2 text-xs font-bold text-slate-600">
                      {s.explanation}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}

          {sel === 'carpim' && grade === 2 && (
            <p className="mt-4 rounded-lg bg-brand-500/10 px-3 py-2 text-xs
                          font-bold text-brand-400">
              Müfredat kontrolü: 2. sınıfta çarpım tablosu <b>sadece 1–5</b>.
              Yukarıdaki örneklerde 5'ten büyük çarpan görürseniz hata var.
            </p>
          )}
        </Panel>
      </div>
    </div>
  );
}
