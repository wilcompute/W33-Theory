# Five independent TOE frontiers — exact W33 certificates (22–23 October 2026)

**Status:** one general-prime theorem, two exact finite construction/failure results, one controlled toy-model theorem, and one limited continuum no-go. No assertion of a solved theory of everything, gravity, chirality mechanism, quantum-computing threshold, or experimental hardware.

This continues the exact point-coordinate Pascal CSS `[[40,20,4]]_3` and five-transvection PSp(4,3) representation already verified in `analysis/w33_20261022_css_logical_sp43_generators.py`. The old 240-edge CSS code and Steinberg 81D carrier are **different** objects.

## 1. General-prime stabilizer Jordan theorem: proved

Let `C` be the rowspace of the W(3,p) noncollinearity matrix `B` over F_p (p prime). Fermat's theorem identifies B's row indexed by w with the projective evaluation of `omega(x,w)^(p-1)`. Polarization (p-1 < p) shows these powers span all homogeneous degree-(p-1) forms, giving the full polynomial module `Sym^(p-1)(V*)`, of dimension `binom(p+2,3)` (the quadratic Veronese identification at p=3 is established prior W33 repo work).

For a nontrivial transvection T, the dual four-dimensional defining module restricts to `J_2 + J_1 + J_1`. Its homogeneous degree p-1 symmetric power decomposes by the degree t assigned to the moving 2D summand:

```text
Sym^(p-1)(J2 + J1 + J1)
 = direct_sum_{t=0}^{p-1} [Sym^t(J2)] ^(p-t)
 = direct_sum_{j=1}^{p} J_j^(p-j+1).
```

Here `Sym^t(J2)=J_(t+1)` for t<p, by the standard action on binary homogeneous polynomials and invertibility of binomial coefficients below p. This is a **general-prime mathematical proof**. Independent exact matrices confirm it at p=2,3,5,7 with full sequences of ranks of `(T-I)^k` on C.

**Boundary:** the extension `0 -> C -> ker(B) -> Q ->0` is non-split a priori; the predicted arbitrary-prime Jordan law for **Q** is not proved by this argument. Pass12187 is reserved by another Codex track; do not overwrite it.

## 2. Clock selection: rigorous toy model and finite-temperature obstruction

On the unit sphere in R^40, with `s_i=x_i²` and the B noncollinearity relation, take the invariant energy

```text
V(x) = -a sum_i x_i^4 + gamma sum_{i<j} B_ij x_i² x_j²,
a>0, gamma>=0.
```

Since `sum_i x_i^4 <= (sum_i x_i²)^2 =1` and the pair term is nonnegative, the **only** minimizers are the eighty `±e_i`, forming forty projective clock choices; the minimum equals `-a`. The tangent Hessian at `±e_i` is **anisotropic**: `4a` on the twelve collinear directions and `4a+2gamma` on the twenty-seven noncollinear directions. This follows by expanding `x_i²=1-sum_(j!=i)x_j²` to quadratic order. Thus a symmetric, explicitly postulated localizing potential has 40 isolated candidate clock vacua, permuted by PSp(4,3).

However, the finite-dimensional Gibbs ensemble at **every finite inverse temperature** is invariant under that group. By transitivity and the unit-sphere constraint it obeys the exact equality `E[x_i²]=1/40` for every i. Thus no unseeded finite-temperature ensemble prefers a clock. A symmetry-breaking perturbation, singular zero-temperature selection, measurement/initial-condition selection, or a genuine thermodynamic limit is still needed.

This energy is a **toy model chosen by hand**; it is not derived from the Holonet photon, Einstein gravity or an E8 action.

## 3. Native Clifford routing: nine triangle-cycles, two abstract SWAP layers

Each of the forty anchored symplectic transvections has cycle structure `1^13 3^9`. Exhaustive verification of all 40 transformations finds that the three vertices in **each** moving cycle are pairwise noncollinear (a B triangle) and pairwise **nonadjacent** in the collinearity graph A.

For each orbit `(a b c)`, the physical position swaps `(b c)` followed by `(a b)` implement the orbit. Because the nine 3-cycles are disjoint, all first swaps can run concurrently and all second swaps concurrently: **18 two-qutrit SWAP gates in depth 2**, provided the required B couplers exist. This is exact in the idealized all-to-all/B-coupled **40-physical-qutrit model** and respects the abstract Clifford gate.

The B topology is 27-regular, whereas the natural W33 collinearity A topology is 12-regular; none of the directly used swaps lies on an A edge. Therefore this does **not** claim depth 2 on the A geometry, on hardware with sparse physical couplers, or on one photon's forty optical modes. Photon losses, mode-to-qudit identification, native swaps and syndrome schedules are unvalidated.

## 4. Attempted ninth-root magic gate: exact 59,049-word leakage obstruction

