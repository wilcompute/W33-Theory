# Five independent W33 follow-ups: finite extension, microscopic clocks, optimality gap, coherent logic and growing fields

**22–23 October 2026.** This packet executes the five nonsequential fronts proposed after the exact GF9 control distinction. It builds on (rather than repeats) Pass12187's all-prime Q Jordan proof and the previous verified W33 A-graph six-layer circuit. Computed objects are mathematical, not verified photonic hardware or a theory of everything.

Producer: `analysis/w33_20261022_five_followups_round5.py`.
Regression: `tests/test_w33_20261022_five_followups_round5.py`.
Frozen certificate: `data/PART_20261022_FIVE_FOLLOWUPS_ROUND5.json`.

## 1. All-prime extension is detected only at higher nilpotent order

Let `C=row B`, `K=C^perp`, `Q=K/C` be the point-coordinate Pascal code sequence on W(3,p), and D=T-I for a nonidentity symplectic transvection. Prior verified theorems give the Jordan types of all three modules. For each k>=1 define a **canonical connecting map**

```text
delta_k: ker(D^k | Q) -> C / D^k C,
delta_k([z]) = [D^k(z_lift)],
```

where z_lift in K is any lift. This is well-defined, because D^k(z_lift) lies in C when [z] is killed by D^k; changing the lift by c in C changes D^k(z_lift) only by D^k c.

The kernel of delta_k is the image of ker(D^k|K) in ker(D^k|Q), whose kernel equals ker(D^k|C). Therefore

```text
rank delta_k
 = dim ker(D^k|Q) - dim ker(D^k|K) + dim ker(D^k|C)
 = rank(D^k|K) - rank(D^k|Q) - rank(D^k|C).
```

Substituting the exact all-prime Jordan rank laws and simplifying proves

```text
rank delta_k = (k-1)(p-k)(p+1)/2,  for 1<=k<=p.
```

This is **zero for k=1** even though the sequence is nonsplit for p>=3; the first nontrivial obstruction appears at k=2, where rank delta_2=(p-2)(p+1)/2. The maximum occurs near k=(p+1)/2. Arithmetic independently checks primes 2,3,5,7,11,13,17,19,23,29,31.

This is a concrete **higher-order extension/Bockstein-style invariant**, not the full isomorphism class of an arbitrary extension. The q=p^t Frobenius-twist interaction was not resolved; the prime-field polynomial shortening proof cannot simply be promoted to extensions by replacing p with q.

## 2. Microscopic two-qutrit Pauli clock and the unavoidable external time-reversal source

Use the actual W33 interpretation as nonidentity projective two-qutrit Pauli directions, indexed by x=(a,b,c,d) in F3^4. Let X|j>=|j+1>, Z|j>=omega^j|j>, omega=e^(2pi i/3). A Hermitian-compatible displacement is

```text
D_(a,b) = omega^(2ab) X^a Z^b,
W_x = D_(a,b) tensor D_(c,d).
```

D_x^dagger=D_(-x), so the symplectic projective direction [x] uniquely determines the real observable Re(W_x)=(W_x+W_x^dagger)/2. An exhaustive check of all 780 distinct pairs proves **W_x and W_y commute exactly when x,y are collinear in W33 A** (up to numerical 1e-9 tolerance in complex evaluation; the commutator relation is algebraic).

Construct the microscopic two-qutrit Hamiltonian

```text
H0 = - sum_(40 projective directions) Re(W_x).
```

Its nine-dimensional exact spectrum (integer eigenvalues certified numerically) is -4 with multiplicity5, +5 with multiplicity4; this is a finite Wigner-parity-type sum, not a propagating many-body field.

Choose computational-basis complex conjugation K as a candidate antiunitary reversal. H0 is real in this basis and satisfies K H0 K^-1=H0. Let

```text
J_X = (X_1-X_1^dagger)/(2i),
H(kappa)=H0+kappa J_X.
```

