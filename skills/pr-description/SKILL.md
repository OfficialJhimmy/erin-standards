---
name: pr-description
description: Generate a PR title and description from the current branch's diff against the default branch. Invoke with /pr-description when ready to open a pull request.
---

# PR description generation

1. Determine the default branch (`git remote show origin` or check for `main`/`master`) and diff the current branch against it: `git diff origin/<default-branch>...HEAD`.

2. Also pull `git log origin/<default-branch>..HEAD --oneline` for commit context.

3. Write a PR description with this structure:

   ```
   ## What
   <2-4 sentences on what changed, in plain language, not a file-by-file list>

   ## Why
   <the problem this solves or the request it addresses>

   ## Testing
   <what you'd actually need to click through or run to verify this, be specific to what changed, not generic "tested locally">

   ## Notes for reviewer
   <anything non-obvious: a tradeoff you made, a follow-up you're deliberately not doing now, a spot you want a second opinion on>
   ```

4. Don't pad this out. If there's nothing worth saying in "Notes for reviewer," omit the section rather than filling it with filler.

5. If the diff touches env vars, migrations, or anything requiring a manual step post-merge, put that at the very top, not buried in "Notes."

6. Print the description in the chat as markdown ready to paste, and ask whether to open the PR directly via `gh pr create` if the `gh` CLI is available and authenticated.
