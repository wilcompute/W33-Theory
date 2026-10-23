# W33 round seven: explicit GF(9) obstruction, source-free chirality, optimal SWAP depth, magic-resource interface and spectral gap

**Date:** 23 October 2026

**Code:** `analysis/w33_20261023_round7_four_frontiers.py` and `analysis/w33_20261023_three_layer_routing_cpsat.py`

**Tests:** `tests/test_w33_20261023_round7_five_frontiers.py`
**Machine-verifiable artifacts:** `data/PART_20261023_ROUND7_FOUR_FRONTIERS.json`, `data/PART_20261023_ROUTING_CPSAT.json`, `data/PART_20261023_ROUTING_FOUR_LAYER_CPSAT.json`

This packet follows five independent scientific tracks requested after the previous q=9 point-space spectroscopy. **No result is a demonstrated theory of everything, observed photonic machine, experimental parity violation, derived Einstein dynamics, or fault-tolerance threshold.** Literature priority is not claimed where a construction follows established quantum coding / gate teleportation principles.

## 1. GF(9) Frobenius obstruction: four *explicit* nonsplit module witnesses

Earlier arithmetic on the q=9 Pascal CSS code gave `C=row(B)`, `K=C^perp=ker(B)`, `Q=K/C` over F3 with dimensions 100, 720, 620. A symplectic transvection T has additive order 3 and D=T-I. The exact rank identity for the connecting map is

```text
delta_1: ker(D|Q) -> C / D(C);
rank delta_1 = rank(D|K)-rank(D|C)-rank(D|Q)
             = 428-54-370 = 4.
```

**New in this round:** Instead of merely evaluating the dimensions, modular row elimination simultaneously tracks *actual 820-coordinate preimages in K* and their *D-images in C*. Taking `D(C)` as a 54-dimensional subspace, the algorithm finds four pairs `(x_i,Dx_i)`, each satisfying

```text
B x_i = 0 (mod 3);
D x_i belongs to C;
rank(span(D(C),Dx_1,Dx_2,Dx_3,Dx_4)) = 58.
```

The JSON certificate freezes the four vectors as base-3 digit strings of length 820, with direct independent verification in pytest. These are **explicit first-order extension-class witnesses**, not just a Jordan counting check.

The finite-field controls in the preceding round showed `rank delta_1=0` for GF(4) and GF(8), but `4` for GF(9). The exact Frobenius-tensor *explanation* and an all-prime-power formula remain open. Rank four is not evidence of four physical dimensions.

## 2. A source-free two-qutrit many-body chiral Hamiltonian

The previous microscopic construction used the exact single-site W33 Pauli sum

```text
H_0=(I-9 Pi)/2,
Pi|a,b>=|-a,-b>,
spec(H_0)={-4 (fivefold), +5 (fourfold)}.
```

Let `O=[Re X_1,Re Z_1]/(2i)`. This is a Hermitian **parity-even** and **computational-complex-conjugation-odd** observable, with

```text
[O,H_0]=0,   O(O²-9/32 I)=0.
P_ground O P_ground:  +/- 3sqrt(2)/8 (each twice), 0 (once).
```

A concrete **source-free** family is

```text
H_N= sum_(i=1)^N H_(0,i) - (J/N) (sum_(i=1)^N O_i)^2; J=1.
```

The Hamiltonian is exactly invariant under global computational complex conjugation K: each O_i changes sign but its total square does not. The operator inequalities `H_(0,i)>=-4I` and `|sum O_i|<=N*3sqrt(2)/8` imply

```text
E_ground(N) >= -4N - (9/32)N.
```

Equality is attained by tensor products of locally parity-even `O=+3sqrt(2)/8` eigenstates (or all negative). There are exactly `2^(N+1)` ground states, and the global K exchanges the positive and negative *macroscopic* chiral sectors. For N=2, independent numerical diagonalization of the full 81x81 Hamiltonian verifies `E0=-8-9/16=-8.5625` and eightfold degeneracy.

This is a **real mathematical K-symmetric degeneracy mechanism without an inserted K-odd source**. It is **not** an established physical time-reversal symmetry, and it uses infinite-range mean-field interactions. Moreover opposite chiral states are exactly degenerate even at finite N: this is not evidence of dynamical tunneling suppression or a genuine thermodynamic origin of time. Constructing a local robust phase and identifying an operational antiunitary is necessary.

## 3. Global optimum: W33 transvection routing takes **exactly four parallel SWAP layers**

The previously verified circuit decomposes any transvection into 36 nearest-neighbor A-graph SWAPs over **four parallel matchings**, routing all 40 tokens. The previous lower bound was only three layers.

**New:** A complete CP-SAT model permits *any* matching in each layer, without imposing one hub per 3-cycle. For every vertex v in each layer, an integer partner `p_l(v)` is restricted to v or an adjacent W33 vertex. The element constraints `p_l(p_l(v))=v` and an all-different constraint ensure every layer is an honest disjoint edge matching. All 40 initial token positions are propagated through the three layers with `x_(l+1)=p_l(x_l)` and constrained to end at the *exact* symplectic-transvection destination. A finite exhaustive search returns **INFEASIBLE** for depth 3. The model is rerun for depth 4, where a separately known concrete construction is supplied as a hint, and yields **OPTIMAL/FEASIBLE** with 36 swaps.

By transitivity of the symplectic projective automorphism group (preserving W33 edges), the same depth lower bound applies to all forty anchor transvections. Thus

