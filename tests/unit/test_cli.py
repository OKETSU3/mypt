import tempfile
from pathlib import Path

import pytest

from demo.cli import main


class TestCLI:
    """Unit tests for CLI functionality."""

    def test_count_command_with_direct_text(self) -> None:
        """CLI count basic - outputs word count for direct text input."""
        result = main(["count", "a b"])
        assert result == 0

    def test_freq_command_with_text_flag(self) -> None:
        """CLI freq basic - outputs frequency for word in text."""
        result = main(["freq", "b", "-t", "a b b"])
        assert result == 0

    def test_count_command_with_file_input(self) -> None:
        """Test count command reading from file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("hello world test")
            temp_path = Path(f.name)

        try:
            result = main(["count", "--file", str(temp_path)])
            assert result == 0
        finally:
            temp_path.unlink()

    def test_freq_command_with_file_input(self) -> None:
        """Test freq command reading from file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("hello world world")
            temp_path = Path(f.name)

        try:
            result = main(["freq", "world", "--file", str(temp_path)])
            assert result == 0
        finally:
            temp_path.unlink()

    def test_count_command_no_input_returns_error(self) -> None:
        """Test count command with no input returns error."""
        result = main(["count"])
        assert result == 1

    def test_freq_command_no_text_returns_error(self) -> None:
        """Test freq command with no text input returns error."""
        result = main(["freq", "word"])
        assert result == 1

    def test_count_command_both_text_and_file_returns_error(self) -> None:
        """Test count command with both text and file returns error."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("test")
            temp_path = Path(f.name)

        try:
            result = main(["count", "text", "--file", str(temp_path)])
            assert result == 1
        finally:
            temp_path.unlink()

    def test_freq_command_both_text_and_file_returns_error(self) -> None:
        """Test freq command with both text and file returns error."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("test")
            temp_path = Path(f.name)

        try:
            result = main(["freq", "word", "-t", "text", "--file", str(temp_path)])
            assert result == 1
        finally:
            temp_path.unlink()

    def test_nonexistent_file_returns_error(self) -> None:
        """Test that nonexistent file returns error."""
        result = main(["count", "--file", "/nonexistent/file.txt"])
        assert result == 1

    def test_no_command_shows_help(self) -> None:
        """Test that no command shows help and returns error."""
        result = main([])
        assert result == 1

    def test_unknown_command_returns_error(self) -> None:
        """Test that unknown command returns error."""
        # argparse will raise SystemExit for unknown commands
        with pytest.raises(SystemExit) as exc_info:
            main(["unknown"])
        assert exc_info.value.code == 2  # argparse error exit code
