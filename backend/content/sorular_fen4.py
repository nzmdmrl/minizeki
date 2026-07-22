"""
FEN BILIMLERI — 4. SINIF EK UNITELERI.
Isik ve Ses, Elektrik, Beslenme ve Sindirim.

Band hedef dogruluk: 1=%90  2=%75  3=%60  4=%40  5=%20
Format: (band, sinif_min, sinif_max, soru, [siklar], dogru_index, aciklama)
"""

# ==================================================== ISIK VE SES

ISIK_SES = [
    # Band 1
    (1, 4, 4, "Hangisi doğal ışık kaynağıdır?", ["Güneş", "Ampul", "Fener", "Mum"], 0, "Güneş doğal ışık kaynağıdır"),
    (1, 4, 4, "Hangisi yapay ışık kaynağıdır?", ["Ampul", "Güneş", "Yıldız", "Şimşek"], 0, "Ampul insan yapımıdır"),
    (1, 4, 4, "Işık olmadan ne olur?", ["Göremeyiz", "Duyamayız", "Koklayamayız", "Tat alamayız"], 0, "Görme ışık gerektirir"),
    (1, 4, 4, "Ses neyle duyulur?", ["Kulak", "Göz", "Burun", "Dil"], 0, "Kulak"),
    (1, 4, 4, "Hangisi ses çıkarır?", ["Zil", "Taş", "Kağıt", "Kalem"], 0, "Zil titreşerek ses üretir"),
    (1, 4, 4, "Gölge nasıl oluşur?", ["Işık engellenince", "Karanlıkta", "Sesle", "Isıyla"], 0, "Işığın engellenmesi"),
    # Band 2
    (2, 4, 4, "Işık nasıl yayılır?", ["Doğrusal (düz)", "Eğri", "Dairesel", "Zikzak"], 0, "Işık düz yol izler"),
    (2, 4, 4, "Ses nasıl oluşur?", ["Titreşimle", "Işıkla", "Isıyla", "Renkle"], 0, "Titreşim ses üretir"),
    (2, 4, 4, "Hangi maddeden ışık geçer?", ["Cam", "Tahta", "Demir", "Karton"], 0, "Cam saydamdır"),
    (2, 4, 4, "Hangi maddeden ışık geçmez?", ["Tahta", "Cam", "Su", "Hava"], 0, "Tahta ışığı geçirmez"),
    (2, 4, 4, "Gölge ne zaman uzun olur?", ["Güneş alçaktayken", "Güneş tepedeyken", "Gece", "Bulutluyken"], 0, "Sabah ve akşam gölge uzar"),
    (2, 4, 4, "Ses hangi ortamda yayılır?", ["Katı, sıvı ve gazda", "Sadece havada", "Sadece suda", "Boşlukta"], 0, "Madde ortamı gerekir"),
    (2, 4, 4, "Uzayda ses duyulur mu?", ["Hayır, boşlukta yayılmaz", "Evet", "Bazen", "Sadece gündüz"], 0, "Ses maddeye ihtiyaç duyar"),
    # Band 3
    (3, 4, 4, "Yankı nasıl oluşur?", ["Ses bir yüzeye çarpıp geri döner", "Ses kaybolur", "Ses hızlanır", "Ses artar"], 0, "Sesin yansıması"),
    (3, 4, 4, "Işık bir aynaya çarpınca ne olur?", ["Yansır", "Kaybolur", "Emilir", "Isıya dönüşür"], 0, "Yansıma"),
    (3, 4, 4, "Şeffaf, yarı saydam ve opak farkı nedir?", ["Işığı geçirme miktarı", "Renk farkı", "Ağırlık farkı", "Boyut farkı"], 0, "Işık geçirgenliği"),
    (3, 4, 4, "Sesin şiddeti neye bağlıdır?", ["Titreşimin büyüklüğüne", "Renge", "Işığa", "Sıcaklığa"], 0, "Titreşim genliği"),
    (3, 4, 4, "Ses kirliliği nedir?", ["Rahatsız edici yüksek sesler", "Sessizlik", "Müzik", "Konuşma"], 0, "Zararlı gürültü"),
    (3, 4, 4, "Gürültüden korunmak için ne yapılır?", ["Ses yalıtımı", "Pencere açmak", "Yüksek sesle konuşmak", "Hiçbir şey"], 0, "Yalıtım malzemeleri"),
    # Band 4
    (4, 4, 4, "Işık mı ses mi daha hızlıdır?", ["Işık", "Ses", "Eşittir", "Değişir"], 0, "Işık çok daha hızlıdır"),
    (4, 4, 4, "Şimşeği neden gök gürültüsünden önce görürüz?", ["Işık sesten hızlıdır", "Ses yoktur", "Işık geç gelir", "Rastgeledir"], 0, "Işık hızı > ses hızı"),
    (4, 4, 4, "Aydınlatma teknolojileri neden geliştirilmiştir?", ["Daha az enerjiyle daha çok ışık için", "Süs için", "Renk için", "Ses için"], 0, "Enerji verimliliği"),
    (4, 4, 4, "Tam gölge ne zaman oluşur?", ["Işık tamamen engellenince", "Işık geçince", "Karanlıkta", "Aydınlıkta"], 0, "Opak cisim arkasında"),
    # Band 5
    (5, 4, 4, "Sesin yayılma hızı hangi ortamda en fazladır?", ["Katı", "Sıvı", "Gaz", "Boşluk"], 0, "Katıda tanecikler sık, ses hızlı yayılır"),
    (5, 4, 4, "Işık kirliliği nedir?", ["Gereksiz ve fazla yapay aydınlatma", "Karanlık", "Az ışık", "Doğal ışık"], 0, "Gökyüzü gözlemini ve canlıları etkiler"),
]

