import argparse
import os
import shutil
from pathlib import Path


class Color:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def calculate_size(folder: str) -> int:
    """Calculate the total size of a folder recursively.

    Args:
        folder (str): Path to the folder.

    Returns:
        int: Total size in bytes.
    """
    size = 0
    for current, _, files in os.walk(folder):
        for file in files:
            size += os.path.getsize(os.path.join(current, file))
    return size


def format_size(size: int) -> str:
    """Format a size in bytes to a human-readable string.

    Args:
        size (int): Size in bytes.

    Returns:
        str: Human-readable size string (e.g. '1.23 MB').
    """

    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size = int(size / 1024)
    return f"{size:.2f} TB"


def find_dirs(search: str, root: str) -> list[Path]:
    """Recursively find all directories matching a given name.

    Skips descending into matched directories to avoid nested results.

    Args:
        search (str): Directory name to search for.
        root (str): Root directory to search from.

    Returns:
        list[Path]: List of matched directory paths.
    """

    results = []

    for current, dirs, _ in os.walk(root):
        if search in dirs:
            found = Path(current) / search
            results.append(found)

            dirs.remove(search)

    return results


def clean(directories: list[Path], yes: bool = False) -> None:
    """Delete a list of directories with optional confirmation.

    Args:
        directories (list[Path]): List of directories to delete.
        yes (bool): If True, skip confirmation prompt. Defaults to False.

    Returns:
        None
    """

    print(Color.YELLOW + f"Found {len(directories)} folder(s) to sweep." + Color.RESET)
    size: int = 0
    dir_size: int = 0
    deleted_dir_num: int = 0
    for directory in directories:
        try:
            if not yes:
                confirm = input(f"Delete {str(directory)} [Y]es/[A]ll/[N]o:")
                if confirm.lower() == "a":
                    yes = True
                    print(Color.RED + f"Removing {str(directory)}..." + Color.RESET)
                    dir_size = calculate_size(str(directory))
                    shutil.rmtree(directory)
                    size += dir_size
                    deleted_dir_num += 1
                elif confirm.lower() == "y":
                    print(Color.RED + f"Removing {str(directory)}..." + Color.RESET)
                    dir_size = calculate_size(str(directory))
                    shutil.rmtree(directory)
                    size += dir_size
                    deleted_dir_num += 1
            else:
                print(Color.RED + f"Removing {str(directory)}..." + Color.RESET)
                dir_size = calculate_size(str(directory))
                shutil.rmtree(directory)
                size += dir_size
                deleted_dir_num += 1
        except PermissionError as e:
            print(
                Color.BOLD
                + Color.RED
                + f"Permission denied due to {str(e)}"
                + Color.RESET
            )
        except OSError as e:
            print(Color.BOLD + Color.RED + f"OS Error occurred: {str(e)}" + Color.RESET)
        except Exception as e:
            print(
                Color.BOLD + Color.RED + f"Exception occurred: {str(e)}" + Color.RESET
            )
    print(
        Color.YELLOW
        + f"Swept {deleted_dir_num}/{len(directories)} folders."
        + Color.RESET
    )
    print(Color.GREEN + f"Freed up {format_size(size)}" + Color.RESET)


def dry_run(directories: list[Path]) -> None:
    """Print directories without deleting them.

    Args:
        directories (list[Path]): List of directories to display.

    Returns:
        None
    """

    for directory in directories:
        print(Color.YELLOW + str(directory) + Color.RESET)


def main() -> None:
    """Entry point for the sweep CLI.

    Parses arguments, finds target directories, and either
    performs a dry run or deletes them based on the provided flags.

    Returns:
        None
    """

    parser = argparse.ArgumentParser(description="Clean folders from directories")

    parser.add_argument("root", help="Target directory")
    parser.add_argument(
        "--target",
        "-t",
        default=["node_modules"],
        nargs="+",
        help="Folder name to sweep",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Display folders' location to sweep"
    )
    parser.add_argument(
        "--yes", "-y", action="store_true", help="Delete all found locations"
    )

    args = parser.parse_args()

    locations = []
    for target in args.target:
        locations.extend(find_dirs(target, args.root))

    if not locations:
        print(
            Color.YELLOW
            + f"No {', '.join(args.target)} folders found in {args.root}"
            + Color.RESET
        )
        return

    if args.dry_run:
        dry_run(locations)
    else:
        clean(locations, args.yes)


if __name__ == "__main__":
    main()
