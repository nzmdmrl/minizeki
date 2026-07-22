"""
Hayat Bilgisi yazili soru bankasi. 1-3. sinif.
MEB'in 6 unitesine birebir eslenir.

Format: (band, sinif_min, sinif_max, soru, [siklar], dogru_index, aciklama)
"""

# ---------------------------------------------------- 1. OKULUMUZDA HAYAT

OKULUMUZ = [
    (1, 1, 3, "Sınıfta söz almak için ne yapmalıyız?", ["Parmak kaldırmalıyız", "Bağırmalıyız", "Ayağa kalkmalıyız", "Sıraya vurmalıyız"], 0, "Söz almak için parmak kaldırılır"),
    (1, 1, 3, "Okula giderken yanımızda ne götürürüz?", ["Çanta", "Yastık", "Battaniye", "Tencere"], 0, "Okul çantası"),
    (1, 1, 3, "Sınıfımızı kim temiz tutar?", ["Hepimiz", "Sadece öğretmen", "Sadece müdür", "Sadece nöbetçi"], 0, "Sınıf temizliği herkesin sorumluluğudur"),
    (1, 1, 3, "Okulda dersleri kim anlatır?", ["Öğretmen", "Müdür", "Hizmetli", "Şoför"], 0, "Öğretmen ders anlatır"),
    (1, 1, 3, "Teneffüste ne yaparız?", ["Dinleniriz ve oynarız", "Ders çalışırız", "Uyuruz", "Eve gideriz"], 0, "Teneffüs dinlenme zamanıdır"),
    (2, 1, 3, "Arkadaşımız düştüğünde ne yapmalıyız?", ["Yardım etmeliyiz", "Gülmeliyiz", "Görmezden gelmeliyiz", "Uzaklaşmalıyız"], 0, "Arkadaşımıza yardım ederiz"),
    (2, 1, 3, "Okulun en yetkili kişisi kimdir?", ["Müdür", "Öğretmen", "Hizmetli", "Öğrenci"], 0, "Okul müdürü"),
    (2, 1, 3, "Kütüphanede nasıl davranmalıyız?", ["Sessiz olmalıyız", "Yüksek sesle konuşmalıyız", "Koşmalıyız", "Şarkı söylemeliyiz"], 0, "Kütüphanede sessizlik önemlidir"),
    (2, 1, 3, "Sınıfta arkadaşımız konuşurken ne yaparız?", ["Dinleriz", "Sözünü keseriz", "Başka şeyle uğraşırız", "Konuşuruz"], 0, "Konuşanı dinlemek nezakettir"),
    (2, 1, 3, "Okul bahçesinde koşarken nelere dikkat etmeliyiz?", ["Arkadaşlarımıza çarpmamaya", "Hızlı koşmaya", "Bağırmaya", "Yere bakmamaya"], 0, "Başkalarına zarar vermemek önemli"),
    (2, 1, 3, "Ödevimizi ne zaman yapmalıyız?", ["Zamanında", "Ders başlayınca", "Hiç yapmasak da olur", "Arkadaşımıza yaptırırız"], 0, "Ödevler zamanında yapılır"),
    (3, 2, 3, "Okulda 'nöbetçi öğrenci' ne yapar?", ["Sınıf düzenine yardım eder", "Ders anlatır", "Not verir", "Ceza verir"], 0, "Nöbetçi öğrenci sınıf düzenine yardımcı olur"),
    (3, 2, 3, "Grup çalışmasında en önemli şey nedir?", ["İş birliği yapmak", "Tek başına çalışmak", "En hızlı bitirmek", "Konuşmamak"], 0, "Grup çalışması iş birliği gerektirir"),
    (3, 2, 3, "Arkadaşımızla anlaşmazlık yaşarsak ne yapmalıyız?", ["Konuşarak çözmeliyiz", "Kavga etmeliyiz", "Küsmeliyiz", "Bağırmalıyız"], 0, "Sorunlar konuşarak çözülür"),
    (3, 2, 3, "Okulda kaybettiğimiz eşyayı nereye sorarız?", ["Öğretmenimize", "Hiç sormayız", "Eve gideriz", "Ağlarız"], 0, "Öğretmene bildiririz"),
    (3, 2, 3, "Sınıf kuralları neden vardır?", ["Düzenli bir ortam için", "Bizi cezalandırmak için", "Zaman geçirmek için", "Öğretmen istediği için"], 0, "Kurallar düzen sağlar"),
    (4, 2, 3, "Okulda demokratik seçim nasıl yapılır?", ["Oylama ile", "Öğretmen seçer", "En güçlü kazanır", "Kura ile"], 0, "Sınıf başkanı oylamayla seçilir"),
    (4, 2, 3, "Bir arkadaşımız dışlanıyorsa ne yapmalıyız?", ["Oyunumuza dahil etmeliyiz", "Görmezden gelmeliyiz", "Biz de dışlamalıyız", "Gülmeliyiz"], 0, "Kimse dışlanmamalı"),
    (4, 3, 3, "Okul kulüpleri neden vardır?", ["İlgi alanımızı geliştirmek için", "Ders yapmak için", "Not almak için", "Zaman geçirmek için"], 0, "Kulüpler yetenek geliştirir"),
    (5, 3, 3, "Sınıf başkanının görevi nedir?", ["Sınıfı temsil etmek", "Ceza vermek", "Not vermek", "Ders anlatmak"], 0, "Sınıf başkanı sınıfı temsil eder"),
]

