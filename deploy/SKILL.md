---
name: deploy
description: Run the pre-deploy checklist and then actually deploy, confirming before anything goes to production. Invoke with /deploy when a merged change is ready to ship, on projects using Vercel. Complements /deploy-check, which only checks readiness, this one checks readiness AND ships.
---

# Deploy

## Step 1: run the readiness checklist

Follow the same steps as `/deploy-check`: typecheck, lint, build, env var check, debug artifact scan, secrets scan, stopping at the first failure. Don't proceed to shipping anything until this passes clean.

## Step 2: confirm the target

Ask, if not already clear from the conversation: is this a preview deploy or production? Don't assume production just because the checklist passed. Confirm which Vercel project this maps to if the project's `CLAUDE.md` doesn't already state it.

## Step 3: check env vars are actually set where they need to be, not just documented

`/deploy-check` only confirms new env vars are documented locally. This step goes further: if the Vercel CLI is available and authenticated (`vercel whoami`), run `vercel env ls` against the target project and cross-check it against the env vars the diff introduced. Flag anything referenced in code but missing from the actual Vercel project, that's the failure mode that only shows up after a broken deploy otherwise.

## Step 4: deploy

- Preview: `vercel` (no flag) if deploying from a branch that isn't wired to auto-deploy.
- Production: `vercel --prod`, or if the project deploys via Vercel's git integration on merge to the default branch, confirm the merge already happened (this may just mean: nothing to do here, the push already triggered it) rather than running a manual deploy that could conflict with the automatic one.

Never run a production deploy without an explicit confirmation in this same conversation. "The checklist passed" is not the same as "ship it."

## Step 5: report back

Give the deployment URL, and if it's a production deploy, say so plainly rather than burying it in output. If the Vercel CLI reports a build failure that the local build didn't catch (different Node version, missing env var only set locally), report that clearly, it usually means the local and Vercel build environments have drifted and that's worth fixing, not just retrying.

## What not to do

Don't skip step 1 because "it probably still passes from last time." Don't deploy to production silently as a side effect of another task, this skill should only run when the user is asking to ship something right now.