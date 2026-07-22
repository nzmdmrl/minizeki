'use client';

import Link from 'next/link';

const ALANLAR = [
  {
    baslik: 'Matematik',
    renk: 'brand',
    konular: ['Sayılar', 'Toplama–Çıkarma', 'Çarpım Tablosu', 'Basamak Değeri', 'Ritmik Sayma', 'Saat Okuma', 'Para Hesabı', 'Örüntü', 'Geometrik Şekiller'],
  },
  {
    baslik: 'Türkçe',
    renk: 'mint',
    konular: ['Hece Sayısı', 'Alfabetik Sıralama', 'Eksik Harf', 'Sesli Harfler', 'Eş Anlamlı', 'Zıt Anlamlı', 'Doğru Yazılış', 'Noktalama'],
  },
  {
    baslik: 'Hayat Bilgisi',
    renk: 'sun',
    konular: ['Okulumuz', 'Ailemiz ve Evimiz', 'Sağlığımız', 'Güvenliğimiz', 'Ülkemiz ve Atatürk', 'Doğa ve Çevre'],
  },
  {
    baslik: 'İngilizce',
    renk: 'coral',
    konular: ['İngilizce Kelimeler', 'İngilizce İfadeler'],
  },
];

const RENK_SINIF: Record<string, { bg: string; text: string; ring: string }> = {
  brand: { bg: 'bg-brand-50', text: 'text-brand-700', ring: 'ring-brand-200' },
  mint: { bg: 'bg-mint-400/10', text: 'text-mint-600', ring: 'ring-mint-400/30' },
  sun: { bg: 'bg-sun-400/10', text: 'text-sun-500', ring: 'ring-sun-400/30' },
  coral: { bg: 'bg-coral-400/10', text: 'text-coral-500', ring: 'ring-coral-400/30' },
};

const ADIMLAR = [
  {
    no: '1',
    baslik: 'Çocuğun seviyesini tanıyoruz',
    metin: 'Kısa bir tanışma turuyla hangi konularda rahat, hangilerinde desteğe ihtiyacı olduğunu belirliyoruz. Not verilmiyor, sıralama yapılmıyor.',
  },
  {
    no: '2',
    baslik: 'Her gün kısa bir görev',
    metin: 'Oturup saatlerce çalışmak yok. Günlük görev birkaç dakikada biter; düzenli tekrar, uzun seanslardan daha çok işe yarar.',
  },
  {
    no: '3',
    baslik: 'Zorlandığı konu daha sık gelir',
    metin: 'Sistem yanlışları takip eder ve o konuyu araya tekrar serpiştirir. Bildiği yerde oyalanmaz, takıldığı yerde pratik yapar.',
  },
];

const SSS = [
  {
    s: 'Süre sınırı gerçekten yok mu?',
    c: 'Yok. Soruların üzerinde geri sayan bir sayaç, "hızlı ol" uyarısı ya da süreye bağlı puan yok. Çocuk soruyu düşünmek için istediği kadar bekleyebilir.',
  },
  {
    s: 'Başka çocuklarla yarışıyor mu?',
    c: 'Hayır. Sıralama tablosu, rakip, canlı düello gibi bölümler yok. İlerleme yalnızca çocuğun kendi geçmişine göre gösterilir.',
  },
  {
    s: 'Hangi sınıflara uygun?',
    c: '1, 2, 3 ve 4. sınıf konularını kapsıyor. İçerik çocuğun seviyesine göre açılıyor, sınıf atladıkça aynı hesap devam ediyor.',
  },
  {
    s: 'Çocuğumun ne yaptığını görebilir miyim?',
    c: 'Evet. Ebeveyn paneli hangi konularda ilerlediğini, nerede zorlandığını ve günlük çalışma geçmişini gösterir. Panel dört haneli PIN ile korunur, çocuk kendi başına giremez.',
  },
  {
    s: 'Reklam var mı?',
    c: 'Yok. Çocuk ekranında reklam, dış bağlantı veya satın alma yönlendirmesi bulunmuyor.',
  },
];

