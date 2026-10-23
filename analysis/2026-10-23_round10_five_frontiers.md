# W33 / H27 round ten — five independent research frontiers and a native GQ(2,4) plaquette bridge

**Date:** 23 October 2026. **Status:** exact algebra + finite computational certificates + explicitly separated physical conjectures.

**Reproducer files:**
- `analysis/w33_20261023_char2_allt_C_jordan.py`
- `analysis/w33_20261023_native_full_qutrit_chirality.py`
- `analysis/w33_20261023_heralded_double_Z.py`
- `analysis/w33_20261023_native_plaquette_ward.py`
- `tests/test_w33_20261023_round10_five_frontiers.py`
- Frozen `data/PART_20261023_{CHAR2_ALLT_C_JORDAN,NATIVE_FULL_QUTRIT_CHIRALITY,HERALDED_DOUBLE_Z,NATIVE_PLAQUETTE_WARD,SWAPCOUNT_34_ROUND10}.json`.

The work respects existing Pass12189–12198 reservations, prior all-prime modular representation work, and the four-layer W33 routing proof. **No theorem of everything, quantum gravity, optical fault tolerance or physically selected arrow of time is claimed.**

## Frontier 1: all-`t` characteristic-two **C-module** Jordan law, not an unjustified all-`t` extension claim

For `q=2^t`, let `C_q=row(B_q)` over `F2`. The already established Lucas/Hamada monomial description yields, after extending scalars to Fq, the t-fold Frobenius-twisted tensor product of natural four-dimensional symplectic modules:

```text
C_q ⊗_F2 Fq  ≅  ⊗_{i=0}^{t-1} V^(2^i).
```

A nonzero symplectic transvection `T` is an involution. On each natural module `V`, `T-I` has rank one, so under the cyclic group C2 the factor decomposes as `J2 ⊕ J1 ⊕ J1`. In characteristic two, `J2` is a free module and tensoring any module with it yields free summands; precisely `J2⊗J2=J2⊕J2` and `J2⊗J1=J2`.

Expanding `(2J1+J2)^{⊗t}`, a `J1` factor survives only if all t choices come from the trivial sectors. Their multiplicity is `2^t=q`. Since total dimension is `4^t=q²`, the rest is `q(q-1)/2` copies of `J2`.

**Algebraic theorem (with the prior Frobenius tensor description as an explicit hypothesis):**

```text
C_q|<T>  ≅  J1^q ⊕ J2^[q(q-1)/2],
rank_F2((T-I)|C_q) = q(q-1)/2  for all t>=1.
```

It reproduces the independent exact `q=4,8,16` ranks 6,28,120. It is a derived representation corollary rather than a claimed novel p-rank theorem. **Crucially, it does not establish the analogous theorem for K=C^perp or the connecting-map rank**. Existing finite results: `rank delta1=0` for q4,8,16 (cyclic extensions split) versus `rank delta1=4` for q9. All-characteristic Frobenius extension classification remains open.

## Frontier 2: complete nine-dimensional Weyl-operator mixing can lift the spectator degeneracy

In the *actual* two-qutrit space of dimension nine, define

```text
H0=(I-9Pi)/2,    Pi|a,b>=|-a,-b>,
O=[Re(X_1),Re(Z_1)]/(2i),    O(O²-9/32 I)=0.
```

The previous abstract Ising reduction required choosing a two-level subspace. Instead choose **explicit onsite Pauli-algebra observables**

```text
M1 = Re(X_1),
M2 = Re(X_1) + (1/3)Re(X_2) + (1/5)Re(Z_2).
```

Both are real, parity even, commute with H0, and do not commute with O. The matrix element `||P_+ M1 P_-||_F=1.299038105676658` verifies genuine mixing between positive- and negative-O sectors without assuming a toy spin.

Diagonalize the physical nine-by-nine onsite tensor products for the two-site Hamiltonian

```text
H2(h,M) = H0⊗I + I⊗H0 - O⊗O -h(M⊗I+I⊗M).
```

Both versions satisfy entrywise reality: `K H2 K^-1=H2` with computational conjugation K. For M1, a fourfold *spectator* degeneracy remains at h=.05,.1,.2. M2 produces a **unique ground level with a positive spectral gap** at all those tested h:

| h | Ground multiplicity M1 | Ground multiplicity M2 | gap M2 |
|---:|---:|---:|---:|
| 0 | 8 | 8 | 0 |
| .05 | 4 | 1 | 0.00982827555 |
| .10 | 4 | 1 | 0.0375 |
| .20 | 4 | 1 | 0.09797958971 |

This is exact-to-floating precision finite-matrix evidence, not a closed-form proof that every positive h has a unique ground level. It is **not** physical spontaneous T breaking: in fact its unique finite ground state *does not* choose one sign of a K-odd order parameter. Infinite volume and a physically justified antiunitary reversal are still missing.

## Frontier 3: unrestricted four-layer SWAP minimization remains unresolved

Re-run the previously established fully unrestricted W33 collinearity-graph four-layer CP-SAT solver with **34 SWAPs maximum**. Result: `UNKNOWN` after approximately 30 seconds, 232,691 branches and 34,589 conflicts. This is **not** proof of either feasibility or infeasibility.

The prior three-layer **INFEASIBLE** proof and the certified four-layer, 36-SWAP circuit remain valid. Parity and transport give

```text
4 parallel layers are necessary and sufficient;
28 <= total edge SWAPs <= 36, possible counts 28,30,32,34,36.
```

No false "36 is gate optimal" claim. Hardware depth/fidelity still requires actual waveguide routing measurements.

## Frontier 4: complete single- and double-site Z-fault *integer-cyclotomic* census for Pass12189

