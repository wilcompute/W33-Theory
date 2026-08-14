# Passes 5142–5149 — theta isoperimetry, modular root-coset arithmetic, and Lie-memory depth

**Status:** EXECUTED on collision-clean branch after Pass5126–5133. Pass5134–5141 was already reserved by another live continuation, so this packet deliberately avoids its q=5 leader-18/heavy-shell, decoder-six, theta-spectrum, and compiler-filtration scope.

## Pass5142 — all-q theta half-regular support theorem
Let `Theta_q` be the intrinsic theta point graph on apartment variables. Every apartment lies in `4(q-1)` theta checks, and each theta check is a triple. For any binary apartment-code support `S`, even theta parity implies that each selected apartment has exactly one selected and one unselected partner in every incident theta check. Therefore `Theta_q` has ambient degree `8(q-1)` while the induced support has

`deg_in = deg_out = 4(q-1)`.

Hence `e(S)=2(q-1)|S|` and the edge boundary has size `4(q-1)|S|`. The distance problem is now intrinsically a minimum-size theta-even half-regular support problem. Half-regularity is necessary, not asserted sufficient by itself.

## Pass5143 — second-moment curvature theorem
Write `k=4(q-1)` and `A` for theta adjacency. For a codeword indicator `x=1_S`, selected vertices have exactly `k` selected neighbors. An unselected vertex sees selected neighbors in pairs, so its selected-neighbor count `t` is even. Therefore

`x^T A^2 x >= k(k+2)|S|`.

The exact defect is

`Delta = x^T A^2 x-k(k+2)|S| = sum_out t(t-2) in 8 Z_{>=0}`.

A chamber star reaches equality at q=2,3,4,5; every exterior boundary apartment then sees exactly two selected neighbors. At q=2 the complete `[90,16,16]_2` code was exhaustively enumerated: all `65535` nonzero codewords were checked, exactly `45` have `Delta=0`, every one has weight 16, and the smallest positive defect is 64. Thus the curvature equality shell exactly reconstructs the 45 chamber stars at q=2.

## Pass5144 — q=7 kills the native-rank cube guess
The q=7 C2 root-coset incidence matrix has shape `2401 x 1372`, row weight 4, column weight 7. Exact ranks are

- F2: 1183
- F3: 1183
- F5: 1183
- F7: 1173
- F11: 1183.

So the native-characteristic rank drop is `10`. The prior q=3,5 drops `1,8` happened to match `((q-1)/2)^3`; at q=7 that guess predicts 27 and is decisively false. No replacement all-q interpolation is asserted.

## Pass5145 — exact q=4 root-coset Smith form
For the 256-by-256 q=4 root-coset incidence matrix, the exact nonzero Smith factors are

`1^180 + 2^4`.

Thus the rational rank is 184, the F2 rank is 180, and

`coker(M_4) ~= Z^72 direct_sum (Z/2)^4`.

The entire characteristic-two rank loss is therefore accounted for by four genuine integral 2-torsion directions. This complements q=3, where the corresponding exact torsion is one `Z/3` factor.

## Pass5146 — rank-two root-height Jennings theorem
In the safe split range `p>h` (Coxeter number), the maximal-unipotent lower-central/Jennings filtration is the positive-root height filtration. Hence

`H_U(t)=product_{alpha>0} (1+t^{ht alpha}+...+t^{(p-1)ht alpha})`.

The rank-two root-height multisets are

- A2: `[1,1,2]`
- C2: `[1,1,2,3]`
- G2: `[1,1,2,3,4,5]`.

Exact safe-range profiles are frozen for A2 at p=5, C2 at p=5, and G2 at p=7. The previously computed C2,p=3 profile is retained only as an independently verified small-characteristic anchor, not folded into the symbolic proof range.

## Pass5147 — augmentation relation versus hidden native defect
Every root-coset incidence column has exactly q ones. If `q=p^f`, the all-ones left functional therefore becomes a native relation because `q=0` in characteristic p. But total native rank drops are

`q=2,3,4,5,7 : 0,1,4,8,10`.

One explicit augmentation relation can account for at most one lost rank dimension. Therefore from q=4 onward there must be additional modular defect dimensions beyond that single displayed mechanism: at least 3, 7, and 9 at q=4,5,7 respectively. Their composition factors remain open.

## Pass5148 — positive-root volume/depth two-statistic calculus
Two different statistics of the same positive-root poset govern two different project structures:

- `N=|Phi+|` controls maximal-unipotent volume `q^N` and first root-coset derivative `N q^(N-1)`;
- `H=sum ht(alpha)` controls top Jennings degree `(p-1)H` in the safe range.

For A2, C2, G2 the pairs `(N,H)` are

`(3,4), (4,7), (6,16)`.

Thus the user's C2 derivative observation is the `N=4` statistic, `q^4 -> 4q^3`, while the memory filtration is governed independently by `H=7`. They are related through the root system without being the same invariant.

## Pass5149 — first-order theta expansion is provably blind
Pass5142 implies every nonzero codeword support has ordinary theta conductance exactly

`Phi(S)=1/2`,

regardless of weight. Equivalently, a one-step theta random walk started uniformly on a selected apartment stays in the support with probability 1/2 and exits with probability 1/2. The adjacency indicator Rayleigh quotient is always `D/2` and the normalized-Laplacian indicator Rayleigh quotient is always `1/2`.

Therefore a proof of `d_q=q^4` cannot come from first-order Cheeger conductance of the theta graph alone. The second moment in Pass5143 is the first local statistic in this hierarchy that can distinguish chamber-star geometry.

## Evidence firewall
- q=5/all-q distance remains open unless another packet closes it.
- The q=7 computation falsifies, rather than extends, the old native-rank cubic guess.
- The Jennings theorem here is restricted to `p>h`; small/bad characteristic must be handled separately.
- Root-height/Jennings depth is an algebraic group-ring filtration, not a hardware clock or physical latency claim.
