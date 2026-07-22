"""
Hayat Bilgisi EK soru bankasi (Parti 1).
sorular_hayat.py'yi tamamlar. MEB'in 6 unitesine bagli.

Band hedef dogruluk: 1=%90  2=%75  3=%60  4=%40  5=%20
Format: (band, sinif_min, sinif_max, soru, [siklar], dogru_index, aciklama)
"""

# ==================================================== 1. OKULUMUZDA HAYAT

OKULUMUZ_EK = [
    # Band 1 — sinifin tamami bilir
    (1, 1, 3, "Okula gitmeden önce ne yaparız?", ["Çantamızı hazırlarız", "Uyuruz", "Oyun oynarız", "Televizyon izleriz"], 0, "Çanta bir gece önce hazırlanır"),
    (1, 1, 3, "Ders başlarken ne yaparız?", ["Yerimize otururuz", "Dışarı çıkarız", "Konuşuruz", "Yemek yeriz"], 0, "Ders zili çalınca yerimize otururuz"),
    (1, 1, 3, "Sınıfa girerken ne deriz?", ["Günaydın", "Hoşça kal", "İyi geceler", "Güle güle"], 0, "Selamlaşmak nezakettir"),
    (1, 1, 3, "Okulda yemek nerede yenir?", ["Yemekhanede", "Sınıfta", "Bahçede", "Koridorda"], 0, "Yemekhane"),
    (1, 1, 3, "Okul çantamızda ne olmalı?", ["Kitap ve defter", "Oyuncak", "Yastık", "Tabak"], 0, "Ders malzemeleri"),
    (1, 1, 3, "Öğretmenimize nasıl davranmalıyız?", ["Saygılı", "Kaba", "İlgisiz", "Bağırarak"], 0, "Saygı"),
    (1, 1, 3, "Sınıfta çöpü nereye atarız?", ["Çöp kutusuna", "Yere", "Sıraya", "Pencereye"], 0, "Çöp kutusu"),
    (1, 1, 3, "Merdivenden nasıl inmeliyiz?", ["Yavaş ve dikkatli", "Koşarak", "Atlayarak", "Kayarak"], 0, "Koşmak tehlikelidir"),
    # Band 2
    (2, 1, 3, "Arkadaşımızın kalemi kırıldı, ne yaparız?", ["Kalemimizi paylaşırız", "Görmezden geliriz", "Güleriz", "Uzaklaşırız"], 0, "Paylaşmak dostluktur"),
    (2, 1, 3, "Sınıf kitaplığındaki kitabı okuduktan sonra ne yaparız?", ["Yerine koyarız", "Sıramızda bırakırız", "Eve götürürüz", "Çantaya koyarız"], 0, "Ortak eşya yerine konur"),
    (2, 1, 3, "Okulda hangi davranış doğrudur?", ["Sıraya girmek", "İtişmek", "Bağırmak", "Koşmak"], 0, "Sıra beklemek"),
    (2, 1, 3, "Ders sırasında acil ihtiyacımız olursa ne yaparız?", ["İzin isteriz", "Sessizce çıkarız", "Bekleriz", "Bağırırız"], 0, "İzin istemek"),
    (2, 1, 3, "Okul bahçesindeki ağaçlara nasıl davranmalıyız?", ["Korumalıyız", "Dallarını kırmalıyız", "Yapraklarını koparmalıyız", "Tırmanmalıyız"], 0, "Doğayı korumak"),
    (2, 1, 3, "Okul kütüphanesinden kitap alırken ne yaparız?", ["Kaydettiririz", "Sessizce alırız", "Söylemeyiz", "Saklarız"], 0, "Kayıt yaptırılır"),
    (2, 2, 3, "Sınıfımıza yeni bir arkadaş geldi, ne yaparız?", ["Tanışır, yardım ederiz", "İlgilenmeyiz", "Uzak dururuz", "Alay ederiz"], 0, "Yeni arkadaşa yardım"),
    (2, 1, 3, "Okuldaki eşyalar kime aittir?", ["Hepimize", "Öğretmene", "Müdüre", "Kimseye"], 0, "Ortak kullanım"),
    (2, 1, 3, "Beden eğitimi dersinde ne giyeriz?", ["Eşofman", "Elbise", "Kravat", "Palto"], 0, "Rahat kıyafet"),
    (2, 2, 3, "Ödevimizi unutursak ne yaparız?", ["Öğretmene doğruyu söyleriz", "Yalan söyleriz", "Saklanırız", "Okula gitmeyiz"], 0, "Dürüstlük"),
    # Band 3
    (3, 2, 3, "Sınıf kuralları nasıl belirlenmeli?", ["Birlikte konuşarak", "Öğretmen tek başına", "En güçlü öğrenci", "Hiç belirlenmemeli"], 0, "Kurallar birlikte belirlenir"),
    (3, 2, 3, "Arkadaşımız bizimle oynamak istemiyorsa ne yaparız?", ["Saygı duyarız", "Zorlarız", "Küseriz", "Kavga ederiz"], 0, "Herkesin seçme hakkı vardır"),
    (3, 2, 3, "Okulda görevli olan hizmetliye nasıl davranmalıyız?", ["Saygılı ve teşekkür ederek", "İlgisiz", "Emir vererek", "Görmezden gelerek"], 0, "Herkes saygıyı hak eder"),
    (3, 2, 3, "Sınıfta bir eşya kırılırsa ne yaparız?", ["Söyleriz ve özür dileriz", "Saklanırız", "Başkasını suçlarız", "Susarız"], 0, "Sorumluluk almak"),
    (3, 2, 3, "Grup çalışmasında herkes ne yapmalı?", ["Görevini yapmalı", "İzlemeli", "Beklemeli", "Konuşmamalı"], 0, "İş bölümü"),
    (3, 2, 3, "Okulda hangi davranış arkadaşımızı üzer?", ["Lakap takmak", "Yardım etmek", "Paylaşmak", "Dinlemek"], 0, "Lakap takmak incitir"),
    (3, 2, 3, "Bir arkadaşımız hasta olduğunda ne yaparız?", ["Geçmiş olsun deriz, notlarını veririz", "Konuşmayız", "Yerini alırız", "Unuturuz"], 0, "Dayanışma"),
    (3, 2, 3, "Sınıf panosuna neler asılır?", ["Öğrenci çalışmaları", "Çöpler", "Kişisel eşyalar", "Yiyecekler"], 0, "Çalışmalarımız sergilenir"),
    (3, 2, 3, "Okulda düzenli olmak neden önemlidir?", ["Zamandan kazandırır", "Gereksizdir", "Yorucudur", "Sıkıcıdır"], 0, "Düzen zaman kazandırır"),
    (3, 3, 3, "Sınıfta oylama neden yapılır?", ["Herkesin fikri alınsın diye", "Zaman geçsin diye", "Öğretmen istediği için", "Eğlenceli olduğu için"], 0, "Demokratik karar"),
    # Band 4
    (4, 2, 3, "Sınıf başkanı nasıl seçilmeli?", ["Oylama ile", "En güçlü olan", "En uzun boylu", "Öğretmen seçer"], 0, "Seçim oylamayla yapılır"),
    (4, 2, 3, "Bir arkadaşımız haksızlığa uğrarsa ne yaparız?", ["Yanında oluruz, öğretmene söyleriz", "Karışmayız", "Biz de katılırız", "İzleriz"], 0, "Haksızlığa sessiz kalmamak"),
    (4, 3, 3, "Okul kulübüne neden katılırız?", ["İlgi alanımızı geliştirmek için", "Ders kaçırmak için", "Not almak için", "Mecbur olduğumuz için"], 0, "Kulüpler yetenek geliştirir"),
    (4, 3, 3, "Okulda çıkan bir sorunu kime iletiriz?", ["Öğretmen veya müdüre", "Kimseye", "Sadece arkadaşımıza", "Ailemize"], 0, "Yetkiliye bildirmek"),
    (4, 3, 3, "Sınıf nöbetçisinin görevi nedir?", ["Sınıf düzenine yardım", "Ders anlatmak", "Not vermek", "Ceza vermek"], 0, "Düzene yardım"),
    (4, 3, 3, "Okulda 'hoşgörü' ne demektir?", ["Farklılıklara saygı", "Her şeye izin", "Kural tanımamak", "Sessiz kalmak"], 0, "Farklılıklara saygı"),
    # Band 5
    (5, 3, 3, "Okulda demokrasi nasıl uygulanır?", ["Herkesin fikrini söyleyip oylama yaparak", "En güçlünün dediği olarak", "Öğretmenin kararıyla", "Kura çekerek"], 0, "Fikir özgürlüğü + oylama"),
    (5, 3, 3, "Sorumluluk almak ne demektir?", ["Görevimizi yapmak ve sonucuna katlanmak", "Başkasını suçlamak", "İşten kaçmak", "Beklemek"], 0, "Sorumluluk = görev + sonuç"),
    (5, 3, 3, "Okulda ortak yaşam kültürü neyi gerektirir?", ["Saygı, paylaşım ve kurallara uymayı", "Sadece susmayı", "Sadece çalışmayı", "Yalnız kalmayı"], 0, "Ortak yaşam çok yönlüdür"),
]

