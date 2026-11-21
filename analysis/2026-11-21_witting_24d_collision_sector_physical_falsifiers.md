# Witting 45-chart photonics: 27-deck optimization, the exact 24D coincidence sector, quantum and spacetime falsifiers

**21 November 2026.** Fifth independent, executed research follow-up to commit `b47deee97d55adc1fa5ba43bc36d2aadd1183689`. Numerical/exact certificate: `data/toe_20261121_device_scheduler_channel_causal_audit.json`. Producer `analysis/toe_20261121_fivefront_physical_falsifiers.py`; offline regression `tests/test_toe_20261121_fivefront_physical_falsifiers.py`.

**Key result:** the exact 24-dimensional kernel invisible to the 27 five-chart Witting POVM schedules is **precisely the linear span of the centered two-photon matched-coincidence profiles**. The observable two-copy data therefore isolate a representation sector suppressed by complete schedule averages. This is a strong operational finite-geometric identity, **not** a theory of fundamental particle interactions, Lorentzian spacetime or quantum gravity.

## Mathematical baseline and prior-art fence

Use the previously committed `analysis/toe_20261121_hermitian45_pauli_sic_bridge.py` and `analysis/toe_20261121_27decks_fivefronts.py`. They certify 40 complex C4 Witting rays r_i, each with projector P_i; 45 8-ray Hermitian-chart supports S_z, each a direct sum of two orthogonal qubit SICs; 27 five-chart complete 40-ray partitions \(\mathcal D_\ell\); and the exact GF4/GF3 geometry with group PGU4(2) = PSp4(3), order25920.

