# CryptoSec-Lab

**Cryptography & Password Security Learning Lab**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](pyproject.toml)
[![MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[中文](README.md) · [Learning guide](docs/index.md) · [Plan](PROJECT_PLAN.md) · [Roadmap](docs/ROADMAP.md)

Runnable Python experiments for learners and security developers: Caesar encryption and English frequency analysis, AES-GCM authenticated encryption and tamper rejection, and bounded Argon2id/scrypt/PBKDF2 password hashing benchmarks. Core explanations are Chinese; this entry and the CLI are available in English. Planned modules are explicitly marked in the Chinese navigation.

## Run locally

Python 3.11+ is required. From the repository root on Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/cryptosec caesar
.venv/bin/cryptosec aes
.venv/bin/cryptosec kdf --repeats 3
.venv/bin/python -m pytest -q
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
```

On Windows, use `py -3.12 -m venv .venv`, `.venv\Scripts\python.exe` and `.venv\Scripts\cryptosec.exe`. Use another supported interpreter if needed. For pinned dependencies, install `requirements-dev.lock` first, then install this project with `--no-deps --no-build-isolation -e .`.

```python
from cryptosec_lab.modern import decrypt, encrypt, new_key

key = new_key()
message = encrypt(key, b"CryptoSec-Lab", b"lesson:01")
assert decrypt(key, message, b"lesson:01") == b"CryptoSec-Lab"
```

`cryptosec aes` reports `roundtrip: true`, `tamper_rejected: true`, and `nonce_bytes: 12`. Keys are generated in memory and never printed. Open [the standalone Caesar visualization](assets/caesar.html) in a local browser; it makes no network requests.

## Experiments

| Lab | Guide | Boundary |
| --- | --- | --- |
| Caesar | [Explanation](docs/classical/caesar.md) | ASCII letters; English scoring is heuristic |
| AES-GCM | [Explanation](docs/modern/aes-gcm.md) | 1 MiB messages; no production key lifecycle |
| Password KDFs | [Explanation](docs/passwords/kdf.md) | Synthetic inputs; 1–5 hashes per algorithm |

Benchmarks run serially in fresh processes, with a 60-second timeout each. Timings cover hashing only; sampled process-tree RSS includes launchers, interpreters, imports and verification, may miss short peaks and may double-count shared pages. Fixed profiles are educational baselines, not equally secure configurations or deployment recommendations. No network targets, account automation, or external credential input are supported.

## Contribute and use responsibly

See [CONTRIBUTING](CONTRIBUTING.md), [SECURITY](SECURITY.md), [verification progress](PROGRESS.md), and [v0.1.0 release notes](docs/releases/v0.1.0.md). The project is a local release candidate; remote CI and releases are not claimed as completed. Six modules span fundamentals, classical cryptography, password storage, security experiments, generated CTFs, and modern engineering.

Use only self-owned environments, synthetic data, CTFs or explicitly authorized targets. No unauthorized access or credential collection. Original code and documentation are licensed under [MIT](LICENSE).
