# Part CLXIV — Toroidal Genus / Reptend Bridge

**Date:** 2026-05-02  
**Status:** genus-equation bridge theorem connecting decimal reptends, toroidal polyhedra, and realization counts

---

## 1. Source hints

The uploaded toroidal-triad page centers the dual hole equations

\[
h=\frac{(v-3)(v-4)}{12}
\]

for the Császár vertex-complete side and

\[
h=\frac{(f-4)(f-3)}{12}
\]

for the Szilassi face-complete side.  It also emphasizes the shared accepted residues

\[
v,f\equiv 0,3,4,7 \pmod{12},
\]

the next shared \(h=6\) edge count \(E=66\), and the realization split

\[
5+2=7.
\]

CLXIV connects these directly to the CLXIII decimal/reptend compiler.

---

## 2. W33 form of the hole equation

In W33 notation,

\[
q=3,
\qquad
q+1=4,
\qquad
k=q(q+1)=12.
\]

So both dual hole equations share the same core gate

\[
H(n)=\frac{(n-q)(n-(q+1))}{k}
=\frac{(n-3)(n-4)}{12}.
\]

This is a genus gate: integer values of \(H(n)\) select admissible residues.

---

## 3. Accepted residues as W33 atoms

The integer-genus residues modulo \(12\\) are

\[
\{0,3,4,7\}\pmod{12}.
\]

Using \(12\) instead of \(0\), this is

\[
\{3,4,7,12\}.
\]

But these are exactly

\[
\{q,q+1,\Phi_6,k\}.
\]

So the hole equation selects:

\[
3=q,
\]

the q-axis root;

\[
4=q+1,
\]

the tetrahedral seed;

\[
7=\Phi_6,
\]

the first toroidal/cyclic value;

and

\[
12=k,
\]

the full mod-12 closure.

---

## 4. CRT interpretation

Because

\[
12=3\cdot4=q(q+1),
\]

the hole equation is a Chinese-remainder gate over moduli \(3\) and \(4\).

The two zero roots have coordinates

\[
3\mapsto(0\bmod3,3\bmod4),
\]

and

\[
4\mapsto(1\bmod3,0\bmod4).
\]

The two recombinations are:

\[
(0,0)\mapsto12,
\]

the full closure, and

\[
(1,3)\mapsto7,
\]

the toroidal solution.

Thus

\[
\boxed{7=\Phi_6}
\]

is the nontrivial CRT recombination of the two zero roots \(3\) and \(4\).

---

## 5. Genus values

At the selected residues:

\[
H(3)=0,
\]

\[
H(4)=0,
\]

\[
H(7)=1,
\]

and

\[
H(12)=6=2q.
\]

Therefore:

- \(4\) is the tetrahedron / genus-zero seed;
- \(7=\Phi_6\) is the genus-one torus solution;
- \(12=k\) is the next closure with genus \(6=2q\).

---

## 6. Polyhedron table

\[
\begin{array}{c|c|c|c|c}
\text{object} & V & E & F & h\\
\hline
\text{tetrahedron} & 4 & 6 & 4 & 0\\
\text{Csasz\'ar} & 7 & 21 & 14 & 1\\
\text{Szilassi} & 14 & 21 & 7 & 1\\
\text{next vertex-complete} & 12 & 66 & 44 & 6\\
\text{next face-complete} & 44 & 66 & 12 & 6
\end{array}
\]

The next \(h=6\) solutions preserve the edge count

\[
E=\binom{12}{2}=66,
\]

while swapping vertices and faces.

---

## 7. Realization bridge

The toroidal-triad page highlights

\[
5+2=7.
\]

CLXIV identifies this as

\[
5+2=\Phi_6.
\]

Here

\[
5=J
\]

is the stabilizer residue from CLXI/CLXII, and

\[
2=q-1
\]

is the binary duality count.

Thus the realization split is

\[
\text{Csasz\'ar realizations} + \text{Szilassi realizations}
= J+(q-1)=\Phi_6.
\]

So the total realization closure is the same number as:

- the toroidal genus-one residue,
- the decimal cyclic denominator,
- the \(\Phi_6\) threshold field.

---

## 8. Decimal bridge

CLXIII showed

\[
\frac17=0.\overline{142857}
\]

is the base-\(\Phi_4\) expansion of \(1/\Phi_6\), with period

\[
2q=6.
\]

CLXIV adds that the genus equation selects the same \(7=\Phi_6\) as its first nonzero toroidal solution.

So

\[
7
\]

is simultaneously:

1. the cyclic decimal denominator,
2. the toroidal genus-one CRT residue,
3. the realization closure \(5+2\),
4. the \(\Phi_6\) threshold field.

---

## 9. Theorem statement

**The dual toroidal hole equations are CRT gates over the denominator \(k=12\).**  The equation

\[
H(n)=\frac{(n-3)(n-4)}{12}
\]

is integral exactly at residues

\[
\{3,4,7,12\}=\{q,q+1,\Phi_6,k\}.
\]

The \(h=1\) torus solution \(7\) is the nontrivial Chinese-remainder recombination of the zero roots \(3\) and \(4\).  The realization split

\[
5+2=7
\]

is the same \(\Phi_6\) value, with \(5\) the stabilizer residue and \(2=q-1\) the binary duality count.

---

## 10. Regression status

Local validation of the CLXIV test file:

```text
7 passed in 0.04s
```

The tests verify:

1. accepted hole-equation residues \(\{3,4,7,12\}\),
2. genus values \(0,0,1,6\),
3. CRT gate coordinates for roots, torus, and closure,
4. realization split \(5+2=7\),
5. shared edges and dual swap,
6. flag counts \(42,84\),
7. audit-level consistency.

---

## 11. Next move

The next target is to combine the CRT gate and decimal reptend into one mod-12 wheel:

\[
\text{hole gate residues } \{3,4,7,12\}
\]

and

\[
\text{decimal partition } \{1,2,4,5,8\}\sqcup\{7\}\sqcup\{3,6,9\}.
\]

The likely hidden object is a four-sector mod-12 wheel whose sector boundaries are \(3,6,9,12\), whose toroidal admissible residues are \(3,4,7,12\), and whose cyclic denominator is \(7=\Phi_6\).
