# Passes 4809–4816 — Golay/homology/decoder continuation

## Executive result

The local-to-global qutrit-code architecture from Passes 4801–4808 is now much more rigid.

1. The quotient minimum shell is complete: all 360 projective lift-weight-six classes are induced K3,3 configurations, one PSp(4,3) orbit (stabilizer 72) and one full order-51840 orbit (stabilizer 144).
2. Exact component decoding factors through 27 local 81-state punctured-Golay tables and the 45 global GQ(4,2) point constraints. At weight two every ambiguity is local Golay; at weight three the first genuinely global ambiguity is exactly the K3,3 homology shell.
3. The two Golay extension directions on every K5 globalize to a canonical 54-object orientation cover. PSp preserves two 27-sheets; the full outer action exchanges them.
4. At q=9 the Linear, K1, and Fi/Mondello minimum-shell classes do not split further under PSp(4,9); each is already one PSp orbit. Betten's BLT classification/names/stabilizers remain prior art; the repo result is the outer-quotient/PSp split computation.
5. The 360 K3,3 minima form a rigid multidesign and can be reconstructed from the decoder's exactly-twofold weight-three collision relation alone.

Pass 4812 is deliberately not promoted to a complete theorem here: an exact 30-bit quotient-SAT orbit classifier has been committed, and the previously known deep-hole coset orbit contains 12,960 cosets, with PSp/full stabilizers 2/4. The final all-orbit blocked-SAT UNSAT certificate has not yet been observed in the repository, so completeness remains open at this release boundary.

## Pass 4809 — complete weight-six homology shell

For the quotient

\[
C^\perp/L \cong H_1(\operatorname{Levi}(GQ(4,2));\mathbf F_3),
\]

Pass 4808 had established minimum triangle-lift weight six and produced 360 induced K3,3 witnesses without claiming completeness. Exhaustion of all local cost patterns at total cost six closes that boundary:

- three cost-2 states: 0 survivors;
- two cost-1 plus two cost-2: 0 survivors;
- four cost-1 plus one cost-2: 0 survivors;
- six cost-1 states: exactly 360 projective survivors.

Every survivor has six active line fibers inducing K3,3. The complete shell is transitive under PSp(4,3) and under the full order-51840 action.

## Pass 4810 — exact hierarchical decoder

On a single ten-triangle K5 fiber, the point-syndrome map has exactly 81 states with minimum local costs

\[
1\times0+20\times1+60\times2.
\]

Therefore every ternary component error is syndrome-equivalent, modulo the local punctured Golay kernel, to one using at most two nonzero triangle coordinates per fiber. Exact component ML decoding becomes a finite 27-by-81 state-selection optimization constrained by the 45 GQ point sums modulo three.

Exact global low-weight census:

- weight 2: 145260 errors; syndrome multiplicities 1:140400 and 3:1620. The 4860 ambiguous errors are exactly same-fiber Golay ambiguity.
- weight 3: 25953120 errors; syndrome multiplicities 1:23385600, 2:7200, 3:842400, 12:2160.

The 7200 exactly-twofold weight-three classes are precisely the first genuinely global ambiguity sector: they are the two halves of the 720 nonzero scalar K3,3 weight-six logicals.

Boundary: this is exact ML in Hamming weight for one ternary X- or Z-component. Independent component decoding is not asserted to minimize joint qutrit Pauli support.

## Pass 4811 — global Golay extension chirality

The two projective one-coordinate extension directions of local G10 transform under S5 by the sign character: all 60 even permutations fix both directions separately, and all 60 odd permutations exchange them.

Global transport gives a 54-object two-cover of the 27 fibers:

- PSp(4,3): two orbits of 27;
- full order-51840 action: one orbit of 54.

Either PSp sheet gives a monomially equivariant direct sum of 27 perfect ternary Golay G11 blocks, [297,162,5]_3. Adjoining both directions gives the self-dual direct sum of 27 extended G12 blocks, [324,162,6]_3, invariant under the full outer action.

No identification with E6 27 plus conjugate-27 modules is inferred from cardinality.

