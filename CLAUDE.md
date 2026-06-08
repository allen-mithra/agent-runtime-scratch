# agent-runtime-scratch

## Basics
- Throwaway target repo for agent-runtime e2e smoke tests. Tasks here are
  intentionally trivial (create a file, open a PR) and exist to exercise the
  agent-runtime → swarm → PR loop end-to-end, not to ship product code.
- No build, no tests, no CI gates of substance. The "contract" for a run is:
  the requested file exists at the requested path with the requested contents,
  and a PR is open against `main` from `swarm/<run_id>`.
- Default branch is `main`. Each run lands on its own `swarm/<run_id>` branch
  — never commit to `main`, never reuse another run's branch.

## Do's & Don'ts
- Do follow the task literally — if it says "exactly one line: hello", the
  file is `hello\n` and nothing else (no heading, no trailing prose).
- Do open the PR with `gh pr create --head swarm/<run_id> ...` after pushing;
  see `.claude/rules/01-gh-pr-create.md` for why `--head` is mandatory here.
- Don't add scaffolding (CI configs, lint setup, package manifests) the task
  didn't ask for. This repo is deliberately empty; extra files are noise in
  the smoke-test signal.
