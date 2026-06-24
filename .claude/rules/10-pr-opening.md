## Pass --head explicitly when opening a PR right after the first push

The Philosophy
`gh pr create` decides whether the branch is "pushed" by inspecting local git
state, and that inspection occasionally races the push it just completed —
including pushes that printed `branch '...' set up to track 'origin/...'`. The
result is a misleading "you must first push the current branch to a remote"
error on a branch that *is* on the remote. Naming the branch with `--head`
bypasses the inference and removes a class of one-shot failures that otherwise
cost a retry every time an agent opens its first PR for a run.

Do's
- Do pass `--head swarm/<run_id>` (or whatever branch you just pushed) on the very first `gh pr create` call.
- Do treat a successful `git push -u origin <branch>` as proof the branch exists on the remote — if `gh` disagrees, it's `gh`, not the push.
- Do keep the title under 70 chars and put detail in the `--body` HEREDOC, per the global PR-creation contract.

Don'ts
- Don't re-push or re-run `git status` to "fix" the gh error — it's not a state problem, it's an inference race.
- Don't open the PR from the GitHub web UI as a workaround; the agent's durable output is the PR opened via `gh`, with the body it controls.