The native Pass12189 heralded instrument uses all 3^10=59,049 codewords of each of three logical cosets, with ideal acceptance `S0=29/81`. The existing single-fault study shows four accepted single-site Z errors, located at the chosen representative's four-coordinate support `u={0,1,2,3}`.

This packet independently recomputes all forty singles and **all 780 unordered pairs** of distinct single-qutrit `Z` errors. For every pair, preserve exact nine-entry integer phase histograms for each logical coset and reduce the polynomial in `zeta9` using its minimal polynomial

```text
Phi9(z)=z^6+z^3+1.
```

A branch is *exactly zero*, not merely below a floating threshold, iff each histogram obeys `h0=h3=h6`, `h1=h4=h7`, and `h2=h5=h8`. An exact-remainder check verifies all 780 pair accept/reject classifications.

Only **6 / 780 pairs** survive: the six unordered pairs inside `{0,1,2,3}`; each has numerical success `2/81` and conditional fidelity `1/58` (consistent with the exact integer histogram algebra). The other **774** pairs are exactly rejected.

For independent Bernoulli Z-error probability p at each of the forty physical positions, expand the full convolution of zero, one and two fault outcomes:

```text
P_accept(p)=29/81 - (128/9)p + (2480/9)p² + O(p³).
F_cond(p)=1 - (228/841)p - (14706/24389)p² + O(p³).
```

These coefficients can also be derived by exact rational arithmetic from the now-certified accepted single/double support sets, survival weights and fidelities. **Boundary:** This is one Pauli Z channel and excludes simultaneous ≥3 faults, X/errors of other charges, measurement faults, faulty Clifford operations, photon loss, all syndrome branches and decoding. It is NOT a magic distillation threshold or a physical device reliability estimate. The third-order remainder is not negligible for arbitrary p.

Prior art: Anwar–Campbell–Browne, *Qutrit Magic State Distillation* (2012), https://arxiv.org/abs/1202.2326; Campbell–Anwar–Browne, *Magic-State Distillation in All Prime Dimensions Using Quantum Reed–Muller Codes*, https://arxiv.org/abs/1205.3104. Their codes/protocols must not be equated to the specific W33 heralded CSS instrument tested here.

## Frontier 5, bonus: actual native 27-point voltage graph is a GQ(2,4) *plaquette complex*

Take the existing Pass11991/12192 connected 27-vertex, 135-edge H27 voltage cover with **integer primitive four-dimensional edge voltages V**, not a hypothetical 4D square grid.

On its base graph, exact enumeration finds **45 triangles**, five through every vertex, one along every edge. A stronger check verifies its adjacency SRG parameters `(27,10,1,5)` and the *defining generalized-quadrangle axiom*: for every triangle/line L and every point p outside L, exactly one vertex of L is adjacent to p. Thus the actual native graph/line incidence realizes `GQ(2,4)`, the same 27/45 finite-geometric scale encountered elsewhere in W33/E6 studies (its mathematical identification may be known; we claim the explicit voltage-gauge verification, not priority for GQ(2,4)).

Each triangle has **zero total period voltage** in all four integer directions. Every triangle therefore closes as a genuine three-edge plaquette in the infinite periodic cover; none wraps nontrivial translation. Let `D(k)` be the 135×27 Bloch-incidence matrix, with entries `-1` at the tail and `exp(i k·V_e)` at the head. Define the 45×135 plaquette curl `F(k)` by oriented traversal, with the correct prefix Bloch phases. Exact algebra gives

```text
F(k) D(k) = 0       for every real k in four dimensions,
F(k)(a+D(k)chi)=F(k)a.
```

All 45 curl rows are independent (they have disjoint edge support) for all k, not just at one sampled momentum. Numeric controls certify

```text
rank D(0)=26,     rank F(0)=45;
rank D(k)=27,     rank F(k)=45  for tested k!=0.
```

The finite base triangle 2-complex has **b0=1,b1=64,b2=0**, Euler characteristic **-63**. Corresponding generic tested Bloch twisted H1 dimension=135−27−45=63. The four independent voltage directions from Pass11991/12192 live in the long-cycle sector; they are **not** four gauge polarizations or four spacetime dimensions derived solely from the 45 triangles.

This is a genuine **microscopic cochain gauge Ward construction on the native edges**, stronger than the previous abstract 4×6 coarse-grained wedge model. It does not yet define a nontrivial electric kinetic energy, Gauss generators or local Lorentzian Maxwell action, nor demonstrate physically propagating photons/gravitons. A family of plaquette curls is **not** a complete gauge theory; the 63–64 unfilled cycle classes and gauge-fixed path integral still require analysis.

## Independent high-impact next experiments

1. Derive `rank delta_k` for `GF(p^t)` symbolically; use the new all-t `C`-module formula and GF16 split vs GF9 rank-4 non-split as strict validation constraints, without incorrectly deducing K from C alone.
2. Test the full nine-dimensional onsite mixing on **growing bounded-degree graphs**, identify actual antiunitary symmetry and evaluate whether chiral susceptibility diverges in a controlled thermodynamic sequence.
3. Resolve 28–36 **total SWAP count** with symmetry-broken SAT/ILP and checkable proof logs. Separate unconstrained per-layer matchings from photonic timing/loss.
4. Compute **triple-site Z faults**, mixed X/Z faults and postselection/decoder branches, and connect the exact p² magic budget to a literature-correct distillation map with the right target attractor.
5. Construct a true **native gauge Hamiltonian**: electric operators on 135 edge links, magnetic operators from the 45 zero-voltage plaquettes, Gauss constraints at all 27 vertices, and nontrivial flux/holonomy dynamics. Verify [Gauss,H]=0, identify the role of the 64 long-cycle modes, and only subsequently explore Lorentzian propagation or coupling to E6/internal W33 fields.