# ==================================================== 2. EVIMIZDE HAYAT

AILEMIZ_EK = [
    # Band 1
    (1, 1, 3, "Ailemizde kim en küçüktür?", ["Bebek", "Anne", "Baba", "Dede"], 0, "Bebek en küçük üyedir"),
    (1, 1, 3, "Kardeşimizin kardeşi bize ne olur?", ["Kardeş", "Kuzen", "Amca", "Dayı"], 0, "Kardeşimizin kardeşi de kardeşimizdir"),
    (1, 1, 3, "Evde uyuduğumuz oda hangisidir?", ["Yatak odası", "Mutfak", "Banyo", "Salon"], 0, "Yatak odası"),
    (1, 1, 3, "Yemekler nerede pişirilir?", ["Mutfakta", "Salonda", "Banyoda", "Balkonda"], 0, "Mutfak"),
    (1, 1, 3, "Evimizi kim temizler?", ["Hepimiz", "Sadece anne", "Sadece baba", "Kimse"], 0, "Ev işleri paylaşılır"),
    (1, 1, 3, "Oyuncaklarımızla oynadıktan sonra ne yaparız?", ["Toplarız", "Bırakırız", "Kırarız", "Saklarız"], 0, "Oyuncaklar toplanır"),
    (1, 1, 3, "Ailemizde en yaşlı kim olabilir?", ["Dede veya nine", "Anne", "Kardeş", "Bebek"], 0, "Büyükanne ve büyükbaba"),
    (1, 1, 3, "Eve girerken ne çıkarırız?", ["Ayakkabılarımızı", "Çorabımızı", "Kazağımızı", "Hiçbir şeyi"], 0, "Temizlik için ayakkabı"),
    # Band 2
    (2, 1, 3, "Halamızın çocuğu bize ne olur?", ["Kuzen", "Kardeş", "Yeğen", "Amca"], 0, "Hala/amca/teyze/dayı çocukları → kuzen"),
    (2, 1, 3, "Kardeşimizin çocuğu bize ne olur?", ["Yeğen", "Kuzen", "Torun", "Kardeş"], 0, "Kardeşimizin çocuğu → yeğen"),
    (2, 1, 3, "Dedemizin bize göre torunu kimdir?", ["Biziz", "Babamız", "Amcamız", "Halamız"], 0, "Biz dedemizin torunuyuz"),
    (2, 1, 3, "Diş fırçamız kime aittir?", ["Sadece bize", "Herkese", "Kardeşimize", "Anneye"], 0, "Kişisel eşya paylaşılmaz"),
    (2, 1, 3, "Evde sofrayı kurarken ne yaparız?", ["Yardım ederiz", "Bekleriz", "Oynarız", "TV izleriz"], 0, "Aileye yardım"),
    (2, 1, 3, "Buzdolabının kapağını neden açık bırakmayız?", ["Elektrik harcar", "Ses yapar", "Kirlenir", "Sorun olmaz"], 0, "Enerji tasarrufu"),
    (2, 2, 3, "Odamızı toplamak kimin görevidir?", ["Bizim", "Annemizin", "Kardeşimizin", "Kimsenin"], 0, "Kendi alanımızdan sorumluyuz"),
    (2, 1, 3, "Misafir geldiğinde ne yaparız?", ["Karşılar, hoş geldiniz deriz", "Odamıza gideriz", "Görmezden geliriz", "Bağırırız"], 0, "Misafirperverlik"),
    (2, 2, 3, "Evde kitap okumak için nasıl bir ortam gerekir?", ["Sessiz ve aydınlık", "Gürültülü", "Karanlık", "Kalabalık"], 0, "Sessizlik ve ışık"),
    (2, 1, 3, "Yatağımızı ne zaman toplarız?", ["Sabah kalkınca", "Akşam", "Hiç", "Haftada bir"], 0, "Sabah düzeni"),
    # Band 3
    (3, 2, 3, "Kardeşimizle aynı oyuncağı istiyorsak ne yaparız?", ["Sırayla oynarız", "Kavga ederiz", "Saklarız", "Kırarız"], 0, "Sıra ve paylaşım"),
    (3, 2, 3, "Ailemizin kuralları neden vardır?", ["Huzurlu yaşamak için", "Bizi kısıtlamak için", "Zaman geçirmek için", "Gereksizdir"], 0, "Kurallar huzur sağlar"),
    (3, 2, 3, "Evde tasarruf nasıl yapılır?", ["Gereksiz kullanımı azaltarak", "Hiç kullanmayarak", "Çok kullanarak", "Umursamayarak"], 0, "Bilinçli kullanım"),
    (3, 2, 3, "Dişimizi fırçalarken musluğu ne yaparız?", ["Kapatırız", "Açık bırakırız", "Az açarız", "Fark etmez"], 0, "Su israfını önlemek"),
    (3, 2, 3, "Aile bireylerinden biri üzgünse ne yaparız?", ["Dinler, destek oluruz", "Karışmayız", "Alay ederiz", "Uzaklaşırız"], 0, "Ailede destek"),
    (3, 2, 3, "Evdeki eşyaları neden dikkatli kullanırız?", ["Uzun süre dayansın diye", "Gereksiz", "Zorunlu olduğu için", "Sıkıcı olduğu için"], 0, "Özenli kullanım"),
    (3, 2, 3, "Evde elektrikli aletleri kim kullanmalı?", ["Büyükler", "Çocuklar", "Herkes", "Kimse"], 0, "Güvenlik"),
    (3, 2, 3, "Aile içinde sır tutmak her zaman doğru mudur?", ["Hayır, bizi üzen şeyler söylenmeli", "Evet, hep", "Fark etmez", "Sadece bazen"], 0, "Bizi rahatsız eden şeyler paylaşılmalı"),
    (3, 3, 3, "Ailemizin geçmişini kimden öğreniriz?", ["Büyüklerimizden", "Kitaplardan", "Televizyondan", "İnternetten"], 0, "Aile büyükleri"),
    # Band 4
    (4, 2, 3, "Biriktirdiğimiz harçlıkla ne yapabiliriz?", ["İstediğimiz bir şeyi alabiliriz", "Hiçbir şey", "Kaybederiz", "Harcayamayız"], 0, "Biriktirmek hedefe ulaştırır"),
    (4, 3, 3, "Ailemizde ihtiyaç ile istek arasındaki fark nedir?", ["İhtiyaç zorunlu, istek zorunlu değil", "Aynı şeydir", "İstek daha önemli", "Fark yoktur"], 0, "İhtiyaç ≠ istek"),
    (4, 3, 3, "Evde enerji tasarrufu neden önemlidir?", ["Doğayı ve bütçeyi korur", "Sadece para kazandırır", "Gereksizdir", "Zordur"], 0, "Çevre + ekonomi"),
    (4, 3, 3, "Aile bütçesi hazırlanırken ne dikkate alınır?", ["Gelir ve giderler", "Sadece istekler", "Komşuların harcaması", "Reklamlar"], 0, "Gelir-gider dengesi"),
    (4, 3, 3, "Akrabalarımızla iletişimi neden sürdürürüz?", ["Bağlarımız güçlensin diye", "Zorunlu olduğu için", "Hediye almak için", "Gereksizdir"], 0, "Aile bağı"),
    (4, 3, 3, "Evde birlikte karar almak neyi sağlar?", ["Herkesin fikrinin değer görmesini", "Zaman kaybını", "Karışıklığı", "Tartışmayı"], 0, "Katılım"),
    # Band 5
    (5, 3, 3, "Aile içi iletişimde en önemli şey nedir?", ["Dinlemek ve anlamak", "Konuşmak", "Haklı çıkmak", "Susmak"], 0, "Dinlemek iletişimin temelidir"),
    (5, 3, 3, "Tasarruf sadece para biriktirmek midir?", ["Hayır, kaynakları bilinçli kullanmaktır", "Evet", "Sadece su için", "Sadece elektrik için"], 0, "Tasarruf = bilinçli kullanım"),
    (5, 3, 3, "Ailede paylaşılan sorumluluk neyi gösterir?", ["Dayanışmayı", "Zayıflığı", "Tembelliği", "Kuralsızlığı"], 0, "Dayanışma"),
]

