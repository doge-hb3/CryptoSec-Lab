import json
import os
import subprocess
import sysconfig
from pathlib import Path

import pytest

from cryptosec_lab.benchmark import benchmark


@pytest.mark.parametrize(
    "command,field", [("caesar", "frequency_recovery"), ("aes", "tamper_rejected")]
)
def test_entrypoint(command, field):
    executable = Path(sysconfig.get_path("scripts")) / (
        "cryptosec.exe" if os.name == "nt" else "cryptosec"
    )
    result = subprocess.run(
        [str(executable), command], capture_output=True, text=True, check=True, timeout=10
    )
    assert json.loads(result.stdout)[field] is True


@pytest.mark.parametrize("count", [0, 6, -1, True])
def test_benchmark_limits(count):
    with pytest.raises(ValueError):
        benchmark(count)


def test_benchmark_real_workers():
    result = benchmark(1)
    assert len(result["results"]) == 3
    for row in result["results"]:
        assert row["median_hash_ms"] > 0
        assert row["sampled_peak_process_tree_rss_mib"] > 0
        assert len(row["hash_ms"]) == 1
