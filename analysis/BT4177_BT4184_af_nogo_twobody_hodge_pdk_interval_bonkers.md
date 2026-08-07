# Passes 4177–4184 — fixed-carrier AF no-go, strict two-mode compiler, Hodge decoder, PDK delay bank, symmetry-stratified interval closure, and three outside-box probes

## 4177 — representation-independent add-only SU(3) asymptotic-freedom obstruction
The fixed 145-state carrier already has total SU(3) Dynkin load 16 and cubic color anomaly -28. In the convention `b0=11-(2/3) sum_Weyl T(R)`, strict asymptotic freedom requires total load <16.5. Any anomaly repair must add colored chiral matter, while every nontrivial finite-dimensional SU(3) irrep has T>=1/2. Therefore strict b0>0 is already impossible before any bounded representation search. Even b0=0 cannot repair the anomaly: its entire colored budget is one weak-singlet 3 or 3bar, with cubic anomaly magnitude only one. Thus every add-only repair of the fixed carrier has b0<0. Escapes require removing/reassigning original colored degrees, changing the gauge embedding, or changing the assumed UV gauge dynamics.

## 4178 — strict two-mode relational compilation
The 58-mode dual-rail architecture no longer needs the previous K2,2 coupling on every logical tree edge. Pairwise rail exchanges plus a pairwise cross-Kerr term implement `CNOT=(I⊗H) CZ (I⊗H)` with no ancilla. The exact hardware graph has 84 couplers, maximum degree four, and diameter nine. Arbitrary payload CNOT routing has depth <=17; clock-controlled payload depth <=11; GHZ28 uses 27 CNOTs, <=82 pair pulses, and parallel depth 10. This assumes native pairwise exchange and pairwise cross-Kerr interactions; platform-specific strengths and fault tolerance remain open.

## 4179 — arbitrary-real-amplitude Hodge decoder
Let D be the 80x160 oriented Levi incidence matrix and let Z have 81 orthonormal rows spanning ker(D). For M=[D;Z],
`M^T M = D^T D + P_H1`
has exact spectrum `1^81, (4-sqrt6)^24, 4^30, (4+sqrt6)^24, 8^1`. Hence sigma_min=1 and condition number 2sqrt2 on the entire 160-dimensional edge space. For arbitrary real errors, least squares obeys `||ehat-e||_2 <= ||n||_2`; if all 161 measurement channels have absolute noise <=eta, the error is <=sqrt(161) eta. The prior two 15-bit modular moments remain the compressed lattice-amplitude mode; this 81-cycle-channel sensor is the globally conditioned fallback.

## 4180 — PDK-grounded tapped-delay materialization
The actual noncrossing layer populations require 919 equalization slot-units, not the older conservative 1280-unit envelope. At 5 ps and assumed group index 2, one slot is 0.749481145 mm, maximum delay is 5.99584916 mm, and aggregate delay length is 0.688773172255 m. The exact delay histogram for 160 routes is `{0:1,1:6,2:6,3:14,4:18,5:20,6:23,7:27,8:45}`.

The selected current public platform input is LIGENTEC's TFLN-on-SiN stack (AN350/AN800-compatible SiN routing): public specifications list SiN optical loss <0.5 dB/m, on-chip modulator loss <0.7 dB, 200 mm processing, and modulation capability up to 100 GHz. At the passive-loss upper bound the longest delay contributes <=0.002998 dB/use and <=0.014990 dB over five uses. A legacy public AN800 reference gives a 50 um bend-radius example with <0.005 dB over ten turns, but the current proprietary PDK must revalidate geometry. The taps are statically assigned; no 200 GHz dynamic 5-ps switch is claimed. GDS/DRC, tap/coupler loss, dispersion, electrical routing, and fabrication remain open.

## 4181 — symmetry-stratified interval push
For the point stabilizer (order 648), the vertex orbits have sizes 1+12+27 and quotient adjacency `[[0,12,0],[1,2,9],[0,4,8]]`. Interval evaluation plus Krawczyk exclusion on the full maximum-principle boxes proves exactly three equilibria for each selector: the origin and one global-sign pair of nonzero mixed roots. The nonzero roots are stable inside this quotient but have the previously certified full-space Morse indices 23 (selector24) and 14 (selector15), so transverse symmetry breaking destabilizes them.

Two larger strata are now explicitly mapped. The setwise edge stabilizer (order 108) has orbit sizes 2+2+18+18; a deterministic 3000-start quotient corpus finds three selector24 roots modulo sign and two selector15 roots. The setwise nonedge stabilizer (order 48) has orbit sizes 2+4+16+2+16; corresponding corpora find seven and five roots modulo sign. Those larger-stratum counts are discovery corpora, not interval-exhaustive theorems.

## 4182 — exact three-channel scattering kernel
Assign adjacency-sector phases 12->1, 2->i, -4->-1. The unique quadratic unitary is
`S=(-3/10+4i/5)I+(19/120+2i/15)A+(-1/240-i/60)A^2`
=`(-1/3+2i/3)I+(1/6+i/6)A+(-1/60-i/15)J`.
A localized input therefore has amplitudes `-7/20+3i/5` on itself, `3/20+i/10` on each neighbor, and `-1/60-i/15` on each nonneighbor. Probabilities are 193/400 self, 39/100 over all neighbors, and 51/400 over all nonneighbors.

## 4183 — exact matrix-forest ensemble
The rooted-spanning-forest partition function is
`Z_f(t)=det(I+tL)=(1+10t)^24(1+16t)^15`.
At t=1 there are exactly `28194101862441165313701387046733006325904913` rooted spanning forests. W33 has `28823037615171174400000000000000000000000` spanning trees. At t=1 the expected forest edge count is 6720/187, expected component count 760/187, and edge-count variance 98400/34969. The finite partition function is analytic for t>=0.

## 4184 — minimum-polynomial spectral lens
`K=P_2-P_-4=(I+A)/3-(13/120)J=(11/20)I+(67/240)A-(13/480)A^2` annihilates the uniform sector, gives +1 on the 24-dimensional sector, and -1 on the 15-dimensional sector. Exactly `K^2=I-J/40` and `K^3=K`. Quadratic degree in A is minimal. One neighbor sum plus exact global consensus applies the filter distributively.

## Evidence boundary
All promoted claims are finite algebraic, graph-theoretic, interval-certified low-dimensional, or explicitly labeled engineering-contract statements. No Standard Model derivation, fabricated processor, measured decoder, DRC-clean chip, global 80D nonlinear completeness theorem, scattering experiment, material phase transition, optical lens fabrication, gravity, cosmology, or theory of everything is claimed.
