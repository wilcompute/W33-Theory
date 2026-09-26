# Pass 10967 — the FI vacuum regenerates R-parity violation

Producer: `analysis/w33_pass10967_fi_vacuum_regenerates_rpv.py`
Certificate: `data/w33_pass10967_fi_vacuum_regenerates_rpv.json`
Frozen orbifolder inputs: `data/w33_pass10967_space_group_discrete_charges.json.gz`
(non-R and R discrete charges of every field, 215 models, from `~/orb/build/discdump`),
`data/w33_pass10967_rpv_coupling_dump.json.gz` (string-allowed couplings from `dumpop`).
Regression: `tests/test_w33_pass10967_fi_vacuum_regenerates_rpv.py`

Builds on Pass 10960 (e80be5eea), 10962 (4e8314ad8), 10964 (0c1a13f0c), 10965 (00610bf4d) and
Holotrade b81ef8c (the three dimension-four operators are locked together; 104 order-4 udd
couplings with singlets) and the cross-track correction 0fee779 / 78ec0a0fc.

## A. The most general matter parity is excluded (0/215)

Pass 10960 scanned the B−L family and Z2 characters of the U(1) lattice that are ±1 on every
field. A matter parity only has to be −1 on q, u^c, d^c, e^c and +1 on the condensing
singlets; exotics may carry any phase. The general object is **any element of the gauge U(1)
torus times the space-group non-R discrete group** (Z6 point-group rule; Z3; in Z6-II also the
Z2 × Z2 fixed-point rules of the SU(2)² plane). Realizability of "even here, odd there" is
decided exactly by a Smith normal form: the rows of the left transform beyond the rank span the
saturated integer left kernel, and the congruences are solvable iff every such row has even
weight on the odd set.

| statement | models |
| --- | --- |
| a matter parity of this general kind exists | **88** (exactly the B−L models) |
| closed by one Farkas vector on the even-able singlets | 87 |
| closed by obstructing all 304 FI-cancelling rays (Z6II_23) | 1 |
| counterexamples | **0** |

In all 87 Z6-I models the even-able singlet types are exactly those of the B−L family:
generality adds nothing. The 145 new Z2 directions that the space group adds in Z6-II create no
new matter parity at all.

## B. Why the forced field is odd under every matter parity

290 of the 302 forced (never-even) singlets satisfy, with single copies of the fields, the
exact U(1) identities

    Q(n) = −Q(u^c d^c d^c) = −Q(q l d^c) = −Q(l l e^c).

This is the SO(10) invariant 16⁴ restricted to ν^c (compare Pass 10964: the forced field is the
ν^c of 16₋₃ ⊂ 78). Every matter parity is −1 on each cubic, hence −1 on n. The other 12 obey one
or two of the identities or their conjugates. Flagship: n₁₂ + u^c₁ + d^c₁ + d^c₂ = 0 in
Z6I_06__SM_20260917_2.

## C. The string selection rules regenerate all three operators

With the orbifolder's full coupling rules (gauge invariance, space group, R-charges):

* in **all 23** D-flat Z6-I models with B−L, none of u^c d^c d^c, q l d^c, l l e^c is allowed
  at order 3, yet **every one of the 9 forced singlets** of every model appears in allowed quartic
  couplings n·u^c d^c d^c, n·q l d^c and n·l l e^c;
* Z6II_23 has q l d^c (20) and l l e^c (16) at order 3, and u^c d^c d^c at order 5 (144
  couplings with two singlets; 1216 at order 6).

**Prior art.** Holotrade b81ef8c already counted 104 order-4 u^c d^c d^c couplings carrying
singlets. The 2026-09-21 cross-track note (Holotrade 0fee779, TOE 78ec0a0fc; recorded in
`.continuity/SESSION_NOTES.md`) observed that those singlets have odd 3(B−L), so b81ef8c's class
closure was *conditional on a matter-parity-breaking vacuum*. What is new here is that the
condition is met: the singlets the FI term forces are exactly the ones that regenerate the
operators, for all three operators, in every D-flat model.

The FI term forces ⟨n⟩ ≠ 0 (Pass 10960, 10964), with ⟨n⟩/M_s ≈ 0.2–0.4 (cfdc1f2). So all three
R-parity-violating operators come back with coefficients of order ⟨n⟩/M_s. The class's
"absent branch" (no cubic RPV) is therefore not stable: the vacuum that SUSY requires switches
the present branch back on.

## Reading

This is Martin's criterion (a VEV of a field with odd 3(B−L) breaks R-parity) realised by an
explicit string mechanism: the FI term is cancelled only by the ν^c-like direction, and that
direction is exactly the one that turns the SO(10) quartic into the RPV cubic. Together with
Passes 10960–10965 the discrete route to proton stability in the W(3,3) Z6 class is closed for
every non-R symmetry of the gauge torus and the space group, and for baryon triality. The
remaining open route is an R-symmetry acting on superspace (Z4^R), whose square would be a
matter parity. By A that square cannot lie in the torus × space-group group. It can still
involve the geometric R-symmetries (Z6^R × Z3^R × Z2^R of the Z6-II lattice; the Z6-I geometry
file defines none), whose W-invariant combinations act on superfields as non-R symmetries. That
extension is the next pass and is **not** covered here.

## Scope

Couplings are at the level of orbifolder labels: `bd` includes vector-like exotic d-type
triplets, and the light d^c are mixtures after decoupling. Coefficients are not computed.
"Allowed" means allowed by every selection rule the orbifolder implements. Non-perturbative
effects and R-symmetries that are not squares of torus × space-group elements are not covered.
