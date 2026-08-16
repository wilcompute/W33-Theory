# Passes 5580–5585 — Reye/tomotope family = projectivity-graph incidence

## Status

**PASS**, with one explicitly separated experimental binary-rank conjecture.

This packet starts from the only structural survivor of the Pass 5480–5579 coincidence audit: the incidence family obtained from the hyperbolic quadratic form

\[
Q(x)=x_0x_1+x_2x_3
\]

and the symplectic form

\[
B(x,y)=x_0y_1-x_1y_0+x_2y_3-x_3y_2.
\]

Passes 5488–5495 had already proved that at \(q=3\) one nonsingular quadratic class together with the singular quadric is the Reye configuration \(12_4\,16_3\), hence the tomotope edge–triangle medial layer, and had verified the same tactical construction at \(q=5,7\). The question here is what the family *is*.

## Pass 5580 — the 4-vector is a 2×2 matrix

Associate

\[
X(x)=\begin{pmatrix}x_0&x_2\\-x_3&x_1\end{pmatrix}.
\]

Then

\[
\det X(x)=x_0x_1+x_2x_3=Q(x).
\]

Therefore the singular quadric \(Q^+(3,q)\) is exactly the projectivized rank-one locus. Writing \(X=uv^T\) gives the Segre parametrization

\[
Q^+(3,q)\cong \mathbf P^1(q)\times\mathbf P^1(q),
\qquad |Q^+(3,q)|=(q+1)^2.
\]

In the coordinates used by the repository verifier,

\[
s(u,v)=(u_0v_0,\,u_1v_1,\,u_0v_1,\,-u_1v_0).
\]

This is not a count match: the executable verifier checks that these are exactly all singular projective points for \(q=3,5,7,11,13\).

## Pass 5581 — symplectic incidence is a graph of a projectivity

For a nonsingular point \(p=(a,b,c,d)\), set

\[
T_p=\begin{pmatrix}c&-a\\-b&-d\end{pmatrix}.
\]

A direct determinant calculation gives

\[
B\bigl(p,s(u,v)\bigr)=0
\quad\Longleftrightarrow\quad
u\sim T_pv,
\]

where \(u\sim T_pv\) means equality as points of \(\mathbf P^1(q)\). Thus every nonsingular point of \(\mathrm{PG}(3,q)\) is a projectivity graph on the Segre grid, and the W(3,q) symplectic-perpendicular incidence is literally graph membership.

Moreover

\[
\det T_p=-Q(p).
\]

Projectively, determinant square class splits \(\mathrm{PGL}_2(q)\) into its two \(\mathrm{PSL}_2(q)\) cosets for odd \(q\). Hence either nonsingular quadratic class is, after multiplying by one fixed projectivity if necessary, the permutation-graph incidence design of

\[
G=\mathrm{PSL}_2(q)\curvearrowright \mathbf P^1(q).
\]

This explains the entire parameter family at once:

\[
|G|=\frac{q(q^2-1)}2,
\qquad
v=(q+1)^2,
\]

\[
\text{row weight}=q+1,
\qquad
\text{column weight}=\frac{q(q-1)}2.
\]

The last number is the point-stabilizer order. Long–Plaza–Sin–Xiang (2016, arXiv:1608.07304) study exactly this 2-transitive action of \(\mathrm{PSL}_2(q)\) on \(\mathrm{PG}(1,q)\) and record the same point-stabilizer size in their EKR analysis. Their paper is useful prior art for the group action; the present packet's new repo-level bridge is the explicit identification of the Pass 5492 incidence family with its graph-incidence matrix.

## Pass 5582 — exact rook-complement Gram factorization

Let \(M\) be the \(|G|\times(q+1)^2\) incidence matrix whose row for \(g\in G\) is the vectorized permutation matrix of \(g\):

\[
M_{g,(x,y)}=1\iff y=g(x).
\]

Two distinct grid cells \((x,y)\) and \((x',y')\) lie on a common projectivity graph iff both coordinates differ. By 2-transitivity, if both differ then exactly the two-point stabilizer

\[
\frac{q-1}{2}
\]

group elements contain both cells. Therefore, if \(A\) is the adjacency matrix of the complement of the \((q+1)\times(q+1)\) rook graph,

\[
\boxed{
M^TM=\frac{q-1}{2}\,(qI+A).
}
\]

The rook-complement graph is \(K_{q+1}\times K_{q+1}\), with spectrum

\[
q^2{}^{\,1},\qquad 1^{\,q^2},\qquad (-q)^{\,2q}.
\]

Hence

\[
\boxed{
\operatorname{spec}(M^TM)
=
\left(\frac{q(q^2-1)}2\right)^1
\oplus
\left(\frac{q^2-1}{2}\right)^{q^2}
\oplus
0^{2q}.
}
\]

