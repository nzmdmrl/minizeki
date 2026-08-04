"""
OKUMA VE ANLAMA — EK METINLER (Parti 2)

20 yeni hikaye, her sinifa 5 tane.
Mevcut metinlerle TEMA CAKISMASI yok:
  Var olanlar: kedi/top/cicek/kus/kar/arkadas (1), yagmur/silgi/bahce/yol/
  kumbara/kutuphane (2), bisiklet/kitaplik/kirlangic/not/sokak kedisi (3),
  bilim fuari/saat/voleybol/su/harita (4)

TASARIM KURALLARI:
  - Duygusal cekirdegi olan hikaye; sadece olay siralamasi degil
    (cikarim sorusu ancak boyle anlamli olur)
  - Siddet, korku, kayip yok
  - 1. sinif: kisa cumle, gunluk kelime, somut
  - 4. sinif: bir fikir ya da ic degisim tasir

SORULAR: her metinde 2 bilgi + 2 cikarim + 1 kelime

Format:
  (id, baslik, metin, sinif_min, sinif_max, seviye, [sorular])
  soru: (tur, soru_metni, [siklar], dogru_index, aciklama)

NOT: Dogru cevap burada ILK siktadir (yazarken okunakli olsun diye).
     seed.py yuklerken siklari KARISTIRIR.
"""

# ==================================================== 1. SINIF (22-32 kelime)

METINLER_1_EK = [
    (
        "ayakkabi_bagi", "Bağcıklarım",
        """Bugün ayakkabımı kendim bağladım.
Önce bir düğüm attım. Sonra iki kulak yaptım.
Annem gülümsedi. Ben çok sevindim.
Artık her sabah kendim bağlıyorum.""",
        1, 2, 1,
        [
            ("bilgi", "Çocuk ne yaptı?",
             ["Ayakkabısını bağladı", "Yemek yaptı", "Resim çizdi", "Kitap okudu"], 0,
             "Ayakkabımı kendim bağladım"),
            ("bilgi", "Önce ne yaptı?",
             ["Bir düğüm attı", "İki kulak yaptı", "Koştu", "Uyudu"], 0,
             "Önce bir düğüm attım"),
            ("cikarim", "Anne neden gülümsedi?",
             ["Çocuğu başardığı için", "Acıktığı için", "Yorulduğu için", "Şaşırdığı için"], 0,
             "Çocuk kendi başardı"),
            ("cikarim", "Çocuk şimdi ne yapabiliyor?",
             ["Yardımsız ayakkabı bağlamayı", "Yemek pişirmeyi", "Araba kullanmayı", "Uçmayı"], 0,
             "Artık her sabah kendim"),
            ("kelime", "\"Düğüm\" ne demektir?",
             ["İpin bağlanmış hâli", "Ayakkabı", "Çorap", "Kutu"], 0,
             "İpi bağlayınca düğüm olur"),
        ],
    ),
    (
        "sut_bardagi", "Devrilen Bardak",
        """Kahvaltıda sütümü devirdim. Bardak yan yattı.
Masa ıslandı. Süt yere damladı.
Korktum. Belki kızarlar diye düşündüm.
Babam mutfaktan bir bez getirdi.
Birlikte sildik. Hiç kızmadı.
"Herkes döker," dedi. Rahatladım.""",
        1, 2, 2,
        [
            ("bilgi", "Çocuk ne devirdi?",
             ["Sütünü", "Çayını", "Suyunu", "Tabağını"], 0, "Sütümü devirdim"),
            ("bilgi", "Baba ne getirdi?",
             ["Bez", "Süt", "Tabak", "Havlu"], 0, "Babam bez getirdi"),
            ("cikarim", "Çocuk neden korktu?",
             ["Kızacaklarını düşündüğü için", "Karanlıktan", "Sütü sevmediği için", "Acıktığı için"], 0,
             "Belki kızarlar diye düşündüm"),
            ("cikarim", "Baba nasıl davrandı?",
             ["Anlayışlı", "Kızgın", "İlgisiz", "Üzgün"], 0,
             "Birlikte sildi, herkes döker dedi"),
            ("kelime", "\"Rahatlamak\" ne demektir?",
             ["Korkusu geçmek", "Yorulmak", "Acıkmak", "Üzülmek"], 0,
             "Rahatlamak = içi rahat etmek"),
        ],
    ),
    (
        "sarki_soyleme", "Sınıfta Şarkı",
        """Öğretmenimiz şarkı söyleyelim dedi.
Herkes başladı. Ben utandım.
Sesim çok kısık çıktı.
Yanımda oturan Ayşe elimi tuttu.
Bana gülümsedi. Beraber söyledik.
Yavaş yavaş sesim yükseldi.""",
        1, 2, 2,
        [
            ("bilgi", "Öğretmen ne dedi?",
             ["Şarkı söyleyelim", "Kitap okuyalım", "Resim yapalım", "Oyun oynayalım"], 0,
             "Şarkı söyleyelim dedi"),
            ("bilgi", "Ayşe ne yaptı?",
             ["Elini tuttu", "Uzaklaştı", "Güldü", "Sustu"], 0, "Elimi tuttu"),
            ("cikarim", "Çocuğun sesi neden önce kısık çıktı?",
             ["Utandığı için", "Hasta olduğu için", "Yorgun olduğu için", "Susadığı için"], 0,
             "Ben utandım"),
            ("cikarim", "Sesi neden sonra yükseldi?",
             ["Arkadaşı yanında olduğu için", "Bağırdığı için", "Kızdığı için", "Koştuğu için"], 0,
             "Beraber söyleyince cesaretlendi"),
            ("kelime", "\"Utanmak\" ne demektir?",
             ["Çekingen hissetmek", "Kızmak", "Sevinmek", "Uyumak"], 0,
             "Utanmak = çekinmek"),
        ],
    ),
    (
        "karinca_yolu", "Karıncalar",
        """Bahçede karıncalar gördüm. Sıra sıra yürüyorlardı.
Biri küçük bir ekmek parçası taşıyordu.
Çok ağırdı. Bir karınca daha geldi.
İkisi birlikte taşıdılar.""",
        1, 2, 2,
        [
            ("bilgi", "Karınca ne taşıyordu?",
             ["Ekmek parçası", "Yaprak", "Taş", "Kum"], 0, "Küçük bir ekmek parçası"),
            ("bilgi", "Karıncalar nasıl yürüyordu?",
             ["Sıra sıra", "Dağınık", "Koşarak", "Zıplayarak"], 0, "Sıra sıra yürüyorlardı"),
            ("cikarim", "İkinci karınca neden geldi?",
             ["Yardım etmek için", "Yemek için", "Oynamak için", "Uyumak için"], 0,
             "Ağır olunca birlikte taşıdılar"),
            ("cikarim", "Bu hikâye bize ne anlatıyor?",
             ["Birlikte iş kolaylaşır", "Karıncalar küçüktür", "Ekmek ağırdır", "Bahçe güzeldir"], 0,
             "İkisi birlikte taşıdılar"),
            ("kelime", "\"Ağır\" ne demektir?",
             ["Taşıması zor", "Hafif", "Küçük", "Renkli"], 0, "Ağır = hafif değil"),
        ],
    ),
    (
        "sira_bekleme", "Kaydırakta",
        """Parkta kaydırağa gittim. Önümde üç çocuk vardı.
Sıramı bekledim. Biraz uzun sürdü.
Sonra sıra bana geldi. İki kez kaydım.
Beklemek zor ama sıra herkesin.""",
        1, 2, 2,
        [
            ("bilgi", "Çocuğun önünde kaç kişi vardı?",
             ["Üç", "İki", "Dört", "Beş"], 0, "Önümde üç çocuk vardı"),
            ("bilgi", "Sırası gelince kaç kez kaydı?",
             ["İki", "Bir", "Üç", "Dört"], 0, "İki kez kaydım"),
            ("cikarim", "Çocuk beklerken ne hissetti?",
             ["Sabırsızlık", "Korku", "Öfke", "Üzüntü"], 0, "Biraz uzun sürdü"),
            ("cikarim", "\"Sıra herkesin\" ne anlatıyor?",
             ["Herkesin hakkı olduğunu", "Sıranın uzun olduğunu", "Kaydırağın güzel olduğunu", "Parkın büyük olduğunu"], 0,
             "Adil paylaşım"),
            ("kelime", "\"Sıra beklemek\" ne demektir?",
             ["Kendi zamanını beklemek", "Koşmak", "Öne geçmek", "Vazgeçmek"], 0,
             "Sırayla ilerlemek"),
        ],
    ),
]

