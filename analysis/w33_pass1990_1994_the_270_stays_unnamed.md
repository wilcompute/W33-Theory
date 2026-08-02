# Passes 1990–1994 — the 270 stays unnamed, and the spread question closes at `q = 3`

Five items. One settles an open question, one refuses to close and is left open
honestly, and one turns three repeated errors into a tool.

---

## Pass 1990 — the 270 stays unnamed

Pass 1984 withdrew the identification of the size-270 class with the ordered
incident line pairs. The class *is* `G/C` with `C ≅ D₈ × S₄`, and that `G`-set
has a definite character:

```text
G/C : 1 + 6 + 15 + 20x2 + 24 + 60 + 60 + 64
```

Searching natural `G`-sets for an orbit of length 270 with that character:

```text
line pairs meeting in a point   : orbit lengths [480]
non-incident point-line pairs   : orbit lengths [1440]
frame pairs                     : orbit lengths [540]
```

**No orbit of length 270 appears in any of them.** The class remains
uncharacterised geometrically, and I am recording that rather than reaching for a
weaker correspondence.

What is known: `|G|/270 = 192`, `C ≅ D₈ × S₄` sits at index 10 inside the
index-27 maximal, and `G/C` decomposes as above. That decomposition is now the
*specification* any candidate object must meet — which is a more useful open
question than the one I had before, since it can be tested rather than guessed.

---

## Pass 1993 — every symplectic spread of `W(3,3)` carries `σ_S`, because `G` is transitive

Pass 1986 proved the `1/q` law for spreads carrying a `σ_S`, leaving open whether
all spreads do. At `q = 3`:

```text
spreads found                    : 36
G-orbit of one spread            : 36
=> G is TRANSITIVE on the spreads : TRUE
```

> **All 36 spreads lie in one `G`-orbit.** Since `σ_S` is canonically attached to
> a spread (Pass 1894: the linewise stabiliser is exactly `C₂`), transitivity
> carries it to all of them — so the `1/q` theorem applies to *every* symplectic
> spread of `W(3,3)`, not only the Desarguesian one it was constructed from.

For general odd `q` this reduces to whether `PGSp(4,q)` is transitive on
symplectic spreads, which is false in general — non-Desarguesian symplectic
spreads exist — so the theorem's scope stays "spreads carrying `σ_S`", with
`q = 3` now known to be all of them.

---

## Pass 1994 — `scripts/gset_audit.py`

Three errors in this arc had one shape: **matching numbers taken as matching
objects** (Passes 1896, 1983, 1984). The counts were right every time; the
objects were not.

Two transitive `G`-sets of the same size are isomorphic **iff their point
stabilisers are conjugate**, equivalently iff their permutation characters agree.
`gset_audit.py` emits the GAP snippet that does exactly that, and reports *how*
two `G`-sets differ when they do — both decompositions — rather than only that
they differ. It also provides `ClassGSet`, since "class `C` indexes object `X`"
is the specific claim that failed, and a conjugacy class as a `G`-set is
`G/Centralizer`.

That joins `constraint_audit.py` (does this constraint restrict anything?) and
`build_topical_aliases.py` (has this result been found before?) as the third tool
built from a repeated failure rather than from a plan.

---

## Pass 1991 — a cross-track claim, tested

The parallel track's Pass 1951 states that the 540 weight-four primal codewords
*are* the 540 frame matchings. From this side:

```text
code dimension                                   : 195   (as claimed)
distinct frame-matching supports                 : 540
every frame matching is a codeword               : True (they are rows of M)
weight-4 words among basis + pairwise sums       : 96, of which NOT frames: 0
```

**Consistent, and not verified** — a complete weight-4 census needs `2¹⁹⁵` words,
so the bounded search finds no counterexample rather than establishing the claim.
Reported at that strength.

---

## Pass 1992 — orbit-built parallel classes

Still not found, and still barely explored: six cyclic-orbit signatures tested in
Pass 1989, none yielding a 60-frame class from orbit unions. Larger and
non-cyclic subgroups are untried. No verdict.

---

## Prior art

- Pass 1984 — the withdrawal that motivates Pass 1990's specification.
- Pass 1894 — **owns** the `C₂` linewise stabiliser that makes `σ_S` canonical.
- Pass 1986 — the `1/q` proof whose scope Pass 1993 widens at `q = 3`.
- Pass 1951 (parallel track) — **owns** the weight-four shell claim Pass 1991
  tests.

## Still open

- What has permutation character `1 + 6 + 15 + 20×2 + 24 + 60 + 60 + 64`.
- `χ(H) = 9`.
- Whether non-Desarguesian symplectic spreads carry a `σ_S`.
