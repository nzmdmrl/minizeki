"""
Tum prosedurel uretecleri toplu test eder.

Kontroller:
  - Tam 4 sik
  - Siklar benzersiz
  - answer_index gecerli
  - Filler sik ('?1' gibi) uretilmemis
  - Soru metni bos degil
  - Mufredat siniri (2. sinif carpim max 5x9, 2. sinifta bolme yok)

Kullanim:  python content/validate_generators.py
"""
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generators import generate, REGISTRY  # noqa: E402

ITER = 300
GRADES = [1, 2, 3, 4]
BANDS = [1, 2, 3, 4, 5]

# Hangi generator hangi siniflarda calisir
SKIP = {
    "bolme": [1, 2],       # bolme 3. siniftan itibaren
    "kesir": [1, 2],       # kesir 3. siniftan itibaren
    "carpim": [1],         # carpim 2. siniftan itibaren
    "sayma": [3, 4],       # sayma 1-2. sinif
    "anagram": [1],
}


def main() -> int:
    hatalar = []
    ornekler = defaultdict(list)
    toplam = 0

    for key in sorted(REGISTRY.keys()):
        for grade in GRADES:
            if grade in SKIP.get(key, []):
                continue
            for band in BANDS:
                for _ in range(ITER):
                    toplam += 1
                    try:
                        q = generate(key, grade, band)
                    except Exception as e:
                        hatalar.append(f"{key} g{grade} b{band}: EXCEPTION {e}")
                        continue

                    opts = q["options"]
                    tag = f"{key} g{grade} b{band}"

                    if len(opts) != 4:
                        hatalar.append(f"{tag}: sik sayisi {len(opts)} -> {opts}")
                    if len(set(opts)) != len(opts):
                        hatalar.append(f"{tag}: tekrar eden sik -> {opts}")
                    if not (0 <= q["answer_index"] < len(opts)):
                        hatalar.append(f"{tag}: gecersiz answer_index")
                    if any(str(o).startswith("?") for o in opts):
                        hatalar.append(f"{tag}: FILLER sik uretildi -> {opts}")
                    if not q["text"].strip():
                        hatalar.append(f"{tag}: bos soru metni")

                    # Mufredat kontrolu
                    if key == "carpim" and grade == 2:
                        parts = q["text"].replace("= ?", "").split("×")
                        a = int(parts[0].strip())
                        if a > 5:
                            hatalar.append(f"{tag}: 2.sinif carpimda {a} > 5 (mufredat disi)")

                if len(ornekler[key]) < 2:
                    ornekler[key].append((grade, band, generate(key, grade, band)))

    print(f"Test edilen soru: {toplam:,}")
    print(f"Generator sayisi: {len(REGISTRY)}")
    print()

    if hatalar:
        print(f"HATA: {len(hatalar)} sorun bulundu")
        seen = set()
        for h in hatalar:
            k = h.split(":")[0]
            if k not in seen:
                seen.add(k)
                print("  -", h)
        return 1

    print("Tum kontroller BASARILI")
    print()
    print("=" * 60)
    print("ORNEK SORULAR")
    print("=" * 60)
    for key in sorted(ornekler):
        g, b, q = ornekler[key][0]
        print(f"\n[{key}] sinif={g} band={b}")
        print(f"  {q['text'][:70]}")
        print(f"  Siklar: {q['options']}")
        print(f"  Dogru:  {q['options'][q['answer_index']]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
