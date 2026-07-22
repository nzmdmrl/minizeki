"""
FEN BILIMLERI soru bankasi (3-4. sinif).

MUFREDAT NOTU:
  - 1-2. sinifta Fen Bilimleri YOKTUR (Hayat Bilgisi vardir)
  - Fen 3. sinifta baslar
  - Isik/Ses, Elektrik, Beslenme 4. sinif uniteleridir

Band hedef dogruluk: 1=%90  2=%75  3=%60  4=%40  5=%20
Format: (band, sinif_min, sinif_max, soru, [siklar], dogru_index, aciklama)
"""

# ==================================================== DUNYA VE GOKYUZU

DUNYA_GOKYUZU = [
    # Band 1
    (1, 3, 4, "Dünya'nın şekli nasıldır?", ["Küreye benzer", "Kare", "Üçgen", "Düz"], 0, "Dünya küre şeklindedir"),
    (1, 3, 4, "Gündüz gökyüzünde ne görürüz?", ["Güneş", "Ay", "Yıldızlar", "Hiçbiri"], 0, "Gündüz Güneş görünür"),
    (1, 3, 4, "Gece gökyüzünde ne görürüz?", ["Ay ve yıldızlar", "Güneş", "Gökkuşağı", "Hiçbiri"], 0, "Gece Ay ve yıldızlar"),
    (1, 3, 4, "Dünya'nın uydusu hangisidir?", ["Ay", "Güneş", "Mars", "Venüs"], 0, "Ay, Dünya'nın tek doğal uydusudur"),
    (1, 3, 4, "Güneş bize ne verir?", ["Işık ve ısı", "Su", "Toprak", "Hava"], 0, "Güneş ışık ve ısı kaynağıdır"),
    (1, 3, 4, "Dünya'nın yüzeyinin çoğu neyle kaplıdır?", ["Su", "Toprak", "Kum", "Buz"], 0, "Yaklaşık dörtte üçü sudur"),
    (1, 3, 4, "Hangisi gökyüzünde görülür?", ["Bulut", "Ağaç", "Taş", "Çiçek"], 0, "Bulutlar gökyüzündedir"),
    # Band 2
    (2, 3, 4, "Ay'ın şekli neden değişiyor gibi görünür?", ["Dünya çevresinde döndüğü için", "Küçüldüğü için", "Büyüdüğü için", "Kaybolduğu için"], 0, "Ay evreleri"),
    (2, 3, 4, "Gece ve gündüz nasıl oluşur?", ["Dünya kendi ekseni etrafında döner", "Güneş söner", "Ay engel olur", "Bulutlar kapatır"], 0, "Dünya'nın kendi ekseni etrafındaki dönüşü"),
    (2, 3, 4, "Dünya'nın kendi ekseni etrafındaki dönüşü kaç saat sürer?", ["24 saat", "12 saat", "365 gün", "30 gün"], 0, "Bir gün = 24 saat"),
    (2, 3, 4, "Güneş bir gezegen midir?", ["Hayır, yıldızdır", "Evet", "Uydudur", "Bulutdur"], 0, "Güneş bir yıldızdır"),
    (2, 3, 4, "Ay kendi ışığını üretir mi?", ["Hayır, Güneş'ten yansıtır", "Evet", "Bazen", "Sadece geceleri"], 0, "Ay Güneş ışığını yansıtır"),
    (2, 3, 4, "Dünya'nın kara parçalarına ne denir?", ["Kıta", "Okyanus", "Deniz", "Göl"], 0, "Kıtalar"),
    (2, 3, 4, "Gökyüzü gündüz neden mavi görünür?", ["Güneş ışığı havada dağılır", "Deniz yansır", "Bulutlar mavi", "Uzay mavi"], 0, "Işığın atmosferde dağılması"),
    (2, 4, 4, "Yıldızlar gündüz neden görünmez?", ["Güneş ışığı çok parlak", "Kaybolurlar", "Sönerler", "Bulutlar kapatır"], 0, "Güneş'in parlaklığı"),
    # Band 3
    (3, 3, 4, "Dünya'nın Güneş etrafındaki bir turu ne kadar sürer?", ["1 yıl", "1 ay", "1 gün", "1 hafta"], 0, "365 gün = 1 yıl"),
    (3, 3, 4, "Mevsimler neden oluşur?", ["Dünya'nın eğik ekseni ve Güneş etrafındaki dönüşü", "Güneş'in sönmesi", "Ay'ın hareketi", "Bulutlar"], 0, "Eksen eğikliği + yıllık hareket"),
    (3, 4, 4, "Ay'ın evreleri nelerdir?", ["Yeni ay, ilk dördün, dolunay, son dördün", "Sadece dolunay", "Sadece yeni ay", "Değişmez"], 0, "4 ana evre"),
    (3, 3, 4, "Güneş tutulması nasıl olur?", ["Ay, Dünya ile Güneş arasına girer", "Güneş söner", "Dünya durur", "Bulutlar kapatır"], 0, "Ay gölgesi Dünya'ya düşer"),
    (3, 4, 4, "Ay tutulması nasıl olur?", ["Dünya, Güneş ile Ay arasına girer", "Ay söner", "Güneş kaybolur", "Ay küçülür"], 0, "Dünya'nın gölgesi Ay'a düşer"),
    (3, 3, 4, "Güneş sisteminde kaç gezegen vardır?", ["8", "9", "7", "10"], 0, "8 gezegen"),
    (3, 3, 4, "Dünya kaçıncı gezegendir?", ["3.", "1.", "2.", "4."], 0, "Güneş'ten üçüncü gezegen"),
    (3, 4, 4, "Hangisi Dünya'ya en yakın gezegendir?", ["Venüs", "Mars", "Jüpiter", "Satürn"], 0, "Venüs en yakın komşudur"),
    # Band 4
    (4, 4, 4, "Atmosfer ne işe yarar?", ["Canlıları korur ve nefes almamızı sağlar", "Işık üretir", "Isı üretir", "Su üretir"], 0, "Koruyucu gaz tabakası"),
    (4, 4, 4, "Kuzey Yarım Küre'de yaz olduğunda Güney'de ne olur?", ["Kış", "Yaz", "İlkbahar", "Aynı mevsim"], 0, "Mevsimler terstir"),
    (4, 4, 4, "Gezegenler kendi ışıklarını üretir mi?", ["Hayır, yıldızlardan yansıtır", "Evet", "Bazıları", "Sadece geceleri"], 0, "Gezegenler ışık yansıtır"),
    (4, 4, 4, "Dünya'nın ekseni neden eğiktir denir?", ["Eğik olduğu için mevsimler oluşur", "Düzdür", "Eğik değildir", "Bilinmez"], 0, "23,5 derece eğiklik"),
    # Band 5
    (5, 4, 4, "Güneş sisteminin merkezinde ne vardır?", ["Güneş", "Dünya", "Ay", "Jüpiter"], 0, "Güneş merkezdedir"),
    (5, 4, 4, "Yerçekimi ne yapar?", ["Cisimleri Dünya'ya doğru çeker", "İter", "Isıtır", "Aydınlatır"], 0, "Kütle çekim kuvveti"),
]

