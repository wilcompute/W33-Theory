# W33 round eight — Frobenius checks, local chirality, swap-count boundary, five-qutrit magic, and orbital continuum obstruction

**Date:** October 23, 2026

**Producer:** `analysis/w33_20261023_five_frontiers_round8.py`; `analysis/w33_20261023_swapcount_optimization.py`

**Controls:** `tests/test_w33_20261023_five_frontiers_round8.py`
**Data:** `data/PART_20261023_FIVE_FRONTIERS_ROUND8.json`, `data/PART_20261023_SWAPCOUNT_35_SEARCH.json`

The packet addresses five independent open problems and a bonus connection after round7, reading the incoming parallel Pass12189–12193 report. The track boundaries matter: 12189 already owns a **29/81 heralded magic state** with accepted fault controls; 12192 already owns a **native four-dimensional periodic Bloch/acoustic carrier**. This packet does not duplicate or supersede either. It neither establishes a TOE nor derives Einstein gravity, observed photonic hardware, a physical arrow of time, or a fault-tolerance threshold.

## 1. An independent elementary proof of the **already-known** all-prime-power p-rank

Let q=p^t and B be the `n=(q+1)(q²+1)` square matrix of symplectic projective noncollinearity:

```text
B_xy = 1 if omega(x,y) != 0, else 0.
```

Since `z^(q-1)` equals 1 for z !=0 and zero at z=0, the y-th column is the evaluation of `omega(x,y)^(q-1)`. Expand this expression as a polynomial in the four y coordinates. Every coordinate exponent is less than q. Tensor-product Vandermonde interpolation over Fq extracts *all* monomial coefficients as Fq-linear combinations of the evaluations at y∈Fq^4 (including the zero vector, which adds nothing); conversely every column is a combination of these coefficients.

For exponents a_0+...+a_3=q-1, the corresponding multinomial coefficient survives mod p precisely if addition in base p has **no carries** (Lucas for multinomials). Each of the t digit columns of q-1 has value p-1, and there are `binom(p+2,3)` ordered four-tuples of nonnegative digits summing to p-1. Thus the number of surviving independent coefficient monomials is `binom(p+2,3)^t`.

Each such monomial has total degree q-1, is invariant under projective scaling, and is a linearly independent polynomial *function* on Fq^4 because every individual exponent is <q. Finally B has Fp entries, so extension of scalars from Fp to Fq does not change rank. Therefore

```
rank_Fp B = binom(p+2,3)^t.
```

**Important literature and repository priority guard:** This p-rank formula is *already known* (Hamada/projective incidence theory) and was present before this pass in `analysis/w33_20261022_allq_pascal_CSS_exact_distance.py`. The increment here is a short, stand-alone coefficient-interpolation proof and independent q=3,4,8,9 matrix controls, not novelty of the formula and **not** the still-open all-q Frobenius connecting-map ranks (GF9 rank delta1=4 already has explicit witnesses from round7).

## 2. The source-free chiral model can be localized on the W33 **graph edges**

The prior `H_N=sum H0_i-(1/N)(sum O_i)^2` was all-to-all. Replace the interaction by **one operator per actual W33 collinearity edge**:

```
H_W33 = sum_(i=1)^40 (I-9Pi_i)/2 - sum_{{i,j} in E(W33)} O_i O_j,
O=[Re(X1),Re(Z1)]/(2i),   O(O²-9/32 I)=0.
```

The 40-vertex 12-regular W33 graph has exactly 240 edges. The local Hermitian operators commute with their own parity-derived onsite Hamiltonians, and operators on different sites commute. Every site contributes at least -4, every edge at least -9/32, hence

```
E0 >= -4*40 - 240*(9/32) = -227.5.
```

Equality holds exactly when all sites are ground states with `O_i=+3sqrt2/8` or all `O_i=-3sqrt2/8`. Connectedness of W33 forbids mixed signs in a ground state. Each sign eigenspace has **two** onsite choices, giving exact ground multiplicity `2*2^40=2^41`. Global computational-basis complex conjugation K changes all signs, leaving H invariant.

We obtain mathematically **local on the W33 graph**, K-symmetric, opposite chiral sectors *without an external odd source*. The one-site zero-charge defect costs exactly `12*(9/32)=27/8`; a sign-flip costs `2*12*(9/32)=27/4`.

W33 also has an expander/domain-wall inequality. Its nontrivial adjacency eigenvalues are 2,-4. For any vertex subset S,

```
cut(S) >= (12-2)|S|(40-|S|)/40.
```

Thus a half-system sign domain with |S|=20 has at least 100 boundary edges and a cost of **at least 56.25** energy units relative to the polarized sector. The lower bound is an exact spectral-graph consequence, not simulation.

**Physical firewall:** This is a commuting mean-field-style onsite operator model with W33 *edge*-coupling, not Euclidean/causal spacetime locality (W33 has graph diameter2). There is exact finite-N degeneracy, no proven tunneling dynamics, and the chosen basis conjugation K need not be the actual physical time reversal. Graph-site permutation symmetry is not equivalent to full internal two-qutrit Clifford covariance. It is not spontaneous physical time or cosmological chirality.

## 3. The unrestricted SWAP **count** is still open, but parity tightens the bound

The previous fully unrestricted CP-SAT model proved parallel depth3 **INFEASIBLE** and produced an exact depth4, 36-A-edge-SWAP circuit. Thus `D_min=4` was already resolved.

