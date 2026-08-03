# erin-standards

Personal Claude Code plugin for your Refactrd client projects (Next.js, TypeScript, Tailwind, Python/AI). One place to update conventions instead of copy-pasting across TalentFlow, CPODS/Spotpay, BlazeCrux, and Sageberg.

## What's in it

- **Skills**
  - `/ai-stack-init`, describe an AI project idea and this figures out whether it needs Next.js only, Python only, or both, proposes the stack, and waits for confirmation before scaffolding
  - `/next-project-init`, scaffold a new Next.js + TypeScript + Tailwind project with Refactrd defaults
  - `/python-ai-project-init`, scaffold a new Python project for AI/LLM work using uv, ruff, and pytest
  - `/feature-branch`, branch + scaffold a new feature matching the repo's existing patterns
  - `/pr-description`, generate a PR title/description from the current diff
  - `/deploy-check`, pre-deploy checklist (typecheck, lint, build, env vars, secrets, debug artifacts)
  - `/readability-refactor`, review a file for readability (function length, nesting, naming, magic numbers) and propose concrete fixes
  - `/naming-audit`, check naming consistency across a directory when conventions have drifted
- **Hooks**
  - Blocks Claude from editing `.env*`, credential, and key files (`PreToolUse`, hard block, exit code 2)
  - Runs eslint on any file Claude edits and surfaces findings back into the conversation (`PostToolUse`, advisory only)
- **Agent**
  - `reviewer`, isolated-context subagent for reviewing a diff before you open a PR

## One-time setup

1. Push this directory to its own git repo, e.g. `github.com/your-username/claude-standards`.

2. On any machine you use Claude Code from:
   ```
   /plugin marketplace add your-username/claude-standards
   /plugin install erin-standards@erin-marketplace
   ```

3. That's it, skills, hooks, and the reviewer agent are now available in every project, not just one repo. No per-project install step.

## Per-project setup (still needed)

The plugin gives you shared behavior. Each project still needs its own `CLAUDE.md` for project-specific facts the plugin can't know: package manager, actual directory structure, which env vars exist, deploy target specifics. Keep it under ~200 lines. A minimal template:

```md
# <Project name>

Stack: Next.js <version>, TypeScript, Tailwind <version>, <state management: Redux / React Query / etc>
Package manager: <pnpm/npm/yarn>, always use this, not another one
Deploy: <Vercel project name / branch that auto-deploys>

## Commands
- Dev: `<command>`
- Typecheck: `<command>`
- Lint: `<command>`
- Build: `<command>`

## Conventions specific to this repo
- <e.g. "job description rendering goes through JobDescriptionRenderer, don't parse description strings directly elsewhere">
- <e.g. "rate card tabs are per-route files under app/rate-card/[tab], not a single monolithic page">

## Don't
- <project-specific footguns, e.g. "don't touch the Google Sheets integration in /api/contact without checking env vars are set">
```

## Updating the standard

When you fix the same thing twice across projects, it belongs here, not in one repo's `CLAUDE.md`. Edit this repo, push, then in each project run:

```
/plugin marketplace update
```

## Testing changes locally before pushing

```
claude plugin validate .
```
then point a test project's marketplace at your local path before pushing to your repo.
