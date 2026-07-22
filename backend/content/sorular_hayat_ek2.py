"""
1-2. SINIF EK SORULARI — Hayat Bilgisi (Parti 4).

ONCELIK: 1. sinif. Envanter analizinde 1. sinif cocugunun sadece 191 yazili
soruya eristigi gorulmustur (2. sinif: 569). Bu dosyadaki sorularin cogu
grade_min=1 olacak sekilde yazilmistir.

1. SINIF DIL KURALI:
  - Soru metni kisa (max 8-9 kelime)
  - Somut ve gunluk hayattan
  - Soyut kavram yok
  - Siklar tek kelime veya kisa obek

Band hedef dogruluk: 1=%90  2=%75  3=%60  4=%40  5=%20
Format: (band, sinif_min, sinif_max, soru, [siklar], dogru_index, aciklama)
"""

# ==================================================== OKULUMUZ (1. sinif agirlikli)

OKULUMUZ_EK2 = [
    (1, 1, 3, "Okulda hangi odada ders yaparız?", ["Sınıf", "Mutfak", "Banyo", "Garaj"], 0, "Sınıf"),
    (1, 1, 3, "Kalemimiz kırılırsa ne yaparız?", ["Kalemtıraşla açarız", "Atarız", "Kırarız", "Saklarız"], 0, "Kalemtıraş"),
    (1, 1, 3, "Okula kaç günde bir gideriz?", ["Hafta içi her gün", "Ayda bir", "Yılda bir", "Hiç"], 0, "Hafta içi 5 gün"),
    (1, 1, 3, "Zil çalınca ne yaparız?", ["Sınıfa gireriz", "Eve gideriz", "Uyuruz", "Yemek yeriz"], 0, "Ders başlar"),
    (1, 1, 3, "Öğretmenimiz konuşurken ne yaparız?", ["Dinleriz", "Konuşuruz", "Uyuruz", "Koşarız"], 0, "Dinlemek"),
    (1, 1, 3, "Sırada nasıl otururuz?", ["Dik", "Yatarak", "Ayakta", "Ters"], 0, "Dik oturmak"),
    (1, 1, 3, "Okul çantamızı kim toplar?", ["Biz", "Öğretmen", "Müdür", "Kimse"], 0, "Kendi sorumluluğumuz"),
    (1, 1, 3, "Hangisi okul eşyasıdır?", ["Silgi", "Tencere", "Yastık", "Havlu"], 0, "Silgi"),
    (1, 1, 3, "Yemekhanede ne yaparız?", ["Yemek yeriz", "Ders yaparız", "Uyuruz", "Koşarız"], 0, "Yemekhane"),
    (1, 1, 3, "Okul bahçesinde ne yaparız?", ["Oynarız", "Ders dinleriz", "Uyuruz", "Yemek pişiririz"], 0, "Oyun alanı"),
    (2, 1, 3, "Arkadaşımız ağlıyorsa ne yaparız?", ["Yanına gider, teselli ederiz", "Güleriz", "Uzaklaşırız", "Görmezden geliriz"], 0, "Empati"),
    (2, 1, 3, "Sınıfta yere çöp düşerse ne yaparız?", ["Alıp çöpe atarız", "Bırakırız", "İteriz", "Görmezden geliriz"], 0, "Temizlik sorumluluğu"),
    (2, 1, 3, "Sıra beklemek neden önemlidir?", ["Herkes hakkını alsın diye", "Zorunlu olduğu için", "Eğlenceli", "Gereksiz"], 0, "Adil paylaşım"),
    (2, 1, 3, "Okula geç kalırsak ne yaparız?", ["Özür diler, sessizce gireriz", "Bağırarak gireriz", "Girmeyiz", "Bekleriz"], 0, "Nezaket"),
    (2, 1, 3, "Ödevimizi ne zaman yaparız?", ["Aynı gün", "Bir hafta sonra", "Hiç", "Sabah okulda"], 0, "Zamanında"),
    (2, 1, 3, "Sınıf kitaplığından kitabı kim alabilir?", ["Herkes sırayla", "Sadece bir kişi", "Kimse", "Sadece öğretmen"], 0, "Ortak kullanım"),
    (2, 1, 3, "Arkadaşımızın eşyasını izinsiz alır mıyız?", ["Hayır, izin isteriz", "Evet", "Bazen", "Sadece kalem"], 0, "İzin istemek"),
    (3, 1, 3, "Sınıf temizliği kimin görevidir?", ["Hepimizin", "Sadece nöbetçinin", "Hizmetlinin", "Öğretmenin"], 0, "Ortak sorumluluk"),
    (3, 2, 3, "Arkadaşımız yanlış cevap verirse ne yaparız?", ["Gülmeyiz, saygı gösteririz", "Güleriz", "Alay ederiz", "Bağırırız"], 0, "Saygı"),
    (3, 2, 3, "Okulda hangi davranış yanlıştır?", ["Koridorda koşmak", "Sıraya girmek", "Selam vermek", "Yardım etmek"], 0, "Koşmak tehlikeli"),
]

