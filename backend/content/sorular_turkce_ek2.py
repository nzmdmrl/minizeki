"""
1-2. SINIF EK SORULARI — Turkce, Geometri, Ingilizce (Parti 4).

ONCELIK: 1. sinif. Mevcut Turkce sorularinin cogu grade_min=2 idi;
1. sinif cocugu Es/Zit Anlamli kategorilerine hic erisemiyordu.
Bu dosya 1. sinif icin basit es/zit anlamli sorular ekler.

1. SINIF DIL KURALI:
  - Gunluk hayatta duydugu kelimeler
  - Soyut kavram yok (adalet, hosgoru gibi)
  - Kisa sik metinleri

Band hedef dogruluk: 1=%90  2=%75  3=%60  4=%40  5=%20
Format: (band, sinif_min, sinif_max, soru, [siklar], dogru_index, aciklama)
"""

# ==================================================== ES ANLAMLI (1. sinif)

ES_ANLAMLI_EK2 = [
    (1, 1, 4, '"Ev" yerine hangisini söyleyebiliriz?', ["Yuva", "Okul", "Bahçe", "Sokak"], 0, "Ev = Yuva"),
    (1, 1, 4, '"Güzel" yerine hangisini söyleyebiliriz?', ["Hoş", "Çirkin", "Kötü", "Zor"], 0, "Güzel = Hoş"),
    (1, 1, 4, '"Büyük" yerine hangisini söyleyebiliriz?', ["Kocaman", "Küçük", "İnce", "Kısa"], 0, "Büyük = Kocaman"),
    (1, 1, 4, '"Küçük" yerine hangisini söyleyebiliriz?', ["Ufak", "Büyük", "Uzun", "Geniş"], 0, "Küçük = Ufak"),
    (1, 1, 4, '"Hızlı" yerine hangisini söyleyebiliriz?', ["Çabuk", "Yavaş", "Ağır", "Durgun"], 0, "Hızlı = Çabuk"),
    (1, 1, 4, '"Sevinç" yerine hangisini söyleyebiliriz?', ["Mutluluk", "Üzüntü", "Korku", "Öfke"], 0, "Sevinç = Mutluluk"),
    (1, 1, 4, '"Yemek" yerine hangisini söyleyebiliriz?', ["Aş", "Su", "Ekmek", "Tabak"], 0, "Yemek = Aş"),
    (1, 1, 4, '"Yol" yerine hangisini söyleyebiliriz?', ["Cadde", "Ev", "Bahçe", "Oda"], 0, "Yol = Cadde"),
    (2, 1, 4, '"Sıcak" yerine hangisini söyleyebiliriz?', ["Kızgın", "Soğuk", "Buzlu", "Serin"], 0, "Sıcak = Kızgın (hava)"),
    (2, 1, 4, '"Zayıf" yerine hangisini söyleyebiliriz?', ["İnce", "Şişman", "Kalın", "Geniş"], 0, "Zayıf = İnce"),
    (2, 1, 4, '"Kırmızı" yerine hangisini söyleyebiliriz?', ["Al", "Mavi", "Yeşil", "Sarı"], 0, "Kırmızı = Al"),
    (2, 1, 4, '"Siyah" yerine hangisini söyleyebiliriz?', ["Kara", "Beyaz", "Gri", "Mavi"], 0, "Siyah = Kara"),
    (2, 1, 4, '"Beyaz" yerine hangisini söyleyebiliriz?', ["Ak", "Kara", "Mor", "Yeşil"], 0, "Beyaz = Ak"),
    (2, 1, 4, '"Okul" yerine hangisini söyleyebiliriz?', ["Mektep", "Ev", "Park", "Market"], 0, "Okul = Mektep"),
    (2, 1, 4, '"Hediye" yerine hangisini söyleyebiliriz?', ["Armağan", "Kutu", "Paket", "Süs"], 0, "Hediye = Armağan"),
    (2, 1, 4, '"Doktor" yerine hangisini söyleyebiliriz?', ["Hekim", "Hemşire", "Hasta", "İlaç"], 0, "Doktor = Hekim"),
    (1, 1, 4, '"Baş" yerine hangisini söyleyebiliriz?', ["Kafa", "El", "Ayak", "Göz"], 0, "Baş = Kafa"),
    (1, 1, 4, '"Ak" yerine hangisini söyleyebiliriz?', ["Beyaz", "Siyah", "Mavi", "Sarı"], 0, "Ak = Beyaz"),
    (1, 1, 4, '"Kara" yerine hangisini söyleyebiliriz?', ["Siyah", "Beyaz", "Kırmızı", "Yeşil"], 0, "Kara = Siyah"),
    (1, 1, 4, '"Al" yerine hangisini söyleyebiliriz?', ["Kırmızı", "Mavi", "Sarı", "Mor"], 0, "Al = Kırmızı"),
    (1, 1, 4, '"Kocaman" yerine hangisini söyleyebiliriz?', ["Çok büyük", "Küçük", "İnce", "Kısa"], 0, "Kocaman = Çok büyük"),
    (1, 1, 4, '"Ufak" yerine hangisini söyleyebiliriz?', ["Küçük", "Büyük", "Uzun", "Kalın"], 0, "Ufak = Küçük"),
    (2, 1, 4, '"Çabuk" yerine hangisini söyleyebiliriz?', ["Hızlı", "Yavaş", "Ağır", "Durgun"], 0, "Çabuk = Hızlı"),
    (2, 1, 4, '"Yuva" yerine hangisini söyleyebiliriz?', ["Ev", "Okul", "Bahçe", "Yol"], 0, "Yuva = Ev"),
    (2, 1, 4, '"Hoş" yerine hangisini söyleyebiliriz?', ["Güzel", "Çirkin", "Kötü", "Zor"], 0, "Hoş = Güzel"),
    (2, 1, 4, '"Mutluluk" yerine hangisini söyleyebiliriz?', ["Sevinç", "Üzüntü", "Korku", "Öfke"], 0, "Mutluluk = Sevinç"),
    (2, 1, 4, '"Aş" yerine hangisini söyleyebiliriz?', ["Yemek", "Su", "Tabak", "Kaşık"], 0, "Aş = Yemek"),
    (2, 1, 4, '"İnce" yerine hangisini söyleyebiliriz?', ["Zayıf", "Kalın", "Şişman", "Geniş"], 0, "İnce = Zayıf"),
]