# ==================================================== 3. SAGLIKLI HAYAT

SAGLIGIMIZ_EK = [
    # Band 1
    (1, 1, 3, "Meyveleri yemeden önce ne yaparız?", ["Yıkarız", "Keseriz", "Soyarız", "Bekletiriz"], 0, "Meyve yıkanır"),
    (1, 1, 3, "Tırnaklarımızı ne yapmalıyız?", ["Kesmeliyiz", "Uzatmalıyız", "Yemeliyiz", "Boyamalıyız"], 0, "Kısa ve temiz tırnak"),
    (1, 1, 3, "Hangisi sağlıklı içecektir?", ["Su", "Gazoz", "Kola", "Enerji içeceği"], 0, "Su en sağlıklı içecektir"),
    (1, 1, 3, "Kahvaltıda hangisi sağlıklıdır?", ["Peynir ve yumurta", "Çikolata", "Cips", "Şeker"], 0, "Protein ve besin değeri"),
    (1, 1, 3, "Saçımızı ne ile tararız?", ["Tarak", "Çatal", "Kaşık", "Kalem"], 0, "Tarak"),
    (1, 1, 3, "Hangisi spor değildir?", ["Televizyon izlemek", "Koşmak", "Yüzmek", "Bisiklet sürmek"], 0, "TV izlemek hareketsizliktir"),
    (1, 1, 3, "Tuvaletten sonra ne yaparız?", ["Ellerimizi yıkarız", "Koşarız", "Yemek yeriz", "Oynarız"], 0, "El hijyeni"),
    (1, 1, 3, "Hangisi vücudumuza zarar verir?", ["Sigara dumanı", "Temiz hava", "Su", "Meyve"], 0, "Sigara dumanı zararlıdır"),
    # Band 2
    (2, 1, 3, "Neden sebze yemeliyiz?", ["Vitamin verir", "Tatlı olduğu için", "Renkli olduğu için", "Ucuz olduğu için"], 0, "Sebzeler vitamin kaynağıdır"),
    (2, 1, 3, "Süt bize ne kazandırır?", ["Güçlü kemikler", "Uzun saç", "Hızlı koşu", "İyi görme"], 0, "Kalsiyum → kemik"),
    (2, 1, 3, "Yatmadan önce ne yapmalıyız?", ["Dişlerimizi fırçalamalıyız", "Şeker yemeliyiz", "Koşmalıyız", "TV izlemeliyiz"], 0, "Gece diş fırçalama"),
    (2, 1, 3, "Hangisi bulaşıcı hastalıktır?", ["Grip", "Kırık kol", "Diş çürüğü", "Baş ağrısı"], 0, "Grip bulaşıcıdır"),
    (2, 2, 3, "Havuç hangi organımıza faydalıdır?", ["Gözlerimize", "Kulaklarımıza", "Ayaklarımıza", "Saçımıza"], 0, "A vitamini → göz sağlığı"),
    (2, 1, 3, "Spor yapmadan önce ne yaparız?", ["Isınma hareketleri", "Yemek yeriz", "Uyuruz", "Hiçbir şey"], 0, "Isınma sakatlanmayı önler"),
    (2, 1, 3, "Yemek yerken ne yapmamalıyız?", ["Konuşmamalıyız", "Yavaş yemeliyiz", "İyi çiğnemeliyiz", "Oturmalıyız"], 0, "Ağız doluyken konuşmak tehlikelidir"),
    (2, 2, 3, "Hangisi kişisel eşyadır?", ["Havlu", "Masa", "Sandalye", "Kapı"], 0, "Havlu paylaşılmaz"),
    (2, 2, 3, "Güneşte uzun süre kalırsak ne olur?", ["Cildimiz yanar", "Güçleniriz", "Uzarız", "Bir şey olmaz"], 0, "Güneş yanığı"),
    (2, 2, 3, "Hangi besin grubu et ve yumurtayla aynı gruptadır?", ["Balık", "Elma", "Ekmek", "Süt"], 0, "Protein grubu"),
    # Band 3
    (3, 2, 3, "Neden çeşitli besinler yemeliyiz?", ["Her besin farklı fayda sağlar", "Sıkılmamak için", "Ucuz olduğu için", "Zorunlu olduğu için"], 0, "Dengeli beslenme"),
    (3, 2, 3, "Hasta arkadaşımızla aynı bardaktan su içersek ne olur?", ["Hastalık bulaşabilir", "Bir şey olmaz", "Güçleniriz", "İyileşiriz"], 0, "Bulaşma riski"),
    (3, 2, 3, "Hapşırırken ne yapmalıyız?", ["Mendille ağzımızı kapatmalıyız", "Elimizle kapatmalıyız", "Kapatmamalıyız", "Bağırmalıyız"], 0, "Mendil veya dirsek içi"),
    (3, 2, 3, "Uyku neden önemlidir?", ["Vücudumuz dinlenir ve büyür", "Zaman geçsin diye", "Sıkıldığımız için", "Gereksizdir"], 0, "Uyku büyüme hormonu salgılatır"),
    (3, 2, 3, "Fazla şeker yemek neye yol açar?", ["Diş çürüğü ve kilo artışı", "Uzun boy", "Güçlü kas", "İyi görme"], 0, "Şekerin zararları"),
    (3, 2, 3, "Hangisi hareketsiz yaşamın sonucudur?", ["Kilo artışı", "Güçlü kas", "Sağlıklı kalp", "İyi uyku"], 0, "Hareketsizlik kilo aldırır"),
    (3, 2, 3, "Yemekten hemen sonra spor yapmalı mıyız?", ["Hayır, beklemeliyiz", "Evet", "Fark etmez", "Her zaman"], 0, "Sindirim için beklenmeli"),
    (3, 2, 3, "Ambalajlı gıdalarda neye bakmalıyız?", ["Son kullanma tarihine", "Rengine", "Fiyatına", "Reklamına"], 0, "Son kullanma tarihi"),
    (3, 3, 3, "Bağışıklık sistemimiz ne işe yarar?", ["Hastalıklara karşı korur", "Yemek sindirir", "Kan pompalar", "Nefes aldırır"], 0, "Savunma sistemi"),
    (3, 2, 3, "Hangi durumda doktora gitmeliyiz?", ["Ateşimiz çıktığında", "Mutlu olduğumuzda", "Uykumuz geldiğinde", "Acıktığımızda"], 0, "Ateş hastalık belirtisidir"),
    # Band 4
    (4, 2, 3, "Aşı olmak neden gereklidir?", ["Vücudumuz hastalığa karşı hazırlanır", "Hasta olmak için", "Zorunlu olduğu için", "Gereksizdir"], 0, "Aşı bağışıklık kazandırır"),
    (4, 3, 3, "Ekran karşısında ne kadar ara vermeliyiz?", ["Her 20 dakikada bir", "Hiç", "Saatte bir", "Günde bir"], 0, "Düzenli ara göz sağlığını korur"),
    (4, 3, 3, "Kemiklerimizin gelişimi için hangi besin gereklidir?", ["Süt ve süt ürünleri", "Cips", "Gazoz", "Şekerleme"], 0, "Kalsiyum"),
    (4, 3, 3, "Hangi davranış hastalıkların yayılmasını en çok önler?", ["Düzenli el yıkamak", "Çok su içmek", "Çok uyumak", "Çok yemek"], 0, "El hijyeni en etkili korunmadır"),
    (4, 3, 3, "İlaç kullanırken neye dikkat edilir?", ["Doktorun söylediği doz ve süre", "Tadına", "Rengine", "Fiyatına"], 0, "Doktor talimatı"),
    (4, 3, 3, "Kişisel hijyen neyi kapsar?", ["Beden, diş, saç ve el temizliği", "Sadece el yıkamayı", "Sadece banyoyu", "Sadece diş fırçalamayı"], 0, "Bütünsel temizlik"),
    # Band 5
    (5, 3, 3, "Dengeli beslenme ne demektir?", ["Tüm besin gruplarından yeterli miktarda almak", "Az yemek", "Çok yemek", "Sadece sebze yemek"], 0, "Yeterli + çeşitli"),
    (5, 3, 3, "Bağımlılık yapan maddeler neden tehlikelidir?", ["Vücuda kalıcı zarar verir ve bırakması zordur", "Pahalıdır", "Kötü kokar", "Tadı kötüdür"], 0, "Kalıcı zarar + bağımlılık"),
    (5, 3, 3, "İlk yardımda ilk adım nedir?", ["112'yi aramak ve ortamı güvene almak", "Hastayı taşımak", "Su vermek", "İlaç vermek"], 0, "Önce yardım çağır, ortamı güvene al"),
]

