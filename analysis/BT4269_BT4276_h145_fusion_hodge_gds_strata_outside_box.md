# Passes 4269–4276 — H145 branching, heralded GHZ fusion, two-row Hodge optimization, corrected GDS geometry, subgroup boundary, and three outside-box probes

## 4269 — The order-72 anchor symmetry acts explicitly on the full carrier

The largest five-anchor stabilizer from Pass 4245 is not merely an order count.  Direct reconstruction inside `PSp(4,3)` gives

`H = C3 × SL(2,3)`, with cyclic center `C6`, commutator `Q8`, and 21 complex irreducible characters.

Using `chi_ab` for one-dimensional characters, `sigma_ab` for the binary-tetrahedral two-dimensional spinors, and `tau_a` for the three-dimensional tetrahedral irreps, the two nontrivial W33 eigenspaces restrict as

- `V15 = 2 chi_00 + chi_10 + chi_20 + sigma_01 + sigma_02 + sigma_11 + sigma_22 + tau_0`;
- `V24 = 2 chi_00 + chi_10 + chi_20 + sigma_01 + sigma_02 + sigma_12 + sigma_21 + 2 tau_0 + tau_1 + tau_2`.

Therefore

`H145 = 23 chi_00 + 8 chi_10 + 8 chi_20 + 8 sigma_01 + 8 sigma_02 + 6 sigma_11 + 6 sigma_22 + 2 sigma_12 + 2 sigma_21 + 10 tau_0 + 2 tau_1 + 2 tau_2`.

A species-wise H-equivariant five-generation charge partition exists at dimensions `(Q,u,d,L,e)=(30,15,15,10,5)`, leaving 70 gauge-singlet states.  However an identical five-dimensional generation factor repeated over all 15 Standard-Model internal states is impossible at order 72: any constituent of that generation factor would need multiplicity at least 15 in H145, and only `chi_00` clears that threshold.  Thus order-72 species covariance survives, but exact family-universal factorization does not.

## 4270 — Explicit nondestructive GHZ28 heralded fusion

Two GHZ blocks are fused by a reusable dual-rail ancilla: CNOT from one block anchor into the ancilla, CNOT from the second anchor, Z-readout of the ancilla, and a tracked block-X frame update for odd parity.  No data qubit is sacrificed.

At the frozen `F_CNOT=0.981`, `p_erasure=0.13` operating point, conservative dynamic programming chooses primitive blocks `5,3,4,4,4,4,4` and the fusion tree `3+4→7`, `5+7→12`, two `4+4→8`, `8+8→16`, `12+16→28`.  An accepted state has 33 CNOTs and six parity measurements.  If an erasure during a fusion destroys both input blocks, expected CNOT attempts are 94.2734, versus 1159.70 for whole-run restart of the 27-CNOT direct tree: a 12.30× attempt reduction.  Conditional independent process factor remains only `0.981^33 = 0.53098`, so better gates/coding remain mandatory.

With one reusable parity ancilla the modular protocol takes 15 entangling rounds.  Reusing the clock plus two additional dual-rail parity ancillas permits three simultaneous first-stage fusions and reduces this to nine rounds, at 93 transmons excluding readout.

## 4271 — The minimum two-row Hodge decoder now has a signed-16 operating point

The information-theoretic minimum remains exactly two extra global scalar rows beyond Levi incidence.  A deterministic 600-pair search over `F_65537` (seed 4269005) found 91 exact-passing pairs; candidate 467 is the best frozen normalized worst-case pair.

Both rows fit signed 16-bit coefficients: max absolute values 32446 and 32692.  Exhaustive cycle/theta modular nonvanishing preserves `spark >= 15`, hence noiseless unique recovery of arbitrary-real seven-sparse errors.  After per-row max-coefficient normalization, the minimum cycle gain is `1.51799e-3` and minimum theta generalized singular value is `1.33507e-5`.  Relative to Pass 4147 these are improvements of 6.41× and 1.805× respectively.

This is a finite Pareto improvement, not a global optimum over every integer pair or a calibrated ADC theorem.

## 4272 — The first dogleg geometry was impossible; the GDS compiler fixes it

Pass 4248's delay counts are correct, but its rounded dogleg placement was not.  Four 50-um quarter bends require horizontal pitch at least `4r=0.20 mm`, so the old `0.12 mm` pitch cannot be drawn.  More subtly, the stored `h=0.31766094 mm` is the vertical straight-leg length in the identity `2h+(2pi-4)r=Lslot`; the actual centerline excursion is `h+2r=0.41766094 mm`, larger than the old 0.36-mm lane pitch.

