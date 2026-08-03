---
name: deploy-check
description: Run the pre-deploy checklist before merging to main or pushing to production. Invoke with /deploy-check before any deploy, especially for client projects on Vercel.
---

# Pre-deploy checklist

Run these in order and stop at the first failure rather than running everything and dumping a wall of errors:

1. **Typecheck**: run the project's typecheck script (check `package.json` for `typecheck` or `tsc --noEmit`). Fix errors before continuing, don't skip this because "it's probably fine."

2. **Lint**: run the project's lint script. Auto-fix what's fixable, report the rest.

3. **Build**: run the production build (`next build` or the project's build script). A build that only works in dev is not deploy-ready.

4. **Env var check**: grep for `process.env.` usage introduced in this branch's diff and confirm each new variable is documented somewhere (`.env.example`, README, or wherever this project keeps that) and that you know whether it's already set in the Vercel project settings. Flag any that aren't, a missing env var in production is a much worse failure mode than catching it now.

5. **Debug artifacts**: search the diff for leftover `console.log`, commented-out blocks, or `debugger` statements and flag them.

6. **Secrets**: confirm nothing in the diff looks like a real API key, token, or credential rather than an env var reference.

Report a short pass/fail summary at the end, not a transcript of every command's full output. If everything passes, say so in one line and note that it's safe to open the PR or merge.
