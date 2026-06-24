## The runner injects an untracked .claude/ — clean it before any checkout-class git op

The Philosophy
At pod startup the swarm runner drops a `.claude/` tree into the worktree (its
own rules, skills, etc.) as untracked files. When a parallel run has already
committed real `.claude/rules/*.md` to the remote branch, any operation that
moves HEAD across those paths — `git rebase`, `git checkout`, `git pull` — aborts
with "untracked working tree files would be overwritten." It looks like a
conflict but it's the runner-injected copy shadowing the real tracked file. The
fix is to remove the injected `.claude/` *before* the checkout-class op; the
real one comes back in the working tree from the rebased commits.

Do's
- Do `rm -rf .claude` before `git rebase`/`git checkout`/`git pull` if `git status` shows `.claude/` as untracked and the remote may have committed rule files.
- Do treat the runner-injected `.claude/` as ephemeral scaffolding — your durable rules live in the commit, not in that directory.
- Do re-author rule files via `Write` after the rebase if you needed them in-tree for this run; the file watcher won't restore them.

Don'ts
- Don't `git stash` or `git add` the injected `.claude/` to "preserve" it — you'd commit the runner's scaffolding into the repo.
- Don't read the "untracked working tree files would be overwritten" error as a real conflict; the tracked version on the remote is authoritative.
