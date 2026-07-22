"""
Geometri + Ingilizce EK soru bankasi (Parti 3).
sorular_diger.py'yi tamamlar.

Band hedef dogruluk: 1=%90  2=%75  3=%60  4=%40  5=%20
Format: (band, sinif_min, sinif_max, soru, [siklar], dogru_index, aciklama)
"""

# ==================================================== GEOMETRI

GEOMETRI_EK = [
    # Band 1
    (1, 1, 4, "Bu şekil nedir?\n\n🟦", ["Kare", "Üçgen", "Daire", "Yıldız"], 0, "Kare"),
    (1, 1, 4, "Bu şekil nedir?\n\n🔴", ["Daire", "Kare", "Üçgen", "Dikdörtgen"], 0, "Daire"),
    (1, 1, 4, "Tekerlek hangi şekle benzer?", ["Daire", "Kare", "Üçgen", "Dikdörtgen"], 0, "Tekerlek yuvarlaktır"),
    (1, 1, 4, "Kapı hangi şekle benzer?", ["Dikdörtgen", "Daire", "Üçgen", "Yıldız"], 0, "Dikdörtgen"),
    (1, 1, 4, "Pencere genelde hangi şekildedir?", ["Dikdörtgen", "Üçgen", "Daire", "Yıldız"], 0, "Dikdörtgen"),
    (1, 1, 4, "Hangi şeklin köşesi yoktur?", ["Daire", "Kare", "Üçgen", "Dikdörtgen"], 0, "Daire yuvarlaktır"),
    (1, 1, 4, "Dikdörtgenin kaç köşesi vardır?", ["4", "3", "5", "0"], 0, "4 köşe"),
    (1, 1, 4, "Bir üçgeni çizmek için kaç çizgi gerekir?", ["3", "4", "2", "5"], 0, "3 kenar = 3 çizgi"),
    # Band 2
    (2, 1, 4, "Karenin kenarları birbirine nasıldır?", ["Eşittir", "Farklıdır", "İkisi kısa", "İkisi uzun"], 0, "Karenin 4 kenarı eşit"),
    (2, 2, 4, "Dikdörtgenin karşılıklı kenarları nasıldır?", ["Eşittir", "Farklıdır", "Hepsi eşittir", "Hiçbiri eşit değildir"], 0, "Karşılıklı kenarlar eşit"),
    (2, 1, 4, "Pizza dilimi hangi şekle benzer?", ["Üçgen", "Kare", "Daire", "Dikdörtgen"], 0, "Üçgen"),
    (2, 2, 4, "Dondurma külahı hangi cisme benzer?", ["Koni", "Küp", "Küre", "Silindir"], 0, "Koni"),
    (2, 2, 4, "Futbol topu hangi cisme benzer?", ["Küre", "Küp", "Koni", "Silindir"], 0, "Küre"),
    (2, 2, 4, "Kutu şeklindeki bir zar hangi cisimdir?", ["Küp", "Küre", "Koni", "Piramit"], 0, "Küp"),
    (2, 2, 4, "Bardak hangi cisme benzer?", ["Silindir", "Küp", "Küre", "Koni"], 0, "Silindir"),
    (2, 2, 4, "Karenin kaç kenarı ve kaç köşesi vardır?", ["4 kenar 4 köşe", "3 kenar 3 köşe", "4 kenar 3 köşe", "5 kenar 5 köşe"], 0, "Kare: 4-4"),
    (2, 2, 4, "Hangisi düz bir çizgidir?", ["Doğru", "Daire", "Kare", "Üçgen"], 0, "Doğru düz çizgidir"),
    # Band 3
    (3, 2, 4, "Bir kenarı 2 cm olan karenin çevresi kaçtır?", ["8 cm", "4 cm", "6 cm", "2 cm"], 0, "4 × 2 = 8 cm"),
    (3, 2, 4, "Bir kenarı 4 cm olan karenin çevresi kaçtır?", ["16 cm", "8 cm", "12 cm", "4 cm"], 0, "4 × 4 = 16 cm"),
    (3, 3, 4, "Kenarları 3 cm ve 5 cm olan dikdörtgenin çevresi kaçtır?", ["16 cm", "15 cm", "8 cm", "11 cm"], 0, "(3+5) × 2 = 16 cm"),
    (3, 3, 4, "Yedigenin kaç kenarı vardır?", ["7", "6", "8", "5"], 0, "Yedigen: 7 kenar"),
    (3, 3, 4, "Sekizgenin kaç kenarı vardır?", ["8", "7", "6", "9"], 0, "Sekizgen: 8 kenar"),
    (3, 2, 4, "Çokgen ne demektir?", ["Çok kenarlı kapalı şekil", "Yuvarlak şekil", "Düz çizgi", "Nokta"], 0, "Çok + kenar"),
    (3, 3, 4, "Küpün kaç yüzü vardır?", ["6", "4", "8", "12"], 0, "Küp: 6 kare yüz"),
    (3, 3, 4, "Bir üçgenin kenarları 3, 4 ve 5 cm ise çevresi kaçtır?", ["12 cm", "10 cm", "15 cm", "9 cm"], 0, "3+4+5 = 12 cm"),
    (3, 3, 4, "Simetri ekseni ne yapar?", ["Şekli iki eş parçaya böler", "Şekli büyütür", "Şekli döndürür", "Şekli küçültür"], 0, "Eş iki parça"),
    (3, 3, 4, "Hangi harfin simetri ekseni vardır?", ["A", "F", "G", "J"], 0, "A dikey simetriye sahiptir"),
    # Band 4
    (4, 3, 4, "Bir kenarı 3 cm olan karenin alanı kaçtır?", ["9 cm²", "12 cm²", "6 cm²", "3 cm²"], 0, "3 × 3 = 9 cm²"),
    (4, 4, 4, "Kenarları 4 cm ve 5 cm olan dikdörtgenin alanı kaçtır?", ["20 cm²", "18 cm²", "9 cm²", "16 cm²"], 0, "4 × 5 = 20 cm²"),
    (4, 4, 4, "Bir karenin köşelerindeki açılar kaç derecedir?", ["90°", "45°", "60°", "180°"], 0, "Karenin tüm açıları diktir (90°)"),
    (4, 4, 4, "Dar açı kaç dereceden küçüktür?", ["90°", "180°", "45°", "360°"], 0, "Dar açı < 90°"),
    (4, 4, 4, "Geniş açı hangi aralıktadır?", ["90° ile 180° arası", "0° ile 90° arası", "180°'den büyük", "Tam 90°"], 0, "90° < geniş açı < 180°"),
    (4, 3, 4, "Eşkenar üçgenin kaç simetri ekseni vardır?", ["3", "1", "2", "0"], 0, "Eşkenar üçgende 3 simetri ekseni"),
    (4, 3, 4, "Dikdörtgenin kaç simetri ekseni vardır?", ["2", "4", "1", "0"], 0, "Dikdörtgende 2 simetri ekseni"),
    # Band 5
    (5, 4, 4, "Düz bir çizgi üzerindeki açı kaç derecedir?", ["180°", "90°", "360°", "45°"], 0, "Doğru açı = 180°"),
    (5, 4, 4, "Tam açı kaç derecedir?", ["360°", "180°", "90°", "270°"], 0, "Tam açı = 360°"),
    (5, 4, 4, "Bir üçgenin iç açıları toplamı kaç derecedir?", ["180°", "360°", "90°", "270°"], 0, "Üçgende iç açılar toplamı 180°"),
    (5, 4, 4, "Dairenin simetri ekseni kaç tanedir?", ["Sonsuz", "1", "2", "4"], 0, "Daire her çapından simetriktir"),
]

