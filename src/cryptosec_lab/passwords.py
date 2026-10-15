"""Fixed, bounded teaching profiles; records contain salts, never plaintext passwords."""

import hashlib
import hmac
import secrets
from dataclasses import dataclass

from argon2 import PasswordHasher, extract_parameters
from argon2.exceptions import InvalidHashError, VerificationError
from argon2.profiles import RFC_9106_LOW_MEMORY

ALGORITHMS = ("argon2id", "scrypt", "pbkdf2")
ARGON = PasswordHasher.from_parameters(RFC_9106_LOW_MEMORY)
PARAMETERS = {
    "argon2id": {"memory_kib": 65536, "time_cost": 3, "parallelism": 4},
    "scrypt": {"n": 16384, "r": 8, "p": 1, "dklen": 32, "maxmem": 33554432},
    "pbkdf2": {"hash": "sha256", "iterations": 100000, "dklen": 32},
}


@dataclass(frozen=True)
class PasswordRecord:
    algorithm: str
    salt: bytes
    digest: str
    version: int = 1  # Version fixes the profiles; no caller-controlled work factors.


def synthetic_password() -> str:
    return secrets.token_urlsafe(24)


def _password(password: str) -> bytes:
    if not isinstance(password, str):
        raise TypeError("password must be str")
    if not password or len(password) > 1024:
        raise ValueError("password length must be 1..1024 characters")
    raw = password.encode("utf-8")
    if len(raw) > 1024:
        raise ValueError("UTF-8 password exceeds 1024 bytes")
    return raw


def _derive(raw: bytes, salt: bytes, algorithm: str) -> bytes:
    if algorithm == "pbkdf2":
        return hashlib.pbkdf2_hmac("sha256", raw, salt, 100000, dklen=32)
    return hashlib.scrypt(raw, salt=salt, n=16384, r=8, p=1, maxmem=33554432, dklen=32)


def hash_password(password: str, algorithm: str = "argon2id") -> PasswordRecord:
    raw = _password(password)
    if algorithm not in ALGORITHMS:
        raise ValueError("unknown algorithm")
    if algorithm == "argon2id":
        return PasswordRecord(algorithm, b"", ARGON.hash(raw))
    salt = secrets.token_bytes(16)
    return PasswordRecord(algorithm, salt, _derive(raw, salt, algorithm).hex())


def verify_password(password: str, record: PasswordRecord) -> bool:
    raw = _password(password)
    if not isinstance(record, PasswordRecord):
        raise TypeError("expected PasswordRecord")
    if record.version != 1 or record.algorithm not in ALGORITHMS:
        raise ValueError("unsupported record version or algorithm")
    if not isinstance(record.digest, str) or len(record.digest) > 256:
        raise ValueError("invalid record digest")
    if record.algorithm == "argon2id":
        try:
            # Refuse huge/unexpected cost factors before invoking the KDF.
            if record.salt != b"" or extract_parameters(record.digest) != RFC_9106_LOW_MEMORY:
                raise ValueError("record is outside the fixed teaching profile")
            return ARGON.verify(record.digest, raw)
        except (InvalidHashError, VerificationError):
            return False
    if not isinstance(record.salt, bytes) or len(record.salt) != 16:
        raise ValueError("salt must be 16 bytes")
    try:
        expected = bytes.fromhex(record.digest)
    except ValueError as error:
        raise ValueError("digest is not hexadecimal") from error
    if len(expected) != 32:
        raise ValueError("digest must be 32 bytes")
    return hmac.compare_digest(expected, _derive(raw, record.salt, record.algorithm))
