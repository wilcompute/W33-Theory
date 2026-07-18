# Pass 440 — Galois-ring conductor tower

## Result

Let `R` be an odd unramified finite chain ring of length `n`, residue field
`F_q`, and cardinality `q^n`. For the flat-section Heisenberg graph on `H(R)`,
the exact conductor `j=1,...,n` of a nontrivial central character is the
complete spectral depth variable.

Write

\[
c_j=q^j-q^{j-1},\qquad t_j=q^j.
\]

The conductor-`j` stratum contributes

\[
\lambda_j^+=q^{2n-j}-1,\qquad m_j^+=c_jt_j(t_j+1)/2,
\]

and

\[
\lambda_j^-=-q^{2n-j}-1,\qquad m_j^-=c_jt_j(t_j-1)/2.
\]

All inactive radical twists contribute eigenvalue `-1`. Together with the
trivial eigenvalue `q^(2n)-1`, these multiplicities sum to `q^(3n)`.

For every prime `ell` different from the characteristic, the critical group is
obtained conductor by conductor by adjoining

\[
(\mathbb Z/\ell^{\nu_\ell(q^j-1)})^{c_jq^j}
\]

and

\[
(\mathbb Z/\ell^{\nu_\ell(q^{2j}-1)})^{c_jq^j(q^j-1)/2},
\]

then merging equal exponents. The first factor is the residual rank and the
second is the paired Smith block.

## Separation achieved

- Residue degree appears only through `q=p^f`.
- Nilpotent depth appears through conductor `j`.
- Length one recovers the finite-field theorem.
- Length two recovers the `GF(p^2)` versus `Z/p^2Z` atlas.
- Length three creates a third spectral and Smith stratum.

The executable census covers `(q,n)=(3,1),(3,2),(3,3),(5,2),(7,2),(9,2),(25,2)`.
Every multiplicity, conductor count, and prime-to-characteristic Matrix–Tree
valuation passes.

## Boundary

The theorem closes every prime-to-characteristic component. The
characteristic-primary layers still require a separate modular-incidence
calculation, as in Pass 425 for the field tower.
