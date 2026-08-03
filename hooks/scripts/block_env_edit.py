#!/usr/bin/env python3
"""PreToolUse hook: blocks Edit/Write/MultiEdit against env and secret files.

Reads the hook event JSON from stdin. Exit code 2 blocks the tool call and
sends stderr back to Claude as the reason. Exit code 0 allows it.
"""
import json
import re
import sys

BLOCKED_PATTERNS = [
    r"(^|/)\.env(\..+)?$",
    r"(^|/)secrets?\.(json|ya?ml|env)$",
    r"(^|/)\.aws/credentials$",
    r"(^|/)id_rsa$",
    r"(^|/)id_ed25519$",
]


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # fail open on malformed input, don't block legitimate work

    file_path = (
        payload.get("tool_input", {}).get("file_path")
        or payload.get("tool_input", {}).get("path")
        or ""
    )

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, file_path):
            print(
                f"Blocked: {file_path} matches a protected secrets/env pattern. "
                "Edit this file by hand outside Claude Code if it genuinely needs a change.",
                file=sys.stderr,
            )
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