# ==================================================== DUYU ORGANLARI

DUYU_ORGANLARI = [
    # Band 1
    (1, 3, 4, "Kaç duyu organımız vardır?", ["5", "3", "4", "6"], 0, "Göz, kulak, burun, dil, deri"),
    (1, 3, 4, "Görme organımız hangisidir?", ["Göz", "Kulak", "Burun", "Dil"], 0, "Göz"),
    (1, 3, 4, "İşitme organımız hangisidir?", ["Kulak", "Göz", "Burun", "Deri"], 0, "Kulak"),
    (1, 3, 4, "Koklama organımız hangisidir?", ["Burun", "Dil", "Göz", "Kulak"], 0, "Burun"),
    (1, 3, 4, "Tat alma organımız hangisidir?", ["Dil", "Burun", "Göz", "Deri"], 0, "Dil"),
    (1, 3, 4, "Dokunma duyusunu hangi organla alırız?", ["Deri", "Göz", "Kulak", "Dil"], 0, "Deri"),
    (1, 3, 4, "Yemeğin tadını hangi organla anlarız?", ["Dil", "Göz", "Kulak", "El"], 0, "Dil"),
    # Band 2
    (2, 3, 4, "Gözümüzü korumak için ne yapmalıyız?", ["Uzaktan ve iyi ışıkta okumalıyız", "Karanlıkta okumalıyız", "Yakından bakmalıyız", "Ovalamalıyız"], 0, "Işık ve mesafe önemli"),
    (2, 3, 4, "Kulağımıza sivri cisim sokmak nasıldır?", ["Çok tehlikeli", "Faydalı", "Normal", "Gerekli"], 0, "Kulak zarı zarar görür"),
    (2, 3, 4, "Dilimizin aldığı temel tatlar hangileridir?", ["Tatlı, tuzlu, ekşi, acı", "Sadece tatlı", "Sadece tuzlu", "Sıcak ve soğuk"], 0, "4 temel tat"),
    (2, 3, 4, "Nezleyken tat almakta zorlanırız çünkü?", ["Burun tıkalıdır", "Dil çalışmaz", "Göz kapalıdır", "Kulak tıkalıdır"], 0, "Koku ve tat birlikte çalışır"),
    (2, 3, 4, "Deri hangi duyuları alır?", ["Sıcak, soğuk, acı, dokunma", "Sadece dokunma", "Sadece acı", "Sadece sıcaklık"], 0, "Deri çok yönlü duyu organıdır"),
    (2, 3, 4, "Çok yüksek ses kulağımıza ne yapar?", ["Zarar verir", "Faydalı olur", "Bir şey olmaz", "Güçlendirir"], 0, "İşitme kaybı riski"),
    (2, 3, 4, "Duyu organlarımızı ne ile temizlemeliyiz?", ["Temiz su ve uygun malzeme", "Sivri cisim", "Kirli bez", "Hiçbir şey"], 0, "Uygun temizlik"),
    # Band 3
    (3, 3, 4, "Gözün rengini veren bölüm hangisidir?", ["İris", "Gözbebeği", "Kirpik", "Kaş"], 0, "İris göz rengini belirler"),
    (3, 3, 4, "Kaş ve kirpikler ne işe yarar?", ["Gözü ter ve tozdan korur", "Süs içindir", "Görmeyi sağlar", "Renk verir"], 0, "Koruyucu görev"),
    (3, 4, 4, "Kulakta sesi ilk karşılayan yapı nedir?", ["Kulak kepçesi", "Kulak zarı", "Çekiç kemiği", "Salyangoz"], 0, "Kulak kepçesi sesi toplar"),
    (3, 3, 4, "Burnumuzdaki kıllar ne işe yarar?", ["Tozu ve mikropları süzer", "Süs içindir", "Koku alır", "Nefes verir"], 0, "Filtre görevi"),
    (3, 3, 4, "Gözlük neden takılır?", ["Görme kusurunu düzeltmek için", "Süs için", "Güneşten korunmak için hep", "Gereksizdir"], 0, "Görme kusuru düzeltilir"),
    (3, 4, 4, "Duyu organlarımız bilgiyi nereye iletir?", ["Beyne", "Kalbe", "Mideye", "Akciğere"], 0, "Sinirler beyne iletir"),
    (3, 3, 4, "Karanlıkta gözbebeğimiz ne olur?", ["Büyür", "Küçülür", "Değişmez", "Kapanır"], 0, "Daha çok ışık almak için büyür"),
    # Band 4
    (4, 4, 4, "Gözde görüntünün oluştuğu tabaka hangisidir?", ["Retina", "Kornea", "İris", "Gözbebeği"], 0, "Retina (ağ tabaka)"),
    (4, 4, 4, "İşitme kaybını önlemek için ne yapmalıyız?", ["Yüksek sesten uzak durmalıyız", "Kulaklığı açmalıyız", "Gürültüde durmalıyız", "Hiçbir şey"], 0, "Gürültüden korunma"),
    (4, 4, 4, "Dilin üzerindeki küçük çıkıntılara ne denir?", ["Tat tomurcukları", "Kaslar", "Damarlar", "Kemikler"], 0, "Tat tomurcukları"),
    (4, 4, 4, "Duyu organları arasında en geniş olanı hangisidir?", ["Deri", "Göz", "Kulak", "Dil"], 0, "Deri vücudun tamamını kaplar"),
    # Band 5
    (5, 4, 4, "Koku ve tat duyusu neden birlikte çalışır?", ["Yiyeceğin lezzetini birlikte oluştururlar", "Aynı organdır", "İlgisizdir", "Sırayla çalışır"], 0, "Lezzet = tat + koku"),
    (5, 4, 4, "Duyu organlarındaki bilgi hangi yolla iletilir?", ["Sinirler", "Kan damarları", "Kaslar", "Kemikler"], 0, "Sinir sistemi"),
]

