# Pass 157 — The three-prime collision theorem and the minimal-shell \(E_8\) bridge

**Status: PASS.** The exact witness
`analysis/w33_pass157_eigenlattice_prime_collision.py` passes all 20 checks;
the focused regression suite is
`tests/test_pass157_eigenlattice_prime_collision.py`.

## 1. The full discriminant group

Let \(A\) be the W33 adjacency matrix and
\[
L_2=\ker_{\mathbb Z}(A-2I).
\]
An integral Smith-kernel basis \(K\) has 24 columns. Exact integer arithmetic
on \(G=K^{\mathsf T}K\) gives
\[
\operatorname{SNF}(G)
=\operatorname{diag}(1^8,2^6,6^9,30),
\]
not merely its determinant. Therefore
\[
L_2^\#/L_2
\cong(\mathbb Z/2)^6\oplus(\mathbb Z/6)^9\oplus\mathbb Z/30
\cong(\mathbb Z/2)^{16}\oplus(\mathbb Z/3)^{10}\oplus\mathbb Z/5.
\]
In particular,
\[
\det L_2=2^{16}3^{10}5,
\]
and every primary factor is elementary: there is no hidden \(4\), \(9\), or
\(25\) torsion.

## 2. What the exponents \(16,10,1\) count

Write \(W=L_2/pL_2\) with its reduced standard dot product. The three
determinant exponents are exactly the radical dimensions of \(W\):
\[
\begin{array}{c|c|c}
p&\dim\operatorname{rad}(W)&\text{intrinsic radical}\\ \hline
2&16&\operatorname{im}(A\bmod2)=C\\
3&10&\operatorname{im}\big((A+I)|_{\mathbf1^\perp}\big)\\
5&1&\langle\mathbf1\rangle .
\end{array}
\]

The middle row closes the unexplained \(3^{10}\). The strongly regular
identity
\[
A^2=8I-2A+4J
\]
implies
\[
(A+I)^2=J\pmod3.
\]
Thus \(N=A+I\) is square-zero on the augmentation hyperplane
\(H=\mathbf1^\perp\). Its full rank is 11, while
\(\operatorname{rank}(N|_H)=10\). Reduction of the integral \(+2\)
eigenlattice gives a 24-dimensional subspace \(W\subseteq\ker N\), and the
exact span and orthogonality checks give
\[
\operatorname{rad}(W)=\operatorname{im}(N|_H),\qquad\dim=10.
\]
The exponent is therefore a modular eigenvalue-collision layer, not the
previous numerical coincidence \(10=\dim\operatorname{Sp}(4)\).

At \(p=2\), \(W=\ker A\), \(A^2=0\), and
\(\operatorname{rad}(W)=\operatorname{im}A=C\), recovering the binary W33
code of dimension 16. At \(p=5\), the Perron eigenvalue \(12\) meets \(2\);
the all-ones vector enters \(W\) and spans its one-dimensional radical.
Together these identify every prime and every exponent in the determinant.

## 3. The complete minimal shell

The earlier claim \(\min L_2=6\) was true, but an LLL-reduced basis did not
prove it. Pass 157 supplies an exact Fincke–Pohst enumeration with PARI:
\[
\min L_2=6,\qquad |\operatorname{Min}(L_2)|=480.
\]

Those 480 vectors have a direct W33 description. For a point \(p\) and an
ordered pair of distinct lines \(L_+,L_-\) through \(p\), set
\[
x(p;L_+,L_-)
=\mathbf1_{L_+\setminus\{p\}}-\mathbf1_{L_-\setminus\{p\}}.
\]
The generalized-quadrangle axiom gives
\[
Ax=2x,\qquad x^{\mathsf T}x=6.
\]
There are exactly
\[
40\cdot4\cdot3=480
\]
such oriented local line pairs. They are all distinct, and the exact
enumeration proves that there are no other minimal vectors. Every minimal
vector has the same inner-product profile against the shell:
\[
\{-6^1,-3^4,-2^{45},-1^{108},0^{164},
  1^{108},2^{45},3^4,6^1\}.
\]

## 4. Why the non-\(E_8\) lattice still carries all \(E_8\) roots

Quotienting the 480 minimal vectors by \(x\sim-x\) forgets the ordering of
\((L_+,L_-)\). Hence the 240 projective minimal rays are exactly the
unordered pairs of lines through a W33 point:
\[
\operatorname{Min}(L_2)/\{\pm1\}
\longleftrightarrow
\{(p,\{L_i,L_j\})\}
\quad(240).
\]
These are precisely the 240 endpoints of the 120 local pencil-octahedron
axes from Pass 123. Pairing complementary endpoints produces an axis, and
Pass 123's exact quadratic-space isometry assigns the two endpoints to the
two signed roots \(\pm\alpha\) of one \(E_8\) root line. Consequently,
\[
\boxed{\operatorname{Min}(L_2)/\{\pm1\}
\longleftrightarrow \Phi(E_8)}
\]
as a 240-element, gauge-fixed combinatorial correspondence.

This does not make \(L_2\) isometric to \(E_8^3\): its rank, determinant, and
minimal-shell metric rule that out. It says something sharper than the old
negative result: the failed eigenlattice contains the complete signed
\(E_8\) root carrier in its **projective minimal shell**, while its three
bad-prime radicals record exactly how the integral metric fails to be
unimodular.

## Reproduce

```bash
./.venv/bin/python analysis/w33_pass157_eigenlattice_prime_collision.py
./.venv/bin/python -m pytest -q tests/test_pass157_eigenlattice_prime_collision.py
```

The generated certificate is
`data/w33_pass157_eigenlattice_prime_collision.json`. When PARI/GP is
available, the script reruns `qfminim` live; otherwise it uses the checked
minimum certificate while retaining all exact Smith, modular-radical, and
combinatorial checks.