The nine moving cycles are each 3-cycles and therefore even permutations. Their product has sign+1. Every SWAP is a transposition, so **every exact implementation uses an even total SWAP count**. Combining this with the earlier transport-distance bound `N>=27` gives

```
28 <= N_SWAP <= 36,
N_SWAP in {28,30,32,34,36}.
```

I also built an **unrestricted four-layer gate-budget CP-SAT model** with `sum(active vertices) <=70`, i.e. at most35 SWAPs (equivalently at most34 due parity). The time-limited 40-second result is **UNKNOWN**, *not* INFEASIBLE. It does not justify any claim that 36 SWAPs is the global optimum. The exact bounded search report and reproductive solver source are frozen, to permit later proofs or discovery of a 34-swap circuit.

## 4. A genuine [[5,1,3]]_3 projector exposes a ninth-root magic mismatch

Rather than assume that a known five-qutrit distiller automatically works for our required phase resource, construct the **actual** cyclic qutrit five-body stabilizers (x-coordinates | z-coordinates in F3, row strings in the certificate). The four generators commute and define a rank-three code projector

```
P = prod_(j=1)^4 (I+G_j+G_j²)/3.
```

The canonical logical frame is fixed by logical Z=`Z^tensor5` and logical X=`(X^tensor5)^2`. Prepare five *perfect copies* of

```
|M+>=(|0>+zeta9|1>+zeta9²|2>)/sqrt3,
```

project onto the trivial stabilizer syndrome and decode. Exact-to-numerical-tolerance 243-dimensional calculations give:

```
success probability P0 = 0.03978052126200278,
max_(C in single-qutrit Clifford group) |<M+|C|psi_out>|²
      = 0.9182226590143102.
```

All 216 projective single-qutrit Cliffords were explicitly enumerated. **Conclusion:** this bare trivial-syndrome, five-copy projection cannot act as an exact fixed-point distiller of the *same* ninth-root `|M+>` target under a single logical Clifford correction, even from five perfect input copies. The code may distill other nonstabilizer states; pre-twirling, different branches, multi-round/more general transformations, and known proper qutrit protocols are NOT ruled out. This is a *specific implementation diagnostic* rather than a no-go against qutrit distillation.

The parallel Pass12189 already gives a different successful heralded W33 nonstabilizer preparation with exact probability29/81; our result does not conflict with it. Relevant prior work: Anwar–Campbell–Browne, arXiv:1202.2326 and Prakash–Singhal, Phys. Rev. A 113, 042404 (April2026) on threshold searches.

## 5. Rigorous all-q **rank-three orbital symmetry** versus scalar continuum dynamics

The finite symplectic group Sp(4,q) acts transitively on projective points. Its action on ordered pairs has exactly **three orbits**: x=y, distinct x orthogonal to y, and x nonorthogonal to y. (A linear-algebra consequence of Witt's lemma.) Therefore its permutation centralizer algebra on scalar complex-valued functions is exactly

```
End_Sp4(q)(C[PG(3,q)]) = span{I,A_q,B_q}.
```

Equivalently any **fully symplectic-equivariant scalar Hamiltonian** has form `aI+bA_q+cB_q` and at most **three distinct eigenvalues** for *all* q. No nonzero simple undirected, fully invariant loopless graph can maintain bounded vertex degree: any such graph uses one or both orbitals and has degree `q(q+1)`, `q³` or `q(q+1)+q³`.

The script independently verifies the strong regularity relation `A²=kI+(q-1)A+(q+1)B` and orbit cardinalities for q=3,4,8,9. This is classical rank-three association-scheme mathematics; the *TOE-relevant consequence* is rigorous:

**A putative scalar W(3,q) continuum model cannot simultaneously retain full Sp4(q) symmetry, have growing multiband spectral structure and preserve a nontrivial uniformly bounded graph degree on these same points.** Possible escapes include growing internal fibers/spins, only subgroup symmetry, physically justified interaction graphs, or a different periodic carrier.

The already constructed Pass11991/12192 periodic Z4-voltage carrier and native four-dimensional Bloch scaling *is a separate, promising kinematic escape*. It supplies a spectral dimension-four **periodic lattice** but still lacks Lorentzian dynamics/Einstein constraints. Neither construction currently supplies quantum gravity.

## Five independent next experiments

1. **Actual Frobenius connecting ranks:** Derive `rank delta_1` and `rank delta_2` over GF(p^t) from the tensor-factor module filtration rather than extrapolating known Hamada rank and GF9 examples; test GF16 and GF27 with sparse symbolic operations.
2. **Local chirality with tunneling:** Add a justified, K-even noncommuting onsite transition to the W33 edge-local model; calculate gap splitting and ground-state chiral susceptibility, then explain how source-free selection could emerge in an appropriate growing graph sequence.
3. **Prove exact minimum SWAP count:** Search specifically for 34 swaps at depth4 or derive a >34 transposition lower bound; exploit permutation parity, edge-cut transport and SAT symmetry reduction. UNKNOWN is inconclusive, not a proof.
4. **Working qutrit magic distillation:** Implement an actual literature-approved five-qutrit/ternary Reed–Muller distillation round for *its genuine target magic attractor*, then map the prepared resource to the required ninth-root ancilla by a verified Clifford hierarchy circuit.
5. **Geometric continuum escape:** Integrate the Sp4 scalar-commutant no-go with the native 4D voltage-cover Bloch carrier: identify the minimal additional internal bands/gauge fields and derive a real, local propagator and Ward constraints before proposing gravity.
