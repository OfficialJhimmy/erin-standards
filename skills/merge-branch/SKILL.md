---
name: merge-branch
description: Merge an approved PR and clean up afterward, merges, deletes the branch locally and remotely, switches back to the default branch, and pulls latest. Invoke with /merge-branch once a PR has been reviewed and approved, not before.
---

# Merge branch

## Before merging

If `gh` is available and authenticated, check the PR's actual state first: `gh pr view --json reviewDecision,mergeable,statusCheckRollup`. Don't merge blind if this information is available. If the PR isn't approved, or checks are failing, stop and tell the user rather than merging anyway because they asked for `/merge-branch`, the command name isn't a request to skip the check.

If `gh` isn't available, ask the user to confirm the PR has actually been approved before proceeding, since there's no way to verify it directly.

## Steps

1. Merge with squash by default (`gh pr merge --squash --delete-branch`), which keeps the default branch's history to one commit per feature rather than every intermediate WIP commit. If the user has stated a different convention for this repo in `CLAUDE.md` (e.g. merge commits for a reason specific to that project), follow that instead.

2. If `gh` isn't available, fall back to plain git: switch to the default branch, `git merge --squash <branch>`, commit with a message summarizing the feature (not a list of every intermediate commit message), push, then delete the branch locally and remotely.

3. After merging: switch to the default branch, `git pull`, and delete the local feature branch if it wasn't already removed by `--delete-branch`.

4. Report what was merged and confirm the working tree is clean and up to date.

## What not to do

Don't merge a PR that hasn't been approved just because the user invoked this skill, flag it and stop instead. Don't silently pick merge commits over squash or vice versa without checking whether the project has already stated a preference.