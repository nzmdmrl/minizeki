"""
Mevcut veritabanina admin alanlarini ekler.

Yeni kurulumda gerekmez (seed.py zaten olusturur).
Bu script daha once kurulmus bir DB'yi guncellemek icindir.

NOT: alembic autogenerate KULLANILMAZ - tablo dusurme riski var.
Dogrudan SQL ile, IF NOT EXISTS mantigiyla calisir.

Kullanim:  python content/migrate_admin.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import inspect, text  # noqa: E402
from models import engine, init_db  # noqa: E402


def main():
    insp = inspect(engine)
    is_sqlite = engine.dialect.name == "sqlite"

    print("Veritabani guncelleniyor...")

    # 1. account.is_admin
    if "account" in insp.get_table_names():
        kolonlar = {c["name"] for c in insp.get_columns("account")}
        if "is_admin" not in kolonlar:
            tip = "BOOLEAN DEFAULT 0" if is_sqlite else "BOOLEAN DEFAULT FALSE"
            with engine.begin() as conn:
                conn.execute(text(f"ALTER TABLE account ADD COLUMN is_admin {tip}"))
            print("  + account.is_admin eklendi")
        else:
            print("  = account.is_admin zaten var")
    else:
        print("  ! account tablosu yok - once seed.py calistirin")

    # 2. audit_log tablosu (create_all IF NOT EXISTS mantigiyla calisir)
    init_db()
    if "audit_log" in inspect(engine).get_table_names():
        print("  = audit_log hazir")

    print("\nGuncelleme tamam.")
    print("\nSonraki adim:")
    print("  python content/make_admin.py sizin@epostaniz.com")
    print("  ADMIN_PASSWORD='guclu-bir-sifre' python main.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
