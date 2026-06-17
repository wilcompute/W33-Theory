# BT1231 -- Sp43 Minimal Transvection Count

## Purpose

BT1228 proved that a concrete four-projective-transvection set reaches the full two-qutrit Clifford target:

\[
|Sp(4,3)|=51840.
\]

BT1230 ruled out one and two projective transvections. BT1231 finishes the remaining gap by checking every three-projective-transvection set.

## Exhaustive check

There are

\[
\binom{40}{3}=9880
\]

triples of projective transvections. The exhaustive closure histogram is

\[
\boxed{24^{360},\quad 27^{160},\quad 72^{2160},\quad 648^{7200}.}
\]

Thus the largest subgroup reached by any triple has order

\[
\boxed{648}.
\]

No triple reaches \(51840\).

## Minimality theorem

BT1228's four-set

\[
(0,0,0,2),\quad (0,2,0,0),\quad (0,0,2,2),\quad (1,0,0,0)
\]

has closure order

\[
\boxed{51840}.
\]

Therefore the exact projective-transvection count is

\[
\boxed{m_{\min}=4.}
\]

## Boundary

This is exact inside the projective-transvection generating family. It does not claim that arbitrary non-transvection generators have the same minimal count.

## Files

- Code: `analysis/bt1231_sp43_minimal_transvection_count.py`
- Result: `data/bt1231_sp43_min_count_summary.json`
