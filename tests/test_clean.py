from unittest.mock import patch

from sweep.__main__ import clean


class TestCleanWithYesFlag:
    def test_deletes_all_without_prompting(self, tmp_path):
        d1 = tmp_path / "d1"
        d2 = tmp_path / "d2"
        d1.mkdir()
        d2.mkdir()

        with (
            patch("builtins.input") as mock_input,
            patch("shutil.rmtree") as mock_rmtree,
        ):
            clean([d1, d2], yes=True)

        mock_input.assert_not_called()
        assert mock_rmtree.call_count == 2


class TestCleanWithPrompts:
    def test_yes_deletes_only_that_folder(self, tmp_path):
        d1 = tmp_path / "d1"
        d2 = tmp_path / "d2"
        d1.mkdir()
        d2.mkdir()

        with (
            patch("builtins.input", side_effect=["y", "n"]),
            patch("shutil.rmtree") as mock_rmtree,
        ):
            clean([d1, d2], yes=False)

        mock_rmtree.assert_called_once_with(d1)

    def test_no_skips_folder(self, tmp_path):
        d1 = tmp_path / "d1"
        d1.mkdir()

        with (
            patch("builtins.input", return_value="n"),
            patch("shutil.rmtree") as mock_rmtree,
        ):
            clean([d1], yes=False)

        mock_rmtree.assert_not_called()

    def test_all_deletes_remaining_without_further_prompts(self, tmp_path):
        d1 = tmp_path / "d1"
        d2 = tmp_path / "d2"
        d3 = tmp_path / "d3"
        for d in (d1, d2, d3):
            d.mkdir()

        with (
            patch("builtins.input", side_effect=["a"]) as mock_input,
            patch("shutil.rmtree") as mock_rmtree,
        ):
            clean([d1, d2, d3], yes=False)

        # only prompted once, since 'a' flips yes=True for the rest
        assert mock_input.call_count == 1
        assert mock_rmtree.call_count == 3

    def test_anything_else_treated_as_skip(self, tmp_path):
        d1 = tmp_path / "d1"
        d1.mkdir()

        with (
            patch("builtins.input", return_value="banana"),
            patch("shutil.rmtree") as mock_rmtree,
        ):
            clean([d1], yes=False)

        mock_rmtree.assert_not_called()


class TestCleanErrorHandling:
    def test_permission_error_does_not_stop_remaining_deletions(self, tmp_path):
        d1 = tmp_path / "d1"
        d2 = tmp_path / "d2"
        d1.mkdir()
        d2.mkdir()

        with patch(
            "shutil.rmtree", side_effect=[PermissionError("denied"), None]
        ) as mock_rmtree:
            clean([d1, d2], yes=True)

        # both deletions attempted despite the first one failing
        assert mock_rmtree.call_count == 2

    def test_os_error_does_not_raise(self, tmp_path):
        d1 = tmp_path / "d1"
        d1.mkdir()

        with patch("shutil.rmtree", side_effect=OSError("boom")):
            clean([d1], yes=True)  # should not raise

    def test_generic_exception_does_not_raise(self, tmp_path):
        d1 = tmp_path / "d1"
        d1.mkdir()

        with patch("shutil.rmtree", side_effect=RuntimeError("weird")):
            clean([d1], yes=True)  # should not raise

    def test_error_on_one_folder_does_not_affect_sibling_deletion(self, tmp_path):
        d1 = tmp_path / "d1"
        d2 = tmp_path / "d2"
        d1.mkdir()
        d2.mkdir()

        def rmtree_side_effect(path):
            if path == d1:
                raise PermissionError("denied")
            # d2 actually gets removed to prove it wasn't skipped
            path.rmdir()

        with patch("shutil.rmtree", side_effect=rmtree_side_effect):
            clean([d1, d2], yes=True)

        assert d1.exists()  # failed deletion, untouched
        assert not d2.exists()  # succeeded despite d1's failure


class TestDryRunNeverDeletes:
    def test_dry_run_does_not_touch_filesystem(self, tmp_path):
        from sweep.__main__ import dry_run

        d = tmp_path / "node_modules"
        d.mkdir()
        (d / "file.txt").write_bytes(b"data")

        dry_run([d])

        assert d.exists()
        assert (d / "file.txt").exists()
