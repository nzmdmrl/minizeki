const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8420';

// ---------------------------------------------------------------- Storage
// Not: Artifact ortaminda degil, gercek tarayicida calisir.

export const store = {
  get(k: string): string | null {
    if (typeof window === 'undefined') return null;
    try { return window.localStorage.getItem(k); } catch { return null; }
  },
  set(k: string, v: string) {
    if (typeof window === 'undefined') return;
    try { window.localStorage.setItem(k, v); } catch { /* ignore */ }
  },
  del(k: string) {
    if (typeof window === 'undefined') return;
    try { window.localStorage.removeItem(k); } catch { /* ignore */ }
  },
};

export const token = {
  get: () => store.get('mz_token'),
  set: (t: string) => store.set('mz_token', t),
  clear: () => { store.del('mz_token'); store.del('mz_pin'); store.del('mz_profile'); store.del('mz_admin'); },
};

export const pinToken = {
  get: () => store.get('mz_pin'),
  set: (t: string) => store.set('mz_pin', t),
  clear: () => store.del('mz_pin'),
};

export const adminToken = {
  get: () => store.get('mz_admin'),
  set: (t: string) => store.set('mz_admin', t),
  clear: () => store.del('mz_admin'),
};

export const activeProfile = {
  get: () => store.get('mz_profile'),
  set: (id: string) => store.set('mz_profile', id),
  clear: () => store.del('mz_profile'),
};

// ---------------------------------------------------------------- Types

export type Question = {
  token: string;
  text: string;
  options: string[];
  svg?: string | null;
  emoji?: string | null;
  image_url?: string | null;
  category_id: string;
  category_name?: string;
  category_icon?: string;
};

export type Profile = {
  id: string;
  name: string;
  avatar_id: string;
  grade: number;
  star_balance: number;
  streak_days: number;
  shield_count: number;
  calibrated: boolean;
  quest_done_today: boolean;
};

export type AnswerResult = {
  correct: boolean;
  answer_index: number;
  correct_option: string;
  medal_up: boolean;
  medal?: { level: number; name: string; icon: string } | null;
  advanced: boolean;
  advance_message?: string | null;
  total_correct: number;
  star_balance: number;
};

export type CategoryItem = {
  id: string;
  name: string;
  subject: string;
  icon: string;
  medal_level: number;
  medal_name: string;
  medal_icon: string;
  total_correct: number;
  progress: number;
  next_at: number | null;
  locked: boolean;
};

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

// ---------------------------------------------------------------- Fetch

