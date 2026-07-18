import pytest


@pytest.fixture
def tree(tmp_path):
    """Build a small directory tree with a few node_modules and .git folders.

    Layout:
        root/
            project_a/
                node_modules/
                    pkg/file.js   (some bytes)
            project_b/
                node_modules/
                    file.txt
                nested/
                    node_modules/     <- should NOT be found (inside another node_modules)
            excluded_dir/
                node_modules/         <- excluded via --exclude
            .git/
    """
    root = tmp_path / "root"

    a_nm = root / "project_a" / "node_modules" / "pkg"
    a_nm.mkdir(parents=True)
    (a_nm / "file.js").write_bytes(b"x" * 100)

    b_nm = root / "project_b" / "node_modules"
    b_nm.mkdir(parents=True)
    (b_nm / "file.txt").write_bytes(b"y" * 50)
    # nested node_modules INSIDE node_modules - should be skipped since
    # find_dirs removes matched dirs from further traversal
    (b_nm / "nested" / "node_modules").mkdir(parents=True)

    excluded_nm = root / "excluded_dir" / "node_modules"
    excluded_nm.mkdir(parents=True)

    (root / ".git").mkdir(parents=True)

    return root
