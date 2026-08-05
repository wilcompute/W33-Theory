# Passes 3570–3576 — maximal cyclic bridge, stable symmetry ancillas, and a gate-minimal quadratic locator

## Exact status

The verifier reports

```text
PASS_7_FRONTS 38ea92c1767dda0b786232710f37ead7ec35628511c36dfb7b3d2c79f35a9ad0
```

This packet continues the exact \(C_5\) rank-20 bridge and the five-bit compound-fault locator from Passes 3556–3569. It closes two previously vague boundaries:

1. what “canonical \(C_5\) intertwiner” can mean from symmetry data alone;
2. whether the five-bit hardware must remain a case-table ROM.

The answers are respectively an exact non-canonicity/stable-extension theorem and a multiplicatively optimal quadratic Boolean compiler.

---

## 3570 — maximal cyclic bridge theorem

Over the rational group algebra of \(C_5\), both rank-20 modules decompose as

\[
P_{20}\downarrow_{C_5}
\cong
W_{20}\downarrow_{C_5}
\cong
4\mathbf1\oplus4\mathbb Q(\zeta_5).
\]

Therefore the rational intertwiner algebra is

\[
\boxed{
\operatorname{Hom}_{\mathbb Q[C_5]}(P_{20},W_{20})
\cong M_4(\mathbb Q)\oplus M_4(\mathbb Q(\zeta_5))
}
\]

and has rational dimension

\[
16+4\cdot16=\boxed{80}.
\]

The invertible intertwiners form the open set

\[
\boxed{GL_4(\mathbb Q)\times GL_4(\mathbb Q(\zeta_5))}.
\]

Thus the \(C_5\) action alone cannot select a preferred map: the ambiguity is an exact 80-dimensional rational gauge algebra, not merely a missing implementation detail.

---

## 3571 — the 16-dimensional cyclotomic core extends to \(D_{10}\)

On the dihedral normalizer \(D_{10}=C_5\rtimes C_2\), the rational multiplicities are

\[
P_{20}:\quad2\mathbf1\oplus2\varepsilon\oplus4V_{\rm cyc},
\]

\[
W_{20}:\quad4\mathbf1\oplus4V_{\rm cyc},
\]

where \(V_{\rm cyc}\) is the four-dimensional rational cyclotomic simple with endomorphism field \(\mathbb Q(\sqrt5)\).

The complete moving sector therefore agrees:

\[
\boxed{(1-e_{\rm fix})P_{20}\cong(1-e_{\rm fix})W_{20}}
\]

with dimension

\[
\boxed{16}.
\]

The obstruction is confined to the four-dimensional \(C_5\)-fixed sector. The Perkel fixed sector splits as \(2\mathbf1+2\varepsilon\), while the W33 fixed sector is \(4\mathbf1\).

Consequently every \(D_{10}\)-equivariant map has rank at most

\[
\boxed{18},
\]

and the minimum kernel and cokernel dimensions are both two.

---

## 3572 — minimal 22-dimensional stable \(D_{10}\) bridge

The fixed-sector mismatch has a unique minimal stabilization at the multiplicity level:

\[
\boxed{
P_{20}\oplus2\mathbf1
\cong
W_{20}\oplus2\varepsilon
\quad\text{as }\mathbb Q[D_{10}]\text{-modules}.
}
\]

Both sides have dimension

\[
\boxed{22}.
\]

No stabilization of smaller total dimension per side can work, because two sign copies are absent from W33 and two trivial copies are absent from Perkel.

The appearance of 22 matches the controller’s 22 valid envelope states arithmetically, but no objectwise identification between those two structures is asserted.

---

## 3573 — minimal 26-dimensional stable \(A_5\) bridge

