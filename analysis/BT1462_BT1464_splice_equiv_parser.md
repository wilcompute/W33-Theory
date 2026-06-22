# BT1462--BT1464: splice status, schedule equivalence, and formula parser upgrade

## BT1462 / BT1459 — Holonet splicer status

The claim-firewalled section is now represented by an executable splicer:

```text
tools/bt1459_holonet_splicer.py
```

It inserts the BT1457 TeX section before the fuel section and is designed to be
idempotent: after execution the input should occur exactly once.  In the current
connector pass the large `photonic_holonet.tex` source was not rewritten through
the contents API; the splicer is the committed source-of-truth edit mechanism.

## BT1463 — schedule equivalence

The compressed schedule loop

\[
(c,s,o)\in C_3\times C_2\times C_2
\]

with

\[
\mathrm{strand}=4c+2s+o
\]

expands to exactly 48 closure events:

\[
12\text{ active ticks}+12\text{ guard pairs}+12\text{ frame updates}+12\text{ readouts}.
\]

The induced qutrit-value trial rows are exactly

\[
24\text{ active rows}+48\text{ guard rows}=72.
\]

The active columns are \(14s+13\), and the guard columns cover the full tail
\(216,\ldots,239\), matching the retwined closure checks.

## BT1464 — formula parser upgrade

The worksheet residual runner now accepts symbolic aliases:

```text
Phi, phi5, delta_g, a_e, Schwinger, ratio_12_13
```

and classifies any evaluated formula by nearest target among:

\[
g/2,\quad \Delta g,\quad a_e,\quad \alpha/\pi,\quad 12/13.
\]

Blank worksheet rows remain blocked.  Filled rows will be evaluated and assigned
nearest-target residuals.

## Current status

\[
\boxed{
\text{idempotent TeX splicer}
+\text{exact schedule equivalence}
+\text{alias-aware formula residual parser}
}
\]
