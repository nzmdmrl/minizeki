'use client';

// Zeki: baykus maskotu. Ruh haline gore ifade degistirir.
// SVG olarak cizilir - harici gorsel bagimliligi yok.

type Mood = 'happy' | 'thinking' | 'cheer' | 'calm' | 'sad';

export function Zeki({ mood = 'calm', size = 96 }: { mood?: Mood; size?: number }) {
  const eyes = {
    happy:    { l: '◕', r: '◕' },
    thinking: { l: '◔', r: '◔' },
    cheer:    { l: '^', r: '^' },
    calm:     { l: '●', r: '●' },
    sad:      { l: '◡', r: '◡' },
  }[mood];

  const beak = mood === 'cheer' || mood === 'happy' ? 'M50 56 L44 64 L56 64 Z' : 'M50 56 L45 63 L55 63 Z';

  return (
    <svg viewBox="0 0 100 100" width={size} height={size}
         className={mood === 'cheer' ? 'animate-float' : ''} aria-hidden="true">
      {/* Govde */}
      <ellipse cx="50" cy="62" rx="30" ry="32" fill="#8b6f47" />
      <ellipse cx="50" cy="66" rx="21" ry="24" fill="#d4b896" />
      {/* Kanatlar */}
      <ellipse cx="22" cy="62" rx="8" ry="20" fill="#7a5f3d" />
      <ellipse cx="78" cy="62" rx="8" ry="20" fill="#7a5f3d" />
      {/* Kafa */}
      <circle cx="50" cy="38" r="27" fill="#8b6f47" />
      {/* Kulak tuyleri */}
      <path d="M30 20 L26 8 L40 16 Z" fill="#7a5f3d" />
      <path d="M70 20 L74 8 L60 16 Z" fill="#7a5f3d" />
      {/* Goz cevresi */}
      <circle cx="39" cy="36" r="12" fill="#f5ede0" />
      <circle cx="61" cy="36" r="12" fill="#f5ede0" />
      {/* Gozler */}
      <text x="39" y="42" textAnchor="middle" fontSize="16" fill="#2d2318"
            fontWeight="bold">{eyes.l}</text>
      <text x="61" y="42" textAnchor="middle" fontSize="16" fill="#2d2318"
            fontWeight="bold">{eyes.r}</text>
      {/* Gaga */}
      <path d={beak} fill="#f59e0b" />
      {/* Ayaklar */}
      <path d="M42 92 L38 96 M42 92 L42 97 M42 92 L46 96" stroke="#f59e0b"
            strokeWidth="2.5" strokeLinecap="round" />
      <path d="M58 92 L54 96 M58 92 L58 97 M58 92 L62 96" stroke="#f59e0b"
            strokeWidth="2.5" strokeLinecap="round" />
    </svg>
  );
}

export function ZekiSays({ text, mood = 'happy' }: { text: string; mood?: Mood }) {
  return (
    <div className="flex items-start gap-3">
      <Zeki mood={mood} size={56} />
      <div className="relative flex-1 rounded-2xl bg-white border-2 border-slate-200 px-4 py-3">
        <div className="absolute -left-2 top-4 h-4 w-4 rotate-45 border-b-2 border-l-2
                        border-slate-200 bg-white" />
        <p className="font-bold text-slate-700">{text}</p>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------- Diger

export function Stat({ icon, value, label }: { icon: string; value: string | number; label?: string }) {
  return (
    <div className="flex items-center gap-1.5 rounded-full bg-white px-3 py-1.5
                    shadow-sm border border-slate-100">
      <span className="text-lg leading-none">{icon}</span>
      <span className="font-extrabold text-slate-800">{value}</span>
      {label && <span className="text-xs font-bold text-slate-400">{label}</span>}
    </div>
  );
}

export function ProgressBar({ value, className = '' }: { value: number; className?: string }) {
  return (
    <div className={`h-3 w-full overflow-hidden rounded-full bg-slate-100 ${className}`}>
      <div className="h-full rounded-full bg-brand-500 transition-all duration-500"
           style={{ width: `${Math.max(0, Math.min(100, value))}%` }} />
    </div>
  );
}

export function Spinner({ label }: { label?: string }) {
  return (
    <div className="flex flex-col items-center gap-3 py-12">
      <div className="h-10 w-10 animate-spin rounded-full border-4 border-slate-200
                      border-t-brand-500" />
      {label && <p className="font-bold text-slate-400">{label}</p>}
    </div>
  );
}

export function ErrorBox({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="card p-6 text-center">
      <p className="mb-4 font-bold text-slate-600">{message}</p>
      {onRetry && <button onClick={onRetry} className="btn-primary">Tekrar dene</button>}
    </div>
  );
}