# ==================================================== 2. SINIF (48-65 kelime)

METINLER_2_EK = [
    (
        "unutulan_beslenme", "Unuttuğum Beslenme",
        """Sabah acele çıktım. Otobüsü kaçırmamak için koştum.
Beslenme çantamı mutfak masasında unuttum.

Öğle arasında karnım acıktı. Çantamı açtım, bomboştu.
Sırada sessizce oturdum. Kimseye bir şey söylemedim.

Yanımda oturan Emre fark etti. Sandviçini çıkardı
ve ortadan ikiye böldü.

"Yarısı senin," dedi. Hiç düşünmeden verdi.

Bugün ben de çantama bir tane fazla koydum.
Belki birinin ihtiyacı olur diye.""",
        2, 3, 2,
        [
            ("bilgi", "Çocuk ne unuttu?",
             ["Beslenme çantasını", "Kitabını", "Kalemini", "Anahtarını"], 0,
             "Beslenme çantamı masada unuttum"),
            ("bilgi", "Emre ne yaptı?",
             ["Sandviçini paylaştı", "Öğretmene söyledi", "Güldü", "Uzaklaştı"], 0,
             "Sandviçini ikiye böldü"),
            ("cikarim", "Çocuk neden kimseye söylemedi?",
             ["Utandığı için", "Aç olmadığı için", "Konuşamadığı için", "Unuttuğu için"], 0,
             "Sessizce oturdu"),
            ("cikarim", "Çocuk neden fazladan bir tane götürüyor?",
             ["Aynı iyiliği yapmak istediği için", "Çok acıktığı için", "Öğretmen istediği için", "Sandviç sevdiği için"], 0,
             "Belki birinin ihtiyacı olur"),
            ("kelime", "\"İhtiyaç\" ne demektir?",
             ["Gerek duyulan şey", "İstenen oyuncak", "Fazla olan şey", "Kaybolan eşya"], 0,
             "İhtiyaç = gereksinim"),
        ],
    ),
    (
        "balkon_domates", "Balkondaki Domates",
        """Annem balkona büyük bir saksı koydu. İçine toprak doldurduk.
Sonra küçük bir domates fidesi diktik.

Ben her akşam düzenli suladım. İlk hafta hiçbir şey olmadı.
Sabırsızlandım ama sulamayı bırakmadım.

İkinci hafta küçük yeşil topaklar çıktı. Her gün bakıp
büyüdüklerini gördüm. Yavaş yavaş kızarmaya başladılar.

Sonunda üç tane domates topladık. Akşam salataya koyduk.

Marketten aldığımız domateslerden daha lezzetli geldi bana.""",
        2, 3, 3,
        [
            ("bilgi", "Balkona ne dikildi?",
             ["Domates fidesi", "Gül", "Çilek", "Nane"], 0, "Domates fidesi dikti"),
            ("bilgi", "Kaç domates toplandı?",
             ["Üç", "İki", "Beş", "Bir"], 0, "Üç domates topladık"),
            ("cikarim", "Domatesler neden daha lezzetli geldi?",
             ["Kendi emeğiyle yetiştiği için", "Daha büyük olduğu için", "Şekerli olduğu için", "Taze olduğu için"], 0,
             "Emek verince değerli olur"),
            ("cikarim", "Çocuk ilk hafta ne hissetmiş olabilir?",
             ["Sabırsızlık", "Korku", "Öfke", "Üzüntü"], 0, "Hiçbir şey olmadı"),
            ("kelime", "\"Fide\" ne demektir?",
             ["Dikilmek için yetiştirilmiş küçük bitki", "Tohum", "Meyve", "Yaprak"], 0,
             "Fide = küçük bitki"),
        ],
    ),
    (
        "yanlis_otobus", "Yanlış Otobüs",
        """Dedemle şehre gittik. Dönüşte otobüse bindik.

Birkaç durak sonra dedem etrafına baktı.
"Galiba yanlış otobüse bindik," dedi.

Korktum. Dedem sakin sakin şoföre sordu.
Şoför bize doğru durağı tarif etti.

İndik, karşıya geçtik, doğru otobüsü bekledik.

Dedem, "Hata yapmak kötü değil," dedi.
"Fark edip düzeltmek önemli."

Eve on dakika geç geldik. O kadar.""",
        2, 3, 3,
        [
            ("bilgi", "Dede fark edince ne yaptı?",
             ["Şoföre sordu", "Bağırdı", "İndi", "Bekledi"], 0, "Sakin sakin şoföre sordu"),
            ("bilgi", "Eve ne kadar geç geldiler?",
             ["On dakika", "Bir saat", "İki saat", "Yarım saat"], 0, "Eve on dakika geç geldik"),
            ("cikarim", "Çocuk neden korktu?",
             ["Kaybolduklarını sandığı için", "Otobüs hızlı olduğu için", "Dedesi kızdığı için", "Karanlık olduğu için"], 0,
             "Yanlış otobüs = kaybolma korkusu"),
            ("cikarim", "Dedenin sözü ne anlatıyor?",
             ["Hatayı düzeltmenin önemli olduğunu", "Otobüslerin karışık olduğunu", "Şoförlerin yardımsever olduğunu", "Şehrin büyük olduğunu"], 0,
             "Fark edip düzeltmek önemli"),
            ("kelime", "\"Tarif etmek\" ne demektir?",
             ["Yolu anlatmak", "Yemek yapmak", "Sormak", "Göstermek"], 0,
             "Tarif = anlatarak yol gösterme"),
        ],
    ),
    (
        "kirik_kalemtiras", "Kalemtıraş",
        """Sınıfta bir tane kalemtıraş vardı. Herkes onu kullanıyordu.

Bir gün kalemtıraş kırıldı. Kimse "ben kırdım" demedi.

Öğretmenimiz kızmadı. Sadece şunu sordu:
"Ortak eşyaya nasıl davranmalıyız?"

Uzun uzun konuştuk. Sonra bir karar aldık:
Herkes kendi kalemtıraşını getirecek, biri de sınıfta duracak.

O günden sonra hiçbir eşya kırılmadı.

Çünkü artık herkesin sorumluluğu vardı.""",
        2, 3, 3,
        [
            ("bilgi", "Sınıfta kaç kalemtıraş vardı?",
             ["Bir tane", "İki tane", "Hiç yoktu", "Herkeste bir tane"], 0,
             "Bir tane kalemtıraş vardı"),
            ("bilgi", "Öğretmen ne yaptı?",
             ["Soru sordu", "Kızdı", "Ceza verdi", "Yeni aldı"], 0,
             "Kızmadı, sadece sordu"),
            ("cikarim", "Kimse neden \"ben kırdım\" demedi?",
             ["Korktukları için", "Bilmedikleri için", "Umursamadıkları için", "Görmedikleri için"], 0,
             "Suçlanma korkusu"),
            ("cikarim", "Neden artık eşya kırılmıyor?",
             ["Herkes kendi eşyasından sorumlu olduğu için", "Kalemtıraş sağlam olduğu için", "Öğretmen izlediği için", "Kimse kullanmadığı için"], 0,
             "Son cümle söylüyor"),
            ("kelime", "\"Ortak eşya\" ne demektir?",
             ["Herkesin kullandığı eşya", "Kişisel eşya", "Yeni eşya", "Pahalı eşya"], 0,
             "Ortak = hepimizin"),
        ],
    ),
    (
        "gece_lambasi", "Gece Lambası",
        """Küçük kardeşim karanlıkta uyuyamıyordu. Her gece ağlıyordu.

Babam ona küçük bir gece lambası aldı. Yıldız şeklindeydi.
Duvara sarı ışıklar düşürüyordu.

İlk gece kardeşim lambaya baktı, baktı ve uyudu.

Şimdi ben de o ışıkta uyuyorum. Meğer ben de seviyormuşum.

Bazen küçük bir şey, büyük bir sorunu çözüyor.""",
        2, 3, 3,
        [
            ("bilgi", "Lamba ne şeklindeydi?",
             ["Yıldız", "Ay", "Kalp", "Çiçek"], 0, "Yıldız şeklindeydi"),
            ("bilgi", "Kardeş neden ağlıyordu?",
             ["Karanlıkta uyuyamadığı için", "Acıktığı için", "Hasta olduğu için", "Üşüdüğü için"], 0,
             "Karanlıkta uyuyamıyordu"),
            ("cikarim", "Anlatıcı lambayla ilgili ne fark etti?",
             ["Kendisinin de sevdiğini", "Bozuk olduğunu", "Pahalı olduğunu", "Gereksiz olduğunu"], 0,
             "Meğer ben de seviyormuşum"),
            ("cikarim", "Son cümle ne anlatıyor?",
             ["Basit çözümlerin işe yarayabildiğini", "Lambaların ucuz olduğunu", "Kardeşlerin ağladığını", "Gecenin uzun olduğunu"], 0,
             "Küçük şey, büyük sorun"),
            ("kelime", "\"Meğer\" ne demektir?",
             ["Sonradan anlaşıldı ki", "Belki", "Asla", "Her zaman"], 0,
             "Meğer = sonradan fark edilen"),
        ],
    ),
]

