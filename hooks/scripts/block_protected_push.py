#!/usr/bin/env python3
"""PreToolUse hook (matcher: Bash): blocks `git push` directly to a
protected branch (main/master). Deploys are meant to happen through a
reviewed PR + /merge-branch, not a direct push that skips review and
(on projects with Vercel git integration) ships straight to production.
Fails open on anything it can't confidently parse.
"""
import json
import re
import sys

PROTECTED_BRANCHES = ("main", "master")


def extract_command(payload):
    return payload.get("tool_input", {}).get("command", "") or ""


def targets_protected_branch(command):
    if not re.search(r"\bgit\s+push\b", command):
        return False

    # Matches: git push origin main / git push origin main:main /
    # git push -u origin main, etc. Doesn't fire on a plain `git push`
    # with no branch named (that pushes the current branch, which is
    # assumed not to be main/master under this workflow already).
    for branch in PROTECTED_BRANCHES:
        if re.search(rf"\bgit\s+push\b.*\b{branch}\b", command):
            return True
    return False


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    command = extract_command(payload)
    if not command:
        sys.exit(0)

    if targets_protected_branch(command):
        print(
            "Blocked: direct push to a protected branch. "
            "Ship changes through a PR and /merge-branch instead, "
            "a direct push skips review and can trigger an unreviewed "
            "production deploy on projects with Vercel's git integration. "
            "If this really is intentional, run the git command by hand "
            "outside Claude Code.",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()