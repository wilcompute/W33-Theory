# Passes 4697--4704 execution ledger

Canonical five-plus-three packet.  The mathematics was first implemented under filenames 4689--4696; a parallel lane later exposed pre-existing prose labels through 4690, so public/manuscript numbering was moved wholesale to 4697--4704 before release.  The old filenames remain provenance-only implementation aliases.

## Pass 4697 -- three dimension-39 carriers

The Pass4639 cross-shell differential has block form

`D0 = [[0,R],[R^T,0]]`,

so its homology splits canonically as

`Hcross = H27 direct-sum H36`, dimensions `15+24=39`.

The apartment-code coefficient module is `F2^40/<1>` because the 40 generator rows have rank 39 with unique all-ones coefficient relation.

Exact PSp(4,3) equivariance gives:

- `dim Hom(Hcross, Cap)=2`; all three nonzero maps have rank 14;
- `dim Hom(Cap, Hcross)=2`; all three nonzero maps have rank 1.

Therefore the cross-shell/periodic-sum identification is exact, while the equal-dimensional apartment code is inequivalent.

Implementation alias: `analysis/w33_pass4689_three_39d_module_comparison.py` and `data/PART_W33_PASS4689_THREE_39D_MODULE_COMPARISON.json`.

## Pass 4698 -- full affine structure of the corrected Golay sextet stabilizer

Inside the corrected Pass4633 sextet stabilizer `H`:

- `|H|=138240`;
- tetrad-action kernel has order 192 and element-order census `1^1 2^63 3^128`;
- identity plus the 63 involutions form a normal elementary abelian `N=C2^6`;
- N acts regularly on the 64 sextet transversals;
- chosen-transversal stabilizer `K` has order 2160;
- `N intersect K = 1` and `H=N semidirect K`;
- K maps onto S6 on the tetrads, with kernel C3;
- nontrivial C3 fixes no nonzero translation;
- K-orbits on the 63 nonzero translations are 18+45.

This internally recovers the affine structure conventionally written `2^6:3.S6`; the group name is no longer inferred from order alone.

Implementation alias: `analysis/w33_pass4690_full_sextet_affine_group.py` and its frozen JSON.

## Pass 4699 -- explicit A1^24 Niemeier to Leech two-neighbor

Start from the Golay Construction-A lattice

`N=(1/sqrt(2)){x in Z^24 : x mod 2 in G24}`.

For corrected-sextet coordinate 0 define

`v=(3,1^23)/sqrt(2)`, `v^2=16`,

`M={x in N : (x,v) even}`, `L=M+Z(v/2)`.

Exact certificate:

- M has index two in N and v/2 has norm four;
- a frozen 24-vector basis of L at scale `1/(2sqrt(2))` has integer numerator determinant `2^36`;
- the resulting Gram matrix is integral, even, and has determinant one;
- all 48 old coordinate roots have odd pairing with v and are removed;
- every vector in the new coset has odd numerator in all 24 coordinates, giving raw norm at least 3, and evenness raises that to at least 4;
- norm four is explicitly attained;
- therefore L is rootless even unimodular of dimension 24 and minimum norm four, hence the Leech lattice;
- the 24 possible distinguished-coordinate neighbors form one orbit under the corrected sextet stabilizer.

Implementation alias: `analysis/w33_pass4691_explicit_leech_two_neighbor.py` and frozen JSON.

## Pass 4700 -- closed primitive-C8 local mass formulas

Put `u=s-1`.  Three local embedding invariants are required:

- rho: intersecting cross-pairs of the two external-transversal families of an apartment;
- sigma: intersecting external-transversal / single-apartment-hit outside-line pairs;
- tau: outside common transversals of the three leaves of an induced K1,3.

The six exact raw masses are

`A1111|22 = 16*((4u^2+2)rho + u^2 sigma + (4t-2)u^4 + 2(t-1))`,

`A1115 = 64u(u^3-u^2+2u-1)`,

`A1133 = 96u^2(u-1)^2`,

`A1111|4 = 64(u+1)u(u-1)(t-1)`,

`S1111|22 = 48(u+1)u^3`,

`S1113|2 = 48(u+1)u tau`.

The primitive coefficient is raw mass divided by eight.  All Pass4635 anchors are reproduced entry-by-entry.

A decisive same-parameter obstruction closes the old `(s,t)`-only hope:

- W33 has `(s,t)=(3,3)`, `(rho,sigma,tau)=(0,16,1)`, apartment/star `(712,180)`;
- dual W33=Q(4,3) also has `(3,3)` but `(rho,sigma,tau)=(4,0,3)`, with direct primitive-C8 coefficients `(728,252)`.

Therefore embedding data is essential.

Implementation alias: `analysis/w33_pass4692_c8_closed_local_mass_formulas.py` and frozen JSON.

