## Explicit changes_requested feedback overrides the run's follow-up task description

The Philosophy
A swarm run can arrive with two instructions that contradict each other: a
`changes_requested` feedback item from a prior PR review (e.g. "set the file
content to X, nothing else") and a "continue" task description that re-states
the original goal in the *pre-feedback* form (e.g. "add a file containing Y").
The agent contract puts feedback first, and reviewer feedback that says
"Nothing else" is an explicit closure on the file's content. Reverting to the
task description's wording would silently undo the very fix the feedback
demanded — turning the next CI cycle into another `changes_requested` round.

Do's
- Do treat `[changes_requested]` items as the authoritative spec for any file/field they pin down, even when a later task instruction names a different value.
- Do leave a PR comment when the feedback and the follow-up task disagree, naming the conflict and the resolution, so the reviewer can see why their wording was preserved.
- Do open exactly one PR per `swarm/<run_id>` branch — if a PR already exists for the branch, push to it and comment, don't try to open a second.

Don'ts
- Don't re-implement the original task verbatim after addressing feedback; the feedback has already redefined what "done" means.
- Don't switch branches or open a parallel PR to satisfy the follow-up task literally — the contract pins one branch per run.