# ==================================================== HAREKET VE KUVVET

KUVVET_HAREKET = [
    # Band 1
    (1, 3, 4, "Bir cismi hareket ettirmek için ne gerekir?", ["Kuvvet", "Renk", "Ses", "Işık"], 0, "Kuvvet hareket başlatır"),
    (1, 3, 4, "İtmek ve çekmek nedir?", ["Kuvvet", "Hız", "Ses", "Işık"], 0, "İtme/çekme = kuvvet"),
    (1, 3, 4, "Topu tekmelediğimizde ne uygularız?", ["Kuvvet", "Isı", "Işık", "Ses"], 0, "Kuvvet uygularız"),
    (1, 3, 4, "Hangisi hareket eden bir cisimdir?", ["Koşan çocuk", "Duran masa", "Asılı tablo", "Duvar"], 0, "Hareket = yer değiştirme"),
    (1, 3, 4, "Kapıyı açarken ne yaparız?", ["İteriz veya çekeriz", "Isıtırız", "Aydınlatırız", "Sesletiriz"], 0, "İtme veya çekme"),
    (1, 3, 4, "Yayı gerdiğimizde ne olur?", ["Şekli değişir", "Rengi değişir", "Kaybolur", "Isınır"], 0, "Kuvvet şekli değiştirir"),
    # Band 2
    (2, 3, 4, "Kuvvet cisimlerde neleri değiştirebilir?", ["Hız, yön ve şekil", "Sadece renk", "Sadece ses", "Sadece koku"], 0, "Kuvvetin etkileri"),
    (2, 3, 4, "Bisiklet frenine bastığımızda ne olur?", ["Yavaşlar", "Hızlanır", "Yön değiştirir", "Durur duruken"], 0, "Fren yavaşlatır"),
    (2, 3, 4, "Hamuru yoğururken ne değiştiririz?", ["Şeklini", "Rengini", "Sesini", "Kokusunu"], 0, "Şekil değişimi"),
    (2, 3, 4, "Yerçekimi cisimleri nereye çeker?", ["Yere doğru", "Yukarı", "Yana", "Hiçbir yere"], 0, "Dünya'nın merkezine doğru"),
    (2, 3, 4, "Topu havaya attığımızda neden geri düşer?", ["Yerçekimi", "Rüzgar", "Hava", "Ses"], 0, "Yerçekimi kuvveti"),
    (2, 3, 4, "Mıknatıs hangi maddeyi çeker?", ["Demir", "Tahta", "Cam", "Plastik"], 0, "Mıknatıs demiri çeker"),
    (2, 4, 4, "Hangisi kuvvet uygulamaz?", ["Bakmak", "İtmek", "Çekmek", "Kaldırmak"], 0, "Bakmak kuvvet değildir"),
    # Band 3
    (3, 3, 4, "Sürtünme kuvveti ne yapar?", ["Hareketi yavaşlatır", "Hızlandırır", "Yön değiştirir", "Etkisizdir"], 0, "Sürtünme hareketi zorlaştırır"),
    (3, 3, 4, "Buzda neden kayarız?", ["Sürtünme azdır", "Sürtünme çoktur", "Yerçekimi yoktur", "Hava basıncı"], 0, "Buz pürüzsüzdür"),
    (3, 3, 4, "Ayakkabı tabanı neden pürüzlüdür?", ["Sürtünmeyi artırıp kaymayı önler", "Süs için", "Hafif olsun diye", "Ucuz olsun diye"], 0, "Sürtünme kaymayı önler"),
    (3, 4, 4, "Paraşüt nasıl çalışır?", ["Hava direnci düşüşü yavaşlatır", "Yerçekimini yok eder", "Uçurur", "İter"], 0, "Hava direnci"),
    (3, 3, 4, "Mıknatısın kaç kutbu vardır?", ["2", "1", "3", "4"], 0, "Kuzey ve güney kutbu"),
    (3, 4, 4, "İki mıknatısın aynı kutupları ne yapar?", ["Birbirini iter", "Çeker", "Yapışır", "Etkisizdir"], 0, "Aynı kutuplar iter"),
    (3, 4, 4, "İki mıknatısın zıt kutupları ne yapar?", ["Birbirini çeker", "İter", "Uzaklaşır", "Etkisizdir"], 0, "Zıt kutuplar çeker"),
    # Band 4
    (4, 4, 4, "Sürtünme kuvveti hangi durumda faydalıdır?", ["Fren yaparken", "Koşarken yorulunca", "Hızlanırken", "Hiçbir zaman"], 0, "Fren, yürüme, tutma"),
    (4, 4, 4, "Makinelerde yağ neden kullanılır?", ["Sürtünmeyi azaltmak için", "Artırmak için", "Isıtmak için", "Renk vermek için"], 0, "Yağ sürtünmeyi azaltır"),
    (4, 4, 4, "Kuvvetin birimi nedir?", ["Newton", "Metre", "Kilogram", "Saniye"], 0, "Newton (N)"),
    (4, 4, 4, "Ağır bir cismi kaldırmak neden zordur?", ["Yerçekimi kuvveti fazladır", "Renk koyudur", "Sıcaktır", "Büyüktür"], 0, "Kütle arttıkça çekim artar"),
    # Band 5
    (5, 4, 4, "Bir cisme kuvvet uygulanmazsa ne olur?", ["Hareket durumu değişmez", "Durur", "Hızlanır", "Yön değiştirir"], 0, "Eylemsizlik"),
    (5, 4, 4, "Uzayda cisimler neden ağırlıksız görünür?", ["Yerçekimi etkisi çok azdır", "Hava yoktur", "Soğuktur", "Karanlıktır"], 0, "Yerçekiminin az olması"),
]