# ---------------------------------------------------- 2. EVIMIZDE HAYAT

AILEMIZ = [
    (1, 1, 3, "Annemizin annesi bize ne olur?", ["Anneanne", "Babaanne", "Teyze", "Hala"], 0, "Anne tarafı → anneanne"),
    (1, 1, 3, "Babamızın annesi bize ne olur?", ["Babaanne", "Anneanne", "Teyze", "Yenge"], 0, "Baba tarafı → babaanne"),
    (1, 1, 3, "Annemizin kız kardeşi bize ne olur?", ["Teyze", "Hala", "Yenge", "Kuzen"], 0, "Anne tarafı kız kardeş → teyze"),
    (1, 1, 3, "Babamızın kız kardeşi bize ne olur?", ["Hala", "Teyze", "Yenge", "Kuzen"], 0, "Baba tarafı kız kardeş → hala"),
    (1, 1, 3, "Yemekten sonra tabakları kim toplamalı?", ["Herkes yardım etmeli", "Sadece anne", "Sadece çocuklar", "Kimse"], 0, "Ev işleri paylaşılır"),
    (2, 1, 3, "Annemizin erkek kardeşi bize ne olur?", ["Dayı", "Amca", "Enişte", "Kuzen"], 0, "Anne tarafı erkek kardeş → dayı"),
    (2, 1, 3, "Babamızın erkek kardeşi bize ne olur?", ["Amca", "Dayı", "Enişte", "Kuzen"], 0, "Baba tarafı erkek kardeş → amca"),
    (2, 1, 3, "Odamızı kim toplamalı?", ["Kendimiz", "Annemiz", "Kardeşimiz", "Kimse"], 0, "Kendi odamızdan sorumluyuz"),
    (2, 1, 3, "Musluğu açık bırakırsak ne olur?", ["Su israf olur", "Bir şey olmaz", "Su temizlenir", "Fatura azalır"], 0, "Su tasarrufu önemlidir"),
    (2, 1, 3, "Odadan çıkarken ışığı ne yapmalıyız?", ["Kapatmalıyız", "Açık bırakmalıyız", "Kırmalıyız", "Sökmeliyiz"], 0, "Elektrik tasarrufu"),
    (2, 1, 3, "Evde en önemli kural nedir?", ["Birbirimize saygı", "Yüksek sesle konuşmak", "İstediğimizi yapmak", "Kural olmaması"], 0, "Ailede saygı esastır"),
    (3, 2, 3, "Kardeşimizle oyuncak paylaşırken ne yaparız?", ["Sırayla oynarız", "Kavga ederiz", "Saklarız", "Kırarız"], 0, "Paylaşmak öğrenilir"),
    (3, 2, 3, "Evde tehlikeli olan nedir?", ["Prizle oynamak", "Kitap okumak", "Resim yapmak", "Oyun oynamak"], 0, "Elektrik prizleri tehlikelidir"),
    (3, 2, 3, "Evde yangın çıkarsa ilk ne yapmalıyız?", ["Büyüklere haber vermeli", "Saklanmalıyız", "Su dökmeliyiz", "Beklemeliyiz"], 0, "Hemen büyüklere haber verilir"),
    (3, 2, 3, "Eşyalarımızı nasıl korumalıyız?", ["Dikkatli kullanarak", "Hızlı kullanarak", "Saklayarak", "Kullanmayarak"], 0, "Eşyalar özenle kullanılır"),
    (3, 2, 3, "Ailemizde kararlar nasıl alınmalı?", ["Birlikte konuşarak", "Sadece babam", "Sadece annem", "Kimse karışmaz"], 0, "Aile kararları birlikte alınır"),
    (4, 2, 3, "Harçlığımızı nasıl kullanmalıyız?", ["Planlı harcamalıyız", "Hemen bitirmeliyiz", "Hiç harcamamalıyız", "Kaybetmeliyiz"], 0, "Tasarruf ve planlama"),
    (4, 3, 3, "Aile bütçesi ne demektir?", ["Ailenin gelir-gider planı", "Ailenin evi", "Ailenin arabası", "Ailenin tatili"], 0, "Bütçe = gelir ve giderlerin planı"),
    (4, 3, 3, "Enerji tasarrufu için ne yapabiliriz?", ["Gereksiz ışıkları kapatmak", "Tüm ışıkları açmak", "Klimayı sürekli çalıştırmak", "Kapıyı açık bırakmak"], 0, "Gereksiz kullanımı azaltmak"),
    (5, 3, 3, "Ailemizde iletişim neden önemlidir?", ["Birbirimizi anlamak için", "Zaman geçirmek için", "Gürültü yapmak için", "Tartışmak için"], 0, "İletişim anlayış sağlar"),
]

