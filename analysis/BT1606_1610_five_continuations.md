# Passes 1606–1610 — torsion filtration, resolution XORs, chiral packing, lattice bridge, and coherent configuration

## Executive result

This packet executes all five continuations opened by Passes 1601–1605 after reconciling the parallel Passes 1537–1541. The deterministic verifier rebuilds W(3,3), the 540-frame carrier, the 45 intrinsic K4,4 octets, the Bockstein map, both edge lattices, and the full PSp(4,3) action. All ten release assertions pass under certificate SHA-256

```text
b7e0a7d9c1333c8daf624a8527d44bee0375bc2321cd34eb41ebcb61264d29d0
```

The global nine-cover resolution remains open.

## Pass 1606 — complete modular structure of the 30-dimensional torsion

The Bockstein quotient

\[
T=\operatorname{Tor}_2(\operatorname{coker}M)\cong\mathbb F_2^{30}
\]

is not irreducible and is not semisimple. Its exact nonsplit filtration has composition factors

\[
\boxed{1,6,8,1,14.}
\]

There is a distinguished 16-dimensional submodule with Loewy profile

\[
\boxed{1\mid(6\oplus8)\mid1,}
\]

and an absolutely irreducible 14-dimensional head. The 6-dimensional factor is absolutely irreducible. The 8-dimensional factor is irreducible over F2 but has generated algebra dimension 32, hence endomorphism field F4 rather than absolute irreducibility over F2. Every nonzero vector generates the full 6- or 8-dimensional factor. Exact section equations prove both the top extension and the middle extension are nonsplit.

## Pass 1607 — independent XOR compiler for the exact resolution problem

The 45 octets yield 405 exact cardinality equations

\[
\sum_{f:\,|f\cap o|=2}x_{f,c}=8,
\qquad o=1,\ldots,45,\ c=1,\ldots,9,
\]

each supported on 72 frame/color variables. Rationally these are implied by the edge equations. Modulo two, they expose the thirty Bockstein directions per color:

\[
195\longrightarrow225.
\]

For the full nine-color system including one-color-per-frame equations, the exact ranks are

\[
\boxed{2100\longrightarrow2340,}
\]

a gain of 240. A deterministic independent basis uses thirty octet rows for each of colors 0 through 7; color 8 is forced by the frame-partition equations. The repository now contains a deterministic solver-neutral compiler for both outputs:

- 240 independent XOR equations;
- all 405 exact-eight equations.

No timeout is promoted to a SAT or UNSAT conclusion.

## Pass 1608 — chiral four-packing orbit and torsion signature

The certified four-cover packing has trivial PSp(4,3) stabilizer, so its inner orbit has size 25,920. An anti-symplectic similitude produces a mirror packing outside that orbit. The two free PSp orbits are fused by PGSp(4,3):

\[
\boxed{25920+25920=51840.}
\]

The base and mirror residual systems have identical exact binary signatures:

```text
residual frames                         300
rank_F2 residual M                      195
rank_F2 residual [M|J]                  225
Bockstein gain                           30
rank_F2 residual J                       44
used octet degree                        32
residual octet degree                    40
```

Their residual octet Gram matrices are literally conjugate under the outer element. Thus the binary Bockstein sector cannot distinguish this packing chirality. The no-fifth result for the mirror follows equivariantly from the frozen Pass-1515 certificate; this is not a global census of all possible four-packings.

## Pass 1609 — saturated free-15 bridge

Let L be the saturated integral point (-4)-eigenlattice. Its unsigned and oriented edge images have Smith forms

\[
\operatorname{SNF}(N^TL)=1^{14}\oplus2,
\]

\[
\operatorname{SNF}(d^TL)=1^{14}\oplus4.
\]

After saturating both rank-15 edge lattices, the canonical unsigned-to-oriented transition is integral and satisfies

\[
\boxed{\operatorname{SNF}=1^{14}\oplus2,\qquad|\det|=2.}
\]

This resolves the old factor 6 in the integral signed bridge: the common ternary index contributes 3, while one unavoidable orientation-parity defect contributes 2.

## Pass 1610 — complete frame/octet coherent configuration

The PSp(4,3) action on the disjoint union of 540 frames and 45 octets forms a two-fiber coherent configuration. Its relation counts are

\[
\boxed{32+3+5+5=45.}
\]

The five frame-to-octet cross subdegrees are

\[
1,6,6,8,24,
\]

and the reverse subdegrees are

\[
12,72,72,96,288.
\]

The half-incidence matrix J is one of the row-valency-six cross orbitals. Its octet Gram coefficients on diagonal, disjoint, and overlapping octet relations are

\[
\boxed{72,6,9.}
\]

The H-cyclic closure satisfies

\[
(H-32I)(H-14I)(H-2I)J=0
\]

and has rank 69. Exact spectral coupling ranks are

\[
32\to32:1,
\]

\[
2\to14:24,
\qquad2\to2:24,
\]

\[
-4\to14:20.
\]

Thus the octet 20-sector lands only in the frame eigenvalue-14 sector, while the octet 24-sector embeds diagonally into two isomorphic frame 24-sectors at eigenvalues 14 and 2.

## Parallel-frontier reconciliation

Passes 1537–1541 already owned the absolutely irreducible modular 14, the 405 exact-eight cuts and rank gain 240, the low-layer weight-enumerator programme, and the exact decoder falsifier. This packet does not relabel those results. It adds the full 30-dimensional Loewy filtration, executable cut exports, the chiral four-packing orbit theorem, the saturated determinant-two free lattice bridge, and the complete two-fiber coherent configuration.

## Evidence boundary

All module, orbit, rank, Smith, export, conjugacy, and coherent-configuration statements are finite exact computations. The packet does not decide the global Hoffman nine-coloring, prove the known four-packing family exhaustive, establish a decoding threshold, or infer continuum physics.
