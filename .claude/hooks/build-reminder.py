#!/usr/bin/env python3
"""
Build reminder advisory PostToolUse hook.

Fires after Edit/Write/MultiEdit to a theme .sty file and injects a NON-BLOCKING
advisory reminding to recompile that theme's sample PDF so the committed preview
stays in sync with the source. Advisory only — never blocks; injects via
hookSpecificOutput.additionalContext so the reminder reaches the model's next
turn. Per-session dedup (5-minute window) avoids re-warning on the same theme.

Mirrors the emit/dedup pattern of derive-check-advisory.py in claude-code-my-workflow.

Install (in .claude/settings.json, PostToolUse, matcher "Write|Edit|MultiEdit"):
    python3 "$CLAUDE_PROJECT_DIR"/.claude/hooks/build-reminder.py

Fail-open on any internal exception (exit 0, no output).
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

# Theme source directory -> build.sh target for that theme's sample.
THEME_TARGETS = {
    "ucdavis_beamer_theme_xelatex": "ucdavis-xe",
    "ucdavis_beamer_theme_pdflatex": "ucdavis-pdf",
    "ca_ed_lab_beamer_theme": "caedlab",
}


def _session_cache_path(project_dir: str) -> Path:
    project_hash = hashlib.md5(project_dir.encode()).hexdigest()[:8]
    d = Path.home() / ".claude" / "sessions" / project_hash
    d.mkdir(parents=True, exist_ok=True)
    return d / "build-reminder-cache.json"


def _already_warned(cache_file: Path, target: str) -> bool:
    """True if this theme was warned within the last 5 minutes; record otherwise."""
    now = time.time()
    try:
        cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    except (json.JSONDecodeError, OSError):
        cache = {}
    cache = {k: v for k, v in cache.items() if now - v < 300}

    warned = now - cache.get(target, 0) < 300
    cache[target] = now
    try:
        cache_file.write_text(json.dumps(cache))
    except OSError:
        pass
    return warned


def _emit(additional_context: str) -> None:
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": additional_context,
        },
        "suppressOutput": True,
    }
    sys.stdout.write(json.dumps(payload))
    sys.stdout.flush()


def _theme_for_path(file_path: str, project_root: Path) -> str | None:
    """Return the build target if file_path is a .sty under a known theme dir."""
    if not file_path.endswith(".sty"):
        return None
    try:
        rel = Path(file_path).resolve().relative_to(project_root.resolve())
    except (ValueError, OSError):
        return None
    parts = rel.parts
    if not parts:
        return None
    return THEME_TARGETS.get(parts[0])


def main() -> None:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    if hook_input.get("tool_name", "") not in {"Edit", "Write", "MultiEdit"}:
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path", "") or ""
    if not file_path:
        sys.exit(0)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", hook_input.get("cwd", ""))
    if not project_dir:
        sys.exit(0)
    project_root = Path(project_dir)

    target = _theme_for_path(file_path, project_root)
    if target is None:
        sys.exit(0)

    cache_file = _session_cache_path(project_dir)
    if _already_warned(cache_file, target):
        sys.exit(0)

    _emit(
        f"You edited a .sty in the '{target}' theme. The committed preview PDF is "
        f"now out of sync. Before finishing, recompile it with: "
        f"scripts/build.sh {target}  (then eyeball the regenerated *_theme_test.pdf)."
    )
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