# ==================================================== AILEMIZ (1. sinif agirlikli)

AILEMIZ_EK2 = [
    (1, 1, 3, "Evimizde en çok kiminle yaşarız?", ["Ailemizle", "Yabancılarla", "Tek başımıza", "Komşularla"], 0, "Aile"),
    (1, 1, 3, "Annemiz bize ne der?", ["Evladım", "Komşum", "Arkadaşım", "Öğretmenim"], 0, "Anne-evlat"),
    (1, 1, 3, "Kardeşimizle nasıl geçinmeliyiz?", ["İyi", "Kavgalı", "Küs", "Uzak"], 0, "İyi geçinmek"),
    (1, 1, 3, "Evde yemekleri genelde nerede yeriz?", ["Sofrada", "Yatakta", "Banyoda", "Balkonda"], 0, "Sofra"),
    (1, 1, 3, "Uyumadan önce ne yaparız?", ["Dişimizi fırçalarız", "Koşarız", "Yemek yeriz", "Oyun oynarız"], 0, "Gece rutini"),
    (1, 1, 3, "Oyuncaklarımızı kiminle paylaşırız?", ["Kardeşimiz ve arkadaşımızla", "Kimseyle", "Sadece kendimizle", "Yabancılarla"], 0, "Paylaşmak"),
    (1, 1, 3, "Evde kim yemek yapar?", ["Anne veya baba", "Bebek", "Kedi", "Kimse"], 0, "Büyükler"),
    (1, 1, 3, "Büyüklerimize nasıl davranmalıyız?", ["Saygılı", "Kaba", "İlgisiz", "Bağırarak"], 0, "Saygı"),
    (1, 1, 3, "Hangisi ailemizin bir üyesidir?", ["Kardeşimiz", "Öğretmenimiz", "Komşumuz", "Doktorumuz"], 0, "Aile üyesi"),
    (1, 1, 3, "Evimize gelen kişiye ne deriz?", ["Hoş geldiniz", "Git", "Hayır", "Bilmiyorum"], 0, "Misafirperverlik"),
    (2, 1, 3, "Evde en çok neye dikkat etmeliyiz?", ["Güvenliğe", "Renklere", "Seslere", "Kokulara"], 0, "Ev güvenliği"),
    (2, 1, 3, "Ocakta yemek pişerken ne yapmalıyız?", ["Yaklaşmamalıyız", "Dokunmalıyız", "Açmalıyız", "Karıştırmalıyız"], 0, "Yanık tehlikesi"),
    (2, 1, 3, "Kirli çamaşırlarımızı nereye koyarız?", ["Kirli sepetine", "Dolaba", "Yatağa", "Yere"], 0, "Düzen"),
    (2, 1, 3, "Ailemizle vakit geçirmek neden güzeldir?", ["Birbirimizi daha iyi tanırız", "Zorunlu olduğu için", "Sıkıcı", "Gereksiz"], 0, "Aile bağı"),
    (2, 1, 3, "Odamızı ne zaman toplamalıyız?", ["Her gün", "Ayda bir", "Yılda bir", "Hiç"], 0, "Düzenli olmak"),
    (2, 1, 3, "Evde ışıkları kim kapatmalı?", ["Odadan çıkan herkes", "Sadece anne", "Sadece baba", "Kimse"], 0, "Tasarruf"),
    (2, 2, 3, "Anneannemiz kimin annesidir?", ["Annemizin", "Babamızın", "Kardeşimizin", "Bizim"], 0, "Anne tarafı"),
    (2, 2, 3, "Babaannemiz kimin annesidir?", ["Babamızın", "Annemizin", "Kardeşimizin", "Bizim"], 0, "Baba tarafı"),
    (3, 2, 3, "Ailede herkesin görevi olmalı mıdır?", ["Evet, paylaşmak gerekir", "Hayır", "Sadece büyüklerin", "Sadece çocukların"], 0, "Görev paylaşımı"),
    (3, 2, 3, "Evde bir eşyayı kırarsak ne yaparız?", ["Söyleriz ve özür dileriz", "Saklarız", "Suçu başkasına atarız", "Susarız"], 0, "Dürüstlük"),
]

