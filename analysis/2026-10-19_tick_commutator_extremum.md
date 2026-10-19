# Exact W33 commutator interaction: Laplacian and sharp seven-point bound
**Date:** 2026-10-19. **Status:** exact finite-geometry theorem and reproducible exhaustive clique certificate. **Continues:** Pass 12055 and the operator-frame majorization certificate. **Boundary:** proposed interaction, not measured quantum dynamics.

## From two-qutrit tick projectors to a graph Hamiltonian
For each \(p\in W(3,3)\), let \(P_{p,k}\) be the three rank-3 eigenspace projectors of its Pauli operator (\(k=0,1,2\)). The exact commutator norm computed in the companion certificate is \(4/3\) for distinct **noncollinear** points and zero for commuting directions. Consequently the 120-by-120 matrix of pairwise squared commutator norms is
\[
K=\frac43\bigl(J_{40}-I_{40}-A_{W33}\bigr)\otimes J_3.
\]
The noncommutation graph of the 40 point labels is the complement SRG(40,27,18,18), with spectrum \(27^1,3^{15},(-3)^{24}\). Tensoring by \(J_3\) immediately gives
\[
\operatorname{spec}K=108^1,12^{15},0^{80},(-12)^{24};
\quad
\operatorname{spec}(108I-K)=0^1,96^{15},108^{80},120^{24}.
\]
These are **exact algebraic spectra**; the executable also checks the 120-by-120 numeric matrices and all SRG common-neighbor counts.

## Repository prior art and novelty boundary

**The seven-point census is not a new combinatorial discovery.** The repository already records the same 2,880 maximum noncollinear heptads in Passes 5904–5919 (including the rediscovery correction identifying them with BT819 beacon heptads) and the 90 size-four maximal partial ovoids in Passes 7269–7276. See `data/PART_W33_PASS5904_5911_ALL_2880_AND_ONE_ORBIT.json`, `data/PART_W33_PASS5912_5919_THE_2880_WAS_BT819S.json`, `data/bt819_beacon_heptads.json`, and `analysis/w33_pass7269_7276_the_ninety_are_maximal_at_four.py`. The independent enumeration here reproduces that frozen census. **The contribution of this packet is the exact 120-tick commutator interaction spectrum and its sharp continuous (4/7) extremum via Motzkin–Straus, applied to the current Pass-12055 microscopic tick model.** No priority claim is made for the already-known W33 heptads or their counts.

## The seven-point obstruction
An independently implemented integer-bitset Bron–Kerbosch search enumerates all **2,970 maximal cliques** of the noncommutation graph: exactly **90 of size 4 and 2,880 of size 7**. In particular, its clique number is 7, so W33 has independence number 7 and **no 8-, 9-, or 10-point mutually noncollinear set**. The \(\vartheta(W33)=10\) spectral/Lovász bound is therefore not attained by a genuine independent set. We explicitly avoid calling a 10-point upper bound an existing ovoid.

For nonnegative weights \(w_{p,k}\) summing to one, let \(s_p=\sum_k w_{p,k}\). The normalized commutator functional is
\[
\mathcal C(w)=\sum_{a<b}w_aw_b\|[P_a,P_b]\|_F^2
=\frac43\sum_{\{p,q\}\in E(\overline{W33})}s_ps_q.
\]
Motzkin–Straus (1965) states that \(\max_{\sum s=1,s\ge0}\sum_{\{p,q\}\in E(G)}s_ps_q=\tfrac12(1-1/\omega(G))\). Therefore the **sharp global bound** is
\[
\boxed{0\ \le\ \mathcal C(w)\ \le\ \frac47}.
\]
A uniform weighting on any seven-point maximum mutually noncollinear set saturates \(4/7\). Weights supported on a commuting line (or a single point) attain zero. This is a complete optimization result with **continuous weights**, not merely a numerical sampling result.

## Physics interpretation and firewall
A positive coupling \(+\kappa\mathcal C\) penalizes noncommutation and favors contexts; a negative coupling energetically favors large noncommuting packets, with an exact seven-point candidate. This furnishes a finite mathematical **competition between contexts and incompatible ticks**. It does not show that either sign occurs in a real microscopic photon or gauge model. The original Pass-12055 Gibbs free energy still selects one tick for every positive temperature under fixed nonnegative \(\ell_p\) rate constraints; the new interaction must be separately motivated before one can assert a change in phase.

Prior mathematics: Jay Lawrence, *Mutually unbiased bases and trinary operator sets for N qutrits*, Phys. Rev. A 70, 012302 (2004), https://doi.org/10.1103/PhysRevA.70.012302; Motzkin–Straus, *Maxima for graphs and a new proof of a theorem of Turán*, Canadian J. Math. 17 (1965); summary at https://optimization-online.org/wp-content/uploads/2002/01/430.pdf. This repository certificate applies known structures to its current tick-selection question, rather than claiming discovery of Pauli algebras or Motzkin–Straus.
