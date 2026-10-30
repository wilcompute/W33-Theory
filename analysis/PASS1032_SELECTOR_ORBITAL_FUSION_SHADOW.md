# Pass 1032 — Selector orbital scheme and the \(C_3	o S_3\) fusion shadow

**Certificate:** `analysis/w33_pass1032_selector_orbital_fusion_shadow.py` →
`data/w33_pass1032_selector_orbital_fusion_shadow.json` (`19/19`, deterministic,
standard-library Python).

## Hidden association scheme identified

BT360 found the base-sheet intersection profile

\[
108^1,\qquad54^2,\qquad12^{36},\qquad4^{27},\qquad2^{54},
\]

and predicted a hidden association scheme on the 120 selector sheets.

Pass 1032 identifies it exactly: it is the rank-five orbital scheme of the
line-phase \(PSp(4,3)\) action. Its subdegrees are

\[
\boxed{1,2,27,36,54}.
\]

The five orbital relations have the geometric reading:

| sheet overlap | valency | geometry |
|---:|---:|---|
| \(108\) | \(1\) | the sheet itself |
| \(54\) | \(2\) | the other two phases over the same line |
| \(12\) | \(36\) | three phases over each of twelve intersecting lines |
| \(4\) | \(27\) | one phase-matched sheet over each skew line |
| \(2\) | \(54\) | two phase-unmatched sheets over each skew line |

Thus the old intersection histogram was already the complete orbital-valency
signature.

## Dual E8 phase scheme

The E8 point-phase action has rank seven, with subdegrees

\[
\boxed{1,1,1,27,27,27,36}.
\]

Its three singleton suborbits are the three individually oriented phase states
over the base point. The three \(27\)-orbits are three distinct phase-transport
classes across the nonneighbor shell, and the \(36\)-orbit is the adjacent shell
with all three phases.

## Fusion shadow

The selector valencies arise from the exact subdegree grouping

\[
[1]+[1+1]+[27]+[36]+[27+27]
=
[1,2,27,36,54].
\]

Equivalently,

\[
1+1\longrightarrow2,
\qquad
27+27\longrightarrow54,
\]

while \(1,27,36\) remain visible.

This is the local upgrade

\[
C_3\longrightarrow S_3=C_3\rtimes C_2:
\]

phase inversion fuses the two nonidentity fibre directions and pairs two of the
three \(27\)-transport classes.

## Important boundary

Pass 1031 proves the two 120-sets are nonisomorphic. Therefore this is a **dual
subdegree-fusion law**, not a literal fusion of Bose–Mesner relation matrices on
one common vertex set.

The result still provides the correct structural crosswalk:

- E8 remembers oriented \(C_3\) phase;
- the selector adds phase inversion and sees the \(S_3\)-fused shadow;
- point/line non-self-duality prevents an internal identification of the carriers.

## Consequence for the selector correction

Any correcting character or cochain must respect the rank-five orbital algebra
and its \(S_3\) inversion. A correction designed only from the cardinality
\(120\), or from an unstructured sheet graph, misses the actual transport classes.
