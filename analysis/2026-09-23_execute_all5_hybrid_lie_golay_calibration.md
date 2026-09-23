# 2026-09-23 — Execute all five: cubic transport, hybrid E8 Lie compiler, Golay Strange lane, G2 no-go, photonic calibration

## Baseline repair

Before extending the frontier, the previously queued dedicated compiler workflow
was inspected. Its three failures were replay plumbing rather than theorem
failures:

1. the Qpsi cubic certificate had moved from a cached sum_Qpsi field to the
   authoritative Qpsi list;
2. the photonic schedule depended on an untracked generated BT1575 JSON even
   though the authoritative protocol table is committed as a Python source;
3. the shared-tail integrity test accidentally rejected the valid single
   backslash \input syntax it first required.

All three were repaired before the five new fronts were integrated.

## 1. Actual E6 cubic tensor -> 73+8 hybrid matter chart

The historical canonical SU(3)+E6 gauge solve remains source-locked under
extracted_v13.  Pass1103 independently supplies an exact e6id -> H27 normal
form coordinate:
  i -> (u0,u1,z).

Those Pass1103 coordinates are a valid exact H27 gauge for the canonical cubic,
but they are not literally the later physical-Clifford address gauge: the two
raw 45-line label sets overlap in 10 triads, including all nine firewall
fibers.  A separate anchored 27-point gauge conjugacy is now frozen.  It sends
e6id 0 to the current H27 identity, maps all nine firewall fibers to the
current center spread, and carries all 45 canonical cubic triads exactly to
the current five-direction/45-coset H27 line set.

In the canonical root gauge,

  [e_(i,a),e_(j,b)] = d_ijk epsilon_abc ebar_(k,c).

Exhaustion gives:

- 45 signed E6 triads;
- sign split 22 plus / 23 minus;
- 810 nonzero unordered g1 x g1 -> g2 root channels;
- exactly 162 channels on the bad-nine/firewall fibers;
- every g1 root participates in 20 channels;
- every g2 root occurs as output ten times.

Let B81 be the landed 73-cubic + 8-dark hybrid basis.  The complete hybrid
cubic tensor is represented exactly and compactly by

  T_hyb = conjugate(B81)^(-1) o T_root o (B81 tensor B81).

A dense 81^3 artifact is unnecessary.

For the tangent maps D_v(x)=[v,x], every root-basis background has rank 20.
However, the collective image span of the 81 root-background Jacobians is all
81 dimensions of g2.  Thus after charge conjugation and the minimal compiler
projection the FAMILY reaches all 54 retyped operator slots.  A single
rank-54 background is not claimed.

Evidence:
- analysis/w33_e6_cubic_hybrid81_transport.py
- data/w33_e6_cubic_hybrid81_transport.json

## 2. Full 248D hybrid Chevalley compiler

The committed source algebra is the complete sparse W33-discrete E8 Chevalley
table:
  artifacts/e8_structure_constants_w33_discrete.json.

Archived exact root metadata maps its 240 roots into the physical
86+81+81 FI grading and supplies i27/i3 labels.  The canonical phase solution
then aligns the matter-root signs with the same E6 cubic gauge used above.

The exact basis transform is

  A = I86 direct_sum (P1 G1 B81)
          direct_sum (P2 G2 conjugate(B81)),

where P1/P2 are root-label permutations and G1/G2 are diagonal +/-1 root
gauges.  Both matter blocks have exact inverses over Q(omega).

The complete hybrid bracket is therefore executable as

  [x,y]_hyb = A^(-1) [A x,A y]_Chevalley.

All six graded products are covered:
  g0g0->g0, g0g1->g1, g0g2->g2,
  g1g1->g2, g1g2->g0, g2g2->g1.

The dedicated workflow performs the full source Jacobi sweep over

  C(248,3) = 2,511,496

basis triples.  Exact invertibility of A then transports the Jacobi polynomial
identically to the hybrid basis.  This closes the finite Lie-algebra coordinate
compiler, not a spacetime Hamiltonian.

Evidence:
- analysis/w33_e8_full_hybrid_chevalley_compiler.py
- data/w33_e8_full_hybrid_chevalley_compiler.json

## 3. W33-internal [[11,1,5]]_3 Strange distillation code

The repo already reconstructs the perfect ternary Golay
G11=[11,6,5]_3 from each local W33 K5 fiber.  The new producer proves the
additional quantum-CSS statement:

  dim G11^perp = 5,
  G11^perp subset G11,
  Hx=Hz=G11^perp,
  k = 11-5-5 = 1,
  d = 5.

