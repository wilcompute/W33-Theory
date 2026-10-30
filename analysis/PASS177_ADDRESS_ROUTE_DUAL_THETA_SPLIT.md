# Pass 177 — Address–Route Dual Theta Split

Pass 173 found the first MacWilliams obstruction to an incidence duality
between the point/address and line/route sides of (W(3,3)).  Pass 177
lifts that obstruction from binary words to explicit integer-lattice
shells.

Let (N) be the (40\times40) line-by-point incidence matrix and set

\[
C_A=\ker_{\mathbf F_2}N=[40,15,8],\qquad
C_R=\ker_{\mathbf F_2}N^{\mathsf T}=[40,15,10].
\]

Their dual context codes have weight-enumerator openings

\[
\begin{array}{c|ccc}
 & A_4&A_6&A_8\\ \hline
C_A^\perp&40&240&5085\\
C_R^\perp&40&240&3645.
\end{array}
\]

For the two parity constructions

\[
K_A=\{x\in\mathbf Z^{40}:x\bmod2\in C_A^\perp\},\qquad
K_R=\{x\in\mathbf Z^{40}:x\bmod2\in C_R^\perp\},
\]

write the theta exponent as (q^{\lVert x\rVert^2/2}).  Exact
MacWilliams transforms and coordinate theta products give

\[
\begin{aligned}
\Theta_{K_A}
 &=1+720q^2+15{,}360q^3+1{,}350{,}960q^4
   +50{,}016{,}256q^5+1{,}534{,}663{,}360q^6+\cdots,\\
\Theta_{K_R}
 &=1+720q^2+15{,}360q^3+982{,}320q^4
   +57{,}094{,}144q^5+1{,}452{,}088{,}000q^6+\cdots.
\end{aligned}
\]

## The delayed obstruction

The equal (720) coefficients are objectwise, not merely numerical:

\[
720=80+40\cdot2^4.
\]

The (80) vectors are the coordinate doubles (\pm2e_i).  On the
address side, the other (640) are the sign lifts of the 40 incidence
lines.  On the route side, they are the sign lifts of the 40 point stars.
The next shell also agrees objectwise in count:

\[
15{,}360=240\cdot2^6,
\]

from the 240 weight-six words on each side.

The first difference occurs at exponent four.  Both sides share

\[
4\binom{40}{2}=3{,}120
\]

pure coordinate vectors and

\[
40\cdot2^4\cdot36\cdot2=46{,}080
\]

vectors obtained from a weight-four word and one coordinate double.
Only the weight-eight sector differs, so

\[
1{,}350{,}960-982{,}320
=(5085-3645)2^8
=\boxed{368{,}640}.
\]

This locates the failure of odd-order point–line self-duality precisely:
the line/point-star openings and the weight-six sectors are blind to it;
the first detector is the signed weight-eight shell.

## Reproducibility and boundary

- Witness: `analysis/w33_pass177_address_route_dual_theta_split.py`
- Certificate: `data/w33_pass177_address_route_dual_theta_split.json`
- Test: `tests/test_pass177_address_route_dual_theta_split.py`

The result is an exact code-to-theta identity.  It does not assert that
(K_A) and (K_R) are isometric, that either route construction is an
integral even lattice under the half form, or that the shell counts alone
carry a physical interpretation.
