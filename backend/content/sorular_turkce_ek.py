"""
Turkce EK soru bankasi (Parti 2).
sorular_turkce.py'yi tamamlar.

Band hedef dogruluk: 1=%90  2=%75  3=%60  4=%40  5=%20
Format: (band, sinif_min, sinif_max, soru, [siklar], dogru_index, aciklama)
"""

# ==================================================== ES ANLAMLI

ES_ANLAMLI_EK = [
    # Band 1
    (1, 2, 4, '"Yol" kelimesinin eş anlamlısı hangisidir?', ["Cadde", "Ev", "Bahçe", "Park"], 0, "Yol = Cadde"),
    (1, 2, 4, '"Kalp" kelimesinin eş anlamlısı hangisidir?', ["Yürek", "Ciğer", "Beyin", "Mide"], 0, "Kalp = Yürek"),
    (1, 2, 4, '"Uçak" kelimesinin eş anlamlısı hangisidir?', ["Tayyare", "Tren", "Gemi", "Otobüs"], 0, "Uçak = Tayyare"),
    (1, 2, 4, '"Kelime" yerine hangisini kullanabiliriz?', ["Sözcük", "Cümle", "Harf", "Nokta"], 0, "Kelime = Sözcük"),
    (1, 2, 4, '"Öğrenci" kelimesinin eş anlamlısı hangisidir?', ["Talebe", "Öğretmen", "Müdür", "Veli"], 0, "Öğrenci = Talebe"),
    (1, 2, 4, '"Soru" kelimesinin eş anlamlısı hangisidir?', ["Sual", "Cevap", "Yanıt", "Konu"], 0, "Soru = Sual"),
    (1, 2, 4, '"Armağan" kelimesinin eş anlamlısı hangisidir?', ["Hediye", "Kutu", "Paket", "Süs"], 0, "Armağan = Hediye"),
    (1, 2, 4, '"Yardım" kelimesinin eş anlamlısı hangisidir?', ["Destek", "Engel", "Zorluk", "Sorun"], 0, "Yardım = Destek"),
    # Band 2
    (2, 2, 4, '"Anı" kelimesinin eş anlamlısı hangisidir?', ["Hatıra", "Hayal", "Rüya", "Düşünce"], 0, "Anı = Hatıra"),
    (2, 2, 4, '"Şarkı" kelimesinin eş anlamlısı hangisidir?', ["Türkü", "Şiir", "Hikâye", "Masal"], 0, "Şarkı = Türkü"),
    (2, 2, 4, '"Kural" kelimesinin eş anlamlısı hangisidir?', ["Nizam", "Oyun", "Ceza", "Ödül"], 0, "Kural = Nizam"),
    (2, 2, 4, '"Sonuç" kelimesinin eş anlamlısı hangisidir?', ["Netice", "Başlangıç", "Neden", "Sebep"], 0, "Sonuç = Netice"),
    (2, 2, 4, '"Görev" kelimesinin eş anlamlısı hangisidir?', ["Vazife", "Hak", "İzin", "Tatil"], 0, "Görev = Vazife"),
    (2, 2, 4, '"Zor" kelimesinin eş anlamlısı hangisidir?', ["Güç", "Kolay", "Basit", "Hafif"], 0, "Zor = Güç"),
    (2, 2, 4, '"Anlam" kelimesinin eş anlamlısı hangisidir?', ["Mana", "Ses", "Harf", "Yazı"], 0, "Anlam = Mana"),
    (2, 2, 4, '"Yetenek" kelimesinin eş anlamlısı hangisidir?', ["Kabiliyet", "Tembellik", "Bilgisizlik", "Zayıflık"], 0, "Yetenek = Kabiliyet"),
    (2, 2, 4, '"Nazik" kelimesinin eş anlamlısı hangisidir?', ["Kibar", "Kaba", "Sert", "Kırıcı"], 0, "Nazik = Kibar"),
    (2, 2, 4, '"Temiz" kelimesinin eş anlamlısı hangisidir?', ["Pak", "Kirli", "Tozlu", "Çamurlu"], 0, "Temiz = Pak"),
    # Band 3
    (3, 2, 4, '"Endişe" kelimesinin eş anlamlısı hangisidir?', ["Kaygı", "Neşe", "Sevinç", "Huzur"], 0, "Endişe = Kaygı"),
    (3, 2, 4, '"Gayret" kelimesinin eş anlamlısı hangisidir?', ["Çaba", "Tembellik", "Uyku", "Dinlenme"], 0, "Gayret = Çaba"),
    (3, 2, 4, '"Ihtiyaç" kelimesinin eş anlamlısı hangisidir?', ["Gereksinim", "İstek", "Hayal", "Arzu"], 0, "İhtiyaç = Gereksinim"),
    (3, 2, 4, '"Sıkıntı" kelimesinin eş anlamlısı hangisidir?', ["Zorluk", "Kolaylık", "Rahatlık", "Huzur"], 0, "Sıkıntı = Zorluk"),
    (3, 3, 4, '"Tecrübe" kelimesinin eş anlamlısı hangisidir?', ["Deneyim", "Bilgi", "Eğitim", "Okul"], 0, "Tecrübe = Deneyim"),
    (3, 3, 4, '"Merhamet" kelimesinin eş anlamlısı hangisidir?', ["Acıma", "Öfke", "Nefret", "Kızgınlık"], 0, "Merhamet = Acıma"),
    (3, 3, 4, '"Fikir" kelimesinin eş anlamlısı hangisidir?', ["Düşünce", "Söz", "Yazı", "Ses"], 0, "Fikir = Düşünce"),
    (3, 3, 4, '"Sükûnet" kelimesinin eş anlamlısı hangisidir?', ["Sessizlik", "Gürültü", "Kalabalık", "Karmaşa"], 0, "Sükûnet = Sessizlik"),
    (3, 2, 4, '"Misafirperver" kelimesinin eş anlamlısı hangisidir?', ["Konuksever", "Cimri", "Bencil", "Kaba"], 0, "Misafirperver = Konuksever"),
    (3, 3, 4, '"Kudret" kelimesinin eş anlamlısı hangisidir?', ["Güç", "Zayıflık", "Yorgunluk", "Hastalık"], 0, "Kudret = Güç"),
    # Band 4
    (4, 3, 4, '"Muhtaç" kelimesinin eş anlamlısı hangisidir?', ["Gereksinimli", "Zengin", "Varlıklı", "Bolluk"], 0, "Muhtaç = Gereksinimli"),
    (4, 3, 4, '"İstikbal" kelimesinin eş anlamlısı hangisidir?', ["Gelecek", "Geçmiş", "Şimdi", "Dün"], 0, "İstikbal = Gelecek"),
    (4, 3, 4, '"Cevval" kelimesinin eş anlamlısı hangisidir?', ["Çevik", "Yavaş", "Tembel", "Ağır"], 0, "Cevval = Çevik"),
    (4, 3, 4, '"Sadakat" kelimesinin eş anlamlısı hangisidir?', ["Bağlılık", "İhanet", "Yalan", "Aldatma"], 0, "Sadakat = Bağlılık"),
    (4, 3, 4, '"Nasihat" kelimesinin eş anlamlısı hangisidir?', ["Öğüt", "Emir", "Ceza", "Şaka"], 0, "Nasihat = Öğüt"),
    (4, 3, 4, '"İnat" kelimesinin eş anlamlısı hangisidir?', ["Direnme", "Uyum", "Kabul", "Teslim"], 0, "İnat = Direnme"),
    # Band 5
    (5, 3, 4, '"Tefekkür" kelimesinin eş anlamlısı hangisidir?', ["Derin düşünme", "Uyuma", "Konuşma", "Yazma"], 0, "Tefekkür = Derin düşünme"),
    (5, 3, 4, '"Vefa" kelimesinin eş anlamlısı hangisidir?', ["Bağlılık ve iyiliği unutmama", "Unutkanlık", "Nankörlük", "İlgisizlik"], 0, "Vefa = İyiliği unutmama"),
    (5, 3, 4, '"Zarafet" kelimesinin eş anlamlısı hangisidir?', ["İncelik", "Kabalık", "Sertlik", "Hoyratlık"], 0, "Zarafet = İncelik"),
]