In particular,

\[
\boxed{\operatorname{rank}_{\mathbf Q}M=q^2+1.}
\]

The verifier independently certifies the lower bound by modular Gaussian elimination at the prime 1,000,003 for \(q=3,5,7,11,13\); the Gram factorization supplies the exact upper bound.

## Pass 5583 — a canonical \(q^2\)-dimensional tight frame

Each row has \(q+1\) ones among \((q+1)^2\) coordinates. Center it by subtracting the constant vector of mean \(1/(q+1)\). The centered norm is \(q\). If two projectivities agree on \(t\in\{0,1,2\}\) projective points, the centered inner product is \(t-1\). After unit normalization the possible inner products are

\[
\boxed{
-\frac1q,\quad0,\quad\frac1q.
}
\]

The constant eigenline has been removed, leaving the single nonzero eigenvalue \((q^2-1)/2\) with multiplicity \(q^2\). Thus the \(|\mathrm{PSL}_2(q)|\) centered rows form a unit-norm tight frame in \(\mathbf R^{q^2}\), with frame bound

\[
\boxed{
\frac{|\mathrm{PSL}_2(q)|}{q^2}
=
\frac{q^2-1}{2q}.
}
\]

At \(q=3\), only intersection sizes \(0,1\) occur, so the Reye member is a two-distance specialization with inner products \(-1/3,0\). For the tested \(q=5,7,11,13\), all three values occur.

## Pass 5584 — why the Reye automorphism group has order 576

At \(q=3\),

\[
\mathrm{PSL}_2(3)\cong A_4
\]

in its natural action on four points. The Reye configuration becomes:

- 12 row-points = the even permutations \(A_4\);
- 16 column-lines = cells \((x,y)\in[4]\times[4]\);
- incidence \(g\sim(x,y)\iff y=g(x)\).

For \((a,b)\in S_4\times S_4\) with equal parity,

\[
(x,y)\mapsto(a x,b y),
\qquad
g\mapsto bga^{-1}
\]

preserves incidence and the row set \(A_4\). There are

\[
\frac{24^2}{2}=288
\]

such transformations. Adjoining transpose/inversion,

\[
(x,y)\leftrightarrow(y,x),
\qquad g\leftrightarrow g^{-1},
\]

doubles this to

\[
\boxed{576.}
\]

The executable verifier constructs all 576 distinct automorphisms directly. The resulting abstract shape is

\[
\boxed{
\{(a,b)\in S_4^2:\operatorname{sgn}a=\operatorname{sgn}b\}\rtimes C_2
\cong ((A_4\times A_4):C_2):C_2.
}
\]

That is exactly the structure previously found by GAP in Pass 5516 for the Klein-\(V_4\) Latin-square autoparatopy group / 13-cover image. This does **not** identify those acted-on objects; it gives a structural reason that the Reye configuration naturally carries the same abstract 576-group rather than merely sharing its order.

## Pass 5585 — binary rank: strong pattern, not yet theorem

The same incidence matrices have measured binary ranks

\[
8,18,32,72,98
\]

at

\[
q=3,5,7,11,13,
\]

respectively. These are exactly

\[
\boxed{
\operatorname{rank}_{2}M=\frac{(q+1)^2}{2}
}
\]

for every tested prime.

This is **not promoted to an all-q theorem**. Characteristic two is precisely where the projective-line permutation module ceases to split semisimply; the existing Pass 5356–5361 firewall already warns against reducing characteristic-zero decompositions modulo two. The next proof target is therefore the image algebra of the binary \(\mathrm{PSL}_2(q)\) permutation representation, not another numerical fit.

## Verification table

| q | rows | columns | rank Q | rank F2 | nonzero centered frame eigenvalue |
|---:|---:|---:|---:|---:|---:|
| 3 | 12 | 16 | 10 | 8 | 4 |
| 5 | 60 | 36 | 26 | 18 | 12 |
| 7 | 168 | 64 | 50 | 32 | 24 |
| 11 | 660 | 144 | 122 | 72 | 60 |
| 13 | 1092 | 196 | 170 | 98 | 84 |

## Evidence boundary

1. The q=3 Reye/tomotope incidence is prior repository work, not re-claimed here.
2. The projectivity-graph identity and Gram factorization are exact coordinate/group-action deductions and are independently replayed at five odd primes.
3. The executable verifier is prime-field only; the prime-power extension is not certified here even though the coordinate formulas strongly suggest it.
4. No q>3 polytope realization is claimed.
5. No physical interpretation follows from the incidence isomorphism.
6. The binary rank formula remains a conjecture outside the five tested primes.