# ---------------------------------------------------- 3. SAGLIKLI HAYAT

SAGLIGIMIZ = [
    (1, 1, 3, "Dişlerimizi günde kaç kez fırçalamalıyız?", ["En az 2 kez", "Hiç", "Haftada 1", "Ayda 1"], 0, "Sabah ve akşam olmak üzere 2 kez"),
    (1, 1, 3, "Yemekten önce ne yapmalıyız?", ["Ellerimizi yıkamalıyız", "Koşmalıyız", "TV izlemeliyiz", "Uyumalıyız"], 0, "Yemekten önce el yıkanır"),
    (1, 1, 3, "Hangisi sağlıklı bir besindir?", ["Elma", "Çikolata", "Cips", "Gazoz"], 0, "Meyveler sağlıklıdır"),
    (1, 1, 3, "Günde kaç öğün yemek yemeliyiz?", ["3 ana öğün", "1 öğün", "Sürekli", "Hiç"], 0, "Sabah, öğle, akşam"),
    (1, 1, 3, "Hangisi vücudumuzu temiz tutar?", ["Banyo yapmak", "Koşmak", "Uyumak", "Yemek"], 0, "Düzenli banyo"),
    (2, 1, 3, "Günde ne kadar uyumalıyız?", ["9-10 saat", "3 saat", "15 saat", "1 saat"], 0, "Çocuklar 9-10 saat uyumalı"),
    (2, 1, 3, "Kahvaltı neden önemlidir?", ["Güne enerji verir", "Kilo aldırır", "Uyku getirir", "Gereksizdir"], 0, "Kahvaltı günün en önemli öğünüdür"),
    (2, 1, 3, "Hangisi bize enerji verir?", ["Ekmek", "Su", "Tuz", "Buz"], 0, "Karbonhidratlar enerji verir"),
    (2, 1, 3, "Spor yapmak bize ne kazandırır?", ["Sağlıklı bir vücut", "Yorgunluk", "Hastalık", "Hiçbir şey"], 0, "Spor sağlığı korur"),
    (2, 1, 3, "Günde ne kadar su içmeliyiz?", ["Bol miktarda", "Hiç", "Bir bardak", "Sadece susayınca"], 0, "Bol su içmek gerekir"),
    (2, 2, 3, "Hasta olunca nereye gideriz?", ["Doktora", "Markete", "Parka", "Sinemaya"], 0, "Hastalıkta doktora gidilir"),
    (3, 2, 3, "Hangisi bulaşıcı hastalıktan korur?", ["El yıkamak", "Koşmak", "Uyumak", "Yemek"], 0, "El hijyeni hastalıkları önler"),
    (3, 2, 3, "Öksürürken ne yapmalıyız?", ["Ağzımızı kapatmalıyız", "Yüksek sesle öksürmeliyiz", "Kimseye söylememeliyiz", "Hiçbir şey"], 0, "Mikropların yayılmasını önler"),
    (3, 2, 3, "Hangisi dişlerimize zarar verir?", ["Çok şekerli yiyecek", "Süt", "Peynir", "Su"], 0, "Şeker diş çürüğü yapar"),
    (3, 2, 3, "İlaçları kim vermeli?", ["Büyüklerimiz", "Kendimiz", "Arkadaşımız", "Kimse"], 0, "İlaç yalnızca büyüklerin bilgisiyle alınır"),
    (3, 2, 3, "Hangisi dengeli beslenme örneğidir?", ["Sebze, meyve, protein birlikte", "Sadece makarna", "Sadece tatlı", "Sadece et"], 0, "Çeşitli besinler bir arada"),
    (4, 2, 3, "Aşı ne işe yarar?", ["Hastalıklardan korur", "Hasta eder", "Uyku getirir", "Kilo aldırır"], 0, "Aşı bağışıklık kazandırır"),
    (4, 3, 3, "Ekranı uzun süre izlemek neye zarar verir?", ["Gözlerimize", "Ayaklarımıza", "Saçımıza", "Tırnağımıza"], 0, "Uzun ekran süresi göz sağlığını bozar"),
    (4, 3, 3, "Vitamin en çok hangisinde bulunur?", ["Meyve ve sebzede", "Cipste", "Gazozda", "Şekerlemede"], 0, "Sebze ve meyveler vitamin deposudur"),
    (5, 3, 3, "İlk yardımda ilk yapılması gereken nedir?", ["112'yi aramak", "Hastayı taşımak", "Su vermek", "Beklemek"], 0, "Önce yardım çağrılır"),
]

