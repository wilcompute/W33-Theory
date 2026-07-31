# Passes 1392–1396 — the cross-matching's cokernel, an exact cover, a 2-closure, and two tools that now cover the whole corpus

Five results. Two are new mathematics on the object Pass 1390 built, one converts
an *inferred* symmetry group into a computed one, and two are infrastructure that
existed only for `analysis/*.md` and now covers all 44,076 files.

---

## Pass 1392 — the cross-matching's cokernel is `Z¹⁵ ⊕ (Z/2)³⁰`

Pass 1390 produced a canonical 9-regular incidence `540 frames → 240 edges`, each
frame contributing a 4-edge perfect matching. The 240-edge carrier already has
fully computed integral arithmetic, so the incidence is a `540 × 240` integer
matrix whose Smith form is a well-posed question that could not be asked before.

```text
rank                       225
invariant factors          1^195 , 2^30
coker(Z^540 -> Z^240) =    Z^15  (+)  (Z/2)^30
```

Three exact statements come with it, all verified over all 540 frames:

```text
frames with a canonical matching     540 of 540   (0 failures)
all rows distinct (map injective)    true
edge coverage multiset               {9}          -- exactly 9, every edge
```

**The torsion is pure 2-torsion of rank 30, and the free corank is 15.**

**A flag, not a claim.** 15 is also the multiplicity of the eigenvalue `−4` in
`spec(A)` (and of `−5` in `spec(A−I)`), and `30 = 2·15`. That is *suggestive and
not asserted*: the 15 here is a corank on the **240-dimensional edge space**,
while the spectral 15 is a multiplicity on the **40-dimensional point space**.
They live on different carriers, so a matching integer is exactly the evidence
this corpus has a five-item failure list about. What would settle it is the
`G`-module structure of the free cokernel — if it is an irreducible of degree 15,
the coincidence becomes a statement. That computation is named here and not run.

---

## Pass 1393 — the 216-line frame's automorphism group, computed rather than inferred

The certified backbone records that the 216 tight-frame lines have angle set
`{0, 1/15, 1/5}` and has treated their symmetry as understood. It was never
computed; it was read off the angle set. `CLAUDE.md`'s failure-mode list puts
"metric or basis-dependent claims are provisional until a second realization is
checked" second, so this computes it.

The 216 lines are the 432 directed Schläfli arcs modulo reversal — that is, the
**216 edges of the Schläfli graph** `SRG(27,16,10,8)`. The right object is the
orbital configuration of `W(E₆)` on them, and the right question is 2-closure:
is the group preserving *every* orbital graph equal to `W(E₆)`, or bigger?

```text
degree-27 primitive group of order 51840        PrimitiveGroup(27, 13)
suborbits from a point                          [10, 16]        -- Schlaefli
edge orbit                                      216             -- as expected
action on the 216: order 51840, faithful        true
transitive                                      true
RANK on the 216 (orbitals incl. diagonal)       10
suborbit lengths                                [5,10,10,20,20,20,30,40,60]
|Aut(orbital configuration)|                    51840
IS W(E6) 2-CLOSED ON THE 216?                   TRUE
```

**The inference was safe** — the automorphism group really is `W(E₆)`, with
nothing extra. That is a confirmation rather than a correction, and it is worth
having precisely because the outcome was not knowable in advance. The rank-10
configuration and its suborbit lengths are new detail: the angle set has three
values, the orbital configuration has **nine** non-diagonal classes, so the angles
merge orbitals and could not have determined the group either way.

---

## Pass 1394 — the 240 edges admit an exact cover by 60 frame matchings

Each frame contributes 4 disjoint edges and each edge lies in exactly 9 frames.
`60 × 4 = 240` makes an exact cover arithmetically possible. It exists:

```text
each edge lies in            9 frame-matchings
exact cover found            YES (6.7 s, Algorithm X)
size                         60 frames
edges covered                240 distinct, every multiplicity 1
```