# ==================================================== INGILIZCE KELIMELER

ING_KELIME_EK = [
    # Band 1
    (1, 2, 4, '"Black" ne demektir?', ["Siyah", "Beyaz", "Mavi", "Kırmızı"], 0, "black = siyah"),
    (1, 2, 4, '"White" ne demektir?', ["Beyaz", "Siyah", "Sarı", "Yeşil"], 0, "white = beyaz"),
    (1, 2, 4, '"Four" ne demektir?', ["Dört", "Üç", "Beş", "Altı"], 0, "four = dört"),
    (1, 2, 4, '"Five" ne demektir?', ["Beş", "Dört", "Altı", "Yedi"], 0, "five = beş"),
    (1, 2, 4, '"Sun" ne demektir?', ["Güneş", "Ay", "Yıldız", "Bulut"], 0, "sun = güneş"),
    (1, 2, 4, '"Moon" ne demektir?', ["Ay", "Güneş", "Yıldız", "Gökyüzü"], 0, "moon = ay"),
    (1, 2, 4, '"Hand" ne demektir?', ["El", "Ayak", "Baş", "Göz"], 0, "hand = el"),
    (1, 2, 4, '"Eye" ne demektir?', ["Göz", "Kulak", "Burun", "Ağız"], 0, "eye = göz"),
    # Band 2
    (2, 2, 4, '"Six" ne demektir?', ["Altı", "Beş", "Yedi", "Sekiz"], 0, "six = altı"),
    (2, 2, 4, '"Ten" ne demektir?', ["On", "Dokuz", "Sekiz", "Yedi"], 0, "ten = on"),
    (2, 2, 4, '"Horse" ne demektir?', ["At", "İnek", "Koyun", "Köpek"], 0, "horse = at"),
    (2, 2, 4, '"Rabbit" ne demektir?', ["Tavşan", "Kedi", "Fare", "Köpek"], 0, "rabbit = tavşan"),
    (2, 2, 4, '"Sister" ne demektir?', ["Kız kardeş", "Erkek kardeş", "Anne", "Teyze"], 0, "sister = kız kardeş"),
    (2, 2, 4, '"Brother" ne demektir?', ["Erkek kardeş", "Kız kardeş", "Baba", "Amca"], 0, "brother = erkek kardeş"),
    (2, 2, 4, '"Bread" ne demektir?', ["Ekmek", "Peynir", "Süt", "Yumurta"], 0, "bread = ekmek"),
    (2, 2, 4, '"Egg" ne demektir?', ["Yumurta", "Ekmek", "Süt", "Peynir"], 0, "egg = yumurta"),
    (2, 2, 4, '"Bag" ne demektir?', ["Çanta", "Kitap", "Kalem", "Defter"], 0, "bag = çanta"),
    (2, 2, 4, '"Table" ne demektir?', ["Masa", "Sandalye", "Kapı", "Pencere"], 0, "table = masa"),
    # Band 3
    (3, 2, 4, '"Chair" ne demektir?', ["Sandalye", "Masa", "Yatak", "Dolap"], 0, "chair = sandalye"),
    (3, 2, 4, '"Window" ne demektir?', ["Pencere", "Kapı", "Duvar", "Zemin"], 0, "window = pencere"),
    (3, 3, 4, '"Friend" ne demektir?', ["Arkadaş", "Öğretmen", "Kardeş", "Komşu"], 0, "friend = arkadaş"),
    (3, 3, 4, '"House" ne demektir?', ["Ev", "Okul", "Park", "Market"], 0, "house = ev"),
    (3, 3, 4, '"Angry" ne demektir?', ["Kızgın", "Mutlu", "Üzgün", "Yorgun"], 0, "angry = kızgın"),
    (3, 3, 4, '"Tired" ne demektir?', ["Yorgun", "Mutlu", "Kızgın", "Aç"], 0, "tired = yorgun"),
    (3, 3, 4, '"Tuesday" ne demektir?', ["Salı", "Pazartesi", "Çarşamba", "Perşembe"], 0, "Tuesday = Salı"),
    (3, 3, 4, '"Friday" ne demektir?', ["Cuma", "Perşembe", "Cumartesi", "Pazar"], 0, "Friday = Cuma"),
    (3, 3, 4, '"Snowy" ne demektir?', ["Karlı", "Yağmurlu", "Güneşli", "Rüzgarlı"], 0, "snowy = karlı"),
    (3, 3, 4, '"Windy" ne demektir?', ["Rüzgarlı", "Yağmurlu", "Karlı", "Güneşli"], 0, "windy = rüzgarlı"),
    # Band 4
    (4, 3, 4, '"Sleep" ne demektir?', ["Uyumak", "Koşmak", "Yemek", "İçmek"], 0, "sleep = uyumak"),
    (4, 3, 4, '"Drink" ne demektir?', ["İçmek", "Yemek", "Uyumak", "Koşmak"], 0, "drink = içmek"),
    (4, 3, 4, '"Write" ne demektir?', ["Yazmak", "Okumak", "Çizmek", "Silmek"], 0, "write = yazmak"),
    (4, 3, 4, '"Read" ne demektir?', ["Okumak", "Yazmak", "Dinlemek", "Konuşmak"], 0, "read = okumak"),
    (4, 3, 4, '"December" ne demektir?', ["Aralık", "Kasım", "Ocak", "Şubat"], 0, "December = Aralık"),
    (4, 3, 4, '"Grandfather" ne demektir?', ["Büyükbaba", "Baba", "Amca", "Dayı"], 0, "grandfather = büyükbaba"),
    # Band 5
    (5, 3, 4, '"Wednesday" ne demektir?', ["Çarşamba", "Salı", "Perşembe", "Pazartesi"], 0, "Wednesday = Çarşamba"),
    (5, 3, 4, '"February" ne demektir?', ["Şubat", "Ocak", "Mart", "Nisan"], 0, "February = Şubat"),
    (5, 3, 4, '"Vegetable" ne demektir?', ["Sebze", "Meyve", "Et", "Ekmek"], 0, "vegetable = sebze"),
]

