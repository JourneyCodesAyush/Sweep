# tests/test_benchmark.py
import os
from pathlib import Path

import pytest

from sweep.__main__ import find_dirs


def naive_find_dirs(search: str, root: str) -> list[Path]:
    """Same traversal, but WITHOUT pruning matched dirs from os.walk.
    Used only to benchmark against the real, pruned implementation.
    """
    results = []
    for current, dirs, _ in os.walk(root):
        if search in dirs:
            results.append(Path(current) / search)
            # no dirs.remove(search) here — walks into it anyway
    return results


def make_tree(base: Path, depth: int, packages: int, files_per_pkg: int):
    nm = base / "node_modules"
    nm.mkdir(parents=True, exist_ok=True)
    for i in range(packages):
        pkg = nm / f"pkg-{i}"
        pkg.mkdir(exist_ok=True)
        for f in range(files_per_pkg):
            (pkg / f"file{f}.js").write_text("// filler")
        if depth > 0 and i % 3 == 0:
            make_tree(pkg, depth - 1, max(2, packages // 2), files_per_pkg)


@pytest.fixture(scope="module")
def big_tree(tmp_path_factory):
    root = tmp_path_factory.mktemp("bench_tree")
    for project in range(5):
        make_tree(root / f"project-{project}", depth=2, packages=15, files_per_pkg=3)
    return root


def test_find_dirs_pruned_benchmark(benchmark, big_tree):
    result = benchmark(find_dirs, "node_modules", str(big_tree))
    assert len(result) > 0


def test_find_dirs_naive_benchmark(benchmark, big_tree):
    result = benchmark(naive_find_dirs, "node_modules", str(big_tree))
    assert len(result) > 0
