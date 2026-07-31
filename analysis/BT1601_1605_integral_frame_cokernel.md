# Passes 1601–1605 — Integral frame cokernel, K4,4 Bockstein, and the 15→45→30 chain

## Executive result

Let

\[
M\in\{0,1\}^{540\times240}
\]

be the canonical frame/edge incidence matrix of the W33 cross-matching construction. Every row is a four-edge matching, and every W33 edge occurs in nine frame rows.

The complete nonzero Smith data of \(M^{\mathsf T}\) is

\[
\boxed{
\operatorname{SNF}(M^{\mathsf T})
=
1^{195}\oplus2^{30}\oplus0^{15}.
}
\]

Equivalently,

\[
\boxed{
\operatorname{coker}(M^{\mathsf T})
\cong
\mathbb Z^{15}\oplus(\mathbb Z/2\mathbb Z)^{30}.
}
\]

The theorem is certified by a deterministic \(2\)-adic reduction and a literal \(225\times225\) minor with

\[
\boxed{|\det|=2^{30}=1{,}073{,}741{,}824.}
\]

This closes the integral structure behind the previously known ranks

\[
\operatorname{rank}_{\mathbb Q}M=225,
\qquad
\operatorname{rank}_{\mathbb F_2}M=195.
\]

The missing \(30\) dimensions are not a numerical accident: they are pure elementary two-torsion.

---

## Pass 1601 — Integral frame-cokernel Smith theorem

A deterministic \(p\)-adic Smith reduction gives the elementary-divisor counts

```text
p = 2: valuation 0 -> 195 factors
       valuation 1 ->  30 factors
       valuation >=2 -> 0 factors
```

The selected full-rank minor has shape \(225\times225\), 861 nonzero entries, and determinant exactly \(2^{30}\). Therefore no odd factor can occur in the product of the nonzero Smith factors, and the \(2\)-adic lower bound is sharp.

Independent rank checks at

\[
p=3,5,7,11,13,17,19,23,29,31
\]

all return rank \(225\). These checks are redundant once the determinant witness is known, but they are retained as drift detectors.

Since a matrix and its transpose have the same nonzero Smith factors, the same elementary two-torsion occurs in \(\operatorname{coker}(M)\), whose free rank is \(540-225=315\).

---

## Pass 1602 — K4,4 Bockstein torsion theorem

Pass 1536 proved that the \(45\) intrinsic induced \(K_{4,4}\) octets form a basis of the binary dual frame code:

\[
\ker_{\mathbb F_2}M
=
[240,45,16]_2.
\]

Let \(K\in\{0,1\}^{45\times240}\) be the octet/edge incidence matrix. Then

\[
MK^{\mathsf T}=0\pmod2,
\qquad
\operatorname{rank}_2K=45.
\]

The integral Smith theorem supplies the exact Bockstein sequence

\[
\boxed{
0\longrightarrow
\ker_{\mathbb Z}M/2\ker_{\mathbb Z}M
\longrightarrow
\ker_{\mathbb F_2}M
\xrightarrow{\ \beta\ }
\operatorname{Tor}_2(\operatorname{coker}M)
\longrightarrow0,
}
\]

where, for a binary word \(y\) and any \(0/1\) lift \(\widetilde y\),

\[
\boxed{
\beta(y)=\frac{M\widetilde y}{2}\pmod{\operatorname{im}M}.
}
\]

The dimensions are now exact:

\[
\boxed{15\longrightarrow45\longrightarrow30.}
\]

Thus the \(45\) geometric octet checks are not merely parity constraints. Modulo the \(15\)-dimensional reduction of the integral kernel, their Bockstein classes generate the full \((\mathbb Z/2)^{30}\) torsion.

The verifier also checks the quotient directly. With

\[
J=\frac12 MK^{\mathsf T}\in\{0,1\}^{540\times45},
\]

one has

\[
\operatorname{rank}_2[M\mid J]-\operatorname{rank}_2M
=225-195=30.
\]

Therefore the half-incidence classes add exactly thirty independent directions modulo the binary image of \(M\).

---

## Pass 1603 — Half-incidence design and bridge-lattice Smith theorem

The matrix

\[
J=\frac12 MK^{\mathsf T}
\]

is itself a clean incidence object. A frame row and an octet column are incident precisely when the four-edge frame matching meets the sixteen-edge \(K_{4,4}\) support in two edges.

The exact parameters are