# ==================================================== SAGLIGIMIZ (1. sinif agirlikli)

SAGLIGIMIZ_EK2 = [
    (1, 1, 3, "Elimizi ne ile yıkarız?", ["Su ve sabun", "Toprak", "Kum", "Yağ"], 0, "Su + sabun"),
    (1, 1, 3, "Dişimizi ne ile fırçalarız?", ["Diş fırçası", "Tarak", "Havlu", "Bez"], 0, "Diş fırçası"),
    (1, 1, 3, "Hangisi meyvedir?", ["Elma", "Ekmek", "Peynir", "Yumurta"], 0, "Elma meyve"),
    (1, 1, 3, "Hangisi sebzedir?", ["Havuç", "Muz", "Süt", "Bal"], 0, "Havuç sebze"),
    (1, 1, 3, "Susadığımızda ne içeriz?", ["Su", "Yağ", "Tuz", "Un"], 0, "Su"),
    (1, 1, 3, "Sabah kalkınca ne yaparız?", ["Yüzümüzü yıkarız", "Tekrar uyuruz", "Koşarız", "Bekleriz"], 0, "Sabah temizliği"),
    (1, 1, 3, "Hangisi bizi hasta edebilir?", ["Kirli eller", "Temiz eller", "Su içmek", "Uyumak"], 0, "Hijyen"),
    (1, 1, 3, "Yemekten sonra ne yaparız?", ["Ağzımızı temizleriz", "Koşarız", "Uyuruz", "Bağırırız"], 0, "Ağız temizliği"),
    (1, 1, 3, "Spor yapmak bize ne verir?", ["Sağlık", "Hastalık", "Yorgunluk", "Uyku"], 0, "Sağlıklı vücut"),
    (1, 1, 3, "Gece ne yapmalıyız?", ["Erken uyumalıyız", "Geç yatmalıyız", "Oyun oynamalıyız", "TV izlemeliyiz"], 0, "Erken uyku"),
    (2, 1, 3, "Neden sebze yemeliyiz?", ["Bizi güçlendirir", "Tatlı olduğu için", "Renkli olduğu için", "Ucuz olduğu için"], 0, "Vitamin"),
    (2, 1, 3, "Hangisi dişimize zarar verir?", ["Çok şeker", "Süt", "Su", "Peynir"], 0, "Şeker çürütür"),
    (2, 1, 3, "Yemek yerken ne yapmalıyız?", ["İyi çiğnemeliyiz", "Hızlı yutmalıyız", "Koşmalıyız", "Konuşmalıyız"], 0, "İyi çiğnemek"),
    (2, 1, 3, "Havlumuzu kim kullanabilir?", ["Sadece biz", "Herkes", "Kardeşimiz", "Arkadaşımız"], 0, "Kişisel eşya"),
    (2, 1, 3, "Hastayken ne yapmalıyız?", ["Dinlenmeliyiz", "Koşmalıyız", "Oyun oynamalıyız", "Okula gitmeliyiz"], 0, "Dinlenme"),
    (2, 1, 3, "Tırnaklarımız nasıl olmalı?", ["Kısa ve temiz", "Uzun", "Kirli", "Boyalı"], 0, "Temiz tırnak"),
    (2, 1, 3, "Hangisi sağlıklı kahvaltıdır?", ["Peynir, zeytin, yumurta", "Çikolata", "Cips", "Gazoz"], 0, "Dengeli kahvaltı"),
    (3, 2, 3, "Mikroplar gözle görülür mü?", ["Hayır, çok küçüktür", "Evet", "Bazen", "Sadece geceleri"], 0, "Mikroskobik"),
    (3, 2, 3, "Neden çeşitli besinler yemeliyiz?", ["Her besinin faydası farklıdır", "Sıkılmamak için", "Ucuz olduğu için", "Zorunlu"], 0, "Dengeli beslenme"),
    (3, 2, 3, "Öksürürken ağzımızı neyle kapatmalıyız?", ["Mendil veya dirseğimizle", "Elimizle", "Hiçbir şeyle", "Kitapla"], 0, "Mikrop yayılmasın"),
]

# ==================================================== GUVENLIGIMIZ (1. sinif agirlikli)

