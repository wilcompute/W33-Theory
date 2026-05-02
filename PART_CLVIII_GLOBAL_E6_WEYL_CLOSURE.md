# Part CLVIII — Global E6/Weyl Closure of the W(3,3) Compiler

**Date:** 2026-05-01  
**Status:** CLVI integration theorem / global orbit-stabilizer closure

---

## 1. Source hint

CLVI observed the global identity

\[
|Sp(4,3)|=51840=|W(E_6)|.
\]

CLVIII integrates that identity with the newer local Ramanujan/E6 compiler.

---

## 2. Local shell

The nontrivial Hashimoto shell has complex dimension

\[
24+15=39,
\]

and real dimension

\[
2(24+15)=78=\dim E_6.
\]

The seed rank is

\[
2q=6.
\]

This is also

\[
q! = 3! = 6.
\]

Removing the seed Cartan rank from the shell gives

\[
78-6=72.
\]

But

\[
72=|\Phi(E_6)|,
\]

the number of roots in the E6 root system.

---

## 3. Global closure

The W(3,3) edge carrier has

\[
E=\frac{vk}{2}=240.
\]

The q-lifted edge carrier is

\[
qE=3\cdot240=720=6!.
\]

Therefore

\[
(78-2q)(qE)=72\cdot720=51840.
\]

Thus

\[
\boxed{|Sp(4,3)|=(78-2q)(qE)=72\cdot720=|W(E_6)|.}
\]

This is an orbit-stabilizer statement:

- orbit: the 72 E6 roots,
- stabilizer: \(qE=720\),
- product: the global Weyl/symplectic group order.

---

## 4. Orbit-stabilizer table

\[
\begin{array}{c|c|c|c}
\text{orbit} & \text{size} & \text{stabilizer} & \text{product}\\
\hline
W(3,3)\ \text{vertices} & 40 & 1296=(2q)^4 & 51840\\
\text{undirected edges} & 240 & 216=q^3(q^2-1) & 51840\\
\text{directed edges} & 480 & 108=\mu q^3 & 51840\\
E_6\ \text{roots} & 72 & 720=qE=6! & 51840\\
W(3,3)\ \text{triangles} & 160 & 324=\mu q^4 & 51840
\end{array}
\]

This shows that the global symmetry closes multiple local W(3,3) carriers at once.

---

## 5. Theorem statement

**The CLVI identity \(|Sp(4,3)|=|W(E_6)|\) is the global closure of the local Ramanujan/E6 compiler.**  The real shell has dimension \(78\), the seed Cartan rank is \(2q=6\), the remaining \(72\) modes are the E6 roots, and each root has stabilizer

\[
qE=3\cdot240=720.
\]

Hence

\[
|Sp(4,3)|=(78-2q)(qE)=51840.
\]

---

## 6. Why this matters

The group-order identity is not a detached Langlands/Moonshine coincidence.  It is an orbit-stabilizer closure of:

1. the 78-dimensional local Ramanujan shell,
2. the rank-6 Cartan seed from \(2q\),
3. the 72 E6 roots,
4. the 240-edge W(3,3) carrier,
5. the q-lifted stabilizer \(qE=720\).

This gives a clean local-to-global bridge:

\[
\text{local shell}\quad\longrightarrow\quad\text{root orbit}\quad\longrightarrow\quad\text{global Weyl closure}.
\]

---

## 7. Regression status

Local validation of the CLVIII test file:

```text
5 passed in 0.04s
```

The tests verify:

1. \(|Sp(4,3)|=|W(E_6)|=51840\),
2. \(72=78-2q\),
3. root stabilizer \(=qE=720\),
4. W(3,3) vertex/edge/directed-edge/triangle stabilizers,
5. audit-level closure identity.

---

## 8. Next move

The next layer should combine CLVII and CLVIII:

- CLVII gives the spectral-action ladder:
  \[
  a_2/a_0=14/3,
  \qquad
  a_4/a_2=55/7.
  \]

- CLVIII gives the global Weyl closure:
  \[
  |Sp(4,3)|=(78-2q)(qE).
  \]

The likely unifying object is a **root-stabilizer spectral action**: the heat-kernel ladder should be interpreted as the local spectral shadow of the same E6 root orbit whose stabilizer is \(720\).