\[
\boxed{J\in\{0,1\}^{540\times45},}
\]

\[
\boxed{\text{row degree }6,\qquad\text{column degree }72.}
\]

Let \(A_{45}\) be the octet-overlap graph from Pass 1536, where two octets are adjacent when they share one W33 edge. Then

\[
A_{45}=\operatorname{SRG}(45,32,22,24),
\]

and the half-incidence Gram matrix satisfies the exact identity

\[
\boxed{
J^{\mathsf T}J
=66I+3A_{45}+6\mathbf J.
}
\]

Consequently,

\[
\boxed{
\operatorname{spec}(J^{\mathsf T}J)
=432^1\oplus72^{24}\oplus54^{20}.
}
\]

This gives a new literal bridge between the 540-frame carrier and the 45-octet SRG.

The existing rational cokernel projector and signed-turn bridge are also refined integrally. Define

\[
C=\frac1{16}N^{\mathsf T}(A-12I)(A-2I)N,
\]

\[
F=\frac1{16}d^{\mathsf T}(A-12I)(A-2I)N,
\]

with \(N\) the unsigned point-edge incidence and \(d\) the oriented incidence. Their nonzero Smith forms are

\[
\boxed{
\operatorname{SNF}(C)=1^{10}\oplus3^5,
}
\]

\[
\boxed{
\operatorname{SNF}(F)=1^{10}\oplus3^4\oplus6.
}
\]

Exact determinant witnesses are

\[
|\det C_{15}|=3^5=243,
\qquad
|\det F_{15}|=2\cdot3^5=486.
\]

---

## Pass 1604 — Integral bridge torsion-kernel theorem

The identity

\[
FM^{\mathsf T}=0
\]

means that \(F\) descends to a homomorphism from \(\operatorname{coker}(M^{\mathsf T})\). Its rational rank is \(15\), equal to the free rank of that cokernel, and its target image is torsion-free. Therefore

\[
\boxed{
0\longrightarrow(\mathbb Z/2\mathbb Z)^{30}
\longrightarrow\operatorname{coker}(M^{\mathsf T})
\xrightarrow{\ F\ }\operatorname{im}(F)
\longrightarrow0.
}
\]

So the bridge kills exactly the full elementary two-torsion and is injective on the free part.

This resolves the old mod-2 count:

\[
\dim_{\mathbb F_2}\operatorname{coker}(M^{\mathsf T})=45,
\qquad
\operatorname{rank}_2F=14,
\]

hence the ambient mod-2 kernel has dimension \(31\). It decomposes arithmetically as

\[
\boxed{31=30+1.}
\]

The \(30\) is genuine cokernel torsion. The final \(1\) comes from the single even Smith factor \(6\) in the embedded image lattice of \(F\). It is an embedding-parity defect, not an additional torsion constituent.

---

## Pass 1605 — Resolution boundary and solver guidance

This packet does **not** decide the global nine-cover resolution.

The torsion modes are exact parity invariants of the frame-edge carrier, but the all-one edge vector already lies in \(\operatorname{im}(M^{\mathsf T})\) because exact covers exist. Therefore the \((\mathbb Z/2)^{30}\) sector is not an UNSAT obstruction by itself.

The safe computational use is:

1. treat the thirty Bockstein modes as certified XOR/parity preprocessing;
2. retain the 4,860-variable, 99,909-clause global CNF as the exact decision problem;
3. never promote a finite solver timeout into a SAT or UNSAT claim;
4. keep the 327-orbit exact-cover frontier explicitly non-exhaustive until a global census certificate exists.

---

## Evidence and prior-art boundary

The Smith normal form is the standard integral invariant of an integer matrix and directly controls its cokernel; Peter Sin’s survey, *Smith Normal Forms of Incidence Matrices* (arXiv:1401.8210), is a general external reference for the method. The ATLAS lists characteristic-zero degree-15 and degree-30 representations for \(U_4(2)\cong PSp(4,3)\), which is compatible with the recurring dimensions here. Neither source identifies this particular W33 frame matrix, its \(1^{195}\oplus2^{30}\oplus0^{15}\) Smith form, or the K4,4 Bockstein realization.

The repository owns all W33-specific matrices, ranks, minors, determinants, hashes, and exact-sequence checks in this packet.

The result does not identify the \(30\)-torsion with a specific irreducible modular representation without a separate equivariant MeatAxe or Brauer-character certificate.
