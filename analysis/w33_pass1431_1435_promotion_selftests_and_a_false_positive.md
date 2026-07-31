# Passes 1431–1435 — the manuscript builds again, the sweep gets a test per blind spot, and my own guard produces a false positive worth keeping

Five items. One is a repair to the manuscript build that had nothing to do with
me, one is a mistake I made and reverted, and one is my new guard being wrong
about the parallel track in an instructive way.

---

## Pass 1431 — `BT1408` promoted, and the manuscript build unblocked

`BT1408` is now `\input` by both root wrappers, matching the convention Pass 1420
established (starred subsection, injected after the table of contents). It stops
being orphan number 190.

Promoting into a manuscript that does not compile would be worth little, so I
compiled. It failed — **and not because of my insert**:

```text
error: manuscripts/tex/part22_fano_synthesis:3: Missing $ inserted
```

The line is

```latex
\textbf{Spectral erratum (PASS1150_SHIFTED_ADJACENCY_RETRACTION).}
```

with **unescaped underscores in text mode**. Verified pre-existing by stashing my
change and recompiling: identical error. The parallel track's own release note
says *"The real `w33_paper.tex` failure was traced to an unescaped identifier in
Part XXII … The integrator repairs that identifier"* — the diagnosis was right
and the repair did not land.

One-line fix, wrapping the identifier in `\texttt{}` with escaped underscores:

```text
w33_paper.tex  ->  1.43 MiB PDF, exit 0
```

**The master manuscript compiles again, with `BT1408` in it.**

---

## Pass 1432 — a mistake I made, in full

My first attempt at that fix was a regex sweep for `ALLCAPS_WITH_UNDERSCORES`
across all manuscript part files. It "fixed" **2,129 identifiers across 32
files** — and almost all of them were legitimate math-mode subscripts: `E_8`,
`A_2`, `C_2`, `G_N`. It replaced working mathematics with `\texttt{E\_8}` and
broke `w33_paper_body.tex` at line 155.

Reverted with `git checkout HEAD --` before anything was committed; the tracked
files made it recoverable. The actual defect was **one** identifier in **one**
file, and I found that out only after breaking thirty-two.

The lesson is specific enough to act on: I ran a rewriting regex over 32 files
without testing it on one. A transformation that edits should be proven on the
single known-bad case first, and only then widened — the same discipline the
guards here already use for *detection*, not yet applied to *modification*.

---

## Pass 1433 — one pinned self-test per blind spot the sweep has had

The Pass 1395 scope filter silently stopped working when a heredoc ate its `\b`
escapes, and nothing noticed for a session. A fix without a pinned case lasts
until the next edit. The sweep now tests all four of its historical blind spots:

```text
[PASS] BT810 boundary vs BT811: 5 shared tokens
[PASS] blockquoted Open: is NOT a boundary
[PASS] scope disclaimer is NOT a live question
[PASS] prose 'the question stays open' IS a boundary
[PASS] .tex files are scanned
```

Each corresponds to a failure that actually happened and cost something.

---

## Pass 1434 — my sampler guard is wrong about Pass 1417, and the reason is the point

`check_sampler_bias.py` flagged `w33_pass1417_exact_cover_orbit_frontier.py` —
the parallel track's own cover census, the file behind the `226800` bound. That
looked alarming, so I read it rather than reporting the flag.

**It is a false positive, and correctly so.** Their enumeration *is*
order-deterministic. But the file computes the full `PSp(4,3)`-orbit of each of
its sixteen covers and **proves them pairwise distinct**, then sums orbit sizes:

```text
16 x 12960  +  6480  +  6480  +  3240  +  3240  =  226800     ✓
```

Every orbit length is `25920 / |Stab|` for the claimed stabiliser, and the sum is
exactly their figure. A lower bound from *exhibited, verified-distinct* objects
is valid no matter how the objects were found — an exhibited object stays
exhibited.

My Pass 1411 did the opposite with the same machinery: it took a sample and
asserted a **universal** property. Same flag, opposite verdicts, and the
difference is the *quantifier*, not the search.

The guard now encodes that: files whose conclusion is a bound, an existence
statement, or an orbit census are downgraded. Universal-claim count drops
`92 → 73`, and Pass 1417 is no longer among them.

### Independent corroboration of their census

My own 24 randomised covers found four of their five stabiliser types:

| type | theirs | mine (24 covers) |
|---|---|---|
| `C4` | ✓ | 9 |
| `C2 × C2` | ✓ | 9 |
| `C4 × C2` | ✓ | 4 |
| `C2` | ✓ | 2 |
| `D8` | ✓ | **0** — never drawn |

`D8` sits in the rarest tier (orbit 3240), so missing it in 24 draws is
unsurprising. Four of five types confirmed from an independent search.

---

## Pass 1435 — the corpus index after the repair

Rebuilt with the five restored regexes and the new `edge240:signed` /
`edge240:unsigned` tokens:

```text
21,268 files   2,689 distinct tokens
collision pairs: 356
```

The head is unchanged from the pre-repair run, which is itself informative: the
dead patterns were `RE_QUESTION`/`RE_DISCLAIMER` in the *boundary sweep*, not in
the *index* grammar, so the collision numbers were never affected. The sweep's
numbers were; those are re-taken in Pass 1433.

Still at the top and still unread by anyone: `BREAKTHROUGH_309` vs `440` (a
cite-across candidate, not a rediscovery — adjudicated in Pass 1413), and
`w33_pass1122_trees.txt` vs `w33_pass1125_1127.txt`, both mine.

## Prior art

- Pass 1420 (parallel track) — **owns** the wrapper mechanism this promotion uses.
- Pass 1417 (parallel track) — **owns** the `226800` census corroborated above.
- [Pass 1428](analysis/w33_pass1426_1430_audit_of_my_own_failure_modes.md) — the guards refined here.
