# Minizeki

İlkokul (1–4. sınıf) için MEB müfredatına uygun eğitim oyunu platformu.

**Bu sürümde:** 1. ve 2. sınıf tam çalışır durumda. 3–4. sınıf altyapısı hazır, soru bankası eklendikçe açılır.

---

## Hızlı başlangıç

### Gereksinimler
- Python 3.11+
- Node.js 18+

### 1. Backend (port **8420**)

```bash
cd backend

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Veritabanını oluştur + kategoriler, sorular, rozetler, eşyalar
python content/seed.py

# Sunucuyu başlat
python main.py
```

Kontrol: http://localhost:8420/api/health
API dokümanı: http://localhost:8420/docs

### 2. Frontend (port **3420**)

```bash
cd frontend
npm install
npm run dev
```

Site: **http://localhost:3420**

---

## İlk kullanım

1. http://localhost:3420 → **Kayıt ol**
2. E-posta, şifre, **4 haneli ebeveyn PIN'i** (bu PIN raporu ve ayarları korur)
3. **Çocuk ekle** → ad, avatar, sınıf (1 veya 2)
4. **Tanışalım** → 8 soruluk kalibrasyon (çocuğa puan gösterilmez)
5. **BAŞLA** → günlük görev (16 soru, ~4 dakika)

Ebeveyn paneli: ana ekran → **Ebeveyn paneli** → PIN

---

## Portlar

| Servis | Port | Değiştirmek için |
|---|---|---|
| Backend | **8420** | `PORT=9000 python main.py` |
| Frontend | **3420** | `package.json` → `next dev -p XXXX` |

Frontend'in backend'i bulması için:
```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8420
```

---

## Veritabanı

Varsayılan **SQLite** (`backend/minizeki.db`) — kurulum gerektirmez.

PostgreSQL'e geçiş:
```bash
export DATABASE_URL="postgresql://kullanici:sifre@localhost:5432/minizeki"
python content/seed.py
python main.py
```

---

## Soru bankası

| Kaynak | Kategori | Soru |
|---|---|---|
| **Prosedürel** (algoritma üretir) | 14 | **Sınırsız** |
| **Yazılı** (bankada) | 13 | **348** |

Prosedürel kategoriler günlük görevin ~%50'sini karşılar ve **hiç tekrarlanmaz**.

### Yazılı soru dağılımı

| Kategori | Soru |
|---|---|
| Eş Anlamlı | 38 |
| Zıt Anlamlı | 36 |
| Doğru Yazılış | 32 |
| Noktalama | 31 |
| İngilizce Kelimeler | 30 |
| İngilizce İfadeler | 30 |
| Doğa ve Çevre | 26 |
| Geometrik Şekiller | 25 |
| Okulumuz / Ailemiz / Sağlığımız / Güvenliğimiz / Ülkemiz | 20'şer |

### Soru eklemek

`backend/content/sorular_*.py` dosyalarına ekleyin:

```python
# (band, sınıf_min, sınıf_max, soru, [şıklar], doğru_index, açıklama)
(2, 1, 3, "Bu şekil nedir?", ["Kare", "Üçgen", "Daire", "Dikdörtgen"], 0, "Kare"),
```

| Band | Hedef doğruluk |
|---|---|
| 1 | %90 (sınıfın tamamı çözer) |
| 2 | %75 |
| 3 | %60 |
| 4 | %40 |
| 5 | %20 (üst düzey) |

Sonra: `python content/seed.py` (idempotent — mevcut sorular atlanır)

---

## Testler

```bash
cd backend

# 96.000 prosedürel soru üretip doğrular
python content/validate_generators.py

# Uçtan uca API testi (52 kontrol)
python content/test_api.py

# Admin paneli testi (64 kontrol)
python content/test_admin.py

# 8 haftalık kullanım simülasyonu — zorluk motorunu doğrular
python content/simulate.py
```

Simülasyon çıktısı, motorun hedef bantta (%75–85) kalıp kalmadığını ölçer.

---

## Yapı

