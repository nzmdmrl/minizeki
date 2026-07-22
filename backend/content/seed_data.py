"""
1. ve 2. sinif kategorileri, rozetler, Zeki'nin Evi esyalari.

MUFREDAT NOTU:
  - 1-2. sinifta FEN BILIMLERI YOKTUR -> Hayat Bilgisi vardir
  - 2. sinifta BOLME YOKTUR -> 3. siniftan itibaren
  - 2. sinifta carpim SADECE 1-5 tablosu
  - Ingilizce 2. siniftan itibaren
"""

# (id, ad, ders, ikon, sinif_min, sinif_max, prosedurel, generator, ust_sinif_var, ucretsiz, sira)
CATEGORIES = [
    # ---------------- MATEMATIK ----------------
    ("sayilar",          "Sayılar",            "matematik", "🔢", 1, 4, True,  "sayilar",          True,  True,  10),
    ("sayma",            "Sayalım",            "matematik", "🍎", 1, 2, True,  "sayma",            True,  True,  11),
    ("toplama_cikarma",  "Toplama–Çıkarma",    "matematik", "➕", 1, 4, True,  "toplama_cikarma",  True,  True,  12),
    ("carpim",           "Çarpım Tablosu",     "matematik", "✖️", 2, 4, True,  "carpim",           True,  True,  13),
    ("basamak",          "Basamak Değeri",     "matematik", "🏗️", 1, 4, True,  "basamak",          True,  False, 14),
    ("ritmik",           "Ritmik Sayma",       "matematik", "🎵", 1, 4, True,  "ritmik",           True,  False, 15),
    ("saat",             "Saat Okuma",         "matematik", "🕐", 2, 4, True,  "saat",             True,  True,  16),
    ("para",             "Para Hesabı",        "matematik", "💰", 2, 4, True,  "para",             True,  False, 17),
    ("oruntu",           "Örüntü",             "matematik", "🔷", 1, 4, True,  "oruntu",           True,  False, 18),
    ("geometri",         "Geometrik Şekiller", "matematik", "📐", 1, 4, False, None,               True,  False, 19),

    # ---------------- TURKCE ----------------
    ("hece",             "Hece Sayısı",        "turkce", "📝", 1, 3, True,  "hece",       True,  True,  20),
    ("alfabetik",        "Alfabetik Sıralama", "turkce", "🔤", 1, 4, True,  "alfabetik",  True,  False, 21),
    ("eksik_harf",       "Eksik Harf",         "turkce", "❓", 1, 3, True,  "eksik_harf", True,  False, 22),
    ("sesli_harf",       "Sesli Harfler",      "turkce", "🅰️", 1, 2, True,  "sesli_harf", True,  False, 23),
    ("anagram",          "Karışık Harfler",    "turkce", "🔀", 2, 4, True,  "anagram",    True,  False, 24),
    ("es_anlamli",       "Eş Anlamlı",         "turkce", "🟰", 2, 4, False, None,         True,  True,  25),
    ("zit_anlamli",      "Zıt Anlamlı",        "turkce", "↔️", 2, 4, False, None,         True,  True,  26),
    ("dogru_yazilis",    "Doğru Yazılış",      "turkce", "✍️", 1, 4, False, None,         True,  False, 27),
    ("noktalama",        "Noktalama",          "turkce", "❗", 2, 4, False, None,         True,  False, 28),

    # ---------------- HAYAT BILGISI (1-3. sinif) ----------------
    ("okulumuz",         "Okulumuz",           "hayat_bilgisi", "🏫", 1, 3, False, None, True,  False, 30),
    ("ailemiz",          "Ailemiz ve Evimiz",  "hayat_bilgisi", "🏠", 1, 3, False, None, True,  False, 31),
    ("sagligimiz",       "Sağlığımız",         "hayat_bilgisi", "🩺", 1, 3, False, None, True,  True,  32),
    ("guvenligimiz",     "Güvenliğimiz",       "hayat_bilgisi", "🚦", 1, 3, False, None, True,  False, 33),
    ("ulkemiz",          "Ülkemiz ve Atatürk", "hayat_bilgisi", "🇹🇷", 1, 3, False, None, True,  False, 34),
    ("doga_cevre",       "Doğa ve Çevre",      "hayat_bilgisi", "🌳", 1, 3, False, None, True,  False, 35),

    # ---------------- INGILIZCE (2. siniftan) ----------------
    ("ing_kelime",       "İngilizce Kelimeler", "ingilizce", "🔠", 2, 4, False, None, True, False, 40),
    ("ing_ifade",        "İngilizce İfadeler",  "ingilizce", "💬", 2, 4, False, None, True, False, 41),
]