Hence the internal code is exactly a [[11,1,5]]_3 CSS code with correctable
Pauli weight two.  This is the code used by the published ternary-Golay
Strange-state distillation protocol.

The exact runtime handoff is now

  DARK_STRANGE_Q3_RAW
    -> STRANGE_Q3_RAW by X Z^2
    -> 11-copy Golay CSS projection/decoding
    -> GOLAY11_STRANGE_LOGICAL.

Published prior art supplies cubic Strange-state error suppression and a
depolarizing threshold near 0.38715 in its convention.  Recent searches and
the 2026 quadratic-residue-code treatment retain Golay as the benchmark.

The physical lane remains fail-closed.  Missing evidence gates include a
measured/twirled input-noise upper bound, 11-copy source correlations,
fault-tolerant syndrome extraction, circuit-level fault census, mapped decoder,
protected non-Clifford injection, physical threshold certificate, and device
calibration.

Evidence:
- analysis/w33_dark_strange_golay11_ft_lane.py
- data/w33_dark_strange_golay11_ft_lane.json

## 4. G2 branching shadow: strict external-C3 extension killed

The dark K-module is

  chi_ext + chi_ext^2 + V_omega + V_omega^2.

After forgetting external C3 this is

  1 + 1 + 3 + 3bar,

matching 1+7 under G2 -> SU(3).

The full external C3 spectrum is instead

  1^6 + omega + omega^2.

Suppose a K-compatible G2 promotion existed with D8=1_G2+7_G2 and with
external C3 commuting with G2.  The G2-fixed line must lie in the two-dimensional
H27-invariant singlet plane and, because external C3 has distinct eigenvalues
there, must be one of the two charge eigenlines.  The complementary irreducible
seven then has spectrum either

  1^6 + omega
or
  1^6 + omega^2.

That is non-scalar.  Schur's lemma says every operator commuting with an
irreducible complex G2 seven is scalar.  Contradiction.

Therefore the strict commuting G2 x C3_ext promotion is impossible.  The
previous G2 observation survives only as a branching shadow after forgetting
external C3.  A larger NONCOMMUTING envelope remains open.

Evidence:
- analysis/w33_dark8_g2_external_c3_no_go.py
- data/w33_dark8_g2_external_c3_no_go.json

## 5. 36-channel coherent photonic calibration theorem

A concrete design target is now frozen:

  F_target = 0.99

for the normalized full 36x36 coherent transfer matrix.  This is an engineering
choice, not a prediction or measurement.

With one phase-referenced tritter and one matched HOLD per channel, separate
common loss from differential coherent error.  For residual phase
|delta_phi_j|<=phi, the coherent phase factor is at least cos^2(phi).  For
positive amplitude gains bounded by exp(+/-s), Kantorovich gives a normalized
gain-overlap lower bound sech^2(s), with

  s = (ln 10 / 20) L_max_dB.

Using the sufficient model

  F_model >= F_TRI cos^2(phi_max) sech^2(s)

and allocating the 0.99 target equally over three factors gives

  f = 0.99^(1/3) = 0.996655493413,

so sufficient component gates are

  F_TRI >= 0.996655493413,
  |delta_phi| <= 0.057863994222 rad = 3.31536265468 degrees,
  |delta_L| <= 0.502880974035 dB about the common HOLD loss.

The peak-to-peak differential-loss window is therefore 1.00576194807 dB.

The decisive laboratory criterion is stronger than the factorized budget:
characterize ONE hardware stack, reconstruct its complete complex transfer
matrix M, and require

  F_HS(M)=|Tr(U_ideal^dag M)|^2 / (36 Tr(M^dag M)) >= 0.99,

while also retaining the existing |delta V(F3)|<=0.05 and radial leakage<=0.10
falsifiers.  Common insertion loss, source efficiency and detector efficiency
are reported separately because they affect success probability rather than
normalized conditional process overlap.

Evidence:
- analysis/w33_hesse36_photonic_process_calibration_theorem.py
- data/w33_hesse36_photonic_process_calibration_theorem.json

## Frontier

The finite TOE/compiler stack is materially sharper:

1. the actual signed E6 cubic is objectwise connected to the current hybrid
   matter/address carrier by an explicit full-45 gauge conjugacy, rather than
   by conflating two independent H27 coordinate gauges;
2. the 248D hybrid atlas now has an exact complete Chevalley bracket transport;
3. the dark Strange ray lands on a W33-internally reconstructed quantum Golay
   code of exactly the published [[11,1,5]]_3 type;
4. the tempting commuting G2 extension is ruled out by the external C3;
5. the photonic compiler now has a falsifiable full-process calibration target.

The remaining gaps are increasingly dynamical/experimental rather than missing
finite algebra.
