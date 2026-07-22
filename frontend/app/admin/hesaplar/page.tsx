'use client';

import { useEffect, useState, useCallback } from 'react';
import { adminApi } from '@/lib/api';
import {
  Panel, AdminSpinner, AdminBtn, AdminInput, AdminSelect, Badge, Empty, Toast,
} from '@/components/admin/UI';

export default function HesaplarPage() {
  const [data, setData] = useState<any>(null);
  const [f, setF] = useState({ q: '', plan: '', page: 1 });
  const [detay, setDetay] = useState<any>(null);
  const [msg, setMsg] = useState('');
  const [err, setErr] = useState('');

  const load = useCallback(async (params = f) => {
    setErr('');
    try { setData(await adminApi.accounts(params)); }
    catch (e: any) { setErr(e.message); }
  }, [f]);

  useEffect(() => { load(); }, []); // eslint-disable-line

  const filtre = (k: string, v: any) => {
    const n = { ...f, [k]: v, page: 1 };
    setF(n); setData(null); load(n);
  };

  const bildir = (m: string) => { setMsg(m); setTimeout(() => setMsg(''), 2500); };

  const planDegistir = async (a: any, plan: string) => {
    const gun = plan === 'family'
      ? parseInt(prompt('Kaç gün? (boş = süresiz)', '365') || '0') || undefined
      : undefined;
    try {
      await adminApi.setPlan(a.id, plan, gun);
      bildir(`${a.email} → ${plan === 'family' ? 'Aile' : 'Ücretsiz'}`);
      load();
    } catch (e: any) { alert(e.message); }
  };

  const adminYap = async (a: any) => {
    const yeni = !a.is_admin;
    if (!confirm(
      yeni
        ? `${a.email} admin yapılsın mı?\n\nBu hesap tüm çocukların verisine ` +
          'erişebilecek ve soruları değiştirebilecek.'
        : `${a.email} adminlikten çıkarılsın mı?`
    )) return;
    try {
      await adminApi.setAdmin(a.id, yeni);
      bildir(yeni ? 'Admin yapıldı' : 'Adminlik kaldırıldı');
      load();
    } catch (e: any) { alert(e.message); }
  };

  const profilleriGor = async (a: any) => {
    try { setDetay(await adminApi.accountProfiles(a.id)); }
    catch (e: any) { alert(e.message); }
  };

  return (
    <div className="grid gap-5">
      <Toast msg={msg} />

      <Panel>
        <div className="flex flex-wrap items-center gap-2">
          <AdminInput placeholder="E-posta ara…" value={f.q} className="w-64"
                      onChange={(e) => setF({ ...f, q: e.target.value })}
                      onKeyDown={(e) => e.key === 'Enter' && filtre('q', f.q)} />
          <AdminSelect value={f.plan} onChange={(e) => filtre('plan', e.target.value)}>
            <option value="">Tüm planlar</option>
            <option value="free">Ücretsiz</option>
            <option value="family">Aile</option>
          </AdminSelect>
          <AdminBtn onClick={() => filtre('q', f.q)}>Ara</AdminBtn>
        </div>
      </Panel>

      {err && <Panel><p className="font-bold text-coral-400">{err}</p></Panel>}
      {!data ? <AdminSpinner /> : (
        <Panel title={`${data.total} hesap`} sub={`Sayfa ${data.page}/${data.pages || 1}`}>
          {data.accounts.length === 0 ? <Empty text="Hesap bulunamadı." /> : (
            <>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-slate-800 text-left text-xs
                                   font-black uppercase text-slate-500">
                      <th className="pb-2 pr-3">E-posta</th>
                      <th className="pb-2 pr-3">Plan</th>
                      <th className="pb-2 pr-3 text-center">Çocuk</th>
                      <th className="pb-2 pr-3">Kayıt</th>
                      <th className="pb-2 pr-3">Son aktivite</th>
                      <th className="pb-2 text-right">İşlem</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.accounts.map((a: any) => (
                      <tr key={a.id} className="border-b border-slate-800/50
                                                hover:bg-slate-800/30">
                        <td className="py-2.5 pr-3">
                          <span className="font-bold text-slate-200">{a.email}</span>
                          {a.is_admin && (
                            <span className="ml-2"><Badge tone="blue">ADMIN</Badge></span>
                          )}
                        </td>
                        <td className="pr-3">
                          {a.plan === 'family'
                            ? <Badge tone="green">Aile</Badge>
                            : <Badge tone="slate">Ücretsiz</Badge>}
                          {a.plan_expires && (
                            <p className="mt-0.5 text-xs font-bold text-slate-600">
                              {a.plan_expires.slice(0, 10)}
                            </p>
                          )}
                        </td>
                        <td className="pr-3 text-center font-bold text-slate-400">
                          {a.profile_count}
                        </td>
                        <td className="pr-3 font-bold text-slate-500">
                          {a.created_at.slice(0, 10)}
                        </td>
                        <td className="pr-3 font-bold text-slate-500">
                          {a.last_activity ? a.last_activity.slice(0, 10) : '—'}
                        </td>
                        <td className="text-right">
                          <div className="flex justify-end gap-1">
                            <button onClick={() => profilleriGor(a)}
                                    className="rounded px-2 py-1 text-xs font-black
                                               text-slate-400 hover:bg-slate-700">
                              👁 Detay
                            </button>
                            <button
                              onClick={() => planDegistir(
                                a, a.plan === 'family' ? 'free' : 'family')}
                              className="rounded px-2 py-1 text-xs font-black
                                         text-brand-400 hover:bg-slate-700">
                              {a.plan === 'family' ? '↓ Ücretsiz' : '↑ Aile'}
                            </button>
                            <button onClick={() => adminYap(a)}
                                    className={`rounded px-2 py-1 text-xs font-black
                                                hover:bg-slate-700 ${
                                      a.is_admin ? 'text-coral-400'
                                                 : 'text-slate-500'}`}>
                              {a.is_admin ? '⚿ Kaldır' : '⚿ Admin'}
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
                            onClick={() => { const n = { ...f, page: f.page - 1 };
                                             setF(n); setData(null); load(n); }}>
                    ←
                  </AdminBtn>
                  <span className="px-3 font-black text-slate-400">
                    {data.page} / {data.pages}
                  </span>
                  <AdminBtn disabled={data.page >= data.pages}
                            onClick={() => { const n = { ...f, page: f.page + 1 };
                                             setF(n); setData(null); load(n); }}>
                    →
                  </AdminBtn>
                </div>
              )}
            </>
          )}
        </Panel>
      )}

      {detay && <ProfilDetay d={detay} onClose={() => setDetay(null)} />}
    </div>
  );
}

