#!/usr/bin/env python3
"""Project name update script.

This script automates the renaming of a Python project template by replacing
the default project name with a user-specified name throughout the codebase.
"""

import argparse
import logging
import re
import sys
from pathlib import Path
from typing import NamedTuple

logger = logging.getLogger(__name__)


class ReplacementStats(NamedTuple):
    """Statistics for replacements made in a file."""

    file_path: Path
    replacements_made: int


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the script."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, format="%(message)s", handlers=[logging.StreamHandler(sys.stdout)]
    )


def get_replacements(old_name: str, new_name: str) -> list[tuple[str, str]]:
    """Generate a list of replacement string pairs.

    Args:
        old_name: The original template name to replace
        new_name: The new project name to use

    Returns:
        List of (old_string, new_string) tuples for replacements
    """
    logger.debug(f"Generating replacements: {old_name} -> {new_name}")

    old_hyphen = old_name.replace("_", "-")
    new_hyphen = new_name.replace("_", "-")

    replacements = [
        # Basic name replacements
        (old_name, new_name),
        (old_hyphen, new_hyphen),
        # Quoted strings
        (f'"{old_name}"', f'"{new_name}"'),
        (f"'{old_name}'", f"'{new_name}'"),
        (f'"{old_hyphen}"', f'"{new_hyphen}"'),
        (f"'{old_hyphen}'", f"'{new_hyphen}'"),
        # Import statements
        (f"from {old_name}", f"from {new_name}"),
        (f"import {old_name}", f"import {new_name}"),
        # Markdown backticks
        (f"`{old_name}`", f"`{new_name}`"),
        (f"`{old_hyphen}`", f"`{new_hyphen}`"),
    ]

    logger.debug(f"Generated {len(replacements)} replacement patterns")
    return replacements


def update_file_contents(
    path: Path, replacements: list[tuple[str, str]], dry_run: bool = False
) -> ReplacementStats:
    """Apply replacements to the contents of a single file.

    Args:
        path: Path to the file to update
        replacements: List of (old, new) replacement pairs
        dry_run: If True, don't actually modify the file

    Returns:
        ReplacementStats with file path and number of replacements made
    """
    logger.debug(f"Processing file: {path}")

    try:
        # Read file content
        content = path.read_text(encoding="utf-8")
        total_replacements = 0

        # Apply each replacement
        for old_str, new_str in replacements:
            if old_str in content:
                replacement_count = content.count(old_str)
                content = content.replace(old_str, new_str)
                total_replacements += replacement_count

                if replacement_count > 0:
                    logger.debug(
                        f"  Replaced '{old_str}' -> '{new_str}' "
                        f"({replacement_count} times)"
                    )

        # Write back if changes were made and not in dry-run mode
        if total_replacements > 0 and not dry_run:
            path.write_text(content, encoding="utf-8")
            logger.info(f"✅ Replaced {total_replacements} occurrences in {path}")
        elif total_replacements > 0 and dry_run:
            logger.info(
                f"[DRY-RUN] Would replace {total_replacements} occurrences in {path}"
            )
        else:
            logger.debug(f"No replacements needed in {path}")

        return ReplacementStats(path, total_replacements)

    except Exception as e:
        logger.error(f"❌ Failed to process {path}: {e}")
        return ReplacementStats(path, 0)


def rename_directory(
    path: Path, old_name: str, new_name: str, dry_run: bool = False
) -> bool:
    """Rename a directory if it matches the old name pattern.

    Args:
        path: Path to check and potentially rename
        old_name: The old directory name to match
        new_name: The new directory name
        dry_run: If True, don't actually rename the directory

    Returns:
        True if directory was renamed (or would be renamed in dry-run), False otherwise
    """
    if not path.exists() or not path.is_dir():
        logger.debug(f"Directory {path} does not exist or is not a directory")
        return False

    if path.name == old_name:
        new_path = path.parent / new_name

        if dry_run:
            logger.info(f"[DRY-RUN] Would rename directory {path} → {new_path}")
            return True
        else:
            try:
                path.rename(new_path)
                logger.info(f"✅ Renamed directory {path} → {new_path}")
                return True
            except Exception as e:
                logger.error(f"❌ Failed to rename directory {path}: {e}")
                return False

    logger.debug(f"Directory {path} does not match pattern '{old_name}'")
    return False


def find_target_files(project_root: Path) -> list[Path]:
    """Identify files to process for project name updates.

    Args:
        project_root: Root directory of the project

    Returns:
        List of Path objects for files that should be processed
    """
    target_files = []

    # Specific files to check
    candidates = [
        project_root / "pyproject.toml",
        project_root / "README.md",
        project_root / ".github" / "workflows" / "ci.yml",
    ]

    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            target_files.append(candidate)
            logger.debug(f"Added target file: {candidate}")
        else:
            logger.debug(f"Skipping non-existent file: {candidate}")

    logger.info(f"Found {len(target_files)} files to process")
    return target_files


def main() -> None:
    """Main function to orchestrate the project name update process."""
    parser = argparse.ArgumentParser(
        description="Update project name throughout the codebase",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/update_project_name.py --new-name my_app
  python scripts/update_project_name.py --new-name my_app --old-name project_name \\
    --verbose
  python scripts/update_project_name.py --new-name my_app --dry-run
        """,
    )

    parser.add_argument(
        "--new-name", required=True, help="The new project name to apply"
    )
    parser.add_argument(
        "--old-name",
        default="project_name",
        help="The original template name to replace (default: project_name)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the changes without modifying any files",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Output detailed logs of replacements"
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)

    logger.info(f"🚀 Starting project name update: {args.old_name} → {args.new_name}")
    if args.dry_run:
        logger.info("🔍 DRY-RUN MODE: No files will be modified")

    # Get project root (assuming script is in scripts/ subdirectory)
    project_root = Path(__file__).parent.parent
    logger.debug(f"Project root: {project_root}")

    # Validate inputs
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", args.new_name):
        logger.error(
            f"❌ Invalid project name '{args.new_name}'. "
            f"Must be a valid Python identifier."
        )
        sys.exit(1)

    # Generate replacements
    replacements = get_replacements(args.old_name, args.new_name)

    # Find target files
    target_files = find_target_files(project_root)

    if not target_files:
        logger.warning("⚠️  No target files found to process")
        return

    # Process files
    stats_list = []
    for file_path in target_files:
        stats = update_file_contents(file_path, replacements, args.dry_run)
        stats_list.append(stats)

    # Handle directory renaming
    src_dir = project_root / "src" / args.old_name
    directory_renamed = rename_directory(
        src_dir, args.old_name, args.new_name, args.dry_run
    )

    # Summary
    total_files_changed = sum(1 for stats in stats_list if stats.replacements_made > 0)
    total_replacements = sum(stats.replacements_made for stats in stats_list)

    logger.info("\n" + "=" * 50)
    logger.info("📊 SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Files processed: {len(target_files)}")
    logger.info(f"Files modified: {total_files_changed}")
    logger.info(f"Total replacements: {total_replacements}")

    if directory_renamed:
        logger.info("Directories renamed: 1")

    if args.dry_run:
        logger.info("\n🔍 This was a dry-run. No files were actually modified.")
        logger.info("Remove --dry-run to apply these changes.")
    else:
        logger.info("\n🎉 Project name updated successfully!")


if __name__ == "__main__":
    main()
