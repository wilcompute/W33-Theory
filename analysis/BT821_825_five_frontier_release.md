# Passes 821–825 — composition structure, the Heisenberg rank-four bridge, integral rigidity, minimax audit allocation, and facet-pruned continuous control

## Pass 821 — the 66-dimensional extension head is not simple

The question posed after Pass 802 assumed that the mod-two head of

\[
Z_1/(L_4+L_0)\cong (\mathbf Z/4)^{66}
\]

was a 66-dimensional simple module. It is not.

A deterministic MeatAxe decomposition gives a composition series with factors

\[
\boxed{14,\ 6,\ 40,\ 6}.
\]

The 14-dimensional factor and both 6-dimensional factors generate full matrix algebras over \(\mathbf F_2\), and the two 6-dimensional factors are isomorphic. The 40-dimensional factor has generated algebra dimension

\[
800=40^2/2
\]

and endomorphism-ring dimension two, so it is irreducible over \(\mathbf F_2\) with endomorphism field \(\mathbf F_4\); over \(\mathbf F_4\) it splits into Frobenius-conjugate 20-dimensional constituents.

The complete 66-dimensional module has endomorphism-ring dimension one but generated algebra dimension

\[
2276<66^2=4356.
\]

Thus it is Schurian and indecomposable, but reducible. This is a structural correction, not merely a relabeling.

## Pass 822 — the proposed cyclotomic rank-four target is retracted

The three-primary interface of the W33 cut lattice is a ten-dimensional \(\mathbf F_3\)-module. Its full-group generators span

\[
M_{10}(\mathbf F_3),
\]

so it is absolutely irreducible for \(PSp(4,3)\). No nonzero proper full-group quotient exists.

Restriction to an extraspecial qutrit Heisenberg subgroup \(H_{27}\) still reveals a striking internal filtration. Its radical dimensions are

\[
10,9,7,3,1,0,
\]

with Loewy layers

\[
\boxed{1,2,4,2,1}.
\]

Thus \(J^2M/J^3M\) is a canonical four-dimensional local layer.

However, the parallel Pass 808 correction proves that the saturated cyclotomic flat-block gluing at \(q=3\) is

\[
\boxed{(\mathbf Z/2)^2},
\]

with three-primary rank zero. The earlier \(\mathbf F_3^4\) flat-block interface came from unsaturated image lattices and a faulty Smith computation. Therefore the requested map from the rank-ten three-primary interface to a cyclotomic rank-four target has **no target to map to**.

The four-dimensional Heisenberg middle layer remains real, but it is an independent W33 local invariant rather than flat-block gluing.

## Pass 823 — the fixed-scalar deformation tower lifts uniquely over every 2-power

The 81-dimensional homology action is already integral. Two generators with entries in \(\{-1,0,1\}\) satisfy orders three and nine, and all seven relation words used in Pass 681 evaluate exactly to the identity over \(\mathbf Z\).

Hence the same matrices define compatible representations over

\[
\mathbf Z/4,\quad \mathbf Z/8,\quad \mathbf Z/16,
\]

and every higher \(2\)-power quotient.

Pass 681 gives

\[
H^1(G,\operatorname{End}V)=0,
\]

and Pass 801 gives

\[
H^2(G,\mathfrak{sl}V)=0.
\]

At every square-zero step, existence is supplied by the exact integral matrices, the realized obstruction cocycle is zero, and uniqueness follows from vanishing \(H^1\). Thus the fixed-scalar compatible lift tower is unique up to strict equivalence.

The surviving scalar \(H^2\) line remains an ambient Schur-multiplier class. The release does not claim that this abstract class vanishes under every Bockstein; it proves that it is not the obstruction class of the realized W33 representation tower.

## Pass 824 — minimax audit-stream allocation

Four audit streams are treated as a finite experiment-design problem against five explicit failure families. The linear program

\[
\max_a\min_j\sum_i a_iD_{ji}
\]

under \(a_i\ge0\) and \(\sum_i a_i=1\) gives

\[
\boxed{a=(0.3046224,\ 0.3348582,\ 0.1820595,\ 0.1784598)}.
\]

The allocation raises the worst-case information from

\[
0.0135246
\]

to

\[
\boxed{0.0163225\text{ nats/photon}},
\]

a \(20.69\%\) gain.

An equal-weight mixture likelihood-ratio e-process retains the anytime guarantee

\[
\Pr_0\!\left(\sup_t E_t\ge1000\right)\le10^{-3}.
\]

Across 100 deterministic replays per failure family, the optimized allocation reduces worst mean alarm delay from \(606.62\) to \(538.03\) photons. All alternatives are detected within the 8,000-photon budget; 500 matched-null replays produce no alarms.

## Pass 825 — exact facet-pruned continuous runtime

The exact continuous min-plus controller from Pass 805 initially contains 5,795 nodes. For every min/max node with affine children, Pass 825 solves exact polyhedral feasibility problems on

\[
(c_1,c_2,o,\kappa)\in[4,7]\times[6,9]\times[0,2]\times[0,2]
\]

to determine whether each affine child attains the envelope anywhere in the real box.

The compiler solves 3,092 LP feasibility problems and removes 2,258 inactive affine pieces. Exact rebuilding reduces the controller to

\[
\boxed{1000\text{ nodes}},
\]

an \(82.74\%\) reduction. Every retained affine piece has a feasible witness, so each affine sibling envelope is facet-minimal on the declared box.

The pruned runtime contains only

\[
\boxed{9}
\]

distinct primitive affine switching hyperplanes and has maximum comparator depth nine. It preserves all 7,776 integer cells, all 22 phases, all 1,308 unique pair cells, and 1,080 exact rational probes.

## Parallel-track integration

Parallel Pass 806 supplies the correct two-branch gluing theorem. Pass 807 retracts the ring-tower deformation over-read. Pass 808 then makes the deeper correction: the saturated odd-q flat-block gluing is pure 2-torsion \( (\mathbf Z/2)^{(q-1)^2/2} \), not a q-primary Burnside interface. Pass 809 generalizes the gluing calculation to multiple eigenbranches, and Pass 810 records the proved-versus-retracted status. Passes 821–825 incorporate all four corrections.

## Verification boundaries

- Pass 821 determines the internal composition series but does not attach external Modular Atlas labels without a standard-generator conjugacy certificate.
- Pass 822 proves that the proposed cyclotomic rank-four target was retracted; its surviving four-dimensional Heisenberg layer is not identified with flat-block gluing.
- Pass 823 proves the unique fixed-scalar lift tower; it does not compute every integral cohomology group or every abstract Bockstein.
- Pass 824 is minimax-optimal for the declared failure family and equal photon costs.
- Pass 825 proves facet minimality for affine sibling envelopes, not global minimality among all nested tropical phase circuits.
