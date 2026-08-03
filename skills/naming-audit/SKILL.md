---
name: naming-audit
description: Check naming consistency across a module or directory (mixed conventions for similar concepts, inconsistent casing, misleading names). Invoke with /naming-audit on a directory when a codebase has grown organically and names have drifted.
---

# Naming consistency audit

## What this catches that readability-refactor doesn't

`readability-refactor` looks at one file in isolation. This looks across multiple files for drift: the same concept named three different ways because different people (or different sessions) built different parts.

## Steps

1. Scan the target directory for the concepts that repeat across files: similar data shapes, similar functions (fetchers, handlers, formatters), similar component patterns.

2. Look for inconsistency in:
   - **Casing conventions**: `camelCase` vs `snake_case` vs `PascalCase` used inconsistently for the same kind of thing (e.g. some API response types are `PascalCase`, others aren't).
   - **Synonym drift**: the same concept called different things in different files (`getUser` / `fetchUser` / `loadUserData` all doing the same kind of thing).
   - **Prefix/suffix conventions**: some handlers named `handleX`, others `onX`, others no prefix at all, with no clear rule for when each applies.
   - **Boolean naming**: some booleans read naturally (`isLoading`, `hasError`), others don't (`loading`, `error` used as a boolean, `disabled` vs `notEnabled`).

3. Don't propose a rename for every inconsistency you find. Group them, and only propose changes where the inconsistency would actually confuse someone working across those files, not every single stylistic difference.

4. Present findings as: the pattern that should win (based on which convention is more common in this codebase already, not an outside "best practice"), and the specific files/names that don't match it. Let the user decide whether to actually run the renames, since renames touch a lot of call sites and aren't free.

5. If asked to apply the renames, do them file by file and run the project's typecheck after each one, don't do a blind find-and-replace across the whole codebase in one shot.