For the ternary CSS `[[40,20,4]]_3`, consider the physical non-Clifford diagonal operator `U = diag(1,zeta_9,zeta_9²)^(tensor 40)`. An encoded computational basis ket is a uniform coset state `|u+C>` for `u in C^perp`. Direct exhaustive evaluation of the **entire** `3^10=59049`-word classical code finds that the integer digit sum of every stabilizer word is `0 mod 9`. Thus `U|0_L>=|0_L>`.

Now take the explicit weight-four logical representative `u=(1,1,1,1,0,...,0)` in the repository's canonical projective ordering; the verifier establishes `Bu=0` and `u not in C`. The phase changes `sum_i (u_i+c_i mod 3) - sum_i u_i` modulo 9 occur as:

| phase difference mod 9 | number of c in C |
|--:|--:|
| 0 | 19,683 |
| 3 | 13,122 |
| 6 | 26,244 |

With `omega=exp(2pi i/3)`, the code-projector amplitude is exactly

```
A_u = (19683+13122 omega+26244 omega²)/59049
    = -i sqrt(3)/9;
|A_u|² = 1/27.
```

The **deterministic transversal ninth-root gate fails** to preserve the logical codespace. A code-projection outcome for that logical state is not guaranteed and has only 1/27 success probability; other logical states, e.g. the encoded zero, behave differently. This is not a successful fault-tolerant non-Clifford logical unitary or a magic-state injection circuit; it is a rigorous failure witness that future injection/decoding schemes must address. The pattern may be an instance of known divisible-code/diagonal-gate theory; no priority claim.

Relevant literature: Hu–Liang–Calderbank, *Divisible Codes for Quantum Computation* (arXiv:2204.13176); Camps-Moreno et al., *Transversal gates for quantum CSS codes* (arXiv:2601.21514); Li–Yeh, *Transversal AND in Quantum Codes* (arXiv:2603.04548). The 2026 qubit universal depth-one result arXiv:2610.06730 is not evidence that our qutrit code has the same property.

## 5. Fixed-characteristic one-anchor continuum no-go

The W(3,q) collinearity adjacency A_q has exactly three eigenvalues:

```text
k=q(q+1), r=q-1, s=-(q+1)
multiplicities 1, q(q+1)^2/2, q(q²+1)/2.
```

For `q=p^t` with **odd fixed prime p** and an anchored order-p transvection `T`, A_q and T commute, because T is a graph automorphism. Thus any *single-anchor* operator

```text
H_q = a(q) I + b(q) A_q + epsilon(q) (2I-T-T^-1)
```

has at most **p+2 distinct eigenvalues**: 1 from the constant representation and at most `(p+1)/2` eigenvalues in each of the two other A_q sectors (T has p-th roots of unity, and T+T^-1 identifies conjugates). The upper bound does not depend on the extension degree t.

This strengthens the **prior** Pass11197 normalized-Laplacian collapse result only for the restricted single-clock family. A fixed number of spectral atoms cannot produce the infinitely many distinct eigenfrequencies required by an elliptic/Lorentzian continuum kinetic operator with a Weyl-law tower. It does **not** rule out tensor products, interacting Hamiltonians, multi-anchor propagation, new adjacency families, or genuine continuum constructions.

## Reproduce and audit

```bash
python analysis/w33_20261022_five_toe_frontiers.py data/PART_20261022_FIVE_TOE_FRONTIERS.json
python -m pytest -q tests/test_w33_20261022_five_toe_frontiers.py
```

The script contains five individually named functions with exact finite-field rank, all-prime structural identities, exhaustive 59,049-word coset enumeration, all-40-anchor permutation checks, and arithmetic spectrum bounds.

## Five non-sequential next steps

1. **Jordan quotient proof:** compute the extension class of C inside C-perp for all primes, aiming to resolve the conjectural `Q = J1^3 + sum_(j=2)^(p-1) Jj^(2j) + Jp^p` and cross-check Pass12187.
2. **Dynamical clock:** add a genuine physical kinetic term/order-parameter coupling, derive it from an experimentally grounded state space, and test whether selection survives a controlled limit without a source bias.
3. **Hardware Clifford:** compile the 18 SWAPs onto the **actual** allowed optical coupling graph, with full mode occupancy, loss probability, operation duration and syndrome recovery.
4. **Logical non-Clifford:** design a conditional-syndrome injection channel, characterize *all* 3^20 logical cosets algebraically or by orbit reduction, and prove a protocol-level success/fidelity/threshold statement rather than assuming the uniform transversal gate works.
5. **Continuum:** test a *multi-anchor* field or interacting tensor-product tower whose number of distinct low-energy spectral levels grows, while enforcing Lorentz covariance, locality, and a nontrivial propagator.
