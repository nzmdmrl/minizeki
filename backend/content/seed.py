"""
Veritabanini kategoriler, rozetler, esyalar ve soru bankasiyla doldurur.

Kullanim:
    python content/seed.py            # ekle/guncelle (idempotent)
    python content/seed.py --reset    # sorulari sil, yeniden yukle
"""
import sys
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models import (  # noqa: E402
    init_db, SessionLocal, Category, Badge, HouseItem, Question,
)
from content.seed_data import CATEGORIES, BADGES, HOUSE_ITEMS  # noqa: E402
from content import sorular_turkce as st  # noqa: E402
from content import sorular_turkce_ek as ste  # noqa: E402
from content import sorular_hayat as sh  # noqa: E402
from content import sorular_hayat_ek as she  # noqa: E402
from content import sorular_diger as sd  # noqa: E402
from content import sorular_diger_ek as sde  # noqa: E402
from content import sorular_fen as sf  # noqa: E402
from content import sorular_fen4 as sf4  # noqa: E402
from content import sorular_sosyal as ss  # noqa: E402
from content import sorular_hayat_ek2 as she2  # noqa: E402
from content import sorular_turkce_ek2 as ste2  # noqa: E402
from content.metinler_12 import METINLER_1, METINLER_2  # noqa: E402
from content.metinler_34 import METINLER_3, METINLER_4  # noqa: E402
from content.metinler_ek import (  # noqa: E402
    METINLER_1_EK, METINLER_2_EK, METINLER_3_EK, METINLER_4_EK,
)


# kategori_id -> soru listesi
SORU_BANKASI = {
    # Turkce
    "es_anlamli":    st.ES_ANLAMLI + ste.ES_ANLAMLI_EK + ste2.ES_ANLAMLI_EK2,
    "zit_anlamli":   st.ZIT_ANLAMLI + ste.ZIT_ANLAMLI_EK + ste2.ZIT_ANLAMLI_EK2,
    "dogru_yazilis": st.DOGRU_YAZILIS + ste.DOGRU_YAZILIS_EK + ste2.DOGRU_YAZILIS_EK2,
    "noktalama":     st.NOKTALAMA + ste.NOKTALAMA_EK + ste2.NOKTALAMA_EK2,
    # Hayat Bilgisi
    "okulumuz":      sh.OKULUMUZ + she.OKULUMUZ_EK + she2.OKULUMUZ_EK2,
    "ailemiz":       sh.AILEMIZ + she.AILEMIZ_EK + she2.AILEMIZ_EK2,
    "sagligimiz":    sh.SAGLIGIMIZ + she.SAGLIGIMIZ_EK + she2.SAGLIGIMIZ_EK2,
    "guvenligimiz":  sh.GUVENLIGIMIZ + she.GUVENLIGIMIZ_EK + she2.GUVENLIGIMIZ_EK2,
    "ulkemiz":       sh.ULKEMIZ + she.ULKEMIZ_EK + she2.ULKEMIZ_EK2,
    "doga_cevre":    sh.DOGA_CEVRE + she.DOGA_CEVRE_EK + she2.DOGA_CEVRE_EK2,
    # Diger
    "geometri":      sd.GEOMETRI + sde.GEOMETRI_EK + ste2.GEOMETRI_EK2,
    "ing_kelime":    sd.ING_KELIME + sde.ING_KELIME_EK + ste2.ING_KELIME_EK2,
    "ing_ifade":     sd.ING_IFADE + sde.ING_IFADE_EK + ste2.ING_IFADE_EK2,
    # --- 3-4. sinif: Fen Bilimleri ---
    "dunya_gokyuzu":  sf.DUNYA_GOKYUZU,
    "duyu_organlari": sf.DUYU_ORGANLARI,
    "kuvvet_hareket": sf.KUVVET_HAREKET,
    "madde":          sf.MADDE,
    "canlilar":       sf.CANLILAR,
    # --- 4. sinif: Fen ek uniteleri ---
    "isik_ses":       sf4.ISIK_SES,
    "elektrik":       sf4.ELEKTRIK,
    "beslenme":       sf4.BESLENME,
    # --- 4. sinif: Sosyal Bilgiler ---
    "kimlik_haklar":  ss.KIMLIK_HAKLAR,
    "tarihimiz":      ss.TARIHIMIZ,
    "cografya":       ss.COGRAFYA,
    "buluslar":       ss.BULUSLAR,
    "ekonomi":        ss.EKONOMI,
    "vatandaslik":    ss.VATANDASLIK,
    "dunya_ulkeleri": ss.DUNYA_ULKELERI,
}


