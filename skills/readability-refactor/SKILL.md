---
name: readability-refactor
description: Review a file or set of files for readability and propose concrete refactors (long functions, deep nesting, unclear naming, magic numbers, dead code). Invoke with /readability-refactor on a file or before a PR, not for general code review (use the reviewer agent for correctness/security).
---

# Readability refactor

This is about how easy the code is to read six months from now, not about correctness or security, that's the `reviewer` agent's job. Don't duplicate it here.

## What to look for, in priority order

1. **Function length and responsibility**: a function doing three unrelated things should be three functions. Flag anything over roughly 40-50 lines or with more than one clear responsibility, and propose the split with actual names for the extracted pieces, not `helperFunction1`.

2. **Nesting depth**: more than 2-3 levels of nested conditionals or loops. Propose early returns, guard clauses, or extracting the inner block into its own function.

3. **Naming**: variables and functions that don't say what they hold or do (`data`, `temp`, `handleClick2`, `flag`). Propose specific replacement names, not just "rename this."

4. **Magic numbers and strings**: unexplained literals (`if (status === 3)`, `setTimeout(fn, 86400000)`) that should be named constants.

5. **Duplicated logic**: the same block appearing more than twice, propose extracting it, but don't over-abstract something that appears only twice with good reason to stay separate.

6. **Comments that compensate for unclear code**: a comment explaining *what* the next line does usually means the code should be rewritten to not need the comment. A comment explaining *why* (a non-obvious business reason, a workaround for a library bug) is worth keeping.

## Output format

For each file, give a short list: what's genuinely worth fixing, with a one-line reason and the concrete change (not just "this could be clearer"). Skip files that are already fine rather than inventing minor nitpicks to seem thorough. If a proposed change is large enough to be its own refactor rather than a quick fix, say so and ask before doing it, don't rewrite half a file's structure unprompted.

Don't touch formatting or anything a linter already enforces.
