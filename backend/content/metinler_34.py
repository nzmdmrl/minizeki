"""
OKUMA VE ANLAMA — 3. ve 4. SINIF METINLERI

3. sinif: 100-150 kelime
4. sinif: 150-220 kelime

Bu seviyede metinler sadece olay anlatmaz; bir fikir, bir degisim
ya da bir ic catisma tasir. Cikarim sorulari ancak boyle anlamli olur.

Format:
  (id, baslik, metin, sinif_min, sinif_max, seviye, [sorular])
  soru: (tur, soru_metni, [siklar], dogru_index, aciklama)
"""

# ==================================================== 3. SINIF (100-150 kelime)

METINLER_3 = [
    (
        "bisiklet_dersi", "Bisiklet Dersi",
        """Babam bana bisiklet sürmeyi öğretiyordu. İlk gün arkadan tutuyordu.
İkinci gün de tuttu. Üçüncü gün ben pedal çevirirken arkama baktım.

Babam çok gerideydi. Meğer uzun süredir tek başıma sürüyormuşum.

Korktum ve dengemi kaybettim. Yere düştüm. Dizim kanadı.

Babam koşarak geldi. Yaramı temizledi.

"Aslında sen zaten sürüyordun," dedi. "Sadece bunu bilmiyordun.
Bilince korktun."

Ertesi gün tekrar bindim. Bu sefer arkama bakmadım.
Sokağın sonuna kadar gittim ve düşmedim.

O gün öğrendim ki bazen en büyük engel, kendi korkumuz oluyor.""",
        3, 4, 3,
        [
            ("bilgi", "Çocuk üçüncü gün ne yaptı?",
             ["Arkasına baktı", "Düşmemek için yavaşladı",
              "Babasını çağırdı", "Bisikletten indi"], 0,
             "Pedal çevirirken arkama baktım"),
            ("bilgi", "Baba yara için ne yaptı?",
             ["Temizledi", "Görmezden geldi", "Eve götürdü", "Doktora gitti"], 0,
             "Yaramı temizledi"),
            ("cikarim", "Çocuk neden düştü?",
             ["Tek başına olduğunu görüp korktuğu için",
              "Hızlı gittiği için", "Yol bozuk olduğu için",
              "Babası bıraktığı için"], 0,
             "Korktum ve dengemi kaybettim"),
            ("cikarim", "Baba \"Sadece bunu bilmiyordun\" derken ne demek istedi?",
             ["Çocuğun becerisi vardı ama farkında değildi",
              "Çocuk yalan söylüyordu", "Bisiklet bozuktu",
              "Baba yardım etmemişti"], 0,
             "Zaten sürüyordu, bilmiyordu"),
            ("kelime", "\"Denge\" ne demektir?",
             ["Düşmeden durabilme hâli", "Hız", "Güç", "Yön"], 0,
             "Denge = dengede kalma"),
        ],
    ),
    (
        "sinif_kutuphanesi", "Sınıf Kütüphanesi",
        """Sınıfımızda küçük bir kitaplık vardı ama içinde sadece
beş kitap bulunuyordu.

Öğretmenimiz bir fikir attı ortaya: "Herkes evden okuduğu bir
kitabı getirsin. Yıl sonunda geri alır."

İlk hafta sadece üç kişi kitap getirdi. İkinci hafta yedi kişi.
Üçüncü hafta neredeyse herkes getirmişti.

Kitaplık doldu taştı. Artık teneffüslerde kitap almak için
sıraya giriyorduk.

En güzeli şuydu: Ahmet'in getirdiği kitabı ben okudum,
benim getirdiğimi Elif okudu. Sonra o kitaplar hakkında
konuşmaya başladık.

Bir kitap, iki kişiye ait olunca daha çok değer kazanıyormuş.""",
        3, 4, 3,
        [
            ("bilgi", "Başlangıçta kitaplıkta kaç kitap vardı?",
             ["Beş", "Üç", "Yedi", "On"], 0, "Sadece beş kitap"),
            ("bilgi", "Öğretmenin fikri neydi?",
             ["Herkesin evden kitap getirmesi", "Kitap satın alınması",
              "Kütüphaneye gidilmesi", "Kitap yazılması"], 0,
             "Herkes evden bir kitap getirsin"),
            ("cikarim", "Neden ilk hafta az, sonraki haftalarda çok kişi getirdi?",
             ["Diğerlerini görünce onlar da istedi", "Öğretmen zorladı",
              "Ödül verildi", "Kitaplar bitmişti"], 0,
             "Örnek olma etkisi"),
            ("cikarim", "\"Bir kitap iki kişiye ait olunca değer kazanır\" ne anlatıyor?",
             ["Paylaşınca üzerine konuşulup zenginleştiğini",
              "Kitapların pahalı olduğunu", "İki kitap gerektiğini",
              "Kitapların eskidiğini"], 0,
             "Kitap hakkında konuşmaya başladılar"),
            ("kelime", "\"Fikir atmak\" ne demektir?",
             ["Bir öneri sunmak", "Bir şey fırlatmak",
              "Vazgeçmek", "Soru sormak"], 0, "Öneri getirmek"),
        ],
    ),
    (
        "kirlangic", "Kırlangıçlar",
        """Her ilkbahar, evimizin saçağına kırlangıçlar gelir.
Aynı çift, aynı yuvaya döner. Nereden biliyorlar, hiç anlamam.

Bu yıl yuva rüzgârdan zarar görmüştü. Kırlangıçlar geldiklerinde
biraz şaşkın göründüler.

Sonra çamur ve saman taşımaya başladılar. Üç gün boyunca
sabahtan akşama kadar çalıştılar. Yuvayı yeniden ördüler.

Babam, "Görüyor musun," dedi. "Yıkılan bir şeyi onarmak,
yenisini yapmaktan daha çok emek ister. Ama onlar vazgeçmedi."

Şimdi yuvada dört yavru var. Sabahları cıvıltılarıyla uyanıyorum.""",
        3, 4, 4,
        [
            ("bilgi", "Kırlangıçlar yuvayı neyle ördü?",
             ["Çamur ve saman", "Dal ve yaprak", "Tüy ve ot", "Taş ve toprak"], 0,
             "Çamur ve saman taşıdılar"),
            ("bilgi", "Yuvaya ne olmuştu?",
             ["Rüzgârdan zarar görmüştü", "Yağmurdan ıslanmıştı",
              "Biri almıştı", "Kediler bozmuştu"], 0, "Rüzgârdan zarar görmüştü"),
            ("cikarim", "Kırlangıçlar geldiklerinde neden şaşkın göründü?",
             ["Yuvalarını bozulmuş buldukları için",
              "Yolu unuttukları için", "Aç oldukları için",
              "Hava soğuk olduğu için"], 0, "Yuva zarar görmüştü"),
            ("cikarim", "Babanın sözü aslında neyi anlatıyor?",
             ["Onarmanın da bir değer olduğunu", "Kuşların akıllı olduğunu",
              "Yuvaların dayanıksız olduğunu", "Rüzgârın zararlı olduğunu"], 0,
             "Vazgeçmeden onarmak"),
            ("kelime", "\"Saçak\" ne demektir?",
             ["Çatının duvardan taşan kenarı", "Bahçe duvarı",
              "Pencere", "Kapı eşiği"], 0, "Çatının taşan kısmı"),
        ],
    ),
    (
        "matematik_notu", "Matematik Notum",
        """Matematik sınavından 55 aldım. Sınıfın en düşük notlarından biriydi.

Eve giderken karnem çantamda ağırlık yapıyordu. Annem sorunca
söylemek istemedim ama söyledim.

Kızacağını sandım. Kızmadı.

"Hangi soruları yapamadın?" diye sordu. Beraber baktık.
Çarpma işlemlerinde hata yapmışım. Aslında konuyu biliyordum,
dikkatsizce hesaplamıştım.

O akşamdan sonra her gün on dakika çarpma çalıştım.
Sıkıcıydı ama kısa sürüyordu.

Bir sonraki sınavdan 80 aldım. Annem yine kızmadı,
ama bu sefer sarıldı.""",
        3, 4, 4,
        [
            ("bilgi", "Çocuk ilk sınavdan kaç aldı?",
             ["55", "80", "45", "65"], 0, "55 aldım"),
            ("bilgi", "Hatası neredeydi?",
             ["Çarpma işlemlerinde", "Toplama işlemlerinde",
              "Problem sorularında", "Geometri sorularında"], 0,
             "Çarpma işlemlerinde hata"),
            ("cikarim", "Anne neden \"Hangi soruları yapamadın?\" diye sordu?",
             ["Sorunun kaynağını bulmak için", "Cezalandırmak için",
              "Öğretmene şikâyet etmek için", "Merak ettiği için"], 0,
             "Çözüm odaklı yaklaşım"),
            ("cikarim", "Çocuğun notu neden yükseldi?",
             ["Eksiğini bilip düzenli çalıştığı için",
              "Sınav kolay olduğu için", "Şanslı olduğu için",
              "Kopya çektiği için"], 0, "Her gün on dakika çalıştı"),
            ("kelime", "\"Dikkatsizce\" ne demektir?",
             ["Özen göstermeden", "Yavaşça", "Bilerek", "Dikkatle"], 0,
             "Dikkat etmeden"),
        ],
    ),
    (
        "sokak_kedisi", "Sokağın Kedisi",
        """Apartmanımızın önünde turuncu bir kedi yaşıyor.
Kimsenin kedisi değil ama herkesin kedisi.

Üçüncü kattaki teyze her sabah mama koyuyor. Bakkal amca
kış gelince kapısının önüne bir karton kutu bıraktı.
Ben de su kabını dolduruyorum.

Geçen hafta kedi ortadan kayboldu. Herkes endişelendi.
Apartmanda konuşulan tek konu oydu.

Dört gün sonra döndü. Yanında üç küçük yavru vardı.

Şimdi hepimiz mama, kutu ve su taşıyoruz.
Kimse kimseye "sen şunu yap" demedi. Kendiliğinden oldu.""",
        3, 4, 4,
        [
            ("bilgi", "Bakkal amca ne yaptı?",
             ["Karton kutu bıraktı", "Mama verdi", "Su koydu",
              "Kediyi eve aldı"], 0, "Kapısının önüne karton kutu"),
            ("bilgi", "Kedi kaç gün sonra döndü?",
             ["Dört", "İki", "Üç", "Beş"], 0, "Dört gün sonra döndü"),
            ("cikarim", "Kedi neden kaybolmuştu?",
             ["Yavrularını doğurmaya gittiği için", "Kaçtığı için",
              "Hasta olduğu için", "Yiyecek aradığı için"], 0,
             "Yanında üç yavruyla döndü"),
            ("cikarim", "\"Kimse kimseye sen şunu yap demedi\" cümlesi neyi anlatıyor?",
             ["Yardımın gönüllü olduğunu", "Kimsenin ilgilenmediğini",
              "Kavga çıktığını", "Görev dağıtıldığını"], 0,
             "Kendiliğinden oldu"),
            ("kelime", "\"Endişelenmek\" ne demektir?",
             ["Kaygılanmak", "Sevinmek", "Kızmak", "Şaşırmak"], 0,
             "Endişe = kaygı"),
        ],
    ),
]