# ==================================================== ZIT ANLAMLI (1. sinif)

ZIT_ANLAMLI_EK2 = [
    (1, 1, 4, '"Sıcak" kelimesinin tersi hangisidir?', ["Soğuk", "Ilık", "Serin", "Yumuşak"], 0, "Sıcak ↔ Soğuk"),
    (1, 1, 4, '"Büyük" kelimesinin tersi hangisidir?', ["Küçük", "Uzun", "Geniş", "Kalın"], 0, "Büyük ↔ Küçük"),
    (1, 1, 4, '"Uzun" kelimesinin tersi hangisidir?', ["Kısa", "İnce", "Dar", "Küçük"], 0, "Uzun ↔ Kısa"),
    (1, 1, 4, '"Gece" kelimesinin tersi hangisidir?', ["Gündüz", "Akşam", "Sabah", "Öğle"], 0, "Gece ↔ Gündüz"),
    (1, 1, 4, '"Açık" kelimesinin tersi hangisidir?', ["Kapalı", "Geniş", "Büyük", "Yeni"], 0, "Açık ↔ Kapalı"),
    (1, 1, 4, '"Aşağı" kelimesinin tersi hangisidir?', ["Yukarı", "İleri", "Geri", "Yan"], 0, "Aşağı ↔ Yukarı"),
    (1, 1, 4, '"Var" kelimesinin tersi hangisidir?', ["Yok", "Çok", "Az", "Bol"], 0, "Var ↔ Yok"),
    (1, 1, 4, '"Gel" kelimesinin tersi hangisidir?', ["Git", "Dur", "Otur", "Bekle"], 0, "Gel ↔ Git"),
    (2, 1, 4, '"Temiz" kelimesinin tersi hangisidir?', ["Kirli", "Düzenli", "Parlak", "Yeni"], 0, "Temiz ↔ Kirli"),
    (2, 1, 4, '"Dolu" kelimesinin tersi hangisidir?', ["Boş", "Ağır", "Büyük", "Geniş"], 0, "Dolu ↔ Boş"),
    (2, 1, 4, '"Yeni" kelimesinin tersi hangisidir?', ["Eski", "Temiz", "Güzel", "Büyük"], 0, "Yeni ↔ Eski"),
    (2, 1, 4, '"Ağır" kelimesinin tersi hangisidir?', ["Hafif", "Büyük", "Kalın", "Sert"], 0, "Ağır ↔ Hafif"),
    (2, 1, 4, '"Hızlı" kelimesinin tersi hangisidir?', ["Yavaş", "Çabuk", "Acele", "Ani"], 0, "Hızlı ↔ Yavaş"),
    (2, 1, 4, '"İçeri" kelimesinin tersi hangisidir?', ["Dışarı", "Yukarı", "Aşağı", "Yan"], 0, "İçeri ↔ Dışarı"),
    (2, 1, 4, '"Ön" kelimesinin tersi hangisidir?', ["Arka", "Sağ", "Sol", "Üst"], 0, "Ön ↔ Arka"),
    (2, 1, 4, '"Islak" kelimesinin tersi hangisidir?', ["Kuru", "Soğuk", "Sıcak", "Yumuşak"], 0, "Islak ↔ Kuru"),
    (1, 1, 4, '"Yukarı" kelimesinin tersi hangisidir?', ["Aşağı", "İleri", "Geri", "Yan"], 0, "Yukarı ↔ Aşağı"),
    (1, 1, 4, '"Git" kelimesinin tersi hangisidir?', ["Gel", "Dur", "Otur", "Koş"], 0, "Git ↔ Gel"),
    (1, 1, 4, '"Kapalı" kelimesinin tersi hangisidir?', ["Açık", "Dar", "Küçük", "Eski"], 0, "Kapalı ↔ Açık"),
    (1, 1, 4, '"Gündüz" kelimesinin tersi hangisidir?', ["Gece", "Sabah", "Öğle", "Akşam"], 0, "Gündüz ↔ Gece"),
    (1, 1, 4, '"Kısa" kelimesinin tersi hangisidir?', ["Uzun", "İnce", "Dar", "Küçük"], 0, "Kısa ↔ Uzun"),
    (1, 1, 4, '"Soğuk" kelimesinin tersi hangisidir?', ["Sıcak", "Ilık", "Serin", "Yumuşak"], 0, "Soğuk ↔ Sıcak"),
    (2, 1, 4, '"Kirli" kelimesinin tersi hangisidir?', ["Temiz", "Düzenli", "Yeni", "Parlak"], 0, "Kirli ↔ Temiz"),
    (2, 1, 4, '"Boş" kelimesinin tersi hangisidir?', ["Dolu", "Ağır", "Büyük", "Geniş"], 0, "Boş ↔ Dolu"),
    (2, 1, 4, '"Eski" kelimesinin tersi hangisidir?', ["Yeni", "Temiz", "Güzel", "Büyük"], 0, "Eski ↔ Yeni"),
    (2, 1, 4, '"Hafif" kelimesinin tersi hangisidir?', ["Ağır", "İnce", "Küçük", "Kısa"], 0, "Hafif ↔ Ağır"),
    (2, 1, 4, '"Yavaş" kelimesinin tersi hangisidir?', ["Hızlı", "Ağır", "Durgun", "Sakin"], 0, "Yavaş ↔ Hızlı"),
    (2, 1, 4, '"Dışarı" kelimesinin tersi hangisidir?', ["İçeri", "Yukarı", "Aşağı", "Yan"], 0, "Dışarı ↔ İçeri"),
    (2, 1, 4, '"Arka" kelimesinin tersi hangisidir?', ["Ön", "Sağ", "Sol", "Üst"], 0, "Arka ↔ Ön"),
    (2, 1, 4, '"Kuru" kelimesinin tersi hangisidir?', ["Islak", "Soğuk", "Sıcak", "Sert"], 0, "Kuru ↔ Islak"),
]

