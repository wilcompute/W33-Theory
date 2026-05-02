# Part CLIX — Root-Stabilizer Spectral Action

**Date:** 2026-05-02  
**Status:** CLVII/CLVIII fusion theorem

---

## 1. What CLIX fuses

CLVII gave the spectral-action ladder:

\[
a_0=480,
\qquad
a_2=2240,
\qquad
a_4=17600,
\]

with

\[
\frac{a_2}{a_0}=\frac{14}{3},
\qquad
\frac{a_4}{a_2}=\frac{55}{7}.
\]

CLVIII gave the global E6/Weyl closure:

\[
|W(E_6)|=|Sp(4,3)|=51840=(78-2q)(qE)=72\cdot720.
\]

CLIX shows these are one structure.

---

## 2. Normalize the spectral action by the global Weyl group

Divide each heat-kernel coefficient by

\[
|W(E_6)|=51840.
\]

Then

\[
\frac{a_0}{|W(E_6)|}
=\frac{480}{51840}
=\frac{1}{108}.
\]

Since

\[
108=\mu q^3,
\]

this is the inverse directed-edge stabilizer.

Next,

\[
\frac{a_2}{|W(E_6)|}
=\frac{2240}{51840}
=\frac{7}{162}.
\]

Since

\[
7=\Phi_6,
\qquad
162=2q^4,
\]

this is

\[
\frac{\Phi_6}{2q^4}.
\]

Finally,

\[
\frac{a_4}{|W(E_6)|}
=\frac{17600}{51840}
=\frac{55}{162}.
\]

Since

\[
55=\binom{k-1}{2},
\]

this is

\[
\frac{\binom{k-1}{2}}{2q^4}.
\]

---

## 3. Interpretation

The normalized coefficients are therefore:

\[
\begin{array}{c|c|c}
\text{coefficient} & \text{global normalized value} & \text{meaning}\\
\hline
a_0 & 1/108 & \text{directed-edge carrier / stabilizer}\\
a_2 & 7/162 & \Phi_6\text{ threshold field over }2q^4\\
a_4 & 55/162 & \text{Hashimoto radial wedge over }2q^4
\end{array}
\]

The heat-kernel ladder is thus the local spectral shadow of the global root-stabilizer closure.

---

## 4. Ratio preservation

Because all coefficients are normalized by the same global order, the original spectral-action ratios survive:

\[
\frac{a_2/|W(E_6)|}{a_0/|W(E_6)|}
=\frac{a_2}{a_0}
=\frac{14}{3},
\]

and

\[
\frac{a_4/|W(E_6)|}{a_2/|W(E_6)|}
=\frac{a_4}{a_2}
=\frac{55}{7}.
\]

So the global Weyl normalization does not destroy the spectral-action ladder; it explains the stabilizer units in which that ladder lives.

---

## 5. Higgs quartic

The Higgs quartic remains the inverse radial-threshold step:

\[
\lambda_H
=\frac{7}{55}
=\frac{\Phi_6}{\binom{k-1}{2}}.
\]

In CLIX language, this is the ratio of the globally normalized \(a_2\) and \(a_4\) numerators:

\[
\lambda_H
=\frac{7/162}{55/162}.
\]

---

## 6. Theorem statement

**The Seeley--DeWitt spectral action is normalized by the global E6/Weyl root-stabilizer closure.** Dividing by

\[
|W(E_6)|=51840
\]

gives

\[
\frac{a_0}{|W|}=\frac1{108},
\qquad
\frac{a_2}{|W|}=\frac{\Phi_6}{2q^4}=\frac7{162},
\qquad
\frac{a_4}{|W|}=\frac{\binom{k-1}{2}}{2q^4}=\frac{55}{162}.
\]

Thus \(a_0\) is the directed-edge carrier, \(a_2\) is the threshold field, and \(a_4\) is the radial wedge, all expressed in the same global root-stabilizer units.

---

## 7. Regression status

Local validation of the CLIX test file:

```text
6 passed in 0.05s
```

The tests verify:

1. global-normalized coefficients \(1/108,7/162,55/162\),
2. \(a_0\) as inverse directed-edge stabilizer,
3. \(a_2,a_4\) as threshold/radial-wedge over \(2q^4\),
4. ratio preservation,
5. \(2q^4\) as half the triangle stabilizer,
6. audit-level consistency.

---

## 8. Next move

The next object should explain why the root stabilizer

\[
qE=720
\]

is also

\[
6!
\]

and how that factorial stabilizer acts on the mixer/projection grammar.  This likely connects the original seed

\[
q!=2q
\]

with the global stabilizer

\[
(2q)! = 6! = 720.
\]
