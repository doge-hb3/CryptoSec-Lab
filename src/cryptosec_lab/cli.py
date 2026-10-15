"""Three reproducible CLI demos; password experiments generate their own inputs."""

import argparse
import json

from cryptography.exceptions import InvalidTag

from cryptosec_lab import classical, modern
from cryptosec_lab.benchmark import benchmark


def main() -> None:
    parser = argparse.ArgumentParser(description="CryptoSec-Lab local teaching experiments")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("caesar", help="encrypt/decrypt and rank all 26 keys")
    sub.add_parser("aes", help="AES-GCM roundtrip and tamper rejection")
    kdf = sub.add_parser("kdf", help="benchmark synthetic passwords only")
    kdf.add_argument("--repeats", type=int, choices=range(1, 6), default=3)
    args = parser.parse_args()
    if args.command == "caesar":
        plain = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG. " * 8
        cipher = classical.encrypt(plain, 7)
        best = classical.analyze(cipher)[0]
        print(
            json.dumps(
                {
                    "ciphertext_prefix": cipher[:19],
                    "recovered_shift": best.shift,
                    "roundtrip": classical.decrypt(cipher, 7) == plain,
                    "frequency_recovery": best.plaintext == plain,
                },
                indent=2,
            )
        )
    elif args.command == "aes":
        key, plain, aad = modern.new_key(), b"CryptoSec-Lab", b"lesson:01"
        envelope = modern.encrypt(key, plain, aad)
        altered = modern.Envelope(
            envelope.nonce, bytes([envelope.ciphertext[0] ^ 1]) + envelope.ciphertext[1:]
        )
        try:
            modern.decrypt(key, altered, aad)
        except InvalidTag:
            rejected = True
        else:
            rejected = False
        print(
            json.dumps(
                {
                    "roundtrip": modern.decrypt(key, envelope, aad) == plain,
                    "tamper_rejected": rejected,
                    "nonce_bytes": len(envelope.nonce),
                },
                indent=2,
            )
        )
    else:
        print(json.dumps(benchmark(args.repeats), indent=2))