# (id, ad, ikon, aciklama)
BADGES = [
    ("ilk_adim",           "İlk Adım",            "🌱", "İlk günlük görevini tamamladın"),
    ("haftalik_kahraman",  "Haftalık Kahraman",   "🔥", "7 gün üst üste oynadın"),
    ("aylik_efsane",       "Aylık Efsane",        "⭐", "30 gün üst üste oynadın"),
    ("mukemmel_gun",       "Mükemmel Gün",        "💯", "Günlük görevde hiç hata yapmadın"),
    ("merakli",            "Meraklı",             "🧭", "10 farklı kategoride oynadın"),
    ("matematik_ustasi",   "Matematik Ustası",    "🧮", "Tüm matematik kategorilerinde Altın"),
    ("kelime_avcisi",      "Kelime Avcısı",       "📖", "Tüm Türkçe kategorilerinde Altın"),
    ("kasif",              "Kâşif",               "🌍", "Tüm Hayat Bilgisi kategorilerinde Altın"),
    ("odaklanmis",         "Odaklanmış",          "🎯", "Bir odak haftasını tamamladın"),
    ("zeki_dostu",         "Zeki'nin Dostu",      "🦉", "Zeki'nin evini tamamen döşedin"),
]


# (id, ad, kategori, fiyat, ikon, sira)
HOUSE_ITEMS = [
    # Mobilya
    ("halı",       "Halı",           "mobilya", 15, "🟫", 1),
    ("sandalye",   "Sandalye",       "mobilya", 20, "🪑", 2),
    ("masa",       "Masa",           "mobilya", 25, "🪵", 3),
    ("koltuk",     "Koltuk",         "mobilya", 30, "🛋️", 4),
    ("yatak",      "Yatak",          "mobilya", 35, "🛏️", 5),
    ("kitaplik",   "Kitaplık",       "mobilya", 45, "📚", 6),
    ("dolap",      "Dolap",          "mobilya", 50, "🗄️", 7),

    # Dekor
    ("bitki",      "Saksı Bitkisi",  "dekor", 15, "🪴", 10),
    ("lamba",      "Lamba",          "dekor", 20, "💡", 11),
    ("saat_duvar", "Duvar Saati",    "dekor", 25, "🕰️", 12),
    ("poster",     "Poster",         "dekor", 25, "🖼️", 13),
    ("ayna",       "Ayna",           "dekor", 30, "🪞", 14),
    ("mum",        "Mum",            "dekor", 15, "🕯️", 15),
    ("cicek",      "Çiçek Vazosu",   "dekor", 35, "💐", 16),
    ("tablo",      "Tablo",          "dekor", 40, "🎨", 17),

    # Ozel
    ("gitar",      "Gitar",          "ozel", 80,  "🎸", 20),
    ("akvaryum",   "Akvaryum",       "ozel", 100, "🐠", 21),
    ("teleskop",   "Teleskop",       "ozel", 120, "🔭", 22),
    ("piyano",     "Piyano",         "ozel", 140, "🎹", 23),
    ("roket",      "Roket Maketi",   "ozel", 150, "🚀", 24),

    # Nadir
    ("dinozor",    "Dinozor İskeleti", "nadir", 200, "🦖", 30),
    ("uzay_ist",   "Uzay İstasyonu",   "nadir", 250, "🛸", 31),
    ("kale",       "Şato Maketi",      "nadir", 300, "🏰", 32),
]