# ==================================================== MADDE VE OZELLIKLERI

MADDE = [
    # Band 1
    (1, 3, 4, "Maddenin kaç hâli vardır?", ["3", "2", "4", "5"], 0, "Katı, sıvı, gaz"),
    (1, 3, 4, "Su hangi hâldedir?", ["Sıvı", "Katı", "Gaz", "Hiçbiri"], 0, "Su sıvıdır"),
    (1, 3, 4, "Buz hangi hâldedir?", ["Katı", "Sıvı", "Gaz", "Hiçbiri"], 0, "Buz katıdır"),
    (1, 3, 4, "Hava hangi hâldedir?", ["Gaz", "Katı", "Sıvı", "Hiçbiri"], 0, "Hava gazdır"),
    (1, 3, 4, "Hangisi katı maddedir?", ["Taş", "Süt", "Buhar", "Hava"], 0, "Taş katıdır"),
    (1, 3, 4, "Hangisi sıvı maddedir?", ["Süt", "Taş", "Tahta", "Demir"], 0, "Süt sıvıdır"),
    (1, 3, 4, "Katı maddelerin şekli nasıldır?", ["Belirlidir", "Değişkendir", "Yoktur", "Sıvı gibidir"], 0, "Katıların belirli şekli vardır"),
    # Band 2
    (2, 3, 4, "Sıvılar hangi şekli alır?", ["Bulundukları kabın şeklini", "Kendi şekillerini", "Kare", "Yuvarlak"], 0, "Sıvı kabın şeklini alır"),
    (2, 3, 4, "Su ısıtılınca ne olur?", ["Buharlaşır", "Donar", "Katılaşır", "Kaybolur"], 0, "Isı ile buharlaşma"),
    (2, 3, 4, "Su soğutulunca ne olur?", ["Donar", "Buharlaşır", "Erir", "Kaynar"], 0, "0°C'de donar"),
    (2, 3, 4, "Buz eriyince ne olur?", ["Su olur", "Buhar olur", "Kaybolur", "Taş olur"], 0, "Katı → sıvı"),
    (2, 3, 4, "Gazların şekli var mıdır?", ["Hayır, her yeri doldurur", "Evet, belirlidir", "Kare", "Yuvarlak"], 0, "Gaz bulunduğu hacmi doldurur"),
    (2, 3, 4, "Hangisi maddenin ölçülebilen özelliğidir?", ["Kütle", "Güzellik", "Mutluluk", "Hız"], 0, "Kütle ölçülebilir"),
    (2, 4, 4, "Kütle hangi araçla ölçülür?", ["Terazi", "Cetvel", "Termometre", "Saat"], 0, "Terazi"),
    # Band 3
    (3, 3, 4, "Erime nedir?", ["Katının sıvıya dönüşmesi", "Sıvının gaza dönüşmesi", "Gazın sıvıya dönüşmesi", "Sıvının katıya dönüşmesi"], 0, "Katı → sıvı"),
    (3, 3, 4, "Donma nedir?", ["Sıvının katıya dönüşmesi", "Katının sıvıya dönüşmesi", "Sıvının gaza dönüşmesi", "Gazın katıya dönüşmesi"], 0, "Sıvı → katı"),
    (3, 3, 4, "Buharlaşma nedir?", ["Sıvının gaza dönüşmesi", "Gazın sıvıya dönüşmesi", "Katının sıvıya dönüşmesi", "Sıvının katıya dönüşmesi"], 0, "Sıvı → gaz"),
    (3, 4, 4, "Yoğuşma nedir?", ["Gazın sıvıya dönüşmesi", "Sıvının gaza dönüşmesi", "Katının erimesi", "Sıvının donması"], 0, "Gaz → sıvı"),
    (3, 3, 4, "Suyun kaynama sıcaklığı kaç derecedir?", ["100°C", "0°C", "50°C", "200°C"], 0, "Deniz seviyesinde 100°C"),
    (3, 3, 4, "Suyun donma sıcaklığı kaç derecedir?", ["0°C", "100°C", "10°C", "-100°C"], 0, "0°C"),
    (3, 4, 4, "Sıcaklık hangi araçla ölçülür?", ["Termometre", "Terazi", "Cetvel", "Saat"], 0, "Termometre"),
    (3, 4, 4, "Camdaki buğu nasıl oluşur?", ["Su buharı yoğuşur", "Cam ıslanır", "Yağmur yağar", "Cam erir"], 0, "Yoğuşma"),
    # Band 4
    (4, 4, 4, "Maddenin hâl değişimi neye bağlıdır?", ["Sıcaklığa", "Renge", "Şekle", "Kokuya"], 0, "Isı alışverişi"),
    (4, 4, 4, "Hâl değişiminde maddenin kütlesi ne olur?", ["Değişmez", "Artar", "Azalır", "Kaybolur"], 0, "Kütle korunur"),
    (4, 4, 4, "Hangisi saf maddedir?", ["Saf su", "Ayran", "Çorba", "Salata"], 0, "Saf su tek maddedir"),
    (4, 4, 4, "Karışım nedir?", ["Birden fazla maddenin bir arada bulunması", "Tek madde", "Saf madde", "Element"], 0, "İki veya daha fazla madde"),
    # Band 5
    (5, 4, 4, "Su neden 'evrensel çözücü' denir?", ["Birçok maddeyi çözebilir", "Her yerde var", "Şeffaf", "Ucuz"], 0, "Çok maddeyi çözer"),
    (5, 4, 4, "Isı ile sıcaklık arasındaki fark nedir?", ["Isı enerji, sıcaklık ölçüsüdür", "Aynı şeydir", "Isı ölçü, sıcaklık enerji", "Fark yoktur"], 0, "Isı = enerji, sıcaklık = ölçüm"),
]

