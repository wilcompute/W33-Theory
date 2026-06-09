# BT624 — Folded Hashimoto Sector Paper Note

## Purpose

BT624 is the paper-facing bridge from BT621--BT623.  It records three linked facts:

1. the raw folded Hashimoto operators grow with the Ihara scale;
2. the protected Hodge sector compresses that growth to a parity clock;
3. the only non-Hodge cross-sector channel is the \(E_1/E_3\) quadratic conjugate packet, not yet a literal \(G_2\)-module.

## Operator family

Let

\[
F_n=TB^nT^T,
\]

where \(B\) is the directed-edge Hashimoto operator of the W33 collinearity graph and \(T\) is the \(480\to160\) directed-edge-to-Levi-flag fold

\[
(p\to q)\longmapsto(p,\ell(p,q)).
\]

BT621 verifies, for \(1\le n\le6\), the raw row-sum law

\[
\boxed{
\operatorname{rowsum}(F_n)=3\cdot 11^n.
}
\]

Thus the full folded transfer still remembers the Ihara/nonbacktracking outdegree

\[
11=k-1.
\]

## Protected parity clock

Let

\[
E_4=\frac1{160}CC^T
\]

be the W33 Levi Hodge projector.  BT621 verifies the protected-sector law

\[
\boxed{
E_4F_nE_4=E_4\qquad(n\text{ odd}),
}
\]

and

\[
\boxed{
E_4F_nE_4=3E_4\qquad(n\text{ even}).
}
\]

So the physical Hodge sector does not inherit the raw \(3\cdot11^n\) growth.  It sees only the two-state parity clock

\[
\boxed{
1,3,1,3,\dots
}
\]

after projection.

## Constant primitive block support

The primitive block support of \(F_n\) is constant over the checked range:

\[
\boxed{
(0,0),(1,1),(1,3),(2,2),(3,1),(3,3),(4,4).
}
\]

Hence the Hodge sector is isolated:

\[
\boxed{
E_iF_nE_4=E_4F_nE_i=0\qquad(i\ne4).
}
\]

The only persistent cross-idempotent channel is

\[
\boxed{
E_1\leftrightarrow E_3.
}
\]

## \(E_1/E_3\) boundary

BT622 and BT623 identify the correct reading of that channel.  The \(E_1,E_3\) primitive sectors are the quadratic conjugate pair attached to the adjacency eigenvalues

\[
2+\sqrt6,\qquad 2-\sqrt6.
\]

The packet has dimension

\[
\boxed{
24+24=48=4\cdot |W(G_2)|.
}
\]

However, BT623 shows that the folded-cubic cross-channel is not a Weyl reflection by itself.  If \(M_{13}=E_1F_3E_3\) and \(M_{31}=E_3F_3E_1\), then

\[
\boxed{
M_{13}M_{31}=-6455E_1,\qquad M_{31}M_{13}=-6455E_3.
}
\]

After normalization, the cross-channel squares to

\[
\boxed{-I}
\]

rather than \(+I\).  It is therefore a complex/quadratic conjugate transport channel, not a literal real reflection action.  The conservative statement is:

\[
\boxed{
E_1+E_3\text{ is a }48=4\cdot12\text{ conjugate lower-shell packet.}
}
\]

An explicit \(W(G_2)\)-equivariant action on this packet remains a separate construction.

## Paper insertion target

This note belongs immediately after the physical propagator normal form and endpoint factorial trace law inserts:

```tex
\input{sections/sec_bt618_physical_propagator_normal_form}
\input{sections/sec_bt619_endpoint_factorial_trace_law}
```

Suggested future section file:

```text
paper/sections/sec_bt624_folded_hashimoto_sector_note.tex
```

## Reviewer-safe summary

\[
\boxed{
\text{raw folded Hashimoto growth}=3\cdot11^n,
}
\]

but

\[
\boxed{
\text{Hodge-projected physical sector}=1,3,1,3,\ldots.
}
\]

The only non-Hodge cross-channel is the \(E_1/E_3\) quadratic conjugate packet.  Its dimension matches \(4\cdot |W(G_2)|\), but the verified \(F_3\) channel has square \(-I\), not \(+I\), so the result is a boundary against overclaiming a literal \(G_2\) Weyl module at this stage.
