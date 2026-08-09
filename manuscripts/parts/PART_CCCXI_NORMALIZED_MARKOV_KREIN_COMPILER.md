# Part CCCXI — Normalized Markov / Krein Compiler

**Date:** 2026-05-05  
**Status:** exact probability/dual-association compiler for W(3,3)

---

## 1. Live-commit trigger

Two new live commit batches landed after the Seidel compiler:

1. **PART CCCIX — Normalized Laplacian Spectrum of W(3,3)**, with normalized Laplacian eigenvalues

\[
0^1,
\left(\frac56\right)^{24},
\left(\frac43\right)^{15}.
\]

It records the exact normalized spectral identities, including trace \(40\), second moment \(130/3\), gap \(5/6\), largest eigenvalue \(4/3\), and the numerator/denominator encodings in the two nontrivial eigenvalues.  fileciteturn389file0

2. **PART CCCX — Krein Parameters of W(3,3)**, with exact dual Bose–Mesner/Krein parameters.  It derives the Q-matrix and records, among others,

\[
q^0_{11}=24,
\qquad
q^0_{22}=15,
\]

\[
q^2_{11}=\frac{40}{3},
\qquad
q^2_{22}=\frac{10}{3},
\]

and

\[
q^1_{11}=\frac{44}{3},
\qquad
q^1_{22}=\frac{20}{3}.
\]

fileciteturn390file0

CCCXI compiles those into the probability-language version of the master theorem.

---

## 2. Random-walk operator

For a \(K\)-regular graph,

\[
P=\frac{A}{K}
\]

is the random-walk transition operator.

Since W(3,3) has adjacency eigenvalues

\[
12,
\quad
2,
\quad
-4,
\]

and

\[
K=12,
\]

we get random-walk eigenvalues

\[
1,
\quad
\frac{1}{6},
\quad
-\frac{1}{3}.
\]

Because

\[
q=3,
\]

these are

\[
1,
\quad
\frac{1}{2q},
\quad
-\frac{1}{q}.
\]

So the stochastic dynamics has a q-clock spectrum:

\[
\boxed{
P\text{ has nontrivial eigenvalues }+\frac{1}{2q}\text{ and }-\frac{1}{q}.
}
\]

The second-largest absolute eigenvalue is therefore

\[
\frac1q=\frac13.
\]

---

## 3. Normalized Laplacian

The normalized Laplacian is

\[
L_{norm}=I-P.
\]

So its nontrivial eigenvalues are

\[
1-\frac{1}{6}=\frac56,
\]

and

\[
1+\frac13=\frac43.
\]

Equivalently,

\[
\frac56=1-\frac{1}{2q},
\]

and

\[
\frac43=1+\frac1q.
\]

They satisfy:

\[
\frac56+\frac43=\frac{13}{6}=\frac{\Phi_3}{2q},
\]

\[
\frac56\cdot\frac43=\frac{10}{9}=\frac{\Phi_4}{q^2},
\]

and

\[
\frac43-\frac56=\frac12.
\]

So the normalized Laplacian packages \(\Phi_3\), \(\Phi_4\), and the half-step gap into the two nontrivial stochastic modes.

---

## 4. Two-step return trace

The random-walk square trace is

\[
\operatorname{tr}(P^2)
=
1+24\left(\frac16\right)^2+15\left(-\frac13\right)^2.
\]

Compute:

\[
\operatorname{tr}(P^2)
=1+\frac{24}{36}+\frac{15}{9}
=1+\frac23+\frac53
=\frac{10}{3}.
\]

But

\[
\frac{10}{3}=\frac{\Phi_4}{q}.
\]

Therefore

\[
\boxed{
\operatorname{tr}(P^2)=\frac{\Phi_4}{q}.
}
\]

This is the q-scaled theta/Fiedler return trace.

---

## 5. Krein dual agreement

From CCCX:

\[
q^2_{22}=\frac{10}{3}.
\]

Therefore

\[
q\,q^2_{22}=3\cdot\frac{10}{3}=10=\Phi_4.
\]

But the Markov trace identity gives

\[
q\operatorname{tr}(P^2)=q\cdot\frac{10}{3}=10=\Phi_4.
\]

So

\[
\boxed{
q\,q^2_{22}=q\operatorname{tr}(P^2)=\Phi_4.
}
\]

This is the cleanest dual/probability weld: the same \(\Phi_4\) appears both as a Krein parameter scaling and a two-step Markov return scaling.

---

## 6. Krein firewall and Cayley carrier square

The Krein multiplicity difference gives

\[
q^0_{11}-q^0_{22}=24-15=9=q^2.
\]

This is the firewall sector again.

The carrier-square identity is

\[
q(q^1_{11}+q^1_{22})
=3\left(\frac{44}{3}+\frac{20}{3}\right)
=64.
\]

But

\[
64=8^2=(J^{-1})^2.
\]

So

\[
\boxed{
q(q^1_{11}+q^1_{22})=(J^{-1})^2.
}
\]

The Krein algebra contains both:

\[
q^2=9
\]

and

\[
8^2=64.
\]

That is, it contains the firewall sector and the Cayley carrier square.

---

## 7. Theorem statement

**The normalized Laplacian turns the spectral theorem into a q-clock Markov channel.**  The random-walk operator

\[
P=A/K
\]

has nontrivial eigenvalues

\[
+\frac{1}{2q},
\qquad
-\frac1q,
\]

so its contraction scale is exactly

\[
\frac1q.
\]

The normalized Laplacian eigenvalues

\[
\frac56,
\qquad
\frac43
\]

have sum

\[
\frac{\Phi_3}{2q},
\]

product

\[
\frac{\Phi_4}{q^2},
\]

and difference

\[
\frac12.
\]

The two-step Markov trace is

\[
\frac{\Phi_4}{q},
\]

matching the Krein dual identity

\[
\Phi_4=q q^2_{22}.
\]

Meanwhile,

\[
q^0_{11}-q^0_{22}=q^2
\]

gives the firewall, and

\[
q(q^1_{11}+q^1_{22})=8^2
\]

gives the Cayley carrier square.

---

## 8. Why this matters

This converts the deterministic operator stack into probability language.

Before CCCXI, the pipeline was:

\[
A,L,Q,\Delta,S,L(W),B_{Hashimoto}.
\]

Now we also have the stochastic operator

\[
P=A/K,
\]

with q-clock modes

\[
+\frac{1}{2q},
\qquad
-\frac1q.
\]

The same constants now appear as:

1. Markov rates,
2. normalized Laplacian moments,
3. Krein dual structure constants,
4. firewall and Cayley-carrier square identities.

---

## 9. Regression status

The CCCXI test file verifies:

1. random-walk q-clock spectrum,
2. random-walk return moments,
3. normalized Laplacian spectrum and invariants,
4. normalized nontrivial sum/product/difference,
5. Krein dual agreement with Markov and carrier identities,
6. global exponents and threshold relation,
7. audit-level consistency.

---

## 10. Next target

The next breakthrough target is to combine:

\[
P=A/K
\]

with the Hashimoto nonbacktracking operator.

The question is whether the nonbacktracking branch law

\[
K-1=11
\]

and the Markov contraction scale

\[
1/q
\]

combine into a single entropy law for loop formation:

\[
\text{ordinary walk probability}
\to
\text{nonbacktracking conditioned probability}
\to
\text{Matrix Tree entropy}.
\]
