# Tick projector operator frame, majorization, and the first geometry-sensitive interaction
**Date:** 2026-10-19. **Status:** exact finite-dimensional calculation plus independently reproducible floating-point witness. **Continues:** Pass 12055. **No fundamental-physics or TOE completion claim.**

## I. What Pass 12055 can and cannot select
Pass 12055 uses the two-qutrit Hilbert space \(\mathbb C^9\) and its 120 tick generators \(h_{p,k}=I_9-\Pi_{p,k}\), where \(\Pi_{p,k}\) is a rank-3 eigenprojector of one of the 40 projective nonzero Pauli directions. At fixed nonnegative rates \(\phi_{p,k}\), \(\sum\phi_{p,k}=R>0\), define \(Q=R^{-1}\sum\phi_{p,k}\Pi_{p,k}\). Then \(0\le Q\le I\), \(\operatorname{Tr}Q=3\), and \(H=R(I-Q)\).

The spectrum of \(Q\) is majorized by \((1,1,1,0,0,0,0,0,0)\). Since \(x\mapsto e^{Rx/T}\) is strictly convex for \(R,T>0\),
\[
\operatorname{Tr}e^{-H/T}\le 3+6e^{-R/T},\qquad
F_T\ge -T\log(3+6e^{-R/T}).
\]
Equality at **positive** temperature requires \(Q\) itself to be a rank-3 projection. Because a nontrivial mixture of distinct equal-rank projections cannot be a projection (use \(\operatorname{Tr}Q^2<3\)), every minimizer is an individual tick, up to duplicate projector labels. This is a **universal rank-projector majorization theorem**, not a W33-specific selection mechanism. At \(T=0\), the ground energy is zero whenever all active projectors have a common vector; therefore compatible mixtures can tie with single ticks. Selection is not unique at zero temperature.

This sharpens the concavity argument, and keeps a firewall: choosing a rank-3 event subspace does not establish an arrow of time, a physical clock rate, or the preference of a real form of \(E_8\) without an independently specified coupling and operational observable.

## II. Exact 120-projector operator frame
With two-qutrit Pauli directions \(p\in W(3,3)\) and outcomes \(k\in\mathbb F_3\), trace orthogonality yields
\[
\operatorname{Tr}(\Pi_{p,k}\Pi_{q,l})=
\begin{cases}
3,&p=q,\ k=l,\\
0,&p=q,\ k\ne l,\\
1,&p\ne q.
\end{cases}
\]
Thus the entire 120-by-120 Hilbert-Schmidt Gram matrix is
\[
G=3I_{120}+(J_{40}-I_{40})\otimes J_3,\qquad
\operatorname{spec}G=120^1\,3^{80}\,0^{39}.
\]
The 80 contrasts \(\Pi_{p,k}-I/3\) give 40 mutually orthogonal, two-dimensional traceless operator planes, spanning the entire 80-dimensional traceless Hermitian operator space on \(\mathbb C^9\). The 39 Gram null modes reflect the 40 copies of the identity decomposition \(\sum_k\Pi_{p,k}=I_9\), with 39 independent differences.

**No-go:** the quadratic overlap Gram does not distinguish W33-collinear and noncollinear distinct points. Any action depending only on this pairwise Gram cannot recover W33 incidence between distinct directions.

## III. The first W33-sensitive interaction
A different two-projector invariant *does* resolve incidence:
\[
\|[\Pi_{p,k},\Pi_{q,l}]\|_F^2=
\begin{cases}
0,&p=q\text{ or }\langle p,q\rangle=0,\\
4/3,&\langle p,q\rangle\ne0.
\end{cases}
\]
For noncommuting Pauli directions, \(\Pi_{p,k}\Pi_{q,l}\Pi_{p,k}=\Pi_{p,k}/3\). Hence \(\operatorname{Tr}(\Pi Q)=1\), \(\operatorname{Tr}(\Pi Q\Pi Q)=1/3\), and the commutator norm is \(2(1-1/3)=4/3\). For commuting directions it vanishes.

Among unordered pairs of the 120 projector labels, exactly 120 share one Pauli direction, 2160 are over 240 W33 edges, and 4860 are over 540 W33 nonedges. This gives the explicit incidence-sensitive functional
\[
\mathcal C(w)=\sum_{a<b}w_aw_b\|[\Pi_a,\Pi_b]\|_F^2
=\frac43\sum_{\{p,q\}\ {\rm noncollinear}}s_p s_q,
\quad s_p=\sum_k w_{p,k}.
\]
It is **a proposed interaction diagnostic**, not a term derived in the Pass-12055 free energy. Demonstrating a microscopic origin, sign, and scale is the next physics task. Positive coupling penalizes noncommuting channels; a negative one rewards them. The bare free-energy minimizer remains the universal one-tick vertex.

## IV. Independent checks and prior art
The accompanying executable regenerates all 120 projectors from \(\mathbb F_3^4\), checks the exact spectral and incidence multiplicities, scans all 7140 unordered pairs, and samples the finite-temperature majorization inequality. Standard sources for the mathematical principle are matrix trace-exponential convexity / the Gibbs variational principle and quantum majorization (e.g. https://link.springer.com/article/10.1007/s13373-018-0123-3 and https://www.nature.com/articles/s41467-018-06261-7).

**Distinction:** the matrix-algebra/Pauli identities are standard; the new contribution here is a focused diagnostic and boundary for the repository's current tick-condensate interpretation, not a priority claim about Pauli theory.
