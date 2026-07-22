'use client';

import { useEffect, useState, useCallback } from 'react';
import { adminApi } from '@/lib/api';
import {
  Panel, AdminSpinner, AdminBtn, AdminInput, AdminSelect, Badge, Empty,
  Toast, STATUS_LABEL,
} from '@/components/admin/UI';

const BOS = {
  category_id: '', grade_min: 2, grade_max: 2, band: 3,
  text: '', options: ['', '', '', ''], answer_index: 0,
  explanation: '', status: 'draft', image_url: null as string | null,
};

export default function SorularPage() {
  const [cats, setCats] = useState<any[]>([]);
  const [data, setData] = useState<any>(null);
  const [f, setF] = useState({ category_id: '', status_f: '', band: '',
                               grade: '', q: '', page: 1 });
  const [edit, setEdit] = useState<any>(null);
  const [showImport, setShowImport] = useState(false);
  const [sel, setSel] = useState<Set<string>>(new Set());
  const [msg, setMsg] = useState('');
  const [err, setErr] = useState('');

  const load = useCallback(async (params = f) => {
    setErr('');
    try { setData(await adminApi.questions({ ...params, size: 50 })); }
    catch (e: any) { setErr(e.message); }
  }, [f]);

  useEffect(() => {
    adminApi.categories().then((r) => setCats(r.categories)).catch(() => {});
    load();
  }, []); // eslint-disable-line

  const filtre = (k: string, v: any) => {
    const n = { ...f, [k]: v, page: 1 };
    setF(n); setData(null); setSel(new Set()); load(n);
  };

  const sayfa = (p: number) => {
    const n = { ...f, page: p };
    setF(n); setData(null); load(n);
  };

  const bildir = (m: string) => { setMsg(m); setTimeout(() => setMsg(''), 2500); };

  const durumDegistir = async (id: string, status: string) => {
    try {
      await adminApi.setQuestionStatus(id, status);
      bildir(`${STATUS_LABEL[status]} yapıldı`);
      load();
    } catch (e: any) { setErr(e.message); }
  };

  const sil = async (q: any) => {
    if (!confirm(`Soru silinsin mi?\n\n"${q.text.slice(0, 60)}"`)) return;
    try {
      await adminApi.deleteQuestion(q.id);
      bildir('Silindi');
      load();
    } catch (e: any) {
      alert(e.message);
    }
  };

  const topluDurum = async (status: string) => {
    if (!sel.size) return;
    try {
      const r = await adminApi.bulkStatus([...sel], status);
      bildir(`${r.updated} soru ${STATUS_LABEL[status]} yapıldı`);
      setSel(new Set());
      load();
    } catch (e: any) { setErr(e.message); }
  };

  const disaAktar = async () => {
    try {
      const r = await adminApi.exportQuestions(f.category_id || undefined);
      const py = r.rows.map((x: any[]) =>
        `    (${x[0]}, ${x[1]}, ${x[2]}, ${JSON.stringify(x[3])}, ` +
        `${JSON.stringify(x[4])}, ${x[5]}, ${JSON.stringify(x[6])}),`
      ).join('\n');
      const içerik = `# ${r.count} soru\n# Format: (band, sinif_min, sinif_max, ` +
                     `soru, [siklar], dogru_index, aciklama)\n\nSORULAR = [\n${py}\n]\n`;
      const blob = new Blob([içerik], { type: 'text/plain' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `sorular_${f.category_id || 'tumu'}.py`;
      a.click();
      bildir(`${r.count} soru indirildi`);
    } catch (e: any) { setErr(e.message); }
  };

  const yaziliKats = cats.filter((c) => !c.is_procedural);

  return (
    <div className="grid gap-5">
      <Toast msg={msg} />

      {/* Filtreler */}
      <Panel>
        <div className="flex flex-wrap items-center gap-2">
          <AdminInput placeholder="Soru ara…" value={f.q}
                      onChange={(e) => setF({ ...f, q: e.target.value })}
                      onKeyDown={(e) => e.key === 'Enter' && filtre('q', f.q)}
                      className="w-52" />
          <AdminSelect value={f.category_id}
                       onChange={(e) => filtre('category_id', e.target.value)}>
            <option value="">Tüm kategoriler</option>
            {yaziliKats.map((c) => (
              <option key={c.id} value={c.id}>{c.icon} {c.name}</option>
            ))}
          </AdminSelect>
          <AdminSelect value={f.status_f}
                       onChange={(e) => filtre('status_f', e.target.value)}>
            <option value="">Tüm durumlar</option>
            <option value="live">Canlı</option>
            <option value="draft">Taslak</option>
            <option value="review">İncelemede</option>
            <option value="retired">Emekli</option>
          </AdminSelect>
          <AdminSelect value={f.band} onChange={(e) => filtre('band', e.target.value)}>
            <option value="">Tüm bantlar</option>
            {[1, 2, 3, 4, 5].map((b) => <option key={b} value={b}>Band {b}</option>)}
          </AdminSelect>
          <AdminSelect value={f.grade} onChange={(e) => filtre('grade', e.target.value)}>
            <option value="">Tüm sınıflar</option>
            {[1, 2, 3, 4].map((g) => <option key={g} value={g}>{g}. sınıf</option>)}
          </AdminSelect>

          <div className="ml-auto flex gap-2">
            <AdminBtn onClick={disaAktar}>↓ Dışa aktar</AdminBtn>
            <AdminBtn onClick={() => setShowImport(true)}>↑ İçe aktar</AdminBtn>
            <AdminBtn tone="primary"
                      onClick={() => setEdit({ ...BOS,
                        category_id: f.category_id || yaziliKats[0]?.id || '' })}>
              + Yeni soru
            </AdminBtn>
          </div>
        </div>

        {sel.size > 0 && (
          <div className="mt-3 flex flex-wrap items-center gap-2 rounded-xl
                          bg-slate-900 px-4 py-3">
            <span className="font-black text-white">{sel.size} soru seçili</span>
            <AdminBtn tone="good" onClick={() => topluDurum('live')}>
              Canlı yap
            </AdminBtn>
            <AdminBtn onClick={() => topluDurum('draft')}>Taslağa al</AdminBtn>
            <AdminBtn onClick={() => topluDurum('retired')}>Emekliye ayır</AdminBtn>
            <AdminBtn onClick={() => setSel(new Set())} className="ml-auto">
              Seçimi temizle
            </AdminBtn>
          </div>
        )}
      </Panel>

      {err && <Panel><p className="font-bold text-coral-400">{err}</p></Panel>}
      {!data ? <AdminSpinner /> : (
        <Panel title={`${data.total} soru`}
               sub={`Sayfa ${data.page}/${data.pages || 1}`}>
          {data.questions.length === 0 ? (
            <Empty text="Bu filtreye uyan soru yok." />
          ) : (
            <>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-slate-800 text-left text-xs
                                   font-black uppercase text-slate-500">
                      <th className="w-8 pb-2">
                        <input type="checkbox"
                               checked={sel.size === data.questions.length &&
                                        sel.size > 0}
                               onChange={(e) => setSel(e.target.checked
                                 ? new Set<string>(data.questions.map((q: any) => q.id))
                                 : new Set<string>())} />
                      </th>
                      <th className="pb-2 pr-3">Soru</th>
                      <th className="pb-2 pr-3">Kategori</th>
                      <th className="pb-2 pr-3 text-center">Sınıf</th>
                      <th className="pb-2 pr-3 text-center">Band</th>
                      <th className="pb-2 pr-3 text-center">İstatistik</th>
                      <th className="pb-2 pr-3">Durum</th>
                      <th className="pb-2 text-right">İşlem</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.questions.map((q: any) => (
                      <tr key={q.id} className="border-b border-slate-800/50
                                                hover:bg-slate-800/30">
                        <td className="py-2.5">
                          <input type="checkbox" checked={sel.has(q.id)}
                                 onChange={(e) => {
                                   const n = new Set<string>(sel);
                                   if (e.target.checked) n.add(q.id);
                                   else n.delete(q.id);
                                   setSel(n);
                                 }} />
                        </td>
                        <td className="max-w-[300px] pr-3">
                          <p className="truncate font-bold text-slate-200"
                             title={q.text}>{q.text}</p>
                          <p className="truncate text-xs font-bold text-mint-500">
                            ✓ {q.options[q.answer_index]}
                          </p>
                        </td>
                        <td className="pr-3 font-bold text-slate-500">
                          {q.category_name}
                        </td>
                        <td className="pr-3 text-center font-bold text-slate-400">
                          {q.grade_min === q.grade_max
                            ? q.grade_min : `${q.grade_min}–${q.grade_max}`}
                        </td>
                        <td className="pr-3 text-center">
                          <Badge tone="slate">{q.band}</Badge>
                        </td>
                        <td className="pr-3 text-center">
                          {q.serve_count > 0 ? (
                            <span className="text-xs font-bold text-slate-400">
                              {q.serve_count}× · %{q.real_accuracy}
                            </span>
                          ) : (
                            <span className="text-xs font-bold text-slate-700">—</span>
                          )}
                        </td>
                        <td className="pr-3">
                          <Badge tone={
                            q.status === 'live' ? 'green'
                            : q.status === 'draft' ? 'yellow'
                            : q.status === 'review' ? 'blue' : 'slate'}>
                            {STATUS_LABEL[q.status]}
                          </Badge>
                        </td>
                        <td className="text-right">
                          <div className="flex justify-end gap-1">
                            {q.status !== 'live' && (
                              <button onClick={() => durumDegistir(q.id, 'live')}
                                      title="Canlı yap"
                                      className="rounded px-2 py-1 text-xs font-black
                                                 text-mint-400 hover:bg-slate-700">
                                ✓
                              </button>
                            )}
                            {q.status === 'live' && (
                              <button onClick={() => durumDegistir(q.id, 'retired')}
                                      title="Emekliye ayır"
                                      className="rounded px-2 py-1 text-xs font-black
                                                 text-slate-400 hover:bg-slate-700">
                                ⏸
                              </button>
                            )}
                            <button onClick={() => setEdit({ ...q })}
                                    title="Düzenle"
                                    className="rounded px-2 py-1 text-xs font-black
                                               text-brand-400 hover:bg-slate-700">
                              ✎
                            </button>
                            <button onClick={() => sil(q)} title="Sil"
                                    className="rounded px-2 py-1 text-xs font-black
                                               text-coral-400 hover:bg-slate-700">
                              ✕
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {data.pages > 1 && (
                <div className="mt-4 flex items-center justify-center gap-2">
                  <AdminBtn disabled={data.page <= 1}
                            onClick={() => sayfa(data.page - 1)}>←</AdminBtn>
                  <span className="px-3 font-black text-slate-400">
                    {data.page} / {data.pages}
                  </span>
                  <AdminBtn disabled={data.page >= data.pages}
                            onClick={() => sayfa(data.page + 1)}>→</AdminBtn>
                </div>
              )}
            </>
          )}
        </Panel>
      )}

      {edit && (
        <QuestionModal q={edit} cats={yaziliKats}
                       onClose={() => setEdit(null)}
                       onSaved={() => { setEdit(null); bildir('Kaydedildi'); load(); }} />
      )}
      {showImport && (
        <ImportModal cats={yaziliKats} onClose={() => setShowImport(false)}
                     onDone={(n: number) => { setShowImport(false);
                                      bildir(`${n} soru eklendi`); load(); }} />
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */

function QuestionModal({ q, cats, onClose, onSaved }: any) {
  const [d, setD] = useState({ ...q });
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);

  const cat = cats.find((c: any) => c.id === d.category_id);

  const save = async () => {
    setErr(''); setBusy(true);
    try {
      const body = {
        category_id: d.category_id, grade_min: +d.grade_min,
        grade_max: +d.grade_max, band: +d.band, text: d.text,
        options: d.options, answer_index: +d.answer_index,
        explanation: d.explanation || '', status: d.status,
        image_url: d.image_url || null,
      };
      if (d.id) await adminApi.updateQuestion(d.id, body);
      else await adminApi.createQuestion(body);
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
      <div className="my-8 w-full max-w-2xl rounded-2xl border border-slate-700
                      bg-slate-900 p-6">
        <div className="mb-5 flex items-center justify-between">
          <h2 className="text-lg font-black text-white">
            {d.id ? 'Soruyu düzenle' : 'Yeni soru'}
          </h2>
          <button onClick={onClose}
                  className="text-2xl font-black text-slate-500
                             hover:text-white">×</button>
        </div>

        <div className="grid gap-4">
          <div className="grid grid-cols-2 gap-3 md:grid-cols-5">
            <div className="col-span-2">
              <L>Kategori</L>
              <AdminSelect value={d.category_id} className="w-full"
                           onChange={(e) => setD({ ...d, category_id: e.target.value })}>
                {cats.map((c: any) => (
                  <option key={c.id} value={c.id}>{c.icon} {c.name}</option>
                ))}
              </AdminSelect>
              {cat && (
                <p className="mt-1 text-xs font-bold text-slate-600">
                  {cat.grade_min}–{cat.grade_max}. sınıf
                </p>
              )}
            </div>
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
              <L>Band</L>
              <AdminSelect value={d.band} className="w-full"
                           onChange={(e) => setD({ ...d, band: +e.target.value })}>
                {[[1, 90], [2, 75], [3, 60], [4, 40], [5, 20]].map(([b, t]) => (
                  <option key={b} value={b}>{b} — hedef %{t}</option>
                ))}
              </AdminSelect>
            </div>
          </div>

          <div>
            <L>Soru metni</L>
            <textarea value={d.text} rows={2}
                      onChange={(e) => setD({ ...d, text: e.target.value })}
                      placeholder="Örn: 7 × 8 = ?"
                      className="w-full rounded-lg border border-slate-700
                                 bg-slate-950 px-3 py-2 font-semibold text-white
                                 outline-none focus:border-brand-500" />
            <p className="mt-1 text-xs font-bold text-slate-600">
              15 kelimeyi geçmeyin — bu yaşta uzun metin bilişsel yük yaratır.
            </p>
          </div>

          <div>
            <L>Şıklar — doğru olanı işaretleyin</L>
            <div className="grid gap-2">
              {d.options.map((o: string, i: number) => (
                <div key={i} className="flex items-center gap-2">
                  <button onClick={() => setD({ ...d, answer_index: i })}
                          title="Doğru cevap olarak işaretle"
                          className={`h-9 w-9 shrink-0 rounded-lg font-black
                                      transition ${
                            +d.answer_index === i
                              ? 'bg-mint-500 text-white'
                              : 'bg-slate-800 text-slate-500 hover:bg-slate-700'}`}>
                    {+d.answer_index === i ? '✓' : String.fromCharCode(65 + i)}
                  </button>
                  <AdminInput value={o} className="flex-1"
                              placeholder={`${i + 1}. şık`}
                              onChange={(e) => {
                                const n = [...d.options];
                                n[i] = e.target.value;
                                setD({ ...d, options: n });
                              }} />
                </div>
              ))}
            </div>
            <p className="mt-1.5 text-xs font-bold text-slate-600">
              Çeldiriciler <b className="text-slate-400">tipik hata</b> olmalı.
              Absürt şık (7×8 için "3" gibi) çocuğun eleyerek bulmasını sağlar,
              öğrenmez.
            </p>
          </div>

          <div>
            <L>Açıklama (yanlış cevaptan sonra gösterilir)</L>
            <AdminInput value={d.explanation || ''} className="w-full"
                        placeholder="Örn: 7 × 8 = 56"
                        onChange={(e) => setD({ ...d, explanation: e.target.value })} />
          </div>

          <div>
            <L>Durum</L>
            <AdminSelect value={d.status}
                         onChange={(e) => setD({ ...d, status: e.target.value })}>
              <option value="draft">Taslak — çocuklara gösterilmez</option>
              <option value="review">İncelemede</option>
              <option value="live">Canlı — çocuklara gösterilir</option>
              <option value="retired">Emekli</option>
            </AdminSelect>
          </div>

          {d.id && d.serve_count > 0 && (
            <p className="rounded-lg bg-sun-500/10 px-3 py-2 text-xs font-bold
                          text-sun-400">
              Bu soru {d.serve_count} kez gösterildi. Metni veya şıkları
              değiştirirseniz istatistikler sıfırlanır — eski veriler artık
              bu soruyu tarif etmiyor.
            </p>
          )}

          {err && (
            <p className="rounded-lg bg-coral-500/15 px-3 py-2 text-sm font-extrabold
                          text-coral-400">{err}</p>
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

/* ------------------------------------------------------------------ */

const ORNEK = `[
  [2, 2, 4, "'hızlı' kelimesinin eş anlamlısı?", ["çabuk", "yavaş", "ağır", "durgun"], 0, "hızlı = çabuk"],
  [3, 2, 4, "'küçük' kelimesinin eş anlamlısı?", ["ufak", "büyük", "geniş", "uzun"], 0, "küçük = ufak"]
]`;

function ImportModal({ cats, onClose, onDone }: any) {
  const [cid, setCid] = useState(cats[0]?.id || '');
  const [json, setJson] = useState('');
  const [status, setStatus] = useState('draft');
  const [err, setErr] = useState('');
  const [sonuc, setSonuc] = useState<any>(null);
  const [busy, setBusy] = useState(false);

  const gonder = async () => {
    setErr(''); setSonuc(null); setBusy(true);
    try {
      const rows = JSON.parse(json);
      if (!Array.isArray(rows)) throw new Error('JSON bir dizi olmalı');
      const r = await adminApi.importQuestions(cid, rows, status);
      setSonuc(r);
      if (r.added > 0 && r.error_count === 0) {
        setTimeout(() => onDone(r.added), 900);
      }
    } catch (e: any) {
      setErr(e.message.includes('JSON') ? `JSON hatası: ${e.message}` : e.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="fixed inset-0 z-40 flex items-start justify-center
                    overflow-y-auto bg-black/70 p-4 backdrop-blur-sm">
      <div className="my-8 w-full max-w-3xl rounded-2xl border border-slate-700
                      bg-slate-900 p-6">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-black text-white">Toplu soru içe aktar</h2>
          <button onClick={onClose}
                  className="text-2xl font-black text-slate-500
                             hover:text-white">×</button>
        </div>

        <p className="mb-4 text-sm font-bold text-slate-400">
          Format:{' '}
          <code className="text-brand-400">
            [band, sınıf_min, sınıf_max, "soru", ["a","b","c","d"], doğru_index, "açıklama"]
          </code>
          <br />
          <span className="text-xs text-slate-600">
            Aynı metne sahip sorular atlanır — aynı dosyayı iki kez göndermek
            zararsızdır.
          </span>
        </p>

        <div className="mb-3 flex flex-wrap gap-2">
          <AdminSelect value={cid} onChange={(e) => setCid(e.target.value)}>
            {cats.map((c: any) => (
              <option key={c.id} value={c.id}>{c.icon} {c.name}</option>
            ))}
          </AdminSelect>
          <AdminSelect value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="draft">Taslak olarak ekle</option>
            <option value="live">Doğrudan canlı</option>
          </AdminSelect>
          <AdminBtn onClick={() => setJson(ORNEK)}>Örnek doldur</AdminBtn>
        </div>

        <textarea value={json} onChange={(e) => setJson(e.target.value)}
                  rows={12} placeholder={ORNEK}
                  className="w-full rounded-lg border border-slate-700 bg-slate-950
                             p-3 font-mono text-xs text-slate-200 outline-none
                             focus:border-brand-500" />

        {err && (
          <p className="mt-3 rounded-lg bg-coral-500/15 px-3 py-2 text-sm
                        font-extrabold text-coral-400">{err}</p>
        )}

        {sonuc && (
          <div className="mt-3 rounded-lg bg-slate-800 p-3">
            <p className="font-black text-white">
              <span className="text-mint-400">{sonuc.added} eklendi</span>
              {sonuc.error_count > 0 &&
                <span className="text-coral-400"> · {sonuc.error_count} hata</span>}
            </p>
            {sonuc.errors?.length > 0 && (
              <ul className="mt-2 grid gap-0.5 text-xs font-bold text-coral-400">
                {sonuc.errors.map((e: any, i: number) => (
                  <li key={i}>Satır {e.row}: {e.error}</li>
                ))}
              </ul>
            )}
          </div>
        )}

        <div className="mt-4 flex justify-end gap-2">
          <AdminBtn onClick={onClose}>Kapat</AdminBtn>
          <AdminBtn tone="primary" onClick={gonder} disabled={busy || !json.trim()}>
            {busy ? 'Aktarılıyor…' : 'İçe aktar'}
          </AdminBtn>
        </div>
      </div>
    </div>
  );
}