# ---------------------------------------------------- 4. GUVENLI HAYAT

GUVENLIGIMIZ = [
    (1, 1, 3, "Acil durumda hangi numarayı ararız?", ["112", "155", "110", "182"], 0, "112 acil çağrı merkezi"),
    (1, 1, 3, "Karşıdan karşıya nereden geçeriz?", ["Yaya geçidinden", "İstediğimiz yerden", "Koşarak", "Araçların arasından"], 0, "Yaya geçidi kullanılır"),
    (1, 1, 3, "Trafik ışığında hangi renkte geçeriz?", ["Yeşil", "Kırmızı", "Sarı", "Mavi"], 0, "Yeşil ışık geçiş demektir"),
    (1, 1, 3, "Trafik ışığında hangi renkte dururuz?", ["Kırmızı", "Yeşil", "Mavi", "Beyaz"], 0, "Kırmızı ışıkta durulur"),
    (1, 1, 3, "Arabada nerede oturmalıyız?", ["Arka koltukta", "Ön koltukta", "Şoförün kucağında", "Bagajda"], 0, "Çocuklar arka koltukta oturur"),
    (2, 1, 3, "Arabada ne takmalıyız?", ["Emniyet kemeri", "Şapka", "Gözlük", "Eldiven"], 0, "Emniyet kemeri hayat kurtarır"),
    (2, 1, 3, "Bisiklete binerken ne takmalıyız?", ["Kask", "Şapka", "Gözlük", "Atkı"], 0, "Kask kafamızı korur"),
    (2, 1, 3, "Tanımadığımız biri bizi çağırırsa ne yaparız?", ["Gitmeyiz, büyüklere söyleriz", "Gideriz", "Konuşuruz", "Adres veririz"], 0, "Tanımadığımız kişilerle gitmeyiz"),
    (2, 1, 3, "Yolda yürürken nerede yürürüz?", ["Kaldırımda", "Yolun ortasında", "Araçların arasında", "Koşarak"], 0, "Yayalar kaldırımda yürür"),
    (2, 2, 3, "Deprem olduğunda ne yaparız?", ["Çök-Kapan-Tutun", "Koşarız", "Bağırırız", "Pencereden atlarız"], 0, "Çök, kapan, tutun"),
    (2, 2, 3, "Yangında asansör kullanılır mı?", ["Hayır, merdiven kullanılır", "Evet", "Bazen", "Fark etmez"], 0, "Yangında asansör kullanılmaz"),
    (3, 2, 3, "Bu işaret ne anlama gelir? 🚸", ["Okul geçidi", "Hastane", "Park", "Dur"], 0, "Okul geçidi işareti"),
    (3, 2, 3, "İtfaiye hangi numaradan aranır?", ["112", "155", "156", "153"], 0, "Tüm acil durumlar 112"),
    (3, 2, 3, "Yolda top peşinden koşarsak ne olur?", ["Kaza olabilir", "Bir şey olmaz", "Top kaybolur", "Eğlenceli olur"], 0, "Yola çıkmak tehlikelidir"),
    (3, 2, 3, "Elektrik prizine ne sokmamalıyız?", ["Hiçbir şey", "Kalem", "Tel", "Parmak"], 0, "Prize hiçbir şey sokulmaz"),
    (3, 2, 3, "Yabancı birinin verdiği yiyeceği yer miyiz?", ["Hayır", "Evet", "Bazen", "Şekerse yeriz"], 0, "Tanımadığımız kişiden bir şey alınmaz"),
    (4, 2, 3, "Deprem çantasında ne olmalı?", ["Su, yiyecek, el feneri", "Oyuncak", "Kitap", "Televizyon"], 0, "Temel ihtiyaç malzemeleri"),
    (4, 3, 3, "Yangın çıkarsa nasıl hareket ederiz?", ["Eğilerek çıkarız", "Koşarak çıkarız", "Saklanırız", "Bekleriz"], 0, "Duman yukarıda toplanır, eğilerek çıkılır"),
    (4, 3, 3, "İnternette tanımadığımız kişiye ne vermeyiz?", ["Kişisel bilgilerimizi", "Selam", "Emoji", "Hiçbir şey"], 0, "Kişisel bilgiler paylaşılmaz"),
    (5, 3, 3, "Depremden sonra ilk ne yapmalıyız?", ["Güvenli alana çıkmak", "Eşya toplamak", "Fotoğraf çekmek", "Beklemek"], 0, "Önce güvenli alana geçilir"),
]

