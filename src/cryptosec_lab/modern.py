"""Authenticated encryption through cryptography's maintained AESGCM API."""

import secrets
from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MAX_MESSAGE = 1_048_576


@dataclass(frozen=True)
class Envelope:
    nonce: bytes
    ciphertext: bytes  # Includes the 16-byte authentication tag.


def new_key() -> bytes:
    return AESGCM.generate_key(bit_length=256)


def _validate(key: bytes, data: bytes, aad: bytes) -> None:
    if not all(isinstance(value, bytes) for value in (key, data, aad)):
        raise TypeError("key, message, and aad must be bytes")
    if len(key) != 32:
        raise ValueError("this lab uses a 32-byte AES-256 key")
    if len(data) > MAX_MESSAGE + 16 or len(aad) > MAX_MESSAGE:
        raise ValueError("teaching limit: 1 MiB plus authentication tag")


def encrypt(key: bytes, plaintext: bytes, aad: bytes = b"") -> Envelope:
    """Generate a fresh 96-bit nonce; caller cannot accidentally pass a reused nonce."""
    _validate(key, plaintext, aad)
    if len(plaintext) > MAX_MESSAGE:
        raise ValueError("teaching limit: 1 MiB plaintext")
    nonce = secrets.token_bytes(12)
    return Envelope(nonce, AESGCM(key).encrypt(nonce, plaintext, aad))


def decrypt(key: bytes, envelope: Envelope, aad: bytes = b"") -> bytes:
    """Raise InvalidTag on wrong key, changed ciphertext, nonce, or AAD."""
    if not isinstance(envelope, Envelope):
        raise TypeError("expected Envelope")
    _validate(key, envelope.ciphertext, aad)
    if not isinstance(envelope.nonce, bytes) or len(envelope.nonce) != 12:
        raise ValueError("nonce must be 12 bytes")
    return AESGCM(key).decrypt(envelope.nonce, envelope.ciphertext, aad)
