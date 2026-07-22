"""
Ders agirligi normalize.

Veli 'Matematik: Cok' derse diger dersler otomatik kisilir.
Sinirlar: hicbir ders %10'un altina inemez, tek ders %45'i gecemez.
"""
import config as cfg


def normalize(weights: dict[str, float], mevcut_dersler: list[str]) -> dict[str, float]:
    """
    Ham agirliklari (0.5 / 1.0 / 1.5) oransal dagilima cevirir.
    Min %10, max %45 sinirlarini uygular.
    """
    aktif = {d: float(weights.get(d, 1.0)) for d in mevcut_dersler}
    if not aktif:
        return {}

    toplam = sum(aktif.values())
    if toplam <= 0:
        esit = 1.0 / len(aktif)
        return {d: esit for d in aktif}

    oran = {d: w / toplam for d, w in aktif.items()}

    # Sinirlari uygula (iteratif: bir dersi kirpinca digerleri buyur)
    n = len(oran)
    min_pay = min(cfg.MIN_SUBJECT_SHARE, 1.0 / n)
    max_pay = max(cfg.MAX_SUBJECT_SHARE, 1.0 / n)

    for _ in range(10):
        kirpildi = False
        for d in oran:
            if oran[d] < min_pay:
                oran[d] = min_pay
                kirpildi = True
            elif oran[d] > max_pay:
                oran[d] = max_pay
                kirpildi = True
        t = sum(oran.values())
        oran = {d: v / t for d, v in oran.items()}
        if not kirpildi:
            break

    return oran


def kontenjan(oran: dict[str, float], toplam_kategori: int) -> dict[str, int]:
    """
    Oranlari tam sayi kategori sayisina cevirir.
    Yuvarlama farkini en buyuk paya ekler/cikarir.
    """
    ham = {d: oran[d] * toplam_kategori for d in oran}
    sonuc = {d: max(1, int(round(v))) for d, v in ham.items()}

    fark = toplam_kategori - sum(sonuc.values())
    if fark != 0:
        sirali = sorted(ham, key=lambda d: ham[d], reverse=(fark > 0))
        i = 0
        while fark != 0 and i < len(sirali) * 3:
            d = sirali[i % len(sirali)]
            if fark > 0:
                sonuc[d] += 1
                fark -= 1
            elif sonuc[d] > 1:
                sonuc[d] -= 1
                fark += 1
            i += 1

    return sonuc
