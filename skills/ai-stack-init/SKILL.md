---
name: ai-stack-init
description: Scaffold a full AI project from a plain description of what to build. Decides whether it needs a Next.js frontend only, a Python AI backend only, or both, proposes the stack, and waits for confirmation before scaffolding anything. Invoke with /ai-stack-init at the start of a new AI product idea, not for adding a feature to an existing project.
---

# AI stack init

This skill exists for the case where you don't yet know the shape of the project, only what it should do. You describe the thing, this skill figures out the architecture, and nothing gets scaffolded until you've confirmed it.

## Step 1: get the description

If the user already described what they're building in the invocation, use that. Otherwise ask one question: "what are you building?" Don't ask a checklist of questions up front, the goal is to work from a plain description the way a person would explain it to a teammate.

## Step 2: decide the architecture

Reason through these questions using the description. Don't ask the user to answer them directly, infer the answers and show your reasoning in the proposal instead.

**Does this need a separate Python backend, or does Next.js alone cover it?**

Default to Next.js only (API routes calling the Anthropic SDK directly) unless the description clearly needs something Next.js/Node can't do well:
- Heavy embedding or data processing pipelines, batch jobs, or anything that would run for minutes rather than the length of a request
- Model fine-tuning or training
- Libraries that are Python-only for what's actually needed (real ML frameworks, not just "Python has more AI tutorials")
- Complex multi-step agent orchestration with many tools, long-running background workers, or scheduled jobs

A chatbot, a RAG feature over a modest document set, a content generation feature, or an AI-assisted form, all of these are fine as Next.js API routes calling the Anthropic SDK. Don't reach for a second service just because the project is "AI." Refactrd's own WriteTech Hub project is exactly this pattern (Next.js, Supabase, Anthropic API, no separate backend), and it works fine. Adding a Python service you don't need adds a second deploy target, a second runtime to keep in sync, and a network hop for no benefit. If you're not sure, say so in the proposal rather than defaulting to "both" to be safe.

**If a Python backend genuinely is needed:**
- Repo layout is a monorepo: `apps/web` (Next.js) and `apps/api` (Python, FastAPI), talking over HTTP. Don't reach for gRPC or a message queue unless the description specifically implies needing one.
- The web app talks to the API through a single `NEXT_PUBLIC_API_URL` (or server-side-only env var if the API should never be called from the browser directly), not scattered endpoint strings.

**What else the description implies:**
- Vector storage: if there's retrieval over documents, ask whether there's already a database in play (Refactrd projects lean on Supabase already, pgvector is the natural default there) before reaching for a separate vector database like Pinecone or a local Chroma instance. Local Chroma is fine for early prototyping only.
- Auth: only scaffold auth if the description implies multiple users or protected data. Don't add it preemptively.
- Background jobs: only if the description implies something async and long-running (batch document ingestion, scheduled re-indexing).

## Step 3: propose the stack and stop

Present a short, concrete proposal, not a wall of options:

```
Here's what I'd set up:
- Frontend: Next.js + TypeScript + Tailwind (apps/web, or root if no backend)
- Backend: <Python/FastAPI in apps/api, or "none, Next.js API routes handle this">
- AI: Anthropic SDK, <specific use: streaming chat / RAG / agent with tools>
- Storage: <none / Supabase+pgvector / other, with a one-line reason>
- Auth: <none / reason for including it>

Reasoning: <1-2 sentences on why this shape fits the description, especially why a second service is or isn't warranted>
```

Then stop and wait. Do not scaffold anything in this same turn. If the user pushes back on a choice (wants a Python backend you didn't propose, doesn't want Supabase, etc.), revise the proposal and confirm again rather than arguing for your original pick, but if you think their alternative genuinely creates a problem (e.g. adding a Python service for something that's a 20-line API route), say so plainly once before deferring to their call.

## Step 4: scaffold, once confirmed

- For the Next.js piece, follow the same steps as the `next-project-init` skill.
- For the Python piece, if included, follow the same steps as the `python-ai-project-init` skill, using FastAPI as the dependency set implies.
- If both exist, set up the monorepo root: a root `README.md` describing the two apps and how to run each, a root `.gitignore` covering both, and a root `CLAUDE.md` that names the architecture decision explicitly ("Python backend exists because X, don't add a second one") so a future session doesn't second-guess or duplicate it.
- Confirm both apps actually start (`pnpm dev` for web, `uv run <entrypoint>` or `uv run uvicorn ...` for the API) before reporting done.

## What not to do

Don't scaffold a Python backend, a vector database, or auth as defaults "because AI projects usually need them." Every piece in the proposal should trace back to something in the description. If the description is genuinely too thin to make these calls (e.g. "build me an AI thing"), say that directly and ask what it should actually do, rather than guessing a stack and hoping it fits.
