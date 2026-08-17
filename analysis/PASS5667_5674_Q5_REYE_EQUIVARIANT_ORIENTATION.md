# Passes 5667–5674 — the q=5 design contains Reye intrinsically, and its orientation character opens all of S12

## Executive result

The outstanding action gate is closed on its strongest branch:

\[
G_{q=5}^{(12)}\cong_{S_{12}}T_{12,165}
  \cong_{S_{12}}G_{\mathrm{Reye}}^{(12)}
  \cong_{S_{12}}G_{\mathrm{Latin}}^{(12)}
  \cong_{S_{12}}W(F_4)/Z\curvearrowright\{\text{12 short-root pairs}\}.
\]

This first equality was not an unanticipated new computation. Pass 5606 had already
written the correct fail-closed GAP gate, but its certificate had never been emitted and
its report still said the map was pending. Native GAP now executes that gate and gives the
explicit q=5-cover-to-Latin conjugator

\[
\boxed{[1,9,4,8,12,7,10,2,5,3,6,11]}.
\]

The genuinely new result begins one layer deeper. The 312 vertices outside the selected
13-cover define an exact multidesign \(2\!-\!(13,6,60)\). Its 286 triples have containment
multiplicities

\[
\boxed{0^{16},\quad16^{30},\quad24^{240}}.
\]

The sixteen zero-containment triples avoid the unique fixed cover point and form, on the
moving twelve points, exactly a Reye configuration

\[
\boxed{12_4\,16_3}.
\]

Thus Reye is not merely matched to the q=5 action after both objects are separately
named. It is reconstructed intrinsically from the q=5 design by the predicate
“contained in zero design rows.”

The GAP certificate is
[`PART_W33_PASS5667_5674_Q5_REYE_EQUIVARIANT_ORIENTATION.json`](../data/PART_W33_PASS5667_5674_Q5_REYE_EQUIVARIANT_ORIENTATION.json),
emitted by
[`w33_pass5667_5674_q5_reye_equivariant_orientation.g`](w33_pass5667_5674_q5_reye_equivariant_orientation.g).
It passes 56/56 exact checks.

## Pass 5667 — activating the latent Pass 5606 gate

The exact Pass 5417 graph has 325 vertices. Its selected cover is

\[
\{7,31,74,112,129,141,158,190,194,227,255,278,321\}.
\]

The setwise stabilizer induces orbits \(1+12\) on this cover. The fixed vertex is 7.
On the moving twelve, GAP finds

\[
|G|=576,\qquad \operatorname{TransitiveIdentification}(G)=165,
\]

with point stabilizer \(\operatorname{SmallGroup}(48,48)\cong C_2\times S_4\) and
subdegrees \((1,3,8)\). The explicit conjugator above transports this action to the
independently defined Klein-\(V_4\) Latin action.

The existing Pass 5606 composer then combines this witness with Pass 5596 and emits a
twelve-row object map from the actual q=5 cover vertices to antipodal short-root pairs of
\(F_4\). This changes Pass 5606 from a pending gate to executed evidence; it does not
transfer ownership of the gate to this packet.

This is the exact discipline demanded by Continuity decision `17868609`: the abstract
isomorphism \(G\cong W(F_4)/Z\) did not choose one of the three faithful degree-12
actions. The explicit \(S_{12}\)-conjugator does.

## Pass 5668 — the exact q=5 multidesign and its third-order fingerprint

For every vertex \(x\) outside the cover, let

\[
B_x=\{j\in\{1,\ldots,13\}:c_j\sim x\}.
\]

GAP verifies:

- there are 312 rows \(B_x\);
- every row has size 6;
- every cover point occurs in 144 rows;
- every pair occurs in 60 rows.

So the rows, with multiplicity, form \(2\!-\!(13,6,60)\). The third-order census is
not uniform. Exactly sixteen triples occur in no row, thirty occur in sixteen rows, and
240 occur in twenty-four rows.

On the moving twelve, the group has four triple orbits:

| orbit size | multiset containment | distinct-row containment |
|---:|---:|---:|
| 12 | 16 | 8 |
| 16 | 0 | 0 |
| 48 | 24 | 8 |
| 144 | 24 | 10 |

The zero orbit is therefore both group-theoretically distinguished and design-theoretically
intrinsic.

## Pass 5669 — Reye is the zero shell

The sixteen zero triples are

```text
249  25(12)  26(10)  27(13)
34(13)  35(10)  36(12)  379
458  46(11)  57(11)  678
89(12)  8(10)(13)  9(10)(11)  (11)(12)(13)
```

where the symbols are one-based positions in the 13-cover. Position 1—the fixed
vertex—is absent. Every one of the other twelve positions lies in four triples, and every
triple has three positions. The Levi graph has 28 vertices and 48 edges. GAP computes

\[
|\operatorname{Aut}(\mathrm{Levi})|=576,
\]

with induced actions

\[
\boxed{T_{12,165}\text{ on points},\qquad T_{16,1034}\text{ on lines}}.
\]

The line action has stabilizer \(S_3\times S_3\) and subdegrees \((1,6,9)\); these are the
rook/complement orbitals. The known facts that Reye is a \(12_4,16_3\) configuration and
has 576 automorphisms remain classical—the tomotope paper explicitly identifies its
medial layer with the Reye Levi graph. The new corpus result is the zero-containment
reconstruction inside this exact q=5 multidesign, not the abstract Reye parameters.

External boundary checks:

- Monson, Pellicer, and Williams, [*The Tomotope*](https://bmonson.ext.unb.ca/fields/tom.pdf),
  Proposition 6.1, owns the tomotope-medial-layer/Reye-Levi identification and order 576.
- The [GAP Transitive Groups manual](https://docs.gap-system.org/pkg/transgrp/doc/manual.pdf)
  defines the library identification used here; equal transitive IDs mean equality up to
  relabeling in the full symmetric group.
- The [ATLAS \(W(F_4)\) page](https://brauer.maths.qmul.ac.uk/Atlas/misc/WF4/)
  supplies the Weyl-group presentations and central quotient background.

No literature hit located either the zero-containment characterization or the natural
\(PSL(2,7)\) join theorem below. That is a search boundary, not a claim of global priority.

## Passes 5670–5671 — one group, two carrier-dependent orientation characters

The faithful point and line actions come from the same order-576 source group, but their
sign characters differ:

\[
G^{(12)}\not\le A_{12},\qquad G^{(16)}\le A_{16}.
\]

The point-side sign kernel is

\[
\boxed{|K|=288,\qquad K=\operatorname{SmallGroup}(288,1025)
      \cong 2^4:(C_3\times S_3)}.
\]

The explicit q=5-to-Latin conjugator carries this kernel literally to the even half of
the Latin action. Pass 5300 already owns the stronger identification of that even-Latin
group with the central quotient of the Hoffman cover stabilizer. The new chain is thus

\[
\ker(\operatorname{sgn}_{q=5,12})
 \xrightarrow[\text{explicit conjugator}]{\cong}
L^+
 \xleftarrow[\text{Pass 5300}]{\cong}
H/Z(H).
\]

This is an orientation bridge, not a physical chirality claim. On the sixteen-line
carrier the sign character is trivial, so orientation is genuinely carrier-dependent.

## Pass 5672 — the 7-side does not stop at the divisibility bound

Embed the natural degree-7 action of \(PSL(2,7)\) in \(S_{12}\) by adjoining five fixed
points. There are exactly 23,760 \(S_{12}\)-conjugates of this subgroup. GAP exhaustively
compresses them into relative-placement orbits and tests one representative of every
orbit.

| order-576 action | lies in \(A_{12}\) | relative orbits | every join |
|---|---:|---:|---:|
| \(T_{12,161}\) | yes | 53 | \(A_{12}\) |
| \(T_{12,163}\) | yes | 62 | \(A_{12}\) |
| \(T_{12,165}\) | no | 58 | \(S_{12}\) |

For the Reye class the relative-orbit sizes range over

\[
24,48,72,96,144,192,288,576.
\]

Every one of its 23,760 relative placements generates full \(S_{12}\):

\[
\boxed{\langle T_{12,165},PSL(2,7)^{g}\rangle=S_{12}\quad
       \text{for every natural }7+1^5\text{ placement }g.}
\]

Pass 5662’s number 4032 remains a valid divisibility lower bound for an unspecified
common overgroup. It is not attained in this natural twelve-symbol carrier. Here the
closure is the full group of order \(12!=479{,}001{,}600\). Parity already distinguishes
class 165 from classes 161 and 163; the full transitive identification is needed only to
separate 161 from 163.

The scope matters: this does not classify every representation of \(PSL(2,7)\), nor does
it say every abstract common overgroup is \(S_{12}\). It is exact for the natural
degree-7 action with five fixed symbols.

## Passes 5673–5674 — the heavy dual twelve is the same action through an outer twist

The 312 multidesign rows collapse to 132 distinct six-subsets:

\[
\boxed{312=120\cdot2+12\cdot6}.
\]

The twelve multiplicity-six (“heavy”) rows avoid the fixed cover point. Every moving
point lies in six heavy rows, and pairs of heavy rows intersect in

\[
2^{18},\qquad3^{48}.
\]

The induced action on the heavy twelve is again \(T_{12,165}\). But the moving-point
stabilizer and heavy-row stabilizer, although both
\(\operatorname{SmallGroup}(48,48)\),
are not conjugate inside the source group. Consequently there is no source-equivariant
point-to-heavy-row bijection. Their permutation images become conjugate only after a
non-inner automorphism—an outer twist.

The twist now lifts all the way back to the source group. GAP constructs an automorphism
whose displayed representative has order eight, whose square is inner, and hence whose
class in \(\operatorname{Out}(G)\) has order two. Exactly 48 inner re-gaugings of that
representative are genuine outer involutions. The frozen one exchanges the two
nonconjugate stabilizer classes. Thus “outer-twisted” is no longer only a diagnosis from
stabilizers: there is an explicit order-two source automorphism realizing the duality.

The sign character does **not** realize this carrier involution. Let
\(\pi_P,\pi_H,\pi_L\) be the point, heavy-support, and line permutation characters.
Exact enumeration over all 576 source elements gives

\[
\langle\pi_P,\pi_P\rangle
=\langle\pi_H,\pi_H\rangle
=\langle\pi_L,\pi_L\rangle=3,
\qquad
\langle\pi_P,\pi_H\rangle
=\langle\pi_P,\pi_L\rangle
=\langle\pi_H,\pi_L\rangle=2.
\]

But if \(\varepsilon_P\) is the sign character of the point action, then

\[
\boxed{\langle\varepsilon_P\pi_P,\pi_H\rangle=0,
\qquad
\langle\varepsilon_P\pi_P,\pi_L\rangle=0.}
\]

Thus tensoring the point permutation module by its sign character is disjoint from both
the heavy and line permutation modules. The point-side sign twist is neither the explicit
source outer involution nor the even line carrier; these are three distinct operations.

That is the right self-duality statement:

\[
\text{same transitive action class}\quad\neq\quad
\text{canonical identification of the two carriers}.
\]

## What changed

Before this packet, the repository had three ingredients separated by provenance:

1. the q=5 cover stabilizer had order 576;
2. the Reye twelve was independently identified as \(T_{12,165}\);
3. Pass 5606 had written, but not executed, the exact action-conjugacy gate.

After this packet:

- the gate is executed and its object map exists;
- the q=5 multidesign itself reconstructs the Reye configuration;
- the 12/16 carriers expose different sign characters of the same group;
- the sign kernel lands on the already built Latin/Hoffman bridge;
- the natural seven-side closes not at 4032 but at all of \(S_{12}\);
- the multidesign contains a second twelve-carrier related by an explicit outer
  involution, but still not by a canonical point-to-support labeling;
- the permutation-character firewall separates that outer involution from the point-side
  sign twist and from the line carrier.

This is an exact finite synthesis. It does not supply continuum dynamics, a gauge field,
a particle spectrum, a spacetime model, or a physical theory of everything.
