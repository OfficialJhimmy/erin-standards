#!/usr/bin/env python3
"""PostToolUse hook: runs eslint on the file that was just edited, if the
project has eslint configured. Output is printed to stdout so Claude sees it
as context. This never blocks: it's advisory, not enforcement (enforcement
lives in the secrets-guard hook and in CI).
"""
import json
import os
import subprocess
import sys

LINTABLE_EXT = (".ts", ".tsx", ".js", ".jsx")

ESLINT_CONFIG_NAMES = (
    "eslint.config.js",
    "eslint.config.mjs",
    "eslint.config.ts",
    ".eslintrc.js",
    ".eslintrc.json",
    ".eslintrc",
)


def find_project_root(start):
    d = start
    for _ in range(6):
        if os.path.exists(os.path.join(d, "package.json")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return start


def has_eslint_config(root):
    return any(os.path.exists(os.path.join(root, name)) for name in ESLINT_CONFIG_NAMES)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    file_path = (
        payload.get("tool_input", {}).get("file_path")
        or payload.get("tool_input", {}).get("path")
        or ""
    )

    if not file_path.endswith(LINTABLE_EXT) or not os.path.exists(file_path):
        sys.exit(0)

    root = find_project_root(os.path.dirname(os.path.abspath(file_path)))
    if not has_eslint_config(root):
        sys.exit(0)

    try:
        result = subprocess.run(
            ["npx", "--no-install", "eslint", "--no-color", file_path],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except Exception:
        sys.exit(0)  # don't fail the edit over a lint runner problem

    if result.returncode != 0 and result.stdout.strip():
        print(f"eslint findings for {os.path.relpath(file_path, root)}:\n{result.stdout.strip()}")

    sys.exit(0)


if __name__ == "__main__":
    main()
