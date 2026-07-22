'use client';

import { useEffect, useState } from 'react';
import { adminApi } from '@/lib/api';
import {
  Panel, AdminSpinner, AdminBtn, Badge, Empty, Toast, Metric,
} from '@/components/admin/UI';

/**
 * GERCEK ZORLUK KALIBRASYONU
 *
 * Sistem her sorunun gercek zorlugunu olcer:
 *   gercek = correct_count / serve_count
 *
 * Bunu bandin hedefiyle karsilastirir (band 3 = %60 gibi).
 * Sapma buyukse soru yanlis banttadir ve zorluk motoru bozulur:
 * cocuk "kolay" sanilan bir soruda takilir, dogruluk hedef bandin disina cikar.
 */
export default function KalibrasyonPage() {
  const [d, setD] = useState<any>(null);
  const [onlyBad, setOnlyBad] = useState(true);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState('');
  const [err, setErr] = useState('');

  const load = async (bad = onlyBad) => {
    setErr('');
    try { setD(await adminApi.calibration(bad)); }
    catch (e: any) { setErr(e.message); }
  };

  useEffect(() => { load(); }, []); // eslint-disable-line

  const toggle = (v: boolean) => { setOnlyBad(v); setD(null); load(v); };

  const apply = async () => {
    if (!confirm(
      'Sapan tüm sorular önerilen banda taşınacak.\n\n' +
      'Bu işlem geri alınamaz ama zararsızdır: sorular silinmez, ' +
      'sadece zorluk bandı düzeltilir.\n\nDevam edilsin mi?'
    )) return;
    setBusy(true);
    try {
      const r = await adminApi.applyCalibration();
      setMsg(`${r.updated} sorunun bandı düzeltildi`);
      setTimeout(() => setMsg(''), 3000);
      setD(null);
      load();
    } catch (e: any) {
      setErr(e.message);
    } finally {
      setBusy(false);
    }
  };

  if (err) return <Panel><p className="font-bold text-coral-400">{err}</p></Panel>;
  if (!d) return <AdminSpinner />;

  const qs = d.questions;
  const bad = qs.filter((q: any) => q.miscalibrated);
  const cokKolay = bad.filter((q: any) => q.deviation > 0).length;
  const cokZor = bad.filter((q: any) => q.deviation < 0).length;

  return (
    <div className="grid gap-5">
      <Toast msg={msg} />

      {/* Aciklama */}
      <div className="rounded-2xl border border-slate-800 bg-slate-800/40 p-5">
        <h2 className="font-black text-white">Gerçek zorluk kalibrasyonu</h2>
        <p className="mt-2 text-sm font-bold leading-relaxed text-slate-400">
          Her soru <b className="text-slate-200">{d.min_serves}+ kez</b> gösterildikten
          sonra gerçek zorluğu ölçülebilir hale gelir:{' '}
          <code className="text-brand-400">doğru ÷ gösterim</code>.
          Bu değer bandın hedefinden ±%{d.tolerance}'den fazla saparsa soru yanlış
          banttadır — çocuk "kolay" sanılan soruda takılır ve zorluk motoru bozulur.
        </p>

        <div className="mt-4 grid grid-cols-2 gap-2 text-xs md:grid-cols-5">
          {[[1, 90], [2, 75], [3, 60], [4, 40], [5, 20]].map(([b, t]) => (
            <div key={b} className="rounded-lg border border-slate-800
                                    bg-slate-900/60 px-3 py-2">
              <span className="font-black text-white">Band {b}</span>
              <span className="ml-2 font-bold text-slate-500">hedef %{t}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Ozet */}
      <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <Metric label="Ölçülebilir soru" value={qs.length}
                hint={`${d.min_serves}+ gösterim`} />
        <Metric label="Yanlış bantta" value={bad.length}
                tone={bad.length > 0 ? 'warn' : 'good'} />
        <Metric label="Çok kolay" value={cokKolay}
                hint="hedeften yüksek doğruluk" />
        <Metric label="Çok zor" value={cokZor}
                hint="hedeften düşük doğruluk" />
      </div>

      <Panel
        title={onlyBad ? 'Yanlış banttaki sorular' : 'Tüm ölçülebilir sorular'}
        sub={`${qs.length} soru`}
        right={
          <div className="flex flex-wrap items-center gap-2">
            <AdminBtn onClick={() => toggle(!onlyBad)}>
              {onlyBad ? 'Hepsini göster' : 'Sadece sapanlar'}
            </AdminBtn>
            {bad.length > 0 && (
              <AdminBtn tone="primary" onClick={apply} disabled={busy}>
                {busy ? 'Uygulanıyor…' : `${bad.length} soruyu düzelt`}
              </AdminBtn>
            )}
          </div>
        }>
        {qs.length === 0 ? (
          <Empty text={
            onlyBad
              ? `Yanlış bantta soru yok. ${d.min_serves}+ kez gösterilen sorular doğru ` +
                'bantta — zorluk motoru sağlıklı çalışıyor.'
              : `Henüz ${d.min_serves} kez gösterilen soru yok. Çocuklar oynadıkça ` +
                'burada veri birikir.'
          } />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-800 text-left text-xs
                               font-black uppercase text-slate-500">
                  <th className="pb-2 pr-3">Soru</th>
                  <th className="pb-2 pr-3">Kategori</th>
                  <th className="pb-2 pr-3 text-center">Band</th>
                  <th className="pb-2 pr-3 text-center">Gösterim</th>
                  <th className="pb-2 pr-3 text-center">Gerçek</th>
                  <th className="pb-2 pr-3 text-center">Hedef</th>
                  <th className="pb-2 pr-3 text-center">Sapma</th>
                  <th className="pb-2 pr-3">Teşhis</th>
                  <th className="pb-2 text-center">Öneri</th>
                </tr>
              </thead>
              <tbody>
                {qs.map((q: any) => (
                  <tr key={q.id} className="border-b border-slate-800/50
                                            hover:bg-slate-800/30">
                    <td className="max-w-[280px] py-2.5 pr-3">
                      <p className="truncate font-bold text-slate-200"
                         title={q.text}>{q.text}</p>
                    </td>
                    <td className="pr-3 font-bold text-slate-500">
                      {q.category_name}
                    </td>
                    <td className="pr-3 text-center">
                      <Badge tone="slate">{q.band}</Badge>
                    </td>
                    <td className="pr-3 text-center font-bold text-slate-400">
                      {q.serve_count}
                    </td>
                    <td className="pr-3 text-center font-black text-white">
                      %{q.real_accuracy}
                    </td>
                    <td className="pr-3 text-center font-bold text-slate-500">
                      %{q.target_accuracy}
                    </td>
                    <td className="pr-3 text-center">
                      <span className={`font-black ${
                        Math.abs(q.deviation) > d.tolerance
                          ? q.deviation > 0 ? 'text-sun-400' : 'text-coral-400'
                          : 'text-slate-600'}`}>
                        {q.deviation > 0 ? '+' : ''}{q.deviation}
                      </span>
                    </td>
                    <td className="pr-3">
                      <Badge tone={
                        q.verdict === 'Çok kolay' ? 'yellow'
                        : q.verdict === 'Çok zor' ? 'red' : 'green'}>
                        {q.verdict}
                      </Badge>
                    </td>
                    <td className="text-center">
                      {q.miscalibrated && q.suggested_band !== q.band ? (
                        <span className="font-black text-brand-400">
                          {q.band} → {q.suggested_band}
                        </span>
                      ) : (
                        <span className="font-bold text-slate-700">—</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Panel>
    </div>
  );
}
