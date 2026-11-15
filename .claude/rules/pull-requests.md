# Pull request rules for this repo

These rules apply to every PR in `ocholuo.github.io`. They override the general PR guidelines in the user's global `CLAUDE.md` where the two differ.

## Does not apply here

- **Radar ID.** Do not ask for a Radar ID. Do not prefix the PR title with `[rdar://...]`.
- **Human-only PR sections.** The general rule that the agent must not write the Motivation, Design decisions or Notes to reviewers sections does not apply. The agent may write the whole PR body, including the motivation, and does not need to prompt the user for those sections.

## Applies here

- Follow `.github/PULL_REQUEST_TEMPLATE.md` exactly: Description, Type of change, How has this been tested, Test Configuration. Keep only the relevant Type of change option.
- Run the `pre-pr-check` skill before creating a PR. This repo has no Makefile and no unit tests. The checks that apply are `bash tools/test`, the standards check and the documentation check. The CI workflow builds the site on every push and PR, and its result is the build evidence.
- Put the pre-pr-check line at the top of the Testing section. If the check is not valid on the head commit, open the PR as a draft and say so in that line.
- Tick a test checkbox only when that test actually ran. Do not tick `bash ./tools/test` when the Jekyll gems are missing.
- Keep a PR as a draft until CI is green on the head commit, then mark it ready.
- Add no `Co-Authored-By` trailer and no AI or agent attribution to commits or to the PR body.
- Alert the user before any push that adds converted PDF content and may hold personal information (see `note-content-rules.md`).