```
backend/
├── main.py                    FastAPI uygulaması
├── config.py                  Tüm ayarlar (port, eşikler, ödüller)
├── models/                    SQLAlchemy modelleri (13 tablo)
├── api/
│   ├── security.py            JWT + PIN + soru token'ı
│   ├── auth.py                Kayıt, giriş, PIN
│   ├── profile.py             Profil + kalibrasyon
│   ├── play.py                Günlük görev, serbest oyun, cevap
│   ├── parent.py              Rapor, ayarlar, odak modu
│   ├── house.py               Zeki'nin Evi
│   └── admin.py               ADMIN PANELİ API'si
├── engine/                    ZORLUK MOTORU
│   ├── level.py               Seviye, madalya, terfi/geri düşüş
│   ├── bands.py               Bant + spiral müfredat dağılımı
│   ├── selection.py           Kategori ve soru seçimi
│   ├── weights.py             Ders ağırlığı normalize
│   └── rewards.py             Yıldız, seri, kalkan, rozet
├── generators/                PROSEDÜREL ÜRETİM (18 üreteç)
│   ├── matematik.py           Hata modelleriyle çeldirici üretimi
│   ├── turkce.py
│   └── kelime_havuzu.py
└── content/
    ├── seed.py                Veritabanını doldur
    ├── seed_data.py           Kategoriler, rozetler, eşyalar
    ├── sorular_*.py           Yazılı soru bankası
    ├── make_admin.py           Hesaba admin yetkisi ver
    ├── migrate_admin.py        Mevcut DB'ye admin alanları ekle
    ├── validate_generators.py
    ├── test_api.py
    ├── test_admin.py
    └── simulate.py

frontend/
├── app/
│   ├── page.tsx               Ana ekran (tek buton)
│   ├── giris/                 Kayıt / giriş
│   ├── profil/yeni/           Çocuk ekle
│   ├── profil/[id]/tanisalim/ Kalibrasyon
│   ├── gorev/                 Günlük görev + sonuç
│   ├── oyna/[cat]/            Serbest oyun
│   ├── kategoriler/           Madalya ızgarası
│   ├── ev/                    Zeki'nin Evi
│   ├── ebeveyn/               PIN + rapor + ayarlar
│   └── admin/                 ADMİN PANELİ
│       ├── page.tsx           Genel bakış + sistem sağlığı
│       ├── kalibrasyon/       Gerçek zorluk kalibrasyonu
│       ├── sorular/           Soru CRUD + içe/dışa aktarma
│       ├── kategoriler/       Kategori yönetimi
│       ├── uretecler/         Prosedürel üreteç önizleme
│       ├── hesaplar/          Hesap + plan yönetimi
│       └── audit/             İşlem kaydı
├── components/
│   ├── QuestionPlayer.tsx     Oyunun kalbi
│   ├── Zeki.tsx               Maskot (SVG) + UI parçaları
│   └── admin/UI.tsx           Admin paneli ortak parçaları
└── lib/api.ts                 API istemcisi
```

---

## Tasarım kuralları (koda gömülü)

Bu kurallar ürünün temelidir; değiştirmeden önce iki kez düşünün.

| Kural | Nerede |
|---|---|
| **Kaybetme yok** — enerji/can yok, yıldız ceza olarak alınmaz | `engine/rewards.py` |
| **Seri kırılınca ceza yok** — yıldız, rozet, madalya korunur | `engine/rewards.py` |
| **Kalkan ücretsiz** — ayda 2 kez otomatik affeder | `config.SHIELD_PER_MONTH` |
| **Isınma kuralı** — turun ilk sorusu her zaman kolay | `engine/selection.py` |
| **Etiket yok** — çocuk "3. sınıf sorusu" görmez, "✨ Yeni sorular açıldı!" görür | `api/play.py` |
| **Süre tehdit değil** — kırmızı ekran/tik sesi/titreşim yok | `components/QuestionPlayer.tsx` |
| **Kalibrasyonda puan yok** — sadece "Harika! Hazırsın" | `profil/[id]/tanisalim` |
| **Cevap sızmaz** — doğru cevap istemciye gitmez, imzalı token'da | `api/security.py` |
| **Ses yok** — platform tamamen sessiz | — |
| **Rakip yok** — çocuk asla tanımadığı biriyle eşleşmez | — |
| **Reklam yok, çocuk para görmez** | — |