def seed_categories(db) -> int:
    n = 0
    for (cid, name, subject, icon, gmin, gmax, proc, gen, upper, free, order) in CATEGORIES:
        c = db.get(Category, cid)
        if c is None:
            c = Category(id=cid)
            db.add(c)
            n += 1
        c.name = name
        c.subject = subject
        c.icon = icon
        c.grade_min = gmin
        c.grade_max = gmax
        c.is_procedural = proc
        c.generator_key = gen
        c.has_upper_grade = upper
        c.is_free = free
        c.in_daily_quest = (cid != "okuma")   # okuma gunluk goreve girmez
        c.sort_order = order
    db.commit()
    return n


def seed_badges(db) -> int:
    n = 0
    for (bid, name, icon, desc) in BADGES:
        b = db.get(Badge, bid)
        if b is None:
            b = Badge(id=bid)
            db.add(b)
            n += 1
        b.name = name
        b.icon = icon
        b.description = desc
    db.commit()
    return n


def seed_house(db) -> int:
    n = 0
    for (iid, name, cat, price, icon, order) in HOUSE_ITEMS:
        i = db.get(HouseItem, iid)
        if i is None:
            i = HouseItem(id=iid)
            db.add(i)
            n += 1
        i.name = name
        i.category = cat
        i.price = price
        i.icon = icon
        i.sort_order = order
    db.commit()
    return n


def _metni_duzenle(ham: str) -> str:
    """
    Kaynak koddaki satir kirilmalarini temizler.

    Metinler .py dosyasinda okunabilirlik icin satirlara bolunmustur.
    Ama bu satir sonlari EKRANDA da kirilma yaratiyordu; cumleler
    ortadan bolunmus gorunuyordu.

    Kural:
      TEK satir sonu   = ayni paragrafin devami -> bosluga cevrilir
      BOS SATIR (\n\n) = paragraf ayrimi       -> korunur
    """
    paragraflar = []
    for p in ham.strip().split("\n\n"):
        satirlar = [x.strip() for x in p.strip().split("\n") if x.strip()]
        if satirlar:
            paragraflar.append(" ".join(satirlar))
    return "\n\n".join(paragraflar)


def seed_stories(db) -> tuple[int, int]:
    """
    Okuma metinlerini ve anlama sorularini yukler. Idempotent.

    SIK KARISTIRMA: Kaynak dosyada dogru cevap her zaman ilk siktadir
    (yazarken okunakli olsun diye). Karistirilmazsa cocuk hep A'ya
    basarak %100 alir. Bu yuzden her sik listesi karistirilir.
    """
    from models import Story, StoryQuestion

    eklenen = guncellenen = 0
    sira = 0
    for liste in (METINLER_1, METINLER_1_EK,
                  METINLER_2, METINLER_2_EK,
                  METINLER_3, METINLER_3_EK,
                  METINLER_4, METINLER_4_EK):
        for (sid, baslik, metin, gmin, gmax, seviye, sorular) in liste:
            sira += 1
            temiz = _metni_duzenle(metin)
            kelime = len(temiz.split())

            st = db.get(Story, sid)
            if st is None:
                st = Story(id=sid)
                db.add(st)
                eklenen += 1
            else:
                guncellenen += 1
            st.title = baslik
            st.text = temiz
            st.word_count = kelime
            st.grade_min = gmin
            st.grade_max = gmax
            st.level = seviye
            st.status = "live"
            st.sort_order = sira

            # Sorular: her zaman yeniden yazilir (metin degisirse tutarli kalsin)
            db.query(StoryQuestion).filter(
                StoryQuestion.story_id == sid).delete(synchronize_session=False)
            for i, (tur, soru, siklar, ai, expl) in enumerate(sorular):
                dogru = siklar[ai]
                karisik = list(siklar)
                random.shuffle(karisik)
                db.add(StoryQuestion(
                    id=f"{sid}_q{i+1}", story_id=sid, type=tur,
                    text=soru, options=karisik,
                    answer_index=karisik.index(dogru),
                    explanation=expl, sort_order=i,
                ))
    db.commit()
    return eklenen, guncellenen