# ==================================================== 4. GUVENLI HAYAT

GUVENLIGIMIZ_EK = [
    # Band 1
    (1, 1, 3, "Yolda yürürken kimin elini tutarız?", ["Büyüğümüzün", "Kimsenin", "Yabancının", "Hayvanın"], 0, "Büyüğün eli"),
    (1, 1, 3, "Kibritle oynamak nasıldır?", ["Tehlikeli", "Eğlenceli", "Faydalı", "Normal"], 0, "Yangın riski"),
    (1, 1, 3, "Sıcak tencereye ne yaparız?", ["Dokunmayız", "Dokunuruz", "İteriz", "Açarız"], 0, "Yanık tehlikesi"),
    (1, 1, 3, "Yaya geçidinde önce ne yaparız?", ["Sağa sola bakarız", "Koşarız", "Telefona bakarız", "Bekleriz"], 0, "Önce bak, sonra geç"),
    (1, 1, 3, "Kaldırım kimin içindir?", ["Yayaların", "Arabaların", "Bisikletlerin", "Kamyonların"], 0, "Yayalar için"),
    (1, 1, 3, "Bıçak kimin kullanması gereken bir alettir?", ["Büyüklerin", "Çocukların", "Herkesin", "Kimsenin"], 0, "Kesici alet"),
    (1, 1, 3, "Merdivende koşarsak ne olabilir?", ["Düşebiliriz", "Hızlanırız", "Güçleniriz", "Bir şey olmaz"], 0, "Düşme riski"),
    (1, 1, 3, "Trafik ışığında sarı ne demektir?", ["Hazır ol, dikkat et", "Geç", "Dur", "Koş"], 0, "Sarı = dikkat"),
    # Band 2
    (2, 1, 3, "Otobüs beklerken nerede dururuz?", ["Durakta, geride", "Yolda", "Yolun ortasında", "Otobüsün önünde"], 0, "Durakta geride beklenir"),
    (2, 1, 3, "Bisiklet sürerken nerede sürmeliyiz?", ["Bisiklet yolunda", "Ana yolda", "Kaldırımda hızlı", "Otoyolda"], 0, "Bisiklet yolu"),
    (2, 1, 3, "Yabancı biri adresimizi sorarsa ne yaparız?", ["Söylemeyiz, büyüğümüze haber veririz", "Söyleriz", "Götürürüz", "Telefonu veririz"], 0, "Kişisel bilgi paylaşılmaz"),
    (2, 1, 3, "Elektrikli aleti ıslak elle tutabilir miyiz?", ["Hayır, çok tehlikeli", "Evet", "Bazen", "Fark etmez"], 0, "Su elektrik iletir"),
    (2, 2, 3, "Deprem çantasında ne bulunmalı?", ["Su, yiyecek, el feneri, düdük", "Oyuncak", "Kitap", "Televizyon"], 0, "Temel ihtiyaç malzemeleri"),
    (2, 1, 3, "Arabadan hangi taraftan inmeliyiz?", ["Kaldırım tarafından", "Yol tarafından", "Fark etmez", "Ön kapıdan"], 0, "Kaldırım tarafı güvenli"),
    (2, 2, 3, "Bu işaret ne anlama gelir? 🚷", ["Yaya giremez", "Yaya geçidi", "Okul geçidi", "Park yeri"], 0, "Yayaya kapalı yol"),
    (2, 2, 3, "Yangın çıkarsa hangi numarayı ararız?", ["112", "155", "156", "153"], 0, "Tüm acil durumlar 112"),
    (2, 1, 3, "Balkondan sarkmak nasıldır?", ["Çok tehlikeli", "Eğlenceli", "Normal", "Faydalı"], 0, "Düşme riski"),
    (2, 2, 3, "Yolda oyun oynanır mı?", ["Hayır, parkta oynanır", "Evet", "Bazen", "Araba yoksa"], 0, "Yol oyun alanı değildir"),
    # Band 3
    (3, 2, 3, "Deprem sırasında ne yaparız?", ["Çök-Kapan-Tutun", "Koşarak çıkarız", "Asansöre bineriz", "Pencereden atlarız"], 0, "Çök, kapan, tutun"),
    (3, 2, 3, "Deprem sırasında nerede durmamalıyız?", ["Pencere ve dolap yanında", "Masa altında", "Sağlam duvar dibinde", "Kolon yanında"], 0, "Devrilecek eşyalardan uzak"),
    (3, 2, 3, "Yangında neden eğilerek çıkarız?", ["Duman yukarıda toplanır", "Daha hızlı olur", "Daha kolay olur", "Görmek için"], 0, "Duman yükselir"),
    (3, 2, 3, "İnternette tanımadığımız biri arkadaş olmak isterse?", ["Kabul etmeyiz, büyüğümüze söyleriz", "Kabul ederiz", "Fotoğraf göndeririz", "Adres veririz"], 0, "İnternet güvenliği"),
    (3, 2, 3, "Arabada emniyet kemeri neden takılır?", ["Kaza anında bizi korur", "Zorunlu olduğu için", "Rahat olduğu için", "Süs olsun diye"], 0, "Hayat kurtarır"),
    (3, 2, 3, "Yolda telefonla oynamak neden tehlikelidir?", ["Dikkatimiz dağılır", "Telefon bozulur", "Şarj biter", "Yorulur"], 0, "Dikkat dağınıklığı"),
    (3, 2, 3, "Trafik polisinin işareti ile ışık farklıysa hangisine uyarız?", ["Trafik polisine", "Işığa", "İkisine de", "Hiçbirine"], 0, "Polis işareti önceliklidir"),
    (3, 2, 3, "Yangın söndürücü nerede bulunur?", ["Görünür ve ulaşılır yerde", "Dolapta", "Bodrumda", "Kilitli odada"], 0, "Kolay ulaşılabilir yerde"),
    (3, 3, 3, "İnternette şifremizi kiminle paylaşırız?", ["Hiç kimseyle", "Arkadaşımızla", "Herkesle", "Öğretmenle"], 0, "Şifre kişiseldir"),
    (3, 2, 3, "Doğal gaz kokusu alırsak ne yaparız?", ["Pencereyi açar, büyüğe haber veririz", "Işığı açarız", "Kibrit yakarız", "Bekleriz"], 0, "Kıvılcım oluşturmadan havalandır"),
    # Band 4
    (4, 2, 3, "Depremden sonra ilk ne yaparız?", ["Güvenli alana çıkarız", "Eşya toplarız", "Fotoğraf çekeriz", "Bekleriz"], 0, "Önce güvenli alan"),
    (4, 3, 3, "Yangında asansör neden kullanılmaz?", ["Elektrik kesilirse içinde kalırız", "Yavaş olduğu için", "Kalabalık olduğu için", "Pahalı olduğu için"], 0, "Elektrik kesintisi riski"),
    (4, 3, 3, "Siber zorbalık ne demektir?", ["İnternette birini rahatsız etmek", "Bilgisayar oyunu", "Hızlı yazmak", "Şifre kırmak"], 0, "İnternette rahatsız etme"),
    (4, 3, 3, "Acil durumda 112'ye ne söylemeliyiz?", ["Adres ve ne olduğunu", "Sadece adımızı", "Hiçbir şey", "Telefon numaramızı"], 0, "Adres + durum"),
    (4, 3, 3, "Toplanma alanı ne işe yarar?", ["Afet sonrası buluşma noktasıdır", "Park yeridir", "Oyun alanıdır", "Pazar yeridir"], 0, "Afet toplanma alanı"),
    (4, 3, 3, "Deprem öncesi evde ne yapılmalı?", ["Ağır eşyalar duvara sabitlenmeli", "Eşyalar yükseğe konmalı", "Hiçbir şey", "Pencereler açılmalı"], 0, "Sabitleme"),
    # Band 5
    (5, 3, 3, "Kişisel güvenliğimiz için en önemli kural nedir?", ["Rahatsız olduğumuzda hayır demek ve büyüğe söylemek", "Sessiz kalmak", "Kabul etmek", "Kaçmak"], 0, "Hayır deme hakkı + bildirim"),
    (5, 3, 3, "Afet bilinci ne demektir?", ["Önceden hazırlıklı olmak", "Korkmak", "Kaçmak", "Beklemek"], 0, "Hazırlık = bilinç"),
    (5, 3, 3, "Trafik kuralları neden vardır?", ["Herkesin güvenli ulaşımı için", "Ceza kesmek için", "Yavaşlatmak için", "Zorlaştırmak için"], 0, "Ortak güvenlik"),
]

