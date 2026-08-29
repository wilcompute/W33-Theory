# The 40x45 carrier is the plane-ovoid / Hermitian PG(3,4) design

The previous packet found forty distinguished nine-point ovoids `O_c` inside
the 45-point `GQ(4,2)` carrier and proved

\[
BB^T=8I+2A_{W33}+J,
\qquad
B^TB=8I+2A_{\overline{GQ(4,2)}}.
\]

It also found all 200 ovoids and the orbit split `40+160`.  This note identifies
that finite geometry in standard language.

## 1. The 40 orbit is the plane-ovoid orbit

The unique `GQ(4,2)` is the Hermitian generalized quadrangle `H(3,4)`, with
45 points on the Hermitian surface in `PG(3,4)`.  Its 200 ovoids are classically
known to split into two automorphism orbits:

- 40 **plane ovoids**, obtained as non-tangent plane sections of `H(3,4)`;
- 160 non-plane ovoids, usually called **tripods**.

The exact repository census `40+160` therefore identifies the distinguished
`O_c` orbit with the plane ovoids.

Equivalently, Hermitian polarity identifies a non-tangent plane with its unique
nonisotropic pole.  There are 40 nonisotropic projective points and 45 isotropic
ones.  Hence

\[
B_{c,m}=1\iff m\in O_c
\]

is precisely the isotropic/nonisotropic Hermitian orthogonality incidence
between the two point types of `PG(3,4)`.

The count

\[
45+40=85=|PG(3,4)|
\]

is structural: in the Veldkamp description of `GQ(4,2)`, the 45 perps and the
40 plane ovoids form the 85 points of a subspace isomorphic to `PG(3,4)`.

## 2. Partial geometric design parameters

Every row of `B` has size 9 and every column has size 8.  The already-certified
spectral identities imply

\[
BB^TB=12J+12B.
\]

Therefore, taking the 40 W33-labelled nonisotropic points as design points and
the 45 carrier labels as blocks, this is a partial geometric (1 1/2-) design
with parameters

\[
\boxed{(v,b,k,r;\alpha,\beta)=(40,45,8,9;12,24)}.
\]

For an antiflag the three-step flag count is 12; for a flag it is 24.

The dual concurrences are equally concrete:

- two orthogonal `GQ(4,2)` carrier points occur together in zero plane ovoids;
- two nonorthogonal carrier points occur together in exactly two;
- two W33 labels have plane-ovoid intersection 3 when adjacent and 1 when
  nonadjacent.

## 3. Full automorphism group

The inner projective unitary/symplectic group

\[
PSU(4,2)\cong PSp(4,3)
\]

of order 25,920 acts on both halves.  The field/outer involution extends this to

\[
\boxed{P\Gamma U(4,2)\cong PSp(4,3){:}2}
\]

of order 51,840.

This is the full automorphism group of the 40x45 incidence structure.  Indeed,
the row intersections recover the W33 graph exactly (3 versus 1), so every
design automorphism injects into `Aut(W33)`, whose order is 51,840; the full
semilinear unitary group already attains that bound.

## 4. Consequence for the W33/GQ bridge

The earlier quotient tower is now coordinatized inside one classical space:

- the 40 W33 labels are the 40 nonisotropic points of `PG(3,4)`;
- the 45 minimum-vector/GQ labels are the 45 isotropic Hermitian points;
- `O_c` is the polar plane section attached to the nonisotropic point `c`;
- the eight-set `C_m={c:m in O_c}` is the nonisotropic neighborhood of the
  isotropic point `m` and induces the previously observed `K4,4` in W33.

So the 40-to-45 correspondence is not a numerical bridge: it is the two-type
point decomposition of the Hermitian `PG(3,4)` geometry.

## Literature cross-check

This agrees with the classical Brouwer-Wilbrink classification of the 200
ovoids of `GQ(4,2)` and with the standard Veldkamp description in which the 45
perps and 40 plane ovoids form a `PG(3,4)` subspace.  The repository derivation
is independent: the orbit sizes, incidence matrix and automorphism bound were
obtained from the W33/minimum-vector construction before this identification.

## Boundary

This is an exact finite-geometric identification.  It does not, by itself,
assign a physical meaning to the two point types.