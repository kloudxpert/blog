#!/usr/bin/env python3
"""Generate a complete gcloud command index from the installed Google Cloud CLI."""

from __future__ import annotations

import datetime as dt
import pathlib
import subprocess
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "commands"
OFFICIAL_REFERENCE = "https://cloud.google.com/sdk/gcloud/reference"
TICK = chr(96)


def run(*args: str) -> str:
    proc = subprocess.run(
        args,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"Command failed ({proc.returncode}): {' '.join(args)}\n{proc.stderr.strip()}"
        )
    return proc.stdout


def get_version() -> str:
    text = run("gcloud", "version")
    return next((line.strip() for line in text.splitlines() if line.strip()), "unknown")


def list_commands() -> list[str]:
    raw = run("gcloud", "meta", "list-commands")
    commands: set[str] = set()

    for line in raw.splitlines():
        line = line.strip()
        if not line.startswith("gcloud"):
            continue
        line = line.split("\t", 1)[0].strip()
        if " - " in line:
            line = line.split(" - ", 1)[0].strip()
        commands.add(line)

    if not commands:
        raise RuntimeError(
            "gcloud meta list-commands returned no command paths. "
            "Check the installed Google Cloud CLI version."
        )

    return sorted(commands)


def split_tracks(commands: list[str]) -> dict[str, list[str]]:
    tracks: dict[str, list[str]] = defaultdict(list)
    for command in commands:
        parts = command.split()
        if len(parts) > 1 and parts[1] == "alpha":
            tracks["alpha"].append(command)
        elif len(parts) > 1 and parts[1] == "beta":
            tracks["beta"].append(command)
        else:
            tracks["ga"].append(command)
    return tracks


def group_key(command: str, track: str) -> str:
    parts = command.split()
    offset = 2 if track in {"alpha", "beta"} else 1
    return parts[offset] if len(parts) > offset else "(root)"


def render(track: str, commands: list[str], version: str, generated: str) -> str:
    label = {"ga": "GA", "beta": "Beta", "alpha": "Alpha"}[track]
    lines = [
        f"# Complete gcloud {label} Command Index",
        "",
        f"> Generated: **{generated}**  ",
        f"> CLI: **{version}**  ",
        f"> Source: installed Google Cloud CLI via {TICK}gcloud meta list-commands{TICK}",
        "",
        "This is a generated snapshot. Commands can move between release tracks or change as the CLI evolves.",
        "",
        f"Official reference: {OFFICIAL_REFERENCE}",
        "",
        f"**Commands in this snapshot: {len(commands):,}**",
        "",
    ]

    grouped: dict[str, list[str]] = defaultdict(list)
    for command in commands:
        grouped[group_key(command, track)].append(command)

    for group in sorted(grouped):
        lines.append(f"## {group}")
        lines.append("")
        for command in grouped[group]:
            lines.append(f"- {TICK}{command}{TICK}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    version = get_version()
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    commands = list_commands()
    tracks = split_tracks(commands)

    for track in ("ga", "beta", "alpha"):
        path = OUT_DIR / f"gcloud-{track}.md"
        path.write_text(
            render(track, tracks.get(track, []), version, generated),
            encoding="utf-8",
        )
        print(f"Wrote {path} ({len(tracks.get(track, []))} commands)")

    summary = OUT_DIR / "README.md"
    summary.write_text(
        "# Generated gcloud Command Indexes\n\n"
        f"Generated: **{generated}**  \n"
        f"CLI: **{version}**\n\n"
        f"- [GA](gcloud-ga.md) — {len(tracks.get('ga', [])):,} commands\n"
        f"- [Beta](gcloud-beta.md) — {len(tracks.get('beta', [])):,} commands\n"
        f"- [Alpha](gcloud-alpha.md) — {len(tracks.get('alpha', [])):,} commands\n\n"
        "For command-specific syntax, use gcloud COMMAND --help or the "
        f"[official reference]({OFFICIAL_REFERENCE}).\n",
        encoding="utf-8",
    )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
