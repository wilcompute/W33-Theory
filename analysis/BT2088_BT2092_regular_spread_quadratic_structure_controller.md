# Passes 2088–2092 — regular spreads are quadratic structures, and the two phase clocks share one inverter

## Scope and provenance

This packet extends the exact q=3,5,7 regular-spread computations of Pass 2064 and the two-`i` obstruction of Passes 2076–2081.  The field-reduction framework and the general stabilizer of a Desarguesian spread are classical; see G. Van de Voorde, *Desarguesian spreads and field reduction for elements of the semilinear group* (2016), especially Theorem 3.11, and J. A. Thas, *Symplectic spreads in PG(3,q), inversive planes and projective planes* (1997).  The new contribution here is the exact restriction to the fixed symplectic-similitude group used by this repository, its identification with the existing 36-spread certificate, and the common-inverter synthesis of the independently certified `mu4` and `mu6` clocks.

The results below classify the canonical regular/Desarguesian symplectic orbit.  They do **not** classify non-Desarguesian symplectic spreads, and they do not promote the all-q intersection graph formulas beyond the scope already frozen in Pass 2064.

---

## 2088 — a regular symplectic spread carries one projective quadratic structure

Let q be odd, choose a nonsquare `mu` in `F_q`, and write

\[
K=\mathbb F_{q^2}=\mathbb F_q[t]/(t^2-\mu).
\]

Regard

\[
V=K^2
\]

as a four-dimensional vector space over `F_q`.  On `K^2` take the alternating `K`-form

\[
\Omega(x,y)=x_1y_2-x_2y_1.
\]

If `beta(x,y)` denotes the `t`-coefficient of `Omega(x,y)`, then `beta` is a nondegenerate alternating `F_q`-form.  Every one-dimensional `K`-subspace of `K^2` is two-dimensional over `F_q` and is totally isotropic for `beta`.  The `q^2+1` such subspaces therefore form a regular symplectic spread of `PG(3,q)`.

Let

\[
Jx=tx.
\]

Then

\[
J^2=\mu I,
\qquad
\beta(Jx,Jy)=\mu\,\beta(x,y).
\]

Thus `J` is a symplectic similitude with nonsquare multiplier.  Its projective image

\[
\sigma=[J]\in PGSp(4,q)
\]

is an involution.  It fixes every member of the field-reduction spread.  Conversely, the spread is recovered as the set of two-dimensional `F_q`-subspaces invariant under `J`, equivalently the one-dimensional `K`-subspaces of `K^2`.

The elementwise field torus is

\[
K^\times/\mathbb F_q^\times\cong C_{q+1}.
\]

Since q is odd, this cyclic group has a unique involution.  Therefore each regular field-reduction spread carries a **unique projective quadratic-structure involution** `sigma`.

For q congruent to 3 modulo 4 one may choose `mu=-1`, so `J` is literally the geometric `i` of Pass 2076.  For q congruent to 1 modulo 4, `-1` is square and one instead uses another nonsquare `mu`; the projective quadratic structure still exists, but it is not multiplication by `sqrt(-1)`.

The q=3 verifier constructs `F_9^2` explicitly, obtains 40 projective `F_3` points partitioned into ten totally isotropic four-point lines, verifies a rank-four alternating Gram matrix, and checks `J^2=2I` and multiplier 2 on every vector pair.

---

## 2089 — exact all-odd-q orbit size

The stabilizer of the regular symplectic spread inside `PGSp(4,q)` is the projective centralizer of `sigma`.

Indeed, a projective similitude centralizing `sigma` has a lift satisfying

\[
gJg^{-1}=\pm J.
\]

The `+` part is `K`-linear.  The `-` part is obtained by composing with the nontrivial Galois automorphism of `K/F_q`.  Restricting the full Desarguesian-spread stabilizer to symplectic similitudes forces the `K`-determinant into `F_q^\times`.  Projectively this gives

\[
C_{PGSp(4,q)}(\sigma)
\cong
C_2\times P\Sigma L_2(q^2),
\]

where the central `C_2=<sigma>` is the unique involution of the field torus and the second factor is `PSL_2(q^2)` extended by the degree-two field automorphism.  Hence

\[
\left|C_{PGSp(4,q)}(\sigma)\right|
=2q^2(q^4-1).
\]

Since

\[
|PGSp(4,q)|=q^4(q^2-1)(q^4-1),
\]

the orbit has size

\[
\boxed{
\frac{|PGSp(4,q)|}{|C_{PGSp(4,q)}(\sigma)|}
=rac{q^2(q^2-1)}2.
}
\]

