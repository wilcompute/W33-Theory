# Round 9: GF(16) extension splitting, chiral tunneling, W33 routing, heralded fault slopes and native four-dimensional Ward identities

**23 October 2026.** This packet continues five independent open fronts of the W33 research program. It reuses and cites existing repository claims without silently promoting old material to novelty. It does **not** solve a theory of everything, build photonic hardware, demonstrate Lorentz covariance, produce a magic-state distillation threshold, or derive an emergent physical time arrow.

**Reproduction:** `analysis/w33_20261023_gf16_first_order_obstruction.py` and `analysis/w33_20261023_round9_five_frontiers.py`. Controls: `tests/test_w33_20261023_round9_five_frontiers.py`. Frozen data: `data/PART_20261023_GF16_FIRST_ORDER_OBSTRUCTION.json`, `data/PART_20261023_ROUND9_FIVE_FRONTIERS.json`, and `data/PART_20261023_SWAPCOUNT_28_SEARCH.json`.

## 1. GF(16): a **splitting** certificate at 4,369 coordinate points

The prior round had computed GF(4), GF(8), GF(9). Here construct GF(16)=F2[z]/(z^4+z+1), all n=(17)(257)=4,369 points of PG(3,16), the B noncollinearity rows, and the transvection `T_w:x -> x+omega(x,w)w`. Build `C=im B` over F2, `K=C^perp` by an actual nullspace basis and set D=T-I. Packed integers give **exact** F2 Gaussian elimination, not numerical estimation.

| q | n | dim C | dim K | rank D(C) | rank D(K) | dim(DK ∩ C) | rank delta_1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 4 | 85 | 16 | 69 | 6 | 26 | 6 | 0 |
| 8 | 585 | 64 | 521 | 28 | 228 | 28 | 0 |
| 16 | 4,369 | 256 | 4,113 | 120 | 1,928 | 120 | **0** |

Here `delta_1:ker(D|K/C)->C/D(C)` is induced by D on a lift, and
`rank delta_1 = dim(DK∩C)-rank D(C)`. The zero obstruction at q=16 validates an expanded characteristic-two pattern. In characteristic two, the cyclic transvection group is C2, whose group algebra is F2[D]/(D²) and whose indecomposables are `J1` and the free/projective `J2`. Therefore `delta_1=0` implies this short exact sequence **splits as a module for the single involution**. It does not establish splitting under all Sp(4,16).

The contrasting previously established GF(9) rank-delta1=4 is unchanged. A *symbolic general q=p^t Frobenius decomposition*, even across all 2^t, is still open. The known Hamada p-rank alone does not determine this extension obstruction.

## 2. Noncommuting chirality: finite-size K-even tunneling rather than a false time arrow

The preceding W33-edge model is `H_W33=sum H0_i-sum_edges O_i O_j`, with local `O` eigencharges +a,-a,0 and `a²=9/32`. It is diagonal in the joint O basis, allowing exact finite-size polarized sectors but **no tunneling**.

Select a K-exchanged local +a/-a pair (a two-dimensional onsite subspace) and add a **K-even local flip** `-h X_i` between the pair. In that chosen low-energy sector this becomes the transverse-field Ising Hamiltonian

```text
H = -(9/32) sum_(ij in E_induced) Z_i Z_j
    -h sum_i X_i
    -epsilon sum_i Z_i .
```

At epsilon=0 the antiunitary is `K=(tensor X_i) complex conjugation` and `KHK^-1=H`. For h>0, connectedness under spin flips makes the matrix irreducible stoquastic; Perron–Frobenius gives a **unique** finite-size ground vector. As K is a symmetry, the ground expectation of the odd total Z order parameter is exactly **zero**, not spontaneously selected.

The producer solves n=2,4,6,8 **connected W33-induced subgraphs** (not arbitrary mean-field graphs) for h=0,.1,.2, and checks the sign reversal of a small epsilon. For two sites, the splitting is exactly

```text
gap_2(h) = sqrt((9/32)^2 + 4h²) - 9/32.
```

The largest circuits are only 2^8 dimensional. This is a **controlled diagnosis of the missing dynamics**: adding noncommuting transitions permits tunneling, and it destroys any claim of a finite-size nonzero source-free chiral expectation. Any thermodynamic symmetry-breaking phase must be proved in a specified growing graph sequence, with physically identified time reversal and nontrivial spatial locality. W33 diameter2 is not Euclidean locality. The selected onsite two-level pair and its mixing gate are engineering assumptions, not derived from the bare 40-point geometry.

## 3. Gate count remains open: an additional genuine bounded search, no guessed optimum

The previous exhaustive CP-SAT certificate proves 3 matching layers **INFEASIBLE** and constructs a four-layer transvection route with 36 edge-SWAPs. The even-permutation parity lower bound establishes **28 <= N_SWAP <=36**.

To attack exact gate-count optimization we re-executed the fully unrestricted four-layer CP-SAT model with a strict budget of at most **28** swaps, an independently frozen deterministic solver seed and 35-second cap. It explored 182,838 branches and 35,713 conflicts, but finished **UNKNOWN**. The prior 35-SWAP-budget search also finished UNKNOWN.

**Neither result rules out 28,30,32 or34 SWAPs.** This pass adds a well-formed, reproducible constraint-solving control and a clearer search-complexity baseline, *not* an unsupported new minimum. The code stays independent of the known hub architecture.

## 4. Integrated Pass12189 heralded magic **first-order** fault-response law