/* ------------------------------------------------------------------ */

function ProfilDetay({ d, onClose }: any) {
  return (
    <div className="fixed inset-0 z-40 flex items-start justify-center
                    overflow-y-auto bg-black/70 p-4 backdrop-blur-sm">
      <div className="my-8 w-full max-w-2xl rounded-2xl border border-slate-700
                      bg-slate-900 p-6">
        <div className="mb-2 flex items-center justify-between">
          <h2 className="text-lg font-black text-white">Hesap detayı</h2>
          <button onClick={onClose}
                  className="text-2xl font-black text-slate-500
                             hover:text-white">×</button>
        </div>
        <p className="mb-4 font-bold text-slate-400">{d.account_email}</p>

        <div className="mb-4 rounded-lg bg-brand-500/10 px-3 py-2 text-xs
                        font-bold text-brand-400">
          Gizlilik: Çocukların adları gösterilmez. Bu ekran yalnızca destek için
          gereken istatistikleri içerir ve görüntülenmesi işlem kaydına yazılır.
        </div>

        {d.profiles.length === 0 ? (
          <Empty text="Bu hesapta çocuk profili yok." />
        ) : (
          <div className="grid gap-3">
            {d.profiles.map((p: any, i: number) => (
              <div key={p.id} className="rounded-xl border border-slate-800
                                          bg-slate-800/40 p-4">
                <div className="mb-3 flex items-center justify-between">
                  <span className="font-black text-white">
                    Çocuk #{i + 1} · {p.grade}. sınıf
                  </span>
                  {!p.calibrated && <Badge tone="yellow">Kalibrasyon yapılmamış</Badge>}
                </div>
                <div className="grid grid-cols-3 gap-2 md:grid-cols-6">
                  <D l="Cevap" v={p.answers} />
                  <D l="Doğruluk" v={p.accuracy != null ? `%${p.accuracy}` : '—'}
                     tone={p.accuracy == null ? '' :
                       p.accuracy >= 75 && p.accuracy <= 85 ? 'text-mint-400'
                       : p.accuracy > 90 ? 'text-sun-400'
                       : p.accuracy < 60 ? 'text-coral-400' : ''} />
                  <D l="Görev" v={p.quests_completed} />
                  <D l="Seri" v={`🔥${p.streak}`} />
                  <D l="Yıldız" v={`⭐${p.stars}`} />
                  <D l="Kayıt" v={p.created_at.slice(5, 10)} />
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="mt-4 flex justify-end">
          <AdminBtn onClick={onClose}>Kapat</AdminBtn>
        </div>
      </div>
    </div>
  );
}

function D({ l, v, tone = '' }: { l: string; v: any; tone?: string }) {
  return (
    <div className="rounded-lg bg-slate-900/60 p-2 text-center">
      <p className={`font-black ${tone || 'text-white'}`}>{v}</p>
      <p className="text-[10px] font-bold text-slate-600">{l}</p>
    </div>
  );
}