# ==================================================== ZIT ANLAMLI

ZIT_ANLAMLI_EK = [
    # Band 1
    (1, 2, 4, '"Sağ" kelimesinin zıt anlamlısı hangisidir?', ["Sol", "Ön", "Arka", "Üst"], 0, "Sağ ↔ Sol"),
    (1, 2, 4, '"Ön" kelimesinin zıt anlamlısı hangisidir?', ["Arka", "Sağ", "Sol", "Yan"], 0, "Ön ↔ Arka"),
    (1, 2, 4, '"İçeri" kelimesinin zıt anlamlısı hangisidir?', ["Dışarı", "Yukarı", "Aşağı", "Yan"], 0, "İçeri ↔ Dışarı"),
    (1, 2, 4, '"Var" kelimesinin zıt anlamlısı hangisidir?', ["Yok", "Çok", "Az", "Bol"], 0, "Var ↔ Yok"),
    (1, 2, 4, '"Girmek" kelimesinin zıt anlamlısı hangisidir?', ["Çıkmak", "Durmak", "Beklemek", "Oturmak"], 0, "Girmek ↔ Çıkmak"),
    (1, 2, 4, '"Almak" kelimesinin zıt anlamlısı hangisidir?', ["Vermek", "Tutmak", "Bırakmak", "Koymak"], 0, "Almak ↔ Vermek"),
    (1, 2, 4, '"Gelmek" kelimesinin zıt anlamlısı hangisidir?', ["Gitmek", "Durmak", "Oturmak", "Koşmak"], 0, "Gelmek ↔ Gitmek"),
    (1, 2, 4, '"Islak" kelimesinin zıt anlamlısı hangisidir?', ["Kuru", "Soğuk", "Sıcak", "Yumuşak"], 0, "Islak ↔ Kuru"),
    # Band 2
    (2, 2, 4, '"Başlangıç" kelimesinin zıt anlamlısı hangisidir?', ["Son", "Orta", "İlk", "Yeni"], 0, "Başlangıç ↔ Son"),
    (2, 2, 4, '"Genç" kelimesinin zıt anlamlısı hangisidir?', ["Yaşlı", "Çocuk", "Bebek", "Küçük"], 0, "Genç ↔ Yaşlı"),
    (2, 2, 4, '"Açmak" kelimesinin zıt anlamlısı hangisidir?', ["Kapatmak", "Çekmek", "İtmek", "Tutmak"], 0, "Açmak ↔ Kapatmak"),
    (2, 2, 4, '"Gülmek" kelimesinin zıt anlamlısı hangisidir?', ["Ağlamak", "Konuşmak", "Bağırmak", "Susmak"], 0, "Gülmek ↔ Ağlamak"),
    (2, 2, 4, '"Sevmek" kelimesinin zıt anlamlısı hangisidir?', ["Nefret etmek", "Bilmek", "Görmek", "Duymak"], 0, "Sevmek ↔ Nefret etmek"),
    (2, 2, 4, '"Erken" kelimesinin zıt anlamlısı hangisidir?', ["Geç", "Hızlı", "Yavaş", "Çabuk"], 0, "Erken ↔ Geç"),
    (2, 2, 4, '"Kazanmak" kelimesinin zıt anlamlısı hangisidir?', ["Kaybetmek", "Oynamak", "Yarışmak", "Koşmak"], 0, "Kazanmak ↔ Kaybetmek"),
    (2, 2, 4, '"Geniş" kelimesinin zıt anlamlısı hangisidir?', ["Dar", "Uzun", "Kısa", "Büyük"], 0, "Geniş ↔ Dar"),
    (2, 2, 4, '"Yumuşak" kelimesinin zıt anlamlısı hangisidir?', ["Sert", "İnce", "Hafif", "Küçük"], 0, "Yumuşak ↔ Sert"),
    (2, 2, 4, '"Derin" kelimesinin zıt anlamlısı hangisidir?', ["Sığ", "Geniş", "Uzun", "Yüksek"], 0, "Derin ↔ Sığ"),
    # Band 3
    (3, 2, 4, '"Bilerek" kelimesinin zıt anlamlısı hangisidir?', ["Kazara", "İsteyerek", "Planlayarak", "Düşünerek"], 0, "Bilerek ↔ Kazara"),
    (3, 2, 4, '"Cesaret" kelimesinin zıt anlamlısı hangisidir?', ["Korku", "Güç", "Kuvvet", "Cesurluk"], 0, "Cesaret ↔ Korku"),
    (3, 2, 4, '"Barış" kelimesinin zıt anlamlısı hangisidir?', ["Savaş", "Dostluk", "Sevgi", "Huzur"], 0, "Barış ↔ Savaş"),
    (3, 2, 4, '"Gerçek" kelimesinin zıt anlamlısı hangisidir?', ["Yalan", "Doğru", "Kesin", "Açık"], 0, "Gerçek ↔ Yalan"),
    (3, 3, 4, '"Bolluk" kelimesinin zıt anlamlısı hangisidir?', ["Kıtlık", "Zenginlik", "Çokluk", "Fazlalık"], 0, "Bolluk ↔ Kıtlık"),
    (3, 3, 4, '"Basit" kelimesinin zıt anlamlısı hangisidir?', ["Karmaşık", "Kolay", "Sade", "Açık"], 0, "Basit ↔ Karmaşık"),
    (3, 2, 4, '"Hatırlamak" kelimesinin zıt anlamlısı hangisidir?', ["Unutmak", "Bilmek", "Öğrenmek", "Anlamak"], 0, "Hatırlamak ↔ Unutmak"),
    (3, 3, 4, '"Aydınlık" kelimesinin zıt anlamlısı hangisidir?', ["Karanlık", "Parlak", "Beyaz", "Açık"], 0, "Aydınlık ↔ Karanlık"),
    (3, 3, 4, '"Misafir" kelimesinin zıt anlamlısı hangisidir?', ["Ev sahibi", "Komşu", "Arkadaş", "Akraba"], 0, "Misafir ↔ Ev sahibi"),
    # Band 4
    (4, 3, 4, '"Cesur" kelimesinin zıt anlamlısı hangisidir?', ["Ürkek", "Yiğit", "Güçlü", "Kahraman"], 0, "Cesur ↔ Ürkek"),
    (4, 3, 4, '"Umut" kelimesinin zıt anlamlısı hangisidir?', ["Umutsuzluk", "Sevinç", "Mutluluk", "Neşe"], 0, "Umut ↔ Umutsuzluk"),
    (4, 3, 4, '"Alçakgönüllü" kelimesinin zıt anlamlısı hangisidir?', ["Kibirli", "Nazik", "Sessiz", "Utangaç"], 0, "Alçakgönüllü ↔ Kibirli"),
    (4, 3, 4, '"Adalet" kelimesinin zıt anlamlısı hangisidir?', ["Haksızlık", "Doğruluk", "Dürüstlük", "İyilik"], 0, "Adalet ↔ Haksızlık"),
    (4, 3, 4, '"Cimrilik" kelimesinin zıt anlamlısı hangisidir?', ["Cömertlik", "Zenginlik", "Fakirlik", "Tutumluluk"], 0, "Cimrilik ↔ Cömertlik"),
    (4, 3, 4, '"Düzenli" kelimesinin zıt anlamlısı hangisidir?', ["Dağınık", "Temiz", "Titiz", "Planlı"], 0, "Düzenli ↔ Dağınık"),
    # Band 5
    (5, 3, 4, '"Fedakâr" kelimesinin zıt anlamlısı hangisidir?', ["Bencil", "Cömert", "İyi", "Yardımsever"], 0, "Fedakâr ↔ Bencil"),
    (5, 3, 4, '"Mütevazı" kelimesinin zıt anlamlısı hangisidir?', ["Kibirli", "Nazik", "Sessiz", "Utangaç"], 0, "Mütevazı ↔ Kibirli"),
    (5, 3, 4, '"Somut" kelimesinin zıt anlamlısı hangisidir?', ["Soyut", "Gerçek", "Açık", "Net"], 0, "Somut ↔ Soyut"),
]