The parallel Pass12189 packet (already on `master`) provides an exact rank-three heralded qutrit instrument with ideal success `S0=29/81`. It stores all 40 per-site physical Z-after-gate fault controls; **only sites 0,1,2,3** are accepted nontrivially. For each, the fault branch succeeds with probability `2/81` and has ideal-state fidelity `1/58`.

Assume each of the 40 Z faults is independent with probability p, and expand the accepted instrument to first order (no other noise sources). The no-fault term is `(1-40p) S0`; each single-fault term is `p S_i`. Hence

```
P_accept(p) = 29/81 - (128/9) p + O(p²).
F_conditional(p) = 1 - (228/841) p + O(p²).
```

These derivatives are computed from the **actual frozen Pass12189 branch data**, not inferred from code distance. Accepted faults carry very poor conditional fidelity and therefore can defeat naive claims of first-order fault suppression. The numeric table at p=0, 0.0001, 0.001 and 0.01 is only the *single-fault-truncated rational model*. Values at finite p are not the full independent-error channel, where multiple simultaneous faults contribute.

This is **a quantitative noise-budget bridge**, not magic distillation or a decoder. The known qutrit magic-distillation literature includes Anwar–Campbell–Browne (arXiv:1202.2326), Campbell–Anwar–Browne (arXiv:1205.3104), and Prakash–Singhal (Phys Rev A 113, 042404; 2026). We do not claim to have reproduced a complete distillation map or threshold.

## 5. Native periodic 4D acoustic metric -> exact discrete **Euclidean gauge Ward template**

Pass11991 already supplies the connected periodic H27 carrier (27 sites, 135 edges per Z4 unit cell); Pass12192 supplies its **four-dimensional Euclidean acoustic dispersion** and metric. Read `graph_inputs()` from `analysis/w33_pass12189_12193_five_bridges.py`, rather than substituting a generic identity metric.

The actual acoustic `G` is

```text
[10/27,  5/27, -6/27,     0]
[ 5/27, 10/27,     0, -6/27]
[-6/27,     0, 12/27, -6/27]
[    0, -6/27, -6/27, 12/27].
```

Its capacity is `rho=sqrt(det G)=2/27`; the dimensionless four-dimensional quadratic form `Q=G/rho` is

```text
[  5,  5/2, -3,  0]
[5/2,    5,  0, -3]
[ -3,    0,  6, -3]
[  0,   -3, -3,  6].
```

For periodic quasi-momentum k, let `p_mu=e^(ik_mu)-1`, `z=sqrt(Q) p` (choose a real positive square root). Define the site-to-frame gradient `d0=z` and the six-by-four antisymmetric cochain curl

```text
(d1 a)_(mu,nu) = z_mu a_nu - z_nu a_mu.
```

**Exact:** `d1 d0=0`, so the Maxwell-like positive operator `M=d1† d1` satisfies the Ward identity `M d0=0`, and `d1(a+d0 alpha)=d1(a)` for any complex alpha. For any nonzero z it has eigenvalues `{0,s,s,s}` where `s=z†z`. Thus the three **off-gauge Euclidean four-vector** modes inherit precisely the same low-k quadratic form `k^T Q k` as the previously certified native acoustic branch. Four refinements N=8,16,32,64 give decreasing relative dispersion errors approximately .1696, .0450, .01142, .002865 for k=(2pi/N)(1,2,1,0).

**Critical layer boundary:** This supplies a new explicit **mathematical gauge-invariant cochain template using the native computed G**. It does NOT show that a microscopic photon gauge field exists on the 27-site circuit, nor select a Lorentzian time direction, produce two physical photon helicities, derive Einstein equations, or yield dynamical equations for the weight-dependent metric. In four *Euclidean* dimensions, three off-gauge vector modes are not a counting of physical photons; obtaining two requires additional Lorentzian constraints and dynamics. The native periodic carrier is not simply the W(3,q) diameter-two graph.

## Additional cross-track observation

The contrast between the *symmetric but gapped scalar 40-point carrier* and the *periodic four-dimensional acoustic carrier with a gauge-Ward template* suggests a precise research division: use finite W33/H27 symplectic structures for **internal operators / logical gates**, and use a genuinely growing periodic cover for **spacetime kinematics**. A coupling between them must preserve finite-code error correction and emergent gauge Ward identities; none is derived in this packet.

## Five independent next steps

1. Derive a symbolic **all-extension** formula for the transvection connecting ranks `delta_k`, checking GF16 splitting against GF9 nonsplitting and Frobenius component structure, rather than extrapolating the classical Hamada rank.
2. Embed a **K-even noncommuting chiral mixing operator** directly in the full 9D two-qutrit onsite Pauli algebra, then determine the gap/susceptibility on growing bounded-degree graphs (not just n<=8 induced subgraphs of one W33).
3. Improve the **28/30/32/34 SWAP budget search** with symmetry breaking, SAT proof logging or independent mathematical cuts. Report UNKNOWN honestly; do not replace feasibility search timeouts with optimality claims.
4. Produce an actual **low-level magic distillation/decoding round** and propagate all single-/double-fault channels; the -228/841 slope gives a new falsifiable first-order benchmark for the heralded state factory.
5. Construct a **microscopic cochain gauge field** on the native 27-site voltage cover that homogenizes to the present Q-dependent d0/d1, including an independently justified Lorentzian time direction and a physical Ward/constraint law. Do not infer gravity from Euclidean spectral dimension alone.
