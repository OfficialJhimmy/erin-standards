---
name: branch-sync
description: Safely update the current feature branch with the latest default branch before continuing work or opening a PR. Invoke with /branch-sync when a branch has drifted from main, or right before opening a PR to catch conflicts early rather than in review.
---

# Branch sync

## Guardrails first

1. Check the current branch (`git branch --show-current`). If it's the default branch itself, stop and tell the user to switch to a feature branch, don't rebase main onto anything.

2. Check for uncommitted changes (`git status --porcelain`). If there are any, stop and ask the user to commit or stash them first. Don't auto-stash, a silent stash is easy to forget about and lose.

## Steps

1. `git fetch origin`.

2. Determine the default branch and rebase onto it: `git rebase origin/<default-branch>`.

3. **If the rebase succeeds cleanly**: report how many commits were replayed. If the branch has already been pushed before, note that a force push will be needed (`git push --force-with-lease`) and ask before doing it, since it rewrites shared history and the user should be the one deciding that's safe (e.g. nobody else has pulled this branch).

4. **If there are conflicts**: stop and list the conflicted files (`git status` after the failed rebase shows these). Don't try to auto-resolve conflicts by guessing which side is "right". Show the user each conflicted section if asked, explain the two sides in plain terms, and let them decide, then `git add` the resolved files and `git rebase --continue`. If a conflict looks like it might lose real logic on either side (not just a trivial import ordering clash), say so explicitly before resolving.

5. If the user wants to bail out partway through, `git rebase --abort` gets them back to where they started, mention this if things start looking messy.

## What not to do

Don't force-push without asking first, even if the rebase succeeded cleanly. Don't resolve conflicts silently and continue, every conflict resolution should be visible to the user before it's committed.