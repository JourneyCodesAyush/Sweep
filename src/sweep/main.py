import os
from pathlib import Path
import shutil

import argparse


def calculate_size(folder: str) -> int:
    size = 0
    for current, _, files in os.walk(folder):
        for file in files:
            size += os.path.getsize(os.path.join(current, file))
    return size


def format_size(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size = int(size / 1024)
    return f"{size:.2f} TB"


def find_dirs(search: str, root: str) -> list[Path]:
    results = []

    for current, dirs, _ in os.walk(root):
        if search in dirs:
            found = Path(current) / search
            results.append(found)

            dirs.remove(search)

    return results


def clean(directories: list[Path], yes: bool = False) -> None:
    size: int = 0
    dir_size: int = 0
    for directory in directories:
        try:
            if not yes:
                confirm = input(f"Delete {str(directory)} [Y]es/[A]ll/[N]o:")
                if confirm.lower() == "a":
                    yes = True
                    print(f"Removing {str(directory)}...")
                    dir_size = calculate_size(str(directory))
                    shutil.rmtree(directory)
                    size += dir_size
                elif confirm.lower() == "y":
                    print(f"Removing {str(directory)}...")
                    dir_size = calculate_size(str(directory))
                    shutil.rmtree(directory)
                    size += dir_size
            else:
                print(f"Removing {str(directory)}...")
                dir_size = calculate_size(str(directory))
                shutil.rmtree(directory)
                size += dir_size
        except PermissionError as e:
            print(f"Permission denied due to {str(e)}")
        except OSError as e:
            print(f"OS Error occurred: {str(e)}")
        except Exception as e:
            print(f"Exception occurred: {str(e)}")

    print(f"Freed up {format_size(size)}")


def dry_run(directories: list[Path]) -> None:
    for directory in directories:
        print(directory)


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean folders from directories")

    parser.add_argument("root", help="Target directory")
    parser.add_argument(
        "--target", "-t", default="node_modules", help="Folder name to sweep"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Display folders' location to sweep"
    )
    parser.add_argument(
        "--yes", "-y", action="store_true", help="Delete all found locations"
    )

    args = parser.parse_args()
    # print(args)
    # print(locations)

    locations = find_dirs(args.target, args.root)
    if not locations:
        print(f"No {args.target} folders found in {args.root}")
        return

    # for location in locations:
    #     print(str(location))

    if args.dry_run:
        dry_run(locations)
    else:
        clean(locations, args.yes)


if __name__ == "__main__":
    main()