# ==================================================== DOGRU YAZILIS (1. sinif)

DOGRU_YAZILIS_EK2 = [
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["kapı", "kapu", "kappı", "gapı"], 0, "kapı"),
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["bebek", "babek", "bebbek", "bebbeg"], 0, "bebek"),
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["balık", "baluk", "ballık", "balig"], 0, "balık"),
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["kuş", "kus", "kuşş", "guş"], 0, "kuş"),
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["anne", "ane", "annne", "enne"], 0, "anne"),
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["baba", "bapa", "babba", "bebe"], 0, "baba"),
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["kedi", "gedi", "keddi", "kedu"], 0, "kedi"),
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["su", "zu", "suu", "sü"], 0, "su"),
    (2, 1, 4, "Hangisi doğru yazılmıştır?", ["çanta", "canta", "çannta", "şanta"], 0, "çanta"),
    (2, 1, 4, "Hangisi doğru yazılmıştır?", ["bardak", "bardag", "barrdak", "bartak"], 0, "bardak"),
    (2, 1, 4, "Hangisi doğru yazılmıştır?", ["yaprak", "yaprag", "yapprak", "yabrak"], 0, "yaprak"),
    (2, 1, 4, "Hangisi doğru yazılmıştır?", ["güneş", "gunes", "güneşş", "künes"], 0, "güneş"),
    (2, 1, 4, "Hangisi doğru yazılmıştır?", ["yıldız", "yildiz", "yılldız", "yıltız"], 0, "yıldız"),
    (2, 1, 4, "Hangisi doğru yazılmıştır?", ["deniz", "denız", "dennız", "teniz"], 0, "deniz"),
]