GUVENLIGIMIZ_EK2 = [
    (1, 1, 3, "Yolda kimin yanında yürürüz?", ["Büyüğümüzün", "Yalnız", "Yabancının", "Hayvanın"], 0, "Büyükle"),
    (1, 1, 3, "Kırmızı ışıkta ne yaparız?", ["Dururuz", "Geçeriz", "Koşarız", "Bekleriz sonra geçeriz"], 0, "Kırmızı = dur"),
    (1, 1, 3, "Yeşil ışıkta ne yaparız?", ["Geçeriz", "Dururuz", "Bekleriz", "Otururuz"], 0, "Yeşil = geç"),
    (1, 1, 3, "Sıcak sobaya dokunur muyuz?", ["Hayır", "Evet", "Bazen", "Kışın"], 0, "Yanık tehlikesi"),
    (1, 1, 3, "Makası nasıl tutmalıyız?", ["Dikkatli", "Koşarak", "Sallayarak", "Ağzımızda"], 0, "Kesici alet"),
    (1, 1, 3, "Yabancı biri bizi çağırırsa ne yaparız?", ["Gitmeyiz", "Gideriz", "Konuşuruz", "Adres veririz"], 0, "Yabancıyla gitmeyiz"),
    (1, 1, 3, "Kaldırımda mı yolda mı yürürüz?", ["Kaldırımda", "Yolda", "Ortada", "Fark etmez"], 0, "Kaldırım yayalar için"),
    (1, 1, 3, "Arabada nerede otururuz?", ["Arka koltukta", "Ön koltukta", "Şoförün yanında", "Bagajda"], 0, "Çocuklar arkada"),
    (1, 1, 3, "Elektrik prizine parmak sokar mıyız?", ["Asla", "Evet", "Bazen", "Kuru elle"], 0, "Çok tehlikeli"),
    (1, 1, 3, "Acil durumda kimi ararız?", ["112", "Arkadaşımızı", "Kimseyi", "Komşuyu"], 0, "112"),
    (2, 1, 3, "Bisiklete binerken kafamıza ne takarız?", ["Kask", "Şapka", "Atkı", "Hiçbir şey"], 0, "Kask korur"),
    (2, 1, 3, "Arabada kemer takar mıyız?", ["Evet, her zaman", "Hayır", "Bazen", "Uzun yolda"], 0, "Emniyet kemeri"),
    (2, 1, 3, "İlaçları kim verir?", ["Büyüklerimiz", "Kendimiz", "Arkadaşımız", "Kimse"], 0, "İlaç tehlikeli olabilir"),
    (2, 1, 3, "Merdivende koşar mıyız?", ["Hayır, dikkatli ineriz", "Evet", "Bazen", "Acelemiz varsa"], 0, "Düşme riski"),
    (2, 1, 3, "Top yola kaçarsa ne yaparız?", ["Büyüğe söyleriz", "Koşarak alırız", "Atlarız", "Bekleriz"], 0, "Yola çıkmayız"),
    (2, 2, 3, "Deprem olunca ne yaparız?", ["Çök-Kapan-Tutun", "Koşarız", "Bağırırız", "Pencereye gideriz"], 0, "Çök, kapan, tutun"),
    (2, 2, 3, "Yangında ne yaparız?", ["Büyüğe haber verip çıkarız", "Saklanırız", "Bekleriz", "Su ararız"], 0, "Hemen haber + tahliye"),
    (3, 2, 3, "Bu işaret ne demektir? 🚭", ["Sigara içilmez", "Dur", "Geç", "Park yeri"], 0, "Sigara yasağı"),
    (3, 2, 3, "Yabancının verdiği şekeri alır mıyız?", ["Hayır", "Evet", "Bazen", "Güzelse"], 0, "Yabancıdan bir şey alınmaz"),
]

# ==================================================== ULKEMIZ (1. sinif agirlikli)