# ==================================================== INGILIZCE IFADELER

ING_IFADE_EK = [
    # Band 1
    (1, 2, 4, '"Hi" ne demektir?', ["Selam", "Hoşça kal", "Teşekkürler", "Lütfen"], 0, "Hi = Selam"),
    (1, 2, 4, '"Welcome" ne demektir?', ["Hoş geldin", "Hoşça kal", "Teşekkürler", "Özür dilerim"], 0, "Welcome = Hoş geldin"),
    (1, 2, 4, '"OK" ne demektir?', ["Tamam", "Hayır", "Belki", "Asla"], 0, "OK = Tamam"),
    (1, 2, 4, '"Look" ne demektir?', ["Bak", "Dinle", "Konuş", "Yaz"], 0, "Look = Bak"),
    (1, 2, 4, '"Stop" ne demektir?', ["Dur", "Git", "Koş", "Gel"], 0, "Stop = Dur"),
    # Band 2
    (2, 2, 4, '"Good luck" ne demektir?', ["İyi şanslar", "Günaydın", "Hoşça kal", "Teşekkürler"], 0, "Good luck = İyi şanslar"),
    (2, 2, 4, '"Be quiet" ne demektir?', ["Sessiz ol", "Konuş", "Bağır", "Şarkı söyle"], 0, "Be quiet = Sessiz ol"),
    (2, 2, 4, '"Close the door" ne demektir?', ["Kapıyı kapat", "Kapıyı aç", "Kapıya bak", "Kapıdan çık"], 0, "Close = Kapat"),
    (2, 2, 4, '"Wash your hands" ne demektir?', ["Ellerini yıka", "Ellerini kaldır", "Ellerini indir", "Ellerini kurula"], 0, "Wash = Yıka"),
    (2, 2, 4, '"Let\'s go" ne demektir?', ["Hadi gidelim", "Hadi duralım", "Hadi oturalım", "Hadi bekleyelim"], 0, "Let's go = Hadi gidelim"),
    (2, 2, 4, '"See you tomorrow" ne demektir?', ["Yarın görüşürüz", "Bugün görüşürüz", "Dün görüştük", "Hiç görüşmeyiz"], 0, "tomorrow = yarın"),
    # Band 3
    (3, 2, 4, '"I am hungry" ne demektir?', ["Açım", "Susadım", "Yorgunum", "Uykum var"], 0, "hungry = aç"),
    (3, 3, 4, '"I am thirsty" ne demektir?', ["Susadım", "Açım", "Yorgunum", "Üşüyorum"], 0, "thirsty = susamış"),
    (3, 3, 4, '"How many?" ne demektir?', ["Kaç tane?", "Ne kadar?", "Nerede?", "Ne zaman?"], 0, "How many? = Kaç tane?"),
    (3, 3, 4, '"What time is it?" ne demektir?', ["Saat kaç?", "Ne zaman?", "Nerede?", "Kim?"], 0, "What time is it? = Saat kaç?"),
    (3, 3, 4, '"Close your book" ne demektir?', ["Kitabını kapat", "Kitabını aç", "Kitabını al", "Kitabını ver"], 0, "Close = Kapat"),
    (3, 3, 4, '"Raise your hand" ne demektir?', ["Elini kaldır", "Elini indir", "Elini yıka", "Elini ver"], 0, "Raise = Kaldır"),
    # Band 4
    (4, 3, 4, '"I don\'t know" ne demektir?', ["Bilmiyorum", "Biliyorum", "Anlıyorum", "Görüyorum"], 0, "I don't know = Bilmiyorum"),
    (4, 3, 4, '"Can you help me?" ne demektir?', ["Bana yardım eder misin?", "Sana yardım edeyim mi?", "Yardıma ihtiyacın var mı?", "Yardım geldi mi?"], 0, "Can you help me? = Yardım eder misin?"),
    (4, 3, 4, '"I like it" ne demektir?', ["Onu beğendim", "Onu beğenmedim", "Onu görmedim", "Onu bilmiyorum"], 0, "I like it = Beğendim"),
    (4, 3, 4, '"What is this?" ne demektir?', ["Bu nedir?", "Bu kimdir?", "Bu nerede?", "Bu ne zaman?"], 0, "What is this? = Bu nedir?"),
    (4, 3, 4, '"Have a nice day" ne demektir?', ["İyi günler", "İyi geceler", "Günaydın", "Hoşça kal"], 0, "Have a nice day = İyi günler"),
    # Band 5
    (5, 3, 4, '"I would like some water" ne demektir?', ["Biraz su istiyorum", "Su içtim", "Su yok", "Su nerede?"], 0, "I would like = İstiyorum (kibar)"),
    (5, 3, 4, '"How much is it?" ne demektir?', ["Ne kadar?", "Kaç tane?", "Nerede?", "Ne zaman?"], 0, "How much? = Fiyatı ne kadar?"),
    (5, 3, 4, '"You are welcome" farkı nedir?', ["Rica ederim (teşekküre cevap)", "Hoş geldin", "Hoşça kal", "Teşekkürler"], 0, "Teşekküre verilen cevap"),
]
