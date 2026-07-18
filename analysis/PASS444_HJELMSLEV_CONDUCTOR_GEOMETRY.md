# Pass 444 — Hjelmslev conductor geometry

The conductor split now has a concrete incidence-geometric realization.

Let `R` be a length-two finite chain ring with residue field `F_q`. In the
affine Hjelmslev plane `AHG(2,R)`:

- there are `q^4` points and `q^4+q^3` lines;
- the residue map has `q^2` point neighborhoods of size `q^2`;
- it has `q(q+1)` line neighborhoods of size `q^2`;
- every line contains `q^2` points;
- every point lies on `q^2+q` lines;
- distinct neighboring points lie on `q` common lines;
- non-neighboring points lie on one common line.

If `B` is the point-line incidence matrix and `N` is the block matrix of the
point-neighborhood relation, then

\[
BB^T=q^2I+(q-1)N+J.
\]

Therefore

\[
\operatorname{Spec}(BB^T)=
\{(q^4+q^3)^1,(q^3)^{q^2-1},(q^2)^{q^4-q^2}\}.
\]

These are precisely the two nontrivial magnitudes in the length-two Heisenberg
conductor spectrum:

- `q^3`: residue-plane oscillations, conductor-one characters;
- `q^2`: within-neighborhood oscillations, primitive characters.

The witness constructs `AHG(2,Z/9Z)` and `AHG(2,Z/25Z)` explicitly and checks
every point pair, line, neighborhood fibre, and symbolic Gram multiplicity. The
nilpotent conductor is literal geometric resolution depth under the Hjelmslev
neighbor map.