async function req<T>(
  path: string,
  opts: RequestInit & { pin?: boolean; admin?: boolean } = {}
): Promise<T> {
  const { pin, admin, ...init } = opts;
  const auth = admin ? adminToken.get() : pin ? pinToken.get() : token.get();

  const res = await fetch(`${API}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(auth ? { Authorization: `Bearer ${auth}` } : {}),
      ...(init.headers || {}),
    },
  });

  if (!res.ok) {
    let msg = 'Bir şeyler ters gitti';
    try {
      const j = await res.json();
      msg = j.detail || msg;
    } catch { /* ignore */ }

    if (res.status === 401 && !pin && !admin) {
      token.clear();
      if (typeof window !== 'undefined') window.location.href = '/giris';
    }
    throw new ApiError(msg, res.status);
  }

  return res.json();
}

const get = <T,>(p: string, pin = false) => req<T>(p, { method: 'GET', pin });
const post = <T,>(p: string, body?: unknown, pin = false) =>
  req<T>(p, { method: 'POST', body: body ? JSON.stringify(body) : undefined, pin });
const put = <T,>(p: string, body?: unknown, pin = false) =>
  req<T>(p, { method: 'PUT', body: body ? JSON.stringify(body) : undefined, pin });

// Admin ucları ayrı token kullanır
const aget = <T,>(p: string) => req<T>(p, { method: 'GET', admin: true });
const apost = <T,>(p: string, body?: unknown) =>
  req<T>(p, { method: 'POST', body: body ? JSON.stringify(body) : undefined, admin: true });
const aput = <T,>(p: string, body?: unknown) =>
  req<T>(p, { method: 'PUT', body: body ? JSON.stringify(body) : undefined, admin: true });
const adel = <T,>(p: string) => req<T>(p, { method: 'DELETE', admin: true });

// ---------------------------------------------------------------- API

export const api = {
  // Auth
  register: (email: string, password: string, pin: string) =>
    post<{ access_token: string; plan: string; email: string }>(
      '/api/auth/register', { email, password, pin }),

  login: (email: string, password: string) =>
    post<{ access_token: string; plan: string; email: string }>(
      '/api/auth/login', { email, password }),

  me: () => get<{ id: string; email: string; plan: string }>('/api/auth/me'),

  verifyPin: (pin: string) =>
    post<{ pin_token: string }>('/api/auth/verify-pin', { pin }),

  // Profil
  profiles: () => get<Profile[]>('/api/profiles'),

  createProfile: (name: string, avatar_id: string, grade: number) =>
    post<Profile>('/api/profiles', { name, avatar_id, grade }),

  profile: (id: string) => get<Profile>(`/api/profiles/${id}`),

  deleteProfile: (id: string) => req(`/api/profiles/${id}`, { method: 'DELETE' }),

  calibrateQuestions: (id: string) =>
    get<{ questions: Question[] }>(`/api/profiles/${id}/calibrate`),

  submitCalibration: (id: string, correct: number, total: number) =>
    post<{ ok: boolean; message: string }>(
      `/api/profiles/${id}/calibrate`, { correct, total }),

  // Oyun
  questToday: (profileId: string) =>
    get<{
      quest_id: string; date: string; total: number; progress: number;
      completed: boolean; questions: Question[];
    }>(`/api/quest/today?profile_id=${profileId}`),

  questComplete: (quest_id: string, correct: number, total: number) =>
    post<any>('/api/quest/complete', { quest_id, correct, total }),

  freePlay: (categoryId: string, profileId: string, count = 10) =>
    get<{ category: { id: string; name: string; icon: string };
          total: number; questions: Question[] }>(
      `/api/play/${categoryId}?profile_id=${profileId}&count=${count}`),

  answer: (t: string, selected: number, duration_ms: number) =>
    post<AnswerResult>('/api/answer', { token: t, selected, duration_ms }),

  categories: (profileId: string) =>
    get<{ categories: CategoryItem[] }>(`/api/categories?profile_id=${profileId}`),

  // Zeki'nin Evi
  house: (profileId: string) => get<any>(`/api/house?profile_id=${profileId}`),

  buyItem: (profile_id: string, item_id: string) =>
    post<any>('/api/house/buy', { profile_id, item_id }),

  // Ebeveyn
  dashboard: (profileId: string) =>
    get<any>(`/api/parent/dashboard?profile_id=${profileId}`, true),

  updateSettings: (profileId: string, body: any) =>
    put<any>(`/api/parent/settings?profile_id=${profileId}`, body, true),

  setFocus: (profileId: string, category_id: string | null, weeks = 1) =>
    put<any>(`/api/parent/focus?profile_id=${profileId}`,
             { category_id, weeks }, true),
};

// ---------------------------------------------------------------- Admin

export const adminApi = {
  login: (password: string) =>
    post<{ admin_token: string; email: string }>('/api/admin/login', { password }),

  me: () => aget<any>('/api/admin/me'),

  overview: () => aget<any>('/api/admin/overview'),

  activityChart: (days = 14) =>
    aget<{ data: any[] }>(`/api/admin/activity-chart?days=${days}`),

  // Kalibrasyon
  calibration: (onlyBad = true) =>
    aget<any>(`/api/admin/calibration?only_bad=${onlyBad}&limit=200`),
  applyCalibration: () => apost<any>('/api/admin/calibration/apply'),

  // Sorular
  questions: (params: Record<string, any>) => {
    const q = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v !== '' && v != null)
        .map(([k, v]) => [k, String(v)])
    );
    return aget<any>(`/api/admin/questions?${q}`);
  },
  createQuestion: (b: any) => apost<any>('/api/admin/questions', b),
  updateQuestion: (id: string, b: any) => aput<any>(`/api/admin/questions/${id}`, b),
  setQuestionStatus: (id: string, status: string) =>
    aput<any>(`/api/admin/questions/${id}/status`, { status }),
  deleteQuestion: (id: string) => adel<any>(`/api/admin/questions/${id}`),
  bulkStatus: (ids: string[], status: string) =>
    apost<any>('/api/admin/questions/bulk-status', { ids, status }),
  importQuestions: (category_id: string, rows: any[], status = 'draft') =>
    apost<any>('/api/admin/questions/import', { category_id, rows, status }),
  exportQuestions: (category_id?: string) =>
    aget<any>(`/api/admin/questions/export${category_id ? `?category_id=${category_id}` : ''}`),

  // Kategoriler
  categories: () => aget<any>('/api/admin/categories'),
  updateCategory: (id: string, b: any) => aput<any>(`/api/admin/categories/${id}`, b),

  // Üreteçler
  generators: () => aget<any>('/api/admin/generators'),
  previewGenerator: (key: string, grade: number, band: number, count = 5) =>
    aget<any>(`/api/admin/generators/${key}/preview?grade=${grade}&band=${band}&count=${count}`),

  // Hesaplar
  accounts: (params: Record<string, any> = {}) => {
    const q = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v !== '' && v != null)
        .map(([k, v]) => [k, String(v)])
    );
    return aget<any>(`/api/admin/accounts?${q}`);
  },
  setPlan: (id: string, plan: string, days?: number) =>
    aput<any>(`/api/admin/accounts/${id}/plan`, { plan, days }),
  setAdmin: (id: string, is_admin: boolean) =>
    aput<any>(`/api/admin/accounts/${id}/admin`, { is_admin }),
  accountProfiles: (id: string) => aget<any>(`/api/admin/accounts/${id}/profiles`),

  // Audit
  audit: (page = 1, action = '') =>
    aget<any>(`/api/admin/audit?page=${page}${action ? `&action=${action}` : ''}`),
};

// ---------------------------------------------------------------- Sabitler

export const AVATARS: Record<string, string> = {
  fox: '🦊', bear: '🐻', panda: '🐼', owl: '🦉', frog: '🐸', cat: '🐱',
};

export const SUBJECT_NAMES: Record<string, string> = {
  matematik: 'Matematik',
  turkce: 'Türkçe',
  hayat_bilgisi: 'Hayat Bilgisi',
  fen: 'Fen Bilimleri',
  sosyal: 'Sosyal Bilgiler',
  ingilizce: 'İngilizce',
};

export const SUBJECT_COLORS: Record<string, string> = {
  matematik: 'bg-brand-500',
  turkce: 'bg-mint-500',
  hayat_bilgisi: 'bg-sun-500',
  fen: 'bg-purple-500',
  sosyal: 'bg-orange-500',
  ingilizce: 'bg-coral-500',
};
