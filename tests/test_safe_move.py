from pathlib import Path
from functions.safe_move import safe_move


class TestSafeMove:
    def test_safe_move(self, tmpdir):
        # Create temporary directories and files for testing
        src_dir = Path(tmpdir.mkdir("temp_src"))
        dst_dir = Path(tmpdir.mkdir("temp_dst"))
        (src_dir / "test_file.txt").write_text("This is a test file.", encoding="utf-8")

        # Test moving a directory
        safe_move(src_dir, dst_dir / "moved_src")
        assert not src_dir.exists()
        assert (dst_dir / "moved_src").exists()
        assert (dst_dir / "moved_src" / "test_file.txt").exists()

    def test_safe_move_into_itself(self, tmpdir):
        # Create temporary directory for testing
        src_dir = Path(tmpdir.mkdir("temp_src"))
        (src_dir / "test_file.txt").write_text("This is a test file.", encoding="utf-8")

        # Test moving a directory into itself
        safe_move(src_dir, src_dir / "nested")
        assert (src_dir / "nested").exists()
