# Passes 1060--1064: signed cover, Springer decision, the real 540, formal obstruction, and dual falsifier

## Release status

All five requested streams were executed against the post-Pass-1059 `master` frontier.

* Python certificates: **37/37 exact checks**.
* Local regression: **6 pytest tests passed in 29.39 s**.
* Formal source: `Pass1063SignedLiftObstruction.lean` is imported by `formal/W33.lean`; the push workflow runs the complete Lake build and also compile-locks the actual Pass575 module.

---

## Pass 1060 -- the minimal signed symmetry is the Schur cover

For every generator of the order-25920 unsigned action on the 120 E8 root lines, the witness solves the sign equations and constructs one of its two signed lifts on the 240 roots. The generated signed group has order 51840. Its kernel on the 120 antipodal blocks is exactly global root negation.

\[
1\longrightarrow C_2\longrightarrow Sp(4,3)\longrightarrow PSp(4,3)\longrightarrow1.
\]

The four-row Pass-1055 certificate is rechecked:

\[
\begin{aligned}
s_0+s_1+s_{49}+s_{50}&=0,\\
s_0+s_1+s_{48}+s_{50}&=0,\\
s_0+s_{49}+s_{50}+s_{60}&=1,\\
s_0+s_{48}+s_{50}+s_{60}&=0.
\end{aligned}
\]

Their XOR is `0=1`, so no section over `PSp(4,3)` exists. Any lifting group therefore needs a nontrivial kernel of size at least two; the constructed 51840-element cover meets that lower bound.

**Decision:** ordinary overgroups such as `PGSp(4,3)`, split `W(E6)`, semilinear extensions, or an external `S3` controller do not remove the internal obstruction, because restriction to their `PSp(4,3)` subgroup would produce the forbidden section. An `S3` device may select a branch operationally, but the mathematical cure is the non-split central double cover.

---

## Pass 1061 -- the Springer normalizer is the code embedding

Pass 1057 correctly reopened Pass 1043 because it had compared point-stabilizer subdegrees with whole-group orbit partitions. The matched action is now computed.

Pass 1021 already certifies that the Springer normalizer acts on its 40 Eisenstein fibres as the **point** action of `W(3,3)`, with full image

\[
\operatorname{Aut}(W(3,3))=PGSp(4,3)\cong W(E_6).
\]

This pass adds a multiplier-2 outer generator and transports it through:

1. the 40-point incidence action;
2. the binary adjacency code `C`;
3. `C^perp/C`;
4. the 120 intrinsic local axes;
5. the 120 E8 root lines.

The axis-to-anisotropic-class map commutes generator-by-generator for the full order-51840 group. The 120 anisotropic classes span the full 8-dimensional quotient, so this determines the complete linear action on all 256 classes.

Measured whole-group orbits:

\[
256=1+120+135.
\]

The ordered-pair embedding's isotropic split `27+36+36+36` is excluded.

**Decision:** the Springer normalizer realizes the **Pass-125 W33 code embedding**, not the ordered-anisotropic-pair branching embedding. This supersedes the original Pass-1043 interpretation.

---

## Pass 1062 -- the real order-48 subgroup behind 540

The full outer coset of `PSp(4,3)` in `PGSp(4,3)` was enumerated. Its outer involutions split into exactly two `PSp(4,3)` conjugacy classes:

| class size | inner centralizer order |
|---:|---:|
| 36 | 720 |
| 540 | 48 |

The unique 540-class therefore satisfies

\[
25920=540\cdot48.
\]

The order-48 centralizer has:

* center order 2;
* derived subgroup order 12;
* abelianization order 4;
* element-order distribution `1:1, 2:19, 3:8, 4:12, 6:8`;
* quotient by its center equal to `S4`.

These are exactly the invariants of

\[
C_2\times S_4,
\]

not `GL(2,3)` or a binary-octahedral double cover. The full `PGSp` centralizer is

\[
C_2\times(C_2\times S_4),
\]

of order 96, matching BT748.

Thus the torsor identity is now constructed rather than guessed:

\[
51840=540\times2\times48.
\]

This exhausts every order-48 subgroup arising as the inner centralizer of an outer involution, which is the exact BT748/540 geometry. It does not claim that no unrelated order-48 subgroup class exists elsewhere in `PSp(4,3)`.

---

## Pass 1063 -- Lean obstruction and actual Pass575 build lock

The new theorem `W33.Pass1063.signedLiftFourRowObstruction` formalizes the four equations over `ZMod 2`. `linear_combination` adds the rows, cancels every sign variable, and derives `0=1`.

The same file imports `W33.Pass575CyclotomicDVRKernel` and defines

```lean
def pass575BuildLock : W33.Pass575.OrderLocalCertificate :=
  W33.Pass575.orderLocalCertificate
```

so the verification targets the actual imported module under `formal/W33/`, not either detached proposal under `analysis/` or `lean/`. Updating `formal/W33.lean` triggers the repository's complete Lake build.

---

## Pass 1064 -- preregistered dual falsifier

One fail-closed protocol now combines two independent questions.

### Arm A: global contextuality

The exact geometry is frozen as 40 contexts of four outcomes, with every point occurring in four contexts. The combinatorial tax is

\[
40-36=4,\qquad CF=\frac4{40}=\frac1{10},
\]

and the 40 optimal failure sets are the 40 movable point-stars.

The primary experimental statistic is the state-independent exclusivity witness

\[
W=\sum_{i=1}^{40}p_i,
\]

with noncontextual bound `alpha=7` and ideal maximally-mixed target `10`. The contextual-fraction/point-star analysis is secondary and uses context-stratified bootstrap uncertainty; no hard-coded binomial sigma or acquisition time is claimed.

### Arm B: local 648-class tomography

Two explicit generators are frozen for each order-648 candidate. For the Hessian point stabilizer there are exactly two nonidentity central `C3` operations; both commute exactly with both generators. The dual line stabilizer is centerless and its best order-3 impostor has exact mismatch score 27.

Preregistered noise gates reserve a gray zone:

* point/Hessian accept: corrected score at most 9 for both central candidates;
* dual accept: every order-3 candidate scores at least 18;
* scores 10--17 or failed controls: inconclusive.

### Joint decision

| contextuality arm | central-C3 arm | verdict |
|---|---|---|
| positive | point/Hessian | supports the W33 contextual point tower |
| negative | point/Hessian | local Hessian class present; contextual substrate rejected |
| positive | dual/no central C3 | contextuality present; selected tower rejected |
| negative | dual/no central C3 | joint rejection |
| either inconclusive | any | no claim; acquire only the preregistered additional blocks |

No cosmology, amplitudes, Yang--Mills, or continuum interpretation is inferred from these finite tests.

---

## Artifacts

* `analysis/w33_pass1060_1064_core.py`
* `analysis/w33_pass1060_minimal_signed_cover.py`
* `analysis/w33_pass1061_springer_embedding_decision.py`
* `analysis/w33_pass1062_inner48_540_geometry.py`
* `analysis/w33_pass1064_dual_falsifier_preregistration.py`
* `data/w33_pass1060_minimal_signed_cover.json`
* `data/w33_pass1061_springer_embedding_decision.json`
* `data/w33_pass1062_inner48_540_geometry.json`
* `data/w33_pass1064_dual_falsifier_preregistration.json`
* `formal/W33/Pass1063SignedLiftObstruction.lean`
* `tests/test_w33_pass1060_1064.py`
* `.github/workflows/pass1060_1064_exact.yml`
