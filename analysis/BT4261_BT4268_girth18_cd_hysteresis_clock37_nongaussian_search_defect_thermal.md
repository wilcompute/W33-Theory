# Passes 4261–4268 — girth 18, dynamically corrected holonomy, full-coordinate metastability, clock-37, non-Gaussian channel search, and three outside-box probes

## Evidence boundary
All statements below are finite-model statements. They do not establish a fabricated high-girth network, fault-tolerant hardware, physical spacetime memory, observed Hawking radiation, physical vacuum thermodynamics, a speed-of-light derivation, gravity, cosmology, or a theory of everything.

## Pass 4261 — explicit girth-18 Levi cover, but compactness remains open
The base point-line Levi graph has 80 vertices, 160 edges and degree four. A BFS spanning tree leaves 81 cotree voltage variables. The frozen assignment in `PART_4261_4268_...json` takes values in the prime cyclic group Z_750019.

The verifier does not rely on a simple-cycle-only argument. For each of the 80 base vertices it expands the sheet-zero voltage-cover ball through radius eight. Every ball contains exactly

`1 + 4(1 + 3 + ... + 3^7) = 13121`

states and is collision free. Cyclic deck translation makes sheet zero representative of every sheet. Therefore the cover contains no cycle of length at most 16 and has girth at least 18.

The explicit cover has 60,001,520 vertices and 120,003,040 edges. This is a constructive girth-18 upper bound, not the desired compact construction: the smallest accepted modulus found in the completed frozen random campaign was 750019, and a sub-10000-sheet girth-18 cover remains open.

## Pass 4262 — four-loop dynamically corrected geometric CZ
Let `cos(theta)=1/4`. A pair of oppositely oriented latitude loops at `theta` and `pi-theta` contributes geometric phase `-(pi/2) cos(delta)` under a common polar offset `delta`. Repeat that pair after swapping adiabatic eigenbranches and reversing the physical loop orientations. The Berry phase adds while any repeatable static loop-dependent dynamical phase changes sign.

The full controlled phase is

`phi(delta) = -pi cos(delta) mod 2pi`,

so `d phi/d delta = 0` at the operating point. At `delta=0.02`, the phase error is 6.28297587046e-4 rad and the phase-only two-qubit average infidelity is 5.92136767286e-8.

Adding the exact transitionless term

`H_CD = (1/2) (n x n_dot) · sigma`

removes ideal nonadiabatic leakage in the two-level control model at arbitrary loop speed. A numerical integration at `omega/Omega=0.1` gives only discretization-level residual leakage for exact CD control. With a 1% CD-amplitude error the two latitude leakages are 5.24858e-7 and 4.77127e-7; a four-loop union bound is 2.00397e-6.

The echo cancels differential static gap errors only when the same loop-dependent errors repeat in the second half. Non-repeatable drift remains an error channel.

## Pass 4263 — full-coordinate Davies/Lindblad hysteresis spectrum
The saturated scale flow is converted to a coordinate potential by `U'(s)=-F(s)` at the coexistence value `g=0.5700939873487846`. The coordinate Hamiltonian

`H = p^2/(2M) + U(s)`

is discretized on `[0.4,6.3]` with 180 grid points and `M=16`. Rather than collapsing the coordinate to two wells, the lowest 20 numerical energy states are coupled to an Ohmic thermal bath through the full coordinate operator `s` with `T=0.25` and dimensionless `kappa=1e-3`.

The slow population/Davies gap converges as the retained energy basis is enlarged:

- K=14: 1.05955718189e-11
- K=16: 1.85845505410e-11
- K=20: 1.87223289437e-11

The K=20 Liouvillian therefore has metastable lifetime about 5.3412159284e10 model-time units. The leading coherent pair decays at real rate 3.36867e-6 while oscillating at 0.427022, so population switching is parametrically slower than local coherence dynamics in this calibration.

The stationary state is the Davies Gibbs state; the first eight weights are frozen in the certificate. The slow population eigenvector exchanges weight primarily between the left-localized ground sector and the right-localized first-excited sector.

## Pass 4264 — exact 3-local clock with 37 auxiliaries
The 45-auxiliary binary architecture needed eight explicit dynamic transition flags. Replace the five Gray clock bits by five three-level digits `{0,1,*}`. During a gate transition the active Gray digit passes through `*`, which itself stores the intermediate flag state.

The previously proved 13 shared pair conjunctions and 24 final spectator-condition ancillas remain, but all separate dynamic flags disappear:

