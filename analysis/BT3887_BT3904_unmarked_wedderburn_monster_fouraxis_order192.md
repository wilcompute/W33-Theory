# Passes 3887–3904 — unmarked axial symmetry, explicit rational modules, corrected local algebras, and the order-192 barcode

## Frozen status

```text
PASS_EXACT_FIVE_FRONTS_THREE_CONSTRUCTIONS_MONSTER_WORDS_PENDING_WITH_OVERFLOW_CORRECTION
6ef2f6c4a0fa7e52da9f4abff6d899d0250eeabde1a601d53c40052a841e7039
```

This packet executes the five fronts published after Passes 3837–3854 and adds three independent constructions. It also withdraws and replaces one result from that packet: the former four-axis generated-dimension census was corrupted by signed 64-bit overflow before modular reduction.

The verifier independently rebuilds the six-bit minus quadratic space, the generalized quadrangle \(GQ(4,2)\), the full group \(O^-_6(2)\), all 200 ovoids, the 19 orbital matrices, and the 24-dimensional projected-coordinate algebra. It does not treat prior JSON as a mathematical oracle.

## 3887–3889 — intrinsic axes and the full unmarked automorphism group

Let \(A\) be the point graph of \(GQ(4,2)\), and set

\[
E=\frac{(A-12I)(A-3I)}{90}.
\]

The algebra is \(V=\operatorname{im}E\), with

\[
x\star y=E(x\circ y).
\]

For a rational basis of \(V\), exact multiplication matrices satisfy

\[
\operatorname{tr}(L_xL_y)=\frac7{30}\langle x,y\rangle.
\]

Thus the Euclidean form is recovered intrinsically from multiplication. Every algebra automorphism preserves this form.

The 45 known axes are

\[
a_i=\frac1{21}(A-12I)(A-3I)e_i.
\]

Each is an idempotent of squared norm

\[
\|a_i\|^2=\frac{480}{49}.
\]

The converse is now proved. Let \(y\ne0\) be an idempotent, let \(m=\max_i y_i\), let \(N\) be the sum of squares over the 12 neighbours of a maximizing point, and let \(Q\) be the corresponding sum over the 32 nonneighbours.

Frobenius gives

\[
\|y\|^2=\sum_i y_i^3\le m\|y\|^2,
\]

so \(m\ge1\). The three quadrangle lines through the maximizing point partition its neighbours into three blocks of four, each summing to \(-m\). Hence

\[
N\ge\frac34m^2.
\]

The nonneighbours sum to \(2m\), so

\[
Q\ge\frac18m^2.
\]

The diagonal, adjacent, and nonadjacent entries of \(E\) yield

\[
m=\frac8{15}m^2-\frac2{15}N+\frac1{30}Q,
\]

and consequently

\[
S:=\|y\|^2=30m-15m^2+5N.
\]

For \(1\le m\le16/7\),

\[
S\ge30m-\frac{45}{4}m^2\ge\frac{480}{49}.
\]

For \(m\ge16/7\),

\[
S=m^2+N+Q\ge\frac{15}{8}m^2\ge\frac{480}{49}.
\]

Equality forces

\[
m=\frac{16}{7},\qquad
 y_j=-\frac47\quad(j\sim i),\qquad
 y_j=\frac17\quad(j\not\sim i),
\]

so \(y=a_i\).

Therefore the 45 axes are exactly the minimum-norm nonzero idempotents. Every unmarked algebra automorphism must permute them. The marked-axis computation from Passes 3837–3854 therefore upgrades to

\[
\boxed{\operatorname{Aut}(V,\star)\cong O^-_6(2)\cong U_4(2):2,\qquad |\operatorname{Aut}|=51{,}840.}
\]

No separate marking hypothesis remains.

## 3890–3892 — explicit rational Wedderburn models

The 19-dimensional orbital algebra has the split rational decomposition

\[
\boxed{
M_2(\mathbb Q)\oplus\mathbb Q\oplus M_2(\mathbb Q)
\oplus\mathbb Q\oplus M_3(\mathbb Q).
}
\]

This packet freezes explicit matrices for every orbital in all five blocks. Their block sizes are

\[
2,1,2,1,3,
\]

and every block commutant has dimension one. Matrix multiplication reproduces all 19 structure constants exactly.

Primitive rational projectors on the 200-point permutation module have ranks

\[
1,81,15,15,24.
\]

The permutation module decomposes as

\[
\boxed{
\mathbb Q^{200}\cong1^{\oplus2}\oplus15_a^{\oplus2}\oplus15_b
\oplus24^{\oplus3}\oplus81.
}
\]

Characters were evaluated on all 51,840 group elements. Their Gram matrix is the \(5\times5\) identity, proving that these five rational characters are irreducible and pairwise distinct.

The packet also computes the exact projections of all pairwise tensor products onto these five known constituents. These are not claimed as complete tensor decompositions: every unaccounted residual dimension remains explicit.

## 3893 — the \(40K_{4,3}\) Monster seed

The smallest tripod–Norton orbital is again reconstructed as

\[
40K_{4,3},
\]

with 480 incidences. Its permutation character has norm

\[
\langle\chi_{480},\chi_{480}\rangle=23.
\]

Projection onto the five constructed irreducibles gives

