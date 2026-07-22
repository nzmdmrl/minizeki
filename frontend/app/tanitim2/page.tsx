'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';

/**
 * /tanitim2 — Alternatif tanitim sayfasi
 *
 * MEVCUT SAYFADAN FARKI:
 *   1. Guncel rakamlar (1.422 soru / 44 konu — eskisinde 809/27 yaziyordu)
 *   2. Fen ve Sosyal Bilgiler kategorileri dahil
 *   3. Ana mesaj degisti: "baskı yok" (savunmaci) yerine
 *      "sistem cocugu taniyor ve kendini ona gore ayarliyor" (farklilastirici)
 *
 * TASARIM YONU: Cizgili okul defteri. Urunun kendi dunyasindan —
 * kurşun kalem grisi, defter mavisi, ogretmen kirmizisi.
 *
 * IMZA OGE: Canli seviye haritasi. Kategori bazli uyarlamayi
 * gorsel olarak anlatir; hicbir rakipte olmayan ozellik.
 */

const GIRIS = '/giris';

// ---------------------------------------------------------------- Veri

const DERSLER = [
  {
    ad: 'Matematik', renk: '#2563eb', sinif: '1–4',
    konular: ['Sayılar', 'Sayalım', 'Toplama–Çıkarma', 'Çarpım Tablosu', 'Bölme',
              'Basamak Değeri', 'Ritmik Sayma', 'Saat Okuma', 'Para Hesabı',
              'Kesirler', 'Örüntü', 'Geometrik Şekiller'],
  },
  {
    ad: 'Türkçe', renk: '#059669', sinif: '1–4',
    konular: ['Hece Sayısı', 'Alfabetik Sıralama', 'Eksik Harf', 'Sesli Harfler',
              'Karışık Harfler', 'Eş Anlamlı', 'Zıt Anlamlı', 'Doğru Yazılış',
              'Noktalama'],
  },
  {
    ad: 'Hayat Bilgisi', renk: '#d97706', sinif: '1–3',
    konular: ['Okulumuz', 'Ailemiz ve Evimiz', 'Sağlığımız', 'Güvenliğimiz',
              'Ülkemiz ve Atatürk', 'Doğa ve Çevre'],
  },
  {
    ad: 'Fen Bilimleri', renk: '#7c3aed', sinif: '3–4',
    konular: ['Dünya ve Gökyüzü', 'Duyu Organları', 'Hareket ve Kuvvet',
              'Madde ve Özellikleri', 'Canlılar ve Yaşam', 'Işık ve Ses',
              'Elektrik', 'Beslenme ve Sindirim'],
  },
  {
    ad: 'Sosyal Bilgiler', renk: '#dc2626', sinif: '4',
    konular: ['Kimlik ve Haklarımız', 'Atatürk ve Tarihimiz', 'Türkiye Coğrafyası',
              'Buluşlar ve Teknoloji', 'Ekonomi ve Meslekler', 'Vatandaşlık',
              'Dünya Ülkeleri'],
  },
  {
    ad: 'İngilizce', renk: '#0891b2', sinif: '2–4',
    konular: ['İngilizce Kelimeler', 'İngilizce İfadeler'],
  },
];

// Imza ogenin verisi: 2. sinif bir cocugun gercekci seviye dagilimi
const HARITA = [
  { ad: 'Çarpım Tablosu', ders: 'Matematik', seviye: 3, oran: 88 },
  { ad: 'Toplama–Çıkarma', ders: 'Matematik', seviye: 3, oran: 93 },
  { ad: 'Saat Okuma', ders: 'Matematik', seviye: 2, oran: 79 },
  { ad: 'Eş Anlamlı', ders: 'Türkçe', seviye: 2, oran: 71 },
  { ad: 'Doğru Yazılış', ders: 'Türkçe', seviye: 1, oran: 58 },
  { ad: 'Sağlığımız', ders: 'Hayat Bilgisi', seviye: 2, oran: 85 },
];

