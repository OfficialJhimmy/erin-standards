#!/usr/bin/env python3
"""PreToolUse hook (matcher: Bash): validates that `git commit` messages
follow Conventional Commits (type(scope): description). Blocks the commit
if the message clearly doesn't match. Fails open (allows the command)
whenever the message can't be confidently extracted, since a false block
on a real commit is worse than an occasional miss.
"""
import json
import re
import sys

COMMIT_TYPES = (
    "feat", "fix", "chore", "refactor", "docs", "test", "style", "perf", "build", "ci"
)
CONVENTIONAL_RE = re.compile(
    r"^(" + "|".join(COMMIT_TYPES) + r")(\([\w./-]+\))?!?: .{1,72}$"
)


def extract_command(payload):
    return payload.get("tool_input", {}).get("command", "") or ""


def is_git_commit(command):
    return bool(re.search(r"\bgit\s+commit\b", command))


def extract_message(command):
    # Heredoc pattern: git commit -m "$(cat <<'EOF' ... EOF)", take the
    # first non-empty line inside the heredoc.
    heredoc = re.search(r"<<['\"]?EOF['\"]?\s*\n(.*?)\nEOF", command, re.S)
    if heredoc:
        lines = [l for l in heredoc.group(1).splitlines() if l.strip()]
        if lines:
            return lines[0].strip()

    # Simple -m "message" or -m 'message' pattern (first occurrence only,
    # commit body via a second -m isn't the part we validate).
    m = re.search(r"-m\s+(\"([^\"]+)\"|'([^']+)')", command)
    if m:
        msg = m.group(2) or m.group(3) or ""
        return msg.splitlines()[0].strip() if msg else ""

    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    command = extract_command(payload)
    if not command or not is_git_commit(command):
        sys.exit(0)

    if "--amend" in command and "-m" not in command and "-F" not in command:
        sys.exit(0)  # amending without changing the message, nothing to check

    message = extract_message(command)
    if not message:
        sys.exit(0)  # couldn't confidently extract it, don't block on a guess

    if CONVENTIONAL_RE.match(message):
        sys.exit(0)

    print(
        "Commit message doesn't follow Conventional Commits: "
        f"\"{message}\"\n"
        "Expected format: type(scope): description, e.g. "
        "\"feat(rate-card): add site mapping tab\" or \"fix(auth): handle expired token\".\n"
        f"Valid types: {', '.join(COMMIT_TYPES)}.",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()