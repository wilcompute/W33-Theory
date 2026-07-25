# Passes 871–875 — exact ATLAS transport, explicit Heisenberg bases, scalar Schur cocycle, adaptive-regret control, and fail-closed photonic dispatch

## Pass 871 — exact ATLAS standard-generator transport

The mod-two factors of dimensions 6, 14, and 40 are matched to the official characteristic-two representations of the outer group

\[
U_4(2){:}2 \cong PSp(4,3){:}2.
\]

The calculation does not assume that an arbitrarily chosen outer intertwiner is already the ATLAS class-2C generator. Instead it reconstructs the index-two inner subgroup inside the official outer matrices, certifies an inner standard pair of orders

\[
(2,5,9),
\]

simultaneously conjugates each repository factor to that inner pair, and transports the official outer generators back through the exact conjugators. The resulting outer pairs have orders

\[
|c|=2,\qquad |d|=9,\qquad |cd|=10
\]

in dimensions 6, 14, and 40, and the dimension-six pair generates the full outer group of order

\[
\boxed{51840}.
\]

The 40-dimensional outer extension generates the full algebra

\[
M_{40}(\mathbf F_2)
\]

and has scalar endomorphism ring. Thus its inner restriction's \(\mathbf F_4\) commutant is explained by fusion of the Frobenius-conjugate 20-dimensional constituents under the outer involution.

## Pass 872 — explicit \(H_{27}\) Loewy bases

The ten-dimensional three-primary correspondence module is restricted to the extraspecial Heisenberg group \(H_{27}\). Two certified subgroup generators yield nilpotent degree-raising operators

\[
x=X-I,\qquad y=Y-I.
\]

A deterministic cyclic vector gives the canonical monomial basis

\[
1;\quad x,y;\quad xx,xy,yx,yy;\quad xxy,xyy;\quad xxyy.
\]

The radical dimensions and Loewy layers are

\[
10,9,7,3,1,0
\]

and

\[
\boxed{1,2,4,2,1}.
\]

The four-dimensional middle layer now has an explicit basis

\[
\boxed{xx,xy,yx,yy},
\]

with its transition blocks and all basis columns expressed in the original cut-quotient coordinates. This also corrects the earlier structural overstatement: for the extraspecial group of order 27,

\[
H_{27}/Z(H_{27})\cong \mathbf F_3^2,
\]

not \(\mathbf F_3^4\). The degree-one layer is correspondingly two-dimensional.

## Pass 873 — explicit scalar Schur factor set

A deterministic section of the projective quotient

\[
Sp(4,3)\longrightarrow PSp(4,3)
\]

chooses lexicographically between \(M\) and \(-M\) for every projective element. The resulting factor set is defined by

\[
s(g)s(h)=(-I_4)^{c(g,h)}s(gh).
\]

The certificate contains all 25,920 section elements, 103,680 directed generator edges, and 49,248 negative edges. It verifies

\[
\boxed{414720}
\]

generator-triple cocycle identities. Coboundary propagation creates 22,200 contradictions, proving the factor set nontrivial. Two displayed presentation relators lift to \(-I_4\), giving a compact presentation representative of the unique nonzero scalar \(H^2\) line.

The associated coefficient cocycle is

\[
\boxed{c(g,h)I_{81}}.
\]

It is the ambient Schur-multiplier class, distinct from the realized W33 deformation obstruction, which remains zero because the exact integral 81-dimensional action supplies the compatible two-adic tower.

## Pass 874 — adaptive audit regret game

The audit problem is formulated as a zero-sum partially observed game with five hidden failure states, four unequal-cost probes, binary observations, and the five-component likelihood-ratio vector as sufficient statistic.

An information relaxation gives the controller the hidden failure identity for free. Its minimax oracle lower bound is

\[
\boxed{540.5675691787816}
\]

physical cost units. Fifteen predictable policies are separated into training, validation, and a third untouched holdout. The prior 20/80 policy does not survive validation. The promoted policy uses

\[
\boxed{30\%\text{ robust exploration}}
\]

and a temperature-one posterior-weighted KL-per-cost exploitation rule.

On the third holdout, its normalized regret above the oracle lower bound is

\[
\boxed{0.1939129570},
\]

versus

\[
0.2272933817
\]

for the incumbent, a 2.72% improvement in worst mean physical cost. No null alarms occur in 100 untouched null trials, and every failure is detected in the declared trial family.

## Pass 875 — fail-closed hardware phase dispatcher

A global audit of the Pass 855 nine-hyperplane depth-four classifier finds

\[
\boxed{1089}
\]

off-wall integer counterexamples. Therefore the nine hyperplanes do not form a complete phase arrangement; the prior tree is exact on its selected 19 witnesses but unsafe as a global continuous classifier.

The corrected hardware is fail-closed:

1. every declared integer cell is stored in an exact 7,776-byte ROM;
2. all 22 phases are encoded;
3. Q12 inputs are accepted by the ROM only when all fractional bits vanish and every coordinate is in range;
4. fractional or out-of-range inputs return phase 255 and assert fallback;
5. the integration layer delegates fallback requests to the exact 1,000-node Pass 825 continuous DAG.

The exact ROM address is

\[
((((((c_1-4)4+(c_2-6))6+(Q-7))3+(s_1-5))3+(s_2-3))3+o)3+\kappa.
\]

The release includes a C header, synthesizable SystemVerilog, and the ROM memory image, all hash-locked by the certificate.

## Verification boundaries

- Pass 871 locks the official source URLs and source SHA-256 digests. Regeneration remains network-dependent until the small public matrices are vendored into the repository.
- Pass 872 gives exact bases and transition matrices for the chosen certified \(H_{27}\); normalizer fusion of every graded layer remains a separate calculation.
- Pass 873 identifies the non-split scalar factor set but does not equate it with the realized deformation obstruction.
- Pass 874 provides an oracle lower bound and out-of-sample regret certificate; it does not prove global dynamic-programming optimality among all measurable adaptive policies.
- Pass 875 is exact on the declared integer atlas and fail-closed elsewhere. It deliberately retracts the unsafe global use of the Pass 855 fast tree.