const SSS = [
  {
    s: 'Çocuğumun seviyesini ben mi ayarlayacağım?',
    c: 'Hayır. Kayıtta yalnızca sınıfını seçersiniz. Gerisini sistem kendi ' +
       'ayarlar: bir konuda zorlanırsa oradaki soruları kolaylaştırır ve alt ' +
       'sınıf tekrarını artırır, ustalaşırsa üst sınıf sorularını açar. ' +
       'Bu ayar her konu için ayrı yapılır.',
  },
  {
    s: 'Süre sınırı var mı?',
    c: 'Yok. Soruda geri sayan sayaç çalışmıyor. Çocuk istediği kadar ' +
       'düşünebilir. Doğru cevaptan sonra otomatik olarak sonraki soruya geçer; ' +
       'yanlış cevapta doğrusunu okuması için bekler.',
  },
  {
    s: 'Başka çocuklarla eşleşiyor mu?',
    c: 'Hayır. Sıralama tablosu, rakip eşleştirme, sohbet ve arkadaş ekleme ' +
       'yok. Çocuk uygulamada hiçbir yabancıyla karşılaşmaz.',
  },
  {
    s: 'Bir gün atlarsa ne olur?',
    c: 'Yıldızları, rozetleri ve ilerlemesi durur. Seri sayacı için ayda iki ' +
       'kez otomatik kullanılan bir hak var; o da biterse sayaç sıfırlanır ama ' +
       'başka hiçbir şey kaybolmaz.',
  },
  {
    s: 'Günde ne kadar sürüyor?',
    c: 'Günlük görev 16–20 soru, yaklaşık dört dakika. Çocuk isterse serbest ' +
       'oyunla devam edebilir. Panelden günlük süre limiti koyabilirsiniz.',
  },
  {
    s: 'Reklam veya uygulama içi satın alma var mı?',
    c: 'Yok. Çocuk ekranında hiçbir yerde fiyat, ödeme ekranı veya reklam ' +
       'görünmez. Ödeme yalnızca PIN korumalı ebeveyn panelinden yapılır.',
  },
  {
    s: 'Kaç çocuk için kullanabilirim?',
    c: 'Aile planında dört çocuğa kadar ayrı profil açabilirsiniz. Her profilin ' +
       'kendi seviyesi, ilerlemesi ve raporu olur.',
  },
];

// ---------------------------------------------------------------- Sayfa

export default function Tanitim2() {
  return (
    <div className="t2">
      <Nav />
      <Hero />
      <Fark />
      <SeviyeHaritasi />
      <Akis />
      <Mufredat />
      <Panel />
      <Odul />
      <Sorular />
      <Kapanis />
      <Footer />
      <Stiller />
    </div>
  );
}

/* ------------------------------------------------------------------ */

function Nav() {
  return (
    <header className="nav">
      <div className="wrap nav-in">
        <Link href="/" className="logo">
          <span className="logo-m">M</span>
          <span>Minizeki</span>
        </Link>
        <nav className="nav-links">
          <a href="#nasil">Nasıl çalışır</a>
          <a href="#konular">Konular</a>
          <a href="#sorular">Sorular</a>
        </nav>
        <Link href={GIRIS} className="btn btn-sm">Giriş yap</Link>
      </div>
    </header>
  );
}

function Hero() {
  return (
    <section className="hero">
      <div className="wrap hero-grid">
        <div>
          <p className="eyebrow">1–4. sınıf · MEB müfredatına göre</p>
          <h1>
            Çocuğunuz nerede zorlanıyorsa,
            <span className="vurgu"> sorular oraya kayar.</span>
          </h1>
          <p className="lead">
            Minizeki her gün dört dakikalık kısa bir görev verir. Hangi konuda
            takıldığını fark eder ve o konunun sorularını sessizce kolaylaştırır;
            ustalaştığı konuda ise bir üst sınıfın sorularını açar.
            Bu ayarı <strong>her konu için ayrı</strong> yapar — siz hiçbir şey
            değiştirmezsiniz.
          </p>
          <div className="cta-row">
            <Link href={GIRIS} className="btn">Ücretsiz başla</Link>
            <a href="#nasil" className="btn btn-ghost">Nasıl çalışır?</a>
          </div>
          <p className="mini">
            Kayıt için e-posta yeterli · Çocuk ekranında reklam ve ödeme yok
          </p>
        </div>

        <SoruKarti />
      </div>
    </section>
  );
}

function SoruKarti() {
  const [secili, setSecili] = useState<number | null>(null);
  const dogru = 1;

  return (
    <div className="demo">
      <div className="demo-ust">
        <span className="demo-kat">✖️ Çarpım Tablosu</span>
        <span className="demo-say">3 / 16</span>
      </div>
      <div className="demo-bar"><i style={{ width: '19%' }} /></div>

      <p className="demo-soru">6 × 7 = ?</p>

      <div className="demo-siklar">
        {['36', '42', '48', '54'].map((o, i) => {
          let k = 'demo-sik';
          if (secili !== null) {
            if (i === dogru) k += ' dogru';
            else if (i === secili) k += ' yanlis';
            else k += ' sonuk';
          }
          return (
            <button key={o} className={k} onClick={() => setSecili(i)}
                    disabled={secili !== null}>
              {o}
            </button>
          );
        })}
      </div>

      {secili === null ? (
        <p className="demo-not">Deneyin — sayaç çalışmıyor.</p>
      ) : secili === dogru ? (
        <p className="demo-not demo-iyi">Doğru. Bu konuda sorular biraz zorlaşacak.</p>
      ) : (
        <p className="demo-not">
          Doğrusu <strong>42</strong> — çocuğa da böyle gösterilir, ceza yok.
        </p>
      )}
    </div>
  );
}

