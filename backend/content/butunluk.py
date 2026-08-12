"""
BUTUNLUK KONTROLU

NEDEN VAR:
  Duzeltmeler ayri ayri zip'lerle dagitildi. Zip'ler yanlis sirayla
  acilirsa eski dosya yenisinin uzerine yazip bir duzeltmeyi SESSIZCE
  geri alabiliyor. Bu bir kez oldu: api-duzeltme.zip sonradan acilinca
  selection.py'deki tekrar duzeltmesi, main.py'deki reading router'i ve
  seed_data.py'deki okuma kategorisi kayboldu.

  Testler bunlarin bir kismini yakaladi ama hepsini yakalayamadi
  (orn. eksik router 404 verir, test o ucu hic denemiyorsa fark edilmez).

KULLANIM:
    python content/butunluk.py

Her deploy oncesi calistirin. Cikti "TUM DUZELTMELER YERINDE" degilse
push etmeyin.
"""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# (dosya, aranan_metin, aciklama)
KONTROLLER = [
    # --- main.py ---
    ("main.py", "reading.router",
     "Okuma modulu router'i bagli"),
    ("main.py", "semayi_guncelle",
     "Otomatik sema guncelleme (eksik kolon hatasi)"),
    ("main.py", "seed_stories",
     "Okuma metinleri otomatik yukleniyor"),
    ("main.py", "api_oneki_uyumu",
     "Traefik /api onek uyumu"),
    ("main.py", "public/stats",
     "Tanitim sayfasi canli rakamlar ucu"),
    ("main.py", "_otomatik_seed",
     "Deploy sonrasi otomatik seed"),

    # --- engine/selection.py ---
    ("engine/selection.py", "kullanilan_id",
     "Tur ici soru tekrari engellemesi"),
    ("engine/selection.py", "tur_ici",
     "Havuz sorgusunda tur ici filtre"),
    ("engine/selection.py", "sadece_gorev",
     "Okuma gunluk goreve girmiyor"),
    ("engine/selection.py", "if s is None or s.last_seen_at is None",
     "Kalibrasyonsuz profil bugu duzeltmesi"),

    # --- content/seed_data.py ---
    ("content/seed_data.py", '"okuma"',
     "Okuma ve Anlama kategorisi"),
    ("content/seed_data.py", "ilk_hikaye",
     "Okuma rozetleri"),
    ("content/seed_data.py", '"fen"',
     "Fen Bilimleri kategorileri (3-4. sinif)"),
    ("content/seed_data.py", '"sosyal"',
     "Sosyal Bilgiler kategorileri (4. sinif)"),

    # --- content/seed.py ---
    ("content/seed.py", "_metni_duzenle",
     "Metin satir kirilmasi duzeltmesi"),
    ("content/seed.py", "random.shuffle(karisik)",
     "Hikaye sorularinda sik karistirma"),
    ("content/seed.py", "aday.options[aday.answer_index] == dogru",
     "Duplicate kontrolu metin+cevap ciftiyle"),
    ("content/seed.py", "kaynakta",
     "Beklenen soru sayisi dogrulamasi"),

    # --- engine/rewards.py ---
    ("engine/rewards.py", "okuma_rozet_kontrol",
     "Okuma rozet mantigi"),

    # --- api/reading.py ---
    ("api/reading.py", "okuma_rozet_kontrol",
     "Okuma sonucunda rozet kontrolu cagriliyor"),
    ("api/reading.py", "MIN_KELIME_HIZ",
     "Kisa metinde hiz gosterilmiyor"),
    ("api/reading.py", "Story.grade_min == p.grade",
     "Kendi sinifina uygun metin onceligi"),

    # --- api/parent.py ---
    ("api/parent.py", "_okuma_ozeti",
     "Ebeveyn panelinde okuma bolumu"),

    # --- models ---
    ("models/__init__.py", "in_daily_quest",
     "Category.in_daily_quest alani"),
    ("models/__init__.py", "class ReadingSession",
     "Okuma oturumu modeli"),
    ("models/__init__.py", "is_admin",
     "Account.is_admin alani"),
    ("models/migrate.py", "semayi_guncelle",
     "Sema guncelleme fonksiyonu"),

    # --- Mola ---
    ("api/break_time.py", "calisma_saniyesi",
     "Calisma suresi olcumu"),
    ("api/break_time.py", "resumed",
     "Acik molaya devam (sayfa yenileme)"),
    ("main.py", "break_time.router",
     "Mola router'i bagli"),
    ("models/__init__.py", "class BreakSession",
     "Mola oturumu modeli"),
    ("models/__init__.py", "break_enabled",
     "Profile mola ayarlari"),
    ("api/parent.py", "_mola_ozeti",
     "Ebeveyn panelinde mola raporu"),
    ("api/parent.py", "study_minutes: int | None",
     "Mola ayarlari degistirilebiliyor"),
]


def main() -> int:
    print("=" * 66)
    print("BUTUNLUK KONTROLU")
    print("=" * 66)

    eksik = []
    dosya_yok = []
    son_dosya = None

    for dosya, metin, aciklama in KONTROLLER:
        yol = BASE / dosya
        if dosya != son_dosya:
            print(f"\n[{dosya}]")
            son_dosya = dosya

        if not yol.exists():
            print(f"  DOSYA YOK  {aciklama}")
            dosya_yok.append(dosya)
            continue

        icerik = yol.read_text(encoding="utf-8")
        if metin in icerik:
            print(f"  OK    {aciklama}")
        else:
            print(f"  EKSIK {aciklama}")
            eksik.append((dosya, aciklama))

    print("\n" + "=" * 66)
    if not eksik and not dosya_yok:
        print("TUM DUZELTMELER YERINDE")
        return 0

    if dosya_yok:
        print(f"{len(set(dosya_yok))} DOSYA BULUNAMADI:")
        for d in sorted(set(dosya_yok)):
            print(f"  - {d}")
    if eksik:
        print(f"{len(eksik)} DUZELTME KAYIP:")
        for d, a in eksik:
            print(f"  - {d}: {a}")
        print("\nMuhtemel sebep: bir zip yanlis sirayla acilip eski dosyayi")
        print("yenisinin uzerine yazmis. PUSH ETMEYIN.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