ULKEMIZ_EK2 = [
    (1, 1, 3, "Bayrağımız hangi renktir?", ["Kırmızı", "Mavi", "Yeşil", "Sarı"], 0, "Kırmızı"),
    (1, 1, 3, "Atatürk kimdir?", ["Cumhuriyetimizin kurucusu", "Bir öğretmen", "Bir doktor", "Bir sporcu"], 0, "Kurucu"),
    (1, 1, 3, "Bayrağımıza nasıl davranırız?", ["Saygıyla", "İlgisizce", "Kirletiriz", "Atarız"], 0, "Saygı"),
    (1, 1, 3, "23 Nisan kimin bayramıdır?", ["Çocukların", "Büyüklerin", "Öğretmenlerin", "Askerlerin"], 0, "Çocuk Bayramı"),
    (1, 1, 3, "Bayramda ne yaparız?", ["Büyüklerimizi ziyaret ederiz", "Uyuruz", "Çalışırız", "Okula gideriz"], 0, "Bayram ziyareti"),
    (1, 1, 3, "Milli marşımızı ne zaman söyleriz?", ["Bayrak töreninde", "Uyurken", "Yemekte", "Oyunda"], 0, "Bayrak töreni"),
    (1, 1, 3, "Bayrak töreninde nasıl dururuz?", ["Hazır ol", "Otururuz", "Yürürüz", "Konuşuruz"], 0, "Saygı duruşu"),
    (2, 1, 3, "Atatürk'ün en sevdiği söz hangisidir?", ["Ne mutlu Türk'üm diyene", "Yavaş git", "Bekle gör", "Sonra bakarız"], 0, "Atatürk'ün sözü"),
    (2, 1, 3, "Vatan ne demektir?", ["Yaşadığımız ülke", "Evimiz", "Okulumuz", "Odamız"], 0, "Vatan = ülke"),
    (2, 2, 3, "Atatürk 23 Nisan'ı kime armağan etti?", ["Çocuklara", "Gençlere", "Askerlere", "Öğretmenlere"], 0, "Çocuklara"),
    (2, 2, 3, "19 Mayıs kimin bayramıdır?", ["Gençlerin", "Çocukların", "Öğretmenlerin", "Annelerin"], 0, "Gençlik ve Spor"),
    (2, 2, 3, "Millet ne demektir?", ["Aynı ülkede yaşayan insanlar", "Bir aile", "Bir sınıf", "Bir şehir"], 0, "Millet"),
    (3, 2, 3, "Atatürk nerede doğdu?", ["Selanik", "Ankara", "İstanbul", "İzmir"], 0, "Selanik"),
    (3, 2, 3, "10 Kasım'da ne yaparız?", ["Atatürk'ü anarız", "Kutlarız", "Tatil yaparız", "Oyun oynarız"], 0, "Anma günü"),
]

# ==================================================== DOGA VE CEVRE (1. sinif agirlikli)

DOGA_CEVRE_EK2 = [
    (1, 1, 3, "Hangisi hayvandır?", ["Kedi", "Masa", "Kalem", "Taş"], 0, "Kedi hayvan"),
    (1, 1, 3, "Hangisi bitkidir?", ["Ağaç", "Araba", "Kitap", "Kaşık"], 0, "Ağaç bitki"),
    (1, 1, 3, "Kuş nerede yaşar?", ["Yuvada", "Denizde", "Toprakta", "Kutuda"], 0, "Kuş yuvası"),
    (1, 1, 3, "Bitki büyümek için neye ihtiyaç duyar?", ["Su ve güneş", "Sadece toprak", "Kum", "Taş"], 0, "Su + güneş"),
    (1, 1, 3, "Kışın hava nasıldır?", ["Soğuk", "Sıcak", "Ilık", "Değişmez"], 0, "Kış soğuktur"),
    (1, 1, 3, "Yazın hava nasıldır?", ["Sıcak", "Soğuk", "Karlı", "Buzlu"], 0, "Yaz sıcaktır"),
    (1, 1, 3, "Ağaçlar bize ne verir?", ["Temiz hava", "Elektrik", "Su", "Kum"], 0, "Oksijen"),
    (1, 1, 3, "Çöpü nereye atmalıyız?", ["Çöp kutusuna", "Yere", "Denize", "Bahçeye"], 0, "Çöp kutusu"),
    (1, 1, 3, "Hangisi cansızdır?", ["Taş", "Kuş", "Çiçek", "Balık"], 0, "Taş cansız"),
    (2, 1, 3, "Yapraklar hangi mevsimde dökülür?", ["Sonbahar", "İlkbahar", "Yaz", "Kış"], 0, "Sonbahar"),
    (2, 1, 3, "Çiçekler hangi mevsimde açar?", ["İlkbahar", "Kış", "Sonbahar", "Hiçbiri"], 0, "İlkbahar"),
    (2, 1, 3, "Suyu neden boşa harcamamalıyız?", ["Su çok değerlidir", "Pahalı olduğu için", "Zor bulunur", "Ağırdır"], 0, "Su tasarrufu"),
    (3, 2, 3, "Geri dönüşüm neden yapılır?", ["Doğayı korumak için", "Zaman geçsin diye", "Zorunlu olduğu için", "Eğlenceli"], 0, "Çevre koruma"),
    (3, 2, 3, "Ağaç kesmek neden zararlıdır?", ["Temiz havamız azalır", "Gürültü olur", "Pahalıdır", "Zordur"], 0, "Oksijen kaynağı"),
]
