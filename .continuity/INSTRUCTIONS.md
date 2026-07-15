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

## Search for the RESULT, not the topic (read this before claiming anything new)

**This corpus is indexed by *when* someone worked, not by *what* they found.**
Analysis files are named `2026-07-10_levi_next5.md`, `PASS178_...`, `BT1654_...`.
A file named for a date carries no topic signal, so a search for a topic cannot
find it. Two agents work this repo in parallel and neither reads the other's
filenames.

**Therefore: before claiming a result is new, grep for the result itself** — the
formula (`(q^2+1)(q+2)`), the integer (`51840`, `25920`), the sequence
(`25/91/225`, `10, 50, 298`). Those hit on day one. `rank` does not.

Then read `docs/index.html` and the recent `analysis/*.md`, and check the
external citations already in the repo (`AUDIT_*.md` has a "External checks used"
block) — the result may be published, cited here, and still get rediscovered.

### The five failure modes this repo has actually produced

Ordered by how hard they are to catch. Each was found the expensive way.

1. **Coordinate artefacts** — a metric/basis claim refuted by a second drawing.
   *Fix:* check another realization before publishing anything metric.
2. **Over-reads** — the result is right, the framing exceeds the proof.
   *Fix:* state the scope the witness actually establishes, not its implication.
3. **Unbuilt objects** — a claim naming no map ("a coupled module"). Can't be
   refuted *or* used. *Fix:* name the map or state the open question.
4. **Unbuilt halves** — a sound file with one ungrounded sentence (a
   dimensionless eigenvalue asserted to be a mass). A file-level audit passes it;
   only reading the sentences catches it. *Fix:* read, don't grep.
5. **Rediscovery** — *the most expensive, and invisible to checks 1–4.* The maths
   is correct, the witness passes, the framing is proportionate, an object is
   named. Nothing internal to the pass is wrong; only its novelty is false — and
   **novelty is not a property of the claim, it is a property of the corpus.**
   It cannot be self-checked. It can only be searched for, by result, before you
   start. See `analysis/w33_pass322_the_rank_law_was_already_ours.py`: ~15 passes
   re-derived a rank law the repo had already proved and formalized in Lean, and
   whose two halves are published (Sastry–Sin; Chandler–Sin–Xiang) and cited here.

### The operational prior

Trust spectral / algebraic / representation-theoretic claims by default; treat
metric or basis-dependent claims as provisional until a second basis is checked;
treat any claim whose scope exceeds its proof as an over-read; a claim that names
no object is not a claim; **and a claim you have not searched the corpus for is
not new.**
