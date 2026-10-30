# Passes 358–359 — GitHub Batch Integrity and the Exact Alpha Code

## Executive result

The July 15 GitHub batch contained two genuinely useful questions buried under
several mutually inconsistent claims.  Exact GAP computation closes both:

1. the ordinary complex Weil carrier for `Sp(4,3)=2.U4(2)` is a non-real
   `9=5+4`, and the full outer-stable object is the real envelope
   `18=10+8`; and
2. the length-137 cyclic CSS construction is not an unsupported
   `[[137,1,3]]`.  It is the binary quadratic-residue construction and has exact
   parameters

   
   \[
     \boxed{[[137,1,21]]}.
   \]

The second conclusion combines an object-level GAP construction with the
published exact minimum distance of the binary QR code of length 137.  It is a
coding theorem.  It does **not** identify the code rate with the physical
fine-structure constant.

## What was checked first

Before computing, the audit read the fetched commits through `9de2d4004`, the
new Passes 353–357 and 75–92, the current `RESULTS_INDEX.md`, the full Theory
section of `docs/index.html`, the affected parts of `w33_paper.tex`, and the
recent analysis witnesses.  Result-first searches found that the correct
defining-characteristic transfer formula and the `9=5+4` ledger were already in
the repository.  The incoming claims had not superseded them; they contradicted
them.

The audit also exposed two mechanical search failures.  Comma-formatted
`35,697,025` was invisible to the integer tokenizer, and regeneration pushed
the flagship `[[40,10,4]]` result from 18 to 27 files, just past the fixed
distinctiveness cutoff.  The index now canonicalizes grouped integers and pins
`[[40,10,4]]` plus `[40,15,8]`, so becoming central can no longer make those
objects disappear from the result-first surface.

## Pass 358 — the exact integrity audit

The GAP witness is
`analysis/w33_pass358_github_batch_integrity_audit.g`; its generated certificate
is `data/w33_pass358_github_batch_integrity_audit.json`.

### The three groups that equal-order prose conflated

\[
\begin{aligned}
 \operatorname{PSp}(4,3)&\cong U_4(2)\cong W(E_6)^+,&|G|&=25920,\\
 \operatorname{Sp}(4,3)&\cong 2.U_4(2),&|G|&=51840,\quad Z(G)=C_2,\\
 \operatorname{PGSp}(4,3)&\cong U_4(2).2\cong W(E_6),&|G|&=51840,\quad Z(G)=1.
\end{aligned}
\]

GAP distinguishes the last two without relying on names: `Sp(4,3)` is perfect
and has center two, whereas `W(E6)` has two linear characters and trivial
center.  Consequently `W(E6)/Z2 ~= PSp(4,3)` is impossible: `W(E6)` has no such
center.  The correct relation is `W(E6)' = W(E6)^+ ~= PSp(4,3)`.

This also kills the proposed Pass-84 generator map.  A simple reflection has
order two; a nontrivial symplectic transvection in characteristic three has
order three.  Pass 358 supplies an explicit order-three symplectic unipotent.

### The Weil carrier and the new outer-envelope theorem

In `CharacterTable("2.U4(2)")`, GAP finds

| sector | CTblLib irreducibles | degree | FS | conjugation | central value |
|---|---:|---:|---:|---|---:|
| even | 2, 3 | 5, 5 | 0, 0 | `2 <-> 3` | `+5` |
| odd | 21, 22 | 4, 4 | 0, 0 | `21 <-> 22` | `-4` |

There is no degree-three irreducible.  Thus a claimed conjugate `6+3` split is
impossible twice over: conjugate representations have equal dimension, and the
required degree three does not exist.

The unique CTblLib class fusion

\[
  2.U_4(2)\;<\;2.U_4(2).2
\]

gives the stronger result

\[
  10\downarrow=5_a+5_b,qquad
  8\downarrow=4_a+4_b.
\]

Therefore the two conjugate nine-dimensional Weil carriers close as

\[
  \boxed{W_\psi\oplus W_\psi^*\cong 10\oplus8}.
\]