# ==================================================== GEOMETRI (1. sinif)

GEOMETRI_EK2 = [
    (1, 1, 4, "Hangisi yuvarlaktır?", ["Daire", "Kare", "Üçgen", "Dikdörtgen"], 0, "Daire yuvarlak"),
    (1, 1, 4, "Saat hangi şekle benzer?", ["Daire", "Kare", "Üçgen", "Yıldız"], 0, "Daire"),
    (1, 1, 4, "Kitap hangi şekle benzer?", ["Dikdörtgen", "Daire", "Üçgen", "Yıldız"], 0, "Dikdörtgen"),
    (1, 1, 4, "Top hangi şekle benzer?", ["Yuvarlak", "Kare", "Üçgen", "Köşeli"], 0, "Yuvarlak"),
    (1, 1, 4, "Çatı genelde hangi şekle benzer?", ["Üçgen", "Daire", "Kare", "Yıldız"], 0, "Üçgen"),
    (2, 1, 4, "Karenin bütün kenarları nasıldır?", ["Eşit", "Farklı", "İkisi uzun", "Üçü kısa"], 0, "Hepsi eşit"),
    (2, 1, 4, "Hangisi köşelidir?", ["Kare", "Daire", "Top", "Yumurta"], 0, "Kare köşelidir"),
    (2, 1, 4, "Tekerlek hangi şekildedir?", ["Daire", "Kare", "Üçgen", "Dikdörtgen"], 0, "Daire"),
]

# ==================================================== INGILIZCE (2. sinif temel)

ING_KELIME_EK2 = [
    (2, 2, 4, '"Pen" ne demektir?', ["Kalem", "Kitap", "Silgi", "Defter"], 0, "pen = kalem"),
    (2, 2, 4, '"Nose" ne demektir?', ["Burun", "Göz", "Kulak", "Ağız"], 0, "nose = burun"),
    (2, 2, 4, '"Mouth" ne demektir?', ["Ağız", "Burun", "Göz", "El"], 0, "mouth = ağız"),
    (2, 2, 4, '"Ear" ne demektir?', ["Kulak", "Göz", "Burun", "Ağız"], 0, "ear = kulak"),
    (2, 2, 4, '"Seven" ne demektir?', ["Yedi", "Altı", "Sekiz", "Dokuz"], 0, "seven = yedi"),
    (2, 2, 4, '"Eight" ne demektir?', ["Sekiz", "Yedi", "Dokuz", "On"], 0, "eight = sekiz"),
    (3, 2, 4, '"Nine" ne demektir?', ["Dokuz", "Sekiz", "On", "Yedi"], 0, "nine = dokuz"),
    (3, 2, 4, '"Orange" ne demektir?', ["Turuncu", "Mor", "Pembe", "Gri"], 0, "orange = turuncu"),
]

