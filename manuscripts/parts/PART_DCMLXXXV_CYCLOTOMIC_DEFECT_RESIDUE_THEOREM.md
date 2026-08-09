# Part DCMLXXXV (985) - Cyclotomic Defect Residue Theorem

**Date:** 2026-05-19
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED THEOREM / AUDITABLE CLASSIFIER

---

## Why this part exists

The new arithmetic-semigroup layer exposed the strongest robust family on the
shift tower:

\[
\Phi_3(q)=q^2+q+1,
\qquad
\Phi_6(q)=q^2-q+1,
\]

with the radical ladder

\[
\operatorname{rad}(\Phi_3(q))=\Phi_6(q+1),
\qquad
\operatorname{rad}(\Phi_6(q))=\Phi_3(q-1)
\]

whenever the relevant cyclotomic values are squarefree.

The next question is not whether there are defects, but whether the defect set
has an exact arithmetic description.  This part promotes the answer:

- yes, the defect locus is explicit;
- yes, it is controlled by split primes in the Eisenstein/discriminant-\(-3\)
  world;
- yes, the first visible defect is the Heawood cube
  \(343=7^3\);
- and on the checked window \(q\le 1000\), the classifier is exact.

Even better, the whole story sits on an Eisenstein norm factorization:

\[
\boxed{\Phi_3(q)=N(q-\omega),\qquad \Phi_6(q)=N(q+\omega)}
\]

in \(\mathbb Z[\omega]\), where \(\omega^2+\omega+1=0\).

---

## Eisenstein norm backbone

In the Eisenstein integers,

\[
N(a+b\omega)=a^2-ab+b^2.
\]

Substituting \((a,b)=(q,-1)\) and \((q,1)\) gives

\[
N(q-\omega)=q^2+q+1=\Phi_3(q),
\qquad
N(q+\omega)=q^2-q+1=\Phi_6(q).
\]

So the cyclotomic pair is not merely analogous to Eisenstein arithmetic; it is
literally an Eisenstein norm pair.  The split-prime defect locus is therefore
the local statement that a split Eisenstein prime above \(p\equiv1\pmod3\)
divides \(q\mp\omega\) to order at least two.

---

## The theorem

Let

\[
\Phi_3(q)=q^2+q+1,
\qquad
\Phi_6(q)=q^2-q+1.
\]

For any split prime \(p\equiv1\pmod 3\), let
\(U_{3,p^2}^{\times}\subset(\mathbb Z/p^2\mathbb Z)^\times\)
denote the two nontrivial order-\(3\) units modulo \(p^2\).

\[
\boxed{
p^2\mid\Phi_3(q)
\iff
q\bmod p^2\in U_{3,p^2}^{\times}.
}
\]

Equivalently, \(q\) lands in one of the two Hensel-lifted roots of

\[
x^2+x+1\equiv0\pmod{p^2}.
\]

Likewise,

\[
\boxed{
p^2\mid\Phi_6(q)
\iff
-q\bmod p^2\in U_{3,p^2}^{\times},
}
\]

so the \(\Phi_6\) defect classes are exactly the negatives of the
\(\Phi_3\) classes.

Thus the nonsquarefree defect locus of the radical ladder is the union over all
split primes \(p\equiv1\pmod3\) of these lifted order-\(3\) unit classes.

---

## Proof skeleton

### 1. Cyclotomic factorization

For \(x\neq1\),

\[
x^3-1=(x-1)(x^2+x+1).
\]

Hence

\[
x^2+x+1\equiv0\pmod{p^2}
\]

iff \(x\) is a nontrivial cube root of unity modulo \(p^2\).

### 2. Split-prime condition

The polynomial \(x^2+x+1\) has discriminant \(-3\).  Modulo an odd prime
\(p\neq3\), it has roots iff \(-3\) is a square modulo \(p\), equivalently iff

\[
p\equiv1\pmod3.
\]

So only split Eisenstein primes can support defects.

### 3. Hensel lift

If \(r\) is a root mod \(p\), then

