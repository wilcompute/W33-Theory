# Five mathematical fronts: 45 tensor charts, octonionic G₂(3), Radon tomography, E₈ phase loss, and invariant-action obstruction

**Date:** 2026-11-20 (US Eastern). **Status:** independently executed finite mathematical tests, **not** a solved Theory of Everything, experimentally observed quantum process, unique spacetime theory, parameter-free coupling, or physically selected vacuum.

**Producer:** [analysis/toe_20261120_octonion_mereology_radon.py](toe_20261120_octonion_mereology_radon.py)  
**Regression:** [tests/test_toe_20261120_octonion_mereology_radon.py](../tests/test_toe_20261120_octonion_mereology_radon.py)  
**Frozen data:** [data/toe_20261120_octonion_mereology_radon.json](../data/toe_20261120_octonion_mereology_radon.json)

## Repo prior-art firewall

The repo already derived the 40 Witting rays as parity-odd two-qutrit projectors (Pass11663), the 40-to-240 E₈ root fibers and explicit Jacobi-valid sl9+84+84 construction (Pass11681), the 45 symplectic two-qutrit tensor factorizations and dynamics-relative gate entanglement (Pass11180), the MUB entanglement census for 45 charts (Pass12636), the triple-trace Pauli operator tomography (2026-10-31), and Witting communication/2-design facts (TOE90–92). Those facts are **not claimed as discoveries here**.

This pass builds an independent five-front computational cross-check and identifies previously untested *state-chart, pair-source, octonion, Radon and commutant* consequences.

## Front 1 — the exact Witting state-by-subsystem atlas

In the standard two-qutrit V=F₃⁴ symplectic geometry, the 90 nondegenerate symplectic 2-planes form 45 unordered decompositions V=P⊕P^⊥. Each chart determines two commuting full M₃(C) local factor algebras.

For each one of the 40 Witting projectors ρ_v=(I−Parity)Π_v/2, compute its reduced purity from all nine local Pauli moments, rather than inferring entanglement from graph edges:

    purity_P(ρ_v) = (1/3) Σ_{u∈P} |Tr(ρ_v W_u)|².

All 1,800 state×chart calculations give exactly two possibilities, numerical residual below 2×10⁻¹⁵: if v lies in either factor plane, purity=1 (product Schmidt values 1,0,0); otherwise purity=1/2 (Schmidt values 1/2,1/2,0).

- 8 product Witting states and 32 rank-2 entangled Witting states per factorization.
- Every single Witting state is product in 9 charts and entangled in 36.
- **All 540 noncommuting / Witting-nonorthogonal unordered ray pairs uniquely select one factorization where *both* are product.**
- All 240 commuting / Witting-orthogonal pairs leave exactly three such factorizations.

For the *explicitly supplied* toy conditional frame energy E(F;v,w)=2−purity_F(v)−purity_F(w):

| Pair type | E=0 charts | E=1/2 charts | E=1 charts |
|---|---:|---:|---:|
| Noncommuting | 1 | 16 | 28 |
| Commuting, distinct | 3 | 12 | 30 |

This is a precise **relational subsystem-selection mechanism conditioned on a chosen noncommuting pair**. It is *not* spontaneous symmetry breaking by an independently derived physical Lagrangian. Uniformly averaging over all 40 rays gives the same summed energy 16 for every one of the 45 charts: symmetric data alone do not select a unique factorization.

## Front 2 — an actual octonionic 364-point split Cayley hexagon

Using **Zorn split-octonion** matrices over F₃, represent a trace-zero octonion by (a,u;v,−a), u,v∈F₃³, with norm −a²−u·v. Form its nonzero projective null points; declare two distinct null points collinear precisely when their Zorn product vanishes.

The producer **constructs** the incidence from these operations, rather than importing a named regular graph. Its checks:

| Observable | Computed |
|---|---:|
| Null projective points | 364 |
| Four-point maximal geometric lines | 364 |
| Point graph collinearity edges | 2,184 |
| Incidence-graph edges | 1,456 |
| Incidence-graph vertices | 728 |
| Incidence-graph girth | 12 |
| Graph distance shells from one point | 1, 12, 108, 243 |
| Point-graph intersection array | {12,9,9;1,1,4} |
| Point adjacency spectrum | 12¹, 5¹⁰⁴, (−1)¹⁶⁸, (−4)⁹¹ |
| Graph first Betti number | 729 |

The point-line cycle number β₁=1456−728+1=729=3⁶ equals the Steinberg degree of type G₂(3); W33 has β₁=160−80+1=81=3⁴, the type C₂(3) Steinberg degree. These are also full matrix-algebra dimensions for three and two qutrits. **Dimension matches do not provide an equivariant map to qutrit operators**, much less a spacetime theory. The octonionic H(3) realization lives in Q(6,3); do not silently identify it with all points and commuting lines of W(5,3).

