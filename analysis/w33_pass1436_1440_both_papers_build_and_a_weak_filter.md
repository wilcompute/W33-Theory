# Passes 1436–1440 — both papers build, my promotion broke one first, and a guard I built is a weak filter

Five items. One caught an error I had introduced, one measures a tool of mine as
mostly-noise, and one reconciles my cover sample against the parallel track's new
census — with my numbers coming off worse.

---

## Pass 1436 — the Holonet build, which my own promotion broke

Last round I promoted `BT1408` into **both** manuscripts and compiled only one.
The prediction I wrote down — *"asserting a promotion without compiling the
target is the error I just spent a pass fixing"* — came true immediately:

```text
error: analysis/BT1408_frame_cross_matching_theorem_insert:20:
       LaTeX Error: Environment lemma undefined.
```

then, after fixing that,

```text
error: analysis/BT1408_frame_cross_matching_theorem_insert:63:
       Undefined control sequence            (\Aut)
```

`w33_paper.tex` defines `lemma`/`proposition`/`remark` and `\PSp`/`\Aut`;
`photonic_holonet.tex` defines **none** of them. An insert that compiles in one
host silently breaks the other, and the failure appears only at promotion time.

Fixed by making the insert host-independent rather than by removing it:

```latex
\makeatletter
\@ifundefined{lemma}{\newtheorem{lemma}[theorem]{Lemma}}{}
...
\makeatother
\providecommand{\PSp}{\mathrm{PSp}}
\providecommand{\Aut}{\mathrm{Aut}}
```

```text
w33_paper.tex        1.43 MiB PDF   exit 0
photonic_holonet.tex  973 KiB PDF   exit 0
```

**Both manuscripts now build with `BT1408` in them.**

---

## Pass 1437 — the 15 other orphans: a portability test instead of 15 promotions

Promoting the remaining recent orphans blind would have reproduced the above bug
up to fifteen times, and they are the parallel track's batch inserts besides. The
useful contribution is the test that makes promotion safe —
`check_orphan_inserts.py --portability`:

```text
checked 189 orphaned inserts
  use host-only macros WITHOUT a guard : 25   <- would break a bare host
```

Twenty-five inserts currently cannot be promoted into `photonic_holonet.tex`
without breaking it. The fix per file is the four-line guarded preamble above.
This is reported rather than applied: they are not mine to rewrite, and the
measurement is what was missing.

---

## Pass 1438 — my own sampler guard has low precision, measured

`check_sampler_bias.py` reduced to 73 "universal-claim" files after the Pass 1434
refinement. I read the four highest-ranked. **All four are false positives:**

| file | the flagged sentence | why it is fine |
|---|---|---|
| `bt1363_q4_clock_tomotope_medial_descent` | "hits all 16 face labels exactly once" | exhaustive over 16 |
| `w33_heawood_toroidal_orbit_correction` | "transitive on all eight" | a proven transitivity |
| `w33_spread_contextual_microkernel_bridge` | "covering every chosen line" | a docstring describing the *search* |
| `w33_pass613_equivariant_groupoid_laplacian` | — | no generalising claim at all |

The cause is linguistic: in this corpus "all"/"every" almost always introduces an
**exhaustive check over a small finite set**, not an inference from a sample.

So the guard is a weak filter and its docstring now says so. Pass 1411 — six
covers, a claim about all covers — remains the only confirmed instance. Recording
this rather than leaving "73 files to read" standing as if it were a queue of
likely errors.

---

## Pass 1439 — the two cover censuses reconciled, and mine loses

The parallel track's Pass 1505 supersedes `226800` with a compiled census: 327
complete, pairwise disjoint `PSp(4,3)`-orbits certifying **3,547,800** covers.
Their arithmetic checks exactly:

```text
228*12960 + 75*6480 + 9*6480 + 9*3240 + 6*3240 = 3,547,800   ✓
327 orbits                                                   ✓
```

Converting orbit counts to **cover** counts is where my own data fails:

| stabiliser | share of covers (their census) | my 24-cover sample |
|---|---:|---:|
| `C2` | **83.3%** | 8.3% |
| `C4` | 13.7% | 37.5% |
| `C2 × C2` | 1.6% | 37.5% |
| `D8` | 0.8% | 0% |
| `C4 × C2` | 0.5% | 16.7% |

If 83% of covers sit in `C2` orbits, a uniform sample of 24 should contain ~20 of
them. Mine contained two.

**So my randomised-order DFS is not a uniform sampler**, and I should not have
presented its proportions as a distribution. Permuting the branch order changes
*which* solutions are reached; it does not make the reached set uniform. What my
sample did establish — that four of the five stabiliser types **exist** — is
unaffected, because existence survives biased sampling.

That is the Pass 1434 quantifier lesson one level up: **existence claims survive a
biased sample; frequency claims do not.** `BT1408`'s cover proposition now carries
their bound and this caveat.

---

## Pass 1440 — two failure modes written into `CLAUDE.md`

Both cost real passes and both are invisible — the code compiles and the output
looks right:

1. **A shell heredoc eats backslash escapes.** `\b` becomes a literal backspace
   byte; the pattern compiles and matches nothing. This happened **four times**
   this session, once disabling the Pass 1395 filter for a whole session. Rule:
   use the Edit/Write tools for anything containing escapes, and copy
   `_assert_no_control_chars()` into any new file that compiles patterns.
2. **A rewriting transformation run before it is tested.** A sweep meant to fix
   one identifier "fixed" 2,129 legitimate math subscripts across 32 files. Rule:
   prove a rewriting transformation on the single known-bad case, then widen; if
   a one-line fix touches thousands, it is not that fix.

The guards here already applied that discipline to *detection*. It was never
applied to *modification*.

## Prior art

- Pass 1420 (parallel track) — **owns** the wrapper mechanism this promotion uses.
- Pass 1505 (parallel track) — **owns** the 327-orbit / 3,547,800 census reconciled here.
- [Pass 1434](analysis/w33_pass1431_1435_promotion_selftests_and_a_false_positive.md) — the quantifier distinction extended above.
