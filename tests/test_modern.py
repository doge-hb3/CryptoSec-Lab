import pytest
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from cryptosec_lab.modern import Envelope, decrypt, encrypt, new_key


@pytest.mark.parametrize("plain", [b"", b"hello", "中文🙂".encode()])
def test_roundtrip_and_interoperability(plain):
    key = new_key()
    message = encrypt(key, plain, b"context")
    assert decrypt(key, message, b"context") == plain
    assert AESGCM(key).decrypt(message.nonce, message.ciphertext, b"context") == plain
    assert len(message.ciphertext) == len(plain) + 16


@pytest.mark.parametrize("change", ["key", "nonce", "ciphertext", "aad", "truncated"])
def test_authentication_rejects_changes(change):
    key, aad = new_key(), b"header"
    message = encrypt(key, b"payload", aad)
    if change == "key":
        key = new_key()
    elif change == "nonce":
        nonce = bytes([message.nonce[0] ^ 1]) + message.nonce[1:]
        message = Envelope(nonce, message.ciphertext)
    elif change == "ciphertext":
        message = Envelope(
            message.nonce, bytes([message.ciphertext[0] ^ 1]) + message.ciphertext[1:]
        )
    elif change == "truncated":
        message = Envelope(message.nonce, message.ciphertext[:-1])
    else:
        aad = b"other"
    with pytest.raises(InvalidTag):
        decrypt(key, message, aad)


def test_boundary_errors():
    with pytest.raises(ValueError):
        encrypt(b"short", b"payload")
    with pytest.raises(TypeError):
        encrypt(new_key(), "text")
    with pytest.raises(ValueError):
        encrypt(new_key(), b"x" * (1048576 + 1))
    with pytest.raises(ValueError):
        decrypt(new_key(), Envelope(b"short", b"data"))
