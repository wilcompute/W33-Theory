# Part LXXV — Target-Side SRG Signatures

**Status:** theorem-grade structural extension  
**Date:** April 27, 2026

Parts LXXIII–LXXIV identify the spread/anti-line measurement architecture:

\[
\text{mean}+\mathrm{ETF}(36,15)+2\cdot\text{two-distance frame}(45,24).
\]

This part identifies the strongly regular graphs carried by those target-side feature systems.

## 1. Spread ETF sign graphs

The centered spread columns form an equiangular tight frame `ETF(36,15)`. Taking positive inner product as adjacency gives

\[
\boxed{\mathrm{SRG}(36,15,6,6).}
\]

Taking negative inner product as adjacency gives the complement

\[
\boxed{\mathrm{SRG}(36,20,10,12).}
\]

Thus the spread ETF target geometry is exactly the 36-spread SRG pair.

## 2. Anti-line quotient graphs

The 90 anti-line feature vectors collapse to 45 duplicate pairs. Each duplicate pair consists of two disjoint anti-lines.

After quotienting by duplicates, the 45 unique feature vectors have off-diagonal inner products

\[
\boxed{\frac35,\qquad -\frac{12}{5}.}
\]

Positive inner product gives

\[
\boxed{\mathrm{SRG}(45,32,22,24).}
\]

Negative inner product gives the complement

\[
\boxed{\mathrm{SRG}(45,12,3,3).}
\]

## 3. Transport graph recovery

The graph

\[
\boxed{\mathrm{SRG}(45,32,22,24)}
\]

is the 45-point transport graph from earlier W(3,3) work. It now has a new origin:

\[
\boxed{
\text{45 transport graph}
=
\text{positive inner-product graph of the anti-line feature quotient}.
}
\]

This consolidates the 45-point transport object into the measurement-frame architecture. It is not external to the spread/anti-line story; it is the target-side quotient of the anti-line channel.

## 4. Unified picture

\[
\boxed{
\text{spread channel}
\Rightarrow
\mathrm{ETF}(36,15)
\Rightarrow
\mathrm{SRG}(36,15,6,6)
}
\]

and

\[
\boxed{
\text{anti-line channel}
\Rightarrow
2\cdot45\text{ feature quotient}
\Rightarrow
\mathrm{SRG}(45,32,22,24).
}
\]

Thus the 36-spread and 45-transport geometries are both target-side signatures of the same Parseval measurement frame.

## 5. The structural compression

The core carrier sequence is now:

\[
\boxed{
W(3,3)\text{ line module}
\to
\text{Parseval measurement frame}
\to
\mathrm{ETF}(36,15)
\oplus
\mathrm{Transport}(45,32,22,24).
}
\]

This suggests that the previously separate spread sector and 45-transport sector are two complementary target geometries of one measurement machine.
