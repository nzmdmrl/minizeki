"""
Turkce prosedurel uretecler icin kelime havuzu.
Hece bolmeleri elle dogrulanmistir (algoritma Turkce'de %100 guvenilir degil).
"""

# (kelime, hece_listesi, sinif)
KELIMELER = [
    # 1. sinif - 1-2 hece
    ("at", ["at"], 1), ("el", ["el"], 1), ("ok", ["ok"], 1),
    ("su", ["su"], 1), ("ev", ["ev"], 1), ("göz", ["göz"], 1),
    ("kuş", ["kuş"], 1), ("top", ["top"], 1), ("kalem", ["ka", "lem"], 1),
    ("kitap", ["ki", "tap"], 1), ("masa", ["ma", "sa"], 1),
    ("araba", ["a", "ra", "ba"], 1), ("elma", ["el", "ma"], 1),
    ("armut", ["ar", "mut"], 1), ("balık", ["ba", "lık"], 1),
    ("çiçek", ["çi", "çek"], 1), ("bebek", ["be", "bek"], 1),
    ("anne", ["an", "ne"], 1), ("baba", ["ba", "ba"], 1),
    ("kedi", ["ke", "di"], 1), ("köpek", ["kö", "pek"], 1),
    ("okul", ["o", "kul"], 1), ("defter", ["def", "ter"], 1),
    ("silgi", ["sil", "gi"], 1), ("kapı", ["ka", "pı"], 1),
    ("pencere", ["pen", "ce", "re"], 1), ("bardak", ["bar", "dak"], 1),
    ("tabak", ["ta", "bak"], 1), ("çanta", ["çan", "ta"], 1),
    ("ayakkabı", ["a", "yak", "ka", "bı"], 1),
    ("gözlük", ["göz", "lük"], 1), ("saat", ["sa", "at"], 1),
    ("ağaç", ["a", "ğaç"], 1), ("yaprak", ["yap", "rak"], 1),
    ("güneş", ["gü", "neş"], 1), ("bulut", ["bu", "lut"], 1),
    ("yıldız", ["yıl", "dız"], 1), ("deniz", ["de", "niz"], 1),

    # 2. sinif - 2-3 hece
    ("bahçe", ["bah", "çe"], 2), ("bisiklet", ["bi", "sik", "let"], 2),
    ("öğretmen", ["öğ", "ret", "men"], 2), ("öğrenci", ["öğ", "ren", "ci"], 2),
    ("kardeş", ["kar", "deş"], 2), ("arkadaş", ["ar", "ka", "daş"], 2),
    ("oyuncak", ["o", "yun", "cak"], 2), ("bilgisayar", ["bil", "gi", "sa", "yar"], 2),
    ("telefon", ["te", "le", "fon"], 2), ("televizyon", ["te", "le", "viz", "yon"], 2),
    ("mutfak", ["mut", "fak"], 2), ("banyo", ["ban", "yo"], 2),
    ("yatak", ["ya", "tak"], 2), ("koltuk", ["kol", "tuk"], 2),
    ("dolap", ["do", "lap"], 2), ("halı", ["ha", "lı"], 2),
    ("perde", ["per", "de"], 2), ("lamba", ["lam", "ba"], 2),
    ("kaşık", ["ka", "şık"], 2), ("çatal", ["ça", "tal"], 2),
    ("peynir", ["pey", "nir"], 2), ("zeytin", ["zey", "tin"], 2),
    ("domates", ["do", "ma", "tes"], 2), ("salatalık", ["sa", "la", "ta", "lık"], 2),
    ("patates", ["pa", "ta", "tes"], 2), ("havuç", ["ha", "vuç"], 2),
    ("karpuz", ["kar", "puz"], 2), ("kavun", ["ka", "vun"], 2),
    ("üzüm", ["ü", "züm"], 2), ("portakal", ["por", "ta", "kal"], 2),
    ("mandalina", ["man", "da", "li", "na"], 2), ("muz", ["muz"], 2),
    ("çilek", ["çi", "lek"], 2), ("kiraz", ["ki", "raz"], 2),
    ("tavşan", ["tav", "şan"], 2), ("kaplumbağa", ["kap", "lum", "ba", "ğa"], 2),
    ("kelebek", ["ke", "le", "bek"], 2), ("karınca", ["ka", "rın", "ca"], 2),
    ("arı", ["a", "rı"], 2), ("örümcek", ["ö", "rüm", "cek"], 2),
    ("aslan", ["as", "lan"], 2), ("kaplan", ["kap", "lan"], 2),
    ("zürafa", ["zü", "ra", "fa"], 2), ("maymun", ["may", "mun"], 2),
    ("penguen", ["pen", "gu", "en"], 2), ("timsah", ["tim", "sah"], 2),
    ("orman", ["or", "man"], 2), ("dağ", ["dağ"], 2),
    ("nehir", ["ne", "hir"], 2), ("köprü", ["köp", "rü"], 2),
    ("sokak", ["so", "kak"], 2), ("cadde", ["cad", "de"], 2),
    ("market", ["mar", "ket"], 2), ("hastane", ["has", "ta", "ne"], 2),
    ("eczane", ["ec", "za", "ne"], 2), ("kütüphane", ["kü", "tüp", "ha", "ne"], 2),
    ("müze", ["mü", "ze"], 2), ("sinema", ["si", "ne", "ma"], 2),
    ("bayrak", ["bay", "rak"], 2), ("vatan", ["va", "tan"], 2),
    ("millet", ["mil", "let"], 2), ("kahraman", ["kah", "ra", "man"], 2),
]


def kelimeler_for_grade(grade: int) -> list:
    """O sinif ve alt siniflarin kelimeleri."""
    return [k for k in KELIMELER if k[2] <= grade]


# Alfabetik siralama icin Turkce alfabe
TURKCE_ALFABE = "aAbBcCçÇdDeEfFgGğĞhHıIiİjJkKlLmMnNoOöÖpPrRsSşŞtTuUüÜvVyYzZ"
_SIRA = {ch: i for i, ch in enumerate("abcçdefgğhıijklmnoöprsştuüvyz")}


def turkce_sort_key(kelime: str):
    return [_SIRA.get(c, 99) for c in kelime.lower()]


# Sesli harfler
SESLI = set("aeıioöuü")
KALIN_SESLI = set("aıou")
INCE_SESLI = set("eiöü")