---

## Zorluk motoru

### Gizli seviye (çocuğa gösterilmez)
Her kategori için **ayrı** seviye tutulur (1–5):
- 3 doğru üst üste → level +1
- 2 yanlış üst üste → level −1

### Level → band eşlemesi

Hedef **%75–85 doğruluk** (yakınsal gelişim alanı). Bantların hedef doğruluğu band 3 = %60 olduğu için, level doğrudan band'a eşlenmez; bir kademe aşağı kaydırılır:

```
lvl 1 → band 1    lvl 2 → band 2    lvl 3 → band 2
lvl 4 → band 3    lvl 5 → band 4
```

Bu kalibrasyon simülasyonla doğrulanmıştır (`content/simulate.py`).

### Spiral müfredat (otomatik tekrar)

2. sınıf seçili bir çocuğun varsayılan dağılımı:

| Kaynak | Oran |
|---|---|
| 1. sınıf (tekrar) | %20 |
| 2. sınıf (ana kütle) | %70 |
| 3. sınıf | %10 — sadece terfi olan kategorilerde |

Zorlanınca tekrar %40'a çıkar, ustalaşınca %5'e iner. **Ebeveyn ayar yapmaz.**

### Terfi / geri düşüş

**Terfi** (üçü birden):
1. Kategori seviyesi 5
2. Son 20 soruda doğruluk ≥ %85
3. Toplam ≥ 40 soru

**Geri düşüş:** Son 8 soruda < %60 → oran %30'dan %10'a iner.
**Kilit asla kalkmaz** — çocuk "açtığım şeyi kaybettim" hissetmez.

---

## MEB müfredat notları

Bunlar `content/seed_data.py`'de zorlanır:

- **1–2. sınıfta Fen Bilimleri YOKTUR** → Hayat Bilgisi vardır
- **2. sınıfta bölme YOKTUR** → 3. sınıfta başlar
- **2. sınıfta çarpım sadece 1–5 tablosu** → 6–10 tablosu 3. sınıf
- **İngilizce 2. sınıftan** itibaren
- Sosyal Bilgiler yalnızca 4. sınıfta

`generators/matematik.py` içindeki `CARPIM_RANGE` bu sınırı kodda uygular.

---

## Ebeveyn ayarları

| Ayar | Var mı? | Neden |
|---|---|---|
| **Ders ağırlığı** (Az/Normal/Çok) | ✅ | Velinin bilgisi (karne, öğretmen). Sistem bunu bilemez. |
| **Odak modu** (1 kategori, 1 hafta) | ✅ | "Bu hafta çarpıma asılalım" |
| **Sınıf seviyesi** | ✅ | Eylül'de sınıf atlama |
| **Tekrar oranı** | ✅ | Az/Orta/Çok |
| **Günlük süre limiti** | ✅ | 15/30/45 dk |
| **Zorluk seviyesi** | ❌ | Sistem otomatik. Veliye verilirse bozar. |

Ders ağırlığı sınırları: hiçbir ders **%10 altına** inmez, hiçbiri **%45 üstüne** çıkmaz.

---

## Admin paneli

**http://localhost:3420/admin**

### Kurulum (2 adım)

Panel **iki koşul birden** ister — biri olmadan diğeri yetmez:

```bash
# 1. Hesabınıza admin yetkisi verin (önce siteden kayıt olun)
cd backend
source venv/bin/activate
python content/make_admin.py sizin@epostaniz.com

# 2. Sunucuyu admin şifresiyle başlatın
ADMIN_PASSWORD='guclu-bir-sifre' python main.py
```

`ADMIN_PASSWORD` ayarlı değilse panel **tamamen kapalıdır** (503 döner).

Mevcut bir kurulumu güncelliyorsanız önce:
```bash
python content/migrate_admin.py
```

Admin listesi: `python content/make_admin.py`
Yetki kaldırma: `python content/make_admin.py e-posta --remove`

### Sayfalar

