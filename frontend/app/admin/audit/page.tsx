'use client';

import { useEffect, useState } from 'react';
import { adminApi } from '@/lib/api';
import {
  Panel, AdminSpinner, AdminBtn, AdminSelect, Badge, Empty,
} from '@/components/admin/UI';

const ACTION_LABEL: Record<string, string> = {
  'admin.login': 'Admin girişi',
  'admin.login_failed': 'Başarısız admin girişi',
  'question.create': 'Soru eklendi',
  'question.update': 'Soru güncellendi',
  'question.delete': 'Soru silindi',
  'question.status': 'Soru durumu değişti',
  'question.bulk_status': 'Toplu durum değişikliği',
  'question.import': 'Toplu soru içe aktarma',
  'question.export': 'Soru dışa aktarma',
  'category.update': 'Kategori güncellendi',
  'calibration.apply': 'Kalibrasyon uygulandı',
  'account.plan': 'Plan değiştirildi',
  'account.admin': 'Admin yetkisi değişti',
  'account.view_profiles': 'Hesap profilleri görüntülendi',
};

const TONE: Record<string, 'slate' | 'green' | 'yellow' | 'red' | 'blue'> = {
  'admin.login': 'blue',
  'admin.login_failed': 'red',
  'question.delete': 'red',
  'question.create': 'green',
  'question.import': 'green',
  'calibration.apply': 'blue',
  'account.admin': 'red',
  'account.plan': 'yellow',
  'account.view_profiles': 'yellow',
};

export default function AuditPage() {
  const [data, setData] = useState<any>(null);
  const [action, setAction] = useState('');
  const [page, setPage] = useState(1);
  const [err, setErr] = useState('');

  const load = async (p = page, a = action) => {
    setErr('');
    try { setData(await adminApi.audit(p, a)); }
    catch (e: any) { setErr(e.message); }
  };

  useEffect(() => { load(); }, []); // eslint-disable-line

  const filtre = (a: string) => {
    setAction(a); setPage(1); setData(null); load(1, a);
  };

  if (err) return <Panel><p className="font-bold text-coral-400">{err}</p></Panel>;

  return (
    <div className="grid gap-5">
      <div className="rounded-2xl border border-slate-800 bg-slate-800/40 p-5">
        <h2 className="font-black text-white">İşlem kaydı</h2>
        <p className="mt-1.5 text-sm font-bold text-slate-400">
          Admin panelinde yapılan her değişiklik burada iz bırakır.
          Çocuk verisine erişen işlemler de kaydedilir.
        </p>
      </div>

      <Panel
        title={data ? `${data.total} kayıt` : 'Yükleniyor'}
        right={
          <AdminSelect value={action} onChange={(e) => filtre(e.target.value)}>
            <option value="">Tüm işlemler</option>
            <option value="question">Soru işlemleri</option>
            <option value="category">Kategori işlemleri</option>
            <option value="account">Hesap işlemleri</option>
            <option value="calibration">Kalibrasyon</option>
            <option value="admin">Admin girişleri</option>
          </AdminSelect>
        }>
        {!data ? <AdminSpinner /> : data.logs.length === 0 ? (
          <Empty text="Kayıt yok." />
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-800 text-left text-xs
                                 font-black uppercase text-slate-500">
                    <th className="pb-2 pr-3">Zaman</th>
                    <th className="pb-2 pr-3">Admin</th>
                    <th className="pb-2 pr-3">İşlem</th>
                    <th className="pb-2">Detay</th>
                  </tr>
                </thead>
                <tbody>
                  {data.logs.map((l: any) => (
                    <tr key={l.id} className="border-b border-slate-800/50
                                              hover:bg-slate-800/30">
                      <td className="whitespace-nowrap py-2.5 pr-3 font-bold
                                     text-slate-500">
                        {l.created_at.slice(0, 19).replace('T', ' ')}
                      </td>
                      <td className="pr-3 font-bold text-slate-300">
                        {l.admin_email}
                      </td>
                      <td className="pr-3">
                        <Badge tone={TONE[l.action] || 'slate'}>
                          {ACTION_LABEL[l.action] || l.action}
                        </Badge>
                      </td>
                      <td className="max-w-[420px]">
                        <code className="block truncate text-xs font-bold
                                         text-slate-600"
                              title={JSON.stringify(l.detail)}>
                          {l.detail && Object.keys(l.detail).length
                            ? JSON.stringify(l.detail) : '—'}
                        </code>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {data.pages > 1 && (
              <div className="mt-4 flex items-center justify-center gap-2">
                <AdminBtn disabled={data.page <= 1}
                          onClick={() => { const p = data.page - 1;
                                           setPage(p); setData(null); load(p); }}>
                  ←
                </AdminBtn>
                <span className="px-3 font-black text-slate-400">
                  {data.page} / {data.pages}
                </span>
                <AdminBtn disabled={data.page >= data.pages}
                          onClick={() => { const p = data.page + 1;
                                           setPage(p); setData(null); load(p); }}>
                  →
                </AdminBtn>
              </div>
            )}
          </>
        )}
      </Panel>
    </div>
  );
}