The corrected compiler uses `r=0.05 mm`, vertical leg 0.31766094 mm, 5-um top straight, 0.205-mm cell pitch, 0.45-mm lane pitch, and 1-um waveguides.  It splits each 40-lane branch into four ten-lane banks, yielding 16 tiles placed on a 6×3 grid.  The keepout-inclusive preliminary bbox is 11.04 mm × 14.85 mm.  Minimum edge-to-edge lane gap is 31.339 um.  The complete schedule produces 1280 cell instances: 919 doglegs and 361 straights, with 3676 quarter bends.

A pure-Python GDSII writer emits one PATH per cell and keepout rectangles.  Each quarter circle is tessellated into 32 segments; the worst eight-dogleg arc-chord deficit is 0.252 um, corresponding to about 1.68 fs group-delay error at `n_g=2`.  A 5% broadening requirement for a 5-ps pulse across the maximum compiled path gives the design constraint `|beta2| < 378.06 ps^2/m` for final PDK simulation.

This is open/public-rule geometry, not proprietary foundry DRC.

## 4273 — The subgroup strategy reaches its natural boundary

The remaining order-12 `P3` and order-9 second-independent triple quotients each give saturated deterministic catalogues of 57 selector-24 and 27 selector-15 roots after 20,000 starts; every discovered root is individually Krawczyk-unique.

The order-6 edge-plus-isolated quotient behaves completely differently.  Twenty thousand starts already produce 2376 distinct locally certified selector-24 roots and 246 selector-15 roots, and the selector-24 sequence is still growing.  These are rigorous lower bounds, not global counts.

The next subset rank explains the explosion.  The 91,390 four-subsets form exactly 16 PSp(4,3) orbits, and one orbit has stabilizer order one.  Trivial symmetry therefore appears already with four marked vertices.  Global nonlinear completion can no longer be reduced to enumerating nontrivial stabilizer fixed spaces; equivariant degree, Conley index, Morse continuation, or another global method is now required.

## 4274 — Outside box: W33 graph state is exactly five-uniform

For the 40-qubit W33 graph state, every cut matrix `A[S,Sbar]` has full binary row rank for every subset `|S|<=5`: 40 + 780 + 9880 + 91390 + 658008 subsets were exhausted.  Hence every reduced state on at most five qubits is maximally mixed.

The graph-state stabilizer distance is exactly six.  There are exactly 240 weight-six stabilizers; every one has `A x = 0 (mod 2)` and support equal to two disjoint W33 triangles.  Example support: `{0,1,2,22,27,29}` with pure-X stabilizer on those six qubits.  Thus the state is 5-uniform but not 6-uniform.

## 4275 — Outside box: point geometry and incidence geometry have opposite local transport curvature

For non-lazy Ollivier neighbor measures, W33 has exactly two pair classes: adjacent pairs have `W1=5/6`, `kappa=1/6`; nonadjacent pairs have `W1=2/3`, `kappa=2/3` at graph distance two.

The Levi graph has four shells: `kappa=-1` at distance 1, `-1/2` at distance 2, `1/6` at distance 3, and `1/2` at distance 4.  With half-lazy measures the corresponding values are `-1/2,-1/4,1/12,1/4`.  The finite point geometry is positively curved in this transport sense while the local incidence geometry is negatively curved.  This is graph transport curvature, not continuum spacetime curvature.

## 4276 — Outside box: exact Hodge-sector fluctuation-dissipation split

For the 160-dimensional Levi edge space, define `Gamma = gamma_H P_H + gamma_G P_G`, with 81 harmonic and 79 gradient modes.  The Ornstein-Uhlenbeck model with separate sector temperatures has

`R(t)=e^{-gamma_H t} P_H + e^{-gamma_G t} P_G`

and

`C(t)=k_B[T_H e^{-gamma_H |t|} P_H + T_G e^{-gamma_G |t|} P_G]`.

Thus each Hodge sector obeys an exact FDT at its own temperature, while a single global temperature exists iff `T_H=T_G`.  For `(T_H,T_G,gamma_H,gamma_G)=(2,1,1,4)` in `k_B=1` units, `tr C(0)=241`, integrated response trace is 100.75, and integrated correlation trace is 181.75.  The same 81/79 split controlling Pass 4251 exergy therefore controls the finite fluctuation-response decomposition.

## Evidence boundary

All promoted statements are finite representation, graph, circuit-resource, integer-sensor, geometry, polynomial-root, graph-state, transport, or stochastic identities.  No phenomenologically complete gauge theory, fabricated GHZ28 processor, globally noise-optimal physical decoder, proprietary DRC-clean photonic chip, globally exhaustive 80-dimensional nonlinear theorem, measured quantum-secret-sharing device, physical spacetime curvature, thermodynamic experiment, gravity, cosmology, or theory of everything is claimed.