# ---------------------------------------------------- 5. ULKEMIZDE HAYAT

ULKEMIZ = [
    (1, 1, 3, "Ülkemizin adı nedir?", ["Türkiye", "Almanya", "Fransa", "İtalya"], 0, "Türkiye Cumhuriyeti"),
    (1, 1, 3, "Bayrağımızın rengi nedir?", ["Kırmızı", "Mavi", "Yeşil", "Sarı"], 0, "Al bayrağımız"),
    (1, 1, 3, "Bayrağımızda ne vardır?", ["Ay ve yıldız", "Güneş", "Ağaç", "Kartal"], 0, "Ay yıldız"),
    (1, 1, 3, "Cumhuriyetimizin kurucusu kimdir?", ["Mustafa Kemal Atatürk", "Fatih Sultan Mehmet", "Yavuz Sultan Selim", "Osman Bey"], 0, "Mustafa Kemal Atatürk"),
    (1, 1, 3, "23 Nisan hangi bayramdır?", ["Ulusal Egemenlik ve Çocuk Bayramı", "Zafer Bayramı", "Cumhuriyet Bayramı", "Gençlik Bayramı"], 0, "23 Nisan Çocuk Bayramı"),
    (2, 1, 3, "29 Ekim hangi bayramdır?", ["Cumhuriyet Bayramı", "Çocuk Bayramı", "Zafer Bayramı", "Gençlik Bayramı"], 0, "29 Ekim Cumhuriyet Bayramı"),
    (2, 1, 3, "Milli marşımızın adı nedir?", ["İstiklal Marşı", "Gençlik Marşı", "Onuncu Yıl Marşı", "Cumhuriyet Marşı"], 0, "İstiklal Marşı"),
    (2, 1, 3, "Başkentimiz neresidir?", ["Ankara", "İstanbul", "İzmir", "Bursa"], 0, "Ankara"),
    (2, 1, 3, "Atatürk nerede doğmuştur?", ["Selanik", "İstanbul", "Ankara", "İzmir"], 0, "Selanik'te doğdu"),
    (2, 2, 3, "19 Mayıs hangi bayramdır?", ["Gençlik ve Spor Bayramı", "Çocuk Bayramı", "Cumhuriyet Bayramı", "Zafer Bayramı"], 0, "19 Mayıs Gençlik ve Spor Bayramı"),
    (2, 2, 3, "30 Ağustos hangi bayramdır?", ["Zafer Bayramı", "Cumhuriyet Bayramı", "Çocuk Bayramı", "Gençlik Bayramı"], 0, "30 Ağustos Zafer Bayramı"),
    (3, 2, 3, "İstiklal Marşı'nın şairi kimdir?", ["Mehmet Akif Ersoy", "Namık Kemal", "Ziya Gökalp", "Yahya Kemal"], 0, "Mehmet Akif Ersoy"),
    (3, 2, 3, "Cumhuriyet hangi yıl ilan edilmiştir?", ["1923", "1920", "1938", "1919"], 0, "29 Ekim 1923"),
    (3, 2, 3, "Atatürk'ün annesinin adı nedir?", ["Zübeyde Hanım", "Fatma Hanım", "Ayşe Hanım", "Makbule Hanım"], 0, "Zübeyde Hanım"),
    (3, 2, 3, "Bayrağımıza nasıl davranmalıyız?", ["Saygı göstermeliyiz", "Yere atmalıyız", "Kirletmeliyiz", "Görmezden gelmeliyiz"], 0, "Bayrak saygı görür"),
    (3, 2, 3, "Atatürk çocuklara hangi bayramı armağan etmiştir?", ["23 Nisan", "29 Ekim", "19 Mayıs", "30 Ağustos"], 0, "23 Nisan çocuklara armağan"),
    (4, 2, 3, "Türkiye Büyük Millet Meclisi ne zaman açılmıştır?", ["23 Nisan 1920", "29 Ekim 1923", "19 Mayıs 1919", "30 Ağustos 1922"], 0, "23 Nisan 1920"),
    (4, 3, 3, "Atatürk'ün 'Yurtta sulh, cihanda sulh' sözü ne anlatır?", ["Barışın önemini", "Savaşın önemini", "Ticaretin önemini", "Eğitimin önemini"], 0, "Barış ilkesi"),
    (4, 3, 3, "Kurtuluş Savaşı hangi tarihte başlamıştır?", ["19 Mayıs 1919", "29 Ekim 1923", "23 Nisan 1920", "30 Ağustos 1922"], 0, "19 Mayıs 1919 Samsun"),
    (5, 3, 3, "Atatürk'ün kabri nerededir?", ["Anıtkabir", "Dolmabahçe", "Topkapı", "Çankaya"], 0, "Anıtkabir, Ankara"),
]

