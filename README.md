# Sweep

![Python Version](https://img.shields.io/badge/python-3.14+-blue)
![GitHub release](https://img.shields.io/github/v/release/JourneyCodesAyush/sweep?sort=semver)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey)

**Sweep** is a minimal, Windows-focused Python CLI tool to recursively find and delete unwanted folders (like `node_modules`) from a target drive or directory.

> Scans your drives, shows you what it finds, and cleans it up - safely and with your confirmation.

> [!WARNING]
> `sweep` deletes folders permanently using `shutil.rmtree()`. Always use `--dry-run` first if you're unsure.

---

## Quick Start

Run as a Python module or install as a CLI command.

```powershell
git clone https://github.com/JourneyCodesAyush/sweep.git
cd sweep

# (Optional but recommended) create a virtual environment
python -m venv .venv
# or
uv venv .venv

# Activate the virtual environment

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Windows (cmd)
.\.venv\Scripts\activate.bat

# macOS / Linux (bash/zsh)
source .venv/bin/activate

# Install as a CLI command
uv pip install -e . --link-mode=copy

# Use it
sweep D:\ --dry-run
```

> [!NOTE]
> Installing in editable mode (`-e`) exposes sweep as a command in your current environment (via PATH).
> The `--link-mode=copy` flag ensures proper behavior on Windows.

### Or run without installing

```powershell
uv run python -m sweep D:\ --dry-run
```

---

## Features

- Recursively searches a target drive or directory
- Targets `node_modules` by default - configurable via `--target`
- Shows a summary of found folders grouped by target before acting
- `--target` accepts multiple folder names in one run
- `--exclude` / `-e` flag to skip specific directories during search
- Per-folder confirmation prompt with `[Y]es/[A]ll/[N]o` options
- `--yes` flag to skip confirmation entirely
- `--dry-run` flag to preview without deleting anything
- Warns before sweeping dangerous targets like `.git`
- Displays total disk space freed after deletion
- Colored terminal output for better DX
- `--version` flag to display current installed version
- Graceful handling of permission errors and unexpected failures
- No third-party dependencies - stdlib only

---

## Dangerous Targets

When targeting directories like `.git`, sweep will warn you before proceeding:

```txt
Warning: .git are dangerous targets and deletion may be irreversible.
Are you sure you want to proceed? [Y]es/[N]o:
```

| Input         | Behaviour                                         |
| ------------- | ------------------------------------------------- |
| `y`           | Proceed with all targets including dangerous ones |
| `n`           | Remove dangerous targets, continue with safe ones |
| anything else | Exit with invalid input message                   |

---

## Supported Platforms

- Windows 10 / 11 (tested)
- macOS / Linux (should work, not fully tested)

> [!NOTE]
> Sweep relies only on Python's standard library, so it is expected to work cross-platform.

---

## Usage

```
usage: sweep [-h] [--target TARGET [TARGET ...]] [--exclude EXCLUDE [EXCLUDE ...]] [--dry-run] [--yes] root

positional arguments:
  root                    Target drive or directory (e.g. D:\)

options:
  -h, --help              show this help message and exit
  --dry-run               Display folders without deleting
  --yes, -y               Skip confirmation and delete all found folders
  --target, -t TARGET [TARGET ...]  Folder names to sweep (default: node_modules)
  --exclude, -e EXCLUDE [EXCLUDE ...] Paths to exclude during search
```

### Examples

> [!NOTE]
> The following examples assume `sweep` is installed as a CLI command.
> Otherwise, prefix commands with `python -m sweep`.

```powershell
# Show installed version
sweep --version

# Preview what would be deleted
sweep D:\ --dry-run

# Clean node_modules with per-folder confirmation
sweep D:\

# Clean node_modules without confirmation
sweep D:\ --yes

# Clean a different folder type
sweep D:\ --target __pycache__

# Combine flags
sweep D:\ --target .git --dry-run

# Sweep multiple targets at once
sweep D:\ --target node_modules __pycache__

# Exclude specific directories
sweep D:\ --exclude D:\Important

# Combine everything
sweep D:\ --target node_modules .venv --exclude D:\Work --dry-run
```

> [!TIP]
> Always run with `--dry-run` first to see what will be deleted before committing.

---

## Confirmation Prompt

When running without `--yes`, sweep asks for confirmation before each deletion:

```
Delete D:\Projects\my-app\node_modules [Y]es/[A]ll/[N]o:
```

| Input                  | Behaviour                             |
| ---------------------- | ------------------------------------- |
| `y`                    | Delete this folder only               |
| `a`                    | Delete this and all remaining folders |
| `n` (or anything else) | Skip this folder                      |

---

## Scope

Sweep is intentionally small in scope:

- No logging to file
- Not explicitly tested on Linux / macOS (but designed to be cross-platform)

---

## Philosophy

Sweep is about **safe, explicit cleanup** - it never deletes anything without telling you first, and `--dry-run` is always available. The goal is a tool that's fast, transparent, and trustworthy.

---

## License

This project is licensed under the [**MIT License**](./LICENSE).

You're free to use, modify, and distribute it.

> [!TIP]
> A tag or mention of [JourneyCodesAyush](https://github.com/JourneyCodesAyush) is always appreciated.
