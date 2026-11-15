# The quiver projections in the rank-27 toroidal charge lattice

The primitive Type IIB link of the cubic surface has six RR Betti charges. The [wrapped-charge test](2026-11-15_cubic_quiver_five_checks.md) shows that the $E_6$ cubic cannot be inferred from those six charges. A separate compactification, M-theory on $T^6$, supplies 27 independent conserved charges: six Kaluza–Klein momenta $P_i$, 15 M2 wrapping numbers $M_{ij}$, and six M5 wrapping numbers $K_i$ on the oriented complementary five-cycles. The cubic surface and toroidal charge correspondence is established in the literature. Here it gives an explicit integer change of basis for the traced quiver supports and a projection rule for each of the 40 charts. [Pioline, toroidal black-hole charges](https://arxiv.org/abs/hep-th/0506228) · [Sati and Voronov, toroidal M-theory and del Pezzo surfaces](https://arxiv.org/abs/2212.13968)

## Integral term-by-term map

For the standard double-six pair of exceptional and conic lines, take $E_i\leftrightarrow P_i$, $Q_i\leftrightarrow K_i$, and $L_{ij}\leftrightarrow M_{ij}$. Choose orientations for the M5 coordinates and write the conventional split cubic as

$$N(P,M,K)=\operatorname{Pf}(M)+\sum_{i<j}M_{ij}(P_iK_j-P_jK_i).$$

The fifteen perfect matchings of six directions are the Pfaffian terms. The two orientations of each of the fifteen pairs give the thirty mixed terms. These are exactly the 45 tritangents, with no extra monomials. The code expands the three determinants and the trace in the quiver presentation, then solves a binary linear system for a signed change of basis. Substituting those signs makes every one of its 45 coefficients agree with the toroidal formula. The map is unimodular, so the comparison works over the integer charge lattices. The same method gives integral signed lifts preserving the cubic for the six simple Weyl reflections. [Duff and Ferrara, the $E_6$ cubic in the three-matrix basis](https://arxiv.org/abs/0704.0507)

## One quiver support is a linear response to crossing M2 charges

Split the six torus directions into unordered triples $U,V$. Let $M_\times$ be the nine M2 directions with one index in each triple. Scale the coordinates in $M_\times$ by $\lambda$ and keep all other charges fixed. Then

$$N(\lambda)=N_0+\lambda N_1+\lambda^3 N_3.$$

A Pfaffian term crosses the split once or three times, since each side has odd size. A mixed term crosses once or zero times, according to its single M2 factor. The exact check identifies $N_1$ with the signed restriction of $N$ to the chart for that cut. Its 27 terms consist of nine Pfaffian terms and eighteen mixed terms. If $N_0\ne0$, this coefficient controls the first variation of the semiclassical nonrotating entropy proportional to $\sqrt{|N|}$ along that charge direction. This use of the classical invariant treats the charges as continuous parameters in supergravity.

There are ten cuts. A Pfaffian matching crosses three times in four cuts, one for each assignment of its paired ends to opposite sides modulo swapping the sides. It therefore contributes to $N_1$ in six cuts. For a mixed term its M2 pair lies on the same side in four cuts, so the mixed term also contributes in six. This supplies a toroidal derivation of the factor $1/6$ in the [ten-support reconstruction](2026-11-15_cubic_quiver_ovoid_recovery.md).

The six signed reflection lifts transport the ten-cut rule to all 36 double-six frames. The verifier matches all 360 frame–cut incidences to the existing ovoid certificate. Each chart occurs in nine frames. Those nine occurrences give three distinct sets of crossing charge directions, each appearing in three frames. The certificate gives the original chart labels and the lift generators.

The dictionary evaluates the same invariant in the established toroidal charge lattice. It supplies no dynamical equivalence between the Type IIB del Pezzo probe and M-theory on the flat torus. Whether a construction can link the two dynamics while retaining the 27 physical charges remains open.

Replay with NetworkX and SymPy.

    python -B analysis/toe_20261115_quiver_torus_charges.py

The [integer certificate](../data/toe_20261115_quiver_torus_charges.json) records the orientations, frame counts, and cut assignments.
