from pathlib import Path

from sweep.__main__ import find_dirs


class TestFindDirs:
    def test_finds_all_matching_dirs(self, tree):
        results = find_dirs("node_modules", str(tree))
        names = sorted(str(p) for p in results)
        assert str(tree / "project_a" / "node_modules") in names
        assert str(tree / "project_b" / "node_modules") in names
        assert str(tree / "excluded_dir" / "node_modules") in names

    def test_does_not_descend_into_matched_dirs(self, tree):
        # project_b/node_modules/nested/node_modules exists but sits INSIDE
        # a node_modules that was already matched, so it must not appear.
        results = find_dirs("node_modules", str(tree))
        nested = tree / "project_b" / "node_modules" / "nested" / "node_modules"
        assert nested not in results

    def test_returns_empty_list_when_nothing_found(self, tmp_path):
        empty_root = tmp_path / "empty_root"
        empty_root.mkdir()
        assert find_dirs("node_modules", str(empty_root)) == []

    def test_finds_dangerous_target(self, tree):
        results = find_dirs(".git", str(tree))
        assert results == [tree / ".git"]

    def test_exclude_skips_directory_entirely(self, tree):
        results = find_dirs(
            "node_modules", str(tree), exclude=[str(tree / "excluded_dir")]
        )
        names = [str(p) for p in results]
        assert str(tree / "excluded_dir" / "node_modules") not in names
        # unrelated matches still found
        assert str(tree / "project_a" / "node_modules") in names

    def test_returns_path_objects(self, tree):
        results = find_dirs("node_modules", str(tree))
        assert all(isinstance(p, Path) for p in results)