**Additional no-go:** Feit–Higman requires 2st to be a square for a finite thick generalized octagon of order (s,t). Equal order s=t=q would make 2q² a square, impossible for integer q>0. Thus the equal-order quadrangle→hexagon tower does **not** automatically continue to an equal-order octagon.

## Front 3 — an operational full-rank displaced Radon tomography

For every projective Pauli direction v let Π_v=(I+W_v+W_{−v})/3 and let Q denote two-qutrit parity. Exactly:

    Σ_{40 directions v} Π_v = 13 I₉ + 3Q.

For any a∈F₃⁴ conjugate this randomized 40-setting binary instrument by the displacement W_a and define Q_a=W_a Q W_a†. Then:

    p0(a) = [13 + 3 Tr(ρ Q_a)]/40,
    Wigner_ρ(a) = [40 p0(a) − 13]/27.

The 81 translated parity operators are Hilbert–Schmidt orthogonal, Tr(Q_a Q_b)=9 δ_ab. Consequently 81 calibrated displaced binary settings reconstruct every two-qutrit Hermitian state. Verified all 81 operator identities, full rank 81, and 1,620 probabilities for 20 independently seeded positive density matrices with residual below 3×10⁻¹⁴. It does **not** prove a quantum advantage, optimal finite-shot efficiency, loss tolerance, or secure key exchange.

## Front 4 — what projective Wigner experiments cannot resolve about E₈

Pass11681 already has the exact 240 E₈ root restrictions yielding 40 Witting rays, six unit-phase lifts per ray. Six scalar multiples have the **same rank-one projector and same Wigner distribution**. Therefore no POVM that receives only the projective Witting state distinguishes those six *algebraic* labels. This is an information-loss obstruction to naive projective E₈ root recovery, not a new 240-root computation. It would take an externally specified coherent reference, physical preparation and a phase-sensitive observable to make root-fiber phases operational.

## Front 5 — symmetry itself forbids a one-ray vacuum selector

For the actual 40 order-three Clifford reflections U_v=I+(ω−1)Π_v in C⁹, solve

    [H,U_v]=0, for every v.

The stacked 3,240×81 complex linear system has matrix rank **79**, and common commutant exactly span_C{I, Q} of dimension **2**. Thus every fully reflection-invariant Hermitian Hamiltonian is aI+bQ. It can separate 5D even and 4D odd parity sectors but cannot energetically select a **single** Witting ray. An actual vacuum-selection theory needs a physically derived symmetry-breaking field, boundary condition, dynamical instability or a smaller fundamental symmetry.

This directly constrains the Front 1 *pair-conditioned* toy action: choosing a noncommuting pair is a concrete source of symmetry breaking, not an outcome furnished for free by the original fully symmetric geometry.

## Reproduction

    python analysis/toe_20261120_octonion_mereology_radon.py
    python -m unittest discover -s tests -p test_toe_20261120_octonion_mereology_radon.py -v

**20/20 tests passed on the authorized Windows machine and an independent 20-test expanded implementation passed in the ChatGPT sandbox.** Original repo modifications should be preserved during syncing. The full expanded executable packet is supplied as a conversation download in addition to these version-controlled files.

## Relevant published mathematics

- Vlasov, *Scheme of quantum communications based on Witting polytope* (2025): https://arxiv.org/abs/2503.18431
- Gross, *Hudson's theorem for finite-dimensional quantum systems*: https://arxiv.org/abs/quant-ph/0602001
- Unique nonnegative stabilizer representation and contextuality: https://doi.org/10.1103/PhysRevLett.129.120403
- GAP FinInG split Cayley hexagon and embedding distinction: https://gap-packages.github.io/FinInG/doc/chap12_mj.html
- Zorn multiplication and octonionic G₂: https://www.sciencedirect.com/science/article/pii/S0022404925000143
- Generalized-hexagon graph parameters: https://mathworld.wolfram.com/Distance-TransitiveGraph.html
- Feit–Higman octagon restriction: https://cage.ugent.be/~hvm/artikels/29.pdf
- Lorentzian continuum requirements and causal sets: https://link.springer.com/article/10.1007/s10714-024-03281-1

## Five independent next frontier gates

1. Supply a microscopic state-preparation/interaction model that actually **chooses the noncommuting ray pair**; test equivariance, noise, energetics and whether the selected source corresponds to physical observables.
2. Construct a **true G₂(3)↔three-qutrit intertwiner** or a proven obstruction; enforce pairwise line incidence, symplectic commutators, phase conventions and group characters, not only cardinality.
3. Turn the displaced **81-setting Radon measurement** into a calibrated finite-shot falsifier and compare its Fisher information, detector losses and adversarial bias against 120 Pauli-tick measurements.
4. Attempt a **coherent E₈ root-phase measurement** only after specifying valid amplitudes and an external phase reference; characterize what information the existing 6:1 projective quotient destroys.
5. Build a local Lorentzian continuum action with meaningful scale flow, gravitational modes, anomaly-free matter, and a pre-registered unfitted prediction; retain the fully symmetric Hamiltonian no-go as a veto condition.
