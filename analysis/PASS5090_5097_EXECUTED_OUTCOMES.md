# Passes 5090–5097 — root-direction derivative geometry, q=4 rigidity, integral sqrt(17), and arithmetic compiler locality

**Status:** EXECUTED 2026-08-14. All promoted statements are finite building/group combinatorics, exact linear algebra, or bounded/local optimization statements. The formal derivative notation in Pass5090/5096 is combinatorial: q is a prime power, not a continuous physical variable.

## 5090 — C2 root-coset first-derivative theorem
For W(3,q), a fixed chamber lies in q^4 apartments. Equivalently, the chambers opposite the fixed chamber form the maximal-unipotent big cell U of type C2, with |U|=q^4. There are four positive roots. Each associated root subgroup U_alpha has order q and therefore q^3 cosets in U.

The chamber-star codeword activates exactly these four root-direction orbit families, so

`A_chamber = 4 q^3 = d(q^4)/dq`

as an exact formal root-coset count. Every active chart contains q of the q^4 supported apartments and every supported apartment belongs to four active charts, giving `4 q^4 = q A_chamber`.

Independent q=2 and q=3 reconstructions identify the chamber-star active-chart hypergraph with the coset hypergraph of the four positive-root subgroups.

**Boundary:** this explains the extremal chamber count. It does not prove that every non-cut cochain has at least 4q^3 active charts; the all-q distance theorem remains open.

## 5091 — q=4 local-minimum-cut rigidity
Assume every active q=4 chart is a minimum 1|4 cut of K5. Fix one apartment. Its four incident active charts have two singleton-root choices each, giving 16 seeds. Exact propagation leaves eight consistent seeds and rejects eight.

The eight consistent solutions are exactly the eight chamber-star weight-256 words through the fixed apartment. Therefore any hypothetical non-chamber weight-256 word must use at least one heavier 2|3 local chart.

If A2=2t counts the heavier 2|3 charts in a weight-256 word, then the number of 1|4 charts is `A1=256-3t` and the total active-chart count is `256-t`.

**Boundary:** conditional rigidity, not complete q=4 minimum-shell classification.

## 5092 — integral sqrt(17) Hecke/transfer bridge
For the twisted-Hecke block

`A=[[1,4],[1,0]]`

and corrected historical transfer block

`B2=[[4,2],[2,5]]`,

the unimodular matrix

`P=[[2,-1],[-1,1]]`, `det P=1`,

satisfies

`A P = P (B2-4I)`.

Thus the blocks are GL(2,Z)-conjugate after the historical shift, not merely rationally similar. The polynomial `x^2-x-4` has discriminant 17 and generates the maximal quadratic order. The q=3 affine block `4A+10I` has polynomial `x^2-24x+76`, discriminant 272=16*17, and generates the conductor-4 suborder.

**Boundary:** exact integral/order bridge; no geometric carrier intertwiner is inferred solely from this similarity.

## 5093 — V24 Smith-floor one-exchange rigidity
Reconstruct the point-local centered transport `Z24=5Z-12J` and the frozen 24 tritangent core. The known raw bases reproduce:

- original: denominator 9360, kappa2 ~186.704;
- balanced: denominator 3120, kappa2 ~105.462;
- Smith floor: denominator 780, kappa2 ~72382.483.

Using an exact Sherman-Morrison denominator update, all 3289 full-rank one-row exchanges around the D=780 floor basis were enumerated. Exactly eight preserve D=780. Every one is worse conditioned; the best floor-preserving neighbor has kappa2 ~74483.194.

Hence the frozen D=780 basis is a strict local minimum of condition number in the one-row exchange graph of D=780 raw bases.

**Boundary:** one-exchange local optimum, not a global optimum over all floor bases.

## 5094 — q=3 derivative graph is the unipotent root-coset graph
The 81 chamber-star apartments and 108 active three-apartment charts form the same incidence geometry as the 81 elements of the C2 maximal unipotent group U and the 108 cosets of its four positive-root subgroups.

The point graph is the Cayley/root-coset graph

`Cay(U, union_alpha(U_alpha - {1}))`.

It has degree 8, diameter 3, distance shells `1,8,32,40`, and characteristic polynomial

`(x-8)(x-5)^4(x-2)^10(x+1)^18(x+4)^12(x^2-4x+1)^6(x^2-x-8)^6(x^2+2x-2)^6`.

In particular it is not the Hamming graph H(4,3). The failure of the naive Hamming model is the first visible sign of noncommutative root-group geometry.

## 5095 — higher derivative is commutator-curved
For odd q, the six unordered pairs of the four positive-root subgroups have generated subgroup orders

`q^2,q^2,q^2,q^2,q^3,q^4`.

Exact anchors:

- q=3: `9,9,9,9,27,81`;
- q=5: `25,25,25,25,125,625`;
- q=7: `49,49,49,49,343,2401`.

Thus four direction pairs behave like independent flat coordinates, one pair closes one extra root direction, and the simple-root pair generates the full unipotent cell. At q=2 the bad-characteristic profile collapses to `4,4,4,4,4,8`.

This supplies a precise interpretation of the calculus analogy: first derivative = root-direction fibers; second and higher direction composition is deformed by Chevalley commutators.

## 5096 — split Lie-type Steinberg derivative law
Let a split finite Chevalley group have N positive roots. Its maximal unipotent subgroup has order q^N, equal to the defining-characteristic Steinberg degree. Each positive-root subgroup has order q, hence has q^(N-1) cosets in U. Summed over all N positive roots, the root-direction coset count is

`N q^(N-1) = d(q^N)/dq`.

For type C2, N=4, recovering 4q^3.

**Boundary:** this is a general root-coset counting law. Only in the rank-two W(3,q) apartment-code setting has the identification with active distance-test charts been established here.

## 5097 — q=3 derivative graph automorphism closure
Exhaustive graph automorphism enumeration gives

`|Aut(G_der)| = 324`.

The full projective W33 symmetry has order 51840 and 160 chambers, so its chamber stabilizer also has order

`51840/160 = 324`.

The natural chamber-stabilizer action is faithful on the derivative incidence geometry; equality of orders therefore identifies the entire derivative-graph automorphism group with the full projective chamber stabilizer. No larger graph symmetry remains.

## Synthesis
The user's observation that 4q^3 resembles the derivative of q^4 is mathematically substantive: the equality is the exact count of first-order positive-root coset directions in the q^4 unipotent/Steinberg big cell. The ordinary four-dimensional Hamming interpretation is false; the correct object is nonabelian C2 root geometry. The commutator census shows exactly where the analogy stops behaving like ordinary multivariable calculus.

The open global problem remains the sharp expansion inequality: prove every nontrivial Levi cohomology class activates at least 4q^3 charts (or equivalently prove the corresponding Fourier extremal bound). Pass5090 explains the equality case but does not supply that universal lower bound.