export default function TanitimPage() {
  return (
    <main className="min-h-screen bg-[var(--bg)]">
      {/* ---------------- Üst bar ---------------- */}
      <header className="mx-auto flex max-w-6xl items-center justify-between px-5 py-5">
        <div className="flex items-center gap-2">
          <div className="grid h-10 w-10 place-items-center rounded-2xl bg-brand-500 text-xl font-black text-white shadow-lg shadow-brand-500/25">
            M
          </div>
          <span className="text-xl font-black tracking-tight text-slate-800">Minizeki</span>
        </div>
        <Link href="/giris" className="btn-ghost !min-h-[44px] !px-5 text-base">
          Giriş yap
        </Link>
      </header>

      {/* ---------------- Hero ---------------- */}
      <section className="mx-auto max-w-6xl px-5 pb-16 pt-10 sm:pt-16">
        <div className="grid items-center gap-12 lg:grid-cols-2">
          <div>
            <span className="inline-block rounded-full bg-mint-400/15 px-4 py-1.5 text-sm font-extrabold text-mint-600">
              1–4. sınıf · Süre yok · Yarış yok
            </span>

            <h1 className="mt-5 text-4xl font-black leading-[1.1] tracking-tight text-slate-800 sm:text-5xl lg:text-6xl">
              Her gün birkaç dakika.
              <br />
              <span className="text-brand-500">Baskı olmadan tekrar.</span>
            </h1>

            <p className="mt-6 max-w-lg text-lg font-semibold leading-relaxed text-slate-600">
              Minizeki, ilkokul çocuğuna günlük kısa görevler vererek konuları
              tekrar ettirir. Zorlandığı konuyu fark eder, orada daha çok pratik
              yaptırır. Geri sayan sayaç, sıralama tablosu ve rakip yok —
              yalnızca kendi hızında ferah bir çalışma alanı.
            </p>

            <div className="mt-8 flex flex-wrap gap-3">
              <Link href="/giris" className="btn-primary text-lg">
                Ücretsiz başla
              </Link>
              <a href="#nasil-calisir" className="btn-ghost text-lg">
                Nasıl çalışır?
              </a>
            </div>

            <p className="mt-4 text-sm font-bold text-slate-400">
              Kayıt için yalnızca e-posta yeterli · Çocuk ekranında reklam yok
            </p>
          </div>

          {/* Görsel taraf: soru kartı önizlemesi */}
          <div className="relative">
            <div className="card animate-float p-6 sm:p-8">
              <div className="flex items-center justify-between">
                <span className="rounded-full bg-brand-50 px-3 py-1 text-sm font-extrabold text-brand-700">
                  Çarpım Tablosu
                </span>
                <span className="text-sm font-extrabold text-slate-400">
                  Günlük görev · 2/5
                </span>
              </div>

              <p className="mt-6 text-2xl font-black text-slate-800">
                6 × 7 kaç eder?
              </p>

              <div className="mt-5 space-y-3">
                <div className="opt opt-muted !min-h-[56px] !py-4 !text-lg">36</div>
                <div className="opt opt-correct !min-h-[56px] !py-4 !text-lg">42</div>
                <div className="opt !min-h-[56px] !py-4 !text-lg">48</div>
              </div>

              <p className="mt-5 text-center text-sm font-bold text-slate-400">
                Acele etmesine gerek yok — sayaç çalışmıyor.
              </p>
            </div>

            <div className="absolute -bottom-4 -left-4 hidden rounded-2xl bg-white px-4 py-3 shadow-lg ring-1 ring-slate-100 sm:block">
              <p className="text-sm font-extrabold text-slate-700">809 soru</p>
              <p className="text-xs font-bold text-slate-400">27 konu başlığı</p>
            </div>
          </div>
        </div>
      </section>

      {/* ---------------- Farkımız ---------------- */}
      <section className="border-y border-slate-100 bg-white py-16">
        <div className="mx-auto max-w-6xl px-5">
          <h2 className="text-center text-3xl font-black tracking-tight text-slate-800 sm:text-4xl">
            Baskı çocuğu öğrenmekten uzaklaştırır
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-center text-lg font-semibold text-slate-600">
            Çoğu eğitim uygulaması dikkat çekmek için süre, seri ve sıralama
            kullanır. Küçük yaşta bu, öğrenmenin değil kaygının kaynağı olur.
            Minizeki bunları kullanmıyor.
          </p>

          <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { b: 'Sayaç yok', m: 'Soruda geri sayım yok. Düşünmek için istediği kadar zamanı var.' },
              { b: 'Sıralama yok', m: 'Başka çocuklarla karşılaştırma yapılmaz. Ölçü kendi ilerlemesi.' },
              { b: 'Seri bozma baskısı yok', m: 'Bir gün atlarsa kaybettiği bir şey olmaz, kaldığı yerden devam eder.' },
              { b: 'Kısa oturum', m: 'Günlük görev birkaç dakika sürer. Düzen, süreden önemlidir.' },
            ].map((x) => (
              <div key={x.b} className="card p-6">
                <p className="text-lg font-black text-slate-800">{x.b}</p>
                <p className="mt-2 text-base font-semibold leading-relaxed text-slate-600">
                  {x.m}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ---------------- Nasıl çalışır ---------------- */}
      <section id="nasil-calisir" className="py-16">
        <div className="mx-auto max-w-6xl px-5">
          <h2 className="text-center text-3xl font-black tracking-tight text-slate-800 sm:text-4xl">
            Nasıl çalışır?
          </h2>

          <div className="mt-10 grid gap-6 md:grid-cols-3">
            {ADIMLAR.map((a) => (
              <div key={a.no} className="card p-7">
                <div className="grid h-12 w-12 place-items-center rounded-2xl bg-brand-500 text-xl font-black text-white">
                  {a.no}
                </div>
                <h3 className="mt-5 text-xl font-black text-slate-800">{a.baslik}</h3>
                <p className="mt-2 text-base font-semibold leading-relaxed text-slate-600">
                  {a.metin}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ---------------- Konular ---------------- */}
      <section className="border-y border-slate-100 bg-white py-16">
        <div className="mx-auto max-w-6xl px-5">
          <h2 className="text-center text-3xl font-black tracking-tight text-slate-800 sm:text-4xl">
            1–4. sınıf konuları
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-center text-lg font-semibold text-slate-600">
            Dört alanda 27 konu başlığı, 809 soru. İçerik çocuğun seviyesine
            göre açılır; sınıf atladıkça aynı hesapla devam eder.
          </p>

          <div className="mt-10 grid gap-5 sm:grid-cols-2">
            {ALANLAR.map((alan) => {
              const r = RENK_SINIF[alan.renk];
              return (
                <div key={alan.baslik} className="card p-7">
                  <h3 className={`text-xl font-black ${r.text}`}>{alan.baslik}</h3>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {alan.konular.map((k) => (
                      <span
                        key={k}
                        className={`rounded-xl ${r.bg} px-3 py-1.5 text-sm font-bold text-slate-700`}
                      >
                        {k}
                      </span>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ---------------- Ebeveyn paneli ---------------- */}
      <section className="py-16">
        <div className="mx-auto max-w-6xl px-5">
          <div className="grid items-center gap-10 lg:grid-cols-2">
            <div>
              <span className="inline-block rounded-full bg-brand-50 px-4 py-1.5 text-sm font-extrabold text-brand-700">
                Ebeveyn paneli
              </span>
              <h2 className="mt-5 text-3xl font-black tracking-tight text-slate-800 sm:text-4xl">
                Çocuğunuzun nerede zorlandığını görün
              </h2>
              <p className="mt-5 text-lg font-semibold leading-relaxed text-slate-600">
                Hangi konuda ilerlediğini, hangisinde takıldığını ve günlük
                çalışma geçmişini panelden takip edebilirsiniz. Panel dört haneli
                bir PIN ile korunur — çocuk kendi başına giremez.
              </p>

              <ul className="mt-6 space-y-3">
                {[
                  'Konu konu ilerleme ve zorlanılan başlıklar',
                  'Günlük çalışma geçmişi',
                  'Birden fazla çocuk için ayrı profil',
                  'PIN korumalı erişim',
                ].map((m) => (
                  <li key={m} className="flex items-start gap-3">
                    <span className="mt-0.5 grid h-6 w-6 shrink-0 place-items-center rounded-full bg-mint-400/20 text-sm font-black text-mint-600">
                      ✓
                    </span>
                    <span className="text-base font-semibold text-slate-700">{m}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="card p-7">
              <p className="text-sm font-extrabold uppercase tracking-wide text-slate-400">
                Bu hafta
              </p>
              <div className="mt-5 space-y-4">
                {[
                  { k: 'Toplama–Çıkarma', d: 'İyi gidiyor', p: 88, renk: 'bg-mint-500' },
                  { k: 'Çarpım Tablosu', d: 'Pratik sürüyor', p: 54, renk: 'bg-sun-500' },
                  { k: 'Noktalama', d: 'Desteğe ihtiyacı var', p: 31, renk: 'bg-coral-500' },
                ].map((x) => (
                  <div key={x.k}>
                    <div className="flex items-baseline justify-between">
                      <span className="font-extrabold text-slate-800">{x.k}</span>
                      <span className="text-sm font-bold text-slate-500">{x.d}</span>
                    </div>
                    <div className="mt-2 h-3 overflow-hidden rounded-full bg-slate-100">
                      <div className={`h-full rounded-full ${x.renk}`} style={{ width: `${x.p}%` }} />
                    </div>
                  </div>
                ))}
              </div>
              <p className="mt-6 text-sm font-bold text-slate-400">
                Örnek görünümdür.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ---------------- Ödül sistemi ---------------- */}
      <section className="border-y border-slate-100 bg-white py-16">
        <div className="mx-auto max-w-6xl px-5">
          <h2 className="text-center text-3xl font-black tracking-tight text-slate-800 sm:text-4xl">
            Motivasyon baskıyla değil, birikimle
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-center text-lg font-semibold text-slate-600">
            Çocuk çalıştıkça yıldız kazanır, rozet toplar ve kendi odasını
            eşyalarla düzenler. Kaybedilen bir şey yok — yalnızca biriken bir şey var.
          </p>

          <div className="mt-10 grid gap-5 sm:grid-cols-3">
            {[
              { b: 'Yıldızlar', m: 'Tamamlanan görevlerden biriken puanlar.' },
              { b: 'Rozetler', m: 'Konu tamamlama ve düzenli çalışma rozetleri.' },
              { b: 'Kendi odası', m: 'Kazandığı eşyalarla düzenlediği kişisel alan.' },
            ].map((x) => (
              <div key={x.b} className="card p-7 text-center">
                <p className="text-xl font-black text-slate-800">{x.b}</p>
                <p className="mt-2 text-base font-semibold leading-relaxed text-slate-600">
                  {x.m}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ---------------- SSS ---------------- */}
      <section className="py-16">
        <div className="mx-auto max-w-3xl px-5">
          <h2 className="text-center text-3xl font-black tracking-tight text-slate-800 sm:text-4xl">
            Sık sorulanlar
          </h2>

          <div className="mt-10 space-y-4">
            {SSS.map((x) => (
              <details key={x.s} className="card group p-6">
                <summary className="cursor-pointer list-none text-lg font-black text-slate-800 marker:hidden">
                  <span className="flex items-center justify-between gap-4">
                    {x.s}
                    <span className="shrink-0 text-2xl font-black text-brand-400 transition-transform group-open:rotate-45">
                      +
                    </span>
                  </span>
                </summary>
                <p className="mt-4 text-base font-semibold leading-relaxed text-slate-600">
                  {x.c}
                </p>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* ---------------- Kapanış CTA ---------------- */}
      <section className="px-5 pb-20">
        <div className="mx-auto max-w-4xl rounded-3xl bg-brand-500 px-8 py-14 text-center shadow-xl shadow-brand-500/25">
          <h2 className="text-3xl font-black tracking-tight text-white sm:text-4xl">
            Bugün kısa bir görevle başlayın
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-lg font-semibold text-brand-50">
            Kayıt için e-posta yeterli. Çocuğunuz için profil oluşturun, ilk
            görev birkaç dakikada bitsin.
          </p>
          <Link
            href="/giris"
            className="btn mt-8 bg-white px-8 text-lg text-brand-600 shadow-lg hover:bg-brand-50"
          >
            Ücretsiz başla
          </Link>
        </div>
      </section>

      {/* ---------------- Footer ---------------- */}
      <footer className="border-t border-slate-100 bg-white py-10">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-5 sm:flex-row">
          <div className="flex items-center gap-2">
            <div className="grid h-8 w-8 place-items-center rounded-xl bg-brand-500 text-base font-black text-white">
              M
            </div>
            <span className="font-black text-slate-700">Minizeki</span>
          </div>
          <p className="text-sm font-bold text-slate-400">
            1–4. sınıf için günlük kısa tekrar
          </p>
          <Link href="/giris" className="text-sm font-extrabold text-brand-600 hover:text-brand-700">
            Giriş yap →
          </Link>
        </div>
      </footer>
    </main>
  );
}
