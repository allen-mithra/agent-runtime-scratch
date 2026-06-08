## Rebase before pushing on a feedback-re-driven swarm branch

The Philosophy
When a PR review or CI failure re-drives a run, the new pod gets a fresh clone
of the branch but a prior pod may already have pushed commits to the same
`swarm/<run_id>` ref — most often a `consolidate` commit landing CLAUDE.md and
`.claude/rules/` to the PR. Your local HEAD therefore lags origin from the very
first turn, even though `git status` looks clean. Pushing your work straight
away gets rejected with "fetch first." Worse, the ephemeral runner often drops
prior-run consolidate output into the working tree as untracked files; those
collide with `git pull --rebase` ("would be overwritten by checkout"). Fetch
and rebase as a deliberate step on these runs, and recognize that an untracked
file that bit-matches the remote version is a duplicate to delete, not a
change to preserve.

Do's
- Do `git fetch origin swarm/<run_id>` and inspect `FETCH_HEAD` vs your local
  HEAD before the first push on a feedback re-drive — assume the remote moved.
- Do rebase your local commit onto `FETCH_HEAD` (`git pull --rebase origin
  swarm/<run_id>`) so your fix lands on top of any prior consolidate commit.
- Do compare untracked CLAUDE.md / `.claude/` files against the remote ref
  (`git show FETCH_HEAD:<path> | diff - <path>`) before deleting; identical
  bytes mean it's a leftover from the prior run's consolidate that's blocking
  rebase, and `rm` is safe.
- Do push only after rebase succeeds — the resulting fast-forward push goes
  through on the first try.

Don'ts
- Don't push your first commit on a re-driven branch without a fetch — the
  rejection costs a turn and the recovery is always the same fetch+rebase, so
  just lead with it.
- Don't `git stash` or rename untracked CLAUDE.md / `.claude/` files that
  match the remote — they're not yours to preserve, they're a duplicate of
  what's already committed; delete them.
- Don't force-push to escape a rejected push on a `swarm/<run_id>` branch —
  you'll clobber the prior run's consolidate commit and lose its rules from
  the PR.