`13 + 24 = 37 auxiliaries`.

The legal history still has 49 states. Clock update terms act on the active qutrit and one condition ancilla, hence are at most two-local. The data term is `|*><*|` on the active clock digit times a two-site SWAP, hence exactly three-local.

The weighted legal-history spectrum remains `-48,-46,...,+48` in units of Omega, with gap `2 Omega`, perfect transfer at `pi/(2 Omega)` and full revival at `pi/Omega`.

The cost is local dimension: five qutrit clock digits replace five binary clock qubits. The 37 count is not a global minimum across all encodings.

## Pass 4265 — low-Fock non-Gaussian attack on the two unresolved Hawking channels
The two correlated-disorder effective signal channels above 50% transmissivity are frozen samples 216 and 220:

- sample 216: tau=0.503965219713, nbar=0.174354483780
- sample 220: tau=0.511302421624, nbar=0.178821875111

The search extended beyond Gaussian thermal inputs. For each channel it audited all two-Fock mixtures with `n,m<=8` while optimizing mixture weight, 2000 random three-Fock mixtures, and 5000 random coherent rank-two mixed states in the span `{|0>,...,|4>}`.

No positive coherent information was found. The two-Fock optima approach zero from below, while the best random coherent rank-two candidates remain negative. Pure signal inputs have exactly zero coherent information in the purified-environment Stinespring picture because the global output is pure across signal output versus complementary output. Thus the tested family maximum is zero, attained on the pure-input boundary.

This is not a zero-capacity theorem. Higher rank, higher energy, entangled multi-use inputs and regularized coherent information remain open.

## Pass 4266 — outside box: continuous-time quantum search
Around any marked Levi vertex the graph collapses exactly to five distance shells of sizes

`[1,4,12,36,27]`

with intersection array

`{4,3,3,3;1,1,1,4}`.

The normalized shell adjacency has off-diagonals `2, sqrt(3), sqrt(3), sqrt(12)`. For

`H = -gamma A - |w><w|`,

an operating point `gamma=0.34166556`, `t=18.62288499` gives marked-vertex probability

`P_w = 0.730160420904`.

The uniform baseline is 1/80, so the finite enhancement factor is 58.4128. This is a concrete finite search operating point, not a proof of global optimum or asymptotic Grover scaling.

## Pass 4267 — outside box: a single defect binds a Levi mode
For a rank-one onsite perturbation

`A -> A + V |w><w|`,

the vertex-transitive local resolvent is

`G(E)=1/80[1/(E-4)+1/(E+4)] + 24/80[1/(E-sqrt6)+1/(E+sqrt6)] + 30/(80E)`.

For every `V>0`, `V G(E)=1` has exactly one root above the top spectral edge `E=4`. At `V=4` the bound-mode energy is

`E_b = 4.96008533144`,

with 76.2018133% probability on the defect shell. The remaining shell probabilities are approximately 17.5600%, 3.6882%, 1.7140% and 0.8360%.

This is a finite graph impurity mode, not a fabricated localized photon or continuum Anderson theorem.

## Pass 4268 — outside box: two-stage thermal death of point-line entanglement
For the harmonic kernel `K=5I-A_Levi`, the point-line incidence singular values are `4^1`, `(sqrt6)^24` and `0^15`. The 15 zero channels are spectators. Each nonzero singular value produces an independent two-mode thermal Gaussian pair.

Solving the partial-transpose threshold `nu_tilde_-=1/2` gives two different temperatures:

- sigma=4 collective pair: `T_c = 1.20272834760`
- sigma=sqrt6 pairs: `T_c = 0.994719682173`

Therefore:

1. below 0.9947196822, all 25 coupled mode pairs are entangled;
2. between 0.9947196822 and 1.2027283476, only the unique sigma=4 collective pair is entangled;
3. above 1.2027283476, point-line logarithmic negativity vanishes.

At `T=1`, the total logarithmic negativity is 0.113509461623 nats, compared with the zero-temperature value 6.98041873907 nats.

## Frozen verification
Semantic SHA-256: `900c1daacd2482cd0711e9b0e1427ced1eeef38003560c1e899bce61f121b3ff`.

The deterministic verifier independently reconstructs the Levi graph, checks all 80 radius-eight voltage-cover balls, recomputes the Davies population-gap convergence, checks the 49-state clock spectrum, reproduces the shell-search and defect eigenmode, and solves both thermal PPT thresholds. The focused regression completed locally with 9 tests passing.
