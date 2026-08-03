---
name: next-project-init
description: Scaffold a new Next.js + TypeScript + Tailwind project with Refactrd defaults. Invoke with /next-project-init when starting a brand new client project, not for adding a feature to an existing one.
---

# Next.js + TypeScript + Tailwind project init

## Before running anything

Ask (once, briefly) if not already stated: project name, and package manager if the user hasn't already told you (default to pnpm if they have no preference, it's the current Next.js documented default and what most Refactrd projects should standardize on going forward, even though some existing repos use npm).

## Steps

1. Scaffold with the official CLI, which already gives TypeScript, Tailwind, ESLint, App Router, `src/` directory, and Turbopack by default:
   ```
   pnpm create next-app@latest <project-name> --yes
   ```
   If the user wants npm or yarn instead, swap the create command accordingly (`npx create-next-app@latest`, `yarn create next-app`), everything downstream is the same.

2. `cd` into the project and confirm it runs: `pnpm dev`, then check `http://localhost:3000` responds (don't just assume the scaffold succeeded).

3. Set up the pieces the CLI doesn't include but every Refactrd client project needs:
   - `.env.example` with placeholder entries (even if empty right now) so env var conventions exist from commit one
   - A `lib/` or `src/lib/` folder for shared utilities, matching whatever the CLI's src-dir choice was
   - Prettier config if the project doesn't already get formatting from ESLint's flat config (check `eslint.config.mjs`, newer scaffolds may already include Tailwind-aware lint rules)

4. Initialize git if it isn't already (the CLI usually does this), make an initial commit, and ask whether to create the GitHub repo now via `gh repo create` or leave that to the user.

5. Copy the CLAUDE.md template from this plugin's README into the new project's `CLAUDE.md` and fill in the placeholders (package manager, commands, deploy target) rather than leaving it generic.

6. Report what was created and the dev server URL. Don't narrate every command's raw output, just the outcome.

## What not to do

Don't add dependencies the user didn't ask for (state management libraries, UI kits, etc.) just because they're common. Ask first if the project's needs aren't already clear from context.
