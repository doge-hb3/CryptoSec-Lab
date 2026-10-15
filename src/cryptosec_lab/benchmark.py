"""Bounded local benchmark, with each KDF isolated in a fresh subprocess."""

import json
import platform
import statistics
import subprocess
import sys
import time

import psutil

from cryptosec_lab.passwords import (
    ALGORITHMS,
    PARAMETERS,
    hash_password,
    synthetic_password,
    verify_password,
)


def _worker(algorithm: str, repeats: int) -> None:
    password = synthetic_password()
    wall, cpu = [], []
    for _ in range(repeats):
        start, cpu_start = time.perf_counter(), time.process_time()
        record = hash_password(password, algorithm)
        cpu.append((time.process_time() - cpu_start) * 1000)
        wall.append((time.perf_counter() - start) * 1000)
        if not verify_password(password, record):
            raise RuntimeError("KDF verification failed")
    print(json.dumps({"hash_ms": wall, "cpu_ms": cpu}))


def benchmark(repeats: int = 3) -> dict:
    if type(repeats) is not int or not 1 <= repeats <= 5:
        raise ValueError("repeats must be 1..5")
    rows = []
    for algorithm in ALGORITHMS:
        with subprocess.Popen(
            [sys.executable, "-m", "cryptosec_lab.benchmark", algorithm, str(repeats)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as process:
            child = psutil.Process(process.pid)
            peak = 0
            deadline = time.monotonic() + 60
            while process.poll() is None:
                if time.monotonic() > deadline:
                    process.kill()
                    process.communicate()
                    raise TimeoutError("worker exceeded 60 seconds")
                try:
                    # Windows venv python.exe may be a launcher with a child interpreter.
                    processes = [child, *child.children(recursive=True)]
                    rss = 0
                    for member in processes:
                        try:
                            rss += member.memory_info().rss
                        except psutil.NoSuchProcess:
                            pass
                    peak = max(peak, rss)
                except psutil.NoSuchProcess:
                    pass
                time.sleep(0.01)
            stdout, stderr = process.communicate()
            if process.returncode:
                raise RuntimeError(f"{algorithm} worker failed: {stderr[:1000]}")
        data = json.loads(stdout)
        rows.append(
            {
                "algorithm": algorithm,
                "parameters": PARAMETERS[algorithm],
                "hash_ms": data["hash_ms"],
                "median_hash_ms": statistics.median(data["hash_ms"]),
                "median_cpu_ms": statistics.median(data["cpu_ms"]),
                "sampled_peak_process_tree_rss_mib": peak / 1024**2,
            }
        )
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "repeats": repeats,
        "results": rows,
        "method": (
            "Fresh process per KDF; hash timing excludes verification; tree RSS sampled at 10 ms."
        ),
        "limits": (
            "RSS includes interpreter/imports/verification, may miss peaks; not equal security."
        ),
    }


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ALGORITHMS:
        raise SystemExit("internal worker: algorithm repeats")
    count = int(sys.argv[2])
    if not 1 <= count <= 5:
        raise SystemExit("repeats must be 1..5")
    _worker(sys.argv[1], count)