Established prior art already owns complex Witting rays, 40 tetrads and 2-design (Waegell–Aravind, *The Penrose dodecahedron and the Witting polytope are identical in CP3*, https://arxiv.org/abs/1701.06512); their quantum-communication proposal (Vlasov, *Scheme of quantum communications based on Witting polytope*, https://arxiv.org/abs/2503.18431); the 45/27 Hermitian generalized quadrangle; GQ/Schläfli finite group structure; and the full projective action. The repo's `scripts/w33_witting_packet_quotient_geometry_audit.py` and `analysis/w33_pass9961_9984_the_unitary_branch.py` had separately reached 45/27 via different routes. **The explicit complementarity of the 27-schedule incidence kernel with all two-copy matched-coincidence profiles is the new audited connection in this follow-up.**

## Front 1: loss-aware four-mode versus eight-mode optical devices

The 40 original orthogonal tetrad measurements use 4 output ports; each of our 27 Hermitian-line schedules chooses uniformly between five valid eight-outcome double-SIC measurements. Each ideal chart has effects E_i(z)=P_i/2, and the unlabeled 40-outcome result is E_i=P_i/10.

A generic Clements rectangular interferometer can be built from N(N-1)/2 two-mode MZI cells, i.e. 6 for N=4 and 28 for N=8, with balanced path depth scaling approximately N. The *absolute per-photon loss* therefore need not decrease, even if the number of setting choices drops 40->5.

A deliberately **illustrative, not calibrated** toy assumes one photon traverses respectively four or eight equal-loss mesh stages; the assumed four detector efficiencies are (.94,.96,.92,.95), the eight are (.94,.96,.92,.95,.90,.93,.97,.91), and per-stage intensity survival is t=1-loss. Every Witting tetrad and all 27 five-chart schedules were checked against four input Witting states. At stage loss .5%, sample input ray0 gives PVM survival .92395 versus 27-schedule eight-port mean .89892. At stage loss 2%, sample input ray39 gives .86810 versus .79348. **The new architecture saves switching configurations in this ledger, not transmitted photons.**

A serious detector loophole is exhibited analytically and numerically. Use an actual separable two-ququart pure input |r0> x |r0*> and select uniformly one of five charts in a deck. The unbiased matched-outcome separable bound is P_match<=.2. In the chart containing r0, pass outcome r0 with unit efficiency and other outcomes at 50%; in the other four charts pass all outcomes at 50%. The probability of surviving *and* matching is .0875; of joint survival .3125; postselected match =.0875/.3125 = **.28**, violating .20 without entanglement. This demonstrates why fair sampling, independently calibrated heralding/loss, and explicit failure outcomes are mandatory before claiming an entanglement witness or QKD security.

External device precedents: Clements rectangular-mesh decomposition, https://docs.pennylane.ai/en/stable/code/api/pennylane.Interferometer.html ; 8x8 reconfigurable photonic multiport demonstration, https://doi.org/10.1038/s41566-025-01806-x . No custom optical chip was built or tested.

## Front 2: complete optimization theory of the 27 five-setting schedules

Let K be the 45x27 binary incidence matrix: K(z,l)=1 iff chart z belongs to deck l. **Exactly 27** five-chart exact covers exist, and five is minimal because eight outcomes x four contexts cover at most32 of the40 rays; equality at five demands disjoint supports. The 5-cliques of the chart-disjointness graph are exactly these 27 Hermitian lines.

Because each chart belongs to 3 decks and every deck to 5 charts:
\[
 K K^\top=3 I_{45}+ A,\qquad
 {\rm spec}(A)=12^1,3^{20},(-3)^{24}
\]
for A the Hermitian chart-collinearity adjacency matrix SRG(45,12,3,3). Consequently
\[
 {\rm spec}(KK^\top)=15^1,6^{20},0^{24},\quad
 {\rm rank}(K)=21,\quad \dim\ker(K^\top)=24.
\]
For any nonnegative additive chart-cost vector c, the 27 deck costs are \(K^\top c\), and their average equals \((1/9)\sum_z c_z\). Thus a cost-optimal deck is never worse than the mean. More strikingly, any positive heterogeneous chart costs of the form c=1+v, with v in ker(K^T), **give exactly the same cost of 5 to every deck**. A deterministic instance with c in [0.75,1.1807] confirms this; the residual is below 10^-15.

This nullspace fact does NOT cover nonlinear context-switch costs, crosstalk, ray-dependent loss, or actual chip stability.

## Front 3: full-Choi audit of the physical but entanglement-breaking bridge

For ququart input Witting POVM E_i=P_i/10, measure outcome i and prepare a 9-dimensional density matrix sigma_i equal to the maximally mixed rank3 +1 eigenspace of the corresponding two-qutrit Pauli operator. This provides an explicit CPTP map:
\[
 \mathcal E(\rho)=\sum_i {\rm Tr}(E_i\rho)\,\sigma_i.
\]
The **normalized** 4x9 Choi state \(J/4=\tfrac14\sum_i E_i^\top\otimes\sigma_i\) is a convex sum of product positive operators and is separable (hence positive and PPT). Independent 36x36 numerical diagonalization finds full rank36 and minimum eigenvalue .00771808, PPT minimum .01198706.

For any coherent isometric encoding \(\mathcal V:\mathbb C^4\to\mathbb C^9\), the maximally entangled Choi target has Schmidt rank4. Any separable state overlaps it by at most 1/4, so measuring the target projector yields
\[
 F_e(\mathcal E,\mathcal V)\le 1/4,\qquad
 \|\mathcal E-\mathcal V\|_\diamond\ge 2(1-1/4)=3/2.
\]
The diamond norm here uses the unhalved convention, maximum2. Thus **no choice of target isometry makes THIS measure-prepare interface close to a coherent encoder**. Its quantum capacity is zero, though its 15-dimensional Hermitian input-information transfer is injective with Hilbert-Schmidt contraction1/15 (inverse amplification15). This does not prohibit other physical 4->9 channels with ancillas.

Prior art: entanglement-breaking channels are standard (Horodecki, Shor and Ruskai, *General Entanglement Breaking Channels*, https://arxiv.org/abs/quant-ph/0302031).

## Front 4: a full 540-pair two-copy chart selector, and **exact 24D coincidence duality**

Let the unscaled two-copy coincidence profile on chart z for two distinct Witting pure states a,b be
\[
 F_z(a,b)=\sum_{i\in S_z}
 |\langle r_i|r_a\rangle|^2|\langle r_i|r_b\rangle|^2.
\]
Physical locally independent double-SIC measurements, with two trusted input copies \(|r_a\rangle\otimes|r_b\rangle\), yield a **matched-outcome probability** \(p_z(a,b)=F_z(a,b)/4\). This is an implementable measurement probability, unlike a postulated fundamental two-photon Hamiltonian.

**Exhaustive exact finite answer:**
- Every one of the 540 **nonorthogonal** ray pairs has the identical 45-chart score histogram: \(8/9\) once, \(5/9\) 32 times, \(4/9\) 12 times. The single maximum is exactly the chart containing BOTH rays.
- Every one of 240 **orthogonal** pairs has score histogram: \(2/3\) three times, \(4/9\) 27 times, \(1/3\) 12 times, \(0\) three times. The maxima tie, so a unique selector needs nonorthogonal sources.
- A nonorthogonal pair's score gap is exactly \(1/3\); its measurable matched-event probability gap is \(\Delta=1/12\). With **independent, ideal, identically calibrated trials at each chart**, Hoeffding and a 45-chart union bound give \(n=\lceil 2\ln(90/0.01)/\Delta^2\rceil=2623\) trials per chart (118035 total) sufficient for selecting the maximum with error probability at most1%. This is conservative, with no dark counts, drift, finite detector efficiencies, context-switch overhead, or adversarial leakage.

**The exactly complementary 24-dimensional sector:** Let \(C\) be the 45x780 matrix whose column indexed by each unordered distinct pair a,b is the chart vector \(F_\bullet(a,b)\). The Witting complex projective 2-design supplies
\[
 \sum_{i=1}^{40}
 |\langle r_i|r_a\rangle|^2|\langle r_i|r_b\rangle|^2
 =2(1+|\langle r_a|r_b\rangle|^2).
\]
Since each deck partitions all 40 rays,
\[
 K^\top F_\bullet(a,b)
 =2(1+|\langle r_a|r_b\rangle|^2)\boldsymbol1_{27}.
\]
Therefore with \(\widetilde C\) the mean-subtracted 45x780 profile matrix,
\[
 K^\top\widetilde C=0,\quad
 A\widetilde C=-3\widetilde C,\quad
 {\rm im}(\widetilde C)\subseteq\ker(K^\top).
\]
**We establish equality of the 24-dimensional spaces with an EXACT arithmetic rank certificate.** Every squared overlap is 0,1/3,or1. Define integer \(W_{ai}=3|\langle r_a|r_i\rangle|^2\in\{0,1,3\}\), integer \(T_{z,ab}=\sum_{i\in S_z}W_{ai}W_{bi}=9F_z(a,b)\), and integer centered matrix \(\widetilde T=5T-({\sum_z T}/9)\boldsymbol1\). Direct integer multiplication yields exactly \(K^\top\widetilde T=0\), \((A+3I)\widetilde T=0\). An independent Gaussian elimination over the field GF(7) gives \({\rm rank}_{GF(7)}\widetilde T=24\). As the rational kernel of \(K^\top\) has dimension24, this forces **rank over Q exactly24** and equality of images. The uncentered pair-profile matrix has exact GF7 rank25.

This ties the physical two-copy coincidence signatures to the **-3 irreducible spectral sector** of the generalized-quadrangle chart graph—precisely the modes invisible to 27 complete-deck sums. It is a new explicit identification in this investigation, though the underlying SRG and its eigenspaces are classical.

**Naive "Hamiltonian" obstructions:** each chart has \(\sum_{i\in S_z}P_i=2I_4\), so any chart selector based only on **total** chart intensity is a scalar and cannot select. For two nonorthogonal Witting rays, \(\|[P_a,P_b]\|_2=\sqrt2/3\): they are NOT independent commuting optical number modes, so writing a cross-Kerr Hamiltonian with such fictitious modes is invalid. An external program-label classical selector can instead have a one-unit unperturbed ground-state gap; any Hermitian perturbation of norm epsilon<1/2 retains uniqueness with gap at least \(1-2\epsilon\), verified for16 random norm-.4 perturbations. The two-copy collision rule avoids the fictitious commuting-mode assumption but does NOT remove external setting or energy requirements.

## Front 5: rigorous finite causal obstruction and an actual qutrit-memory dimension witness

The 45-chart collinearity graph obeys the **exact integer identity** \(A^2=9I+3J\). Thus in one graph step any chart reaches12 neighbors, and after two all45 charts are reachable (including itself). The normalized random-walk transition P=A/12 gives
\[
 (P^2)_{zz}=1/12,\qquad (P^2)_{zw}=1/48\text{ for all }z\ne w.
\]
Using seven explicit Hermitian projective group generators, all **540 oriented adjacent vertex pairs** lie in one orbit, including each edge and its reverse. A nontrivial invariant orientation is therefore impossible under the full projective group. A time-indexed *lift* (chart,t)->(neighbor,t+1) is acyclic but **adds time externally**, has immediate two-tick global reach, and is neither Lorentzian geometry nor microcausal QFT.

Separately, for a **properly implemented** causal break and trusted12-state qutrit MUB 2-design tomography, the average input/output state fidelity is related to the channel's Choi entanglement fidelity via \(F_{\rm avg}=(3F_e+1)/4\). If the intermediate memory retains at most k-dimensional quantum coherence, the temporal Choi Schmidt number is at most k and \(F_e\le k/3\). Therefore:
- \(F_{\rm avg}>1/2\) excludes all entanglement-breaking storage across the causal break.
- \(F_{\rm avg}>3/4\) certifies Schmidt number at least3, so storage of at least three-dimensional quantum coherence was necessary across that cut, under the stated assumption that only the memory carries input-dependent information.
These are **necessary dimension-witness thresholds**, not achievable fidelity upper bounds for every restricted architecture. An ideal two-SWAP qutrit memory attains fidelity1; a computational-basis dephasing channel attains1/2; a memoryless fixed reset attains1/3.

Prior art exists for Schmidt-number memory fidelity benchmarks (https://journals.aps.org/pra/abstract/10.1103/PhysRevA.85.010305); recent research explicitly uses projective 2-design probes to quantify quantum-memory fidelity (https://arxiv.org/abs/2610.08445). Our contribution is a reproducible side-by-side falsification model, not discovery of these memory inequalities.

## Reproducibility, source audit and honesty boundary

```powershell
python analysis/toe_20261121_fivefront_physical_falsifiers.py
python tests/test_toe_20261121_fivefront_physical_falsifiers.py
python tests/test_toe_20261121_27decks_fivefronts.py
python tests/test_toe_20261121_hermitian45_pauli_sic_bridge.py
```

This producer regenerates a frozen JSON certificate with **no network calls** and modifies none of the preceding results. The auxiliary scientific references above are background/prior-art, not a claim to have read every referenced full text during this pass. All simulated optical detector numbers, noise and per-stage transmission are **assumptions**; no photon experiment, device calibration, secure-key-rate proof or gravitational physical prediction has been obtained.

## Top five independent next steps

1. **Two-copy physical selector circuit:** synthesize all 45 chart-specific 8-mode Naimark unitaries into a calibrated, loss-aware two-photon matched-outcome experiment; measure the universal \(1/12\) chart discrimination gap and keep failures explicitly.
2. **Exact representation-sector theorem:** derive the 24-dimensional collision profile sector from group characters/Schur projectors, and compare its code-distance/conditioning properties with the 20-dimensional visible deck-cost sector.
3. **Robust simultaneous tomography:** combine a five-chart deck (full rank40-outcome informational completeness) with a sparse set of coincidence charts; optimize the number of observations required to reconstruct the 24D hidden cost deviations under heteroskedastic and correlated losses.
4. **Coherent versus entanglement-breaking encoder:** construct and optimize a genuinely coherent 4-to-9 Stinespring isometry or quantum instrument under explicit restricted Pauli covariance, with a laboratory-checkable Choi-fidelity lower bound.
5. **Physical time and memory falsifier:** specify an event-ready qutrit causal-break experiment with an intermediate memory dimension cap, independent SPAM/herald efficiency bounds, and a distinct Lorentzian continuum action satisfying microcausal locality.
