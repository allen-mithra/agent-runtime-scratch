# agent-runtime-scratch

## Basics
- Throwaway target repo for the agent-runtime / swarm e2e smoke tests. There is no application code, no build, and no test suite — work in this repo means landing a PR that demonstrates the runner's plumbing end-to-end.
- Typical task shape: add (or modify) a small marker file at the repo root — usually named `incluster-<id>.md` or similar — containing exactly the literal content the task specifies, then open a PR from `swarm/<run_id>` against `main`.
- Tooling available in the container: `git`, `gh`, `node`/`npm`, `python`/`uv`, `codegraph`, `ripgrep`. Nothing in this repo needs them beyond `git`/`gh`.

## Architecture
- Repo root: `README.md`, plus per-run marker files added by individual swarm runs. Nothing is layered or modular — flat root is the whole repo.
- `.claude/rules/` collects empirical rules learned across swarm runs against this repo; each run's PR is expected to add or refine rules here when something non-obvious comes up.

## CI & Tests
- No build, lint, or unit-test gates configured in this repo. "Done" = the requested file content matches exactly and the PR is open.
- Verification is purely textual: `cat <file>` shows the literal content the task (or its `changes_requested` feedback) specified, with no extra lines.

## E2E flows
- The end-to-end smoke is the swarm pipeline itself: control-plane → Redis → KEDA-spawned pod → branch `swarm/<run_id>` → committed change → PR open. This repo's only role is to be the target whose PR confirms the pipeline ran.

## Do's & Don'ts
- Do match the task's content spec character-for-character (including whether a trailing newline is implied) — reviewers grade these PRs on exact-match.
- Do address `changes_requested` feedback before the follow-up task; the feedback is the new spec for any file it pins down.
- Don't add app scaffolding, package manifests, or test harnesses — this repo is intentionally empty and a PR that adds them will be rejected.
- Don't open a second PR from the same `swarm/<run_id>` branch; push follow-up commits to the existing PR instead.