# ==================================================== 5. ULKEMIZDE HAYAT

ULKEMIZ_EK = [
    # Band 1
    (1, 1, 3, "Bayrağımızda kaç yıldız vardır?", ["1", "2", "3", "5"], 0, "Bir ay, bir yıldız"),
    (1, 1, 3, "Atatürk'ün soyadını kim vermiştir?", ["Türkiye Büyük Millet Meclisi", "Annesi", "Babası", "Öğretmeni"], 0, "TBMM 1934'te verdi"),
    (1, 1, 3, "İstiklal Marşı okunurken ne yaparız?", ["Hazır ol duruşunda dururuz", "Otururuz", "Konuşuruz", "Yürürüz"], 0, "Saygı duruşu"),
    (1, 1, 3, "Bayramlarda ne yaparız?", ["Büyüklerimizi ziyaret ederiz", "Uyuruz", "Okula gideriz", "Çalışırız"], 0, "Bayram ziyareti"),
    (1, 1, 3, "Atatürk'ün en sevdiği hayvan hangisidir?", ["Köpek", "Kedi", "Kuş", "Balık"], 0, "Foks adlı köpeği vardı"),
    (1, 1, 3, "Ülkemizin bayrağı hangi renklerdedir?", ["Kırmızı ve beyaz", "Mavi ve beyaz", "Yeşil ve beyaz", "Sarı ve kırmızı"], 0, "Kırmızı zemin, beyaz ay yıldız"),
    (1, 1, 3, "Okulumuzda hangi gün bayrak töreni yapılır?", ["Pazartesi ve Cuma", "Her gün", "Salı", "Perşembe"], 0, "Hafta başı ve sonu"),
    (1, 1, 3, "Atatürk ne zaman doğmuştur?", ["1881", "1923", "1938", "1919"], 0, "1881 Selanik"),
    # Band 2
    (2, 1, 3, "Atatürk hangi şehirde vefat etmiştir?", ["İstanbul", "Ankara", "İzmir", "Selanik"], 0, "10 Kasım 1938, Dolmabahçe"),
    (2, 1, 3, "10 Kasım'da ne yaparız?", ["Atatürk'ü saygıyla anarız", "Kutlama yaparız", "Tatil yaparız", "Oyun oynarız"], 0, "Anma günü"),
    (2, 1, 3, "TBMM nerededir?", ["Ankara", "İstanbul", "İzmir", "Bursa"], 0, "Başkent Ankara"),
    (2, 2, 3, "Atatürk'ün kız kardeşinin adı nedir?", ["Makbule", "Zübeyde", "Fatma", "Ayşe"], 0, "Makbule Atadan"),
    (2, 1, 3, "Milli bayramlarımızda evlere ne asılır?", ["Bayrak", "Balon", "Çiçek", "Işık"], 0, "Türk bayrağı"),
    (2, 2, 3, "İstiklal Marşı kaç kıtadır?", ["10", "5", "7", "12"], 0, "10 kıtadır, ilk ikisi okunur"),
    (2, 1, 3, "Atatürk hangi mesleği yapmıştır?", ["Askerlik", "Doktorluk", "Öğretmenlik", "Mühendislik"], 0, "Asker ve devlet adamı"),
    (2, 2, 3, "Cumhuriyet ne demektir?", ["Halkın kendini yönetmesi", "Padişahın yönetmesi", "Askerin yönetmesi", "Tek kişinin yönetmesi"], 0, "Halk egemenliği"),
    (2, 2, 3, "Atatürk'ün 'Hayatta en hakiki mürşit ilimdir' sözü neyi anlatır?", ["Bilimin önemini", "Savaşın önemini", "Paranın önemini", "Gücün önemini"], 0, "Bilim rehberdir"),
    (2, 2, 3, "23 Nisan'da meclis nerede açılmıştır?", ["Ankara", "İstanbul", "Sivas", "Erzurum"], 0, "23 Nisan 1920, Ankara"),
    # Band 3
    (3, 2, 3, "Kurtuluş Savaşı hangi olayla başlamıştır?", ["Atatürk'ün Samsun'a çıkışı", "Cumhuriyetin ilanı", "Meclisin açılışı", "Sakarya Savaşı"], 0, "19 Mayıs 1919 Samsun"),
    (3, 2, 3, "Atatürk 19 Mayıs'ı kime armağan etmiştir?", ["Gençlere", "Çocuklara", "Askerlere", "Öğretmenlere"], 0, "Gençlik ve Spor Bayramı"),
    (3, 2, 3, "30 Ağustos hangi savaşın zaferidir?", ["Büyük Taarruz", "Çanakkale", "Sakarya", "İnönü"], 0, "Başkomutanlık Meydan Muharebesi"),
    (3, 2, 3, "Anıtkabir hangi şehirdedir?", ["Ankara", "İstanbul", "İzmir", "Selanik"], 0, "Ankara"),
    (3, 2, 3, "Harf inkılabı ne zaman yapılmıştır?", ["1928", "1923", "1920", "1938"], 0, "1928 Yeni Türk harfleri"),
    (3, 2, 3, "Atatürk kadınlara hangi hakkı vermiştir?", ["Seçme ve seçilme", "Okuma", "Çalışma", "Gezme"], 0, "1934 seçme ve seçilme hakkı"),
    (3, 3, 3, "Milli değerlerimiz nelerdir?", ["Bayrak, dil, tarih, kültür", "Sadece bayrak", "Sadece dil", "Sadece tarih"], 0, "Milli değerler bütünü"),
    (3, 2, 3, "İstiklal Marşı ne zaman kabul edilmiştir?", ["12 Mart 1921", "29 Ekim 1923", "23 Nisan 1920", "19 Mayıs 1919"], 0, "12 Mart 1921"),
    (3, 3, 3, "Türkiye Cumhuriyeti'nin ilk cumhurbaşkanı kimdir?", ["Mustafa Kemal Atatürk", "İsmet İnönü", "Celal Bayar", "Fevzi Çakmak"], 0, "Atatürk"),
    (3, 2, 3, "Atatürk'ün eğitim aldığı okul hangisidir?", ["Harp Okulu", "Tıp Fakültesi", "Hukuk Fakültesi", "Öğretmen Okulu"], 0, "Askeri okullar"),
    # Band 4
    (4, 2, 3, "'Yurtta sulh, cihanda sulh' sözü neyi anlatır?", ["Barış ilkesini", "Savaş ilkesini", "Ticaret ilkesini", "Eğitim ilkesini"], 0, "Barışçı dış politika"),
    (4, 3, 3, "Cumhuriyetin ilanı neyi değiştirmiştir?", ["Yönetim şeklini", "Bayrağı", "Dili", "Başkenti"], 0, "Saltanattan cumhuriyete"),
    (4, 3, 3, "Atatürk neden eğitime çok önem vermiştir?", ["Çağdaş bir toplum için", "Zorunlu olduğu için", "Kolay olduğu için", "Ucuz olduğu için"], 0, "Eğitim çağdaşlaşmanın temeli"),
    (4, 3, 3, "Milli mücadelede halkın rolü ne olmuştur?", ["Topyekûn destek vermiştir", "İzlemiştir", "Karışmamıştır", "Karşı çıkmıştır"], 0, "Halkın topyekûn katılımı"),
    (4, 3, 3, "Kültürel mirasımızı neden korumalıyız?", ["Geçmişimizi geleceğe taşımak için", "Turist gelsin diye", "Para kazanmak için", "Gereksizdir"], 0, "Kültürel süreklilik"),
    (4, 3, 3, "'Egemenlik kayıtsız şartsız milletindir' ne demektir?", ["Yönetme hakkı halkındır", "Yönetme hakkı padişahındır", "Yönetme hakkı askerindir", "Yönetme hakkı yoktur"], 0, "Milli egemenlik"),
    # Band 5
    (5, 3, 3, "Atatürk ilkelerinden 'laiklik' ne anlama gelir?", ["Din ve devlet işlerinin ayrılması", "Dinsizlik", "Din özgürlüğü olmaması", "Tek din olması"], 0, "Din ve devlet işlerinin ayrılığı"),
    (5, 3, 3, "Milli birlik ve beraberlik neden önemlidir?", ["Güçlü bir ülke için", "Zorunlu olduğu için", "Kolay olduğu için", "Gereksizdir"], 0, "Birlik güç getirir"),
    (5, 3, 3, "Cumhuriyetin bize kazandırdığı en önemli şey nedir?", ["Söz ve karar hakkı", "Bayrak", "Marş", "Tatil"], 0, "Halkın yönetime katılımı"),
]

