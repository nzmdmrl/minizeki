import random
from typing import Callable

REGISTRY: dict[str, Callable] = {}


def register(key: str):
    def deco(fn):
        REGISTRY[key] = fn
        return fn
    return deco


def finalize(text: str, correct, distractors: list, band: int,
             explanation: str = "", svg: str | None = None,
             emoji: str | None = None) -> dict:
    """
    Siklari karistirir, dogru cevabin indeksini bulur.
    correct ve distractors str'e cevrilir.
    """
    correct_s = str(correct)
    seen = {correct_s}
    opts = [correct_s]
    for d in distractors:
        ds = str(d)
        if ds not in seen:
            seen.add(ds)
            opts.append(ds)
        if len(opts) == 4:
            break

    # Yeterli celdirici yoksa doldur (nadir durum)
    filler = 1
    while len(opts) < 4:
        cand = str(int(correct) + filler) if str(correct).lstrip("-").isdigit() else f"?{filler}"
        if cand not in seen:
            seen.add(cand)
            opts.append(cand)
        filler += 1

    random.shuffle(opts)
    return {
        "text": text,
        "options": opts,
        "answer_index": opts.index(correct_s),
        "band": band,
        "explanation": explanation,
        "svg": svg,
        "emoji": emoji,
        "procedural": True,
    }


def pick3(candidates: set, exclude) -> list:
    """Aday celdiricilerden 3 tane sec. Pozitif ve dogru cevaptan farkli."""
    pool = [c for c in candidates if c != exclude]
    if len(pool) <= 3:
        return pool
    return random.sample(pool, 3)


def generate(key: str, grade: int, band: int) -> dict:
    fn = REGISTRY.get(key)
    if not fn:
        raise ValueError(f"Generator bulunamadi: {key}")
    band = max(1, min(5, band))
    return fn(grade, band)
