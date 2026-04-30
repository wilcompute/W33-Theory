# Part CXXXI — PEL Least-Change Action and W33 Loop Realization

**Status:** theorem-grade structural extension  
**Date:** April 29, 2026

The Cycle Clock Theory book repeatedly frames the Principle of Efficient Language as a least-computational-cost principle, and it later connects this to a Least Change Principle.  The W33 Hashimoto carrier gives an exact finite version of that idea.

Parts CXXVIII--CXXX established:

```text
local non-backtracking language -> 11^n words,
loop closure -> Tr(B^n),
trit-weighted efficient language -> normalized 3^{-K_3} loop measure.
```

This part identifies the natural action functional.

## 1. Local alphabet and closure cost

For a directed edge `e`, the local branch alphabet has size

\[
q_H = k-1 = 11.
\]

A length-`n` non-backtracking word therefore has uniform local trit cost

\[
K_{\mathrm{local}}(n)=n\log_3(11).
\]

If the history closes, it lands in the loop-admissible sublanguage of size

\[
\frac{Z_n}{480}=\frac{\operatorname{Tr}(B^n)}{480}.
\]

The loop selection information is therefore

\[
\boxed{
I_n=\\log_3\frac{11^n}{Z_n/480}
=n\log_3(11)-\log_3\left(\frac{Z_n}{480}\right).
}
\]

This is the exact trit-cost of imposing self-consistency at length `n`.

## 2. First least-change event

The first nonzero loop occurs at `n=3`:

\[
\frac{Z_3}{480}=2.
\]

Thus

\[
\boxed{
I_3=\log_3\frac{11^3}{2}
=3\log_3(11)-\log_3(2).
}
\]

The two surviving words are precisely the two triangle closures through the initial directed edge.  So the first W33 realization event is

```text
11 local options per step
3 steps
2 self-consistent triangle closures
```

or

\[
\boxed{11^3 \longrightarrow 2.}
\]

## 3. Efficient action

Define the W33 loop action by

\[
\boxed{
\mathcal A_n(e)=K_{\mathrm{local}}(n)-K_{\mathrm{closed}}(n)
=n\log_3(11)-\log_3\left(\frac{Z_n}{480}\right).
}
\]

Equivalently,

\[
\boxed{
\mathcal A_n(e)=-\log_3\Pr_n(\mathrm{loop}\mid e).
}
\]

Thus the least-change/efficient-language principle becomes:

```text
realized loops are weighted by the negative trit-log of their closure probability.
```

This is a finite action principle, not a continuum approximation.

## 4. Long-loop equilibrium

From CXXIX,

\[
\Pr_n(\mathrm{loop}\mid e)=\frac{1}{480}+O(11^{-n/2}).
\]

Therefore

\[
\boxed{
\mathcal A_n \to \log_3(480)
}
\]

with Ramanujan-rate oscillatory correction.  The limiting action is the trit information needed to specify one directed-edge state out of 480.

So W33 has two exact action regimes:

```text
first realization action:  log_3(1331/2),
thermal/equilibrium action: log_3(480).
```

## 5. Theorem CXXXI

**Theorem CXXXI (PEL Least-Change Action).**  On the W33 Hashimoto carrier, the Principle of Efficient Language has an exact finite action functional

\[
\boxed{
\mathcal A_n=-\log_3\left(\frac{\operatorname{Tr}(B^n)}{480\cdot 11^n}\right).
}
\]

The first nonzero loop action is

\[
\boxed{
\mathcal A_3=\log_3(1331/2),
}
\]

and the long-loop action converges to

\[
\boxed{
\lim_{n\to\infty}\mathcal A_n=\log_3(480).
}
\]

The convergence correction is governed by the nontrivial Ihara/Ramanujan poles.

## 6. Meaning

CCT says efficient language and least change should generate probability distributions from finite computation.  W33 supplies the exact arithmetic:

```text
least change = minimum trit action,
probability = 3^{-action},
realization = loop closure,
equilibrium = uniform directed-edge return law,
fluctuation = Ramanujan zeta oscillation.
```

This turns the philosophical PEL statement into a finite graph action principle.

The accompanying regression tests are in:

```text
tests/test_pel_least_change_action_cxxxi.py
```