# ==================================================== 6. DOGADA HAYAT

DOGA_CEVRE_EK = [
    # Band 1
    (1, 1, 3, "Canlılar ne yapar?", ["Büyür ve çoğalır", "Hiç değişmez", "Sadece durur", "Kırılır"], 0, "Canlılar büyür, beslenir, çoğalır"),
    (1, 1, 3, "Kuşun yavrusuna ne denir?", ["Yavru kuş", "Kuzu", "Tay", "Buzağı"], 0, "Kuş yavrusu"),
    (1, 1, 3, "Kedinin yavrusuna ne denir?", ["Yavru kedi", "Kuzu", "Civciv", "Tay"], 0, "Yavru kedi"),
    (1, 1, 3, "Hangi mevsimde okullar açılır?", ["Sonbahar", "Yaz", "Kış", "İlkbahar"], 0, "Eylül = sonbahar"),
    (1, 1, 3, "Arı bize ne verir?", ["Bal", "Süt", "Yumurta", "Yün"], 0, "Bal"),
    (1, 1, 3, "Koyundan ne elde ederiz?", ["Yün", "Bal", "Yumurta", "Deri"], 0, "Yün"),
    (1, 1, 3, "Tavuktan ne elde ederiz?", ["Yumurta", "Süt", "Bal", "Yün"], 0, "Yumurta"),
    (1, 1, 3, "İnekten ne elde ederiz?", ["Süt", "Bal", "Yumurta", "Yün"], 0, "Süt"),
    # Band 2
    (2, 1, 3, "Hangisi kışın uyur?", ["Ayı", "Kedi", "Köpek", "Kuş"], 0, "Kış uykusu"),
    (2, 1, 3, "Kuşlar kışın ne yapar?", ["Sıcak yerlere göç eder", "Uyur", "Ölür", "Saklanır"], 0, "Göç"),
    (2, 1, 3, "Bitkinin toprak altındaki kısmı hangisidir?", ["Kök", "Yaprak", "Çiçek", "Meyve"], 0, "Kök"),
    (2, 1, 3, "Hangisi çiçek açar?", ["Gül", "Taş", "Kum", "Su"], 0, "Gül bir bitkidir"),
    (2, 2, 3, "Hangisi sürüngendir?", ["Yılan", "Kedi", "Kuş", "Balık"], 0, "Yılan sürüngendir"),
    (2, 2, 3, "Kurbağa nerede yaşar?", ["Hem suda hem karada", "Sadece suda", "Sadece karada", "Havada"], 0, "İki yaşamlı"),
    (2, 1, 3, "Yağmur hangi mevsimde daha çok yağar?", ["İlkbahar", "Yaz", "Kış", "Sonbahar"], 0, "İlkbahar yağışlıdır"),
    (2, 1, 3, "Pil hangi kutuya atılır?", ["Özel pil kutusuna", "Mavi", "Sarı", "Yeşil"], 0, "Piller özel toplanır"),
    (2, 2, 3, "Hangisi ağaçtan elde edilir?", ["Kağıt", "Cam", "Plastik", "Metal"], 0, "Kağıt selülozdan"),
    (2, 1, 3, "Balık ne ile nefes alır?", ["Solungaç", "Akciğer", "Deri", "Burun"], 0, "Solungaç"),
    # Band 3
    (3, 2, 3, "Memeli hayvanların ortak özelliği nedir?", ["Yavrularını sütle besler", "Yumurtlar", "Suda yaşar", "Uçar"], 0, "Memeliler yavrusunu emzirir"),
    (3, 2, 3, "Bitkiler nasıl beslenir?", ["Güneş ışığıyla besin üretir", "Toprak yer", "Su içer", "Avlanır"], 0, "Fotosentez"),
    (3, 2, 3, "Orman yangınlarının en büyük nedeni nedir?", ["İnsanların dikkatsizliği", "Yağmur", "Kar", "Rüzgar"], 0, "Yangınların çoğu insan kaynaklıdır"),
    (3, 2, 3, "Geri dönüşüm neyi sağlar?", ["Kaynakların yeniden kullanımını", "Çöpün artmasını", "Enerji harcamayı", "Kirliliği"], 0, "Kaynak tasarrufu"),
    (3, 2, 3, "Suyun buharlaşıp bulut olması neye denir?", ["Su döngüsü", "Yağmur", "Rüzgar", "Kar"], 0, "Su döngüsü"),
    (3, 2, 3, "Hangisi otçul hayvandır?", ["İnek", "Aslan", "Kartal", "Köpekbalığı"], 0, "İnek ot yer"),
    (3, 2, 3, "Hangisi etçil hayvandır?", ["Aslan", "İnek", "Koyun", "Tavşan"], 0, "Aslan et yer"),
    (3, 2, 3, "Kelebek hangi evrelerden geçer?", ["Yumurta, tırtıl, koza, kelebek", "Sadece yumurta", "Sadece tırtıl", "Doğrudan kelebek"], 0, "Başkalaşım"),
    (3, 3, 3, "Toprak kirliliğine ne yol açar?", ["Çöp ve kimyasal atıklar", "Yağmur", "Güneş", "Rüzgar"], 0, "Atıklar toprağı kirletir"),
    (3, 2, 3, "Ağaç dikmek neden önemlidir?", ["Oksijen üretir, erozyonu önler", "Gölge yapar sadece", "Güzel görünür", "Gereksizdir"], 0, "Çok yönlü fayda"),
    # Band 4
    (4, 2, 3, "Besin zincirinin başında kim vardır?", ["Bitkiler", "Etçiller", "Otçullar", "İnsanlar"], 0, "Bitkiler üreticidir"),
    (4, 3, 3, "Rüzgar enerjisi nasıl elde edilir?", ["Rüzgar türbinleriyle", "Kömür yakarak", "Su kaynatarak", "Ateş yakarak"], 0, "Türbinler rüzgarı elektriğe çevirir"),
    (4, 3, 3, "Küresel ısınmanın nedeni nedir?", ["Sera gazları", "Yağmur", "Kar", "Rüzgar"], 0, "Sera gazı salınımı"),
    (4, 3, 3, "Nesli tükenen hayvanlar neden korunmalı?", ["Doğal denge bozulmasın diye", "Güzel oldukları için", "Nadir oldukları için", "Pahalı oldukları için"], 0, "Ekolojik denge"),
    (4, 3, 3, "Erozyon nedir?", ["Toprağın su ve rüzgarla taşınması", "Toprağın kirlenmesi", "Toprağın ısınması", "Toprağın donması"], 0, "Toprak aşınması"),
    (4, 3, 3, "Bitkiler havaya ne verir?", ["Oksijen", "Karbondioksit", "Duman", "Toz"], 0, "Fotosentez oksijen üretir"),
    # Band 5
    (5, 3, 3, "Ekosistem ne demektir?", ["Canlıların ve cansız çevrenin birlikte oluşturduğu sistem", "Sadece hayvanlar", "Sadece bitkiler", "Sadece toprak"], 0, "Canlı + cansız birlikte"),
    (5, 3, 3, "Biyoçeşitlilik neden önemlidir?", ["Doğal dengeyi korur", "Güzel görünür", "Gereksizdir", "Sadece bilim için"], 0, "Çeşitlilik = denge"),
    (5, 3, 3, "Sürdürülebilir yaşam ne demektir?", ["Kaynakları gelecek nesillere bırakacak şekilde kullanmak", "Hiç kullanmamak", "Çok kullanmak", "Sadece geri dönüşüm"], 0, "Gelecek nesilleri düşünmek"),
]
