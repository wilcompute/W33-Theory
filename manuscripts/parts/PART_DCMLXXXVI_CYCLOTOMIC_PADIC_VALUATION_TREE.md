# Part DCMLXXXVI (986) - Cyclotomic p-adic Valuation Tree

**Date:** 2026-05-19
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED THEOREM / LOCAL DENSITY LAW

---

## Why this part exists

Part DCMLXXXV promoted the cyclotomic defect set from a numerical anomaly list
to an explicit Eisenstein/Hensel residue theorem modulo \(p^2\).  The next
natural step is to push that local theorem all the way up the \(p\)-adic tower.

The result is sharper than merely saying that the bad classes lift:

- for every split prime \(p\equiv1\pmod3\), there are exactly two defect
  branches modulo \(p^n\) for every \(n\ge1\);
- their \(p\)-adic measure is exactly computable;
- and the first cube defect \(343=7^3\) is the first visible depth-3 node on
  the \(p=7\) branch.

---

## The valuation-tree theorem

For a split prime \(p\equiv1\pmod3\), let

\[
\Phi_3(q)=q^2+q+1,
\qquad
\Phi_6(q)=q^2-q+1.
\]

Then for every \(n\ge1\):

1. the congruence \(\Phi_3(q)\equiv0\pmod{p^n}\) has exactly two residue
   classes modulo \(p^n\);
2. the congruence \(\Phi_6(q)\equiv0\pmod{p^n}\) also has exactly two residue
   classes modulo \(p^n\), namely the negatives of the \(\Phi_3\) classes;
3. each class lifts uniquely from level \(p^n\) to level \(p^{n+1}\).

So each split prime contributes **two infinite Hensel branches**.

---

## Proof skeleton

The derivative

\[
f'(x)=2x+1
\]

does not vanish at a nontrivial cube root modulo \(p\) for \(p\neq3\).  Hence
every root lifts uniquely at each stage by Hensel's lemma.  Since there are two
roots modulo \(p\), there are two roots modulo every \(p^n\).

The \(\Phi_6\) branch follows from

\[
\Phi_6(q)=\Phi_3(-q).
\]

---

## Local p-adic densities

Because there are exactly two bad classes modulo \(p^n\), the \(p\)-adic measure
of the divisibility event is

\[
\boxed{
\mu\bigl(v_p(\Phi_3(q))\ge n\bigr)=\mu\bigl(v_p(\Phi_6(q))\ge n\bigr)=\frac{2}{p^n}.
}
\]

Therefore the exact valuation law is

\[
\boxed{
\mu\bigl(v_p(\Phi_3(q))=n\bigr)=\mu\bigl(v_p(\Phi_6(q))=n\bigr)=\frac{2(p-1)}{p^{n+1}}.
}
\]

So the valuation depth decays geometrically along each split-prime tree.

---

## First trees

For \(p=7\), the first five levels are:

- \(\Phi_3\): roots modulo \(7^n\) begin
  \(\{2,4\}\), \(\{18,30\}\), and continue uniquely upward;
- \(\Phi_6\): roots are the negatives,
  \(\{3,5\}\), \(\{19,31\}\), and continue uniquely upward.

For \(p=13\), the first nontrivial lifted classes are

\[
\Phi_3: \{22,146\}\pmod{13^2},
\qquad
\Phi_6: \{23,147\}\pmod{13^2}.
\]

For \(p=19\), they are

\[
\Phi_3: \{68,292\}\pmod{19^2},
\qquad
\Phi_6: \{69,293\}\pmod{19^2}.
\]

---

## The Heawood cube as the first depth-3 node

The first visible cube defect is

\[
\Phi_3(18)=7^3,
\qquad
\Phi_6(19)=7^3.
\]

So on the \(p=7\) tree,

\[
v_7\bigl(\Phi_3(18)\bigr)=3,
\qquad
v_7\bigl(\Phi_6(19)\bigr)=3.
\]

This is why the earlier residue theorem's first cube defect is not an accident:
it is literally the first depth-3 node on the split-prime \(7\)-branch.

---

## What is now exact

The promoted exact statements are:

1. each split prime \(p\equiv1\pmod3\) contributes two infinite Hensel branches;
2. the \(\Phi_6\) branches are negatives of the \(\Phi_3\) branches;
3. the divisibility measure is exactly \(2/p^n\);
4. the exact valuation law is \(2(p-1)/p^{n+1}\);
5. the first depth-3 node is the Heawood cube \(343=7^3\).

---

## Correct status

\[
\boxed{
\text{The cyclotomic defect set is not only explicit modulo }p^2\text{; it forms a full }p\text{-adic valuation tree with exact local measure.}
}
\]

The next remaining frontier is global: connect this local valuation tree and
the isolated cube witness to a fully proved global perfect-power theorem for
\(x^2\pm x+1=y^n\).

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_valuation_tree.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_valuation_tree.json`
- Result: `PART_DCMLXXXVI_cyclotomic_padic_valuation_tree_results.json`
