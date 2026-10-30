# Passes 468–472 — semisimple, Galois-ring, cover, and custody release

This rung advances all five v1.8 gates while preserving the two boundaries that cannot be closed without new formal-library work or measured hardware.

## Pass 468 — explicit semisimple sheet intertwiner

Pass 463 identified the q=5 collision as exchange of the two Galois-conjugate quintics between square and nonsquare central-character classes. Pass 468 constructs the exact normal-form intertwiner

\[
W^{-1}\operatorname{diag}(C(P_+),C(P_-))W
=
\operatorname{diag}(C(P_-),C(P_+)),
\]

where `C(P)` is the companion matrix and `W` is the block swap. Restoring the regular and character multiplicities gives a 100-dimensional faithful-component intertwiner. The quotient `F_5^*/{±1}` is `C_2`; its unique nontrivial element is the sheet exchange. This is not a vertex permutation or graph isomorphism.

## Pass 469 — Galois-ring conductor tower

For `R=GR(p^n,f)`, valuation-`r` characters form a stratum of size

\[
p^{f(n-r)}-p^{f(n-r-1)}.
\]

Their central kernel has size `p^{fr}`, the alternating radical on `R^2` has size `p^{2fr}`, the character order is `p^{n-r}`, and the coefficient order is `Z[zeta_{p^{n-r}}]` with ramification index `phi(p^{n-r})`. The exact witnesses include `Z/9`, `Z/25`, `GR(9,2)`, `GR(27,2)`, and `GR(25,2)`.

## Pass 470 — integral conductor-coupling matrices

The exact p-adic Schur-complement tower of the `Z/9` reduced Laplacian is now recorded. At level six the residual is an `18 x 18` matrix divisible by 3, so its direct mod-3 rank is zero. Dividing that same integral matrix by 3 produces the level-seven coupling matrix of rank 11; the remaining `7 x 7` level-eight matrix has full rank 7. Thus the top multiplicities

\[
0,11,7
\]

are predicted directly by the integral coupling matrices, not reconstructed from kernel-growth second differences. A symbolic formula for every `p,n` remains open.

## Pass 471 — uniform prime-power cover witnesses

The central-elation bulk chart is exhaustively verified over `F_3`, `F_5`, `F_7`, and the nonprime field `F_9`. In every case the bulk graph is distance-regular with

\[
\{q^2-1,q(q-1),1;1,q,q^2-1\}
\]

and shell sizes

\[
1,
q^2-1,
(q-1)(q^2-1),
q-1.
\]

The fibers are independent, distinct fiber mates have exactly `q+1` projective common neighbors all in the rim, and every bulk neighbor of a nontrivial fiber mate lies in shell two. A single uniform finite-field cardinality proof in Lean remains open.

## Pass 472 — hardware custody gate

The frozen classifier, one-percent abstention threshold, balanced-accuracy endpoint, parent protocol hash, and all four lab templates are bound into one SHA-256 custody token. The gate fails closed unless the complete measured input triple is present and the measured manifest explicitly says `measured=true`.

Current physical status:

```text
OPEN_NO_MEASURED_INPUTS
```

No laboratory score is claimed.

## Reproducibility

Run:

```bash
python analysis/w33_pass468_semisimple_sheet_intertwiner.py --check
python analysis/w33_pass469_galois_ring_conductor_tower.py --check
python analysis/w33_pass470_integral_conductor_coupling.py --check
python analysis/w33_pass471_uniform_cover_prime_power_witness.py --check
python analysis/w33_pass472_hardware_custody_gate.py --check
python -m pytest -q tests/test_pass468_472_semisimple_galois_cover_release.py
```