def seed_questions(db, reset: bool = False) -> tuple[int, int]:
    if reset:
        db.query(Question).delete()
        db.commit()

    eklenen = 0
    atlanan = 0

    for cid, sorular in SORU_BANKASI.items():
        cat = db.get(Category, cid)
        if cat is None:
            print(f"  UYARI: kategori yok -> {cid}")
            continue

        for (band, gmin, gmax, text, options, ai, expl) in sorular:
            dogru = options[ai]

            # Idempotent kontrol: ayni metin VE ayni dogru cevap varsa atla.
            #
            # DIKKAT: Sadece metne bakmak YANLIS. "Hangisi dogru yazilmistir?"
            # gibi kalip sorular onlarca kez, farkli siklarla kullanilir.
            # Metne bakan kontrol bunlarin ilkini alip gerisini atardi.
            mevcut = None
            for aday in db.query(Question).filter(
                Question.category_id == cid, Question.text == text
            ).all():
                if aday.options[aday.answer_index] == dogru:
                    mevcut = aday
                    break
            if mevcut:
                atlanan += 1
                continue

            # Siklari karistir, dogru indeksi guncelle
            karisik = options[:]
            random.shuffle(karisik)

            db.add(Question(
                category_id=cid,
                grade_min=gmin, grade_max=gmax, band=band,
                text=text, options=karisik,
                answer_index=karisik.index(dogru),
                explanation=expl,
                source="human", status="live",
            ))
            eklenen += 1

    db.commit()
    return eklenen, atlanan


def dogrula(db) -> list[str]:
    """Seed sonrasi tutarlilik kontrolu."""
    hatalar = []

    # Okuma kategorisi Question tablosunu kullanmaz; Story + StoryQuestion
    # tablolarindan beslenir. Bu yuzden soru sayisi kontrolunden muaftir.
    OZEL_KATEGORILER = {"okuma"}

    # 1. Her yazili kategorinin sorusu var mi?
    for c in db.query(Category).filter(Category.is_procedural.is_(False)).all():
        if c.id in OZEL_KATEGORILER:
            continue
        n = db.query(Question).filter(Question.category_id == c.id,
                                      Question.status == "live").count()
        if n == 0:
            hatalar.append(f"'{c.name}' kategorisinde hic soru yok")
        elif n < 15:
            hatalar.append(f"'{c.name}' kategorisinde sadece {n} soru (az)")

    # 2. Prosedurel kategorilerin generator'i var mi?
    from generators import REGISTRY
    for c in db.query(Category).filter(Category.is_procedural.is_(True)).all():
        if c.generator_key not in REGISTRY:
            hatalar.append(f"'{c.name}' icin generator yok: {c.generator_key}")

    # 3. Sorularin sik sayisi ve dogru indeksi
    for q in db.query(Question).all():
        if len(q.options) != 4:
            hatalar.append(f"Soru {q.id[:8]}: {len(q.options)} sik")
        if not (0 <= q.answer_index < len(q.options)):
            hatalar.append(f"Soru {q.id[:8]}: gecersiz answer_index")
        if len(set(q.options)) != len(q.options):
            hatalar.append(f"Soru {q.id[:8]}: tekrar eden sik")

    # 4. Her sinif icin yeterli kategori var mi?
    import config as cfg
    for grade in (1, 2):
        n = db.query(Category).filter(Category.grade_min <= grade,
                                      Category.grade_max >= grade).count()
        hedef = cfg.QUEST_CATEGORY_COUNT.get(grade, 8)
        if n < hedef:
            hatalar.append(f"{grade}. sinif icin sadece {n} kategori (gerekli: {hedef})")

    # 5. Kaynak dosyadaki soru sayisi DB'ye tam yansidi mi?
    #
    # Bu kontrol gercek bir hatayi yakalamak icin var: duplicate kontrolu
    # sadece metne bakarsa, "Hangisi dogru yazilmistir?" gibi kalip sorularin
    # ilki alinip gerisi sessizce atlanir. Sayilar tutmazsa burada patlar.
    for cid, sorular in SORU_BANKASI.items():
        if cid in OZEL_KATEGORILER:
            continue
        beklenen = len(sorular)
        gercek = db.query(Question).filter(Question.category_id == cid).count()
        if gercek < beklenen:
            c = db.get(Category, cid)
            ad = c.name if c else cid
            hatalar.append(
                f"'{ad}': kaynakta {beklenen} soru var ama DB'de {gercek} "
                f"({beklenen - gercek} soru eksik!)"
            )

    # 6b. Dogru cevap dagilimi dengeli mi?
    #     Tum dogru cevaplar ayni sikta olursa cocuk ezberden gecer.
    from collections import Counter
    for tablo, ad in ((Question, "soru bankasi"),):
        dag = Counter(q.answer_index for q in db.query(tablo).all())
        toplam = sum(dag.values())
        if toplam > 20:
            en_cok = max(dag.values())
            if en_cok > toplam * 0.45:
                hatalar.append(
                    f"{ad}: dogru cevaplarin %{100*en_cok//toplam}'i ayni sikta "
                    f"- siklar karistirilmali")

    # 6. Okuma metinleri saglikli mi?
    from models import Story, StoryQuestion
    for st in db.query(Story).filter(Story.status == "live").all():
        n = db.query(StoryQuestion).filter(
            StoryQuestion.story_id == st.id).count()
        if n != 5:
            hatalar.append(f"'{st.title}' metninde {n} soru var (5 olmali)")
        if st.word_count < 15:
            hatalar.append(f"'{st.title}' cok kisa ({st.word_count} kelime) "
                           f"- okuma hizi olculemez")

    # Hikaye sorularinda dogru cevap dagilimi
    sq_dag = Counter(q.answer_index for q in db.query(StoryQuestion).all())
    sq_toplam = sum(sq_dag.values())
    if sq_toplam > 20:
        en_cok = max(sq_dag.values())
        if en_cok > sq_toplam * 0.45:
            hatalar.append(
                f"okuma sorulari: dogru cevaplarin %{100*en_cok//sq_toplam}'i "
                f"ayni sikta - siklar karistirilmali")
    for g in (1, 2, 3, 4):
        n = db.query(Story).filter(Story.grade_min <= g, Story.grade_max >= g,
                                   Story.status == "live").count()
        if n < 3:
            hatalar.append(f"{g}. sinif icin sadece {n} okuma metni var "
                           f"(en az 3 olmali)")

    return hatalar


