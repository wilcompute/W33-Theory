# Pass 452 — length-three Hjelmslev conductor filtration

The affine Hjelmslev plane \(AHG(2,\mathbb Z/27\mathbb Z)\) is constructed explicitly:

\[
729\text{ points},\qquad972\text{ lines},\qquad27\text{ points per line},\qquad36\text{ lines through each point}.
\]

Let \(N_j\) be the block matrix for equality modulo \(3^j\). The incidence Gram matrix satisfies

\[
BB^{\mathsf T}=3^3I+J+(3-1)N_1+(3^2-3)N_2.
\]

Its spectrum is

\[
972^1\oplus243^8\oplus81^{72}\oplus27^{648}.
\]

The three nonconstant levels \(3^5,3^4,3^3\) match conductor depths one, two, and three in the Pass 440 Heisenberg tower.

More generally,

\[
BB^{\mathsf T}=q^nI+J+\sum_{j=1}^{n-1}(q^j-q^{j-1})N_j,
\]

with nonconstant eigenlevel \(q^{2n-j}\) of multiplicity \(q^{2j}-q^{2j-2}\). This identifies additive-character conductor with geometric resolution depth throughout the neighbor tower.
