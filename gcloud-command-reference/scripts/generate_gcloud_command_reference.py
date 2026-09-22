#!/usr/bin/env python3
"""Generate searchable gcloud command references with a short explanation for every command.

The command inventory and descriptions come from the installed Google Cloud CLI.
This keeps the reference tied to a real CLI release instead of a hand-maintained list.
"""

from __future__ import annotations

import datetime as dt
import os
import pathlib
import re
import shlex
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "commands"
OFFICIAL_REFERENCE = "https://cloud.google.com/sdk/gcloud/reference"
TICK = chr(96)
TRACKS = ("ga", "beta", "alpha", "preview")
MAX_WORKERS = int(os.environ.get("GCLOUD_DOC_WORKERS", "10"))


def run(args: list[str], timeout: int = 120) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["CLOUDSDK_CORE_DISABLE_PROMPTS"] = "1"
    return subprocess.run(
        args,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        timeout=timeout,
    )


def require_output(args: list[str], timeout: int = 120) -> str:
    proc = run(args, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(
            f"Command failed ({proc.returncode}): {' '.join(args)}\n{proc.stderr.strip()}"
        )
    return proc.stdout


def get_version() -> str:
    text = require_output(["gcloud", "version"])
    return next((line.strip() for line in text.splitlines() if line.strip()), "unknown")


def list_commands() -> list[str]:
    raw = require_output(["gcloud", "meta", "list-commands"], timeout=300)
    commands: set[str] = set()

    for line in raw.splitlines():
        line = line.strip()
        if not line.startswith("gcloud"):
            continue

        line = line.split("\t", 1)[0].strip()
        if " - " in line:
            line = line.split(" - ", 1)[0].strip()

        # Keep command paths only; ignore examples or malformed output.
        if re.fullmatch(r"gcloud(?: [A-Za-z0-9_.:-]+)+", line):
            commands.add(line)

    if not commands:
        raise RuntimeError(
            "gcloud meta list-commands returned no command paths. "
            "Check the installed Google Cloud CLI version."
        )

    return sorted(commands)


def extract_summary(help_text: str, command: str) -> str:
    lines = help_text.splitlines()

    # gcloud help pages normally expose the best one-line summary in NAME:
    #
    # NAME
    #     gcloud compute instances list - list Google Compute Engine instances
    try:
        name_index = next(i for i, line in enumerate(lines) if line.strip() == "NAME")
        for line in lines[name_index + 1 : name_index + 8]:
            cleaned = " ".join(line.strip().split())
            if not cleaned:
                continue
            if " - " in cleaned:
                _, summary = cleaned.split(" - ", 1)
                if summary.strip():
                    return summary.strip().rstrip(".") + "."
    except StopIteration:
        pass

    # Fall back to the first paragraph in DESCRIPTION.
    try:
        desc_index = next(i for i, line in enumerate(lines) if line.strip() == "DESCRIPTION")
        paragraph: list[str] = []
        for line in lines[desc_index + 1 :]:
            stripped = line.strip()
            if not stripped:
                if paragraph:
                    break
                continue
            if stripped in {
                "EXAMPLES",
                "POSITIONAL ARGUMENTS",
                "FLAGS",
                "REQUIRED FLAGS",
                "OPTIONAL FLAGS",
                "GCLOUD WIDE FLAGS",
                "NOTES",
            }:
                break
            paragraph.append(stripped)

        if paragraph:
            summary = " ".join(paragraph)
            summary = re.sub(r"\s+", " ", summary).strip()
            if len(summary) > 320:
                summary = summary[:317].rsplit(" ", 1)[0] + "..."
            return summary
    except StopIteration:
        pass

    return f"Run {command} --help for this command's description and arguments."


def describe_command(command: str) -> tuple[str, str]:
    args = shlex.split(command) + ["--help"]
    try:
        proc = run(args, timeout=90)
        text = proc.stdout or proc.stderr
        if proc.returncode == 0 and text.strip():
            return command, extract_summary(text, command)
        return command, f"Help was unavailable while generating this snapshot. Run {command} --help locally."
    except Exception as exc:
        return command, f"Description generation failed ({type(exc).__name__}). Run {command} --help locally."


def split_tracks(commands: list[str]) -> dict[str, list[str]]:
    tracks: dict[str, list[str]] = defaultdict(list)
    for command in commands:
        parts = command.split()
        if len(parts) > 1 and parts[1] in {"alpha", "beta", "preview"}:
            tracks[parts[1]].append(command)
        else:
            tracks["ga"].append(command)
    return tracks


def group_key(command: str, track: str) -> str:
    parts = command.split()
    offset = 2 if track in {"alpha", "beta", "preview"} else 1
    return parts[offset] if len(parts) > offset else "(root)"


def render(
    track: str,
    commands: list[str],
    descriptions: dict[str, str],
    version: str,
    generated: str,
) -> str:
    label = {
        "ga": "GA",
        "beta": "Beta",
        "alpha": "Alpha",
        "preview": "Preview",
    }[track]

    lines = [
        f"# Complete gcloud {label} Command Reference",
        "",
        f"> Generated: **{generated}**  ",
        f"> CLI: **{version}**  ",
        f"> Source: installed Google Cloud CLI command tree and built-in {TICK}--help{TICK} text",
        "",
        "Each entry includes the command and a short explanation taken from the same installed CLI release.",
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
            lines.append(f"### {TICK}{command}{TICK}")
            lines.append("")
            lines.append(f"**What it does:** {descriptions.get(command, 'Description unavailable.')}")
            lines.append("")
            lines.append(f"**Usage help:** {TICK}{command} --help{TICK}")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    version = get_version()
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    commands = list_commands()
    tracks = split_tracks(commands)

    print(f"Found {len(commands):,} gcloud commands. Reading built-in help text...")

    descriptions: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(describe_command, cmd): cmd for cmd in commands}
        completed = 0
        for future in as_completed(futures):
            command, summary = future.result()
            descriptions[command] = summary
            completed += 1
            if completed % 100 == 0 or completed == len(commands):
                print(f"Documented {completed:,}/{len(commands):,} commands")

    for track in TRACKS:
        track_commands = tracks.get(track, [])
        path = OUT_DIR / f"gcloud-{track}.md"
        path.write_text(
            render(track, track_commands, descriptions, version, generated),
            encoding="utf-8",
        )
        print(f"Wrote {path} ({len(track_commands):,} commands)")

    summary = OUT_DIR / "README.md"
    summary.write_text(
        "# Generated gcloud Command References\n\n"
        f"Generated: **{generated}**  \n"
        f"CLI: **{version}**\n\n"
        "Every command entry includes a short 'What it does' explanation derived "
        "from the built-in help for this CLI release.\n\n"
        f"- [GA](gcloud-ga.md) — {len(tracks.get('ga', [])):,} commands\n"
        f"- [Beta](gcloud-beta.md) — {len(tracks.get('beta', [])):,} commands\n"
        f"- [Alpha](gcloud-alpha.md) — {len(tracks.get('alpha', [])):,} commands\n"
        f"- [Preview](gcloud-preview.md) — {len(tracks.get('preview', [])):,} commands\n\n"
        "For full syntax and flags, use gcloud COMMAND --help or the "
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