# ==================================================== 3. SINIF (68-85 kelime)

METINLER_3_EK = [
    (
        "yuzme_dersi", "Suya İlk Adım",
        """Yaz tatilinde yüzme kursuna yazıldım. İlk gün havuzun kenarında
durdum ve aşağı baktım. Su bana çok derin göründü.

Hocamız yanıma geldi. "Kimse seni itmeyecek," dedi.
"Hazır olduğunda kendin gireceksin."

Diğer çocuklar birer birer girdi. Ben on beş dakika kenarda
oturdum ve onları izledim. Kimse bana bir şey demedi,
kimse acele ettirmedi.

Sonra ayaklarımı suya soktum. Düşündüğüm kadar soğuk değildi.
Yavaş yavaş merdivenden aşağı indim.

O gün sadece kenarda tutundum. Yüzemedim ama girdim.

İkinci haftanın sonunda havuzun bir ucundan diğerine yüzüyordum.
Hocam haklıymış: Zorla değil, hazır olunca oluyormuş.""",
        3, 4, 3,
        [
            ("bilgi", "Çocuk ilk gün kaç dakika kenarda oturdu?",
             ["On beş", "Beş", "Otuz", "Kırk"], 0, "On beş dakika kenarda oturdum"),
            ("bilgi", "Hoca ne söyledi?",
             ["Kimsenin onu itmeyeceğini", "Hemen girmesi gerektiğini", "Eve gitmesini", "Yüzme bilmesi gerektiğini"], 0,
             "Kimse seni itmeyecek"),
            ("cikarim", "Çocuk neden hemen giremedi?",
             ["Korktuğu için", "Üşüdüğü için", "Yorgun olduğu için", "İstemediği için"], 0,
             "Su çok derin göründü"),
            ("cikarim", "Hocanın yaklaşımı neden işe yaradı?",
             ["Çocuğa zaman tanıdığı için", "Sert davrandığı için", "Ödül verdiği için", "Zorladığı için"], 0,
             "Hazır olunca oldu"),
            ("kelime", "\"Tutunmak\" ne demektir?",
             ["Bir yere sıkıca yapışmak", "Yüzmek", "Dalmak", "Zıplamak"], 0,
             "Tutunmak = sıkıca kavramak"),
        ],
    ),
    (
        "eski_bisiklet", "Komşunun Bisikleti",
        """Alt kattaki Mehmet abi bisikletini satacağını söyledi. Bisiklet
eskiydi ama sağlamdı. Zinciri yağlanmış, lastikleri yeniydi.

Babam bir teklif yaptı: "Biriktirdiğin paranın yarısını verirsen
ben de kalan yarısını veririm."

Üç ay boyunca harçlığımı biriktirdim. Arkadaşlarım sinemaya
giderken ben gitmedim. Kantinden şeker almadım. Bazen zor oldu.

Bisikleti aldığımız gün Mehmet abi bir de zil hediye etti.
Gidona kendi elleriyle taktı.

Şimdi her sabah okula bisikletle gidiyorum.

Arkadaşlarımın bisikletleri benimkinden yeni ve parlak.
Ama hiçbiri kendi biriktirdiği parayla almadı.

Bu fark bana yetiyor.""",
        3, 4, 4,
        [
            ("bilgi", "Kaç ay biriktirdi?",
             ["Üç", "İki", "Altı", "Bir"], 0, "Üç ay boyunca"),
            ("bilgi", "Mehmet abi ne hediye etti?",
             ["Zil", "Kask", "Sepet", "Pompa"], 0, "Bir de zil hediye etti"),
            ("cikarim", "Çocuk neden sinemaya gitmedi?",
             ["Para biriktirdiği için", "Sinemayı sevmediği için", "Vakti olmadığı için", "Yasak olduğu için"], 0,
             "Harçlığını biriktiriyordu"),
            ("cikarim", "\"Bu fark bana yetiyor\" ne anlatıyor?",
             ["Kendi emeğiyle almanın gurur verdiğini", "Bisikletin eski olduğunu", "Arkadaşlarını kıskandığını", "Yeni bisiklet istediğini"], 0,
             "Emeğin verdiği gurur"),
            ("kelime", "\"Sağlam\" ne demektir?",
             ["Bozulmamış, dayanıklı", "Yeni", "Pahalı", "Hızlı"], 0,
             "Sağlam = dayanıklı"),
        ],
    ),
    (
        "yagmur_solucani", "Kaldırımdaki Solucan",
        """Gece yağmur yağmıştı. Sabah okula giderken kaldırımda
onlarca solucan gördüm. Fen dersinde öğrenmiştik: Yağmur yağınca
toprak suyla dolar, solucanlar nefes almak için yüzeye çıkarmış.

Ama güneş açmıştı. Bazıları kurumaya başlamıştı bile.

Yerden geniş bir yaprak aldım. Solucanları tek tek üstüne alıp
yol kenarındaki toprağa taşıdım. Sayarak yaptım: On dört tane.

Okula on dakika geç kaldım. Öğretmenime neden geciktiğimi anlattım.
Kızacağını sandım.

"Bugün on dört canlı kurtardın," dedi. "Geç kalmana değer."

Şimdi her yağmur sonrası aynı yoldan yürüyorum.""",
        3, 4, 4,
        [
            ("bilgi", "Kaç solucan taşıdı?",
             ["On dört", "On", "Yirmi", "Beş"], 0, "On dört tane saydım"),
            ("bilgi", "Solucanları neyle taşıdı?",
             ["Bir yaprakla", "Eliyle", "Çöp kürekle", "Kağıtla"], 0, "Bir yaprak aldım"),
            ("cikarim", "Solucanlar neden tehlikedeydi?",
             ["Güneşte kuruyacakları için", "Araba geçeceği için", "Kuşlar yiyeceği için", "Soğuk olduğu için"], 0,
             "Güneş çıkmıştı, kurumaya başladılar"),
            ("cikarim", "Öğretmen neden \"geç kalmana değer\" dedi?",
             ["Yaptığı işi değerli bulduğu için", "Geç kalmayı sevdiği için", "Solucanları sevdiği için", "Şaka yaptığı için"], 0,
             "Canlı kurtarmak değerli"),
            ("kelime", "\"Kurumak\" ne demektir?",
             ["Nemini kaybetmek", "Islanmak", "Büyümek", "Soğumak"], 0,
             "Kurumak = suyunu kaybetmek"),
        ],
    ),
    (
        "sinif_kavgasi", "İki Arkadaş",
        """Kerem'le sınıfın en yakın iki arkadaşıydık. Bir gün teneffüste
oyun kuralları yüzünden tartıştık. İkimiz de haklı olduğumuzu
düşünüyorduk. Sesimizi yükselttik.

Üç gün boyunca hiç konuşmadık. Teneffüslerde bahçenin ayrı
köşelerinde oturduk. Ben oynadığım oyundan zevk almıyordum.
Sanırım o da almıyordu.

Dördüncü gün Kerem yanıma geldi. Elinde iki tane bilye vardı.
Bir süre bir şey söylemedi.

"Biri senin," dedi sonunda.

Ben de kalemliğimi açtım, onun çok sevdiği yeşil kalemi çıkardım.

O gün fark ettik ki kavganın neden çıktığını ikimiz de
hatırlamıyorduk artık.""",
        3, 4, 4,
        [
            ("bilgi", "Kaç gün konuşmadılar?",
             ["Üç", "İki", "Bir hafta", "Beş"], 0, "Üç gün konuşmadık"),
            ("bilgi", "Kerem'in elinde ne vardı?",
             ["İki bilye", "İki kalem", "Bir kitap", "Bir top"], 0, "Elinde iki bilye vardı"),
            ("cikarim", "İkisi de oyundan neden zevk almıyordu?",
             ["Birbirlerini özledikleri için", "Oyun sıkıcı olduğu için", "Yorgun oldukları için", "Hava soğuk olduğu için"], 0,
             "Küskünlük ikisini de etkiledi"),
            ("cikarim", "Son cümle ne anlatıyor?",
             ["Kavganın sebebinin önemsiz olduğunu", "Hafızalarının zayıf olduğunu", "Uzun zaman geçtiğini", "Kavganın büyük olduğunu"], 0,
             "Dostluk sebepten önemliydi"),
            ("kelime", "\"Tartışmak\" ne demektir?",
             ["Farklı görüşleri yüksek sesle savunmak", "Konuşmak", "Oynamak", "Susmak"], 0,
             "Tartışma = anlaşmazlık"),
        ],
    ),
    (
        "market_hesabi", "Marketteki Hesap",
        """Annem beni ilk kez tek başıma markete gönderdi. Ekmek, süt ve
yumurta alacaktım. Elime yirmi lira verdi ve listeyi tekrarladı.

Rafların arasında dolaşırken güzel bir çikolata gördüm.
Uzun süre baktım. Çok istedim.

Sonra aklımdan hesapladım: Ekmek, süt ve çikolatayı alırsam
yumurtaya para yetmeyecekti.

Çikolatayı yerine bıraktım ve listedeki üç şeyi aldım.

Eve geldiğimde annem para üstünü sordu. Bozuklukları verdim.
Çikolata olayını da anlattım, saklamadım.

Annem o an hiçbir şey demedi. Ama ertesi akşam alışverişten
dönerken çantasından bir çikolata çıkardı ve bana uzattı.""",
        3, 4, 4,
        [
            ("bilgi", "Anne kaç lira verdi?",
             ["Yirmi", "On", "Otuz", "Elli"], 0, "Elime yirmi lira verdi"),
            ("bilgi", "Ne alması gerekiyordu?",
             ["Ekmek, süt, yumurta", "Çikolata ve süt", "Sadece ekmek", "Meyve ve sebze"], 0,
             "Ekmek, süt ve yumurta"),
            ("cikarim", "Çocuk çikolatayı neden bıraktı?",
             ["Yumurtaya para yetmeyeceği için", "Sevmediği için", "Pahalı olduğu için", "Annesi yasakladığı için"], 0,
             "Aklından hesapladı"),
            ("cikarim", "Anne neden ertesi gün çikolata aldı?",
             ["Çocuğun sorumlu davranışını takdir ettiği için", "Kendisi canı çektiği için", "Unuttuğunu hatırladığı için", "İndirimde olduğu için"], 0,
             "Ödül değil, takdir"),
            ("kelime", "\"Para üstü\" ne demektir?",
             ["Alışverişten sonra geri kalan para", "Harçlık", "Fiyat", "Borç"], 0,
             "Verilen paradan kalan"),
        ],
    ),
]

