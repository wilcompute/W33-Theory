# Passes 5102–5109 — root expansion, q=4 closure, unified U81 controller, and three outside-box probes

**Status:** EXECUTED 2026-08-14. This packet executes the five queued continuations after Pass5098–5101 plus three independent probes. All promoted statements are finite building/code theory, exact linear algebra, finite-group/module theory, or explicitly solver-certified. The all-q and q=5 distance theorem remains open.

## 5102 — the mean-value attack becomes an all-q low-generator theorem
For two distinct chamber stars at gallery distance `d=1,2,3,4`, the apartment intersection is exactly `q^(4-d)`. Thus every distinct pair meets in at most `q^3` apartments.

For the XOR of `m` distinct chamber stars, let `n_A` be the number of selected stars through apartment `A`. Pointwise,

`1_(n_A odd) >= n_A - 2 C(n_A,2)`.

Summing and applying the pair-intersection bound gives

`wt >= m q^4 - 2 C(m,2) q^3 = q^3 m(q+1-m)`.

Hence for every `1<=m<=q`,

`wt >= q^4`.

The bound is sharp: choosing `m` chambers in one point or line panel gives exactly `q^3 m(q+1-m)`. Therefore any counterexample to the all-q distance theorem must have chamber-generator leader at least `q+1`.

At q=5, the exact fixed-base three-star census has minimum `1125=5^3*3*(6-3)` with 20 representatives. A separate minimum-cut chart propagator gives 8 satisfiable and 8 contradictory seeds; every satisfiable support is one of the eight chamber stars through the fixed apartment. Thus any q=5 counterexample must simultaneously have generator leader at least 6 and contain at least one heavier local K6 cut. This sharply narrows the wall but does not prove `d=625`.

## 5103 — q=4 complete minimum shell and active-chart expansion close
Pass5090 proved that if every active q=4 K5 chart is a minimum `1|4` cut, the word is a chamber star. The only unresolved possibility was a heavier `2|3` cut.

Condition one heavy cut and minimize the global apartment-code weight with all theta constraints. A fixed apartment lies in four chart roles. In each role the induced PGL(2,4) stabilizer of the selected local edge has order 6 and acts transitively on the six heavy cuts crossing that edge, so one representative per role suffices.

All four exact MILPs return

`OPTIMUM = 384`, `MIP gap = 0`.

Every displayed optimum is a two-chamber panel word. Therefore a q=4 word is either a chamber star of weight 256 or, if it contains any heavy chart, has weight at least 384. Consequently the complete minimum shell of `[13600,256,256]_2` is exactly the 425 chamber stars.

The active-chart theorem also closes. A heavy word satisfies `4 wt = sum local weights <= 6 A`; since `wt>=384`, this gives `A>=256`. A no-heavy word is a chamber star and also has `A=256`. Hence

`A(y) >= 256 = 4*4^3`

for every nonzero q=4 codeword. This is the q=4 analogue of Pass5083's exact q=3 theorem.

## 5104 — the sqrt(17) bridge becomes a global integral map with a minimal index obstruction
On the 30-dimensional global theta carrier from Pass5087, each quadratic lane has companion

`C=[[0,16],[1,2]]`, `chi=x^2-2x-16`.

The twisted Hecke lane is

`T6=[[2,8],[2,0]]`.

The integral matrix

`P=[[2,-2],[0,1]]`

satisfies `C P = P T6` and has determinant 2. Solving the integral intertwining equation completely gives

`P(c,d)=[[2d,8c-2d],[c,d]]`,

`det P(c,d) = -2(4c^2-cd-d^2)`.

Thus every nonsingular integral intertwiner has even determinant, and index 2 is minimal. The doubled historical shifted transfer block `2(B2-4I)` also admits an index-2 integral map into the same theta companion.

Tensoring over the 15 Levi line-kernel lanes gives an explicit global lattice map of index

`2^15 = 32768`

into the exact rank-30 apartment theta carrier. This upgrades the factor-17 spectral coincidence to an explicit global integral intertwiner while proving that no unimodular identification exists in these natural lattices.

Boundary: the theta side has explicit W33 apartment geometry; the historical transfer block is still only operator/lattice data. No historical-object-to-apartment geometric bijection is claimed.

## 5105 — the U81 root controller literally unifies the BT865 state/program torsors
Align the standard type-C2 maximal unipotent subgroup with the chamber used by BT865. Inside the resulting `U81`:

- `H_state=<X0,X2>` has order 27, center 3, is normal in the point stabilizer, and acts regularly on the 27 noncollinear points. It is exactly the BT865 extraspecial `H27` state torsor.
- `H_program=<X1,X2,X3>` has order 27, center 27, is normal in the line stabilizer, and acts regularly on the 27 disjoint lines. It is exactly the BT865 flat `F3^3` program torsor.

They satisfy

`H_state intersection H_program = U'`, `|U'|=9`,

`<H_state,H_program>=U81`,

and `Z(U81)=Z(H_state)=C3`.

The canonical diagonal `V4` complement normalizes both order-27 subgroups, so the full local derivative controller is `U81 semidirect V4` of order 324.