ING_IFADE_EK2 = [
    (1, 2, 4, '"Good morning" ne zaman söylenir?', ["Sabah", "Akşam", "Gece", "Öğlen"], 0, "Sabah selamı"),
    (1, 2, 4, '"Thank you" ne zaman söylenir?', ["Teşekkür ederken", "Selam verirken", "Vedalaşırken", "Özür dilerken"], 0, "Teşekkür"),
    (2, 2, 4, '"My name is..." ne demektir?', ["Benim adım...", "Senin adın...", "Onun adı...", "Bizim adımız..."], 0, "Kendini tanıtma"),
    (2, 2, 4, '"How are you?" sorusuna ne cevap verilir?', ["I am fine", "My name is Ali", "Thank you", "Goodbye"], 0, "Nasılsın → İyiyim"),
    (2, 2, 4, '"Yes" ve "No" ne demektir?', ["Evet ve Hayır", "Hayır ve Evet", "Belki ve Tamam", "Dur ve Git"], 0, "Yes = Evet, No = Hayır"),
    (3, 2, 4, '"Good bye" ne zaman söylenir?', ["Ayrılırken", "Gelirken", "Otururken", "Yerken"], 0, "Vedalaşma"),
    (3, 2, 4, '"I am a student" ne demektir?', ["Ben öğrenciyim", "Ben öğretmenim", "Ben doktorum", "Ben çocuğum"], 0, "student = öğrenci"),
    (3, 2, 4, '"Excuse me" ne zaman kullanılır?', ["Birinden izin isterken", "Teşekkür ederken", "Vedalaşırken", "Selam verirken"], 0, "Affedersiniz"),
]

# ==================================================== NOKTALAMA (2. sinif temel)

NOKTALAMA_EK2 = [
    (1, 2, 4, "Cümle sonunda hangi işaret kullanılır?\n\nBugün okula gittim __", [".", "?", "!", ","], 0, "Nokta"),
    (1, 2, 4, "Soru cümlesinin sonuna ne konur?", ["?", ".", "!", ","], 0, "Soru işareti"),
    (1, 2, 4, "Cümlenin ilk harfi nasıl yazılır?", ["Büyük", "Küçük", "Kalın", "İnce"], 0, "Büyük harf"),
    (1, 2, 4, "İsimlerin ilk harfi nasıl yazılır?", ["Büyük", "Küçük", "Kalın", "Eğik"], 0, "Özel isim büyük harfle"),
    (2, 2, 4, "Hangisi doğru yazılmıştır?", ["Ali okula gitti.", "ali okula gitti.", "Ali okula gitti", "ali Okula gitti."], 0, "Özel isim + nokta"),
    (2, 2, 4, "Hangisi doğru yazılmıştır?", ["Bugün ne yaptın?", "bugün ne yaptın?", "Bugün ne yaptın.", "Bugün ne yaptın"], 0, "Büyük harf + soru işareti"),
    (2, 2, 4, "Sevinç bildiren cümlenin sonuna ne konur?", ["!", ".", "?", ","], 0, "Ünlem"),
    (3, 2, 4, "Şehir isimleri nasıl yazılır?", ["Büyük harfle", "Küçük harfle", "Fark etmez", "Kalın"], 0, "Özel isim"),
    (3, 2, 4, "Hangisinde büyük harf hatası vardır?", ["ankara güzel bir şehirdir.", "Ankara güzel bir şehirdir.", "Ankara büyüktür.", "Bugün Ankara'ya gittik."], 0, "Özel isim büyük yazılır"),
]
