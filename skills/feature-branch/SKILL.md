---
name: feature-branch
description: Start a new feature. Creates a properly named branch and scaffolds files matching the project's existing conventions. Invoke with /feature-branch when starting new work, not for small fixes.
---

# Feature branch workflow

Use this when the user says "let's start a new feature" or names a feature to build (e.g. "/feature-branch add candidate notes to TalentFlow").

## Steps

1. Confirm the feature name and which part of the repo it touches if not already clear from the user's message. Ask once, briefly, if genuinely ambiguous, don't ask if the current directory or recent conversation already makes it obvious.

2. Check current branch and working tree status (`git status`, `git branch --show-current`). If there are uncommitted changes unrelated to this feature, flag it before branching, don't silently stash or discard work.

3. Create the branch from the latest default branch:
   - `git fetch origin`
   - `git checkout -b feature/<kebab-case-name> origin/<default-branch>`
   Use `fix/`, `chore/`, or `refactor/` prefixes instead of `feature/` when the task is a bugfix, cleanup, or refactor rather than new functionality.

4. Look at 1-2 existing features in the same area of the codebase (same directory tree, similar module) to find the actual convention in use, don't assume a generic Next.js layout. Check things like: where types live, whether it's server components or client components, how data fetching is structured, naming conventions for files.

5. Scaffold the new feature's files matching what you found in step 4. Don't invent a different pattern than what's already there, even if you'd personally structure it differently, consistency with the existing codebase beats a "better" pattern the rest of the repo doesn't use. If you think the existing pattern is genuinely bad, say so to the user directly instead of quietly deviating.

6. Report back: branch name, files created, and one line on which existing feature you used as the pattern reference.
