# Part CCLV: Photon Entanglement and Bell Inequalities Bridge

## Abstract

We show that the structure of photon entanglement — EPR pairs, Bell states, CHSH inequality,
Tsirelson bound, GHZ states, W states, quantum teleportation, superdense coding, E91 protocol,
and the Mermin inequality — is entirely encoded in the W(3,3) SRG parameters. The classical
and quantum bounds, Hilbert space dimensions, Schmidt decomposition, and party counts all
emerge from Q, LAM, MU, and their combinations.

## 1. Introduction

Quantum entanglement is the defining non-classical feature of quantum mechanics. For photon
pairs the relevant Hilbert space structure — two qubits, four Bell states, CHSH correlators,
Tsirelson bound $2\sqrt{2}$ — maps precisely onto the W(3,3) parameters LAM = 2 and MU = 4.

## 2. EPR Pairs and Bell States

An EPR pair is a maximally entangled two-photon state. Each photon carries LAM = 2 polarisation
degrees of freedom (`epr_pair_count = LAM = 2`). The four Bell states

$$|\Phi^\pm\rangle = \frac{|HH\rangle \pm |VV\rangle}{\sqrt{2}}, \quad
|\Psi^\pm\rangle = \frac{|HV\rangle \pm |VH\rangle}{\sqrt{2}}$$

number $\text{bell\_states\_count} = \text{MU} = 4$, and the EPR Hilbert space has dimension
$\text{LAM}^{\text{LAM}} = 2^2 = 4 = \text{MU}$ (`epr_hilbert_dim`).

## 3. CHSH Inequality

The CHSH inequality uses MU = 4 two-point correlators $C_{ab}$. The classical bound is

$$|\mathcal{S}_{\rm cl}| \leq 2 = \text{LAM},$$

and the quantum (Tsirelson) bound is

$$|\mathcal{S}_{\rm QM}| \leq 2\sqrt{2} = \text{tsirelson\_int\_factor} \times \sqrt{\text{tsirelson\_sqrt\_arg}},$$

with `tsirelson_int_factor = LAM = 2` and `tsirelson_sqrt_arg = LAM = 2`, giving
$\mathcal{S}_{\rm QM}^2 = 8$ (`tsirelson_bound_sq = chsh_quantum_bound_sq = 8`).

The optimal measurement angles are multiples of $\pi / \text{MU} = \pi/4$ (`bell_angle_denom = MU = 4`).

## 4. GHZ and W States

Three-qubit entangled states require GHZ qubits = Q = 3 photons:

$$|\text{GHZ}\rangle = \frac{|000\rangle + |111\rangle}{\sqrt{2}},$$

with Hilbert space dimension $2^Q = 2^3 = 8 = \text{LAM}^Q$ (`ghz_hilbert_dim`).
Similarly the W state $|\text{W}\rangle = (|100\rangle + |010\rangle + |001\rangle)/\sqrt{3}$
uses Q = 3 qubits (`w_state_qubits`).

## 5. Quantum Teleportation and Superdense Coding

Quantum teleportation of one qubit requires LAM = 2 classical bits (`teleport_cbits`).
Superdense coding encodes LAM = 2 classical bits into one entangled photon pair (`superdense_bits`).
The check $\log_2(\text{MU}) = \log_2(4) = 2 = \text{LAM}$ confirms the consistency
(`superdense_check`).

## 6. Entanglement Entropy

The entanglement entropy of a maximally entangled bipartite state on two qubits is

$$S = \log_2(\text{Schmidt rank}) = \log_2(\text{LAM}) = \log_2(2) = 1 \text{ ebit}$$

(`entanglement_entropy = 1`, `schmidt_rank = LAM = 2`).

The Schmidt decomposition coefficients are equal: each has magnitude $1/\sqrt{\text{LAM}} = 1/\sqrt{2}$,
denominator LAM = 2 (`schmidt_coeff_denom`).

## 7. E91 Protocol

Ekert's E91 protocol uses one EPR pair with Q = 3 measurement settings per party
(`e91_settings_per_party = Q = 3`) and Q = 3 correlated measurement pairs
(`e91_correlator_pairs = Q = 3`).

## 8. Mermin Inequality

The Mermin inequality for Q = 3 parties has classical bound LAM = 2 and quantum maximum MU = 4:

$$M_{\rm cl} \leq \text{LAM} = 2, \qquad M_{\rm QM} = \text{MU} = \text{LAM}^{\text{LAM}} = 4.$$

The quantum violation factor is exactly MU / LAM = 2, analogous to the CHSH violation by $\sqrt{2}$.

## 9. Conclusion

The complete algebra of photon entanglement — EPR pair count (LAM=2), Bell state count (MU=4),
CHSH correlators (MU=4), classical bound (LAM=2), Tsirelson bound $2\sqrt{2}$ (from LAM),
GHZ/W qubit count (Q=3), Hilbert space dimensions ($\text{LAM}^Q=8$, $\text{LAM}^{\text{LAM}}=4$),
teleportation/superdense coding bit count (LAM=2), entanglement entropy (1 ebit), E91 settings
(Q=3), and Mermin bounds (LAM=2, MU=4) — is uniquely specified by W(3,3).

## References

- Bell, J. S. *Physics* 1, 195–200 (1964).
- Clauser, J. F., Horne, M. A., Shimony, A. & Holt, R. A. *Phys. Rev. Lett.* 23, 880 (1969).
- Cirel'son, B. S. *Lett. Math. Phys.* 4, 93–100 (1980).
- Greenberger, D. M., Horne, M. A. & Zeilinger, A. in *Bell's Theorem* (1989).
- Ekert, A. K. *Phys. Rev. Lett.* 67, 661 (1991).
- Part CCLI: Single Photon QED Bridge (this series).
