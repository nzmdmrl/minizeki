"""
OKUMA VE ANLAMA — 1. ve 2. SINIF METINLERI

TASARIM KURALLARI:
  - Cocuk dunyasindan, duygusal bir cekirdegi olan kisa hikayeler
  - Siddet, korku, kayip yok
  - Cikarim sorusu sorulabilecek kadar derinlik olmali
    (sadece olay anlatan metin "neden" sorusuna izin vermez)
  - 1. sinif: 30-50 kelime, kisa cumleler, gunluk kelimeler
  - 2. sinif: 60-90 kelime, biraz daha uzun cumle

SORU TURLERI (her metinde 5 soru):
  bilgi   : metinde acikca yaziyor         (2 tane)
  cikarim : metinde yazmiyor, cikarilmali  (2 tane)
  kelime  : kelime dagarcigi               (1 tane)

Format:
  (id, baslik, metin, sinif_min, sinif_max, seviye, [sorular])
  soru: (tur, soru_metni, [siklar], dogru_index, aciklama)
"""

# ==================================================== 1. SINIF (30-50 kelime)

METINLER_1 = [
    (
        "kedi_minnos", "Minnoş",
        """Minnoş küçük bir kedidir. Tüyleri beyazdır.
Her sabah bahçeye çıkar. Kelebekleri kovalar.
Sonra yorulur ve ağacın altında uyur.
Akşam olunca eve döner. Süt içer.""",
        1, 2, 1,
        [
            ("bilgi", "Minnoş nerede uyur?",
             ["Ağacın altında", "Evde", "Bahçe kapısında", "Arabada"], 0,
             "Metinde: ağacın altında uyur"),
            ("bilgi", "Minnoş akşam ne içer?",
             ["Süt", "Su", "Çay", "Meyve suyu"], 0, "Süt içer"),
            ("cikarim", "Minnoş neden ağacın altında uyur?",
             ["Kelebek kovalayınca yorulduğu için", "Karnı aç olduğu için",
              "Üşüdüğü için", "Korktuğu için"], 0,
             "Önce kovalar, sonra yorulur"),
            ("cikarim", "Minnoş nasıl bir kedidir?",
             ["Hareketli ve oyuncu", "Uykucu ve tembel", "Korkak", "Yaramaz"], 0,
             "Her sabah çıkar, kelebek kovalar"),
            ("kelime", "\"Kovalamak\" ne demektir?",
             ["Peşinden koşmak", "Saklanmak", "Uyumak", "Beslemek"], 0,
             "Kovalamak = arkasından koşmak"),
        ],
    ),
    (
        "top_ali", "Ali'nin Topu",
        """Ali'nin kırmızı bir topu var.
Bugün parkta oynadı. Topu çok yükseğe attı.
Top ağaca takıldı. Ali üzüldü.
Komşusu Ahmet Amca geldi. Uzun bir dalla topu indirdi.
Ali çok sevindi.""",
        1, 2, 1,
        [
            ("bilgi", "Ali'nin topu ne renk?",
             ["Kırmızı", "Mavi", "Sarı", "Yeşil"], 0, "Kırmızı bir topu var"),
            ("bilgi", "Topu kim indirdi?",
             ["Ahmet Amca", "Ali", "Annesi", "Öğretmeni"], 0, "Komşusu Ahmet Amca"),
            ("cikarim", "Ali neden üzüldü?",
             ["Topu ağaca takıldığı için", "Parka gidemediği için",
              "Arkadaşı gelmediği için", "Topu kaybolduğu için"], 0,
             "Top ağaca takılınca üzüldü"),
            ("cikarim", "Ahmet Amca nasıl biridir?",
             ["Yardımsever", "Kızgın", "Üzgün", "Aceleci"], 0,
             "Yardım etmek için geldi"),
            ("kelime", "\"Takılmak\" ne demektir?",
             ["Bir yere sıkışıp kalmak", "Düşmek", "Zıplamak", "Koşmak"], 0,
             "Takılmak = sıkışıp kalmak"),
        ],
    ),
    (
        "cicek_zeynep", "Zeynep'in Çiçeği",
        """Zeynep bir saksıya tohum ekti.
Her gün su verdi. Güneşe koydu.
Bir hafta bekledi. Hiçbir şey olmadı.
Zeynep sabırla beklemeye devam etti.
Sonunda küçük yeşil bir yaprak çıktı.""",
        1, 2, 2,
        [
            ("bilgi", "Zeynep saksıya ne ekti?",
             ["Tohum", "Yaprak", "Çiçek", "Taş"], 0, "Tohum ekti"),
            ("bilgi", "Sonunda ne çıktı?",
             ["Yeşil bir yaprak", "Kırmızı bir çiçek", "Bir böcek", "Bir dal"], 0,
             "Küçük yeşil bir yaprak"),
            ("cikarim", "Zeynep bir hafta sonra ne hissetmiş olabilir?",
             ["Merak ve biraz sabırsızlık", "Korku", "Öfke", "Uyku"], 0,
             "Bekledi ama vazgeçmedi"),
            ("cikarim", "Bu hikâye bize ne öğretiyor?",
             ["Sabırlı olmayı", "Hızlı olmayı", "Yardım istemeyi", "Paylaşmayı"], 0,
             "Sabırla bekledi ve sonuç aldı"),
            ("kelime", "\"Sabır\" ne demektir?",
             ["Beklemeyi bilmek", "Acele etmek", "Kızmak", "Vazgeçmek"], 0,
             "Sabır = beklemeyi bilmek"),
        ],
    ),
    (
        "kus_yuvasi", "Balkondaki Yuva",
        """Ayşe balkonda bir yuva gördü.
İçinde üç küçük yumurta vardı.
Anne kuş her gün geliyordu.
Ayşe balkona çıkmadı. Kuşları korkutmak istemedi.
Bir gün yumurtalardan yavrular çıktı.""",
        1, 2, 2,
        [
            ("bilgi", "Yuvada kaç yumurta vardı?",
             ["Üç", "İki", "Dört", "Beş"], 0, "Üç küçük yumurta"),
            ("bilgi", "Ayşe balkona neden çıkmadı?",
             ["Kuşları korkutmamak için", "Hava soğuk olduğu için",
              "Yasak olduğu için", "Yorgun olduğu için"], 0,
             "Kuşları korkutmak istemedi"),
            ("cikarim", "Ayşe nasıl bir çocuktur?",
             ["Duyarlı ve düşünceli", "Korkak", "Meraksız", "Aceleci"], 0,
             "Kuşları düşünüp kendini kısıtladı"),
            ("cikarim", "Anne kuş neden her gün geliyordu?",
             ["Yumurtalarına baktığı için", "Yemek aradığı için",
              "Ayşe'yi izlediği için", "Yuva yaptığı için"], 0,
             "Yumurtalarının başında"),
            ("kelime", "\"Yuva\" ne demektir?",
             ["Kuşların yaşadığı yer", "Ağaç dalı", "Yumurta", "Bahçe"], 0,
             "Yuva = kuşların evi"),
        ],
    ),
    (
        "kar_gunu", "İlk Kar",
        """Sabah perdeyi açtım. Her yer bembeyazdı.
Kar yağmıştı! Hemen giyindim.
Bahçeye koştum. Kardan adam yaptım.
Burnuna havuç taktım. Eldivenim ıslandı ama üşümedim.""",
        1, 2, 2,
        [
            ("bilgi", "Kardan adamın burnuna ne takıldı?",
             ["Havuç", "Taş", "Dal", "Düğme"], 0, "Havuç taktım"),
            ("bilgi", "Ne ıslandı?",
             ["Eldiven", "Ayakkabı", "Şapka", "Palto"], 0, "Eldivenim ıslandı"),
            ("cikarim", "Çocuk neden üşümedi?",
             ["Oynarken hareket ettiği için", "Hava sıcak olduğu için",
              "Kalın giyindiği için", "Kısa süre kaldığı için"], 0,
             "Hareket edince ısınırız"),
            ("cikarim", "Çocuk kar yağdığını görünce ne hissetti?",
             ["Heyecan", "Korku", "Üzüntü", "Kızgınlık"], 0,
             "Hemen giyinip koştu"),
            ("kelime", "\"Bembeyaz\" ne demektir?",
             ["Çok beyaz", "Biraz beyaz", "Gri", "Parlak"], 0,
             "Bembeyaz = tamamen beyaz"),
        ],
    ),
    (
        "yeni_arkadas", "Yeni Arkadaş",
        """Sınıfımıza yeni bir öğrenci geldi.
Adı Deniz. Kimseyi tanımıyordu.
Teneffüste tek başına oturdu.
Ben yanına gittim. Elma verdim.
Sonra birlikte oyun oynadık.""",
        1, 2, 2,
        [
            ("bilgi", "Yeni öğrencinin adı ne?",
             ["Deniz", "Ali", "Ayşe", "Zeynep"], 0, "Adı Deniz"),
            ("bilgi", "Anlatan çocuk ne verdi?",
             ["Elma", "Kalem", "Kitap", "Oyuncak"], 0, "Elma verdim"),
            ("cikarim", "Deniz teneffüste neden tek başına oturdu?",
             ["Kimseyi tanımadığı için", "Yorgun olduğu için",
              "Kızgın olduğu için", "Hasta olduğu için"], 0,
             "Kimseyi tanımıyordu"),
            ("cikarim", "Deniz sonunda nasıl hissetmiş olabilir?",
             ["Mutlu", "Üzgün", "Korkmuş", "Kızgın"], 0,
             "Birlikte oyun oynadılar"),
            ("kelime", "\"Teneffüs\" ne demektir?",
             ["Ders arası", "Ders saati", "Öğle yemeği", "Okul çıkışı"], 0,
             "Teneffüs = ders arası"),
        ],
    ),
]

