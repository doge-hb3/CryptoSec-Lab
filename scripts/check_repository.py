"""Check local Markdown links, executable documentation and common secret patterns.

This is a focused pre-publication check, not a comprehensive security audit.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {".git", ".venv", ".pytest_cache", ".ruff_cache", "dist", "__pycache__", "build"}
PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{32,}\b"),
)


def main() -> None:
    errors = []
    paths = sorted(
        p
        for p in ROOT.rglob("*")
        if p.is_file() and not EXCLUDE.intersection(p.relative_to(ROOT).parts)
    )
    for path in paths:
        if path.suffix not in {".md", ".py", ".toml", ".yml", ".html", ".lock"}:
            continue
        content = path.read_text(encoding="utf-8")
        if any(pattern.search(content) for pattern in PATTERNS):
            errors.append(f"possible secret: {path.relative_to(ROOT)}")
        if path.suffix != ".md":
            continue
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            target = target.split("#")[0]
            if target and not (path.parent / target).resolve().exists():
                errors.append(f"missing link: {path.relative_to(ROOT)} -> {target}")
        for number, block in enumerate(re.findall(r"```python\n(.*?)```", content, re.S), 1):
            try:
                exec(compile(block, f"{path.name}:example{number}", "exec"), {})
            except Exception as error:
                errors.append(f"example failed: {path.name} block {number}: {error}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Repository checks passed: {len(paths)} files; links, Python examples, secret patterns.")


if __name__ == "__main__":
    main()