# ==================================================== 4. SINIF (95-125 kelime)

METINLER_4_EK = [
    (
        "kutuphane_karti", "Kütüphane Kartı",
        """Mahallemizde küçük bir halk kütüphanesi var. Yıllardır önünden
geçerdim, hiç girmemiştim.

Bir cumartesi merak edip girdim. İçerisi sessizdi. Görevli teyze
gülümsedi.

"Kart çıkartmak ister misin?" diye sordu. Ücretsizmiş.

Adımı yazdı, küçük bir karton kart verdi. Üzerinde adım yazıyordu.

O gün iki kitap aldım. İki hafta sonra getirecektim.

İlk kitabı üç günde bitirdim. İkinciyi bir haftada.

Geri götürdüğümde teyze, "Beğendin mi?" diye sordu.
Uzun uzun anlattım. O da bana benzer kitaplar önerdi.

Şimdi her cumartesi oradayım. Kart hâlâ cebimde.
Kâğıt bir karton ama bana bir kapı açtı.""",
        4, 4, 4,
        [
            ("bilgi", "Kart ne kadara mal oldu?",
             ["Ücretsizdi", "On lira", "Beş lira", "Yirmi lira"], 0, "Ücretsizmiş"),
            ("bilgi", "İlk seferde kaç kitap aldı?",
             ["İki", "Bir", "Üç", "Dört"], 0, "O gün iki kitap aldım"),
            ("cikarim", "Görevli teyze neden kitap önerdi?",
             ["Çocuğun ilgisini fark ettiği için", "Zorunlu olduğu için", "Kitaplar eskidiği için", "Çocuk istediği için"], 0,
             "Uzun uzun anlatınca ilgisini gördü"),
            ("cikarim", "\"Bana bir kapı açtı\" ne anlatıyor?",
             ["Yeni bir dünyayla tanıştırdığını", "Kütüphane kapısını açtığını", "Kartın değerli olduğunu", "Ücretsiz olduğunu"], 0,
             "Mecazi anlam: yeni imkân"),
            ("kelime", "\"Önermek\" ne demektir?",
             ["Tavsiye etmek", "Satmak", "Zorlamak", "Almak"], 0,
             "Önermek = tavsiye"),
        ],
    ),
    (
        "kompost", "Mutfaktaki Deney",
        """Fen dersinde çöplerin doğaya zararını öğrendik. Öğretmenimiz
kompost diye bir şeyden bahsetti: Sebze artıkları toprağa
karıştırılınca gübreye dönüşüyormuş.

Evde denemek istedim. Annem balkona küçük bir kova koymamıza
izin verdi.

Her gün soğan kabuğu, elma çekirdeği, çay posası attık.
Ara sıra karıştırdım.

İlk iki hafta hiçbir şey değişmedi. Sabırsızlandım.

Dördüncü hafta kova içindeki artıklar koyu bir toprağa
benzemeye başladı. Kokusu bile toprak gibiydi.

O toprağı annemin çiçeğine koyduk. Çiçek üç haftada
gözle görülür şekilde büyüdü.

Çöp sandığım şey, meğer başka bir şeyin başlangıcıymış.""",
        4, 4, 5,
        [
            ("bilgi", "Kovaya neler atıldı?",
             ["Soğan kabuğu, elma çekirdeği, çay posası", "Plastik ve cam",
              "Kağıt ve karton", "Metal kutular"], 0,
             "Sebze ve meyve artıkları"),
            ("bilgi", "Kaçıncı haftada değişim başladı?",
             ["Dördüncü", "İkinci", "Altıncı", "Birinci"], 0,
             "Dördüncü hafta benzemeye başladı"),
            ("cikarim", "Çocuk ilk iki hafta neden sabırsızlandı?",
             ["Değişim görmediği için", "Kokudan rahatsız olduğu için",
              "Annesi kızdığı için", "Kova küçük olduğu için"], 0,
             "Hiçbir şey değişmedi"),
            ("cikarim", "Son cümle ne anlatıyor?",
             ["Atık sandığımız şeyin değerli olabileceğini",
              "Çöplerin kötü koktuğunu", "Deneylerin uzun sürdüğünü",
              "Çiçeklerin büyüdüğünü"], 0,
             "Çöp değil, başlangıç"),
            ("kelime", "\"Artık\" ne demektir?",
             ["Kullanıldıktan sonra geriye kalan", "Yeni malzeme",
              "Toprak", "Gübre"], 0, "Artık = geriye kalan"),
        ],
    ),
    (
        "kar_tatili", "Beklenen Kar",
        """Akşam hava durumunda ertesi gün kar yağacağı söylendi.
Bütün sınıf heyecanlandı. Gruplarda tek konu buydu:
Acaba okullar tatil olur muydu?

O gece yatağıma girdim ama uyuyamadım. Camdan defalarca baktım.
Sabaha karşı ince ince yağmaya başladı.

Sabah kalktığımda her yer bembeyazdı. Hemen telefona baktım.
Tatil ilan edilmemişti. Kar, okulların kapanmasına yetecek
kadar kalın değilmiş.

Önce büyük bir hayal kırıklığına uğradım. Kahvaltıda konuşmadım.

Ama okula giderken kar altında yürümek beklediğimden güzeldi.
Ağaçların dalları bembeyazdı. Ayak sesleri bile farklı çıkıyordu.
Kar her şeyi sessizleştirmişti.

Teneffüste bütün sınıf bahçede kartopu oynadık.
Öğretmenimiz bile katıldı, üstü başı kar oldu.

Akşam yatağımda düşündüm: Tatil olsaydı bunların hiçbiri
olmayacaktı. Evde oturuyor olacaktım.

Bazen istediğimiz şey olmayınca daha güzel bir şey oluyor.""",
        4, 4, 4,
        [
            ("bilgi", "Tatil neden ilan edilmedi?",
             ["Kar yeterince kalın olmadığı için", "Kar yağmadığı için",
              "Sınav olduğu için", "Yollar açık olduğu için"], 0,
             "Okulun kapanmasına yetecek kadar kalın değilmiş"),
            ("bilgi", "Teneffüste ne yapıldı?",
             ["Kartopu oynandı", "Ders çalışıldı", "Eve gidildi",
              "Sınıfta oturuldu"], 0, "Bahçede kartopu oynadık"),
            ("cikarim", "Çocuk gece neden defalarca camdan baktı?",
             ["Karın yağmasını beklediği için", "Uyuyamadığı için",
              "Korktuğu için", "Ödevi olduğu için"], 0,
             "Tatil umuduyla bekliyordu"),
            ("cikarim", "Çocuğun akşamki düşüncesi neyi gösteriyor?",
             ["Bakış açısının değiştiğini", "Tatili hâlâ istediğini",
              "Karı sevmediğini", "Okulu sevmediğini"], 0,
             "Hayal kırıklığı yerini başka bir güzelliğe bıraktı"),
            ("kelime", "\"Hayal kırıklığı\" ne demektir?",
             ["Umulanın gerçekleşmemesi", "Kızgınlık", "Korku", "Şaşkınlık"], 0,
             "Beklenti karşılanmayınca"),
        ],
    ),
    (
        "sunum_korkusu", "Tahtanın Önünde",
        """Sosyal Bilgiler dersi için herkesin bir sunum hazırlaması istendi.
Kura çektik, bana Türkiye'nin gölleri düştü.

Bir hafta boyunca çalıştım. Ansiklopediden bilgi topladım,
büyük kartonlar hazırladım, harita çizip resimler yapıştırdım.
Akşamları aynanın karşısında defalarca tekrar ettim.

Sunum günü geldi. Sıra bana geldiğinde tahtanın önüne çıktım.
Otuz kişi bana bakıyordu. Sınıf hiç bu kadar sessiz olmamıştı.

Sesim titredi. Ezberlediğim ilk cümleyi unuttum. Yüzümün
kızardığını hissettim. Bir an kaçmak istedim.

Öğretmenim sakin bir sesle, "Acele etme," dedi. "Kartonuna bak."

Baktım. Notlarım oradaydı, hepsi yerli yerinde. Derin bir nefes
aldım ve baştan başladım.

İlk yarım dakika çok zordu. Sonra sesim düzeldi, elim titremeyi
bıraktı. Sonunda arkadaşlarım alkışladı.

Şimdi anlıyorum: Korkunun en zor kısmı başlangıcıymış.""",
        4, 4, 5,
        [
            ("bilgi", "Sunum konusu neydi?",
             ["Türkiye'nin gölleri", "Türkiye'nin dağları",
              "Atatürk'ün hayatı", "Hayvanlar"], 0, "Türkiye'nin gölleriydi"),
            ("bilgi", "Öğretmen ne söyledi?",
             ["Acele etmemesini", "Yerine oturmasını", "Yüksek sesle konuşmasını",
              "Yarın anlatmasını"], 0, "Acele etme, kartonuna bak"),
            ("cikarim", "Çocuk neden aynada tekrar etti?",
             ["Hazırlıklı olmak istediği için", "Aynayı sevdiği için",
              "Annesi söylediği için", "Vakit geçirmek için"], 0,
             "Bir hafta çalıştı, hazırlanıyordu"),
            ("cikarim", "\"Korkunun en zor kısmı başlangıçmış\" ne anlatıyor?",
             ["Başlayınca korkunun azaldığını", "Korkunun hiç geçmediğini",
              "Sunumun kolay olduğunu", "Hazırlığın gereksiz olduğunu"], 0,
             "İlk yarım dakika zordu, sonra kolaylaştı"),
            ("kelime", "\"Sunum\" ne demektir?",
             ["Bir konuyu topluluğa anlatma", "Ödev yapma", "Sınav",
              "Not alma"], 0, "Sunum = anlatma"),
        ],
    ),
    (
        "eski_fotograf", "Sarı Fotoğraf",
        """Anneannemlerin tavan arasında karton bir kutu buldum. İçinde
onlarca eski fotoğraf vardı. Hepsi siyah beyazdı, kenarları
zamanla sararmıştı.

Bir tanesinde tanımadığım bir çocuk vardı. Kısa pantolonluydu,
ayakları çıplaktı. Elinde tahtadan yapılmış bir oyuncak araba
tutuyordu. Fotoğrafa gülümsüyordu.

Fotoğrafı anneanneme götürüp sordum. Eline aldı, gözlüğünü taktı
ve uzun uzun baktı. Bir süre hiç konuşmadı.

"Bu benim ağabeyim," dedi sonunda. "Burada yedi yaşında."

Sonra anlatmaya başladı. Bir köyde büyümüşler. O yıllarda
oyuncak diye bir şey yokmuş. Ağabeyi o arabayı bir tahta
parçasından kendi eliyle yontmuş. Tekerlekleri makara
kapağındanmış, ipini de kendi örmüş.

"Bir tane oyuncağı vardı," dedi anneannem. "Ama onu dünyadaki
herkesten çok severdi. Her akşam yastığının yanına koyardı."

Kendi odamı düşündüm. Rafta otuz kadar oyuncak var.
Hiçbirini o kadar sevdiğimi söyleyemem.

O akşam kutuyu kapatmadım. Uzun süre o fotoğrafa baktım.""",
        4, 4, 5,
        [
            ("bilgi", "Fotoğraftaki çocuk kimmiş?",
             ["Anneannenin ağabeyi", "Anneannenin babası",
              "Anlatıcının dedesi", "Bir komşu"], 0, "Bu benim ağabeyim"),
            ("bilgi", "Tahta arabanın tekerlekleri neydenmiş?",
             ["Makara kapağından", "Tahtadan", "Metalden", "Plastikten"], 0,
             "Tekerlekleri makara kapağındanmış"),
            ("cikarim", "Anneanne neden fotoğrafa uzun uzun baktı?",
             ["Anıları canlandığı için", "Göremediği için",
              "Tanımadığı için", "Fotoğraf bulanık olduğu için"], 0,
             "Geçmişini hatırladı"),
            ("cikarim", "Anlatıcı sonunda ne fark etti?",
             ["Çok şeye sahip olmanın değer vermeyi azaltabildiğini",
              "Oyuncaklarının eski olduğunu", "Fotoğrafların önemli olduğunu",
              "Köyde yaşamak istediğini"], 0,
             "Otuz oyuncak ama hiçbirini o kadar sevmiyor"),
            ("kelime", "\"Yontmak\" ne demektir?",
             ["Bir maddeyi keserek şekil vermek", "Boyamak", "Yapıştırmak",
              "Kırmak"], 0, "Yontmak = keserek biçimlendirmek"),
        ],
    ),
]
