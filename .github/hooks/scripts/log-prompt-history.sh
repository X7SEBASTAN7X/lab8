#!/usr/bin/env python3
"""
Hook: log-prompt-history.sh
Event: UserPromptSubmit
Purpose: Append the user prompt to prompts_history.md and JOURNAL.md
using the journal logger template.

This file intentionally keeps the original .sh name for existing hook references,
but it is implemented in Python for cross-platform compatibility.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Internal version (increment on each edit): X.YZ
VERSION = "1.03"
JOURNAL_AGENT_VERSION = "2.2"

# Toggle local transcript copy (original filename is preserved).
ENABLE_LOCAL_TRANSCRIPT_COPY = False

# Destination folder under repo root when transcript copy is enabled.
LOCAL_TRANSCRIPT_COPY_DIR = Path("tmp") / "transcripts"


def get_repo_root(script_dir: Path) -> Path:
  try:
    output = subprocess.check_output(
      ["git", "-C", str(script_dir), "rev-parse", "--show-toplevel"],
      stderr=subprocess.DEVNULL,
      text=True,
    ).strip()
    if output:
      return Path(output)
  except Exception:
    pass
  return Path.cwd()


def parse_payload(stdin_text: str) -> dict:
  try:
    payload = json.loads(stdin_text)
    if isinstance(payload, dict):
      return payload
  except Exception:
    pass
  return {}


def get_user_identity(repo_root: Path) -> str:
  for key in ["user.email", "user.name"]:
    try:
      value = subprocess.check_output(
        ["git", "-C", str(repo_root), "config", key],
        stderr=subprocess.DEVNULL,
        text=True,
      ).strip()
      if value:
        return value
    except Exception:
      pass

  return "default_user"


def normalize_prompt(prompt: str) -> str:
  return prompt if prompt.strip() else "unknown"


def sanitize_prompt_for_history(prompt: str) -> str:
  return " ".join(prompt.splitlines()).strip() or "unknown"


def get_payload_string(payload: dict, keys: list[str], fallback: str = "unknown") -> str:
  for key in keys:
    value = payload.get(key)
    if isinstance(value, str) and value.strip():
      return value.strip()
  return fallback


def get_copilot_mode(payload: dict) -> str:
  mode = get_payload_string(
    payload,
    ["copilot_mode", "mode", "chat_mode", "session_mode"],
    fallback="Agent",
  )
  normalized = mode.lower()
  allowed = {
    "ask": "Ask",
    "plan": "Plan",
    "edit": "Edit",
    "agent": "Agent",
  }
  return allowed.get(normalized, "Agent")


def get_model_name(payload: dict) -> str:
  return get_payload_string(
    payload,
    ["copilot_model", "model", "model_name", "runtime_model"],
    fallback="GPT-5.3-Codex",
  )


def ensure_history_file(history_file: Path) -> None:
  if history_file.exists():
    return

  history_file.write_text(
    "# Prompts History\n\n"
    "Automatically captured prompt log. Entries are appended in chronological order (oldest first).\n\n",
    encoding="utf-8",
  )


def append_entry(history_file: Path, entry: str) -> None:
  with history_file.open("a", encoding="utf-8") as handle:
    handle.write(entry)


def ensure_journal_file(journal_file: Path) -> None:
  if journal_file.exists():
    return

  journal_file.write_text(
    "# This Journal gets updated automatically by the Journal Logger Agent\n\n",
    encoding="utf-8",
  )


def maybe_copy_transcript(transcript_path: Path, repo_root: Path) -> None:
  if not ENABLE_LOCAL_TRANSCRIPT_COPY:
    return

  if not transcript_path.is_file():
    return

  destination_dir = repo_root / LOCAL_TRANSCRIPT_COPY_DIR
  destination_dir.mkdir(parents=True, exist_ok=True)
  destination_path = destination_dir / transcript_path.name
  shutil.copy2(transcript_path, destination_path)


def safe_git_commit(repo_root: Path, files_to_add: list[Path], timestamp: str) -> None:
  try:
    for file_path in files_to_add:
      subprocess.run(
        ["git", "-C", str(repo_root), "add", str(file_path)],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
      )
    subprocess.run(
      [
        "git",
        "-C",
        str(repo_root),
        "commit",
        "-m",
        f"chore: log prompt [{timestamp}]",
        "--no-verify",
        "-q",
      ],
      check=False,
      stdout=subprocess.DEVNULL,
      stderr=subprocess.DEVNULL,
    )
  except Exception:
    pass


def main() -> int:
  try:
    script_dir = Path(__file__).resolve().parent
    repo_root = get_repo_root(script_dir)
    history_file = repo_root / "prompts_history.md"
    journal_file = repo_root / "JOURNAL.md"

    stdin_text = sys.stdin.read()
    payload = parse_payload(stdin_text)

    prompt_raw = str(payload.get("prompt", "unknown"))
    prompt = normalize_prompt(prompt_raw)
    prompt_for_history = sanitize_prompt_for_history(prompt)
    transcript_path_raw = str(payload.get("transcript_path", "")).strip()
    transcript_path = Path(transcript_path_raw) if transcript_path_raw else Path()

    timestamp_history = datetime.now().strftime("%d-%m-%Y %H:%M")
    timestamp_journal = datetime.now().strftime("%d-%m-%Y %H:%M")
    user_identity = get_user_identity(repo_root)
    copilot_mode = get_copilot_mode(payload)
    model_name = get_model_name(payload)
    socratic_mode = "ON"

    maybe_copy_transcript(transcript_path, repo_root)
    ensure_history_file(history_file)
    ensure_journal_file(journal_file)

    history_entry = (
      f"### {timestamp_history}\n"
      f"- **Prompt**: {prompt_for_history}\n\n"
    )

    journal_entry = (
      "\n### **New Interaction**\n"
      f"- **Agent Version**: {JOURNAL_AGENT_VERSION}\n"
      f"- **Date**: {timestamp_journal}\n"
      f"- **User**: {user_identity}\n"
      f"- **Prompt**: {prompt}\n"
      f"- **CoPilot Mode**: {copilot_mode}\n"
      f"- **CoPilot Model**: {model_name}\n"
      f"- **Socratic Mode**: {socratic_mode}\n"
      "- **Changes Made**: Automated prompt capture entry appended; no file edits performed by this hook.\n"
      "- **Context and Reasons for Changes**: Maintains chronological interaction logging for traceability and compliance with repo instructions.\n"
    )

    append_entry(history_file, history_entry)
    append_entry(journal_file, journal_entry)
    safe_git_commit(repo_root, [history_file, journal_file], timestamp_history)
  except Exception:
    # Non-blocking hook by design.
    return 0

  return 0


if __name__ == "__main__":
  sys.exit(main())