## Pass 4812 — exact deep-hole classifier, completeness pending evidence

The committed classifier represents H10 cosets by a 30-bit syndrome under a parity-check basis. A weight-14 deep-hole leader is constrained by wt(x)=14 and d(x,c)>=14 for every c in H10. After one solution is found, its complete PSp orbit of 30-bit coset syndromes is blocked, and the SAT instance is solved again. Iteration to a final UNSAT is an exhaustive orbit classifier.

The already certified witness coset has 64 weight-14 leaders and weight distribution

\[
64z^{14}+128z^{16}+192z^{18}+256z^{20}+192z^{22}+128z^{24}+64z^{26}.
\]

Its PSp orbit contains 12960 distinct deep-hole cosets (stabilizer 2); the full order-51840 orbit is the same 12960 cosets (stabilizer 4). No claim is made here that this is the only deep-hole orbit until the final blocked-SAT UNSAT certificate is frozen.

## Pass 4813 — q=9 classes remain three PSp orbits

Betten's complete q=9 BLT classification gives three PΓO(5,9) classes: Linear, K1, and Fi/Mondello. Evaluating the Frobenius and orthogonal/spinor outer bits of the published stabilizers shows that every class stabilizer surjects onto the full outer C2 x C2 quotient PΓO/PΩ. Hence none splits when restricted to PSp(4,9)=PΩ(5,9).

The PSp orbit/stabilizer data are:

- Linear: orbit 239112, stabilizer 7200;
- K1: orbit 1195560, stabilizer 1440;
- Fi/Mondello: orbit 17216064, stabilizer 100.

Prior-art firewall: BLT representatives, class names, completeness, and PΓO stabilizers are Betten's results. This pass adds the outer-quotient evaluation and PSp orbit conclusion.

## Pass 4814 — bonkers: the 54-set is an orientation cover

The full stabilizer of one base fiber has order 1920 and induces S5 on its five GQ points, with elementary-abelian kernel C2^4 of order 16. Since the Golay direction bit is the sign character of this S5, a direction stabilizer is the preimage of A5, order 960.

Thus the exact cover is

\[
W(E_6)/(2^4{:}A_5)\longrightarrow W(E_6)/(2^4{:}S_5),
\]

of degrees 54 to 27. This specifically rules out treating the 54 objects as an untwisted disjoint union of two W(E6)-invariant 27-sets.

## Pass 4815 — bonkers: K3,3 multidesign/completion geometry

Across the 360 projective K3,3 minima:

- 27 line fibers occur 80 times each;
- 45 GQ points occur 72 times each;
- 270 physical triangle coordinates occur 8 times each;
- adjacent line pairs occur 24 times each;
- nonadjacent line pairs occur 10 times each.

The 27-line graph has exactly 720 independent triples, each forming one side of a unique K3,3. Every one of the 2160 induced K1,3 stars also has a unique K3,3 completion. The 1080 induced P3 triples each lie in six K3,3 blocks.

## Pass 4816 — bonkers: decoder ambiguity reconstructs topology

Each projective K3,3 signed logical has two nonzero scalar multiples and ten unordered 3+3 support partitions. Each partition gives two weight-three errors with the same syndrome, so each projective K3,3 contributes exactly 20 exactly-twofold collision classes:

\[
360\times20=7200.
\]

Pass 4810 independently exhausts the complete weight-three error space and finds exactly 7200 twofold classes. The difference of either colliding pair is the signed weight-six logical, so projectivizing that difference reconstructs the unique K3,3 class. Thus the decoder collision relation alone reconstructs the entire minimum nonlocal homology shell.

## Firewalls

- Local G10 words are logical ambiguity, not correctable syndrome information.
- The decoder theorem is per ternary component, not a joint-Pauli-weight optimality theorem.
- The 54 Golay-direction cover is orientation-twisted; no E6 module identification follows from 27+27 counts.
- q=9 BLT classification data are prior art; only the PSp split evaluation is claimed here.
- Pass 4812 remains incomplete until the final orbit-blocked SAT instance is observed UNSAT.