The current J_X is Hermitian and K-odd, and
K H(kappa) K^-1=H(-kappa), so H(+1) and H(-1) have identical spectra. With the source parameter kappa held fixed and nonzero, the model is not K-invariant. **No spontaneous time-reversal violation follows**, because the odd source was explicitly inserted. Moreover K is a *chosen basis antiunitary*, not independently justified as the physical time-reversal operator of photon/qutrit hardware.

This supplies a truly microscopic **operator-algebra candidate** and exposes the gap between discrete commutation geometry and a derived time arrow.

## 3. Exact 40-anchor W33 collinearity SWAP depth 4 — improvement from depth 6

For each point-anchor symplectic transvection, 13 of forty coordinates are fixed and the other 27 lie in nine disjoint 3-cycles (a b c). The three vertices of each cycle are pairwise **nonadjacent in collinearity graph A** (though they form a B triangle). Crucially, they have **exactly four common neighbors in A**, all among the 13 fixed points.

A bipartite augmenting-path matching assigns each cycle its own hub h, avoiding every moving endpoint. For a cycle with target permutation a->b->c->a, execute the four A-edge position SWAPs

```text
SWAP(h,a), SWAP(h,b), SWAP(h,c), SWAP(h,a).
```

The hub returns to its original state; the three nonadjacent endpoints realize precisely the desired 3-cycle. For all nine cycles, disjointness of the hub assignments makes each stage executable in parallel. Thus **each of the forty symplectic transvections has a verified schedule of 36 A-edge SWAPs in only 4 parallel layers**. The certificate freezes every hub and all four layers for each anchor; the verifier independently replays the exact induced 40-label permutation.

Improved exact complexity interval:

```text
27 <= minimum A-edge SWAP count <= 36,
 3 <= minimum parallel SWAP depth <= 4.
```

The 27 and 3 lower bounds were established in the preceding pass. Four layers and 36 swaps are verified achievable bounds, **not proven optimal**. A hardware graph implementing these edges as unit-fidelity physical qutrit SWAPs is assumed. Translating to one-photon time-frequency/OAM modulation, loss, cross-talk and photonic syndrome extraction remains an open engineering problem.

## 4. Coherent qutrit ancilla extracts an encoded charge and applies a logical ninth-root phase

The preceding work ruled out applying the *uniform transversal physical* `diag(1,zeta9,zeta9^2)^(tensor40)` followed by **immediate projective syndrome measurement and classical feedforward** as one deterministic encoded unitary. It did not rule out ancilla-mediated logical gates.

A fully reversible, explicit alternative uses a weight-four logical Z representative
`v=(1,1,1,1,0,...,0)` in the repository's projective ordering. Direct computation verifies

```text
Bv=0 mod3, v not in C, v.v=1 mod3.
```

Therefore the ternary charge `q(x)=sum_(i=0)^3 x_i mod3` is **constant on every CSS coset x+C**, and takes values 0,1,2 on the three representative cosets C, v+C,2v+C.

Prepare an extra physical qutrit ancilla in |0>. Apply four controlled-SUM gates (each data coordinate to the ancilla), yielding |x>|q(x)>. Apply the **externally supplied** ninth-root resource `M=diag(1,zeta9,zeta9^2)` on the ancilla, then apply the four inverse SUM gates. Algebraically

```text
|x>|0> -> zeta9^{q(x)} |x>|0>.
```

Because q(x) is constant on each CSS logical coset and the ancilla disentangles *exactly*, the induced operator on the code is the **coherent encoded non-Clifford phase M_L of one logical qutrit**. It acts unitarily on arbitrary encoded superpositions, not merely on computational basis states. The code verifies the full local four-qutrit truth table (81 classical inputs) and 177147 coset basis configurations across the three chosen logical charge values. This constitutes a correct circuit-level solution to the coherence problem for an **already available resource M**.