\[
\boxed{
\chi_{480}=1+2\cdot81+2\cdot15_a+15_b+3\cdot24+\rho_{200}.
}
\]

The accounted part has degree 280. The residual character has

\[
\rho_{200}(1)=200,
\qquad
\langle\rho_{200},\rho_{200}\rangle=4,
\]

and is orthogonal to all five known characters.

This is a new representation-theoretic carrier. It is not yet decomposed into irreducibles.

The current explicit maximal-subgroup database for the Monster was searched at frozen commit

```text
1fa1e5cc5ad92bb822a1f11d2818e6703904271a
```

for direct keys `U4(2)`, `U4(2):2`, `O6-(2)`, and `40K4,3`. No direct key was found. Portable maximal-overgroup seeds exist for routes through \(3.\mathrm{Fi}_{24}'\), \((D_{10}\times HN).2\), and \(2^2.{}^2E_6(2):S_3\), but no serialized descent words or executed class fusion are promoted.

## 3894–3898 — corrected four-axis classification

### Withdrawn computation

Passes 3837–3854 used

```python
np.einsum('kab,a,b->k', structure, x, y, dtype=np.int64) % p
```

with coefficients modulo \(1{,}000{,}003\). The three-factor products were formed before reduction and could exceed signed 64-bit range. The resulting generated dimensions were therefore not reliable.

The replacement contracts in two stages:

```python
temp = np.tensordot(structure, x, axes=([1], [0])) % p
product = (temp @ y) % p
```

The corrected dimensions are identical over

\[
p\in\{101,103,107,1009,10007,1000003\}.
\]

### Corrected census

The 20 four-generator orbits have weighted generated-dimension census

\[
\boxed{
4^{135},
5^{720},
6^{1080},
10^{16740},
12^{5040},
14^{27000},
16^{14040},
24^{84240}.
}
\]

The former \(24^{103320}\) count is withdrawn. Five orbit types move into newly visible dimensions 12 and 16.

For every orbit representative, the local algebra has:

- zero annihilator;
- full square span;
- nondegenerate trace form;
- zero nucleus;
- full associator ideal;
- no identity;
- multiplication envelope \(M_d\).

Thus every local algebra is simple and nonunital.

The 20 generating-set orbits collapse to exactly eight subalgebra orbits, one in each dimension

\[
\boxed{4,5,6,10,12,14,16,24.}
\]

Their orbit sizes and contained-axis counts are

\[
\begin{array}{c|c|c}
d&\#\text{ subalgebras}&\#\text{ contained axes}\\\hline
4&27&5\\
5&720&4\\
6&120&6\\
10&540&7\\
12&40&9\\
14&36&15\\
16&45&13\\
24&1&45
\end{array}
\]

## 3899–3901 — the order-192 anti-coincidence barcode

Four recurring order-192 mechanisms are now separated.

### \(W(D_4)\)

The stabilizer of an ordered incident point-line pair in the 27-point \(GQ(2,4)\) action has

\[
1^1\,2^{43}\,3^{32}\,4^{84}\,6^{32},
\]

center order 2, derived subgroup order 96, and point orbits

\[
1,1,1,8,8,8.
\]

This is the same \(W(D_4)\) mechanism as the frame stabilizer.

### \(D_8\times S_4\)

A distinguished involution centralizer has

\[
1^1\,2^{59}\,3^8\,4^{68}\,6^{40}\,12^{16},
\]

center order 2, derived subgroup order 24, and abelianization order 8. Its census agrees exactly with \(D_8\times S_4\).

### Octonion axis-line stabilizer

The archived signed-permutation group acts freely and transitively on each 192-element axis-fixed embedding slice. Exact prior source gives center order 1 and 48 elements of order 8. It is therefore not \(W(D_4)\), despite sharing the order 192 and the same carrier count.

### Exceptional tomotope completion

The corrected Passes 3871–3886 result is

\[
2^4:D_{12},
\]

with trivial center, normal elementary abelian subgroup of order 16, ordinary kernel \(2^4:S_3\) of order 96, and a split outer \(C_2\) extension.

Hence

\[
\boxed{
192\text{ occurs through at least four structurally distinct mechanisms.}
}
\]

## 3902–3904 — three additional constructions

1. **Minimum-idempotent reconstruction.** The abstract multiplication recovers its Euclidean trace form, and the trace form recovers the 45 quadrangle points as the unique minimum-norm nonzero idempotents. The finite geometry is intrinsic to the algebra.

2. **Hidden degree-200 carrier.** The \(40K_{4,3}\) incidence action contains a degree-200 character of norm four orthogonal to \(1,15_a,15_b,24,81\). This is a precise new target for the Monster descent and for completing the rational character table seen by the carrier tower.

3. **Eight-species local zoo.** The corrected four-axis orbits form eight simple nonunital species in dimensions \(4,5,6,10,12,14,16,24\). The inclusion geometry of these species is now a finite, executable object.

## Evidence boundary

No portable Monster words, Monster class fusion, complete decomposition of the degree-200 residual, complete tensor-product table, SmallGroup identification of the octonion stabilizer, remote CI/PDF success, hardware result, laboratory result, thermodynamic result, or physical mechanism is claimed without separate executed evidence.
