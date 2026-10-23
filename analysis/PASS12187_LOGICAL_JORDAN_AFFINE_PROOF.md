# Pass12187 — All-prime logical transvection law by affine shortening

22 October2026. Reservation `d7e64b620e16bc61e8e930f50d8f6b236fead563`.

This proves the general-prime formula left conjectural by the parallel track's
[exact census](2026-10-22_pascal_css_logical_transvection_jordan.md). The earlier
four-prime computations and polynomial-code identification belong to that work;
the p=3 Veronese model also appears in Pass5744–5751. The new contribution here
is the explicit shortening/projection argument which resolves the quotient's
extension problem. We do not claim global priority over modular representation
or Reed–Muller literature.

## The theorem

Let p be any prime, let B be the symplectic noncollinearity matrix of W(3,p),
C=row(B) over F_p and Q=C^perp/C. For any nonidentity symplectic transvection T,
write J_j for a length-j unipotent block. Then

```
Q restricted to <T> = J1^3 + sum(j=2..p-1) Jj^(2j) + Jp^p.
```

For D=T-I,

```
rank_Q D^0 = (2p^3+p+3)/3,
rank_Q D^k = (p-k)*((p-k)*(2p+k)+1)/3,  1<=k<=p.
```

Consequently dim ker D=p²+1, rank D=p(p-1)(2p-1)/3 and rank D^(p-1)=p.
For p=2 the middle sum is empty and the answer is J1^3+J2^2.
These are finite-field linear maps, not physical oscillation frequencies.

## 1. The existing polynomial model

The ambient projective point set P=PG(3,p) has n=(p+1)(p²+1) points.
For a point representative w,

```
B[x,w]=omega(x,w)^(p-1).
```

The nondegenerate alternating form supplies all linear forms; polarization in
degree p-1<p shows that their powers span all homogeneous polynomials of that
degree. Evaluation on P is injective: a homogeneous degree-p-1 polynomial
vanishing on all projective representatives vanishes on F_p^4, and a reduced
polynomial with each variable degree<p is determined by its evaluations.
Thus C is exactly that evaluation code and r=dim C=binom(p+2,3).
Self-orthogonality B²=0 and the point-coordinate CSS construction are prior work
([all-q exact-distance producer](w33_20261022_allq_pascal_CSS_exact_distance.py));
none of their distance claims is reproved or extended here.

## 2. Choose the geometry of this operator, not an arbitrary quotient basis

Write a nonidentity transvection as x -> x+omega(x,w)w. Its fixed projective
hyperplane is H=P(ker omega(-,w)). On A=P minus H, normalize
omega(x,w)=1 and choose affine coordinates (t,u,v) with t in direction w.
Then A=F_p^3 and T acts by t -> t+1, while it fixes H pointwise. A nonzero
transvection parameter is absorbed by rescaling t. The opposite pullback
convention replaces T with T^-1 and has the same Jordan lengths.

Split the ambient function space M=M_H plus M_A. Define the shortened code
C_A=C intersect M_A, identifying functions on A with zero extensions to P.

**Shortening lemma.** C_A=RM_p(p-2,3).

Indeed, a homogeneous degree-p-1 polynomial that vanishes on H has restriction
zero as a polynomial on its three-dimensional vector space: injectivity holds
in degree p-1<p there too. It is therefore divisible by the linear form defining
H. Set that form to1 on A. The resulting polynomials have total degree at most
p-2, and conversely every such affine polynomial homogenizes this way.

**Projection lemma.** The projection of C^perp onto M_A is exactly C_A^perp.

One inclusion follows from orthogonality. Conversely, if a in C_A^perp, then
c -> -<a,c|A> is a well-defined linear functional on C/C_A, hence on the image
of C in M_H. Extend this functional to M_H. Nondegeneracy of the standard dot
product on M_H gives an h realizing it; then (h,a) lies in C^perp. This proves
surjectivity without assuming a splitting as a module for <T>.

## 3. Identify the projected dual, including the duality proof

Use reduced affine polynomials: each variable exponent lies in0..p-1.
Generalized Reed–Muller duality gives

```
U=projection_A(C^perp)=RM_p(p-2,3)^perp=RM_p(2p-2,3).
```

Here it has a short independent proof. Products of monomials of total degrees
at most p-2 and2p-2 have degree at most3p-4. At least one variable exponent is
less than p-1, so its power sum over F_p vanishes, including exponent0 since
p=0 in F_p. Thus the codes are orthogonal. Complementing exponents by
(a,b,c) -> (p-1-a,p-1-b,p-1-c) shows their dimensions sum to p³: degree at most
p-2 complements precisely degree at least2p-1. Hence orthogonality is equality
with the dual. The ordinary reduced monomial basis is independent by evaluation.

