# Passes 4984–4991 — executed outcomes

**Date:** 2026-08-11  
**Status:** EXECUTED locally/exactly; dedicated remote replay will be reported separately.

## Pass 4984 — the residual 810 A4 shell is one chordless W(E6) orbit

The complete dual weight-four shell `A4=10530` is exactly the sigma-even simple four-cycle shell of H36. It splits by chord count as

- 810 chordless cycles;
- 6480 one-chord cycles;
- 3240 two-chord cycles.

The 9720 words reached by `shell3+shell3` are exactly the one- and two-chord classes, with the Pass4976 multiplicities `1^6480 2^3240`. Thus the previously anonymous 810 remainder is exactly the chordless class. The full W(E6) action is transitive on it; its stabilizer has order 64, with order-8 action on the square support and order-8 kernel.

If `U0,U1,U2` are character sums on the three A4 orbits and `V6` is the shell3-pair weight-six sum, then

`T3^2 = 1080 + 2(U1 + 2 U2 + V6)`.

The residual `U0` is precisely invisible to this second convolution. Covering radius remains rigorously `134 <= rho(K) <= 173`.

## Pass 4985 — collision audit: the first “corrected” 4968–4972 packet still contained errors

The collided commit correctly retracted the fabricated srg(33) story, but Pass4985 found and hardened three further errors:

1. A graph automorphism commutes with adjacency, so it cannot interchange the distinct 24- and 15-dimensional eigenspaces. The finite PGSp/PSp sign is not automatically physical CPT.
2. The Ihara roots are `(1 +- i sqrt(10))/11` and `(-2 +- i sqrt(7))/11`, not the previously stated sqrt(43)/sqrt(107) roots. The associated class-number story is withdrawn.
3. The critical-group order `2^81*5^23` survives, but the exact frozen group is `(Z/10)^8 (+) Z/40 (+) (Z/160)^14`; the ad-hoc hypercharge invariant-factor paragraph is withdrawn.

The older Pass4968/4969/4970/4972 files and the srg33 erratum were updated in place so they do not remain live stale sources.

## Pass 4986 — the honest dark carrier is the twin 30-dimensional Levi nullspace

For point-line incidence `Z`, exact spectral projectors give

`P15_point Z = 0`, `Z P15_line = 0`.

The point module is `1+24+15_p`; the line module is `1+24+15_l`. The 80-vertex Levi adjacency has rank 50 and exact nullity 30, equal to `15_p (+) 15_l`.

The W33 point graph and W33 line-intersection/Q43 graph are not isomorphic: their GF(2) adjacency ranks are 16 and 10. Therefore there is no incidence-preserving point↔line side-swap/correlation at q=3. Together with Pass4977's negative PGSp outer twist, this closes the ordinary symmetry-preserving 15↔15 route. The minimal honest symmetric dark carrier is the twin 30-space; an off-diagonal bridge must break symmetry or use a larger nonpermutation carrier.

## Pass 4987 — exact 40+45 decoder

Let `C` be the 36x40 spread-line reader and `M` the 45x36 tritangent selector, and stack measurements as

`R = [C^T; M]`, shape 85x36.

Then

`R^T R = 18 I_36 + 22 J_36`.

Hence the squared singular spectrum is `810^1,18^35`, the 2-norm condition number is `sqrt(45)=3 sqrt(5)`, and

`R^dagger = ((1/18)I-(11/7290)J)R^T`.

For `y_L=C^T x`, `y_T=Mx`, an explicit decoder is

`x=(C y_L+M^T y_T)/18-(11/90)(sum y_L) 1`.

Thirty-six sensors are information-theoretically minimal. Rank bounds force a minimal 36-row reader to have composition only `15 line + 21 tritangent` or `16 line + 20 tritangent`; exact integer bases of both types were found, with determinants `2^7*3^22` and `-2^8*3^21`. Every erasure set of size at most four was exhaustively verified to retain rank; an explicit 12-line erasure kills rank, so the exact first-failure size currently lies in `[5,12]`.

## Pass 4988 — intrinsic structure does not break the 12-fold affine gauge

The local full line stabilizer `S3 wr S3` has order 1296 and is transitive on all 12 AG(2,3) completions. Restricting to the PSp index-two subgroup leaves a local stabilizer of order 648 that is still transitive on all 12; a completion stabilizer has order 54 inside PSp.

Therefore Witting orientation, whose exact finite role is to detect the PGSp/PSp sign, cannot select an affine completion. Canonical tritangent incidence and the canonical S3 connection are likewise equivariant under a transitive local group, so they do not select one without an additional reference/frame. Chern/OAM and time-bin labels may be external calibration data, but no intrinsic equivariant map from those labels to the 12 completions is currently proved.

## Pass 4989 — bonkers: `810 = 270 x 3` octahedral equator bundle

Every residual chordless A4 check is missed by exactly two of the 45 tritangents. These zero-tritangent pairs run through exactly all 270 intersecting tritangent pairs, each with multiplicity three.

For any intersecting pair of tritangents, exactly six double-sixes are unselected by both. Their induced H36 graph is

`K6 - 3K2 = K_{2,2,2}`,

the octahedral graph. Exactly three residual A4 checks lie above that pair: the three equatorial squares of the octahedron. The omitted vertex pairs are its three nonedges, equivalently spread-overlap-4 pairs.

Thus the residual shell is a canonical three-fold bundle

`810 residual A4 = 270 intersecting tritangent pairs x 3 octahedral equators`.

Also `270 = 27 cubic lines x C(5 tritangents through a cubic line,2)`.

## Pass 4990 — bonkers: the centered 85-reader is an equal-bound tight frame

Center line rows by `1/4` and tritangent rows by `2/3`. The exact frame operators are

- line centered reader: `18 P_15`;
- tritangent centered reader: `18 P_20`;
- combined centered reader: `18(I-J/36)=18 P_{1^perp}`.

So after removing the common mean, the 40 line channels and 45 tritangent channels form orthogonal tight frames of the same bound 18 on the complementary 15- and 20-dimensional sectors. Their union, scaled by `1/sqrt(18)`, is a Parseval frame for the entire 35-dimensional mean-zero spread carrier.

## Pass 4991 — bonkers: the 12 affine completions canonically project to the four points of the base line

Among the 66 pairs of local AG(2,3) completions:

- 54 pairs share three added transversal lines;
- 12 pairs share none.

The disjointness graph on the 12 completions is exactly `4 K3`. Therefore the 12-fold ambiguity has four canonical 3-packets. The local stabilizer induces `S4` on these four packets, exactly as it does on the four points of the underlying W33 line. There is exactly one equivariant bijection between the four completion packets and the four line points.

Thus the 12-fold gauge is not featureless: it canonically maps `3-to-1` onto the four points of the base W33 line. Choosing a distinguished point reduces the local affine ambiguity to a residual triple, but the bare geometry itself does not distinguish a point.

## Packet synthesis

The packet produces three linked structures:

1. **Code geometry:** `A4=810+6480+3240`, with the residual 810 now an octahedral tritangent bundle.
2. **Readout geometry:** the raw 85-reader has closed-form inverse and the centered reader is a 15+20 tight-frame decomposition of the 35 mean-zero spread dimensions.
3. **Gauge geometry:** the 12 affine completions survive all tested intrinsic symmetry, but canonically organize as four point-indexed triples.

No claim in this packet lowers the covering-radius upper bound below 173, identifies the finite outer sign with physical CPT, or derives a hardware qutrit labeling without an explicit calibration/reference choice.
