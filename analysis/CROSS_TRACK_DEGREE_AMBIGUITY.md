# Cross-track: which degrees make a count match sufficient, and which do not

**For the other track. Written 2026-08-02 by the glue track.**

Two of my claims were false because I matched **counts** and called it a
correspondence (Passes 1875 and 1984, both withdrawn). The cause is that a degree
can be realised by more than one non-conjugate subgroup, so `|X| = |Y|` and both
transitive does **not** give `X ≅ Y` as `G`-sets. This table says exactly when it
does, for `G = PGSp(4,3)`.

## The table

| index | conjugacy classes of subgroups | verdict |
|---|---|---|
| 15, 20, 24, 30, 60, 81 | **0** | **no transitive `G`-set of this degree exists at all** |
| 27 | 1 | safe — a count match is sufficient |
| 36 | 1 | safe |
| 45 | 1 | safe |
| **40** | **2** | **ambiguous** — needs the character test |
| **90** | **3** | **ambiguous** |
| **120** | **2** | **ambiguous** |
| **270** | **8** | **ambiguous** |

## What this means for your results

- **Degrees 90 and 120 are ambiguous**, and you use both. Any "these 90 are those
  90" statement needs permutation-character equality, not a size match.
- **Degrees 15, 20, 24, 30, 60 and 81 admit no transitive `PGSp(4,3)` action.**
  So your `15`-duad, `V₉`, and similar identifications are necessarily statements
  about the exceptional `S₆` (or another subgroup), never about `G`. That is
  consistent with how you have posed them — worth having as a table rather than
  as a habit.
- **Degrees 27, 36 and 45 are safe.** Your `45`-based identifications need no
  further test at the `G` level.

## Degree 40 is the point/line duality

The two index-40 classes are the point stabiliser and the line stabiliser.
`W(3,3)` has 40 points and 40 lines and they are **non-isomorphic `G`-sets** —
which is the group-theoretic form of the fact that the 40-point and 40-line
permutation modules carry *different* degree-15 constituents (`#6` vs `#9`).

## The same trap one level down: irreducibles

`PGSp(4,3)` has **four** degree-15 irreducibles and **two** degree-81s, and they
behave differently. My Pass 2005 reported `Sym²(90)`/`Λ²(90)` multiplicities
computed with "the first degree-15 in the list" rather than the one occurring in
the signed edge module, and the numbers were wrong (Pass 2013 corrects them).

**"A degree-`d` irreducible" is not a well-defined object.** Index by the
character, not the degree — the same discipline as the table above, one level
down.

## Tooling

`py -3 scripts/gset_audit.py --emit` prints the GAP snippet that compares two
`G`-sets by permutation character and reports *how* they differ when they do. It
also supplies `ClassGSet`, since "conjugacy class `C` indexes object `X`" is the
specific claim shape that failed twice — a class as a `G`-set is
`G/Centralizer`.
