import pytest

from cryptosec_lab.classical import analyze, decrypt, encrypt


@pytest.mark.parametrize("shift", [-1001, -26, -1, 0, 3, 26, 1001])
@pytest.mark.parametrize("text", ["", "Az za! 中文🙂 123", "ATTACK AT DAWN"])
def test_roundtrip(text, shift):
    assert decrypt(encrypt(text, shift), shift) == text


def test_known_vector():
    assert encrypt("Attack at dawn!", 3) == "Dwwdfn dw gdzq!"


def test_frequency_candidates_and_long_english():
    text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG. " * 8
    candidates = analyze(encrypt(text, 7))
    assert {c.shift for c in candidates} == set(range(26))
    assert candidates[0].shift == 7
    assert candidates[0].plaintext == text


@pytest.mark.parametrize("text", ["", "中文123!", "🙂"])
def test_no_letters(text):
    with pytest.raises(ValueError):
        analyze(text)


def test_invalid_and_bounded_input():
    with pytest.raises(TypeError):
        encrypt("abc", True)
    with pytest.raises(TypeError):
        encrypt(b"abc", 1)
    with pytest.raises(ValueError):
        encrypt("x" * 100001, 1)


def test_non_ascii_case_expansion_does_not_affect_scores():
    ascii_result = analyze("HELLO WORLD")
    unicode_result = analyze("HELLO WORLD ßﬀ")
    assert [(c.shift, c.chi_square) for c in ascii_result] == [
        (c.shift, c.chi_square) for c in unicode_result
    ]
