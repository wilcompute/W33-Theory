# Passes 2088–2092 Exact Release

This release closes five linked finite-geometric and controller-algebra frontiers opened by Passes 2053–2081.

## 2088 — regular spreads are projective quadratic structures

For odd q, field reduction from `F_{q^2}^2` to `F_q^4` gives a regular symplectic spread.  Multiplication by a quadratic generator `t`, with `t^2=mu` nonsquare, defines a symplectic similitude `J` whose projective image is the unique involution of the field torus.  The spread is exactly the set of two-dimensional `F_q` subspaces invariant under `J`.

The q=3 verifier literally constructs the ten totally isotropic spread lines partitioning all 40 points of `PG(3,3)`, verifies nondegeneracy, and checks

\[
J^2=2I,
\qquad
\beta(Jx,Jy)=2\beta(x,y).
\]

## 2089 — the all-odd-q orbit-size theorem

The projective centralizer is

\[
C_{PGSp(4,q)}([J])\cong C_2\times P\Sigma L_2(q^2)
\]

of order

\[
2q^2(q^4-1).
\]

Therefore the canonical regular symplectic spread orbit has size

\[
\boxed{q^2(q^2-1)/2}.
\]

This proves the orbit-size part of the family for every odd q and recovers the complete computational values

\[
36,\ 300,\ 1176
\]

at q=3,5,7.  At q=11 it predicts 7260.

## 2090 — the q=3 stabilizer is `C2 x S6`

At q=3 the full spread stabilizer has order 1440.  The existing inner route-clock certificate identifies the order-720 factor as `S6`, so

\[
\boxed{C_{PGSp(4,3)}([J])\cong C_2\times S_6.}
\]

The central involution is silent on the local spread graph, leaving the visible `S6` action on the Kneser local graph `K(6,2)` and Johnson second subconstituent `J(6,3)`.

## 2091 — the shared-inversion controller

The `mu4` and `mu6` clocks have inversion presentations `C4:C2` and `C6:C2`.  If they are independent apart from the common inverter, they generate

\[
\Gamma=(C_4\times C_6):C_2,
\qquad |\Gamma|=48.
\]

Exact enumeration gives

\[
Z(\Gamma)\cong C_2^2,
\qquad
[\Gamma,\Gamma]\cong C_6,
\qquad
\Gamma_{ab}\cong C_2^3.
\]

The embedded `D4` and `D12` intersect only in the common inverter and generate all of `Gamma`.  Despite the shared order 48, this group is not `C2 x S4`; their centers and derived subgroups have different orders.

## 2092 — verification and manuscripts

Published artifacts:

- `analysis/w33_pass2088_2092_complex_structure_controller.py`
- `data/w33_pass2088_2092_complex_structure_controller.json`
- `tests/test_w33_pass2088_2092.py`
- `analysis/BT2088_BT2092_regular_spread_quadratic_structure_controller.md`
- `analysis/BT2092_regular_spread_quadratic_structure_controller_insert.tex`
- `.github/workflows/pass2088_2092_complex_structure_controller.yml`

Both `w33_paper.tex` and `photonic_holonet.tex` now inject the shared theorem insert.

The frozen certificate has status `PASS`; its canonical SHA-256 is

```text
722becaee46130193dfadb0cb8be3c97a5c2bbdfeb9de9bb2e27bc30250a9f6e
```

## Evidence boundaries

- Field reduction and Desarguesian-spread stabilizers retain classical literature ownership.
- The theorem classifies the canonical regular/Desarguesian symplectic orbit, not non-Desarguesian spreads.
- The all-q rank-three intersection graph remains outside the theorem.
- The order-48 controller assumes independence of the two phase clocks apart from their common inverter.
- No charge, colour, generation, flux, neutrino, coupling-constant, or particle identification is asserted.
