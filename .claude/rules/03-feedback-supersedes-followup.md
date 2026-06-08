## PR review feedback supersedes a conflicting follow-up task

The Philosophy
A feedback-re-driven run often arrives with two instructions: the review
comment that triggered the re-drive, and the original task description still
attached to the run. When both target the same file on the same branch and
disagree on what the file should contain, treating the original task as
authoritative undoes the reviewer's request and looks like the agent ignored
the review. The reviewer's comment is the most recent, human, and contextual
signal — it wins. The honest move is to apply the review change, then call
the conflict out explicitly in a PR comment so the human can redirect if they
actually wanted both.

Do's
- Do treat PR review feedback as the source of truth when it conflicts with
  the standing task description on the same artifact.
- Do post a PR comment that names the conflict ("the follow-up task asked for
  X, your review asked for Y, I went with Y") so the reviewer can override if
  needed.
- Do reference the addressing commit SHA in the reply so the reviewer can see
  exactly what landed.

Don'ts
- Don't silently re-apply the original task's content over the reviewer's
  request — that reads as ignoring the review.
- Don't try to satisfy both by adding extra files or duplicating content the
  task didn't ask for; surface the conflict instead of inventing a compromise.
- Don't bury the conflict in the commit message alone — the reviewer is
  watching the PR thread, so the explanation belongs there.