**Crucial boundary:** A non-Clifford gate has not been distilled, prepared, or obtained transversally for free. The procedure requires one non-Clifford *physical ancilla* gate plus eight two-qutrit SUM/CX operations, with no fault-tolerance or photon compatibility proved. Therefore it does not solve native Holonet universality or contradict the prior transversal+measurement no-go.

## 5. Field-tower escape: exact regular-representation spectral growth

Prior established that restricting two noncommuting transvections to F3-rational directions generates a fixed SL(2,3) group, so the same 13-atom upper bound holds for all extensions q=3^t in that narrow model. The previous q9 control result demonstrated that a tunable shear coefficient outside the square class can enlarge the group to full SL(2,9).

Here we test a deliberately *different*, growing family in the elementary two-dimensional symplectic group, with

```text
U=[[1,1],[0,1]], L_a=[[1,0],[a,1]],
F3, F9=F3[z]/(z²+1), F27=F3[z]/(z³-z-1).
```

Choose the coefficients a=1,4,3 in the script's exact integer field encoding. Full breadth-first multiplication certifies group orders 24,720,19656: respectively the whole SL(2,3), SL(2,9), SL(2,27). These are **actual matrix group closures**, not order guesses.

Build the degree-four undirected Cayley graph generated by U,U^-1,L_a,L_a^-1 and its real symmetric **regular-representation Laplacian**
`L_Cayley=4I-U-U^-1-L_a-L_a^-1`.
Use the rational Krylov vectors `delta_e,L delta_e,L² delta_e,...` and certify their linear independence modulo prime65521. Nonzero modular determinants certify genuine rational independence. Because the Cayley Laplacian is real symmetric, its cyclic Krylov degree is bounded by its number of distinct real eigenvalues.

| Field | Exact generated group order | Certified *lower bound* on distinct Cayley eigenvalues |
|---|---:|---:|
| F3 | 24 | 6 |
| F9 | 720 | 37 |
| F27 | 19,656 | **65** |

At F27 the 65-step cutoff is **not saturated**, so ≥65 is only the current certified lower bound, not an exact count. This exhibits **unbounded-by-13 complexity in the tested finite instances**, demonstrating how broadening the actual generated group can escape the previous *fixed-group* spectral obstruction.

**Essential geometry firewall:** This is the Laplacian of the regular Cayley representation of SL(2,q), NOT the W(3,q) point-coordinate single/two-clock Hamiltonian. The result neither establishes an actual q->infinity limit nor a Weyl law, spectral dimension, local causal propagation, relativistic field dynamics, or gravity. Identifying a physical implementation and an operator family with such properties is still open.

For background, the general symplectic-transvection generator `T_(v,lambda)(x)=x+lambda omega(x,v)v` and generation of symplectic groups are classical group theory (e.g. Robert A. Wilson, *The Finite Simple Groups*, chapter on symplectic groups). No global mathematical priority claimed.

## Five strongest independent next steps

1. **Extension Frobenius problem:** Materialize the connecting maps delta_k with explicit canonical matrices at q=4,9 and test how Frobenius-twisted polynomial evaluation changes the filtration.
2. **Physical time dynamics:** Replace the external kappa J_X source with a W33-invariant microscopic many-qutrit interaction; compute exact ground-state chiral order and assess real antiunitary symmetry rather than a chosen basis K.
3. **Routing optimality:** Prove/disprove existence of a 3-layer native-A SWAP circuit and a 27–35 SWAP circuit using SAT/ILP or matching constraints, then add calibrated optical coupler and loss budgets.
4. **Fault-tolerant non-Clifford magic:** Produce the needed physical ninth-root resource via a real injection/distillation circuit with a decoder and error threshold; exploit the coherent eight-SUM charge-extraction construction as a baseline.
5. **Actual continuum model:** Replace the growing SL(2,q) *regular* Laplacian by a physically defined W(3,q) interaction generator and calculate low-energy dispersion, spectral dimension and locality across q=3^t.
