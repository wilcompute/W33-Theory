# Pass 12667: the 5D attractor flow of a mixed state's charge stays inside state space, ends at a pseudo-pure state, and the endpoint is majorised by the start

Claude track. Follows Pass 12665. **Not a theory of everything.**

## 1. The endpoint is a physical state

For a state with N > 0 the attractor charge is X* = N^{1/3}(4Π − I) (Pass 12665). So I + X* has eigenvalues 1 + 3N^{1/3} (twice) and 1 − N^{1/3} (six times), both ≥ 0 because N ≤ 1. The endpoint is therefore the charge of the **pseudo-pure state**

ρ* = c·Π/2 + (1 − c)·I/8,  c = N^{1/3},

with Π the projector onto the top quaternionic eigenspace of ρ_J. It has the same cubic invariant N.

## 2. The path stays physical (`w33_attractor_path_physicality.py`)

Along the geodesic Q(t) = exp(tA*)Q, t ∈ [0, 1], from the moduli origin to the attractor, for 8 random mixed states with N from 0.20 to 0.995:
- the endpoint equals the pseudo-pure state above to 10⁻¹⁰ to 10⁻¹⁶;
- **the smallest eigenvalue of I + X(Q(t)) is never below its value at t = 0**, so every intermediate charge is the charge of a physical state;
- the purity of ρ_J decreases monotonically along the path;
- the black-hole potential |Q(t)|² decreases monotonically, as geodesic convexity predicts.

## 3. Majorisation (`w33_attractor_majorisation.py`)

ρ* depends only on N, so the comparison is a statement on the simplex {p₁ ≥ … ≥ p₄ ≥ 0, Σp = 1/2} of quaternionic spectra.
- In 158,011 random points with N > 0 (Dirichlet samples at four concentrations, plus vertices, edges and face centres), the spectrum of ρ_J (each p_i doubled) **majorises** the spectrum of ρ* every time.
- The worst partial-sum margin is 0 (−1×10⁻¹⁶), reached only where start and end coincide.

Since ρ* is diagonal in the eigenbasis of ρ_J, majorisation means ρ* is a convex combination of eigenvalue permutations of ρ_J (Birkhoff), i.e. ρ* = Φ(ρ_J) for a random-permutation (unital, mixing) channel Φ. **So the 5D attractor endpoint is reachable from ρ_J by a physical mixing process.**

**Status.** Numerical over the simplex, not proved. The first partial-sum condition is λ_max(X) ≥ 3N^{1/3}; it holds with equality at the pure states, and its proof was not completed here.

**Caveat.** The step ρ ↦ ρ_J = (ρ + JρJ⁻¹)/2 involves the antiunitary J (a transposition), which is **not** a quantum channel. So the physical-process statement holds from ρ_J onward, not from ρ.

## Reading

In the three-qubit dictionary of Passes 12665–12667:
- the attractor mechanism of 5D maximal supergravity acts on a state's charge as a path through state space;
- the path keeps the state physical, lowers purity and preserves the entropy invariant N;
- it ends at the pseudo-pure state built from the top quaternionic eigenvector;
- that endpoint is majorised by the start.

This is a statement about one map between two known structures, and it says nothing about gravity.

## Addendum: the majorisation is a theorem

Use the other track's diagonal frame (`analysis/2026-11-14_e6_attractor_torus.md`, 3e5e71b64). A compact transformation brings X to coefficients (a, b, c) on three commuting Paulis, with quaternionic spectrum {s₁a + s₂b + s₃c : s₁s₂s₃ = 1} and N = abc. For N > 0, flipping two signs only permutes this set, so take a ≥ b ≥ c > 0. Then x = (a+b+c, a−b−c, b−a−c, c−a−b) in decreasing order, and the endpoint is g·(3, −1, −1, −1) with g = (abc)^{1/3}.

| partial sum | start | endpoint | reason |
|---|---|---|---|
| 1 | a + b + c | 3g | AM-GM |
| 2 | 2a | 2g | the maximum is at least the geometric mean |
| 3 | a + b − c | g | a + b − c ≥ a ≥ g, since b ≥ c |
| 4 | 0 | 0 | traceless |

**Theorem.** For every charge with N > 0 (in particular every state with N > 0), the quaternionic spectrum majorises N^{1/3}·(3, −1, −1, −1). Equality holds iff a = b = c, i.e. the charge is N^{1/3} times a pure-state charge. Consequently the pseudo-pure endpoint ρ* is a random-permutation mixture of ρ_J (Birkhoff), as found numerically in §3. The caveat about ρ ↦ ρ_J not being a channel stands.
