# BT1204 -- Holonet Demonstrator / Fault-Tolerant Milestone Dashboard

This is the paper-facing dashboard corresponding to `data/bt1203_holonet_demonstrator_fault_tolerance_dashboards.json`.

## Boundary

The single-photon demonstrator is an unencoded logical experiment. It can falsify the substrate logic, the holonomic gate claim, the `2T = SL(2,3)` fingerprint, the Boerdijk--Coxeter clock, and the qutrit Chern-protection claim. It cannot demonstrate fault tolerance by itself, because one fixed-photon-number carrier cannot carry a many-photon GKP grid state.

The fault-tolerant machine is the concatenated continuous-variable stack

\[
240\text{ squeezed modes}
\to 120D_4\text{ GKP pairs}
\to 240\text{ GKP qutrits}
\to [[240,81,4]]_3
\to 81\text{ logical qutrits}.
\]

## A. Near-term single-photon falsifiers

| ID | Test | Exact claim | Falsifies if |
|---|---|---|---|
| D1 | Trace--Choi visibility | \(V(U)=|\operatorname{Tr}U|/3\), with \(V(F_3)=1/3\), \(V(X)=V(Z)=0\). | Visibility spectrum cannot be fit by the qutrit trace law. |
| D2 | Holonomic timing-independence | Same loop in control space gives the same unitary under timing reparametrization. | Gate changes systematically with speed or pulse shape while the path is fixed. |
| D3 | Holonomy-group fingerprint | Gates close into \(2T=\mathrm{SL}(2,3)\), order 24, order spectrum \(\{1,1,8,6,8\}\). | Tomography recovers a different group/order spectrum. |
| D4 | BC quasicrystal aperiodicity | \(\theta=\arccos(-2/3)\) never recurs exactly. | A genuine finite recurrence appears after hardware-locking artifacts are ruled out. |
| D5 | Spin-1 topological pump | Rotation-realized qutrit pump has extremal Chern magnitude \(|C|=2\). | Pump is trivial, or only qubit-strength \(|C|=1\), in the claimed regime. |

## B. Fault-tolerant machine milestones

| ID | Milestone | Target | Evidence needed |
|---|---|---|---|
| F1 | Threshold squeezed light | Protocol-dependent approximately 7--20 dB, eased by \(D_4/E_8\) coding gains. | Mode-resolved squeezing, loss budget, and qutrit decoder noise model. |
| F2 | Qutrit GKP state generation | Finite-squeezing qutrit GKP states in the \(D_4\) two-mode lattice. | State tomography or decoder-level evidence of qutrit displacement-error correction. |
| F3 | \(D_4\) inner analog-to-digital code | 120 \(D_4\) GKP pairs yielding 240 discrete qutrit error channels. | Closest-lattice-point syndrome decoding and measured coding gain. |
| F4 | Steinberg outer code | \([[240,81,4]]_3\) on the W(3,3) 240-edge carrier. | Syndrome extraction and logical-error suppression consistent with distance 4. |
| F5 | Cubic non-Gaussian resource | Degree-3 \(E_6\) matter-shell magic. | Cubic-phase or magic-state certification compatible with the encoded Clifford layer. |
| F6 | Encoded \(\mathrm{Sp}(4,3)\) Clifford network | Programmable beamsplitter/phase/squeeze/modulator network on encoded qutrits. | Encoded gate tomography and closure under \(\mathrm{Sp}(4,3)\) modulo Pauli/frame conventions. |
| F7 | Homodyne and qutrit syndrome readout | Stable inner GKP and outer Steinberg syndrome readout. | Repeated syndrome extraction with tracked logical frame and below-threshold residual displacement noise. |

## Use in the manuscript

The split should be cited whenever the holonet demonstrator is discussed. The demonstrator can make the substrate hypothesis experimentally vulnerable now; the fault-tolerant machine remains a separate CV engineering target.