function Fark() {
  const maddeler = [
    ['Sayaç yok', 'Soruda geri sayım çalışmaz. Düşünmek için süre sınırı yok.'],
    ['Sıralama yok', 'Başka çocuklarla karşılaştırma yapılmaz.'],
    ['Ceza yok', 'Yanlış cevapta puan gitmez, seri kırılınca kazandıkları durur.'],
    ['Etiket yok', 'Çocuk “3. sınıf sorusu” veya “seviye 4” yazısı görmez.'],
    ['Reklam yok', 'Çocuk ekranında fiyat, ödeme ve reklam bulunmaz.'],
    ['Ses yok', 'Sessiz çalışır. Sınıfta, otobüste, kütüphanede kullanılabilir.'],
  ];
  return (
    <section className="fark">
      <div className="wrap">
        <h2 className="h2">Küçük yaşta baskı, öğrenmeyi değil kaygıyı büyütür</h2>
        <p className="alt">
          Çoğu uygulama ilgiyi ayakta tutmak için sayaç, seri ve sıralama kullanır.
          Bunlar kısa vadede işe yarar, uzun vadede çocuğu kaçırır. Minizeki
          hiçbirini kullanmıyor.
        </p>
        <ul className="fark-liste">
          {maddeler.map(([b, a]) => (
            <li key={b}>
              <span className="fark-b">{b}</span>
              <span className="fark-a">{a}</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

/* ---------------- IMZA OGE: canli seviye haritasi ---------------- */

function SeviyeHaritasi() {
  const [gorunur, setGorunur] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(
      ([e]) => e.isIntersecting && setGorunur(true),
      { threshold: 0.25 }
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return (
    <section className="harita" id="nasil" ref={ref}>
      <div className="wrap">
        <p className="eyebrow">Farkımız</p>
        <h2 className="h2">Tek bir seviye yok. Her konunun kendi seviyesi var.</h2>
        <p className="alt">
          Aşağıdaki tablo 2. sınıf bir çocuğun altı haftalık gerçek dağılımına
          benziyor. Matematikte bir üst sınıfın soruları açılmışken, doğru
          yazılışta hâlâ birinci sınıf tekrarı geliyor. Bunun için hiçbir ayar
          yapılmadı.
        </p>

        <div className="harita-kutu">
          {HARITA.map((k, i) => (
            <div className="satir" key={k.ad}
                 style={{ transitionDelay: `${i * 90}ms` }}>
              <div className="satir-ad">
                <span className="satir-baslik">{k.ad}</span>
                <span className="satir-ders">{k.ders}</span>
              </div>

              <div className="satir-cizgi">
                {[1, 2, 3].map((s) => (
                  <span key={s} className={`nokta ${gorunur && k.seviye >= s ? 'dolu' : ''}`}
                        style={{ transitionDelay: `${i * 90 + s * 70}ms` }} />
                ))}
                <em className="satir-etiket">
                  {k.seviye === 1 && 'alt sınıf tekrarı ağırlıkta'}
                  {k.seviye === 2 && 'kendi sınıfında'}
                  {k.seviye === 3 && 'üst sınıf soruları açıldı'}
                </em>
              </div>

              <div className="satir-oran">
                <div className="oran-bar">
                  <i style={{ width: gorunur ? `${k.oran}%` : '0%',
                              transitionDelay: `${i * 90}ms` }} />
                </div>
                <span>%{k.oran}</span>
              </div>
            </div>
          ))}
        </div>

        <p className="mini harita-not">
          Sistem her konuda doğruluğu %75–85 arasında tutmayı hedefler. Bu aralık,
          çocuğun zorlandığını hissettiği ama yapabildiği yerdir; altında
          yılgınlık, üstünde sıkılma başlar.
        </p>
      </div>
    </section>
  );
}

function Akis() {
  const adimlar = [
    ['Sekiz soruluk tanışma',
     'Çocuk oyuna başlar gibi başlar. Puan gösterilmez, not verilmez — sistem ' +
     'yalnızca nereden başlayacağını anlar.'],
    ['Her gün dört dakika',
     'Günlük görev 16–20 soru. Sekiz farklı konudan karışık gelir; çünkü tek ' +
     'konuya gömülmek kısa vadede kolay, uzun vadede daha az kalıcıdır.'],
    ['Zorlandığı konu geri gelir',
     'Yanlış yaptığı konu ertesi gün yine karşısına çıkar, ama daha kolay ' +
     'sorularla. Bildiği konu seyrekleşir ve zorlaşır.'],
  ];
  return (
    <section className="akis">
      <div className="wrap">
        <h2 className="h2">Günlük akış</h2>
        <ol className="akis-liste">
          {adimlar.map(([b, a], i) => (
            <li key={b}>
              <span className="akis-no">{i + 1}</span>
              <div>
                <h3>{b}</h3>
                <p>{a}</p>
              </div>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}

function Mufredat() {
  const [acik, setAcik] = useState<string | null>('Matematik');
  return (
    <section className="mufredat" id="konular">
      <div className="wrap">
        <div className="mufredat-ust">
          <div>
            <h2 className="h2">44 konu, 1.422 soru</h2>
            <p className="alt">
              Konular MEB müfredatına göre açılır. Birinci sınıfta Fen yoktur,
              üçüncü sınıfta başlar. İkinci sınıfta bölme yoktur. Sosyal Bilgiler
              dördüncü sınıfta gelir. Sistem bunu bilir ve sınıfa uymayan soruyu
              göstermez.
            </p>
          </div>
          <div className="sayilar">
            <div><b>44</b><span>konu</span></div>
            <div><b>1.422</b><span>hazır soru</span></div>
            <div><b>16</b><span>sınırsız üreten konu</span></div>
          </div>
        </div>

        <div className="dersler">
          {DERSLER.map((d) => {
            const ac = acik === d.ad;
            return (
              <div key={d.ad} className={`ders ${ac ? 'ac' : ''}`}
                   style={{ ['--c' as any]: d.renk }}>
                <button className="ders-bas" onClick={() => setAcik(ac ? null : d.ad)}
                        aria-expanded={ac}>
                  <span className="ders-ad">{d.ad}</span>
                  <span className="ders-sinif">{d.sinif}. sınıf</span>
                  <span className="ders-adet">{d.konular.length} konu</span>
                  <span className="ders-ok" aria-hidden>{ac ? '−' : '+'}</span>
                </button>
                {ac && (
                  <div className="ders-ic">
                    {d.konular.map((k) => <span key={k}>{k}</span>)}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <p className="mini">
          Çarpım tablosu, saat, para gibi 16 konuda sorular anlık üretilir —
          havuz tükenmez, aynı soru tekrar gelmez.
        </p>
      </div>
    </section>
  );
}

function Panel() {
  return (
    <section className="panel">
      <div className="wrap panel-grid">
        <div>
          <p className="eyebrow">Ebeveyn paneli · PIN korumalı</p>
          <h2 className="h2">Ne öğrendiğini değil, nerede takıldığını görün</h2>
          <p className="alt">
            Panel dört haneli bir PIN ile açılır; çocuk kendi başına giremez.
            Konu konu doğruluk oranını, hangi konunun kolaylaştırıldığını ve
            hangisinde üst sınıfa geçtiğini görürsünüz.
          </p>
          <ul className="panel-liste">
            <li>Konu bazlı doğruluk ve haftalık gelişim eğrisi</li>
            <li>Zorlandığı konularda ne yapıldığının açıklaması</li>
            <li>Günlük süre limiti (15 / 30 / 45 dakika)</li>
            <li>Ders ağırlığı — “bu ay matematiğe yüklenelim” diyebilirsiniz</li>
            <li>Odak modu — bir konuyu bir haftalığına öne çıkarır</li>
            <li>Dört çocuğa kadar ayrı profil</li>
          </ul>
        </div>

        <div className="rapor">
          <div className="rapor-ust">
            <span>Bu hafta</span><span className="rapor-pin">🔒 PIN</span>
          </div>
          {[
            ['Toplama–Çıkarma', 93, 'iyi'],
            ['Çarpım Tablosu', 88, 'iyi'],
            ['Saat Okuma', 79, 'orta'],
            ['Eş Anlamlı', 71, 'orta'],
            ['Doğru Yazılış', 58, 'dusuk'],
          ].map(([ad, o, d]) => (
            <div className="rapor-satir" key={ad as string}>
              <span className="rapor-ad">{ad}</span>
              <div className="rapor-bar">
                <i className={`b-${d}`} style={{ width: `${o}%` }} />
              </div>
              <span className={`rapor-oran o-${d}`}>%{o}</span>
            </div>
          ))}
          <p className="rapor-uyari">
            Doğru Yazılış’ta zorlanıyor. Bu konuda alt sınıf tekrarı
            artırıldı.
          </p>
          <p className="rapor-alt">Örnek görünüm</p>
        </div>
      </div>
    </section>
  );
}

function Odul() {
  return (
    <section className="odul">
      <div className="wrap">
        <h2 className="h2">Kaybedilen değil, biriken</h2>
        <p className="alt">
          Yıldız harcanır ama ceza olarak alınmaz. Can, enerji, geri sayım yok.
          Çocuk bir gün gelmezse ertesi gün kaldığı yerden devam eder.
        </p>
        <div className="odul-grid">
          {[
            ['⭐', 'Yıldız', 'Tamamlanan görevden kazanılır, harcanır — asla eksilmez.'],
            ['🏅', 'Rozet', 'Konu tamamlama ve düzenli çalışma rozetleri.'],
            ['🏠', 'Zeki’nin Evi', 'Kazandığı yıldızlarla maskotun odasını döşer.'],
            ['🛡️', 'Kalkan', 'Ayda iki kez, atlanan günü otomatik affeder.'],
          ].map(([i, b, a]) => (
            <div className="odul-kart" key={b as string}>
              <span className="odul-ikon" aria-hidden>{i}</span>
              <h3>{b}</h3>
              <p>{a}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Sorular() {
  const [acik, setAcik] = useState<number | null>(0);
  return (
    <section className="sss" id="sorular">
      <div className="wrap wrap-dar">
        <h2 className="h2">Sık sorulanlar</h2>
        <div className="sss-liste">
          {SSS.map((q, i) => {
            const ac = acik === i;
            return (
              <div key={q.s} className={`sss-oge ${ac ? 'ac' : ''}`}>
                <button onClick={() => setAcik(ac ? null : i)} aria-expanded={ac}>
                  <span>{q.s}</span>
                  <i aria-hidden>{ac ? '−' : '+'}</i>
                </button>
                {ac && <p>{q.c}</p>}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

function Kapanis() {
  return (
    <section className="kapanis">
      <div className="wrap wrap-dar">
        <h2>Bugün dört dakikayla başlayın</h2>
        <p>
          Çocuğunuz için profil oluşturun, kısa tanışma turunu yapsın.
          Sistem gerisini kendi ayarlar.
        </p>
        <Link href={GIRIS} className="btn btn-buyuk">Ücretsiz başla</Link>
        <p className="mini">Kredi kartı istenmez · İstediğiniz zaman silebilirsiniz</p>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="footer">
      <div className="wrap footer-in">
        <div className="logo">
          <span className="logo-m">M</span>
          <span>Minizeki</span>
        </div>
        <span className="footer-not">1–4. sınıf için günlük kısa tekrar</span>
        <Link href={GIRIS}>Giriş yap →</Link>
      </div>
    </footer>
  );
}

/* ------------------------------------------------------------------ */

function Stiller() {
  return (
    <style jsx global>{`
      /* Tasarim yonu: cizgili okul defteri.
         Kursun kalem grisi (#1e293b), defter mavisi (#2563eb),
         ogretmen kirmizisi (#dc2626), kagit (#fbfcfe). */

      .t2 {
        --kagit: #fbfcfe;
        --murekkep: #16233a;
        --soluk: #5b6a83;
        --cizgi: #dde5f0;
        --mavi: #2563eb;
        --kirmizi: #dc2626;
        --yesil: #059669;
        --sari: #f59e0b;
        --r: 14px;

        background: var(--kagit);
        color: var(--murekkep);
        font-family: 'Nunito', system-ui, sans-serif;
        line-height: 1.6;
      }
      .t2 * { box-sizing: border-box; }

      .wrap { max-width: 1120px; margin: 0 auto; padding: 0 24px; }
      .wrap-dar { max-width: 760px; }

      .t2 h1, .t2 h2, .t2 h3 { line-height: 1.15; margin: 0; letter-spacing: -0.02em; }
      .t2 p { margin: 0; }

      .h2 { font-size: clamp(26px, 3.4vw, 38px); font-weight: 900; }
      .alt {
        margin-top: 14px; max-width: 62ch;
        font-size: 17px; font-weight: 600; color: var(--soluk);
      }
      .eyebrow {
        font-size: 12px; font-weight: 900; letter-spacing: 0.12em;
        text-transform: uppercase; color: var(--mavi); margin-bottom: 12px;
      }
      .mini { margin-top: 14px; font-size: 13px; font-weight: 700; color: #93a3ba; }

      .btn {
        display: inline-flex; align-items: center; justify-content: center;
        min-height: 52px; padding: 0 26px; border-radius: 12px;
        background: var(--mavi); color: #fff; font-weight: 900; font-size: 16px;
        text-decoration: none; border: 2px solid var(--mavi);
        transition: transform .15s, box-shadow .15s, background .15s;
        box-shadow: 0 3px 0 #1d4ed8;
      }
      .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 0 #1d4ed8; }
      .btn:active { transform: translateY(1px); box-shadow: 0 1px 0 #1d4ed8; }
      .btn-sm { min-height: 42px; padding: 0 18px; font-size: 14px; box-shadow: 0 2px 0 #1d4ed8; }
      .btn-buyuk { min-height: 60px; padding: 0 36px; font-size: 18px; }
      .btn-ghost {
        background: transparent; color: var(--murekkep);
        border-color: var(--cizgi); box-shadow: none;
      }
      .btn-ghost:hover { border-color: var(--mavi); color: var(--mavi); box-shadow: none; }

      /* --- Nav --- */
      .nav {
        position: sticky; top: 0; z-index: 40;
        background: rgba(251,252,254,.92); backdrop-filter: blur(10px);
        border-bottom: 1px solid var(--cizgi);
      }
      .nav-in { display: flex; align-items: center; gap: 28px; padding-block: 14px; }
      .logo {
        display: flex; align-items: center; gap: 9px;
        font-weight: 900; font-size: 18px; color: var(--murekkep); text-decoration: none;
      }
      .logo-m {
        display: grid; place-items: center; width: 30px; height: 30px;
        border-radius: 9px; background: var(--mavi); color: #fff; font-size: 16px;
      }
      .nav-links { display: flex; gap: 22px; margin-left: auto; }
      .nav-links a {
        font-size: 14px; font-weight: 800; color: var(--soluk); text-decoration: none;
      }
      .nav-links a:hover { color: var(--mavi); }

      /* --- Hero: defter cizgileri --- */
      .hero {
        padding: 68px 0 76px;
        background:
          repeating-linear-gradient(
            to bottom, transparent 0 35px, var(--cizgi) 35px 36px
          );
        border-bottom: 1px solid var(--cizgi);
      }
      .hero-grid {
        display: grid; grid-template-columns: 1.08fr .92fr;
        gap: 56px; align-items: center;
      }
      .hero h1 {
        font-size: clamp(34px, 5vw, 54px); font-weight: 900;
      }
      .vurgu {
        color: var(--mavi);
        /* Ogretmen kalemi gibi alti cizili */
        background-image: linear-gradient(transparent 62%, rgba(37,99,235,.18) 0);
      }
      .lead {
        margin-top: 20px; max-width: 56ch;
        font-size: 17px; font-weight: 600; color: var(--soluk);
      }
      .lead strong { color: var(--murekkep); }
      .cta-row { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px; }

      /* --- Demo karti --- */
      .demo {
        background: #fff; border: 2px solid var(--cizgi);
        border-radius: 20px; padding: 22px;
        box-shadow: 0 18px 44px -26px rgba(22,35,58,.35);
      }
      .demo-ust {
        display: flex; justify-content: space-between; align-items: center;
        font-size: 12px; font-weight: 900; color: var(--soluk);
      }
      .demo-bar {
        height: 7px; border-radius: 99px; background: #eef2f8;
        margin: 10px 0 18px; overflow: hidden;
      }
      .demo-bar i { display: block; height: 100%; background: var(--mavi); border-radius: 99px; }
      .demo-soru { font-size: 30px; font-weight: 900; margin-bottom: 16px; }
      .demo-siklar { display: grid; gap: 9px; }
      .demo-sik {
        width: 100%; text-align: left; padding: 15px 18px;
        border: 2px solid var(--cizgi); border-radius: 12px; background: #fff;
        font: inherit; font-size: 18px; font-weight: 800; color: var(--murekkep);
        cursor: pointer; transition: .14s;
      }
      .demo-sik:hover:not(:disabled) { border-color: #a9c2f5; background: #f6f9ff; }
      .demo-sik:disabled { cursor: default; }
      .demo-sik.dogru { border-color: var(--yesil); background: #ecfdf5; color: var(--yesil); }
      .demo-sik.yanlis { border-color: var(--kirmizi); background: #fef2f2; color: var(--kirmizi); }
      .demo-sik.sonuk { opacity: .38; }
      .demo-not {
        margin-top: 14px; font-size: 13px; font-weight: 700; color: #93a3ba;
      }
      .demo-not.demo-iyi { color: var(--yesil); }
      .demo-not strong { color: var(--murekkep); }

      /* --- Fark --- */
      .fark { padding: 76px 0; }
      .fark-liste {
        list-style: none; margin: 34px 0 0; padding: 0;
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 0;
        border-top: 1px solid var(--cizgi); border-left: 1px solid var(--cizgi);
      }
      .fark-liste li {
        padding: 22px;
        border-right: 1px solid var(--cizgi); border-bottom: 1px solid var(--cizgi);
      }
      .fark-b {
        display: block; font-weight: 900; font-size: 17px; margin-bottom: 5px;
      }
      .fark-b::before { content: '—'; color: var(--kirmizi); margin-right: 8px; }
      .fark-a { font-size: 14px; font-weight: 600; color: var(--soluk); }

      /* --- IMZA: seviye haritasi --- */
      .harita { padding: 82px 0; background: #f4f7fc; border-block: 1px solid var(--cizgi); }
      .harita-kutu {
        margin-top: 34px; background: #fff;
        border: 2px solid var(--cizgi); border-radius: 18px; overflow: hidden;
      }
      .satir {
        display: grid; grid-template-columns: 200px 1fr 130px;
        gap: 18px; align-items: center;
        padding: 17px 22px; border-bottom: 1px solid var(--cizgi);
      }
      .satir:last-child { border-bottom: 0; }
      .satir-baslik { display: block; font-weight: 900; font-size: 15px; }
      .satir-ders { font-size: 12px; font-weight: 700; color: #93a3ba; }

      .satir-cizgi { display: flex; align-items: center; gap: 7px; }
      .nokta {
        width: 26px; height: 8px; border-radius: 99px; background: #e6ecf5;
        transition: background .45s ease;
      }
      .nokta.dolu { background: var(--mavi); }
      .satir-etiket {
        margin-left: 10px; font-size: 12px; font-weight: 800;
        font-style: normal; color: var(--soluk);
      }

      .satir-oran { display: flex; align-items: center; gap: 9px; }
      .oran-bar {
        flex: 1; height: 8px; border-radius: 99px; background: #eef2f8; overflow: hidden;
      }
      .oran-bar i {
        display: block; height: 100%; border-radius: 99px; background: var(--yesil);
        transition: width .9s cubic-bezier(.22,.61,.36,1);
      }
      .satir-oran span { font-size: 13px; font-weight: 900; min-width: 36px; text-align: right; }
      .harita-not { max-width: 66ch; }

      /* --- Akis --- */
      .akis { padding: 76px 0; }
      .akis-liste {
        list-style: none; margin: 34px 0 0; padding: 0;
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 26px;
      }
      .akis-liste li { display: flex; gap: 15px; }
      .akis-no {
        flex: none; display: grid; place-items: center;
        width: 34px; height: 34px; border-radius: 10px;
        background: var(--murekkep); color: #fff; font-weight: 900; font-size: 15px;
      }
      .akis-liste h3 { font-size: 17px; font-weight: 900; margin-bottom: 6px; }
      .akis-liste p { font-size: 14px; font-weight: 600; color: var(--soluk); }

      /* --- Mufredat --- */
      .mufredat { padding: 76px 0; background: #f4f7fc; border-block: 1px solid var(--cizgi); }
      .mufredat-ust {
        display: grid; grid-template-columns: 1.25fr .75fr; gap: 40px; align-items: end;
      }
      .sayilar { display: flex; gap: 26px; }
      .sayilar b { display: block; font-size: 30px; font-weight: 900; line-height: 1; }
      .sayilar span { font-size: 12px; font-weight: 800; color: var(--soluk); }

      .dersler { margin-top: 32px; display: grid; gap: 9px; }
      .ders {
        background: #fff; border: 2px solid var(--cizgi); border-radius: 14px;
        overflow: hidden; transition: border-color .18s;
      }
      .ders.ac { border-color: var(--c); }
      .ders-bas {
        width: 100%; display: flex; align-items: center; gap: 14px;
        padding: 16px 20px; background: none; border: 0; cursor: pointer;
        font: inherit; text-align: left;
      }
      .ders-ad {
        font-weight: 900; font-size: 17px;
        border-left: 4px solid var(--c); padding-left: 11px;
      }
      .ders-sinif {
        font-size: 12px; font-weight: 800; color: #fff; background: var(--c);
        padding: 3px 9px; border-radius: 99px;
      }
      .ders-adet { font-size: 13px; font-weight: 700; color: var(--soluk); }
      .ders-ok {
        margin-left: auto; font-size: 22px; font-weight: 900; color: var(--soluk);
        line-height: 1;
      }
      .ders-ic {
        display: flex; flex-wrap: wrap; gap: 7px;
        padding: 0 20px 18px 35px;
      }
      .ders-ic span {
        font-size: 13px; font-weight: 700; color: var(--soluk);
        background: #f4f7fc; border: 1px solid var(--cizgi);
        padding: 5px 11px; border-radius: 8px;
      }

      /* --- Panel --- */
      .panel { padding: 82px 0; }
      .panel-grid {
        display: grid; grid-template-columns: 1fr 1fr; gap: 52px; align-items: center;
      }
      .panel-liste { list-style: none; margin: 24px 0 0; padding: 0; display: grid; gap: 11px; }
      .panel-liste li {
        position: relative; padding-left: 26px;
        font-size: 15px; font-weight: 700; color: var(--soluk);
      }
      .panel-liste li::before {
        content: '✓'; position: absolute; left: 0;
        color: var(--yesil); font-weight: 900;
      }

      .rapor {
        background: #fff; border: 2px solid var(--cizgi); border-radius: 18px;
        padding: 22px; box-shadow: 0 18px 44px -28px rgba(22,35,58,.3);
      }
      .rapor-ust {
        display: flex; justify-content: space-between;
        font-size: 12px; font-weight: 900; color: var(--soluk);
        padding-bottom: 13px; border-bottom: 1px solid var(--cizgi); margin-bottom: 15px;
      }
      .rapor-satir {
        display: grid; grid-template-columns: 128px 1fr 44px;
        gap: 11px; align-items: center; margin-bottom: 11px;
      }
      .rapor-ad { font-size: 13px; font-weight: 800; }
      .rapor-bar { height: 8px; border-radius: 99px; background: #eef2f8; overflow: hidden; }
      .rapor-bar i { display: block; height: 100%; border-radius: 99px; }
      .b-iyi { background: var(--yesil); }
      .b-orta { background: var(--sari); }
      .b-dusuk { background: var(--kirmizi); }
      .rapor-oran { font-size: 12px; font-weight: 900; text-align: right; }
      .o-iyi { color: var(--yesil); } .o-orta { color: var(--sari); } .o-dusuk { color: var(--kirmizi); }
      .rapor-uyari {
        margin-top: 15px; padding: 11px 13px; border-radius: 10px;
        background: #fffbeb; border: 1px solid #fde68a;
        font-size: 13px; font-weight: 700; color: #92400e;
      }
      .rapor-alt { margin-top: 11px; font-size: 11px; font-weight: 700; color: #b6c2d3; }

      /* --- Odul --- */
      .odul { padding: 76px 0; background: #f4f7fc; border-block: 1px solid var(--cizgi); }
      .odul-grid {
        margin-top: 32px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;
      }
      .odul-kart {
        background: #fff; border: 2px solid var(--cizgi);
        border-radius: 14px; padding: 22px;
      }
      .odul-ikon { font-size: 28px; display: block; margin-bottom: 11px; }
      .odul-kart h3 { font-size: 16px; font-weight: 900; margin-bottom: 6px; }
      .odul-kart p { font-size: 13px; font-weight: 600; color: var(--soluk); }

      /* --- SSS --- */
      .sss { padding: 76px 0; }
      .sss-liste { margin-top: 28px; border-top: 1px solid var(--cizgi); }
      .sss-oge { border-bottom: 1px solid var(--cizgi); }
      .sss-oge button {
        width: 100%; display: flex; align-items: center; gap: 18px;
        padding: 19px 0; background: none; border: 0; cursor: pointer;
        font: inherit; font-size: 16px; font-weight: 800; text-align: left;
        color: var(--murekkep);
      }
      .sss-oge i {
        margin-left: auto; font-size: 22px; font-weight: 900;
        color: var(--soluk); font-style: normal; line-height: 1;
      }
      .sss-oge.ac i { color: var(--mavi); }
      .sss-oge p {
        padding: 0 40px 19px 0; font-size: 15px; font-weight: 600; color: var(--soluk);
      }

      /* --- Kapanis --- */
      .kapanis { padding: 88px 0; text-align: center; background: var(--murekkep); color: #fff; }
      .kapanis h2 { font-size: clamp(28px, 4vw, 40px); font-weight: 900; }
      .kapanis p { margin: 16px auto 28px; max-width: 46ch; font-weight: 600; color: #b3c0d4; }
      .kapanis .btn { background: #fff; color: var(--murekkep); border-color: #fff; box-shadow: 0 3px 0 #c7d3e6; }
      .kapanis .mini { color: #7e8ea6; }

      /* --- Footer --- */
      .footer { border-top: 1px solid var(--cizgi); padding: 26px 0; }
      .footer-in { display: flex; align-items: center; gap: 20px; }
      .footer-not { font-size: 13px; font-weight: 700; color: var(--soluk); }
      .footer a {
        margin-left: auto; font-size: 14px; font-weight: 800;
        color: var(--mavi); text-decoration: none;
      }

      /* --- Erisilebilirlik --- */
      .t2 a:focus-visible, .t2 button:focus-visible {
        outline: 3px solid var(--mavi); outline-offset: 3px; border-radius: 8px;
      }
      @media (prefers-reduced-motion: reduce) {
        .t2 *, .t2 *::before { transition: none !important; animation: none !important; }
      }

      /* --- Mobil --- */
      @media (max-width: 900px) {
        .hero-grid, .panel-grid, .mufredat-ust { grid-template-columns: 1fr; gap: 36px; }
        .fark-liste, .akis-liste { grid-template-columns: 1fr 1fr; }
        .odul-grid { grid-template-columns: 1fr 1fr; }
        .nav-links { display: none; }
      }
      @media (max-width: 620px) {
        .fark-liste, .akis-liste, .odul-grid { grid-template-columns: 1fr; }
        .satir { grid-template-columns: 1fr; gap: 9px; }
        .satir-oran { max-width: 220px; }
        .sayilar { flex-wrap: wrap; gap: 18px; }
        .hero { padding: 44px 0 52px; }
        .ders-bas { flex-wrap: wrap; gap: 9px; }
        .ders-ok { margin-left: 0; }
      }
    `}</style>
  );
}
