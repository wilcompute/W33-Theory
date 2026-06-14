# Project Instructions

How this repository prefers to work with AI assistants.

## Git operations: use GitKraken (all agents)

**For anything git-related — searching history, status, staging, committing,
pushing, fetching, pulling, diffing, blame, branches — use the GitKraken MCP
tools, not raw `git` shell commands.** This applies to every agent working in
this repo.

- Status: `git_status` · Log/diff/search: `git_log_or_diff` (and `git_blame`)
- Stage/commit: `git_add_or_commit` · Push: `git_push`
- Fetch/pull: `git_fetch` / `git_pull` · Branches: `git_branch`,
  `git_checkout`

Always `git_fetch` and review recent `origin/master` commits before starting
or committing work — multiple agents push to the same `BT####` sequence, so
pick the next free number from `origin` and avoid duplicating an existing
packet.

Exception: operations the GitKraken tools do not expose (e.g. force-adding a
git-ignored artifact such as `data/*.json`, which needs `git add -f`) may use
the shell `git` as a narrow fallback; everything else goes through GitKraken.