# ==================================================== 2. SINIF (60-90 kelime)

METINLER_2 = [
    (
        "yagmurlu_gun", "Yağmurlu Gün",
        """Ali sabah uyandığında pencereye koştu. Dışarısı çok karanlıktı
ve yağmur camlara vuruyordu. Bugün parka gidecekti, top oynayacaktı.

Babası odaya girdi. Ali'nin yüzüne baktı ve gülümsedi.

"Bugün dışarı çıkamayız oğlum, hava çok soğuk ve yağmurlu," dedi.

Ali'nin gözleri doldu. Babası onun yanına oturdu.

"Ama seninle kule yapabiliriz. Hem de kocaman bir kule!"

Ali hemen kutuyu getirdi. O gün öğlene kadar oynadılar.""",
        2, 3, 2,
        [
            ("bilgi", "Ali sabah uyanınca nereye koştu?",
             ["Pencereye", "Mutfağa", "Bahçeye", "Kapıya"], 0, "Pencereye koştu"),
            ("bilgi", "Baba neden dışarı çıkamayacaklarını söyledi?",
             ["Hava soğuk ve yağmurlu olduğu için", "Ali hasta olduğu için",
              "Park kapalı olduğu için", "İşi olduğu için"], 0,
             "Hava çok soğuk ve yağmurlu"),
            ("cikarim", "Ali'nin gözleri neden doldu?",
             ["Planı bozulduğu için", "Babasına kızdığı için",
              "Yağmurdan korktuğu için", "Uykusu geldiği için"], 0,
             "Parka gitmeyi planlıyordu"),
            ("cikarim", "Baba Ali'yi nasıl neşelendirdi?",
             ["Birlikte oynamayı önererek", "Hediye alarak",
              "Parka götürerek", "Televizyon açarak"], 0,
             "Kule yapmayı önerdi"),
            ("kelime", "\"Kocaman\" ne demektir?",
             ["Çok büyük", "Küçük", "Renkli", "Ağır"], 0, "Kocaman = çok büyük"),
        ],
    ),
    (
        "kayip_silgi", "Kaybolan Silgi",
        """Elif'in çok sevdiği bir silgisi vardı. Üzerinde küçük bir
papatya resmi vardı. Bir gün silgisini bulamadı. Çantasına baktı,
sırasına baktı, hiçbir yerde yoktu.

Yan sırada oturan Mert'in elinde aynı silgiden gördü. Elif çok kızdı
ama bir şey söylemedi.

Eve gelince çantasının küçük cebini açtı. Silgisi oradaydı.

Ertesi gün Mert'e gitti. "Dün sana yanlış düşündüm, özür dilerim," dedi.""",
        2, 3, 3,
        [
            ("bilgi", "Silginin üzerinde ne resmi vardı?",
             ["Papatya", "Kelebek", "Kalp", "Yıldız"], 0, "Küçük bir papatya resmi"),
            ("bilgi", "Elif silgisini nerede buldu?",
             ["Çantasının küçük cebinde", "Sırasında", "Mert'te", "Yerde"], 0,
             "Çantasının küçük cebi"),
            ("cikarim", "Elif Mert'e neden kızdı?",
             ["Silgisini aldığını düşündüğü için", "Mert ona vurduğu için",
              "Mert konuşmadığı için", "Mert güldüğü için"], 0,
             "Aynı silgiyi Mert'te görünce"),
            ("cikarim", "Elif ertesi gün özür dileyerek ne yapmış oldu?",
             ["Hatasını kabul etti", "Mert'i suçladı",
              "Silgiyi geri istedi", "Öğretmene şikâyet etti"], 0,
             "Yanlış düşündüğünü kabul etti"),
            ("kelime", "\"Özür dilemek\" ne demektir?",
             ["Hatayı kabul edip affetmesini istemek", "Kızmak",
              "Teşekkür etmek", "Sormak"], 0, "Hatayı kabul etmek"),
        ],
    ),
    (
        "dede_bahce", "Dedemin Bahçesi",
        """Yaz tatilinde dedemin evine gittim. Dedemin arka tarafında
küçük bir bahçesi var. Domates, biber ve salatalık yetiştiriyor.

Her sabah erkenden kalkıyor. Bitkileri suluyor, yabani otları
temizliyor. Bana da bir kova verdi.

"Bitkiler de bizim gibi," dedi. "Su ister, güneş ister, ilgi ister."

O yaz ilk domatesimi ben kopardım. Hiçbir domates o kadar lezzetli
olmamıştı.""",
        2, 3, 3,
        [
            ("bilgi", "Dede bahçede neler yetiştiriyor?",
             ["Domates, biber, salatalık", "Elma, armut, kiraz",
              "Gül, papatya, lale", "Buğday ve arpa"], 0,
             "Domates, biber ve salatalık"),
            ("bilgi", "Dede sabahları ne yapıyor?",
             ["Bitkileri suluyor ve otları temizliyor", "Uyuyor",
              "Markete gidiyor", "Gazete okuyor"], 0, "Suluyor, temizliyor"),
            ("cikarim", "Dede \"Bitkiler de bizim gibi\" derken ne anlatmak istedi?",
             ["Onların da bakıma ihtiyacı olduğunu", "Bitkilerin konuştuğunu",
              "Bitkilerin yürüdüğünü", "Bitkilerin uyuduğunu"], 0,
             "Su, güneş, ilgi ister"),
            ("cikarim", "İlk domates neden bu kadar lezzetli geldi?",
             ["Kendi emeğiyle yetiştiği için", "Çok büyük olduğu için",
              "Şekerli olduğu için", "Aç olduğu için"], 0,
             "Emek verdiği için değerli"),
            ("kelime", "\"Yabani ot\" ne demektir?",
             ["Kendiliğinden çıkan istenmeyen bitki", "Meyve ağacı",
              "Sebze", "Çiçek"], 0, "Ekilmeden çıkan zararlı ot"),
        ],
    ),
    (
        "okul_yolu", "Okul Yolunda",
        """Her sabah okula yürüyerek giderim. Yolda bir simitçi amca var.
Beni görünce her zaman el sallar.

Bir gün çok geç kalmıştım. Koşarak geçiyordum. Simitçi amca beni
durdurdu.

"Yavaş koş," dedi. "Yol kaygan, dün yağmur yağdı."

Ben yine de koştum. Köşeyi dönerken ayağım kaydı ve düştüm.
Dizim biraz acıdı.

O günden sonra büyüklerin sözünü daha dikkatli dinliyorum.""",
        2, 3, 3,
        [
            ("bilgi", "Simitçi amca ne söyledi?",
             ["Yavaş koşmasını", "Hızlı koşmasını", "Durmasını", "Geri dönmesini"],
             0, "Yavaş koş, yol kaygan"),
            ("bilgi", "Yol neden kaygandı?",
             ["Dün yağmur yağdığı için", "Kar yağdığı için",
              "Yeni yıkandığı için", "Buz tuttuğu için"], 0, "Dün yağmur yağdı"),
            ("cikarim", "Çocuk neden düştü?",
             ["Uyarıyı dinlemediği için", "Ayakkabısı eski olduğu için",
              "Biri ittiği için", "Çantası ağır olduğu için"], 0,
             "Uyarıya rağmen koştu"),
            ("cikarim", "Çocuk bu olaydan ne öğrendi?",
             ["Büyüklerin uyarısını dinlemeyi", "Koşmayı",
              "Erken kalkmayı", "Simit almayı"], 0,
             "Son cümlede söylüyor"),
            ("kelime", "\"Kaygan\" ne demektir?",
             ["Ayağın kayabileceği", "Sert", "Sıcak", "Dar"], 0,
             "Kaygan = kayma tehlikesi olan"),
        ],
    ),
    (
        "kumbara", "Kumbaram",
        """Doğum günümde teyzem bana bir kumbara hediye etti.
Kırmızı bir domuzcuk şeklindeydi.

Her hafta harçlığımın bir kısmını içine attım. Bazen çok zor oldu.
Arkadaşlarım şeker alırken ben almadım.

Üç ay sonra kumbarayı açtım. İçinden epeyce para çıktı.
O parayla hep istediğim boya kalemlerini aldım.

Kendi biriktirdiğim parayla almak çok güzel bir duyguydu.""",
        2, 3, 4,
        [
            ("bilgi", "Kumbarayı kim hediye etti?",
             ["Teyzesi", "Annesi", "Dedesi", "Arkadaşı"], 0, "Teyzem hediye etti"),
            ("bilgi", "Biriken parayla ne aldı?",
             ["Boya kalemleri", "Oyuncak", "Kitap", "Şeker"], 0,
             "Hep istediği boya kalemleri"),
            ("cikarim", "Biriktirmek neden bazen zor oldu?",
             ["Arkadaşları harcarken kendini tutması gerektiği için",
              "Kumbara ağır olduğu için", "Para bulamadığı için",
              "Unuttuğu için"], 0, "Şeker almadı"),
            ("cikarim", "Çocuk sonunda neden mutlu oldu?",
             ["Kendi emeğiyle aldığı için", "Ucuza aldığı için",
              "Hediye geldiği için", "Çok para biriktiği için"], 0,
             "Kendi biriktirdiği parayla"),
            ("kelime", "\"Epeyce\" ne demektir?",
             ["Oldukça çok", "Çok az", "Hiç", "Biraz"], 0, "Epeyce = hayli, oldukça"),
        ],
    ),
    (
        "kutuphane", "Kütüphanedeki Sessizlik",
        """Sınıfça okul kütüphanesine gittik. Öğretmenimiz kapıda durdu.

"İçeride sessiz olacağız," dedi. "Çünkü herkes okumaya
odaklanmak ister."

İçeri girdik. Gerçekten çok sessizdi. Sadece sayfa çevirme
sesleri duyuluyordu.

Ben hayvanlarla ilgili bir kitap seçtim. O kadar dalmışım ki
zil çaldığında irkildim.

Meğer sessizlik, insanın kitaba dalmasını kolaylaştırıyormuş.""",
        2, 3, 4,
        [
            ("bilgi", "Öğretmen kapıda ne söyledi?",
             ["Sessiz olmaları gerektiğini", "Kitap almamalarını",
              "Hızlı olmalarını", "Oturmalarını"], 0, "İçeride sessiz olacağız"),
            ("bilgi", "Çocuk ne hakkında kitap seçti?",
             ["Hayvanlar", "Uzay", "Tarih", "Spor"], 0, "Hayvanlarla ilgili"),
            ("cikarim", "Çocuk zil çalınca neden irkildi?",
             ["Kitaba çok dalmış olduğu için", "Korktuğu için",
              "Uyuduğu için", "Zil çok yüksek olduğu için"], 0,
             "O kadar dalmıştı ki"),
            ("cikarim", "Bu hikâyenin ana fikri nedir?",
             ["Sessizlik odaklanmayı kolaylaştırır", "Kütüphaneler büyüktür",
              "Kitaplar pahalıdır", "Zil sesi rahatsız eder"], 0,
             "Son cümlede söylüyor"),
            ("kelime", "\"İrkilmek\" ne demektir?",
             ["Ani sesle ürkmek", "Sevinmek", "Uyumak", "Gülmek"], 0,
             "İrkilmek = ani şaşırıp ürkmek"),
        ],
    ),
]
