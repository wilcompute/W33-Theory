# BT1450--BT1452: Otto quartic replication, closure schedule, and D4/Clifford lift

## BT1450 — Otto quartic and formula acquisition packet

The public source situation is now encoded conservatively.  The SCIRP/ResearchGate pages expose the paper and surrounding prose, but equations (49), (50), (64), (65), and (66) still require rendered PDF/image transcription.  However, Otto's related quartic work exposes the varied golden quartic

\[
g(x)=x^4-x^3-(4-\phi^2)x^2+(4-\phi^2)x+1,
\]

where

\[
\phi=\frac{\sqrt5-1}{2}.
\]

The coefficient obeys

\[
4-\phi^2=3+\phi=\sqrt{13+\phi^5}=3.618033988749895\ldots
\]

The reproduced roots are approximately

\[
-1.8516617610676734,
\quad -0.2283085816032673,
\quad 1.4619363539210459,
\quad 1.618033988749895.
\]

The last root is the ordinary golden ratio \(1/\phi\).  This gives a reproducible Python analogue to Otto's older QBASIC-style numerical workflow while the missing equation images remain gated.

## BT1451 — closure schedule compiler

The retwined closure decoder is now compiled into a symbolic schedule.  For each of 12 closure strands, the schedule runs:

1. active closure tick;
2. guard orientation pair;
3. retwined CSS frame update;
4. X/Z syndrome readout.

The schedule has

\[
12+12+12+12=48
\]

steps and covers active closure columns \(14s+13\) and the full guard tail \(216,\ldots,239\).  The three fixed-hexagon opposite-pair channels are balanced four times each.

## BT1452 — D4/Clifford closure lift

The closure state space is represented as

\[
12=4\text{ side/orientation branches}\times3\text{ opposite-pair phases}.
\]

The Szilassi/Frobenius closure action is modeled by

\[
\tau_4: (b,p)\mapsto (b\oplus2,p),
\]

while the D4 injection shear is

\[
S:(b,p)\mapsto (b,p+b\bmod3).
\]

The important result is not bare commutation:

\[
\tau_4S\ne S\tau_4.
\]

But the conjugate

\[
\tau_4S\tau_4^{-1}
\]

is still an order-3 legal shear.  The generated closure/shear layer has order

\[
18
\]

with order profile

\[
1^1,\quad2^3,\quad3^8,\quad6^6.
\]

So the correct compatibility statement is: the Szilassi closure does not commute with the D4 shear as a bare symmetry, but it is compatible as a retwined/conjugating Clifford-frame operation.

## Current refined closure law

\[
\boxed{
\text{odd half-turn}
\to
\tau_4\text{ fixed-face closure}
\to
\text{symbolic schedule}
\to
\text{retwined/conjugated D4 shear}
}
\]