This is standard generalized Reed–Muller machinery, not claimed as new. See
[Elkies, Math256x, Reed–Muller discussion](https://people.math.harvard.edu/~elkies/M256.13/index.html)
for the same power-sum/dimension proof. The novelty boundary is its application
to the earlier logical-quotient conjecture and the exact intersection below.

## 4. The intersection that resolves the extension problem

For k>=1, D kills M_H, so the projection lemma gives

```
D^k(C^perp)=D^k U contained in M_A,
C intersect D^k(C^perp)=C_A intersect D^k U,
rank_Q D^k=dim D^k U - dim(C_A intersect D^k U).
```

Use the binomial basis b_i(t)=binom(t,i), 0<=i<=p-1, with factorials invertible
in F_p. The triangular change from t^i to b_i preserves each total-degree
filtration, and

```
D b_i=b_(i-1),  D b_0=0.
```

This identity holds also across t=p-1 ->0 in the finite field. It follows that
D^k U has the independent basis

```
b_l(t) u^j v^m,
0<=l<=p-1-k, 0<=j,m<=p-1,
l+j+m<=2p-2-k.
```

The shortened code C_A uses the same full affine basis, with total degree at
most p-2. Their intersection is therefore exactly the common subset of basis
vectors, not an assumed semisimple or split intersection.

For fixed l in0..p-1-k, the two counts are respectively

```
p²-(k+l)(k+l+1)/2,
(p-1-l)(p-l)/2.
```

For the first, remove the triangular corner j+m>2p-2-k-l; for the second count
the triangle j+m<=p-2-l. The endpoint l=p-1 when it occurs has empty triangle;
for k>=1 here l<=p-2 anyway. Summing their difference gives

```
R_k=sum(l=0..p-1-k)
 [p²-((k+l)(k+l+1)+(p-1-l)(p-l))/2]
 =(2p³-3kp²+k³+p-k)/3.
```

For k=p the sum is empty and R_p=0. Dimension supplies
R_0=(2p³+p+3)/3; note the extra1 compared with extrapolating the k>=1 cubic
to zero. Omitting that1 would give the wrong number of trivial blocks.

Second differences give m_1=R_0-2R_1+R_2=3,
m_j=R_(j-1)-2R_j+R_(j+1)=2j for2<=j<=p-1, and m_p=R_(p-1)=p.
For p=2 use m_1=R_0-2R_1 and m_2=R_1 directly. This proves the theorem.

## Independent computational controls

- Symbolic summation and all second-difference/dimension identities vanish.
- For p=2,3,5, independently evaluate the full native projective code, shorten
  at x0=0 and project its actual kernel onto x0=1; compare exact row spaces with
  both affine codes. No supplied quotient basis is trusted.
- Evaluate affine functions independently and calculate actual finite
  differences, image ranks and intersections for p=2,3,5.
- Re-run the prior full projective quotient computation for p=2,3,5.
- Check binomial finite differences including wraparound for p=2,3,5,7.
- Enumerate common affine basis supports at primes through31 and check the
  rank law. These are controls on a proof, not its all-prime justification.

Producer: `w33_pass12187_logical_jordan_affine_proof.py`;
certificate: `../data/w33_pass12187_logical_jordan_affine_proof.json`;
regressions: `../tests/test_w33_pass12187_logical_jordan_affine_proof.py`.
All16 focused regressions pass in127.70s in the actual checkout. An identical isolated copy passes in1.80s; no speed comparison is used as mathematical evidence.

## What this opens, and what remains missing

This closes one explicitly stated mathematical problem in the incoming work.
For p=3, it supplies a proof of J1^3+J2^4+J3^3 on the20-dimensional logical
label quotient. The parallel [faithful PSp(4,3) action](2026-10-22_pascal_css_faithful_logical_clifford.md)
therefore has an exact uniform-prime transvection fingerprint. No identification
with the native four-period module, E6 matter or three particle families follows
from the number3 of trivial Jordan blocks.

The proof depends crucially on degree p-1<p and on translation over F_p.
Substituting a prime power q for p is not justified: degree q-1 polarization and
characteristic-p finite differences behave differently. Photonic locality,
non-Clifford resources, a physical clock scale, a dynamical spacetime and a
stable realistic flavour vacuum remain separate requirements.
