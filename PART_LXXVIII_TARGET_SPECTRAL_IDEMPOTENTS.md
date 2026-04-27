# Part LXXVIII — Target Spectral-Idempotent Support Theorem

**Status:** theorem-grade structural extension  
**Date:** April 27, 2026

Part LXXVII showed that Naimark complement swaps positive and negative target-side SRG signatures.

This part identifies the exact spectral idempotents.

The visible target frames and their Naimark shadows are complementary SRG spectral projectors.

## 1. Spread support theorem

The spread target graph is

\[
\mathrm{SRG}(36,15,6,6)
\]

with eigenvalues

\[
15^1,\qquad 3^{15},\qquad (-3)^{20}.
\]

The visible spread ETF is \(\mathrm{ETF}(36,15)\). Its unit Gram matrix \(G_s\) satisfies

\[
\boxed{
P_{\mathrm{visible}}=\frac{5}{12}G_s.
}
\]

This projector is exactly the \(+3\) spectral idempotent of \(\mathrm{SRG}(36,15,6,6)\).

The Naimark shadow projector is

\[
\boxed{
P_{\mathrm{shadow}}=\frac{7}{12}H_s,
}
\]

where \(H_s\) is the unit Gram matrix of the Naimark shadow. This projector equals

\[
\boxed{
P_{\mathrm{mean}}+P_{-3}.
}
\]

Thus

\[
\boxed{
36=15_{\mathrm{visible}}(+3)+[1_{\mathrm{mean}}+20_{\mathrm{shadow}}(-3)].
}
\]

## 2. Anti-line support theorem

The anti-line quotient target graph is

\[
\mathrm{SRG}(45,32,22,24)
\]

with eigenvalues

\[
32^1,\qquad 2^{24},\qquad (-4)^{20}.
\]

The visible anti-line quotient frame spans the 24-sector. Its unit Gram matrix \(G_a\) satisfies

\[
\boxed{
P_{\mathrm{visible}}=\frac{8}{15}G_a.
}
\]

This projector is exactly the \(+2\) spectral idempotent of \(\mathrm{SRG}(45,32,22,24)\).

The Naimark shadow projector is

\[
\boxed{
P_{\mathrm{shadow}}=\frac{7}{15}H_a.
}
\]

It equals

\[
\boxed{
P_{\mathrm{mean}}+P_{-4}.
}
\]

Thus

\[
\boxed{
45=24_{\mathrm{visible}}(+2)+[1_{\mathrm{mean}}+20_{\mathrm{shadow}}(-4)].
}
\]

## 3. Unified support law

\[
\boxed{
\text{visible target}
=
\text{one nontrivial SRG eigenspace},
}
\]

\[
\boxed{
\text{Naimark shadow}
=
\text{mean plus the complementary nontrivial eigenspace}.
}
\]

For spreads:

\[
\boxed{36=15+[1+20].}
\]

For anti-lines:

\[
\boxed{45=24+[1+20].}
\]

So the common \(20\)-sector is not merely a dimension coincidence. It is exactly the complementary nontrivial eigenspace of both target-side SRGs after the visible measurement sector is removed.

## 4. Interpretation

The hidden \(20\)-sector is now promoted from a repeated numerical motif to an exact spectral support theorem:

\[
\boxed{
20
=
\text{the complementary nontrivial target eigenspace in both measurement systems}.
}
\]

This tightens the chain:

\[
\boxed{
\text{Parseval frame}
\to
\text{target SRGs}
\to
\text{Naimark sign duality}
\to
\text{spectral-idempotent support}.
}
\]