# ==================================================== CANLILAR VE YASAM

CANLILAR = [
    # Band 1
    (1, 3, 4, "Hangisi canlıdır?", ["Ağaç", "Taş", "Su", "Hava"], 0, "Ağaç büyür ve çoğalır"),
    (1, 3, 4, "Canlılar ne yapar?", ["Büyür, beslenir, çoğalır", "Sadece durur", "Hiç değişmez", "Kırılır"], 0, "Canlıların ortak özellikleri"),
    (1, 3, 4, "Bitkiler nereden büyür?", ["Tohumdan", "Taştan", "Sudan", "Havadan"], 0, "Tohum"),
    (1, 3, 4, "Hangisi hayvandır?", ["Kelebek", "Gül", "Çam", "Kaya"], 0, "Kelebek hayvandır"),
    (1, 3, 4, "Hangisi bitkidir?", ["Papatya", "Kedi", "Kuş", "Balık"], 0, "Papatya bitkidir"),
    (1, 3, 4, "Canlılar yaşamak için neye ihtiyaç duyar?", ["Su, hava, besin", "Sadece güneş", "Sadece toprak", "Hiçbir şey"], 0, "Temel ihtiyaçlar"),
    # Band 2
    (2, 3, 4, "Bitkinin bölümleri nelerdir?", ["Kök, gövde, yaprak, çiçek", "Sadece yaprak", "Sadece kök", "Kanat ve kuyruk"], 0, "Bitki bölümleri"),
    (2, 3, 4, "Kökün görevi nedir?", ["Su ve mineral almak, tutunmak", "Işık almak", "Çiçek açmak", "Meyve vermek"], 0, "Kök besin ve destek sağlar"),
    (2, 3, 4, "Yaprağın görevi nedir?", ["Besin üretmek", "Su emmek", "Tutunmak", "Çoğalmak"], 0, "Fotosentez yaprakta olur"),
    (2, 3, 4, "Hangisi memeli hayvandır?", ["Kedi", "Kartal", "Balık", "Yılan"], 0, "Kedi yavrusunu emzirir"),
    (2, 3, 4, "Hangisi yumurta ile çoğalır?", ["Kuş", "İnek", "Köpek", "At"], 0, "Kuşlar yumurtlar"),
    (2, 3, 4, "Kurbağa hangi grupta yer alır?", ["İki yaşamlılar", "Memeliler", "Kuşlar", "Balıklar"], 0, "Amfibi (iki yaşamlı)"),
    (2, 4, 4, "Balıklar ne ile solunum yapar?", ["Solungaç", "Akciğer", "Deri", "Burun"], 0, "Solungaç"),
    # Band 3
    (3, 3, 4, "Fotosentez nedir?", ["Bitkinin güneş ışığıyla besin üretmesi", "Bitkinin su içmesi", "Bitkinin büyümesi", "Bitkinin çiçek açması"], 0, "Işık + su + CO2 → besin + O2"),
    (3, 3, 4, "Bitkiler fotosentezde havaya ne verir?", ["Oksijen", "Karbondioksit", "Azot", "Duman"], 0, "Oksijen üretilir"),
    (3, 3, 4, "Hayvanlar beslenmelerine göre nasıl ayrılır?", ["Etçil, otçul, hepçil", "Büyük, küçük", "Hızlı, yavaş", "Renkli, renksiz"], 0, "Beslenme tipleri"),
    (3, 3, 4, "Hangisi hepçil hayvandır?", ["Ayı", "Aslan", "İnek", "Koyun"], 0, "Ayı hem et hem bitki yer"),
    (3, 4, 4, "Besin zinciri nedir?", ["Canlıların birbirini yeme sırası", "Yiyecek listesi", "Market rafı", "Menü"], 0, "Enerji akışı"),
    (3, 3, 4, "Kelebek hangi evrelerden geçer?", ["Yumurta, tırtıl, koza, kelebek", "Sadece yumurta", "Doğrudan kelebek", "Yumurta ve kelebek"], 0, "Başkalaşım (metamorfoz)"),
    (3, 4, 4, "Hangisi sürüngendir?", ["Kaplumbağa", "Kurbağa", "Balık", "Kuş"], 0, "Kaplumbağa sürüngendir"),
    (3, 4, 4, "Mikroskop ne işe yarar?", ["Küçük canlıları görmemizi sağlar", "Uzağı görmemizi", "Isı ölçmeyi", "Ağırlık ölçmeyi"], 0, "Gözle görülmeyeni büyütür"),
    # Band 4
    (4, 4, 4, "Bitkilerin yaprağındaki yeşil maddeye ne denir?", ["Klorofil", "Selüloz", "Nişasta", "Protein"], 0, "Klorofil fotosentezi sağlar"),
    (4, 4, 4, "Doğal yaşam alanı ne demektir?", ["Canlının yaşadığı doğal ortam", "Hayvanat bahçesi", "Ev", "Kafes"], 0, "Habitat"),
    (4, 4, 4, "Nesli tükenen canlı ne demektir?", ["Artık yeryüzünde bulunmayan tür", "Az bulunan", "Küçük olan", "Nadir görülen"], 0, "Tamamen yok olmuş tür"),
    (4, 4, 4, "Canlıların çeşitliliğine ne denir?", ["Biyoçeşitlilik", "Ekosistem", "Habitat", "Popülasyon"], 0, "Biyoçeşitlilik"),
    # Band 5
    (5, 4, 4, "Ekosistemde üreticiler kimlerdir?", ["Bitkiler", "Etçiller", "Otçullar", "Mantarlar"], 0, "Bitkiler kendi besinini üretir"),
    (5, 4, 4, "Bir türün yok olması ekosistemi nasıl etkiler?", ["Doğal denge bozulur", "Etkilemez", "İyileştirir", "Hızlandırır"], 0, "Zincirleme etki"),
]
