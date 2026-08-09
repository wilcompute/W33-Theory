# Part CCCXVIII — Master Resource / Zeta Theorem

**Date:** 2026-05-05  
**Status:** unified finite invariant theorem for the Markov / Hashimoto / Ihara / Matrix Tree / Dirac / photonic stack

---

## 1. Purpose

The previous parts produced strong bridges, but they were still distributed across separate notes:

\[
\text{Markov},
\quad
\text{Hashimoto},
\quad
\text{Ihara},
\quad
\text{Matrix Tree},
\quad
\text{Dirac determinant},
\quad
\text{Seidel},
\quad
\text{critical fusion},
\quad
\text{Clifford orbits}.
\]

CCCXVIII packages them into one exact finite theorem.

---

## 2. Base W33 atoms

The W33 atoms are:

\[
q=3,
\qquad
\lambda=2,
\qquad
\mu=4.
\]

The graph has

\[
V=40,
\qquad
K=12,
\qquad
E=240,
\qquad
2E=480.
\]

The cyclotomic atoms are

\[
\Phi_3=13,
\qquad
\Phi_4=10,
\qquad
\Phi_6=7.
\]

The threshold/carrier pair is

\[
J=5,
\qquad
J^{-1}=8\pmod {13}.
\]

The generation/carrier counts are

\[
q^3=27,
\qquad
q^4=81.
\]

---

## 3. Directed-carrier normalizer

The directed carrier is

\[
2E=480.
\]

Three independent second-moment laws normalize against it:

\[
\frac{\operatorname{tr}(Q^2)}{480}=\Phi_3=13,
\]

\[
\frac{\operatorname{tr}(\Delta^2)}{480}=\Phi_4=10,
\]

\[
\frac{\operatorname{tr}(A_{L(W)}^2)}{480}=K-1=11.
\]

So the directed carrier reads off:

\[
\boxed{
\Phi_3,
\quad
\Phi_4,
\quad
K-1.
}
\]

---

## 4. Energy normalizer

The signless Laplacian energy is

\[
QLE=120.
\]

The Seidel spectrum has balanced masses

\[
S_+=120,
\qquad
S_-=120.
\]

Critical fusion at

\[
p=\frac12
\]

also splits the edge shell into

\[
pE=(1-p)E=120.
\]

The critical triangle trace is also

\[
6p^3T=120.
\]

So the same 120 is:

\[
\boxed{
QLE=S_+=S_-=pE=(1-p)E=6p^3T.
}
\]

---

## 5. Markov to Hashimoto

The ordinary random walk has

\[
K=12
\]

choices per step.

The Hashimoto nonbacktracking walk has

\[
K-1=11
\]

choices after orientation.

For \(n\)-edge paths,

\[
\frac{N_{NB}(n)}{N_{RW}(n)}
=
\left(\frac{K-1}{K}\right)^{n-1}
=
\left(\frac{11}{12}\right)^{n-1}.
\]

The entropy gap is

\[
\log\frac{12}{11}.
\]

---

## 6. Hashimoto to Ihara

The reciprocal Ihara zeta factorization is

\[
Z_W(u)^{-1}
=
(1-u^2)^{200}
(1-12u+11u^2)
(1-2u+11u^2)^{24}
(1+4u+11u^2)^{15}.
\]

The restricted Hashimoto roots sit on

\[
|x|=\sqrt{11}.
\]

At

\[
u=1,
\]

Ihara restricted factors become Laplacian eigenvalues:

\[
1-	heta+11=12-	heta.
\]

Thus

\[
1-2+11=10,
\]

and

\[
1+4+11=16.
\]

---

## 7. Ihara to Matrix Tree

The restricted Ihara determinant at \(u=1\) gives

\[
10^{24}16^{15}.
\]

This is the reduced Laplacian pseudo-determinant.

Matrix Tree gives

\[
\tau(W)=\frac{10^{24}16^{15}}{40}.
\]

Therefore

\[
\boxed{
\tau(W)=2^{81}5^{23}.
}
\]

The exponents are:

\[
81=q^4,
\]

and

\[
23=\Phi_3+\Phi_4.
\]

---

## 8. Dirac determinant compression

The paper determinant is

\[
Z_D(x)=(1-5x)^{10}(1+x)^{16}(1+7x)^6.
\]

Its bases are

\[
\{5,-1,-7\}=\{J,-1,-\Phi_6\}.
\]

Its exponents are

\[
\{10,16,6\}=\{\Phi_4,\mu^2,2q\}.
\]

So the determinant compresses the same Laplacian pair and gap.

The exponent product is

\[
10\cdot16\cdot6=960=\operatorname{tr}(A^3).
\]

The signed first moment is

\[
10\cdot5+16(-1)+6(-7)=-8=-J^{-1}.
\]

The second moment is

\[
10\cdot5^2+16+6\cdot7^2=560=\Phi_6(q^4-1).
\]

---

## 9. Critical fusion and Seidel split

The Type-II fusion probability is

\[
p_{fusion}=\frac{\lambda}{\mu}=\frac12.
\]

At this value,

\[
pE=(1-p)E=120.
\]

So critical fusion realizes the Seidel split

\[
120+120.
\]

The expected retained degree is

\[
pK=6=2q.
\]

The expected stabilizer weight is

\[
1+pK=7=\Phi_6.
\]

The expected full-cluster fusion trial count is

\[
E/p=480,
\]

the Hashimoto carrier.

---

## 10. Resource ladder and Clifford envelope

The physical/operator resource ladder is

\[
120\to240\to480\to960.
\]

Specifically:

\[
120=QLE=S_+=S_-=pE,
\]

\[
240=E=\text{edge shell}=\text{Seidel energy},
\]

\[
480=2E=\text{Hashimoto carrier}=E/p,
\]

\[
960=\operatorname{tr}(A^3)=6T.
\]

The Clifford/W33 automorphism group has order

\[
|\mathrm{Sp}(4,\mathbb F_3)|=51840.
\]

Dividing by the resource ladder gives

\[
\frac{51840}{120}=432=\mu^2q^3,
\]

\[
\frac{51840}{240}=216=J^{-1}q^3,
\]

\[
\frac{51840}{480}=108=\mu q^3,
\]

\[
\frac{51840}{960}=54=\lambda q^3.
\]

So the Clifford group resolves the whole ladder into exact orbit quotients.

---

## 11. Master theorem

**W33's operator, zeta, determinant, and photonic resource layers are one finite invariant system.**

Ordinary Markov walking passes to Hashimoto nonbacktracking with branch

\[
K-1=11.
\]

Ihara–Bass converts the Hashimoto quadratics into Laplacian eigenvalues

\[
10,
\quad
16
\]

at \(u=1\).  Matrix Tree gives

\[
\tau(W)=2^{81}5^{23}.
\]

The Dirac determinant compresses the same Laplacian pair and gap as exponents

\[
10,
16,
6.
\]

Seidel and critical fusion split the edge shell into

\[
120+120.
\]

The Clifford group order

\[
51840
\]

resolves the resource ladder

\[
120\to240\to480\to960
\]

by exact orbit quotients.

---

## 12. Honest boundary

This is an exact theorem package about the finite W33 structure and its graph/operator/resource interpretations.

It is not, by itself, a completed empirical theory of physics.

It is the exact invariant skeleton any such physical interpretation must be tested against.

---

## 13. Regression status

The CCCXVIII test file verifies:

1. W33 and cyclotomic atoms,
2. operator normalizers,
3. Ihara/Matrix Tree/Dirac compatibility,
4. critical fusion and resource ladder,
5. Clifford resource envelope,
6. threshold relations,
7. audit-level consistency.
