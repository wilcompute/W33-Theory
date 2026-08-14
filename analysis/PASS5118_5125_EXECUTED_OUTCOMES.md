# Passes 5118–5125 — q=5 distance-scheme barrier, theta isoperimetry, explicit U81 compiler, Jennings memory, and three outside-box probes

**Status:** EXECUTED 2026-08-14. This packet collision-reconciles against the independently landed Pass5110–5117 continuation. All promoted statements are finite code/building theory, exact linear algebra, finite group/module theory, or explicit finite computation. The q=5/all-q minimum-distance theorem remains open.

## 5118 — q=5 counterexample leader barrier rises from 14 to 17
Pass5110 identifies chamber-generator gauge with the Levi cut space, and Pass5111 already excluded cut-minimal leaders through 13. For q=5 the chamber graph is distance-regular with shells `1,10,50,250,625` and adjacency eigenvalues `10,4,-2,4±sqrt(10)`.

For cut-minimal selected chamber sets of sizes 14,15,16, an exact universal subcubic girth-8 search bounds adjacent selected chamber pairs by `20,22,24`. The search works in the larger class of C4/C6-free bipartite graphs of maximum degree three, so the bound is independent of W(3,5) coordinates. Equality is realized by an 8-cycle with 6,7,8 pendant edges.

The 4-class Delsarte positivity inequalities were then enumerated exactly over integer distance distributions. Maximum pair-overlap terms and second-order Bonferroni weight lower bounds are:

- m=14: `(N1,N2,N3,N4)=(20,47,24,0)`, overlap 3795, `wt>=1160`;
- m=15: `(22,53,30,0)`, overlap 4225, `wt>=925`;
- m=16: `(24,59,37,0)`, overlap 4660, `wt>=680`.

Hence every hypothetical q=5 word below 625 must have minimum chamber leader at least **17**. This is a real strengthening, not a q=5 distance proof.

## 5119 — every codeword support is half-regular in the intrinsic theta graph
The theta point graph has degree `8(q-1)`. Every apartment belongs to `4(q-1)` theta triples, no apartment pair belongs to two theta triples, and every codeword has even parity on every theta triple. Therefore if an apartment coordinate is selected, each incident theta triple contains exactly one selected partner and one unselected partner. Thus every support S induces a `4(q-1)`-regular subgraph and every selected vertex has `4(q-1)` external neighbors:

`|delta_theta(S)| = 4(q-1)|S|`.

For q=5 any counterexample support must therefore be 16-regular inside the degree-32 theta graph while satisfying all triangle parities and the leader>=17 cut-gauge condition. This recasts distance as a constrained intrinsic isoperimetry problem. Half-regularity alone is necessary, not sufficient.

## 5120 — explicit polynomial state/root/program compiler inside U81
With the standard C2 positive-root ordering,

`u(a,b,c,d)=x0(a)x1(b)x2(c)x3(d)`.

Two exact matrix factorizations are

`u=[x0(a)x2(c)x3(d)] x1(b)`

and

`u=[x1(b)x2(c+ab)x3(d+2ac+a^2 b)] x0(a)`.

Hence state coordinates may be taken as `(b;a,c,d)` and program coordinates as `(a;b,c+ab,d+2ac+a^2b)`. The symbolic matrix identity is exact over the coefficient ring and all 81 q=3 elements were exhaustively verified. Ordering the regular `delta_u` basis by the H27 state cosets or the F3^3 program cosets therefore gives an explicit permutation transport on the canonical regular controller module from Pass5105. An additional comparison is still required to identify this ordering with BT865's independently seeded chain-level bases.

## 5121 — the q=3 Z/3 Smith defect now has an explicit generator and symmetry character
For the 81x108 root-coset incidence matrix H, `ker_Q(H^T)` has dimension 12 while `ker_F3(H^T)` has dimension 13. An explicit extra modular vector `a` is frozen in the certificate. It satisfies `H^T a ≡0 mod3` but lies outside the mod-3 reduction of the primitive rational kernel.

Set

`w=(H^T a)/3 in Z^108`.

Then `[w]` is nonzero and generates the unique `Z/3` saturation defect. The witness has support 74 and L1 norm 76. U81 acts trivially on this torsion line. The canonical diagonal V4 acts with character

`(e,a,b,c) -> (+,-,+,-)`.

## 5122 — rank-two protected memory is a Jennings root-height filtration
In defining characteristic the Steinberg module is projective of dimension `|U|`, so its restriction to a Sylow/maximal unipotent p-subgroup is one regular module. In the safe prime-field range where the Jennings dimension series agrees with the positive-root height filtration,

`Hilb gr_J(F_p[U]) = product_{alpha>0} (1+t^ht(alpha)+...+t^((p-1)ht(alpha)))`.

Exact sample layer profiles are frozen for A2,p=3 (dimension 27), C2,p=5 (625), and G2,p=7 (117649). The existing C2,p=3 U81 computation is retained as a separately verified small-prime anchor where the same root-height factorization happens to hold. No blanket bad-prime formula is promoted.

## 5123 — BONKERS 1: q=7 kills the naive native-rank drop law
The full q=7 C2 root-coset incidence matrix has shape 2401x1372. Compiled modular elimination gives

`rank_F2=1183`, `rank_F11=1183`, `rank_F7=1173`.

Thus the native drop is exactly 10. The tempting two-anchor law `drop=((q-1)/2)^3` predicted 27 and is false. Exact odd-prime drops are now q3:1, q5:8, q7:10. No replacement all-q formula is asserted.

## 5124 — BONKERS 2: a binary bicycle family appears at q=3,5,7
Exact point-line incidence ranks over F2 are

- q=3: 25 of 40, nullity 15;
- q=5: 91 of 156, nullity 65;
- q=7: 225 of 400, nullity 175.

For odd q, the even Levi degree makes `BB^T mod2=[[0,N],[N^T,0]]`, hence `dim Bike = 2 null_F2(N)-1`. The exact bicycle dimensions are therefore

`29,129,349`,

which match `q^3+q-1` at all three odd anchors. q=3 recovers the old Bike29 layer. The all-odd-q formula remains a conjecture pending a cross-characteristic 2-rank proof.

## 5125 — BONKERS 3: the arithmetic torsion defect is the triality-center module
Pass5109 showed that `Z(U81)=Z(H27)=C3` transforms under the same V4 by `(+,-,+,-)`: two involutions fix the center and two invert it. U81 acts trivially by conjugation on its center. Pass5121 gives exactly the same U81 and V4 actions on `Tor coker(H^T) ~= Z/3`.

Therefore

`Tor coker(H^T) ~= Z(U81)`

as `F3[U81 semidirect V4]`-modules. Sending the nonzero torsion generator to either nonzero central generator gives the two scalar-related equivariant isomorphisms. This is a genuine module identification, not a count equality. No physical charge or particle interpretation is attached.

## Evidence boundary
The q=5 wall is now leader>=17 but the distance 625 theorem remains open. The theta half-regular theorem is necessary support structure, not a converse. The state/program transform is exact on the canonical regular U81 model but is not yet the old BT865 seed-to-seed chain map. The q7 native-rank computation falsifies rather than establishes an all-q pattern. The odd-q bicycle formula has three exact anchors and remains conjectural.