def main():
    reset = "--reset" in sys.argv

    print("Veritabani olusturuluyor...")
    init_db()

    db = SessionLocal()
    try:
        print("\nKategoriler...")
        n = seed_categories(db)
        toplam = db.query(Category).count()
        print(f"  {n} yeni, toplam {toplam}")

        print("Rozetler...")
        n = seed_badges(db)
        print(f"  {n} yeni, toplam {db.query(Badge).count()}")

        print("Zeki'nin Evi esyalari...")
        n = seed_house(db)
        print(f"  {n} yeni, toplam {db.query(HouseItem).count()}")

        print("Okuma metinleri...")
        e, g = seed_stories(db)
        from models import Story, StoryQuestion
        print(f"  {e} yeni, {g} guncellendi -> {db.query(Story).count()} metin, "
              f"{db.query(StoryQuestion).count()} anlama sorusu")

        print("Soru bankasi...")
        eklenen, atlanan = seed_questions(db, reset)
        print(f"  {eklenen} eklendi, {atlanan} zaten vardi")
        print(f"  Toplam yazili soru: {db.query(Question).count()}")

        # Kategori bazli dagilim
        print("\n  Kategori bazli:")
        for cid in SORU_BANKASI:
            c = db.get(Category, cid)
            n = db.query(Question).filter(Question.category_id == cid).count()
            if c:
                print(f"    {c.icon} {c.name:22s} {n:3d} soru")

        print("\nDogrulama...")
        hatalar = dogrula(db)
        if hatalar:
            print(f"  {len(hatalar)} uyari:")
            for h in hatalar:
                print(f"    - {h}")
        else:
            print("  Tum kontroller basarili")

        # Ozet
        print("\n" + "=" * 55)
        proc = db.query(Category).filter(Category.is_procedural.is_(True)).count()
        yazili = db.query(Category).filter(Category.is_procedural.is_(False)).count()
        print(f"Kategori:      {toplam} ({proc} prosedurel + {yazili} yazili)")
        print(f"Yazili soru:   {db.query(Question).count()}")
        print(f"Prosedurel:    sinirsiz ({proc} kategori)")
        for grade in (1, 2):
            n = db.query(Category).filter(Category.grade_min <= grade,
                                          Category.grade_max >= grade).count()
            print(f"{grade}. sinif:      {n} kategori")
        print("=" * 55)

    finally:
        db.close()


if __name__ == "__main__":
    main()