# ==================================================== 4. SINIF (150-220 kelime)

METINLER_4 = [
    (
        "bilim_fuari", "Bilim Fuarı",
        """Okulumuzda bilim fuarı düzenleniyordu. Ben ve Kerem birlikte
proje yapmaya karar verdik. Fikrimiz basitti: Bitkiler müzikten
etkilenir mi?

İki saksıya aynı tohumdan ektik. Birinin yanına her gün yarım saat
müzik açtık, diğerine hiçbir şey yapmadık. Su ve ışık ikisinde de
aynıydı.

Üç hafta boyunca her gün boy ölçtük, defterimize yazdık.

Sonuçta iki bitki de neredeyse aynı boydaydı. Aradaki fark
yarım santimetreydi.

Kerem üzüldü. "Hiçbir şey bulamadık," dedi.

Öğretmenimiz sunumumuzu dinledikten sonra şöyle dedi:

"Bir deneyin sonucu 'fark yok' çıkması da bir sonuçtur.
Siz düzenli ölçüm yaptınız, kayıt tuttunuz, dürüst davrandınız.
Bilim böyle yapılır. Beklediğiniz sonucu bulamamak
başarısızlık değildir."

Fuarda birinci olmadık. Ama o günden sonra bir şeyi merak
ettiğimde önce ölçmeye başladım.""",
        4, 4, 4,
        [
            ("bilgi", "Projenin sorusu neydi?",
             ["Bitkiler müzikten etkilenir mi", "Bitkiler ne kadar su ister",
              "Işık bitkiyi büyütür mü", "Toprak çeşidi önemli mi"], 0,
             "Bitkiler müzikten etkilenir mi"),
            ("bilgi", "İki bitki arasındaki fark ne kadardı?",
             ["Yarım santimetre", "Beş santimetre", "İki santimetre",
              "Hiç fark yoktu"], 0, "Aradaki fark yarım santimetre"),
            ("cikarim", "Su ve ışığı neden ikisinde de aynı tuttular?",
             ["Sadece müziğin etkisini ölçebilmek için",
              "Kolay olduğu için", "Öğretmen söylediği için",
              "Zamandan kazanmak için"], 0,
             "Tek değişken müzik olmalı"),
            ("cikarim", "Öğretmen neden 'fark yok' sonucunu değerli buldu?",
             ["Düzgün ve dürüst yöntemle elde edildiği için",
              "Kolay olduğu için", "Beklenen sonuç olduğu için",
              "Birinci geldikleri için"], 0,
             "Yöntem doğruysa sonuç değerlidir"),
            ("kelime", "\"Sunum\" ne demektir?",
             ["Bir çalışmayı başkalarına anlatma", "Yazılı sınav",
              "Deney malzemesi", "Ölçüm aleti"], 0, "Anlatma, sergileme"),
        ],
    ),
    (
        "dedemin_saati", "Dedemin Saati",
        """Dedemin eski bir kol saati vardı. Kordonu yıpranmış, camı
çizilmişti. Kaç kez yeni saat aldık, hiçbirini takmadı.

Bir gün sordum: "Dede, neden bu eski saati takıyorsun?"

Saati çıkardı, avucuna koydu.

"Bu saati bana babam verdi," dedi. "Ben on dört yaşındayken.
İlk işime başladığım gün. 'Zamanın kıymetini bil' demişti."

Sonra biraz durdu.

"Yeni saatler daha doğru gösteriyor olabilir. Ama bu saat bana
sadece saati göstermiyor. Bir günü gösteriyor."

O gün anladım ki bazı eşyalar taşıdıkları anılar yüzünden
değerlidir. Fiyatı ne olursa olsun.

Geçen ay dedem hastanedeyken saatini bana emanet etti.
Şimdi kolumda. Biraz büyük geliyor ama her baktığımda
dedemi hatırlıyorum.

Belki bir gün ben de birine veririm.""",
        4, 4, 5,
        [
            ("bilgi", "Dede saati kaç yaşındayken almış?",
             ["On dört", "On", "On sekiz", "Yirmi"], 0, "On dört yaşındayken"),
            ("bilgi", "Saati dedeye kim vermiş?",
             ["Babası", "Annesi", "Dedesi", "Arkadaşı"], 0, "Bu saati bana babam verdi"),
            ("cikarim", "\"Bir günü gösteriyor\" sözüyle dede ne demek istedi?",
             ["Saatin özel bir anıyı hatırlattığını",
              "Saatin bozuk olduğunu", "Saatin sadece gündüz çalıştığını",
              "Saatin eski olduğunu"], 0, "İşe başladığı günü hatırlatıyor"),
            ("cikarim", "Torun saati takarken ne hissediyor?",
             ["Dedesine bağlılık ve özlem", "Rahatsızlık",
              "Gurur ve üstünlük", "Merak"], 0,
             "Her baktığında dedeyi hatırlıyor"),
            ("kelime", "\"Emanet etmek\" ne demektir?",
             ["Korunması için birine bırakmak", "Hediye etmek",
              "Satmak", "Kaybetmek"], 0, "Güvenerek bırakmak"),
        ],
    ),
    (
        "takim_oyunu", "Takım Oyunu",
        """Sınıflar arası voleybol turnuvasında finale kalmıştık.
Takımın en iyi oyuncusu bendim. En azından ben öyle sanıyordum.

Maçta her topu ben almaya çalıştım. Arkadaşlarıma pas vermedim.
Birkaç sayı attım ama çok da hata yaptım.

İlk seti kaybettik.

Molada kaptanımız Elif konuştu: "Sen iyi oynuyorsun ama tek
başına oynuyorsun. Altı kişiyiz."

Kızdım önce. Sonra düşündüm.

İkinci sette pas vermeye başladım. Mert'e attığım top sayı oldu.
Ayşe'nin bloğu sayı oldu. Ben daha az sayı attım ama takım
daha çok sayı yaptı.

Seti kazandık. Üçüncü seti de kazandık.

Kupayı alırken Elif bana baktı ve gülümsedi. Hiçbir şey demedi.
Zaten söylemesine gerek yoktu.""",
        4, 4, 4,
        [
            ("bilgi", "Kaptanın adı neydi?",
             ["Elif", "Ayşe", "Mert", "Deniz"], 0, "Kaptanımız Elif"),
            ("bilgi", "İlk sette ne oldu?",
             ["Kaybettiler", "Kazandılar", "Berabere kaldılar",
              "Maç iptal oldu"], 0, "İlk seti kaybettik"),
            ("cikarim", "Anlatıcı ilk sette neden başarısız oldu?",
             ["Takım arkadaşlarını kullanmadığı için",
              "Yorgun olduğu için", "Rakip iyi olduğu için",
              "Sakatlandığı için"], 0, "Tek başına oynadı"),
            ("cikarim", "Elif maç sonunda neden hiçbir şey söylemedi?",
             ["Anlatıcının kendisi anlamıştı", "Kızgın olduğu için",
              "Yorgun olduğu için", "Konuşmayı sevmediği için"], 0,
             "Söylemesine gerek yoktu"),
            ("kelime", "\"Blok\" voleybolda ne demektir?",
             ["Rakibin topunu filede engelleme", "Sayı atma",
              "Servis atma", "Oyuncu değişikliği"], 0,
             "Filede topu engelleme"),
        ],
    ),
    (
        "su_damlasi", "Bir Damla Su",
        """Fen dersinde öğretmenimiz bir soru sordu:
"Musluğu kapatmadığınızda ne kadar su boşa gider?"

Kimse bilmiyordu. Öğretmenimiz bir deney önerdi.

Sınıfça bir musluğu saniyede bir damla akacak şekilde
ayarladık. Altına ölçekli bir kap koyduk. Ertesi gün geldiğimizde
kapta yaklaşık on beş litre su vardı.

On beş litre. Sadece bir musluktan. Sadece bir günde.

Öğretmenimiz tahtaya yazdı: Okulumuzda 40 musluk var.

Sonra hesapladık. Eğer hepsi damlasa günde 600 litre eder.
Bir ayda 18.000 litre.

O günden sonra sınıfça bir karar aldık. Her teneffüs sonunda
bir arkadaşımız lavaboları kontrol ediyor.

Küçük bir damla, çarpınca büyük oluyormuş.""",
        4, 4, 5,
        [
            ("bilgi", "Bir günde kapta ne kadar su birikti?",
             ["Yaklaşık on beş litre", "Bir litre", "Yüz litre", "Beş litre"], 0,
             "Yaklaşık on beş litre"),
            ("bilgi", "Okulda kaç musluk var?",
             ["40", "15", "60", "100"], 0, "Okulumuzda 40 musluk var"),
            ("cikarim", "Öğretmen neden anlatmak yerine deney yaptırdı?",
             ["Öğrenciler kendi görüp inansın diye",
              "Ders boş geçsin diye", "Kolay olduğu için",
              "Müfredatta olduğu için"], 0,
             "Görerek öğrenme daha etkili"),
            ("cikarim", "\"Küçük bir damla, çarpınca büyük oluyormuş\" ne anlatıyor?",
             ["Küçük israfların toplanınca büyüdüğünü",
              "Damlaların ağır olduğunu", "Matematiğin zor olduğunu",
              "Musluğun bozuk olduğunu"], 0,
             "40 musluk × her gün = büyük kayıp"),
            ("kelime", "\"Ölçekli kap\" ne demektir?",
             ["Miktarı gösteren çizgileri olan kap", "Büyük kova",
              "Cam bardak", "Kapaklı kutu"], 0, "Üzerinde ölçü çizgileri olan"),
        ],
    ),
    (
        "harita_dedesi", "Haritadaki Yer",
        """Coğrafya dersinde Türkiye haritasına bakıyorduk.
Öğretmenimiz herkesten ailesinin geldiği yeri bulmasını istedi.

Ben babaannemi aradım telefonla.

"Sivas'ın bir köyü," dedi. "Adı Yıldızeli. Ben on yaşındayken
İstanbul'a geldik."

Haritada Yıldızeli'ni buldum. Küçücük bir noktaydı.

"Nasıl bir yerdi babaanne?" diye sordum.

Uzun uzun anlattı. Kışın yolların kapandığını, yaz akşamları
damda uyuduklarını, bahçedeki dut ağacını.

Ertesi gün sınıfta anlattım. Sonra fark ettim ki herkesin
bir hikâyesi vardı. Kayseri, Trabzon, Muğla, Kars...

Öğretmenimiz haritaya iğneler koydu. Otuz iğne, otuz farklı yer.

"Bu sınıf," dedi, "Türkiye'nin küçük bir haritası."

O gün haritaya bakışım değişti. Artık her nokta bir yer değil,
birinin hikâyesi.""",
        4, 4, 5,
        [
            ("bilgi", "Babaanne nereden geliyor?",
             ["Sivas Yıldızeli", "Kayseri", "Trabzon", "Kars"], 0,
             "Sivas'ın bir köyü, Yıldızeli"),
            ("bilgi", "Öğretmen haritaya kaç iğne koydu?",
             ["Otuz", "Yirmi", "Kırk", "On"], 0, "Otuz iğne, otuz farklı yer"),
            ("cikarim", "Anlatıcının haritaya bakışı neden değişti?",
             ["Noktaların insan hikâyeleri taşıdığını anladığı için",
              "Haritayı ezberlediği için", "Coğrafyayı sevdiği için",
              "Yeni harita aldıkları için"], 0,
             "Her nokta birinin hikâyesi"),
            ("cikarim", "Öğretmen \"Bu sınıf Türkiye'nin küçük bir haritası\" derken ne demek istedi?",
             ["Sınıfta ülkenin her yerinden insan olduğunu",
              "Sınıfın küçük olduğunu", "Haritanın büyük olduğunu",
              "Coğrafya dersinin önemli olduğunu"], 0,
             "Otuz farklı yerden geliyorlar"),
            ("kelime", "\"Dam\" ne demektir?",
             ["Evin düz çatısı", "Bahçe duvarı", "Ahır", "Kuyu"], 0,
             "Damda uyumak = düz çatıda"),
        ],
    ),
]