| Sayfa | Ne işe yarar |
|---|---|
| **Genel bakış** | Kullanıcı/aktivite metrikleri, 14 günlük grafik, **sistem sağlığı** |
| **Kalibrasyon** | Yanlış banttaki soruları bulur ve düzeltir |
| **Sorular** | Ekle/düzenle/sil, filtre, toplu durum, içe/dışa aktarma |
| **Kategoriler** | Sınıf aralığı, ücretsiz/aile, terfi ayarı, zayıf banka uyarısı |
| **Üreteçler** | 18 prosedürel üretecin canlı önizlemesi |
| **Hesaplar** | Plan değiştir, admin yetkisi, profil istatistikleri |
| **İşlem kaydı** | Her admin işleminin denetim kaydı |

### Kalibrasyon — panelin en değerli parçası

Sistem her sorunun gerçek zorluğunu ölçer:

```
gerçek doğruluk = correct_count / serve_count
```

Bunu bandın hedefiyle karşılaştırır:

| Band | Hedef doğruluk |
|---|---|
| 1 | %90 |
| 2 | %75 |
| 3 | %60 |
| 4 | %40 |
| 5 | %20 |

Bir soru 30+ kez gösterildikten sonra sapma ±%20'yi geçerse **yanlış banttadır**.
Band 1'e (%90 hedef) konmuş ama gerçekte %20 doğrulanan bir soru, çocuğun
"kolay" sanılan soruda takılmasına ve doğruluğun hedef bandın (%75–85) dışına
çıkmasına yol açar.

Panel bunları listeler, doğru bandı önerir ve tek tıkla düzeltir.
**Bu ekran olmadan soru bankası zamanla bozulur.**

### Güvenlik

| Önlem | Nasıl |
|---|---|
| İki katmanlı erişim | `is_admin` bayrağı **+** `ADMIN_PASSWORD` |
| Ayrı token | Admin token'ı normal oturumdan bağımsız, 4 saat geçerli |
| Yetki yükseltme yok | Normal `access_token` admin uçlarına erişemez |
| Denetim kaydı | Her değiştiren işlem `audit_log`'a yazılır |
| Çocuk gizliliği | Panel çocukların **adını göstermez** — sadece istatistik |
| Kendini kilitleme koruması | Admin kendi yetkisini kaldıramaz |
| Veri bütünlüğü | Gösterilmiş soru silinemez (emekliye ayrılır) |
| İstatistik tutarlılığı | Soru metni değişirse istatistikler sıfırlanır |

---

## Üretim ortamı

```bash
# Backend
export SECRET_KEY="$(openssl rand -hex 32)"        # ZORUNLU
export ADMIN_PASSWORD="$(openssl rand -hex 16)"   # boşsa admin paneli kapalı
export DATABASE_URL="postgresql://..."
export FRONTEND_ORIGIN="https://minizeki.com"
gunicorn main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8420 -w 4

# Frontend
export NEXT_PUBLIC_API_URL="https://api.minizeki.com"
npm run build && npm start
```

**Deploy öncesi kontrol listesi:**
- [ ] `SECRET_KEY` değiştirildi (varsayılan kesinlikle kullanılmamalı)
- [ ] `ADMIN_PASSWORD` güçlü ve gizli
- [ ] Admin hesapları gözden geçirildi (`python content/make_admin.py`)
- [ ] PostgreSQL'e geçildi
- [ ] `FRONTEND_ORIGIN` gerçek domain
- [ ] HTTPS aktif
- [ ] `python content/seed.py` çalıştırıldı
- [ ] Günlük DB yedeği kuruldu

---

## Sonraki adımlar

| İş | Not |
|---|---|
| Soru bankası büyütme | 348 → 2.600 (2. sınıf tam) |
| 3–4. sınıf | Fen ve Sosyal Bilgiler kategorileri |
| Haftalık karne e-postası | Celery task — en güçlü tutundurma aracı |
| Ödeme (Iyzico) | Aile planı ₺79/ay · ₺590/yıl |
| Öğretmen paneli | Okul planı (B2B) |

---

## Lisans

Özel — tüm hakları saklıdır.
