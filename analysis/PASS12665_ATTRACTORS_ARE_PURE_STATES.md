# Pass 12665: in the three-qubit Pauli realisation of the E6(6) cubic, 5D attractor charges are pure states, and the flow from a mixed state lands on its top quaternionic eigenvector

Claude track. Follows Pass 12664. **Not a theory of everything.** A dictionary between a known supergravity mechanism and known quantum states, checked numerically.

## Setting

From Pass 12656: the 27 three-qubit Paulis commuting with J = (Y⊗I⊗I)K form an elliptic quadric. For Q ∈ R²⁷ put X(Q) = Σ Q_v P_v and N(Q) = Tr X³/48; this is the E6(6) cubic (78-dimensional stabiliser, unique sign class, Pass 12655). A density matrix ρ has charge Q_v = Tr(ρP_v), with X = 8ρ_J − I, where ρ_J = (ρ + JρJ⁻¹)/2. A pure state has X = 4Π − I, |Q|² = 3 and N = 1.

**5D reading** (Ferrara–Günaydin, hep-th/0606108). Q are the 27 charges of maximal 5D supergravity. At the origin of the scalar manifold E6(6)/USp(8) the central charge is Q. The black-hole potential is V(φ) = |exp(φ·P)Q|² over the 42 non-compact generators P. Its minimum is the attractor, and the entropy is S ∝ √|N|. There is a single entropy-carrying orbit, 1/8-BPS, with residual symmetry USp(2) × USp(6). That is the stabiliser of a point of HP³, i.e. of a pure-state image 4Π − I.

## 1. Attractors (`w33_attractor_pure_states.py`)

- **Algebra.** The stabiliser of N in the Pauli basis is 78 = 36 + 42. The 36 skew generators preserve Tr X² and Tr X⁴ (they are the conjugation action of usp(8)).
- **Pure states are critical points.** For pure-state charges ⟨Q, PQ⟩ = 0 for all 42 P, to 9×10⁻¹⁶.
- **Flows.** For 12 random charges, minimising V over φ ∈ R⁴² gives:
  - **V_min = 3·|N|^{2/3}** in every case (relative error ≤ 9×10⁻¹⁴);
  - the attractor charge Q* always has quaternionic spectrum |N|^{1/3}·(3, −1, −1, −1) (sign of N);
  - **N > 0 (3 cases):** Q*/N^{1/3} is the charge of an explicit pure state. (X*/N^{1/3} + I)/4 is a rank-2 projector, and a vector ψ in its range reproduces the charge to 2×10⁻⁸.
  - **N < 0 (9 cases):** Q* is minus a pure-state charge, which is not the charge of any state (I + X* has eigenvalue −2).
- **N = 0:** V flows to 0 (6×10⁻¹⁶), so there is no attractor ("small" black holes).

Mathematically this is the Kempf–Ness picture: minimal-norm points of closed orbits are where the moment map ⟨Q, PQ⟩ vanishes. The content here is that in this realisation the minimal-norm set with N > 0 is exactly the set of pure-state charges (times N^{1/3}).

## 2. Mixed states (`w33_attractor_of_mixed_states.py`, `w33_attractor_mixed_precision.py`)

- For physical charges (X = 8ρ_J − I, ρ_J with quaternionic eigenvalues p₁ ≥ … ≥ p₄, Σp_i = 1/2): **N = Σ(8p_i − 1)³/24**, checked against the cubic for 10 states.
- **N ≤ 1 for every state**, since Σ(8p − 1)³ is convex on the simplex and is largest at its vertices. **Equality holds iff ρ is supported on a single quaternionic line span{ψ, Jψ}.** That includes every pure state, but also mixtures such as Π/2, since the charge only sees ρ_J. So the 5D entropy √N of a state's charge is largest exactly for states on one quaternionic line. N < 0 occurs, e.g. p = (1/6, 1/6, 1/6, 0) gives −1/27.
- **Flat directions.** The charge stabiliser F4(4) is non-compact, so the minima of V form a manifold, not a point. Different BFGS starts land on different minima: same V = 3N^{2/3}, different attractor projectors, spread about 3×10⁻³.
- **Nearest attractor = spectral truncation.** The minimiser reached from the origin of moduli space has:
  - the smallest displacement |A| among the five minima found per state;
  - attractor projector equal to **the projector onto the top quaternionic eigenspace of ρ_J**, to 10⁻⁸–10⁻¹⁵ (four rank-4 states, analytic gradients, BFGS gtol 10⁻¹³; also overlap > 0.99999 for ten earlier states).
- So, numerically: the 5D attractor flow, started at the origin, sends a mixed state's charge to N^{1/3} times the charge of its dominant quaternionic eigenvector.
- "Nearest" means nearest among the minima found; no proof that it is the global geodesic projection.

## Literature and scope

- The black-hole/qubit correspondence relates the 4D STU model to three qubits (Duff, hep-th/0601134) and 5D E6 to three qutrits (Duff–Ferrara, arXiv:0704.0507). Lévay (arXiv:0708.2799) writes the 4D potential as the norm of a three-qubit state containing charges and moduli. The Pauli labelling of the 27 is Lévay–Saniga–Vrana–Pracna (PRD 79, 084036).
- The statements here — 27 charges as **Pauli expectation values**, attractors as **pure states**, and the flow as **purification by spectral truncation** — were not found in the sources searched. Novelty is therefore unverified.
- Nothing here derives gravity, particles or a black hole. It is an exact dictionary on one side and numerics on the other.

## Link to the certainty relation (Passes 12663–12664)

The type B certainty relation fails for mixed states: some rank-two mixtures look exactly like noise (other track, `2026-11-14_typeB_mixed_control.md`). In the present dictionary, mixed states are where N < 1 and the attractor flow does work. Whether the two phenomena are related was not examined.
