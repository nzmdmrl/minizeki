"""
OTOMATIK SEMA GUNCELLEME

SORUN:
  SQLAlchemy'nin create_all() fonksiyonu EKSIK TABLOLARI olusturur ama
  VAR OLAN TABLOYA KOLON EKLEMEZ. Modele yeni bir alan eklendiginde
  (orn. Category.in_daily_quest) mevcut veritabani eski semada kalir ve
  o tabloya yapilan HER sorgu "no such column" hatasi verir.

  Docker/Coolify gibi ortamlarda veritabani kalici volume'de durdugu icin
  bu durum deploy sonrasi tum uygulamayi coker.

COZUM:
  Acilista modeldeki kolonlarla veritabanindaki kolonlar karsilastirilir,
  eksik olanlar ALTER TABLE ile eklenir. Veri KAYBOLMAZ.

SINIRLAR:
  - Sadece kolon EKLER. Kolon silmez, tip degistirmez, tablo yeniden
    adlandirmaz. Bunlar icin elle mudahale gerekir.
  - Yeni kolonlar NULL veya varsayilan degerle dolar.
"""
import logging

from sqlalchemy import inspect, text

from models import Base, engine

log = logging.getLogger("minizeki.migrate")

# SQLAlchemy tipi -> SQL tipi (ALTER TABLE icin)
def _sql_tipi(kolon, lehce: str) -> str:
    try:
        return kolon.type.compile(dialect=engine.dialect)
    except Exception:
        return "TEXT"


def _varsayilan(kolon, lehce: str) -> str:
    """Yeni kolon icin DEFAULT ifadesi. Mevcut satirlar bununla dolar."""
    d = kolon.default
    if d is None or getattr(d, "is_callable", False):
        # Callable default (orn. datetime.utcnow) SQL'e cevrilemez
        return ""
    deger = getattr(d, "arg", None)
    if deger is None or callable(deger):
        return ""
    if isinstance(deger, bool):
        return f" DEFAULT {1 if deger else 0}"
    if isinstance(deger, (int, float)):
        return f" DEFAULT {deger}"
    if isinstance(deger, str):
        return f" DEFAULT '{deger}'"
    return ""


def semayi_guncelle() -> list[str]:
    """
    Eksik tablolari ve kolonlari ekler.
    Yapilan degisikliklerin listesini dondurur.
    """
    degisiklikler: list[str] = []
    lehce = engine.dialect.name

    # 1) Eksik TABLOLAR (create_all bunu zaten yapar, garanti icin)
    Base.metadata.create_all(bind=engine)

    # 2) Eksik KOLONLAR
    insp = inspect(engine)
    mevcut_tablolar = set(insp.get_table_names())

    for tablo_adi, tablo in Base.metadata.tables.items():
        if tablo_adi not in mevcut_tablolar:
            continue  # yeni olusturuldu, kolonlari zaten tam

        db_kolonlar = {c["name"] for c in insp.get_columns(tablo_adi)}
        for kolon in tablo.columns:
            if kolon.name in db_kolonlar:
                continue
            if kolon.primary_key:
                # Birincil anahtar sonradan eklenemez - elle mudahale gerekir
                log.warning("Tablo %s icin eksik birincil anahtar: %s "
                            "(elle mudahale gerekir)", tablo_adi, kolon.name)
                continue

            tip = _sql_tipi(kolon, lehce)
            vars_ = _varsayilan(kolon, lehce)
            sql = f'ALTER TABLE {tablo_adi} ADD COLUMN {kolon.name} {tip}{vars_}'
            try:
                with engine.begin() as conn:
                    conn.execute(text(sql))
                degisiklikler.append(f"{tablo_adi}.{kolon.name}")
                log.info("Sema: %s.%s eklendi", tablo_adi, kolon.name)
            except Exception as e:
                # Kolon zaten varsa veya lehce desteklemiyorsa uygulama
                # durmamali - sadece log'a yazilir.
                log.warning("Sema: %s.%s eklenemedi (%s)",
                            tablo_adi, kolon.name, str(e)[:80])

    return degisiklikler