# ==================================================== ELEKTRIK

ELEKTRIK = [
    # Band 1
    (1, 4, 4, "Ampulü yakmak için ne gerekir?", ["Elektrik", "Su", "Hava", "Toprak"], 0, "Elektrik enerjisi"),
    (1, 4, 4, "Hangisi elektrikle çalışır?", ["Buzdolabı", "Sandalye", "Kitap", "Masa"], 0, "Buzdolabı elektrikli araçtır"),
    (1, 4, 4, "Pil ne işe yarar?", ["Elektrik enerjisi sağlar", "Işık verir", "Ses çıkarır", "Isıtır"], 0, "Enerji kaynağı"),
    (1, 4, 4, "Elektrik prizine ne sokulmamalı?", ["Hiçbir şey", "Fiş", "Kablo", "Priz"], 0, "Sadece fiş takılır"),
    (1, 4, 4, "Islak elle elektrikli alete dokunulur mu?", ["Hayır, çok tehlikeli", "Evet", "Bazen", "Fark etmez"], 0, "Su elektriği iletir"),
    # Band 2
    (2, 4, 4, "Basit elektrik devresinde neler bulunur?", ["Pil, ampul, kablo", "Sadece ampul", "Sadece pil", "Su ve toprak"], 0, "Kaynak + iletken + alıcı"),
    (2, 4, 4, "Devre kesilirse ampul ne olur?", ["Söner", "Yanar", "Parlar", "Değişmez"], 0, "Akım geçmez"),
    (2, 4, 4, "Anahtarın görevi nedir?", ["Devreyi açıp kapatmak", "Işık vermek", "Isıtmak", "Ses çıkarmak"], 0, "Akım kontrolü"),
    (2, 4, 4, "Hangisi elektriği iletir?", ["Bakır tel", "Plastik", "Cam", "Tahta"], 0, "Metaller iletkendir"),
    (2, 4, 4, "Hangisi elektriği iletmez?", ["Plastik", "Bakır", "Demir", "Alüminyum"], 0, "Plastik yalıtkandır"),
    (2, 4, 4, "Kablolar neden plastikle kaplıdır?", ["Yalıtım ve güvenlik için", "Süs için", "Ağırlık için", "Renk için"], 0, "Plastik yalıtkandır"),
    # Band 3
    (3, 4, 4, "Elektrik devresinde akım nereden geçer?", ["İletken kablodan", "Havadan", "Plastikten", "Camdan"], 0, "İletken yol"),
    (3, 4, 4, "İki pil kullanınca ampul nasıl olur?", ["Daha parlak yanar", "Söner", "Değişmez", "Kırılır"], 0, "Daha fazla enerji"),
    (3, 4, 4, "Elektrik tasarrufu için ne yapılır?", ["Gereksiz ışıkları kapatmak", "Hepsini açmak", "Sürekli çalıştırmak", "Hiçbir şey"], 0, "Bilinçli kullanım"),
    (3, 4, 4, "Elektrik enerjisi hangi enerjilere dönüşür?", ["Işık, ısı, hareket", "Sadece ışık", "Sadece ısı", "Hiçbiri"], 0, "Çok yönlü dönüşüm"),
    (3, 4, 4, "Elektrikli ısıtıcıda elektrik neye dönüşür?", ["Isı enerjisine", "Ses enerjisine", "Işık enerjisine", "Hareket enerjisine"], 0, "Isı dönüşümü"),
    (3, 4, 4, "Vantilatörde elektrik neye dönüşür?", ["Hareket enerjisine", "Isı enerjisine", "Ses enerjisine", "Işığa"], 0, "Hareket (kinetik) enerji"),
    # Band 4
    (4, 4, 4, "Elektrik santralleri ne yapar?", ["Elektrik enerjisi üretir", "Elektrik tüketir", "Su üretir", "Isı depolar"], 0, "Enerji üretimi"),
    (4, 4, 4, "Hangisi yenilenebilir elektrik kaynağıdır?", ["Rüzgar", "Kömür", "Petrol", "Doğalgaz"], 0, "Rüzgar tükenmez"),
    (4, 4, 4, "Güneş panelleri ne yapar?", ["Güneş enerjisini elektriğe çevirir", "Isıtır", "Aydınlatır", "Su üretir"], 0, "Fotovoltaik dönüşüm"),
    (4, 4, 4, "Kısa devre nedir?", ["Akımın yanlış yoldan geçmesi", "Devrenin kapanması", "Pilin bitmesi", "Ampulün yanması"], 0, "Tehlikeli durum, yangın riski"),
    # Band 5
    (5, 4, 4, "Elektrik akımının birimi nedir?", ["Amper", "Volt", "Watt", "Ohm"], 0, "Amper (A)"),
    (5, 4, 4, "Elektrik enerjisi neden tasarruflu kullanılmalı?", ["Kaynaklar sınırlı ve çevreye zarar veriyor", "Pahalı olduğu için sadece", "Gereksiz", "Zor üretildiği için"], 0, "Çevre + kaynak"),
]

