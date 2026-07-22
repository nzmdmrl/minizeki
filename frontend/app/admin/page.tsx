'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { adminApi } from '@/lib/api';
import { Panel, Metric, AdminSpinner, Badge } from '@/components/admin/UI';

export default function AdminOverview() {
  const [d, setD] = useState<any>(null);
  const [chart, setChart] = useState<any[]>([]);
  const [err, setErr] = useState('');

  useEffect(() => {
    adminApi.overview().then(setD).catch((e) => setErr(e.message));
    adminApi.activityChart(14).then((r) => setChart(r.data)).catch(() => {});
  }, []);

  if (err) return <Panel><p className="text-coral-400 font-bold">{err}</p></Panel>;
  if (!d) return <AdminSpinner />;

  const h = d.health;
  const tone = { good: 'good', ok: 'default', warn: 'warn',
                 bad: 'bad', unknown: 'default' }[h.status as string] as any;

  return (
    <div className="grid gap-5">
      {/* Sistem sagligi — en ustte, cunku en onemli sinyal */}
      <div className={`rounded-2xl border p-5 ${
        h.status === 'good' ? 'border-mint-500/40 bg-mint-500/10'
        : h.status === 'bad' ? 'border-coral-500/40 bg-coral-500/10'
        : h.status === 'warn' ? 'border-sun-500/40 bg-sun-500/10'
        : 'border-slate-800 bg-slate-800/40'}`}>
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-xs font-extrabold uppercase tracking-wide
                          text-slate-400">Sistem sağlığı</p>
            <p className="mt-1 text-xl font-black text-white">{h.message}</p>
            <p className="mt-0.5 text-sm font-bold text-slate-400">
              Bu haftaki doğruluk: %{h.accuracy_week} · Hedef bant: %75–85
            </p>
          </div>
          {h.miscalibrated_questions > 0 && (
            <Link href="/admin/kalibrasyon"
                  className="rounded-xl bg-sun-500 px-4 py-3 text-sm font-black
                             text-white transition hover:bg-sun-400">
              {h.miscalibrated_questions} soru yanlış bantta → Düzelt
            </Link>
          )}
        </div>
      </div>

      {/* Kullanicilar */}
      <Panel title="Kullanıcılar">
        <div className="grid grid-cols-2 gap-3 md:grid-cols-6">
          <Metric label="Hesap" value={d.users.accounts} />
          <Metric label="Çocuk profili" value={d.users.profiles} />
          <Metric label="Ödeyen" value={d.users.paying}
                  hint={`%${d.users.conversion} dönüşüm`}
                  tone={d.users.conversion >= 4 ? 'good' : 'default'} />
          <Metric label="Bugün aktif" value={d.users.dau} />
          <Metric label="Bu hafta" value={d.users.wau} />
          <Metric label="Bu ay" value={d.users.mau} />
        </div>
      </Panel>

      {/* Aktivite */}
      <Panel title="Aktivite">
        <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
          <Metric label="Bugün cevap" value={d.activity.answers_today} />
          <Metric label="Bu hafta cevap" value={d.activity.answers_week} />
          <Metric label="Bugün tamamlanan görev" value={d.activity.quests_today} />
          <Metric label="Görev tamamlama" value={`%${d.activity.completion_rate}`}
                  hint="hedef >%85"
                  tone={d.activity.completion_rate >= 85 ? 'good'
                        : d.activity.completion_rate >= 70 ? 'warn' : 'bad'} />
        </div>
      </Panel>

      {/* Grafik */}
      {chart.length > 0 && <ActivityChart data={chart} />}

      {/* Icerik */}
      <Panel title="İçerik" right={
        <Link href="/admin/sorular"
              className="rounded-lg bg-slate-700 px-3 py-2 text-sm font-extrabold
                         text-white hover:bg-slate-600">Soruları yönet</Link>
      }>
        <div className="grid grid-cols-2 gap-3 md:grid-cols-6">
          <Metric label="Kategori" value={d.content.categories} />
          <Metric label="Prosedürel" value={d.content.procedural}
                  hint="sınırsız soru" tone="good" />
          <Metric label="Yazılı kategori" value={d.content.written} />
          <Metric label="Canlı soru" value={d.content.questions_live} tone="good" />
          <Metric label="Taslak" value={d.content.questions_draft}
                  tone={d.content.questions_draft > 0 ? 'warn' : 'default'} />
          <Metric label="Üreteç" value={d.content.generators} />
        </div>
      </Panel>
    </div>
  );
}

/* ------------------------------------------------------------------ */

function ActivityChart({ data }: { data: any[] }) {
  const max = Math.max(...data.map((d) => d.answers), 1);

  return (
    <Panel title="Son 14 gün" sub="Çubuk: cevap sayısı · Çizgi: doğruluk (%)">
      <div className="flex h-52 items-end gap-1.5">
        {data.map((d) => {
          const h = (d.answers / max) * 100;
          const acc = d.accuracy;
          const tone = acc === 0 ? 'bg-slate-700'
            : acc >= 75 && acc <= 85 ? 'bg-mint-500'
            : acc > 90 ? 'bg-sun-500'
            : acc < 60 ? 'bg-coral-500' : 'bg-brand-500';
          return (
            <div key={d.date} className="group relative flex flex-1 flex-col
                                          items-center justify-end">
              {/* Tooltip */}
              <div className="pointer-events-none absolute bottom-full mb-2 hidden
                              whitespace-nowrap rounded-lg bg-slate-950 px-2 py-1.5
                              text-xs font-bold text-white shadow-xl
                              group-hover:block z-10">
                {d.date}<br />
                {d.answers} cevap · %{d.accuracy}<br />
                {d.active} aktif çocuk
              </div>
              <div className={`w-full rounded-t ${tone} transition-all`}
                   style={{ height: `${Math.max(h, 2)}%` }} />
              <span className="mt-1.5 text-[9px] font-bold text-slate-600">
                {d.date.slice(8)}
              </span>
            </div>
          );
        })}
      </div>
      <div className="mt-4 flex flex-wrap gap-3 text-xs font-bold text-slate-500">
        <span className="flex items-center gap-1.5">
          <i className="h-2.5 w-2.5 rounded-sm bg-mint-500" /> %75–85 hedef bant
        </span>
        <span className="flex items-center gap-1.5">
          <i className="h-2.5 w-2.5 rounded-sm bg-sun-500" /> &gt;%90 çok kolay
        </span>
        <span className="flex items-center gap-1.5">
          <i className="h-2.5 w-2.5 rounded-sm bg-coral-500" /> &lt;%60 çok zor
        </span>
        <span className="flex items-center gap-1.5">
          <i className="h-2.5 w-2.5 rounded-sm bg-brand-500" /> ara değer
        </span>
      </div>
    </Panel>
  );
}
