# BT1459--BT1461: Holonet splicer, schedule compressor, and residual runner

## BT1459 — Holonet splicer

The claim-firewalled TeX section now has an executable idempotent splicer:

\[
\texttt{tools/bt1459\_holonet\_splicer.py}.
\]

The splicer inserts

\[
\texttt{analysis/BT1457\_claim\_firewalled\_holonet\_section.tex}
\]

into `photonic_holonet.tex` before the fuel section and verifies that the input is present exactly once.  In this connector pass, the large main TeX file was not rewritten directly through the contents API; the committed splicer performs the exact edit in a checkout.

## BT1460 — \(S_3\times C_3\) schedule compressor

The primitive closure schedule has 48 steps:

\[
12\text{ strands}\times4\text{ operations}.
\]

Using the factorization

\[
S_3\text{ switch}\times C_3\text{ phase},
\]

the schedule compresses to a four-operation template over the loop space

\[
3\times2\times2=12.
\]

The loop variables are:

- central \(C_3\) pair index;
- \(S_3\)-side bit;
- orientation bit.

The strand formula is

\[
\text{strand}=4c+2s+o.
\]

The compressed template still covers active columns \(14s+13\), the full guard tail \(216,\ldots,239\), and balances the three Szilassi opposite-pair channels four times each.

## BT1461 — equation worksheet residual runner

The residual runner reads the BT1458 CSV worksheet.  Blank formula cells stay blocked.  Once formulas are filled, it evaluates expressions against:

\[
g/2=1.00115965218059,
\]

\[
\Delta g=0.002319304361180219,
\]

\[
a_e=0.0011596521805901094,
\]

\[
\alpha/\pi=0.0023228194643817837,
\]

and

\[
12/13=0.9230769230769231.
\]

This is the formula-level audit harness for Otto equations (49), (50), (64), (65), and (66).

## Current architecture

\[
\boxed{
\text{claim-firewalled TeX insert}
\quad+\quad
4\text{-op }S_3\times C_3\text{ schedule template}
\quad+\quad
\text{formula residual runner}
}
\]
