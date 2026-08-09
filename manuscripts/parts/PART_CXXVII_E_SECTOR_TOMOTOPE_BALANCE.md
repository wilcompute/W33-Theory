# Part CXXVII — E-Sector Tomotope Balance in the S4 Relative-Cycle Law

**Status:** theorem-grade structural extension  
**Date:** April 29, 2026

Part CXXIV left one place where the pair-overlap law was not decided by the relative `S4` cycle type alone: the `E/E` relative 3-cycle layer.  The unresolved-looking split is actually highly structured once the two chiral sectors are kept together.

This part extracts the exact balance law hiding in that split.

## 1. Input from CXXIV

The even frame sectors are

```text
E+ : 12 frames
E- : 12 frames
```

For same-chirality `E/E` pairs, the relative 3-cycle layer splits as

```text
18 four-overlap pairs,
30 one-overlap pairs.
```

This happens separately in `E+` and in `E-`.

For opposite-chirality `E+/E-` pairs, the relative 3-cycle layer splits as

```text
60 four-overlap pairs,
36 one-overlap pairs.
```

## 2. The 192-pair 3-cycle layer

Within one even chirality sector, there are 12 frames.  For a fixed source frame, the even skeleton has 8 relative 3-cycles, so the unordered same-sector 3-cycle count is

\[
\frac{12\cdot 8}{2}=48.
\]

There are two same-chirality sectors, hence

\[
48+48=96
\]

same-chirality 3-cycle pairs.

Between `E+` and `E-`, the 3-cycle layer is bipartite, so the count is

\[
12\cdot 8=96.
\]

Therefore the full even-sector relative 3-cycle layer has

\[
\boxed{96+96=192}
\]

pairs.

This is the first clean appearance, inside the MUB-frame overlap law itself, of the `192` tomotope/flag count motif.

## 3. Exact 96/96 overlap balance

Aggregate the CXXIV splits over the whole even sector:

Same chirality:

\[
2(18,30)=(36,60).
\]

Opposite chirality:

\[
(60,36).
\]

Total:

\[
(36,60)+(60,36)=(96,96).
\]

So the full `E`-sector relative 3-cycle layer is perfectly balanced:

\[
\boxed{
192\text{ relative-3-cycle pairs}
=96\text{ four-overlap}+96\text{ one-overlap}.
}
\]

## 4. The 24-dimensional chiral imbalance

The same/opposite contrast is not noise.  It is exactly a `24`-unit imbalance:

\[
60-36=24.
\]

Thus chirality exchange swaps the pair counts by the W33 self-dual block size:

```text
same chirality     : 36 four, 60 one
opposite chirality : 60 four, 36 one
imbalance          : 24
```

Equivalently, in the 3-cycle layer, chirality flip exchanges the two counts around the balanced midpoint `48`:

\[
36=48-12,
\qquad
60=48+12.
\]

The total imbalance between four-overlap and one-overlap is therefore

\[
(60-36)=24.
\]

## 5. Mean-overlap form

For same chirality, the mean total overlap on the relative 3-cycle layer is

\[
\frac{18\cdot 4+30\cdot 1}{48}=\frac{17}{8}.
\]

For opposite chirality, it is

\[
\frac{60\cdot 4+36\cdot 1}{96}=\frac{23}{8}.
\]

The two values are centered at

\[
\frac{5}{2}
\]

with deviation

\[
\frac{3}{8}.
\]

Thus the relative 3-cycle layer carries the affine chirality law

\[
\boxed{
\langle\operatorname{ov}\rangle_{3\text{-cycle}}
=\frac{5}{2}-\frac{3}{8}\chi,
\qquad
\chi=+1\text{ for same chirality},\quad \chi=-1\text{ for opposite chirality}.
}
\]

## 6. Theorem CXXVII

**Theorem CXXVII (E-Sector Tomotope Balance).**  In the complete two-qutrit stabilizer MUB-frame overlap geometry, the even-sector relative 3-cycle layer has exactly 192 pairs and splits evenly into 96 four-overlap pairs and 96 one-overlap pairs.  The same/opposite chirality refinement is

\[
\boxed{
\begin{array}{c|cc}
&4\text{-overlap}&1\text{-overlap}\\
\hline
\text{same chirality}&36&60\\
\text{opposite chirality}&60&36
\end{array}}
\]

so chirality exchange produces a `24`-unit imbalance, exactly the `24`-dimensional W33 block.

## 7. Meaning

The CXXIV phrase

```text
where cycle type alone does not decide the overlap, the remaining split is exactly the lift-phase/chirality data
```

can now be sharpened:

```text
inside the E/E 3-cycle layer, binary-octahedral chirality produces a 192-pair tomotope-scale packet, balanced as 96/96, with a 24-dimensional chiral imbalance.
```

So the `3-cycle ambiguity` is not an imperfection in the S4 law.  It is the place where the binary-octahedral lift injects the W33 `24` block into the MUB-frame overlap geometry.

## 8. Paper insertion point

This belongs immediately after Part CXXIV's same/opposite chirality split.  It converts the remaining fine split into a clean theorem and connects the MUB-frame law to the existing `96/192` tomotope motif without adding any new assumptions.

The accompanying regression tests are in:

```text
tests/test_e_sector_tomotope_balance_cxxvii.py
```