So there is a set of **60 frames whose canonical cross-matchings partition the
entire edge set of `W(3,3)`** — a resolution of the 240 edges into 60 four-edge
blocks, each block being a frame's own matching. Certificate:
`data/w33_pass1394_exact_cover.json`.

**Scope.** One cover is exhibited. The number of such covers, whether `G` acts
transitively on them, and whether any is `G`-invariant are all open and are not
claimed here.

---

## Pass 1395 — scope disclaimers are not open questions (the sweep's largest false-positive source)

Pass 1387 measured the boundary sweep's precision at 2/5 on the top of the ranked
list. Adjudicating twelve candidates by hand found the systematic cause of the
misses, and it is not tuning:

> **A third of the flagged "boundaries" ask nothing at all.**

`BT663`, `BT665`, `BT666`, `BT669` were all flagged on sections that read

```text
"This theorem does not claim W(G2) acts on the original 160 Levi flags."
"Do not claim that the raw complement is Q4."
"It does not turn the raw Levi complement into Q4."
```

These **fence** a result rather than leave one open. A later file in the same
programme naturally repeats their vocabulary, so they flag every run and can
never be resolved — there is nothing to resolve. They are permanent noise.

A boundary is now treated as live only if it contains an interrogative or a
forward commitment, and only if that outweighs the disclaimer language:

```text
candidates before the filter    32
candidates after                11        (-66%)
known true positives retained   both      (pass76 -> the [[137,1,3]] thread; BT808 -> BT809)
gated self-test                 unaffected, still 5 shared tokens
```

The remaining 11 all have genuine-question boundaries, so the pool is now worth
reading end to end rather than sampling.

---

## Pass 1396 — a persistent index over the whole corpus, certificates included

Three separate measurements said the same thing:

| measurement | finding |
|---|---|
| Pass 328 | 21% of pass files assert a code parameter that exists elsewhere, uncited |
| Pass 1382 | 8.4% of `analysis/*.md` share a group result with an uncited file |
| this session | the wrong 432-stabiliser order sat in **`data/ALIAS_REGISTRY.json`** |

The third is the one that matters. `RESULTS_INDEX.md` and every guard cover
**prose**; the error that took a pass to refute lived in a **certificate**.
`CLAUDE.md`'s own intake rule says certificates are part of the corpus — "re-read
the JSON, not just the prose" — and nothing indexed them.

`scripts/corpus_index.py` does:

```text
indexed 44,076 files, 23,594 distinct tokens        (first build 598 s)
extensions covered   .md .py .g .tex .json .txt .lean .yml
storage              SQLite, persistent
refresh              incremental by (size, mtime); a no-change refresh is one stat per file
```

Two design points were forced by this session rather than chosen:

- **Persistent and incremental**, because a `grep -r` over this repo (20,695
  tracked files, 1.4 GB `.git`) takes **over 600 s** and a full re-tokenise takes
  ~600 s. Neither is usable interactively.
- **Tokenising is wrapped per file and names the offending file on failure**,
  because a backtracking regex silently hung the entire sweep earlier today
  (>200 s on one 4 KB file). A `SLOW` canary prints any file over 2 s.

```bash
py -3 scripts/corpus_index.py build          # incremental
py -3 scripts/corpus_index.py find 'grp:2^3:S3'
py -3 scripts/corpus_index.py collisions     # uncited shared results, corpus-wide
```

## Prior art

- [Pass 1390](analysis/w33_pass1390_1391_frame_cross_matching.md) — the cross-matching whose lattice and covers are computed here.
- [Pass 1387](analysis/w33_pass1385_1389_a4_negative_precision_manuscripts.md) — the first precision measurement this sharpens.
- [Pass 1147](PASS1147_SCHLAEFLI_STEINBERG_FOURIER_BRIDGE.md) — **owns** the 216-line tight frame and its angle set.
- [`pass1012`](analysis/w33_pass1012_edge_root_equivariance_obstruction.py) — **owns** the 240-edge/240-root obstruction; the 240 here is the edge set.
