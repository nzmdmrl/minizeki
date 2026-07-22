'use client';

/* Admin paneli icin ortak parcalar. Koyu tema. */

export function Panel({ title, sub, right, children }: {
  title?: string; sub?: string; right?: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-800/40">
      {(title || right) && (
        <div className="flex items-start justify-between gap-4 border-b
                        border-slate-800 px-5 py-4">
          <div>
            {title && <h2 className="font-black text-white">{title}</h2>}
            {sub && <p className="mt-0.5 text-xs font-bold text-slate-500">{sub}</p>}
          </div>
          {right}
        </div>
      )}
      <div className="p-5">{children}</div>
    </section>
  );
}

export function Metric({ label, value, hint, tone = 'default' }: {
  label: string; value: React.ReactNode; hint?: string;
  tone?: 'default' | 'good' | 'warn' | 'bad';
}) {
  const c = {
    default: 'text-white',
    good: 'text-mint-400',
    warn: 'text-sun-400',
    bad: 'text-coral-400',
  }[tone];
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
      <p className="text-xs font-extrabold uppercase tracking-wide text-slate-500">
        {label}
      </p>
      <p className={`mt-1 text-2xl font-black ${c}`}>{value}</p>
      {hint && <p className="mt-0.5 text-xs font-bold text-slate-600">{hint}</p>}
    </div>
  );
}

export function Badge({ children, tone = 'slate' }: {
  children: React.ReactNode;
  tone?: 'slate' | 'green' | 'yellow' | 'red' | 'blue';
}) {
  const c = {
    slate: 'bg-slate-700 text-slate-300',
    green: 'bg-mint-500/20 text-mint-400',
    yellow: 'bg-sun-500/20 text-sun-400',
    red: 'bg-coral-500/20 text-coral-400',
    blue: 'bg-brand-500/20 text-brand-400',
  }[tone];
  return (
    <span className={`inline-block rounded-md px-2 py-0.5 text-xs font-black ${c}`}>
      {children}
    </span>
  );
}

export const STATUS_TONE: Record<string, 'slate' | 'green' | 'yellow' | 'red'> = {
  live: 'green', draft: 'yellow', review: 'blue' as any, retired: 'slate',
};
export const STATUS_LABEL: Record<string, string> = {
  live: 'Canlı', draft: 'Taslak', review: 'İncelemede', retired: 'Emekli',
};

export function AdminInput(props: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input {...props}
      className={`rounded-lg border border-slate-700 bg-slate-900 px-3 py-2
                  text-sm font-semibold text-white outline-none
                  focus:border-brand-500 ${props.className || ''}`} />
  );
}

export function AdminSelect(props: React.SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select {...props}
      className={`rounded-lg border border-slate-700 bg-slate-900 px-3 py-2
                  text-sm font-semibold text-white outline-none
                  focus:border-brand-500 ${props.className || ''}`} />
  );
}

export function AdminBtn({ tone = 'default', ...p }:
  React.ButtonHTMLAttributes<HTMLButtonElement> &
  { tone?: 'default' | 'primary' | 'danger' | 'good' }) {
  const c = {
    default: 'bg-slate-700 hover:bg-slate-600 text-white',
    primary: 'bg-brand-500 hover:bg-brand-600 text-white',
    danger: 'bg-coral-500 hover:bg-coral-400 text-white',
    good: 'bg-mint-500 hover:bg-mint-600 text-white',
  }[tone];
  return (
    <button {...p}
      className={`rounded-lg px-3 py-2 text-sm font-extrabold transition
                  disabled:opacity-40 ${c} ${p.className || ''}`} />
  );
}

export function AdminSpinner() {
  return (
    <div className="flex justify-center py-16">
      <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-700
                      border-t-brand-400" />
    </div>
  );
}

export function Empty({ text }: { text: string }) {
  return (
    <p className="py-12 text-center text-sm font-bold text-slate-600">{text}</p>
  );
}

export function Toast({ msg, tone = 'good' }: {
  msg: string; tone?: 'good' | 'bad';
}) {
  if (!msg) return null;
  return (
    <div className={`fixed bottom-6 left-1/2 z-50 -translate-x-1/2 rounded-xl
                     px-5 py-3 font-extrabold shadow-2xl ${
      tone === 'good' ? 'bg-mint-500 text-white' : 'bg-coral-500 text-white'}`}>
      {msg}
    </div>
  );
}
