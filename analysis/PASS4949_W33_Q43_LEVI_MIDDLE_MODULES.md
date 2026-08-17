# Pass 4949 — the two 40-carriers and the outer-sensitive middle complex

## Result

The 40 fibers inherited from the Steiner construction are not the point graph
of \(W(3,3)\).  Native GAP reconstructs them from the underlying
\(Q^-(5,2)\) action and proves that their quotient graph is the
line-intersection graph \(Q(4,3)\).  Its 40 maximal \(K_4\) pencils then
recover the dual point-collinearity graph \(W(3,3)\) object by object.

Both graphs have parameters

\[
  \operatorname{SRG}(40,12,2,4)
\]

and projective/full group orders 25,920 and 51,840.  Those shared coarse
invariants do not identify the graphs.  Their characteristic-three ranks give
an immediate exact separator:

\[
 \operatorname{rank}_{\mathbf F_3}(A_{W}+I)=11,
 \qquad
 \operatorname{rank}_{\mathbf F_3}(A_{Q}+I)=15.
\]

Consequently their augmentation filtrations are different:

\[
 W(3,3): 10\mid19\mid10,
 \qquad
 Q(4,3): 14\mid11\mid14.
\]

This corrects the point/line carrier label inherited by Passes 4870, 4874,
4939, 4941, 4942, and 4945--4947.  It does not invalidate their computations
that depend only on the explicitly constructed Steiner carrier; it changes
which of the two dual 40-object geometries those computations describe.

## The middle-module theorem

The 19-dimensional middle quotient on the actual W33 point augmentation has
submodule dimensions

\[
  0,5,14,19
\]

and splits as \(5\oplus14\).  The distinguished 19-dimensional submodule of
the Pass-4865 Levi pairing radical instead has submodule dimensions

\[
  0,14,19
\]

and is a nonsplit extension \(14\mathbin{\cdot}5\).  Equal dimension therefore
does not imply module isomorphism.

Solving the full intertwining equations nevertheless exposes a sharper bridge.
For \(PSp(4,3)\) there are unique maps up to scalar

\[
 W_{19}\xrightarrow{\ f\ }L_{19}
 \xrightarrow{\ g\ }W_{19},
 \qquad
 \operatorname{rank}f=14,
 \qquad
 \operatorname{rank}g=5,
\]

with

\[
 \ker f=W_5,\quad \operatorname{im}f=L_{14},
 \qquad
 \ker g=L_{14},\quad \operatorname{im}g=W_5,
 \qquad
 fg=gf=0.
\]

Thus the two nonisomorphic middle modules form an exact two-periodic complex.
The outer similitude retains \(f\) without a twist, but kills \(g\); twisting
the W33 target by the outer sign restores the rank-five reverse map.  The
failure of a full-rank identification is therefore structured information,
not a dead end: it detects both extension class and chirality.

## Evidence

- GAP owner: `analysis/w33_pass4949_w33_levi_middle19_intertwiner.g`
- Frozen certificate:
  `data/PART_W33_PASS4949_W33_Q43_LEVI_MIDDLE_MODULES.json`
- Focused regression:
  `tests/test_w33_pass4949_w33_q43_levi_middle_modules.py`
- Native result: `46/46 checks; status=PASS` after the Pass-4959 incidence
  factorization was added to the shared in-memory carrier build

The witness rebuilds the two carriers from a common \(Q^-(5,2)\) generator
system, enumerates both modular submodule lattices, and solves the Hom spaces
over \(\mathbf F_3\).  The regression requires both the exact PASS line and
byte identity with the frozen JSON certificate.

## Boundary

This is an exact finite characteristic-three theorem.  It does not identify
the two 19-spaces, split the Levi extension, equate point and line carriers,
or establish a continuum field, particle, coupling, security property, or
hardware implementation.  It supplies a corrected carrier dictionary and a
literal equivariant complex that later compiler work can use.