Over \(\mathbb Q[A_5]\), write the rational six-dimensional constituent as \(3\oplus3'\). The two modules are

\[
P_{20}=\mathbf1\oplus(3\oplus3')\oplus2\cdot4\oplus5,
\]

\[
W_{20}=3\mathbf1\oplus3\cdot4\oplus5.
\]

Their maximum common submodule has dimension

\[
\boxed{14},
\]

and the rational Hom space has dimension ten.

The minimal stable extension is

\[
\boxed{
P_{20}\oplus2\mathbf1\oplus4
\cong
W_{20}\oplus(3\oplus3')
}
\]

of common dimension

\[
\boxed{26}.
\]

This gives the exact symmetry-extension ladder

\[
\boxed{20\xrightarrow{D_{10}}22\xrightarrow{A_5}26}
\]

for invertible stable bridges, while the maximum unstabilized ranks descend as

\[
\boxed{20\to18\to14}.
\]

---

## 3574 — the Borel observable algebra cannot supply an order-five selector

The new Perkel Borel packet uses

\[
B=C_{19}\rtimes C_9,
\qquad |B|=171=3^2\cdot19.
\]

Hence

\[
\gcd(|B|,5)=1
\]

and \(B\) contains no element of order five. Its exact 11-observable/10-phase orbital decomposition is valuable for Borel-equivariant kernels, but it supplies neither a \(C_5\) generator nor its dihedral normalizer.

Therefore that decomposition is not automatically a canonical \(C_5\)-equivariant selector. Any preferred objectwise bridge must introduce additional cross-module geometry beyond the separate group actions.

---

## 3575 — quadratic normal form of the five-bit locator

Let the four axis bits be \(x_0,x_1,x_2,x_3\in\mathbb F_2\), and let the five companion bits be \(y_0,\ldots,y_4\). Möbius inversion of the exact 16-row truth table gives

\[
y_0=x_0x_2+x_0x_3+x_1x_3,
\]

\[
y_1=x_2+x_0x_2+x_1x_2+x_0x_3,
\]

\[
y_2=x_2+x_0x_2+x_1x_2+x_1x_3,
\]

\[
y_3=x_2+x_1x_2+x_0x_3+x_1x_3,
\]

\[
y_4=x_2+x_1x_2+x_0x_3+x_2x_3.
\]

All five outputs have algebraic degree two. Their homogeneous quadratic parts have rank

\[
\boxed5
\]

inside the six-dimensional quadratic space. More precisely, they span exactly the hyperplane in which the \(x_0x_1\) coefficient vanishes.

In any XOR–AND circuit, each AND gate can enlarge the span of homogeneous quadratic parts by at most one. Therefore at least five AND gates are necessary.

The five products

\[
a=x_0x_2,\quad b=x_0x_3,\quad c=x_1x_2,
\quad d=x_1x_3,\quad e=x_2x_3
\]

attain that lower bound. Hence

\[
\boxed{\text{multiplicative complexity}=5}.
\]

One shared-subexpression network uses those five AND gates and eight XOR gates:

\[
\begin{aligned}
t_0&=a+b,&y_0&=t_0+d,\\
t_1&=x_2+t_0,&y_1&=t_1+c,\\
t_2&=y_1+a,&y_2&=t_2+y_0,\\
y_3&=t_0+y_2,&y_4&=t_2+e.
\end{aligned}
\]

---

## 3576 — exact RTL replacement and fault-distance preservation

The quadratic RTL is exhaustively compared against the original 16-entry table for all axis words. The complete compound code is then rebuilt from the quadratic implementation and rechecked over all

\[
1+16+\binom{16}{2}=137
\]

zero-, single-, and double-device-fault patterns.

The minimum distance remains

\[
\boxed3.
\]

Thus the table and quadratic circuit are functionally identical, while the nonlinear gate count is globally minimal.

---

## Boundaries

- \(C_5\) action alone cannot choose a preferred intertwiner; extra cross-module geometry may still do so.
- The Borel no-order-five theorem does not say every Borel observable is useless; it says no canonical \(C_5\) selector follows from the Borel action alone.
- The exact symmetry-stabilization dimensions 22 and 26 are representation-theoretic ancilla costs, not yet physical qubit or slot counts.
- The chromatic frontier remains \(10\le\chi(H)\le11\).
- The cohomology radius remains \(389\le D_{H^1}\le435\).
- The unrestricted magnetic optimum remains open.
- RTL timing, area, and power remain synthesis/placement evidence.
