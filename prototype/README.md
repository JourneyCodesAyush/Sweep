# Sweep

![Python Version](https://img.shields.io/badge/python-3.14+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey)

**Sweep** is a minimal, Windows-focused Python CLI tool to recursively find and delete unwanted folders (like `node_modules`) from a target drive or directory.

> Scans your drives, shows you what it finds, and cleans it up - safely and with your confirmation.

> [!WARNING]
> `sweep` deletes folders permanently using `shutil.rmtree()`. Always use `--dry-run` first if you're unsure.

---

## Quick Start

```powershell
git clone https://github.com/JourneyCodesAyush/sweep.git
cd sweep

# Using uv (recommended)
uv run prototype/main.py D:\ --dry-run

# Or with plain Python
python prototype/main.py D:\ --dry-run
```

---

## Features

- Recursively searches a target drive or directory
- Targets `node_modules` by default - configurable via `--target`
- Per-folder confirmation prompt with `[Y]es/[A]ll/[N]o` options
- `--yes` flag to skip confirmation entirely
- `--dry-run` flag to preview without deleting anything
- Graceful handling of permission errors and unexpected failures
- No third-party dependencies - stdlib only

---

## Supported Platforms

- Windows 10 / 11
- Windows-focused by design (for now)

> [!NOTE]
> Only tested on Windows

---

## Installation

> [!NOTE]
> `sweep` is currently a Python prototype

1. Clone the repository:

   ```powershell
   git clone https://github.com/JourneyCodesAyush/sweep.git
   cd sweep
   ```

2. Run directly with `uv`:

   ```powershell
   uv run prototype/main.py <path> [options]
   ```

   Or with plain Python (3.14+):

   ```powershell
   python prototype/main.py <path> [options]
   ```

---

## Usage

```
usage: main.py [-h] [--target TARGET] [--dry-run] [--yes] root

positional arguments:
  root                    Target drive or directory (e.g. D:\)

options:
  -h, --help              show this help message and exit
  --target, -t TARGET     Folder name to sweep (default: node_modules)
  --dry-run               Display folders without deleting
  --yes, -y               Skip confirmation and delete all found folders
```

### Examples

```powershell
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
- No multiple targets in one run
- No cross-platform support
- Windows-focused by design

---

## Philosophy

Sweep is about **safe, explicit cleanup** - it never deletes anything without telling you first, and `--dry-run` is always available. The goal is a tool that's fast, transparent, and trustworthy.

---

## License

This project is licensed under the [**MIT License**](../LICENSE).

You're free to use, modify, and distribute it.

> [!TIP]
> A tag or mention of [JourneyCodesAyush](https://github.com/JourneyCodesAyush) is always appreciated.
