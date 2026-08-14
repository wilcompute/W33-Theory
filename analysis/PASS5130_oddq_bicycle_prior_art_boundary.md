# Pass5130 — odd-q Levi bicycle prior-art boundary

## External ownership
The cross-characteristic binary rank of the point-line incidence matrix of the symplectic generalized quadrangle W(3,q) for odd prime powers is prior literature, not a repository novelty claim. The relevant primary incidence-module line includes:

- P. Sin and Q. Xiang, *On the dimensions of certain LDPC codes based on q-regular bipartite graphs*, arXiv:cs/0506011.
- D. B. Chandler, P. Sin and Q. Xiang, *The permutation action of finite symplectic groups of odd characteristic on their standard modules*, arXiv:math/0603100.

For the W(3,q) point-line incidence matrix N in odd characteristic, the binary rank formula used in Pass5130 is

`rank_F2 N = 1 + q(q+1)^2/2`.

The repository had already flagged Chandler--Sin--Xiang as relevant symplectic incidence-module prior art in Pass4483; Pass5130 makes the specific connection to the binary Levi bicycle family explicit.

## Repository deduction
Pass5124 supplies the Levi block-matrix mechanism. For odd q, the Levi degree q+1 is even, so over F2 the vertex-edge incidence Gram has off-diagonal point-line incidence blocks. Therefore

`dim Bike_2(Levi) = 2 null_F2(N) - 1`.

Substituting the prior-art rank theorem gives

`null_F2(N)=q(q^2+1)/2`

and hence

`dim Bike_2(Levi)=q^3+q-1`.

This deduction promotes the former q=3,5,7 empirical pattern to an all-odd-prime-power theorem and identifies q=3 with the repository's Bike29 layer. Exact repository anchors at q=3,5,7,11 are 29,129,349,1341.

## Nonclaims
Pass5130 does not claim discovery of the W(3,q) binary incidence rank formula, does not extend the odd-q formula to even q, and does not attach a particle or physical-charge interpretation to the bicycle dimension.
