# 2026-11-14: The E6 minimal-charge ensemble is an exact discrete twistor 2-design

## The result and its scope

The existing Pass 12668 counted 1,080 three-qubit stabilizer pure states over 180 minimal integral positive-cubic charges, six per charge. Here we independently reconstruct all 1,080 rank-one stabilizer projectors **without diagonalizing eigenvectors** and find a stronger structural statement: those six states are an **exact complex projective 2-design inside the CP1 twistor fiber** of a quaternionic rank-one projector. The 36 packet Clifford quarter turns act transitively on all 180 charge points. All discrete identities are Gaussian-integer matrix equalities, not tolerance-based approximate matches.

**Producer:** \`analysis/toe_20261114_stabilizer_twistor_2design.py\`; **certificate:** \`data/toe_20261114_stabilizer_twistor_2design.json\`; **regression:** \`tests/test_toe_20261114_stabilizer_twistor_2design.py\`.

## Exact Pauli twistor map

Use the repository's signed Pauli chart with J=P(YII)K, J squared=-I, 27 J-even Hermitian Paulis P_v (elliptic-quadric coordinates) and 36 J-odd Paulis. For a normalized pure 8-component complex vector psi define the quaternionic two-plane projector

    Pi(psi) = |psi><psi| + |J psi><J psi|
            = (I8 + sum_{Q(v)=0} z_v P_v)/4,
    z_v = <psi|P_v|psi>.

The two vectors psi and J psi are orthogonal because J squared=-I. Consequently Pi has complex rank two, quaternionic rank one. Every pure state has charge norm squared sum z_v^2=3 and cubic N(z)=1. The charge map is **precisely the standard higher-dimensional twistor fibration**

    CP1 -> CP7 -> HP3,

with real dimensions 2 -> 14 -> 12. Points in its CP1 fiber are complex lines within the fixed quaternionic two-plane; the 27 E6 charge expectations cannot distinguish them. A general pure three-qubit state is therefore **not uniquely encoded by its 27 cubic charge expectations**; precisely a logical Bloch sphere remains unobserved. This is a geometric loss of distinguishing information under a nonlinear coordinate map, not proof of a physical measurement, decoherence process or CPTP channel.

## Complete integral stabilizer census and exact projective 2-design

There are exactly 135 maximal commuting F2^3 Pauli subspaces, each with eight rank-one stabilizer projectors, giving 1,080 projective stabilizer states. The 45 signed cubic tritangent supports yield exactly four positive-unit-cubic sign patterns per support, or 180 minimal integral charges. Every fiber has exactly six stabilizer states (three orthogonal pairs; the twelve remaining unordered overlaps have squared magnitude 1/2). All 1,080 projectors have identical twirled projector within each six-element fiber, proving the identification without grouping by approximate eigenvectors.

For each fiber let rho_i be its six rank-one complex projectors, Pi its quaternionic rank-two complex projector, and S the swap on C8 tensor C8. The verifier checks, on **all 180 fibers**, the exact 8x8 and 64x64 Gaussian-integer identities

    sum_{i=1}^6 rho_i = 3 Pi,
    sum_{i=1}^6 (rho_i tensor rho_i)
       = (Pi tensor Pi)(I64 + S).

Equivalently, the six projective lines exactly reproduce the Haar **first and second moments** on the fiber CP1. This is a 2-design, not a higher-design claim. The proof leverages the already-known qubit fact that three mutually unbiased Pauli eigenbases are a projective 2-design; the **repo-specific result** is that *every* minimal-charge fiber is one of those designs in the exact signed 27-coordinate E6 model.

The 36 nonquadric Pauli Clifford quarter-turn conjugations preserve the 180 charges and have a **single orbit of size 180**, checked by signed 27-coordinate exact BFS. The charge and state counts factor as 45 tritangent supports x 4 positive-cubic signs x 6 stabilizer representatives.

24 independent non-stabilizer complex pure states were also checked: their 27-charge map agrees with the quaternionic twirl at residual below 7e-16, and randomly rotating psi within span{psi,J psi} leaves all 27 expectations unchanged. This last part is a floating-point numerical control; discrete stabilizer and 2-design statements are exact.

## New bridge to the independently studied attractor flag collapse

The repository now exhibits **two different fibrations over the same HP3 base**:

1. Quantum-state twistor: CP1 -> CP7=Sp4/(Sp3 x U1) -> HP3, with **2D** Bloch-sphere fiber.
2. Generic charge-eigenframe flag: Sp3/Sp1^3 -> Sp4/Sp1^4 -> HP3, with **12D** lower-eigenflag fiber.

They are **not the same fibration**. Their common-base fiber product is the classical homogeneous space

    CP7 x_HP3 (Sp4/Sp1^4)  =  Sp4/(U1 x Sp1^3),

of real dimension 36-(1+3*3)=26. Over a fixed top quaternionic eigenline, the product independently chooses (a) a complex pure-state line in that top eigenspace and (b) the ordered quaternionic eigenflags in its orthogonal H3 complement. This furnishes a coherent mathematical dictionary linking the repo's *six-to-one quantum-state sampling* and its *twelve-dimensional attractor flag degeneration*, without identifying quantum measurement with gravitational radial dynamics.

## Falsifiers, practical implication, literature priority

- A single integer failure of the second-moment identity in one of the 180 fibers kills the exact 2-design claim. The producer checks all 180.
- A violation of fiber invariance of the full set of 27 J-even expectations contradicts the twistor interpretation. It has been checked exactly on 1,080 stabilizers and numerically on 24 generic nonstabilizer states.
- A proposed physical decoder claiming to reconstruct *arbitrary pure three-qubit amplitudes from only 27 cubic charges* is underdetermined by two real parameters; it needs additional J-odd observables or other data. This is an information-theoretic modeling constraint, not an impossibility of tomography with extra measurements.
- The group transitivity is for the specified **signed Clifford packet action**, not a statement that any physically fixed device selects those 180 points or that the whole split E6 group acts as quantum channels.

**Prior art and attribution:** CP(2n+1)->HP(n) twistor fibrations are classical; see https://www.cambridge.org/core/services/aop-cambridge-core/content/view/9B9221D2685FCA16C0A52B66DFB7FFAE/S0008414X24000282a.pdf and https://ncatlab.org/nlab/show/twistor+fibration . The projective 2-design property of complete MUBs is Klappenecker and Roetteler, *Mutually Unbiased Bases are Complex Projective 2-Designs* (2005), https://arxiv.org/abs/quant-ph/0502031 . The 1,080-to-180 six-per-charge counting and qubit overlap observation were already established in this repository's \`analysis/PASS12668_STABILISER_STATES_ARE_MINIMAL_BPS_CHARGES_LEAN.md\`; do not claim priority over it. We add the full **twistor map, exact 64x64 second-moment certificates, signed group transitivity, and common-base flag correspondence**. These are mathematical results; no TOE or quantum-gravity mechanism has been shown.
