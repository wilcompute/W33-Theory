# Pass 4754 — odd-q kernel distance and the involution mod-4 branch

Let `A_*` be the line-intersection adjacency matrix of the symplectic generalized quadrangle `W(3,q)` and let

`K_q = ker_{F_2}(A_*)`.

## 1. Universal lower bound

Take a nonzero support `S` of size `w` in `K_q`, choose a line `ell in S`, and let `t` be the number of other members of `S` meeting `ell`.  The parity equation at `ell` gives `t` even.  The line `ell` has `q(q+1)` neighbours, so `q(q+1)-t` lines outside `S` meet `ell`.  Every such outside line already meets one member of `S` (`ell`), hence its even-parity equation forces it to meet at least one further member of `S`.

If `n in S\{ell}` meets `ell`, at most `q-1` outside lines can meet both: they are the remaining lines through their common point.  If `n` is skew to `ell`, exactly `q+1` lines meet both in a generalized quadrangle.  Double counting therefore gives

`q(q+1)-t <= t(q-1)+(w-1-t)(q+1) = (w-1)(q+1)-2t`.

Thus

`(w-1)(q+1) >= q(q+1)+t`,

so `w >= q+1`.  If equality holds then necessarily `t=0`.  Since `ell` was arbitrary, every minimum support is pairwise skew.  Equality in the double count further forces every outside line meeting the support to meet exactly two support lines.

## 2. Odd-q construction from the dual parabolic quadric

For odd `q`, the dual generalized quadrangle is `Q(4,q)`.  Choose a nondegenerate anisotropic 2-space `W` in the underlying 5-dimensional orthogonal vector space and set `U=W^perp`.  Then `U` is a nondegenerate 3-space and the projective plane `P(U)` cuts `Q(4,q)` in a nondegenerate conic `C` of `q+1` points.

For `c in C`, the polar hyperplane `c^perp` meets `P(U)` in the tangent to `C` at `c`, so after deleting `c` itself the point-graph adjacency row meets `C` zero times.  For `p in Q(4,q)\C`, the line `p^perp intersect P(U)` cannot be tangent to `C`: if it were tangent at `c`, then `p` would differ projectively from `c` by a vector in the anisotropic complement `W`, and isotropy of `p` would force a nonzero isotropic vector in `W`, contradiction.  Hence that polar line is secant or external and meets `C` in two or zero points.

Therefore the incidence vector of `C` lies in the binary adjacency kernel.  Under duality it becomes `q+1` pairwise-skew lines of `W(3,q)`.  Together with the lower bound:

**Theorem.** For every odd prime power `q`,

`d(K_q)=q+1`.

Every minimum word is a pairwise-skew `(q+1)`-set satisfying the exact `0/2` transversal parity law.  The argument constructs one such orbit; it does **not** claim that every minimum word is an anisotropic-plane conic without an additional classification proof.

## 3. Why the involution theorem branches mod 4

Let `T=diag(J,J)` with `J=[[0,1],[-1,0]]`.  Projectively `T` is an involution because `T^2=-I`.

* If `-1` is nonsquare (`q = 3 mod 4`), `F_q[T]` is the quadratic field.  The `T`-invariant 2-spaces are the `F_{q^2}`-lines, and the totally isotropic ones form the Hermitian isotropic set of size `q+1`.  Hence the projective involution fixes `q+1` W-lines, so its fixed set is a minimum kernel word.
* If `-1` is square (`q = 1 mod 4`), `T` has two 2-dimensional eigenspaces `V_+` and `V_-`.  Each eigenspace is itself totally isotropic, giving two fixed W-lines.  Every other invariant 2-space is `L_+ direct-sum L_-` with one projective point from each eigenspace; total isotropy chooses the unique `L_-` orthogonal to each `L_+`.  This contributes `q+1` more fixed lines.  The total is therefore `q+3`, two above the kernel minimum `q+1`.

This explains the Pass-4739 data `4,8,8` for `q=3,5,7`: the q=3 involution/minimum-shell coincidence is the first member of the `q = 3 mod 4` branch, while q=5 is not an anomaly.

## Prior-art boundary

Bagchi, Brouwer and Wilbrink, *Notes on binary codes related to the O(5,q) generalized quadrangle for odd q*, Geometriae Dedicata 39 (1991), studied dimensions of binary line and point-neighbourhood codes for `Sp(4,q)` and its dual `O(5,q)`.  Key, Moori and Rodrigues (2005) studied adjacency codes from odd-characteristic symplectic rank-3 actions and obtained general minimum-weight bounds.  This pass records the explicit adjacency-**kernel** counting/conic proof and the mod-4 fixed-line comparison needed by this repository; it does not assert publication novelty without a line-by-line comparison with those papers.
