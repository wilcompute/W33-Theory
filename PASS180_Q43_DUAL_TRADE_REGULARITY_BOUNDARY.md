# Pass 180 — (Q(4,3)) Dual-Trade Regularity Boundary

Pass 180 has one genuinely new geometric observation and two important
boundaries.

Let (N) be the line-by-point incidence matrix of (W(3,3)).  The dual
quadrangle has the original lines as its points and incidence matrix
(N^{\mathsf T}).  Therefore

\[
L_{\rm route}=\ker_{\mathbf Z}N^{\mathsf T}
\]

is, by definition, the integral point-trade lattice of the dual
quadrangle (Q(4,3)).

An exact scan of every noncollinear pair gives

\[
\operatorname{span}_{W(3,3)}(x,y)=4,
\qquad
\operatorname{span}_{Q(4,3)}(x,y)=2.
\]

This is the classical regular/antiregular distinction.  It is consistent
with the sharply different trade shells—90 norm-eight vectors on the
address side and 432 norm-ten vectors on the route side—but the span
census alone does not derive those lattice minima.  Their completeness
remains the stronger PARI-backed theorem of Pass 173.

## Two corrections

First, (W(3,3)) and (Q(4,3)) form a nonisomorphic dual pair.  Odd-order
(W(3,q)) is not incidence-self-dual; equal point/line counts and equal
strongly regular parameters do not change this.

Second, one Smith-coordinate generator of the route discriminant’s
(\mathbf Z/8) block has

\[
q(h)=11/8.
\]

This is an existence statement, not a canonical law.  Pass 174 proves
that the outer-fixed order-eight generators split equally between
(q=11/8) and (q=3/8).  Hence (11/8) exists on both address and route
sides, but it is not invariant under changing the generator and cannot
be promoted to an invariant of the dual pair.

## Reproducibility

- Witness: `analysis/w33_pass180_dual_trade_lattice_q43.py`
- Certificate: `data/w33_pass180_dual_trade_lattice_q43.json`
- Focused test: `tests/test_pass180_dual_trade_lattice_q43.py`

The determinant, Smith form, code enumerator, and minimum-shell
regression repeat Pass 173.  The new content is the dual-geometry naming
and the exact (4)-versus-(2) span census.