# ---------------------------------------------------- 6. DOGADA HAYAT

DOGA_CEVRE = [
    (1, 1, 3, "Hangisi canlıdır?", ["Ağaç", "Taş", "Masa", "Kalem"], 0, "Ağaç canlıdır, büyür"),
    (1, 1, 3, "Hangisi cansızdır?", ["Kaya", "Kedi", "Çiçek", "Kuş"], 0, "Kaya cansızdır"),
    (1, 1, 3, "Kaç mevsim vardır?", ["4", "3", "5", "2"], 0, "İlkbahar, yaz, sonbahar, kış"),
    (1, 1, 3, "Balık nerede yaşar?", ["Suda", "Ağaçta", "Toprakta", "Havada"], 0, "Balıklar suda yaşar"),
    (1, 1, 3, "İneğin yavrusuna ne denir?", ["Buzağı", "Kuzu", "Tay", "Civciv"], 0, "İnek → buzağı"),
    (1, 1, 3, "Koyunun yavrusuna ne denir?", ["Kuzu", "Buzağı", "Tay", "Yavru"], 0, "Koyun → kuzu"),
    (1, 1, 3, "Atın yavrusuna ne denir?", ["Tay", "Kuzu", "Buzağı", "Civciv"], 0, "At → tay"),
    (2, 1, 3, "Tavuğun yavrusuna ne denir?", ["Civciv", "Kuzu", "Tay", "Buzağı"], 0, "Tavuk → civciv"),
    (2, 1, 3, "Bitkiler büyümek için neye ihtiyaç duyar?", ["Su ve güneş", "Sadece toprak", "Sadece hava", "Hiçbir şey"], 0, "Su, güneş, toprak, hava"),
    (2, 1, 3, "Hangi mevsimde yapraklar dökülür?", ["Sonbahar", "İlkbahar", "Yaz", "Kış"], 0, "Sonbaharda yapraklar dökülür"),
    (2, 1, 3, "Kağıt hangi kutuya atılır?", ["Mavi", "Sarı", "Yeşil", "Kırmızı"], 0, "Mavi kutu: kağıt"),
    (2, 1, 3, "Cam şişe hangi kutuya atılır?", ["Yeşil", "Mavi", "Sarı", "Siyah"], 0, "Yeşil kutu: cam"),
    (2, 1, 3, "Plastik hangi kutuya atılır?", ["Sarı", "Mavi", "Yeşil", "Kırmızı"], 0, "Sarı kutu: plastik/metal"),
    (2, 2, 3, "Kelebek hangi hayvan grubundandır?", ["Böcek", "Kuş", "Balık", "Memeli"], 0, "Kelebek bir böcektir"),
    (3, 2, 3, "Hangisi memeli hayvandır?", ["Kedi", "Kartal", "Yılan", "Balık"], 0, "Kedi memelidir, süt emer"),
    (3, 2, 3, "Hangi hayvan yumurtayla çoğalır?", ["Tavuk", "Kedi", "İnek", "Köpek"], 0, "Kuşlar yumurtlar"),
    (3, 2, 3, "Ağaçlar bize ne verir?", ["Oksijen", "Karbondioksit", "Duman", "Toz"], 0, "Ağaçlar oksijen üretir"),
    (3, 2, 3, "Geri dönüşüm neden önemlidir?", ["Doğayı korur", "Zaman kaybıdır", "Para harcatır", "Gereksizdir"], 0, "Kaynakları korur"),
    (3, 2, 3, "Hangisi bitkinin bölümü değildir?", ["Kanat", "Kök", "Gövde", "Yaprak"], 0, "Bitkilerde kanat yoktur"),
    (3, 2, 3, "Kar hangi mevsimde yağar?", ["Kış", "Yaz", "İlkbahar", "Sonbahar"], 0, "Kışın kar yağar"),
    (4, 2, 3, "Bitkinin su ve besini alan bölümü hangisidir?", ["Kök", "Yaprak", "Çiçek", "Meyve"], 0, "Kök topraktan su ve mineral alır"),
    (4, 3, 3, "Hangisi doğayı kirletir?", ["Çöp atmak", "Ağaç dikmek", "Geri dönüşüm", "Su tasarrufu"], 0, "Çöp doğaya zarar verir"),
    (4, 3, 3, "Suyun buharlaşıp bulut olmasına ne denir?", ["Su döngüsü", "Yağmur", "Rüzgar", "Kar"], 0, "Su döngüsü"),
    (4, 3, 3, "Hangisi yenilenebilir enerji kaynağıdır?", ["Güneş", "Kömür", "Petrol", "Doğalgaz"], 0, "Güneş tükenmez"),
    (5, 3, 3, "Besin zincirinde ilk sırada kim vardır?", ["Bitkiler", "Etçiller", "Otçullar", "İnsanlar"], 0, "Bitkiler üreticidir"),
    (5, 3, 3, "Ormanların azalması neye yol açar?", ["Havanın kirlenmesine", "Havanın temizlenmesine", "Yağmurun artmasına", "Hiçbir şeye"], 0, "Ormanlar havayı temizler"),
]
