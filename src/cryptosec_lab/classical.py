"""Caesar experiments over ASCII letters, with English-only statistical analysis."""

from collections import Counter
from dataclasses import dataclass

ENGLISH = (
    8.167,
    1.492,
    2.782,
    4.253,
    12.702,
    2.228,
    2.015,
    6.094,
    6.966,
    0.153,
    0.772,
    4.025,
    2.406,
    6.749,
    7.507,
    1.929,
    0.095,
    5.987,
    6.327,
    9.056,
    2.758,
    0.978,
    2.360,
    0.150,
    1.974,
    0.074,
)
MAX_TEXT = 100_000


def _text(text: str) -> None:
    if not isinstance(text, str):
        raise TypeError("text must be str")
    if len(text) > MAX_TEXT:
        raise ValueError("teaching limit: 100000 characters")


def encrypt(text: str, shift: int) -> str:
    """Rotate ASCII letters; preserve case, Unicode, punctuation, and spaces."""
    _text(text)
    if type(shift) is not int:
        raise TypeError("shift must be an integer")
    shift %= 26
    result = []
    for char in text:
        base = 65 if "A" <= char <= "Z" else 97 if "a" <= char <= "z" else None
        result.append(char if base is None else chr(base + (ord(char) - base + shift) % 26))
    return "".join(result)


def decrypt(text: str, shift: int) -> str:
    if type(shift) is not int:
        raise TypeError("shift must be an integer")
    return encrypt(text, -shift)


@dataclass(frozen=True)
class Candidate:
    shift: int
    plaintext: str
    chi_square: float


def analyze(ciphertext: str) -> list[Candidate]:
    """Rank all 26 keys by chi-square; ranking is a heuristic, not a proof."""
    _text(ciphertext)
    counts = Counter(c.upper() for c in ciphertext if "A" <= c <= "Z" or "a" <= c <= "z")
    total = sum(counts.values())
    if not total:
        raise ValueError("frequency analysis requires ASCII letters")
    result = []
    for shift in range(26):
        score = sum(
            (counts.get(chr(65 + (i + shift) % 26), 0) - total * freq / 100) ** 2
            / (total * freq / 100)
            for i, freq in enumerate(ENGLISH)
        )
        result.append(Candidate(shift, decrypt(ciphertext, shift), score))
    return sorted(result, key=lambda candidate: (candidate.chi_square, candidate.shift))