# ==================================================== DOGRU YAZILIS

DOGRU_YAZILIS_EK = [
    # Band 1
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["defter", "deftar", "defder", "deffter"], 0, "defter"),
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["masa", "massa", "mase", "masaa"], 0, "masa"),
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["pencere", "pencare", "penncere", "pençere"], 0, "pencere"),
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["bahçe", "bahce", "bahçce", "baçhe"], 0, "bahçe"),
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["köpek", "köpak", "kopek", "köppek"], 0, "köpek"),
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["silgi", "silki", "sillgi", "silgii"], 0, "silgi"),
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["tavşan", "tavsan", "tavşşan", "tafşan"], 0, "tavşan"),
    (1, 1, 4, "Hangisi doğru yazılmıştır?", ["kelebek", "kelabek", "kellebek", "kelebbek"], 0, "kelebek"),
    # Band 2
    (2, 1, 4, "Hangisi doğru yazılmıştır?", ["arkadaş", "arkadas", "arkkadaş", "arkadaç"], 0, "arkadaş"),
    (2, 1, 4, "Hangisi doğru yazılmıştır?", ["bisiklet", "bisiklat", "bisklet", "bisikklet"], 0, "bisiklet"),
    (2, 2, 4, "Hangisi doğru yazılmıştır?", ["kütüphane", "kütüpane", "kütüphhane", "kütphane"], 0, "kütüphane"),
    (2, 2, 4, "Hangisi doğru yazılmıştır?", ["eczane", "ezcane", "eczzane", "ecane"], 0, "eczane"),
    (2, 1, 4, "Hangisi doğru yazılmıştır?", ["öğrenci", "ögrenci", "öğrencı", "örenci"], 0, "öğrenci"),
    (2, 2, 4, "Hangisi doğru yazılmıştır?", ["televizyon", "televizyön", "telavizyon", "televizon"], 0, "televizyon"),
    (2, 2, 4, "Hangisi doğru yazılmıştır?", ["bilgisayar", "bilgisayer", "biligisayar", "bilgsayar"], 0, "bilgisayar"),
    (2, 2, 4, "Hangisi doğru yazılmıştır?", ["kaplumbağa", "kaplumbaga", "kaplumba", "kaplumbaağa"], 0, "kaplumbağa"),
    (2, 2, 4, "Hangisi doğru yazılmıştır?", ["portakal", "protakal", "portokal", "portakkal"], 0, "portakal"),
    (2, 2, 4, "Hangisi doğru yazılmıştır?", ["mandalina", "mandelina", "mandalena", "mandallina"], 0, "mandalina"),
    # Band 3
    (3, 2, 4, "Hangisi doğru yazılmıştır?", ["hiçbiri", "hiç biri", "hicbiri", "hiçbirisi"], 0, "hiçbiri (bitişik)"),
    (3, 2, 4, "Hangisi doğru yazılmıştır?", ["her şey", "herşey", "her sey", "herşeyy"], 0, "her şey (ayrı)"),
    (3, 2, 4, "Hangisi doğru yazılmıştır?", ["birkaç", "bir kaç", "birkac", "birkkaç"], 0, "birkaç (bitişik)"),
    (3, 2, 4, "Hangisi doğru yazılmıştır?", ["pek çok", "pekçok", "pekcok", "pek-çok"], 0, "pek çok (ayrı yazılır)"),
    (3, 2, 4, "Hangisi doğru yazılmıştır?", ["herhangi", "her hangi", "herhangı", "herhanki"], 0, "herhangi (bitişik)"),
    (3, 2, 4, "Hangisi doğru yazılmıştır?", ["ilk önce", "ilkönce", "ilk-önce", "ilkonce"], 0, "ilk önce (ayrı)"),
    (3, 2, 4, "Hangisi doğru yazılmıştır?", ["hoş geldiniz", "hoşgeldiniz", "hoşgeldinniz", "hos geldiniz"], 0, "hoş geldiniz (ayrı)"),
    (3, 2, 4, "Hangisi doğru yazılmıştır?", ["teşekkür", "teşekür", "tesekkür", "teşşekkür"], 0, "teşekkür"),
    (3, 3, 4, "Hangisi doğru yazılmıştır?", ["yalnızca", "yanlızca", "yalnuzca", "yalnızcaa"], 0, "yalnızca"),
    (3, 2, 4, "Hangisi doğru yazılmıştır?", ["inşallah", "inşaallah", "inşalah", "inşşallah"], 0, "inşallah"),
    # Band 4
    (4, 3, 4, "Hangisi doğru yazılmıştır?", ["mühendis", "mühendiz", "muhendis", "mühhendis"], 0, "mühendis"),
    (4, 3, 4, "Hangisi doğru yazılmıştır?", ["asansör", "asansor", "ansansör", "assansör"], 0, "asansör"),
    (4, 3, 4, "Hangisi doğru yazılmıştır?", ["kilometre", "kilometere", "kilomerte", "kilometire"], 0, "kilometre"),
    (4, 3, 4, "Hangisi doğru yazılmıştır?", ["restoran", "restorant", "restauran", "restoranı"], 0, "restoran"),
    (4, 3, 4, "Hangisi doğru yazılmıştır?", ["antrenman", "antreman", "antrenmann", "antirenman"], 0, "antrenman"),
    (4, 3, 4, "Hangisi doğru yazılmıştır?", ["kağıt", "kaat", "kaağıt", "kağıtt"], 0, "kâğıt / kağıt"),
    # Band 5
    (5, 3, 4, '"Şimdiye kadar" anlamındaki kelime hangisidir?', ["hâlâ", "hala", "haala", "halâ"], 0, "hâlâ = şimdiye kadar / hala = babanın kız kardeşi"),
    (5, 3, 4, "Hangisi doğru yazılmıştır?", ["mütevazı", "mütevazi", "mütevaazı", "müteevazı"], 0, "mütevazı"),
    (5, 3, 4, "Hangisi doğru yazılmıştır?", ["poğaça", "poaça", "pogaça", "poğaca"], 0, "poğaça"),
]

