# BT1447--BT1449: Otto equation extraction, canonical Fano map, and retwined closure decoder

## BT1447 — actual equation extraction ledger

The accessible SCIRP HTML for Otto's paper exposes equation numbers and prose contexts for equations (49), (50), (64), (65), and (66), but not machine-readable formula bodies.  The relevant visible contexts are:

- (49): golden-mean representation of the anomalous part of the electron g-factor;
- (50): series expansion claimed accurate to the tenth decimal place;
- (64): icosahedron-based numerical interpretation of the anomalous part;
- (65): power of the ratio of 12 slings to 13 half-turns;
- (66): modified Schwinger alpha/pi approximation from a Moebius calculation.

The extraction ledger therefore keeps these equations blocked until the rendered formulas are transcribed from the PDF or images.

## BT1448 — fixed-hexagon to Fano canonical map

BT1443 gave a valid ordered bijection

\[
12(13+1)=168=21\cdot8.
\]

BT1448 upgrades the ordering by using the Szilassi/Frobenius closure seed.  The fixed face is

\[
4,
\]

and the canonical involution is

\[
\tau_4(x)=-x+1\pmod 7.
\]

Therefore the canonical face order is

\[
[4,0,1,2,6,3,5],
\]

with transposition pairs

\[
(0,1),\quad(2,6),\quad(3,5).
\]

The fixed hexagon supplies opposite vertex pairs

\[
(11,10),\quad(9,8),\quad(12,13).
\]

The map verifies 21 Fano flags, 12 strands, 168 active bins, 12 closure ticks, and complete coverage of all 24 guard bins.

## BT1449 — retwined closure decoder

The closure tick was inserted into the BT1425 retwined CSS frame rule.  The tested sample consists of:

\[
12\text{ closure ticks},
\qquad
24\text{ active value trials},
\qquad
48\text{ guard value trials},
\qquad
72\text{ total trials}.
\]

The retwined CSS ranks remain

\[
\operatorname{rank}(H_X)=39,
\qquad
\operatorname{rank}(H_Z)=120,
\qquad
k=81.
\]

For every tested closure event and both nonzero qutrit values, the syndrome relation holds:

\[
\operatorname{syn}_{H}(e)=\operatorname{syn}_{H'}(Je).
\]

This means the Szilassi closure tick is legal in the finite CSS active/guard bus.  It still does not prove Otto's physical helix model; it proves the finite retwined decoder compatibility of the closure carrier.

## Current closure law

\[
\boxed{
\text{Otto odd half-turn}
\to
\text{Szilassi fixed face }4
\to
\tau_4=(0\ 1)(2\ 6)(3\ 5)(4)
\to
\text{retwined guard decoder}
}
\]