```text
minimum parallel matching depth = 4.
```

This is a genuine **finite exhaustive solver certificate**, conditioned on the verifiable CP-SAT model's faithful encoding; it is not a hand-derived closed-form lower bound and the repository does not include an independently checkable proof trace. The model, solver configuration, counts and feasible four-layer schedule are frozen in the two JSON artifacts. The minimum *total SWAP count*, still bounded between 27 and 36, remains open.

This is abstract physical-qudit nearest-neighbor routing; optical timing, mode couplers, loss and cross-talk are not measured.

Relevant prior algorithmic context: Kawahara, Saitoh, Yoshinaka, *The Time Complexity of Permutation Routing via Matching, Token Swapping and a Variant*, arXiv:1612.02948.

## 4. Exact single-qutrit magic-to-Choi conversion and a noise budget

The preceding round verified all nine corrected Bell-teleportation branches for the non-Clifford qutrit phase gate
`M=diag(1,zeta_9,zeta_9²)`. Here is an explicit offline resource-preparation interface:

```text
|M+> = (|0> + zeta9 |1> + zeta9² |2>)/sqrt3.
|M+> tensor |0> --SUM--> |R_M>
            = (|00>+zeta9|11>+zeta9²|22>)/sqrt3.
```

The only conversion operation is a **Clifford controlled-SUM**; no expensive non-Clifford gate need be applied at injection time once |M+> is prepared. Combined with Bell measurement and Clifford feedback, this supplies the same exact logical resource as the previous codeword charge-extraction architecture.

For a transparent example error model
`rho=(1-epsilon)|M+><M+|+epsilon I/3`,
the resulting Choi resource has *exact* fidelity
`F=1-2epsilon/3` relative to |R_M>. With otherwise ideal Clifford preparation and measurement, trace-norm contractivity and Fuchs–van de Graaf yield an output trace **distance** bound `<=sqrt(2epsilon/3)`. The certificate evaluates eps=0,0.001,0.01,0.05,0.1. This is a conservative single-resource error budget, **not a distillation map or fault threshold**.

Literature: Anwar, Campbell, Browne, *Qutrit Magic State Distillation* (2012), arXiv:1202.2326; Campbell, Anwar, Browne, *Magic-State Distillation in All Prime Dimensions Using Quantum Reed-Muller Codes*, Phys. Rev. X 2, 041021 (2012), arXiv:1205.3104. Those papers establish actual distillation procedures; no novel distillation threshold is claimed here.

## 5. All-q restricted no-go: positive W33 kinetic defects cannot close its normalized spectral gap

The previous pass found at least 51 distinct energies on W(3,9) for the **signed** sparsified two-anchor Hamiltonian. A rich finite energy spectrum does not imply low-energy gapless dynamics. To test that distinction, use the **natural normalized positive graph kinetic operator**

```text
L0_q=I-A_q/[q(q+1)],
A_q = symplectic collinearity adjacency for W(3,q).
```

The generalized quadrangle is strongly regular with adjacency eigenvalues
`q(q+1)`, `q-1`, `-(q+1)`; therefore

```text
spec(L0_q) = { 0, 1-(q-1)/[q(q+1)],
                    1+1/q }.
```

Add any two (or any finite number of) **positive** transvection-defect Laplacians with nonnegative coupling:

```text
L_q=L0_q+sum_i epsilon_i (2I-T_i-T_i^-1), epsilon_i>=0.
```

Each defect is positive semidefinite and annihilates the constant vector. The Poincaré/min-max principle gives the **exact family-wide lower bound**

```text
lambda_2(L_q) >= 1-(q-1)/[q(q+1)] -> 1 as q grows.
```

Hence this specific normalized positive graph/defect operator family **cannot** acquire a gapless near-zero band in the naive q→infinity limit; no accumulating low-energy Weyl spectrum arises without different dynamics/scaling. This is a *restricted but all-q theorem*, not merely a finite check. It **does not** exclude the previous signed sparse H, negative couplings, interactions with other kinetic terms or alternative physical coarse-graining. Finite q=3,4,8,9 matrix-Rayleigh tests accompany the analytic proof.

Reference geometry: symplectic generalized quadrangle Sp(4,q) parameters and eigenvalues are standard in algebraic graph theory; see Brouwer's symplectic graph tables, https://aeb.win.tue.nl/graphs/Sp.html.

## Top five **independent** next steps

1. Derive the GF(9) first-order rank-four obstruction directly from Frobenius twists and prove a general rank formula over GF(p^t), checking against the newly materialized four module-extension witnesses.
2. Replace the all-to-all chiral interaction with *bounded-degree* nearest-neighbor W33 incidence couplings; numerically identify whether a K-symmetric local model has separated chiral pure phases and an operationally justified physical reversal.
3. Translate the now-proved **four-layer minimum** into native photon/OAM/time-bin control; minimize *total* SWAP count (currently 27–36), waveguide crossings and loss, preserving the unstructured matching model.
4. Implement and certify an **actual** 5-qutrit or Reed–Muller magic-state distillation map for the exact |M+> injection target; calculate success probability, noise-suppression curve and logical-resource overhead.
5. Search for a **different, physically justified** local W(3,q) kinetic Hamiltonian that avoids both the positive-gap theorem and the diameter-two locality obstruction. Demand scaling of propagators, spectral dimension and causal behavior before making continuum-gravity claims.