Both outer characters have Frobenius–Schur indicator `+1`.  The signed outer
controller swaps both Eisenstein pairs, so one nine-dimensional carrier is not
canonically selected.  This is the oscillator-level realization of Pass 346's
selection no-go.  It also matches the general existence of two Weil
representations and their extended organization in Chun-Hui Wang,
[“Extended Weil representations: the finite field cases”](https://arxiv.org/abs/2204.03987).

The character table alone does not label whether a chosen carrier is
`5a+4a` or `5a+4b`; an explicit Schrödinger generator comparison would fix that
convention.  The conjugation and no-selection theorem do not depend on it.

### The transfer polynomial and the q=7 closure

Chandler–Sin–Xiang give

\[
 \alpha_{1,2}=\frac{p(p+1)^2}{4}
 \pm\frac{p(p+1)(p-1)}{12}\sqrt{17}.
\]

At `p=5`, GAP obtains

\[
 x^2-90x+325,qquad
 \alpha_{1,2}=45\pm10\sqrt{17},qquad
 \Delta=6800.
\]

The incoming `35,697,025` determinant came from substituting a rank at the wrong
Frobenius level.  The follow-on identity was arithmetically one unit wrong:

\[
  8449^2=71,385,601\ne71,385,600.
\]

The Pass-92 question also closes exactly:

\[
  3089\text{ is prime},\qquad \operatorname{ord}_{3089}(2)=772\ne1544.
\]

So `q=7` fails the batch's own near-maximal-order test.  This preserves only a
finite checked range for the `q=3` uniqueness observation; it does not prove a
global uniqueness theorem over all prime powers.

## Pass 359 — the exact quadratic-residue CSS code

The GAP witness is `analysis/w33_pass359_alpha_code_qr_css.g`; its certificate
is `data/w33_pass359_alpha_code_qr_css.json`.

GAP proves

\[
  \operatorname{ord}_{137}(2)=68,qquad
  x^{137}-1=(x-1)g_Qg_N,qquad
  \deg g_Q=\deg g_N=68,
\]

and checks that the roots of `g_Q` are exactly the 68 nonzero quadratic
residues modulo 137, while `g_N` carries the complementary nonresidues.  The two
cyclic generator matrices have shape `69 x 137` and rank 69.  Their right
nullspaces give two rank-68 check matrices satisfying

\[
 H_QH_N^{\mathsf T}=0,qquad
 137-68-68=1,qquad
 Q^\perp\subset N,quad N^\perp\subset Q.
\]

Thus the repository construction is exactly the QR/NQR CSS pair.  GAP also
performs direct finite-field searches showing that no codeword of weight 3, 4,
or 5 exists, refuting the unsupported Pass-77 and Pass-91 words.

The exact classical result is known:

\[
 Q_{137}=[137,69,21],qquad \widehat Q_{137}=[138,69,22].
\]

Tjhai, Tomlinson, Ambroze, and Ahmed compute the full weight distributions and
state these parameters in
[“On the Weight Distribution of the Extended Quadratic Residue Code of Prime 137”](https://arxiv.org/abs/0801.3926).
The QR and NQR codes are multiplier-equivalent.  Their dual stabilizer spaces
are even, while the minimum words have odd weight 21, so those words are logical
rather than stabilizer words.  Hence the CSS distance is exactly 21.

### Honest interpretation

What is proved:

- a binary cyclic CSS code `[[137,1,21]]`;
- its exact QR/NQR construction and dual inclusions;
- a sevenfold distance improvement over the stale claimed value 3.

What is not proved:

- that `137` rather than `137.035999...` derives the physical coupling;
- that code rate is a running gauge coupling;
- that weight-21 logical supports are Feynman vertices or momentum-conservation
  laws.

## Disposition of the fetched batch

| incoming thread | exact disposition |
|---|---|
| Passes 353–355, `6+3` Weil chirality | **refuted**; exact carrier is non-real `5+4`, outer closure `18=10+8` |
| Passes 351–357, complex `B5` spectrum | **refuted**; `x^2-90x+325`, real roots `45+-10sqrt(17)` |
| Pass 75, an `F2` subgeometry inside `F3` | **refuted**; `F2` is not a subfield of `F3`; the honest doily bridge is functorial, not coordinate inclusion |
| Passes 77/91, weight-three Alpha word | **refuted and upgraded**; exact CSS code is `[[137,1,21]]` |
| Passes 78/83, direct `[[40,2,4]]` | **unbuilt/refuted**; the exact anchor remains `[[40,10,4]]` and adjacency 2-rank 16 |
| Passes 80/87/92, global uniqueness of 137 | **over-read**; q=7 is now closed negatively, but a finite scan is not an all-q theorem |
| Passes 81/82/84/87/90, `W(E6)=Sp(4,3)` | **refuted**; the corrected three-group ledger above applies |
| Pass 84, four lines in a tritangent plane | **refuted**; a tritangent plane contains three surface lines |
| Passes 85/88/90/91, SM identifications | **unbuilt**; no equivariant field map, gauge normalization, or continuum dynamics is supplied |
| Pass 89, Ihara graph RH | **survives after Pass 344's pole correction**; “all SRGs are Ramanujan” does not |

The current `docs/index.html` Theory section and the corrected group ledger in
`w33_paper.tex` had not absorbed these regressions.  They remain the honest
publication surfaces; this packet adds the exact corrections rather than
rewriting history as another speculative synthesis.

## Reproduce

```bash
gap -q analysis/w33_pass358_github_batch_integrity_audit.g
gap -q analysis/w33_pass359_alpha_code_qr_css.g
python3 -m pytest -q tests/test_pass358_359_gap_github_integrity_alpha_code.py
```

Expected: Pass 358 reports `33` checks, Pass 359 reports `26`, and pytest reports
`4 passed` on a GAP-equipped runner.