# ==================================================== BESLENME VE SINDIRIM

BESLENME = [
    # Band 1
    (1, 4, 4, "Besinler bize ne verir?", ["Enerji", "Renk", "Ses", "Işık"], 0, "Besinler enerji kaynağıdır"),
    (1, 4, 4, "Hangisi sağlıklı besindir?", ["Sebze", "Cips", "Gazoz", "Şekerleme"], 0, "Sebzeler sağlıklıdır"),
    (1, 4, 4, "Günde kaç öğün yemeliyiz?", ["3 ana öğün", "1 öğün", "5 ana öğün", "Sürekli"], 0, "Sabah, öğle, akşam"),
    (1, 4, 4, "Yemek yerken ne yapmalıyız?", ["İyi çiğnemeliyiz", "Hızlı yutmalıyız", "Konuşmalıyız", "Koşmalıyız"], 0, "Çiğnemek sindirimi kolaylaştırır"),
    (1, 4, 4, "Su vücudumuz için gerekli midir?", ["Evet, çok gerekli", "Hayır", "Bazen", "Sadece yazın"], 0, "Su hayati önemdedir"),
    # Band 2
    (2, 4, 4, "Sindirim nerede başlar?", ["Ağızda", "Midede", "Bağırsakta", "Yemek borusunda"], 0, "Ağızda çiğneme + tükürük"),
    (2, 4, 4, "Besinler ağızdan sonra nereye gider?", ["Yemek borusuna", "Mideye", "Bağırsağa", "Akciğere"], 0, "Yemek borusu"),
    (2, 4, 4, "Hangisi protein kaynağıdır?", ["Et", "Ekmek", "Şeker", "Yağ"], 0, "Et, yumurta, süt protein içerir"),
    (2, 4, 4, "Hangisi vitamin kaynağıdır?", ["Meyve", "Ekmek", "Yağ", "Tuz"], 0, "Meyve ve sebzeler"),
    (2, 4, 4, "Süt hangi besin grubundadır?", ["Süt ve ürünleri", "Et grubu", "Tahıl grubu", "Yağ grubu"], 0, "Süt grubu, kalsiyum kaynağı"),
    (2, 4, 4, "Dişlerimiz sindirimde ne yapar?", ["Besinleri parçalar", "Tat alır", "Yutar", "Emer"], 0, "Mekanik sindirim"),
    # Band 3
    (3, 4, 4, "Sindirim sisteminin bölümleri nelerdir?", ["Ağız, yemek borusu, mide, bağırsaklar", "Sadece mide", "Kalp ve akciğer", "Böbrek"], 0, "Sindirim kanalı"),
    (3, 4, 4, "Midede ne olur?", ["Besinler öğütülür ve karıştırılır", "Besin emilir", "Besin çiğnenir", "Hiçbir şey"], 0, "Kimyasal + mekanik sindirim"),
    (3, 4, 4, "Besinlerin kana geçtiği yer neresidir?", ["İnce bağırsak", "Mide", "Ağız", "Yemek borusu"], 0, "İnce bağırsakta emilim"),
    (3, 4, 4, "Dengeli beslenme nedir?", ["Tüm besin gruplarından yeterli almak", "Az yemek", "Çok yemek", "Sadece meyve yemek"], 0, "Çeşitli + yeterli"),
    (3, 4, 4, "Karbonhidratlar ne işe yarar?", ["Enerji verir", "Kemik yapar", "Kan üretir", "Saç uzatır"], 0, "Ana enerji kaynağı"),
    (3, 4, 4, "Kalsiyum hangi organımız için önemlidir?", ["Kemikler ve dişler", "Gözler", "Kulaklar", "Saçlar"], 0, "Kemik gelişimi"),
    # Band 4
    (4, 4, 4, "Besin zehirlenmesinden nasıl korunuruz?", ["Temiz ve taze besin tüketerek", "Çok yiyerek", "Az yiyerek", "Hiç yemeyerek"], 0, "Hijyen ve tazelik"),
    (4, 4, 4, "Son kullanma tarihi neden önemlidir?", ["Bozulmuş besin zararlıdır", "Fiyat için", "Süs için", "Gereksizdir"], 0, "Gıda güvenliği"),
    (4, 4, 4, "Kalın bağırsağın görevi nedir?", ["Su emilimi ve atık oluşumu", "Besin emilimi", "Çiğneme", "Öğütme"], 0, "Su emilir, atık oluşur"),
    (4, 4, 4, "Aşırı şekerli beslenme neye yol açar?", ["Diş çürüğü ve kilo artışı", "Uzun boy", "Güçlü kemik", "İyi görme"], 0, "Şekerin zararları"),
    # Band 5
    (5, 4, 4, "Besin piramidinin tabanında ne bulunur?", ["Tahıllar", "Yağlar", "Şeker", "Et"], 0, "En çok tüketilmesi gerekenler altta"),
    (5, 4, 4, "Sindirim enzimleri ne yapar?", ["Besinleri kimyasal olarak parçalar", "Besinleri çiğner", "Su emer", "Enerji verir"], 0, "Kimyasal sindirim"),
]
