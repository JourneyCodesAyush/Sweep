# `sweep` Philosophy

`sweep` is intentionally minimal. It exists to solve **one simple problem**: recursively finding and deleting named folders (like `node_modules`) from a target directory, safely and with your confirmation.

## Design Principles

### 1. Cross-platform by default

- Built and tested on Windows 10+ by a Windows user.
- Since `sweep` relies purely on Python's stdlib (`os`, `pathlib`, `shutil`),
  it is cross-platform by default.
- Linux and macOS compatibility has not been explicitly tested, but should work.

### 2. Folder-level only

- `sweep` targets **folders by name**, not individual files.
- It does not uninstall programs, clean residual files, or touch system directories.

### 3. Safety first

- Nothing is deleted without showing you what will be removed.
- `--dry-run` is always available to preview before committing.
- `--yes` exists for power users who know what they're doing.

### 4. Explicit over automatic

- `sweep` never assumes. It asks.
- The `[Y]es/[A]ll/[N]o` prompt gives you full control over every deletion.

### 5. Minimalism

- Zero third-party runtime dependencies - stdlib only.
- One file, one purpose.

### 6. Dumb by design

- `sweep` does not make decisions for you.
- It finds folders, tells you what it found, and waits for your input.
- **You have total control over your system.**

## What `sweep` is **NOT**

- A program uninstaller
- A residual file cleaner
- A system-level cleanup tool
- A general-purpose file manager
- A smart or automated cleanup tool - it does exactly what you tell it to, nothing more.

`sweep` is for **named folder cleanup**. It prioritizes **safety, transparency, and simplicity** over automation or scope creep.