This proves the orbit-size part of the regular-spread family for every odd q.  In particular,

\[
q=3:\ 36,
\qquad
q=5:\ 300,
\qquad
q=7:\ 1176,
\qquad
q=11:\ 7260.
\]

The first three values are exactly the complete computational orbit sizes frozen in Pass 2064.  Thus those numbers are not isolated enumerative coincidences: they are the conjugacy-class indices of the projective quadratic structures that generate the regular spreads.

### Boundary

This proves the canonical regular-spread orbit and its size.  It does not by itself prove that the `1` versus `q+1` intersection relation is rank three for every odd q; that stronger association-scheme statement remains under the Pass-2064 computational/conjectural boundary.

---

## 2090 — the q=3 stabilizer is `C2 x S6`

At q=3,

\[
|C_{PGSp(4,3)}(\sigma)|=2\cdot 3^2(3^4-1)=1440.
\]

The existing inner route-clock certificate identifies the order-720 spread stabilizer in `PSp(4,3)` as `S_6`.  The central projective quadratic involution supplies the missing outer factor.  Therefore

\[
\boxed{
C_{PGSp(4,3)}(\sigma)\cong C_2\times S_6.
}
\]

This explains the local structure of the spread graph identified in Pass 2053:

* the full point stabilizer has order 1440;
* its central `C_2` is the quadratic-structure involution;
* quotienting by that silent central involution leaves `S_6`;
* `S_6` is exactly the full automorphism group of the local Kneser graph `K(6,2)` and acts naturally on the Johnson second subconstituent `J(6,3)`.

So the earlier `S_6` route clock and the newer 36-spread `NO_6^-(2)` graph are two views of the same field-reduction stabilizer.  The `S_6` does not arrive from a numerical factorization of 720; it is the visible quotient of the exact `C_2 x S_6` spread stabilizer.

---

## 2091 — one inverter controls both phase clocks

Pass 2076 produced the geometric/representation phase relation

\[
C_4:C_2\cong D_4
\]

with the outer spread involution acting by inversion.  The earlier `mu6` phase packet produced

\[
C_6:C_2\cong D_{12}
\]

with the same inversion law.

Assume the `mu4` and `mu6` clocks are independent except for sharing that one outer inverter.  Their generated controller is then

\[
\Gamma=(C_4\times C_6):C_2,
\]

where the final `C_2` sends `(a,b)` to `(-a,-b)`.  Therefore

\[
\boxed{|\Gamma|=48.}
\]

It contains the two certified phase groups as subgroups:

\[
D_4=\langle C_4,s\rangle,
\qquad
D_{12}=\langle C_6,s\rangle,
\]

with

\[
D_4\cap D_{12}=\langle s\rangle\cong C_2,
\qquad
\langle D_4,D_{12}\rangle=\Gamma.
\]

The verifier enumerates all 48 elements and proves

\[
Z(\Gamma)=(C_4\times C_6)[2]\cong C_2^2,
\]

\[
[\Gamma,\Gamma]=2(C_4\times C_6)\cong C_6,
\]

and

\[
\Gamma_{\mathrm{ab}}\cong C_2^3.
\]

Although `|Gamma|=48`, this is **not** the frame stabilizer `C_2 x S_4`: the latter has center of order 2 and derived subgroup of order 12, whereas `Gamma` has center order 4 and derived subgroup order 6.  The equality of orders is therefore not an identification.

### Boundary

The order-48 synthesis is conditional only on the independence of the two phase clocks apart from their common inverter.  It is a finite controller algebra, not a coupling constant, particle multiplet, or hardware measurement.

---

## 2092 — validation and manuscript status

Canonical verifier:

```bash
python analysis/w33_pass2088_2092_complex_structure_controller.py \
  --write-json data/w33_pass2088_2092_complex_structure_controller.json
pytest -q tests/test_w33_pass2088_2092.py
```

The frozen certificate has status `PASS`.  It checks the literal q=3 field-reduction model, all order/index identities at q=3,5,7,11, the 48-element controller multiplication table, its center and derived subgroup, both dihedral subgroups, their intersection, and the non-isomorphism with `C_2 x S_4`.

The companion TeX insert is shared by `w33_paper.tex` and `photonic_holonet.tex`.  The evidence firewall remains explicit:

1. field reduction and Desarguesian-spread stabilizers retain classical literature ownership;
2. the symplectic restriction and reconciliation with the repository certificates are exact finite mathematics;
3. non-Desarguesian spreads and the all-q rank-three graph remain outside this theorem;
4. no withdrawn physics reading is restored.
