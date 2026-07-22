"""
Bir hesabi admin yapar / admin listesini gosterir.

Admin paneli IKI kosul birden ister:
  1. Hesabin is_admin bayragi (bu script ile acilir)
  2. ADMIN_PASSWORD ortam degiskeni (sunucuyu baslatirken verilir)

Kullanim:
    python content/make_admin.py                      # admin listesi
    python content/make_admin.py eposta@ornek.com     # admin yap
    python content/make_admin.py eposta@ornek.com --remove
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models import SessionLocal, Account, init_db  # noqa: E402
import config as cfg  # noqa: E402


def main():
    init_db()
    db = SessionLocal()
    try:
        args = [a for a in sys.argv[1:] if not a.startswith("--")]
        remove = "--remove" in sys.argv

        # Liste
        if not args:
            adminler = db.query(Account).filter(Account.is_admin.is_(True)).all()
            print("\nMevcut adminler:")
            if not adminler:
                print("  (yok)")
            for a in adminler:
                print(f"  - {a.email}")

            print(f"\nADMIN_PASSWORD: "
                  f"{'AYARLI' if cfg.ADMIN_PASSWORD else 'AYARLI DEGIL -> panel KAPALI'}")
            print("\nKullanim:")
            print("  python content/make_admin.py eposta@ornek.com")
            print("  python content/make_admin.py eposta@ornek.com --remove")
            print("\nSunucuyu admin sifresiyle baslatin:")
            print("  ADMIN_PASSWORD='guclu-bir-sifre' python main.py")
            return 0

        email = args[0].lower()
        acc = db.query(Account).filter(Account.email == email).first()
        if acc is None:
            print(f"\nHATA: '{email}' bulunamadi.")
            print("Once siteden normal kayit olun, sonra bu scripti calistirin.\n")
            print("Kayitli hesaplar:")
            for a in db.query(Account).order_by(Account.created_at).limit(20):
                print(f"  - {a.email}")
            return 1

        acc.is_admin = not remove
        db.commit()

        if remove:
            print(f"\n'{email}' artik admin DEGIL.\n")
        else:
            print(f"\n'{email}' admin yapildi.\n")
            if not cfg.ADMIN_PASSWORD:
                print("DIKKAT: ADMIN_PASSWORD ayarli degil, panel yine de kapali.")
                print("Sunucuyu soyle baslatin:\n")
                print("  ADMIN_PASSWORD='guclu-bir-sifre' python main.py\n")
            else:
                print("Panel: http://localhost:3420/admin\n")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
