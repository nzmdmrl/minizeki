'use client';

import { useEffect, useState } from 'react';
import { adminApi, SUBJECT_NAMES } from '@/lib/api';
import {
  Panel, AdminSpinner, AdminBtn, AdminInput, AdminSelect, Badge, Toast, Empty,
} from '@/components/admin/UI';

export default function KategorilerPage() {
  const [cats, setCats] = useState<any[]>([]);
  const [edit, setEdit] = useState<any>(null);
  const [msg, setMsg] = useState('');
  const [err, setErr] = useState('');

  const load = async () => {
    setErr('');
    try { setCats((await adminApi.categories()).categories); }
    catch (e: any) { setErr(e.message); }
  };

  useEffect(() => { load(); }, []);

  if (err) return <Panel><p className="font-bold text-coral-400">{err}</p></Panel>;
  if (!cats.length) return <AdminSpinner />;

  const gruplar = cats.reduce<Record<string, any[]>>((a, c) => {
    (a[c.subject] ||= []).push(c);
    return a;
  }, {});
  const uyarili = cats.filter((c) => c.warning);

  return (
    <div className="grid gap-5">
      <Toast msg={msg} />

      {uyarili.length > 0 && (
        <Panel title="⚠️ Dikkat gerektiren kategoriler"
               sub="Soru bankası zayıf ya da zorluk dengesiz">
          <div className="grid gap-2">
            {uyarili.map((c) => (
              <div key={c.id} className="flex items-center gap-3 rounded-lg
                                          bg-sun-500/10 px-4 py-2.5">
                <span className="text-xl">{c.icon}</span>
                <span className="font-black text-white">{c.name}</span>
                <span className="text-sm font-bold text-sun-400">{c.warning}</span>
              </div>
            ))}
          </div>
        </Panel>
      )}

      {Object.entries(gruplar).map(([subject, items]) => (
        <Panel key={subject} title={SUBJECT_NAMES[subject] || subject}
               sub={`${items.length} kategori`}>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-800 text-left text-xs
                               font-black uppercase text-slate-500">
                  <th className="pb-2 pr-3">Kategori</th>
                  <th className="pb-2 pr-3 text-center">Sınıf</th>
                  <th className="pb-2 pr-3">Kaynak</th>
                  <th className="pb-2 pr-3 text-center">Canlı</th>
                  <th className="pb-2 pr-3 text-center">Taslak</th>
                  <th className="pb-2 pr-3 text-center">Cevap</th>
                  <th className="pb-2 pr-3 text-center">Doğruluk</th>
                  <th className="pb-2 pr-3">Plan</th>
                  <th className="pb-2 text-right">İşlem</th>
                </tr>
              </thead>
              <tbody>
                {items.map((c) => (
                  <tr key={c.id} className="border-b border-slate-800/50
                                            hover:bg-slate-800/30">
                    <td className="py-2.5 pr-3">
                      <span className="mr-2">{c.icon}</span>
                      <span className="font-black text-white">{c.name}</span>
                      {c.warning && (
                        <span className="ml-2 text-xs font-bold text-sun-400"
                              title={c.warning}>⚠️</span>
                      )}
                    </td>
                    <td className="pr-3 text-center font-bold text-slate-400">
                      {c.grade_min}–{c.grade_max}
                    </td>
                    <td className="pr-3">
                      {c.is_procedural ? (
                        <Badge tone="blue">⚙️ {c.generator_key}</Badge>
                      ) : (
                        <Badge tone="slate">✍️ yazılı</Badge>
                      )}
                    </td>
                    <td className="pr-3 text-center font-bold text-slate-300">
                      {c.is_procedural ? (
                        <span className="text-mint-400">∞</span>
                      ) : (
                        <span className={c.questions_live < 20
                          ? 'text-sun-400' : ''}>{c.questions_live}</span>
                      )}
                    </td>
                    <td className="pr-3 text-center font-bold text-slate-500">
                      {c.is_procedural ? '—' : c.questions_draft}
                    </td>
                    <td className="pr-3 text-center font-bold text-slate-400">
                      {c.answers}
                    </td>
                    <td className="pr-3 text-center">
                      {c.accuracy == null ? (
                        <span className="font-bold text-slate-700">—</span>
                      ) : (
                        <span className={`font-black ${
                          c.accuracy >= 75 && c.accuracy <= 85 ? 'text-mint-400'
                          : c.accuracy > 92 ? 'text-sun-400'
                          : c.accuracy < 55 ? 'text-coral-400' : 'text-slate-300'}`}>
                          %{c.accuracy}
                        </span>
                      )}
                    </td>
                    <td className="pr-3">
                      {c.is_free ? <Badge tone="green">Ücretsiz</Badge>
                                 : <Badge tone="slate">Aile</Badge>}
                    </td>
                    <td className="text-right">
                      <button onClick={() => setEdit({ ...c })}
                              className="rounded px-2 py-1 text-xs font-black
                                         text-brand-400 hover:bg-slate-700">
                        ✎ Düzenle
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Panel>
      ))}

      {edit && (
        <CategoryModal c={edit} onClose={() => setEdit(null)}
                       onSaved={() => {
                         setEdit(null);
                         setMsg('Kaydedildi');
                         setTimeout(() => setMsg(''), 2000);
                         load();
                       }} />
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */

function CategoryModal({ c, onClose, onSaved }: any) {
  const [d, setD] = useState({ ...c });
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);

  const save = async () => {
    setErr(''); setBusy(true);
    try {
      await adminApi.updateCategory(d.id, {
        name: d.name, subject: d.subject, icon: d.icon,
        grade_min: +d.grade_min, grade_max: +d.grade_max,
        has_upper_grade: d.has_upper_grade, is_free: d.is_free,
        sort_order: +d.sort_order,
      });
      onSaved();
    } catch (e: any) {
      setErr(e.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="fixed inset-0 z-40 flex items-start justify-center
                    overflow-y-auto bg-black/70 p-4 backdrop-blur-sm">
      <div className="my-8 w-full max-w-lg rounded-2xl border border-slate-700
                      bg-slate-900 p-6">
        <div className="mb-5 flex items-center justify-between">
          <h2 className="text-lg font-black text-white">Kategoriyi düzenle</h2>
          <button onClick={onClose}
                  className="text-2xl font-black text-slate-500
                             hover:text-white">×</button>
        </div>

        <div className="grid gap-4">
          <div className="grid grid-cols-4 gap-3">
            <div>
              <L>İkon</L>
              <AdminInput value={d.icon} className="w-full text-center text-xl"
                          onChange={(e) => setD({ ...d, icon: e.target.value })} />
            </div>
            <div className="col-span-3">
              <L>Ad</L>
              <AdminInput value={d.name} className="w-full"
                          onChange={(e) => setD({ ...d, name: e.target.value })} />
            </div>
          </div>

          <div>
            <L>Ders</L>
            <AdminSelect value={d.subject} className="w-full"
                         onChange={(e) => setD({ ...d, subject: e.target.value })}>
              {Object.entries(SUBJECT_NAMES).map(([k, v]) => (
                <option key={k} value={k}>{v}</option>
              ))}
            </AdminSelect>
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <L>Sınıf min</L>
              <AdminSelect value={d.grade_min} className="w-full"
                           onChange={(e) => setD({ ...d, grade_min: +e.target.value })}>
                {[1, 2, 3, 4].map((g) => <option key={g} value={g}>{g}</option>)}
              </AdminSelect>
            </div>
            <div>
              <L>Sınıf max</L>
              <AdminSelect value={d.grade_max} className="w-full"
                           onChange={(e) => setD({ ...d, grade_max: +e.target.value })}>
                {[1, 2, 3, 4].map((g) => <option key={g} value={g}>{g}</option>)}
              </AdminSelect>
            </div>
            <div>
              <L>Sıra</L>
              <AdminInput type="number" value={d.sort_order} className="w-full"
                          onChange={(e) => setD({ ...d, sort_order: e.target.value })} />
            </div>
          </div>

          <label className="flex cursor-pointer items-start gap-3 rounded-lg
                            bg-slate-800/50 p-3">
            <input type="checkbox" checked={d.is_free} className="mt-1"
                   onChange={(e) => setD({ ...d, is_free: e.target.checked })} />
            <div>
              <p className="font-black text-white">Ücretsiz planda açık</p>
              <p className="text-xs font-bold text-slate-500">
                Kapalıysa sadece Aile planındaki çocuklar oynayabilir.
              </p>
            </div>
          </label>

          <label className="flex cursor-pointer items-start gap-3 rounded-lg
                            bg-slate-800/50 p-3">
            <input type="checkbox" checked={d.has_upper_grade} className="mt-1"
                   onChange={(e) => setD({ ...d, has_upper_grade: e.target.checked })} />
            <div>
              <p className="font-black text-white">Terfi edebilir</p>
              <p className="text-xs font-bold text-slate-500">
                Çocuk ustalaştığında üst sınıf soruları açılır. Üst sınıfta
                karşılığı olmayan konularda (örn. "Okulumuz") kapatın.
              </p>
            </div>
          </label>

          {d.is_procedural && (
            <p className="rounded-lg bg-brand-500/10 px-3 py-2 text-xs font-bold
                          text-brand-400">
              Prosedürel kategori — soruları{' '}
              <code>{d.generator_key}</code> üreteci üretir. Soru bankası
              gerekmez, hiç tekrarlanmaz.
            </p>
          )}

          {err && (
            <p className="rounded-lg bg-coral-500/15 px-3 py-2 text-sm
                          font-extrabold text-coral-400">{err}</p>
          )}

          <div className="flex justify-end gap-2">
            <AdminBtn onClick={onClose}>Vazgeç</AdminBtn>
            <AdminBtn tone="primary" onClick={save} disabled={busy}>
              {busy ? 'Kaydediliyor…' : 'Kaydet'}
            </AdminBtn>
          </div>
        </div>
      </div>
    </div>
  );
}

function L({ children }: { children: React.ReactNode }) {
  return (
    <label className="mb-1 block text-xs font-black uppercase tracking-wide
                      text-slate-500">{children}</label>
  );
}