## Pass 4701 -- complete exact support-12 apartment-code census

Let `A_w` count all support-12 coefficient subsets yielding codeword weight w and `B_w` those containing one fixed coefficient position.  Aut(C)=PGSp(4,3) is transitive on the 40 coefficient positions, so double counting `(support,selected-position)` gives

`12 A_w = 40 B_w`, hence `A_w=(10/3)B_w`.

Only

`C(39,11)=1,676,056,044`

fixed-position subsets therefore need exhaustive native XOR/popcount accumulation.  A fresh audit re-ran this mass exactly after a scratch representative was discovered to have been mislabeled; the committed spectrum itself was correct.

Exact support-12 result:

- all `C(40,12)=5,586,853,480` subsets accounted for;
- 151 distinct codeword weights;
- minimum 608 with multiplicity 1620;
- maximum 990 with multiplicity 4320;
- every fixed-position count is divisible by three, as required by the rescaling identity;
- the full 151-entry spectrum is frozen.

The complete labelled frontier is now exact through support 12.  Supports 13--20 remain OPEN; no full enumerator claim is made.

Implementation alias: `analysis/w33_pass4693_support12_transitivity_exact.py` and frozen JSON.

## Pass 4702 -- outside box: direct Golay-affine / cubic-U6 identification is impossible

The faithful six-dimensional F2 translation module N of K admits no nonzero invariant form:

- full invariant quadratic-function system (21 coefficients): nullity 0;
- full arbitrary bilinear-form system (36 coefficients): nullity 0.

Hence this Golay affine six-space is not orthogonal, not self-dual through a bilinear form, and cannot be identified directly with the cubic O^-(6,2) module U6.  This is a representation-theoretic no-go, not a dimension argument.

Implementation alias: `analysis/w33_pass4694_golay_affine_u6_form_nogo.py` and frozen JSON.

## Pass 4703 -- outside box: support-12 minima are exactly apartment corner-star thickenings

For an apartment A, let T(A) be all W33 lines through the four corner points of A.  Each corner has two additional lines beyond the two apartment lines, so

`|T(A)| = 4 + 4*2 = 12`.

Exact computation over all apartments gives:

- 1620 distinct thickenings;
- every thickening has apartment-code weight 608;
- Pass4701 proves the entire support-12 minimum shell has exactly 1620 members, hence all minima are these thickenings;
- the induced line-graph degree census on every thickening is `4^8 6^4`;
- each thickening contains 11 apartments;
- among those 11, exactly one has contained-apartment overlap profile `{0:2,2:8}`; eight have `{0:2,1:4,2:4}` and two have `{0:6,2:4}`.

Thus the original apartment is intrinsically recoverable and the support-12 minimum shell is canonically PGSp-equivariantly bijective with the apartment set.

Implementation alias: `analysis/w33_pass4695_support12_minima_are_apartment_thickenings.py` and frozen JSON.

## Pass 4704 -- outside box: thickening shell spans the even apartment subcode and recovers W33 edges

The 1620 thickening coefficient masks all have even weight 12 and rank 39.  Since the even-weight hyperplane of F2^40 itself has dimension 39, they span it completely.  The all-ones coefficient kernel also has even weight, so their image in the apartment code has dimension

`39-1=38`.

The Pass4495 exhaustive low-weight certificate then gives the exact image subcode

`[1620,38,270]`.

Its 240 minimum words are the sums of adjacent generator pairs, exactly the 240 W33 edges.  Therefore the new chain is

`1620 apartment thickenings -> [1620,38,270] even apartment subcode -> 240 W33 edges`.

Implementation alias: `analysis/w33_pass4696_thickening_span_even_apartment_subcode.py` and frozen JSON.

## Release state

- canonical theorem insert: `analysis/PASS4697_4704_affine_leech_c8_support12_insert.tex`;
- canonical public theorem card and standalone page are registered through the safe public extension manifest;
- `docs/index.html` is not directly overwritten;
- all three canonical manuscript wrappers include the new insert after completed Passes4681--4688;
- `tests/test_w33_pass4697_4704_affine_leech_c8_support12.py` freezes the eight result certificates;
- `.github/workflows/w33_pass4697_4704_affine_leech_c8_support12.yml` has a core exact-regeneration/manuscript job and a separate exhaustive support-12 job;
- aliases 4689--4696 are explicitly marked noncanonical in `analysis/PASS4689_4696_RESERVATION.md`.

Evidence boundary remains fail-closed: no equal-dimensional module identification without an intertwiner; no Leech identification without the explicit rootless even-unimodular basis; no `(s,t)`-only C8 law after the dual-W33 counterexample; and no full apartment enumerator claim before supports 13--20 and the final 2^39 checksum are closed.
