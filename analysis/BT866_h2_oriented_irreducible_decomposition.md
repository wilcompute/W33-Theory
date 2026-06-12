# BT866 - The Oriented Timetable Spectrum

**Status: PROVEN** by GAP-backed verifier
<code>analysis/bt866_h2_oriented_irreducible_decomposition.py</code>, with
evidence in <code>data/bt866_h2_oriented_irreducible_decomposition.json</code>.

BT862 proved that the top homology of the W33 triangle complex is not the
plain permutation module on 40 lines. A symmetry fixing a line acts on its
tetrahedron-boundary 2-cycle by the parity of the induced permutation of the
line's four points. BT866 identifies the resulting three irreducible
constituents exactly.

## Induction from the line parabolic

Let \(G=PSp(4,3)=U4(2)\), and let \(P=3^3:S4\) be the index-40 line
parabolic. It has exactly two linear characters: the trivial character and
the sign character inherited from its \(S4\) quotient. GAP computes

\[
\operatorname{Ind}_P^G(1)=1+15+24,
\qquad
\operatorname{Ind}_P^G(\operatorname{sign}_{S4})
  =5_{\omega}+5_{\omega^2}+30.
\]

The first line is the ordinary unoriented line module. The second is exactly
\(H_2\), the oriented timetable carrier. Both induced characters have degree
40 and character norm 3.

| carrier | irreducible spectrum |
| --- | --- |
| unoriented lines | \(1+15+24\) |
| oriented line boundaries \(H_2\) | \(5_{\omega}+5_{\omega^2}+30\) |

## Eisenstein chirality and the outer Weyl lift

The two 5-dimensional constituents are complex conjugates with character
field \(CF(3)=\mathbb Q(\zeta_3)\). The 30-dimensional constituent is
rational. The outer extension \(U4(2).2=W(E_6)\) acts in the precise way
required by a chirality merger:

- \(5_{\omega}+5_{\omega^2}\) is the restriction of one irreducible
  10-dimensional \(W(E_6)\) representation;
- the rational 30-dimensional constituent has **two** inequivalent
  extensions to \(W(E_6)\).

Thus the oriented timetable carrier has a canonical projective decomposition
\[
H_2=5_{\omega}+5_{\omega^2}+30
\]
and a full-Weyl reading
\[
H_2\longrightarrow 10_{\mathrm{chiral}}
  +30^{\mathrm{outer\ parity}}.
\]

The pair of 30-dimensional extensions is a real \(C_2\) choice: projective
geometry determines the 30-sector, while the outer lift must choose its
parity.

## Completed homology spectrum

Combining BT861, BT862, BT865, and BT866 gives
\[
H_0=1,\qquad H_1=\mathrm{St}_{81},\qquad
H_2=5_{\omega}+5_{\omega^2}+30.
\]
The Euler dimension is
\[
1-81+(5+5+30)=-40,
\]
so the substrate's \(-v\) Euler charge now has an irreducible
representation-theoretic resolution: vacuum minus protected memory plus
oriented timetable channels.

## Architecture reading

BT865 identifies \(H_1\) as the dual state/program compiler. BT866 identifies
what sits above it: \(H_2\) is the orientation header for that compiler.

- the conjugate 5-sectors carry ternary handedness;
- their outer fusion produces a 10-dimensional Weyl-visible chiral channel;
- the rational 30-sector carries the orientation-neutral payload;
- its two outer extensions expose one unresolved parity bit.

This is stronger than saying there are 40 contexts. The topological carrier
stores which timetable is active **and** how its tetrahedral orientation
transforms.

## Boundary

The \(5_{\omega}+5_{\omega^2}\) fusion pattern matches the two BT859 chiral
cache branches, which the outer Weyl involution also fuses, but BT866 does
not yet construct an objectwise intertwiner between those spaces. Likewise,
the two outer extensions of the 30-sector have the right form to host
BT857's local dodecahedral gauge bit, but that identification remains open.
