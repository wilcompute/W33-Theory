# W33 Arithmetic Clock Split and Rank-Two Interface — 2026-10-21

**Status:** Exact local finite-field/operator deductions and reproducible finite-rank tests. No classical Riemann hypothesis proof, device-level phase revival, or all-prime arithmetic correspondence.

## Repo search and priority correction

Existing repository work is broader than filenames suggest:

- Pass 5041 (data/PART_W33_PASS5041_INTEGRAL_APARTMENT_GENERATION.json) already proves an integral unimodular 81-apartment basis of the Levi cycle lattice. Independent Hermite normal form I_81 reproduces **prior work**, not a new theorem.
- Pass 5051 (data/PART_W33_PASS5051_Q_FAMILY_THETA_CODE.json) already certifies the q=3 apartment character code [1620,81,81]. The independently calculated three-edge frustration minimum 81 is not a new distance theorem.
- analysis/2026-10-21_levi_genus2_local_frobenius_bridge.md already identified p3 local genus-two and elliptic factors; analysis/2026-10-21_rh_five_followups_synthesis.md supplies the rational 156D operator embedding.
- analysis/2026-10-21_rh_next5_deep_results.md already disproves exact zeta-zero matching for the previously proposed Lambert-W model using inverse-fourth moments.
- The new work is a cross-prime *arithmetic phase-order comparison* and a density-preserving W33/external-operator interface, not a rediscovery claim about the classical arithmetic geometry.

## 1. Exact prime-3 supersingular eight-step spectral revival

Let L be the 80-vertex W33 Levi adjacency matrix and T=[[L,-3I],[I,0]] the 160D Bass companion. Its 156-dimensional nontrivial invariant sector is a 96D sum of 24 cyclic modules annihilated by x^4+9 and a 60D sum of 30 modules annihilated by x^2+3.

Consequently (T^8-81I) vanishes **identically** on this nontrivial sector, equivalently (T/sqrt(3))^8=I. This is exact integer linear algebra verified in the producer.

The normalized nontrivial traces have period eight and first period:

    n=1..8:  0, -60, 0, -36, 0, -60, 0, 156.

The local Frobenius factors arise from C/F3: y^2=x^5+1 (genus two, x^4+9) and E/F3: y^2=x^3-x (elliptic, x^2+3). Every Frobenius 3-adic Newton slope is 1/2: both are supersingular. This is a standard algebraic consequence of these Weil polynomials, and the special genus-two curve was specifically studied by Everett W. Howe (2006).

## 2. Exact prime-11 ordinary and infinite-order obstruction

The W33 40-vertex collinearity graph has a distinct 78D nontrivial p11 packet, corresponding to elliptic local polynomials x^2-2x+11 (multiplicity 24) and x^2+4x+11 (multiplicity 15). Exact F11 curve counts for y^2=x^3+x-1 and y^2=x^3+x+2 give 10 and 16 points, hence traces 2 and -4. Both are **ordinary** because 11 divides neither trace.

No normalized nontrivial Frobenius eigenvalue is a root of unity: if lambda/sqrt(11) were a root of unity then lambda/sqrt(11)+sqrt(11)/lambda would be an algebraic integer, but this number squared is 4/11 or 16/11, a rational noninteger. Hence there is no finite-order normalized p11 clock analogous to the Levi p3 result.

This is a local arithmetic distinction across different characteristics, not an all-prime obstruction to zeta by itself.

## 3. Rank-two Feshbach interface avoids 39-fold zero density inflation

The W33 nonconstant internal matrix is K=2I_24 direct_sum(-4I_15), with 39 modes. Couple one separable channel of a self-adjoint arithmetic candidate H_a:

    H_total=[[H_a, eta u v*],[eta v u*, K]]

where u in l2(N), v in C^39. The off-diagonal perturbation has rank at most two. Finite-rank interlacing gives |N_total(T)-N_a(T)| <= 39+2=41 at every threshold. Hence the external T log T counting coefficient survives **without** a repeated 39-fold tower. Bounded coupling preserves compact resolvent if H_a has it.

When v has a nonzero component in both K eigenspaces, the exactly dark subspace has dimension (24-1)+(15-1)=37. Only two bright internal combinations participate.

The Schur complement identity is

    det(z-H_total)/[det(z-H_a)det(z-K)] = 1 - eta^2 g(z) h(z)

for g(z)=<u,(z-H_a)^-1 u> and h(z)=<v,(z-K)^-1 v>, away from poles with polynomial continuation. If v is uniform and normalized, h(z)=(24/39)/(z-2)+(15/39)/(z+4).

A 120-level Lambert-W *toy* arithmetic diagonal and eta=0.1, u_n=1/n passes 10 eigenvalue-count comparisons and 5 determinant-ratio checks against independently formed 159x159 matrices. The external toy fails Xi moment identities (already established in concurrent research); the interface does not fix that.

### Exact obstruction: density preservation does not imply an Xi spectral determinant

The proposed rank-two interface, with normalized v, has perturbation operator norm <= eta ||u|| < 0.13. The uncoupled spectrum consists of 15 copies of -4, 24 copies of 2, and external arithmetic ordinates above 17.84 for this toy model. Weyl eigenvalue perturbation bounds show that the full coupled matrix **still has at least 39 eigenvalues in the interval (-4.13,2.13)**. The test verifies this alongside the 37 exact dark levels. Yet the first positive classical Riemann zero ordinate is about 14.134725, and its negatives are symmetric; Xi has no zeros at such low absolute ordinates. Therefore the unmodified full coupled determinant **cannot equal Xi**, even if the external operator's high-lying level count is correct. The two-sector internal degrees of freedom must instead be treated as auxiliary/compressed or removed via a mathematically justified quotient/renormalization. An unproven cancellation is not an acceptable regularization.

An attempt to eliminate all *exact* dark levels by increasing the coupling rank still leaves 39 additional low-lying levels under sufficiently small norm perturbations. The counting coefficient remains right, but the full zero set stays wrong. This is an explicit negative result for this Hilbert-Polya block ansatz, not a general no-go theorem for arithmetic spectral triples.

## External sources and scope

- Everett W. Howe (2006), supersingular genus-two curves characteristic three: https://arxiv.org/abs/math/0604413
- Connes, Consani, Moscovici (2026), Zeta Spectral Triples: https://alainconnes.org/2026/07/zeta-spectral-triples/
- Independent Connes triple replication by Giuseppe Sorge (June 2026): https://github.com/giuseppesorge/zeta-spectral-triples-replication

The independent Connes construction numerically fits actual low-lying zeros dramatically better than a tuned asymptotic Lambert-W ladder. This suggests replacing the toy external diagonal with *actual prime-dependent arithmetic spectral operators* before assigning any evidence to W33 coupling. Finite-rank design by itself says nothing about Xi determinant equality.

## Five independent next steps

1. Build an actual Galois-compatible map (or character-level no-go) for the 156D supersingular Frobenius/Levi transfer packet.
2. Reproduce finite-prime Connes–Consani–Moscovici operators independently; compare Xi moments and determinants before/after rank-two coupling.
3. Prove interval-certified completed Weil positivity for smooth compact-supported test-function families, with all prime, gamma and endpoint terms.
4. Classify Newton slopes and normalized Frobenius phase orders for q-family Levi local factors at several characteristics, not by naive extrapolation from 3.
5. Seek a global arithmetic trace formula for the two W33 bright channels, or prove their incompatibility with the exact classical zeta explicit formula.

**Claim firewall:** All statements concerning classical RH remain open. The finite spectral revival is not a physical clock experiment.