# ==================================================== NOKTALAMA

NOKTALAMA_EK = [
    # Band 1
    (1, 2, 4, "Cümlenin sonuna hangi işaret gelmeli?\n\nBabam işe gitti __", [".", "?", "!", ","], 0, "Bildiren cümle → nokta"),
    (1, 2, 4, "Cümlenin sonuna hangi işaret gelmeli?\n\nNe zaman geleceksin __", ["?", ".", "!", ";"], 0, "Soru cümlesi"),
    (1, 2, 4, "Cümlenin sonuna hangi işaret gelmeli?\n\nDikkat, araba geliyor __", ["!", ".", "?", ","], 0, "Uyarı → ünlem"),
    (1, 2, 4, "Cümlenin sonuna hangi işaret gelmeli?\n\nKitabımı okudum __", [".", "?", "!", ":"], 0, "Bildiren cümle"),
    (1, 2, 4, "Hangisi soru işaretidir?", ["?", ".", "!", ","], 0, "Soru işareti: ?"),
    (1, 2, 4, "Hangisi ünlem işaretidir?", ["!", "?", ".", ";"], 0, "Ünlem işareti: !"),
    # Band 2
    (2, 2, 4, "Cümlenin sonuna hangi işaret gelmeli?\n\nHangi renk daha güzel __", ["?", ".", "!", ","], 0, "Soru cümlesi"),
    (2, 2, 4, "Cümlenin sonuna hangi işaret gelmeli?\n\nAman, düşeceksin __", ["!", ".", "?", ":"], 0, "Uyarı → ünlem"),
    (2, 2, 4, "Hangi cümlede noktalama doğrudur?", ["Okula gidiyorum.", "Okula gidiyorum?", "Okula gidiyorum!", "Okula gidiyorum,"], 0, "Bildiren cümle"),
    (2, 2, 4, "Hangisi doğru yazılmıştır?", ["Adın ne?", "Adın ne.", "Adın ne!", "Adın ne,"], 0, "Soru cümlesi"),
    (2, 2, 4, "Boşluğa hangi işaret gelmeli?\n\nKırmızı __ mavi ve sarı boyalarım var.", [",", ".", "?", ":"], 0, "Sıralamada virgül"),
    (2, 2, 4, "Cümlenin sonuna hangi işaret gelmeli?\n\nBu ne kadar güzel bir hediye __", ["!", ".", "?", ","], 0, "Hayranlık → ünlem"),
    (2, 2, 4, "Nokta hangi cümlede kullanılır?", ["Bildiren cümlede", "Soru cümlesinde", "Ünlem cümlesinde", "Hiçbirinde"], 0, "Bildiren cümle noktayla biter"),
    # Band 3
    (3, 2, 4, "Boşluğa hangi işaret gelmeli?\n\nAyşe __ lütfen kapıyı kapat.", [",", ".", "!", ":"], 0, "Hitaptan sonra virgül"),
    (3, 2, 4, "Hangi cümlede virgül doğru kullanılmıştır?", ["Elma, armut ve kiraz aldım.", "Elma armut, ve kiraz aldım.", "Elma, armut, ve kiraz aldım.", "Elma armut ve, kiraz aldım."], 0, "'ve'den önce virgül konmaz"),
    (3, 2, 4, "Boşluğa hangi işaret gelmeli?\n\nMarketten şunları al __ ekmek, süt, yumurta.", [":", ",", ".", "?"], 0, "Açıklama öncesi iki nokta"),
    (3, 3, 4, "Hangisinde kesme işareti doğru kullanılmıştır?", ["İstanbul'da yaşıyorum.", "İstanbulda yaşıyorum.", "İstanbul da yaşıyorum.", "İstanbul'da' yaşıyorum."], 0, "Özel isme gelen ek"),
    (3, 3, 4, "Kısaltmadan sonra hangi işaret kullanılır?\n\nDr __ Mehmet Bey", [".", ",", ":", "!"], 0, "Kısaltmadan sonra nokta"),
    (3, 2, 4, "Hangisi ünlem cümlesidir?", ["Ne kadar sıcak!", "Hava sıcak.", "Hava sıcak mı?", "Hava sıcaklaşıyor."], 0, "Hayranlık/şaşkınlık"),
    (3, 3, 4, "Tarih yazarken hangi işaret kullanılır?\n\n29 __ 10 __ 1923", [".", ",", ":", "-"], 0, "29.10.1923"),
    (3, 2, 4, "Hangi cümlede noktalama hatası vardır?", ["Kaç yaşındasın.", "Kaç yaşındasın?", "Beş yaşındayım.", "Ne güzel!"], 0, "Soru cümlesi noktayla bitmez"),
    # Band 4
    (4, 3, 4, "Hangi cümlede tırnak doğru kullanılmıştır?", ['Annem "Yemek hazır" dedi.', 'Annem Yemek hazır dedi.', 'Annem, Yemek hazır dedi.', 'Annem "Yemek hazır dedi.'], 0, "Başkasının sözü tırnak içinde"),
    (4, 3, 4, "Boşluğa hangi işaret gelmeli?\n\nÖğretmen __ \"Kitapları açın\" dedi.", [":", ",", ".", "?"], 0, "Konuşmadan önce iki nokta"),
    (4, 3, 4, "Hangisinde kesme işareti gereklidir?", ["Ali'nin kalemi", "Alinin kalemi", "Ali nin kalemi", "Ali-nin kalemi"], 0, "Özel isim + ek"),
    (4, 3, 4, "Konuşma çizgisi hangisidir?", ["—", ".", ",", "?"], 0, "Konuşma çizgisi: —"),
    (4, 3, 4, "Hangi cümlede iki nokta doğru kullanılmıştır?", ["Şunları aldım: kalem, defter.", "Şunları aldım, kalem: defter.", "Şunları: aldım kalem, defter.", "Şunları aldım. kalem: defter"], 0, "Açıklama öncesi iki nokta"),
    (4, 3, 4, "Sayılara gelen ek nasıl yazılır?\n\n5 __ inci sınıf", ["'", ".", ",", "-"], 0, "5'inci"),
    # Band 5
    (5, 3, 4, "Noktalı virgül (;) ne zaman kullanılır?", ["Virgülle ayrılmış grupları ayırırken", "Cümle sonunda", "Soru sorarken", "Ünlem bildirirken"], 0, "Grupları ayırır"),
    (5, 3, 4, "Üç nokta (...) ne anlatır?", ["Sözün tamamlanmadığını", "Soruyu", "Ünlemi", "Bitişi"], 0, "Söz tamamlanmamış"),
    (5, 3, 4, "Parantez ne için kullanılır?", ["Ek açıklama için", "Soru için", "Ünlem için", "Sıralama için"], 0, "Ek bilgi/açıklama"),
]
