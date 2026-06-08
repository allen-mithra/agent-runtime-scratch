## Always pass --head to `gh pr create` in containerized runs

The Philosophy
In a fresh container clone, `gh` cannot always infer the current branch's
remote even right after a successful `git push -u`. The push sets upstream in
the local config, but `gh`'s branch-detection sometimes runs before that state
is observable to it and aborts with "you must first push the current branch to
a remote, or use the --head flag." Passing `--head <branch>` explicitly removes
the inference step entirely, so the PR opens on the first try instead of after
a failed turn and a retry.

Do's
- Do call `gh pr create --head swarm/<run_id> --title ... --body ...` from the
  start, not as a fallback after the inference path fails.
- Do push the branch with `git push -u origin swarm/<run_id>` before creating
  the PR — `--head` tells `gh` which ref to open the PR for, but the ref still
  has to exist on the remote.
- Do pass the title and body via flags (HEREDOC for the body) rather than
  letting `gh` open `$EDITOR`; there is no interactive editor in a headless run.

Don'ts
- Don't rely on `gh pr create` auto-detecting the current branch in a fresh
  container clone — treat `--head` as required, not optional.
- Don't `git push` and immediately `gh pr create` without `--head` "to see if
  it works"; the failure costs a turn and the recovery is exactly to add
  `--head`, so just lead with it.
