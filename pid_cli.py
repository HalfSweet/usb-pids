#!/usr/bin/env python3
"""
Utility CLI for managing OpenSiFli USB PIDs.

Features:
1. List all allocated PIDs.
2. Assign a random PID within the SF32 range (0x9000-0xAFFF) and scaffold index.toml.
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import tomllib

PID_DIR = Path("pid")
PID_RANGE_START = 0x9000
PID_RANGE_END = 0xAFFF
INDEX_FILENAME = "index.toml"
INDEX_FIELDS = ["title", "desc", "owner", "license", "homepage", "repository"]


def load_toml(path: Path) -> Dict[str, str]:
    """Load TOML file using stdlib tomllib."""
    with path.open("rb") as fp:
        return dict(tomllib.load(fp))


def iter_pid_entries(pid_root: Path) -> Iterable[Tuple[str, Path]]:
    """Yield (pid_slug, directory) for each PID entry directory."""
    if not pid_root.exists():
        return
    for entry in sorted(pid_root.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue
        yield entry.name, entry


def read_title(entry_dir: Path) -> str:
    """Return title from index.toml or placeholder."""
    index_path = entry_dir / INDEX_FILENAME
    if not index_path.exists():
        return "<missing index.toml>"
    try:
        data = load_toml(index_path)
    except Exception as exc:  # pragma: no cover - defensive path
        return f"<error reading index.toml: {exc}>"
    title = data.get("title")
    return str(title) if title else "<missing title>"


def format_pid(pid_name: str) -> str:
    """Normalize PID directory name to hex representation with 0x prefix."""
    if pid_name.lower().startswith("0x"):
        pid_name = pid_name[2:]
    try:
        value = int(pid_name, 16)
    except ValueError:
        return pid_name
    return f"0x{value:04X}"


def list_pids(pid_root: Path) -> None:
    """Print all allocated PIDs."""
    entries = list(iter_pid_entries(pid_root))
    if not entries:
        print("No PID entries found.")
        return

    for idx, (pid_slug, entry_dir) in enumerate(entries, start=1):
        display_pid = format_pid(pid_slug)
        title = read_title(entry_dir)
        print(f"{idx}. pid: {display_pid}, title: {title}")


def collect_used_pids(pid_root: Path) -> Dict[int, Path]:
    """Return mapping of integer PID value to directory Path."""
    used: Dict[int, Path] = {}
    for pid_slug, entry_dir in iter_pid_entries(pid_root):
        slug = pid_slug.lower()
        if slug.startswith("0x"):
            slug = slug[2:]
        try:
            pid_value = int(slug, 16)
        except ValueError:
            continue
        used[pid_value] = entry_dir
    return used


def choose_random_pid(used: Dict[int, Path]) -> Optional[int]:
    """Select a random unused PID within allowed range."""
    available = [
        pid for pid in range(PID_RANGE_START, PID_RANGE_END + 1) if pid not in used
    ]
    if not available:
        return None
    return random.choice(available)


def prompt_field(field: str) -> str:
    """Prompt user for a field value."""
    prompt = f"{field} ({'required' if field != 'homepage' and field != 'repository' else 'optional'}): "
    try:
        value = input(prompt).strip()
    except EOFError:
        print("\nInput interrupted.", file=sys.stderr)
        sys.exit(1)
    return value


def ensure_repo_root() -> Path:
    """Ensure script runs from repository root by checking PID_DIR."""
    root = Path.cwd()
    if not (root / PID_DIR).exists():
        print(
            f"Cannot find '{PID_DIR}' directory. Please run this script from the repository root.",
            file=sys.stderr,
        )
        sys.exit(1)
    return root


def write_index_file(target_dir: Path, field_values: Dict[str, str]) -> None:
    """Write index.toml with collected values."""
    index_path = target_dir / INDEX_FILENAME
    lines = []
    for key in INDEX_FIELDS:
        value = field_values.get(key, "")
        escaped = value.replace('"', '\\"')
        lines.append(f'{key} = "{escaped}"\n')
    index_path.write_text("".join(lines), encoding="utf-8")


def normalize_pid_input(pid_text: str) -> Optional[int]:
    """Parse user-provided PID string in 0x____ format."""
    text = pid_text.strip()
    if len(text) < 3 or not text.lower().startswith("0x"):
        return None
    try:
        value = int(text[2:], 16)
    except ValueError:
        return None
    if value < 0 or value > 0xFFFF:
        return None
    return value


def assign_pid(pid_root: Path, requested_pid: Optional[str]) -> None:
    """Assign PID (manual or random) and scaffold index.toml."""
    used = collect_used_pids(pid_root)

    selected: Optional[int] = None
    if requested_pid:
        value = normalize_pid_input(requested_pid)
        if value is None:
            print(
                "Invalid PID format. Please provide a 0x-prefixed hexadecimal number.",
                file=sys.stderr,
            )
            return
        if not (PID_RANGE_START <= value <= PID_RANGE_END):
            print(
                f"PID must be within 0x{PID_RANGE_START:04X}-0x{PID_RANGE_END:04X}.",
                file=sys.stderr,
            )
            return
        if value in used:
            print(
                f"PID 0x{value:04X} is already allocated at {used[value]}.",
                file=sys.stderr,
            )
            return
        selected = value
    else:
        selected = choose_random_pid(used)
        if selected is None:
            print("No available PIDs in range 0x9000-0xAFFF.")
            return

    pid_slug = f"0x{selected:04X}"
    target_dir = pid_root / pid_slug

    if target_dir.exists():
        print(
            f"Selected PID directory '{target_dir}' already exists. Please rerun the command.",
            file=sys.stderr,
        )
        return

    print(f"Assigned PID: {pid_slug}")
    print("Please provide project details for index.toml.")

    field_values: Dict[str, str] = {}
    for field in INDEX_FIELDS:
        value = prompt_field(field)
        field_values[field] = value

    target_dir.mkdir(parents=True, exist_ok=False)
    write_index_file(target_dir, field_values)

    print(f"Created directory: {target_dir}")
    print(f"Created {INDEX_FILENAME} with supplied values.")
    print("Remember to add up to two PNG images if desired.")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="OpenSiFli USB PID management CLI.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List all allocated PIDs.")
    assign_parser = subparsers.add_parser(
        "assign", help="Assign a random PID or use --pid to set a specific one."
    )
    assign_parser.add_argument(
        "--pid",
        dest="pid",
        help="Specify a 0x-prefixed hexadecimal PID within 0x9000-0xAFFF.",
    )

    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    ensure_repo_root()
    pid_root = PID_DIR

    if args.command == "list":
        list_pids(pid_root)
    elif args.command == "assign":
        assign_pid(pid_root, getattr(args, "pid", None))
    else:  # pragma: no cover - defensive
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
