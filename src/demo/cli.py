import argparse
import sys
from pathlib import Path

from .core.text_processor import SimpleTextProcessor
from .utils.logging_config import get_logger

logger = get_logger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="demo",
        description="Simple text processing utility demonstrating TDD best practices",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Count subcommand
    count_parser = subparsers.add_parser("count", help="Count words in text")
    count_parser.add_argument("text", nargs="?", help="Text to count words in")
    count_parser.add_argument(
        "--file",
        type=Path,
        help="File to read text from (exclusive with positional text)",
    )

    # Frequency subcommand
    freq_parser = subparsers.add_parser(
        "freq", help="Count frequency of a specific word"
    )
    freq_parser.add_argument("word", help="Word to count frequency of")
    freq_parser.add_argument("-t", "--text", help="Text to search in")
    freq_parser.add_argument(
        "--file", type=Path, help="File to read text from (exclusive with --text)"
    )

    return parser


def get_text_input(text: str | None, file: Path | None) -> str:
    """Get text input from either text argument or file.

    Args:
        text: Direct text input
        file: File path to read text from

    Returns:
        Text content

    Raises:
        ValueError: If both or neither text and file are provided
        FileNotFoundError: If file doesn't exist
    """
    if text and file:
        raise ValueError("Cannot specify both text and file")

    if not text and not file:
        raise ValueError("Must specify either text or file")

    if file:
        try:
            return file.read_text(encoding="utf-8")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {file}") from e

    return text  # type: ignore[return-value]


def cmd_count(args: argparse.Namespace) -> int:
    """Handle the count command."""
    try:
        text = get_text_input(args.text, args.file)
        processor = SimpleTextProcessor(text)
        count = processor.count_words()

        print(count)
        logger.info("Count command completed", word_count=count)
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        logger.exception("Count command failed", error=str(e))
        return 1


def cmd_freq(args: argparse.Namespace) -> int:
    """Handle the freq command."""
    try:
        text = get_text_input(args.text, args.file)
        processor = SimpleTextProcessor(text)
        frequency = processor.word_frequency(args.word)

        print(frequency)
        logger.info("Frequency command completed", word=args.word, frequency=frequency)
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        logger.exception("Frequency command failed", error=str(e), word=args.word)
        return 1


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point.

    Args:
        argv: Command line arguments (for testing)

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "count":
        return cmd_count(args)
    elif args.command == "freq":
        return cmd_freq(args)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
