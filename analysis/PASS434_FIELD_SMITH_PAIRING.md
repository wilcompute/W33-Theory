# Pass 434 — Field-sensitive 2-adic Smith pairing

## Result

Pass 433 left one explicit v1.2 gate open: compute the native Heisenberg-bulk Laplacian at \(q=7\) and decide whether the observed 2-primary shape was a two-point coincidence.

That gate now closes exactly:

\[
K_{7,(2)}\cong (\mathbb Z/2)^{42}\oplus(\mathbb Z/16)^{126}.
\]

The certificate also computes two independent extensions:

\[
K_{9,(2)}\cong (\mathbb Z/8)^{72}\oplus(\mathbb Z/16)^{288}
\]

for the proper \(GF(9)\) Heisenberg construction, and

\[
K_{11,(2)}\cong (\mathbb Z/2)^{110}\oplus(\mathbb Z/8)^{550}.
\]

Together with the already certified \(q=3,5\) cases, the exact field list is now

\[
q\in\{3,5,7,9,11\}.
\]

## Spectral-to-Smith pairing law

For the native bulk graph, the adjacency spectrum has multiplicities

\[
(q^2-1)^1,
\qquad
(q-1)^{\,q(q^2-1)/2},
\qquad
(-(q+1))^{\,q(q-1)^2/2},
\qquad
(-1)^{\,q^2-1}.
\]

Write

\[
a=\nu_2(q-1),\qquad c=\nu_2(q+1).
\]

In every certified finite-field case, the 2-primary Smith factors are

\[
\boxed{
K_{q,(2)}\cong
(\mathbb Z/2^a)^{q(q-1)}
\oplus
(\mathbb Z/2^{a+c})^{q(q-1)^2/2}
}
\]

or equivalently

\[
(\mathbb Z/2^{\nu_2(q-1)})^{q(q-1)}
\oplus
(\mathbb Z/2^{\nu_2(q^2-1)})^{q(q-1)^2/2}.
\]

The multiplicities have an exact spectral interpretation. If

\[
m_+=\frac{q(q^2-1)}2,
\qquad
m_-=\frac{q(q-1)^2}2,
\]

then

\[
m_+-m_-=q(q-1).
\]

Thus the negative spectral sector supplies exactly the number of glued Smith directions. Each such direction combines one \(\nu_2(q-1)\) layer with one \(\nu_2(q+1)\) layer to produce \(\nu_2(q^2-1)\); the residual positive sector carries the unglued \(\nu_2(q-1)\) factors.

The valuation sum agrees identically with the Matrix–Tree spectrum:

\[
\nu_2(\tau_q)
=
\frac{q(q^2-1)}2\nu_2(q-1)
+
\frac{q(q-1)^2}2\nu_2(q+1).
\]

## Field-versus-ring falsifier

The strongest boundary test is at order nine.

Using the actual field

\[
GF(9)=GF(3)[\alpha]/(\alpha^2+1)
\]

gives the predicted shape

\[
(\mathbb Z/8)^{72}\oplus(\mathbb Z/16)^{288}.
\]

Replacing the field arithmetic by the superficially similar ring arithmetic of \(\mathbb Z/9\mathbb Z\) gives instead

\[
\boxed{
(\mathbb Z/2)^6
\oplus
(\mathbb Z/8)^{60}
\oplus
(\mathbb Z/16)^{216}
}.
\]

So the Smith law is not a numerological consequence of the integer \(q=9\). It detects the finite-field Heisenberg geometry.

## Exact status

Proved by deterministic unit-pivot elimination for \(GF(3),GF(5),GF(7),GF(9),GF(11)\). The general odd-prime-power formula remains a conjecture; this pass upgrades it from a two-point guess to a five-field certificate with a ring falsifier.

## Reproduction

```bash
python analysis/w33_pass434_field_smith_pairing.py --extended
pytest -q tests/test_w33_pass434_field_smith_pairing.py
```