On the protected W33 homology, the Steinberg character restricts to `{81:1,0:80}` on U, hence over C it is the regular character. Over the native field F3 an explicit cycle seed has 81 U-translates contributing rank 81 modulo the 120-dimensional boundary space. Therefore

`H1(F3)|U ~= F3[U]`

is free rank one. Restricting that one regular module to either index-3 subgroup gives exactly BT865's previous

`3 Reg(H27)` and `3 Reg(F3^3)`.

This is an explicit controller/compiler weld, not a dimension match. It remains finite algebra, not optical hardware performance.

## 5106 — A2/C2/G2 rank-two derivative-curvature calculus
For a rank-two positive-root system, the first derivative law counts positive-root subgroup cosets. In good characteristic:

- A2: `N=3`, first derivative `3q^2`, pair-closure polynomial `2 z^2 + z^3`;
- C2: `N=4`, first derivative `4q^3`, pair-closure polynomial `4 z^2 + z^3 + z^4`;
- G2: `N=6`, first derivative `6q^5`, pair-closure polynomial `10 z^2 + 3 z^3 + z^5 + z^6`.

Thus the C2 phenomenon is one member of a rank-two family: first derivative counts root directions, while pair-generated closure records noncommutative curvature.

For G2 the positive-root Chevalley structure-constant magnitudes are `1,1,2,3,3` on the five nonzero positive brackets. Reducing only the Lie-bracket data gives bad-prime shadows

- p=2: `11 z^2 + 4 z^3`;
- p=3: `12 z^2 + 2 z^3 + z^4`.

These bad-prime rows are intentionally firewalled: full bad-characteristic Chevalley group commutator formulas can retain higher divided terms even when a Lie coefficient vanishes. The good-characteristic group closure statement is the theorem.

## 5107 — BONKERS 1: the derivative foliation has a Z/3 Smith defect
Let H be the 81x108 incidence matrix of q=3 U81 elements versus the 108 cosets of its four positive-root subgroups. Exact Smith reduction gives

`SNF(H)=1^68, 3^1, 0^12`.

Therefore

`coker(H) ~= Z^12 + Z/3`.

The ranks are `rank_Q=69`, `rank_F2=69`, `rank_F3=68`. The column kernel has rank 39 over Q and 40 over F3. Also

`H H^T = 4 I + A_derivative`,

so the 12 rational row-defect directions are precisely the `-4` adjacency eigenspace. The q=2 control has Smith form `1^15,0` and no torsion.

This is a genuine ternary arithmetic residue of the root-coset foliation, but no physical charge interpretation is asserted.

## 5108 — BONKERS 2: the protected memory remembers C2 root heights
Since Pass5105 identifies protected H1(F3) with the regular group algebra F3[U81], compute powers of its augmentation ideal J. The exact dimensions are

`81,80,78,74,69,62,54,45,36,27,19,12,7,3,1,0`,

with successive layers

`1,2,4,5,7,8,9,9,9,8,7,5,4,2,1`.

The Hilbert series factors exactly as

`(1+t+t^2)^2 (1+t^2+t^4) (1+t^3+t^6)`,

which is the product attached to C2 positive-root heights `1,1,2,3` at p=3.

The two BT865 restrictions recover distinct sub-filtrations:

- H27 state shell: `(1+t+t^2)^2(1+t^2+t^4)` with Heisenberg heights `1,1,2`;
- flat F3^3 program shell: `(1+t+t^2)^3`.

Thus the one U81 regular memory refines both old 27-coordinate systems and encodes the noncommutative C2 root-height hierarchy as nilpotent memory depth. This is algebraic Loewy/Jennings depth, not timing or decoherence.

## 5109 — BONKERS 3: the 12-dimensional curvature defect splits 4+4+2+2
The free rational defect from Pass5107 is `ker(H^T)` of dimension 12. The canonical diagonal V4 normalizer fixes each of the four positive-root parallel classes setwise. Its character traces on the defect are

`chi(e)=12`, `chi(a)=0`, `chi(b)=-4`, `chi(c)=0`.

Therefore the four rational one-dimensional V4 characters occur with multiplicities

`2,4,2,4`,

or sorted sector dimensions

`4+4+2+2=12`.

So the Smith-free curvature defect has a nontrivial symmetry decomposition rather than being a featureless 12-space. No particle-family identification is inferred.

## External research cross-checks
The global expansion strategy is now naturally comparable with recent finite-Heisenberg Loomis–Whitney work, which controls finite sets by noncommutative projection sizes; that literature is a route suggestion, not a proof of our four-foliation inequality. Recent work on dimension-independent cosystolic expansion of spherical buildings provides a second local-to-global comparison point. For G2, published Chevalley structure-constant/commutator tables independently corroborate the root-string arithmetic used in Pass5106. None of those external papers is used as a substitute for the exact repo certificates above.

## Remaining wall
The all-q minimum-distance theorem is now proved at q=2,3,4 and open from q=5 onward. The q=5 search space is much narrower: any counterexample must have generator leader at least six and contain a heavy local K6 cut. A general root-coset/noncommutative projection inequality strong enough to rule those out is the primary remaining theorem target.
