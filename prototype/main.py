import os
from pathlib import Path
import shutil

import argparse


def find_dirs(search: str, root: str) -> list[Path]:
    results = []

    for current, dirs, _ in os.walk(root):
        if search in dirs:
            found = Path(current) / search
            results.append(found)

            dirs.remove(search)

    return results


def clean(directories: list[Path]) -> None:
    for directory in directories:
        print(f"Removing {str(directory)}...")
        shutil.rmtree(directory)


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
        clean(locations)


if __name__ == "__main__":
    main()