\[
f(x)=x^2+x+1,
\qquad
f'(x)=2x+1.
\]

At a nontrivial cube root, \(f'(r)\not\equiv0\pmod p\) for \(p\neq3\), so each
root lifts uniquely from mod \(p\) to mod \(p^2\).

Therefore each split prime contributes exactly two classes modulo \(p^2\).

### 4. The \(\Phi_6\) branch

Since

\[
(-q)^2+(-q)+1=q^2-q+1=\Phi_6(q),
\]

the \(\Phi_6\) defect classes are exactly the negatives of the
\(\Phi_3\) classes.

### 5. Order-3 unit formulation

Because \((\mathbb Z/p^2\mathbb Z)^\times\) is cyclic of order
\(p(p-1)\), a primitive root \(g\) modulo \(p^2\) generates the two nontrivial
cube roots:

\[
g^{p(p-1)/3},
\qquad
g^{2p(p-1)/3}.
\]

These are exactly the two Hensel-lifted roots of \(x^2+x+1\equiv0\pmod{p^2}\).

---

## First residue classes

The first split primes produce the exact tables

\[
p=7:
\quad
\Phi_3\text{-classes }\{18,30\}\pmod{49},
\quad
\Phi_6\text{-classes }\{19,31\}\pmod{49};
\]

\[
p=13:
\quad
\Phi_3\text{-classes }\{22,146\}\pmod{169},
\quad
\Phi_6\text{-classes }\{23,147\}\pmod{169};
\]

\[
p=19:
\quad
\Phi_3\text{-classes }\{68,292\}\pmod{361},
\quad
\Phi_6\text{-classes }\{69,293\}\pmod{361}.
\]

These agree exactly with the code-generated order-\(3\) unit classes.

---

## The first cube defect

The first defect is

\[
\Phi_3(18)=343=7^3,
\qquad
\Phi_6(19)=343=7^3.
\]

This is not an arbitrary early exception.  It is the first split-prime square
class for \(p=7\), and it is simultaneously the first point at which the
cyclotomic value becomes a visible perfect power.  In the current local
terminology, this is the **Heawood cube defect**.

---

## Perfect-power isolation on the scanned window

The larger scan to

\[
q\le10^5
\]

finds exactly one perfect-power hit on each branch:

\[
\Phi_3(18)=7^3,
\qquad
\Phi_6(19)=7^3.
\]

No further perfect powers occur in that window.

So, at least on the checked range, the visible cube defect is isolated.

---

## What is now exact

The promoted exact statements are:

1. the radical-ladder defect locus is the union of lifted split-prime
   \(p^2\)-residue classes;
2. those classes are exactly the nontrivial order-\(3\) units modulo \(p^2\);
3. the \(\Phi_6\) classes are negatives of the \(\Phi_3\) classes;
4. every repeated defect prime seen on the checked window lies in the split
   class \(p\equiv1\pmod3\);
5. the first and only perfect-power witness seen on \(q\le10^5\) is the
   Heawood cube \(343=7^3\).

There is also a density statement. Since each split prime \(p\equiv1\pmod3\)
contributes exactly two forbidden residue classes modulo \(p^2\), and these
local conditions combine independently by the Chinese remainder theorem, the
defect locus has natural density

\[
\boxed{
\delta_{\mathrm{defect}}
=1-\prod_{p\equiv1\ (3)}\left(1-\frac{2}{p^2}\right)
\approx 0.06516.
}
\]

The empirical scans on both branches match this value closely.

---

## Correct status

\[
\boxed{
\text{The cyclotomic defect set is no longer a numerical anomaly list; it is an explicit Eisenstein/Hensel residue theorem.}
}
\]

The remaining non-computational frontier is to connect the observed perfect-power
isolation to a classical global theorem for
\(x^2\pm x+1=y^n\), rather than only to the local residue classifier and the
large finite scan.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_defect_residue_classifier.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_defect_residue_classifier.json`
- Result: `PART_DCMLXXXV_cyclotomic_defect_residue_theorem_results.json`
