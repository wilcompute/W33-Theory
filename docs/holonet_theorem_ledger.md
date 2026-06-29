# Holonet Public Theorem Ledger

This ledger turns the Holonet from a narrative into an auditable specification.  Each row has a claim, a status tier, the command or witness that recomputes it, and the output artifact that should be inspected.  The intended public contract is simple:

```bash
holonet verify
holonet audit
holonet bench
```

`verify` checks that the virtual node works.  `audit` re-derives the headline constants from `q=3`.  `bench` separates deterministic operation counts from host-relative timing.  The ledger below is the reader-facing map from claims to executable evidence.

## Status tiers

| Tier | Meaning | Public wording |
|---|---|---|
| E | Exact / theorem / exhaustive computation | “Verified by a finite witness.” |
| S | Simulation / Monte Carlo / finite model | “Measured in simulation under stated assumptions.” |
| P | Physical demonstrator pending | “Falsifiable by the first bench run.” |
| C | Corpus identification / postdiction | “Arithmetically matched or structurally identified; not yet a dynamical derivation.” |
| F | Frontier / conjectural application | “Promising direction, not a proven reduction or built system.” |

## Public audit ledger

| Claim | Tier | Witness / command | Output artifact | Pass condition | Boundary |
|---|---:|---|---|---|---|
| `W(3,3)=GQ(3,3)=SRG(40,12,2,4)` | E | `holonet audit`; `analysis/w33_master_audit.py` | `data/w33_master_audit.json` | 40 points, degree 12, lambda 2, mu 4 | Finite model only; not a hardware run. |
| Diameter-2 routing | E | `analysis/holonet_node.py`; `holonet route` | `data/holonet_node_demo.json` | every route length <= 2 | Classical routing layer. |
| Table-free forwarding | E | `analysis/w33_minimal_architecture.py`; `analysis/w33_holonet_asm.py` | `data/w33_minimal_architecture.json`; `data/w33_holonet_asm.json` | symplectic test reproduces adjacency for all ordered pairs | Firmware listings are abstract targets, not vendor binaries. |
| `Sp(4,3)` / `W(E6)` size 51840 | E | `analysis/w33_isa_encoding.py`; `analysis/w33_one_group_machine.py` | `data/w33_isa_encoding.json`; `data/w33_one_group_machine.json` | closure/order check gives 51840 | Must keep `Sp(4,3)` double cover and projective Weyl extension distinct. |
| One-group machine reading | E/C | `analysis/w33_one_group_machine.py`; `holonet audit` | `data/w33_one_group_machine.json` | same order and actions support processor/network/memory/readout | Exact group actions; broad interpretation is architectural. |
| Bisection 100 and non-planar fabric directive | E | `analysis/w33_noc_floorplan.py`; `holonet audit` | `data/w33_noc_floorplan.json` | bisection lower bound met by explicit cut | VLSI/photonic hardware implication is engineering interpretation. |
| Link scheduling / one-factorization | E | `analysis/w33_scheduler_os.py` | `data/w33_scheduler_os.json` | 12 conflict-free perfect matchings | Physical timing closure still pending. |
| Contextual fraction `1/10` | E/P | `analysis/w33_contextual_fraction.py`; `analysis/w33_ks_inequality.py` | `data/w33_contextual_fraction.json`; `data/w33_ks_inequality.json` | max satisfiable contexts 36/40; CSW 10 > 7 | Exact finite witness; physical certification pending. |
| Parity law: contextual iff `q` odd for `q=2,3` scan | E | `analysis/w33_audit_qscan.py` | `data/w33_audit_qscan.json` | `q=2` has ovoid/CF 0; `q=3` no ovoid/CF 1/10 | Current witness scans sister geometries in scope, not every finite polar space. |
| Magic robustness `R=3` and classical cost `9^t` | E/S | `analysis/w33_magic_dial.py`; `analysis/w33_provable_advantage.py` | `data/w33_magic_dial.json`; `data/w33_provable_advantage.json` | exact robustness plus unbiased small-`t` signed Monte Carlo | Quantum advantage is priced, not supplied by laptop. |
| QEC correction of all single-qutrit errors | E | `analysis/holonet_qec_demo.py` | `data/holonet_qec_demo.json` | all 40 single-qutrit errors correct to fidelity 1 | `[[5,1,3]]_3` stand-in, not full `[[66,8,3]]_3` device. |
| Threshold curve `P_L ~ A p^2` | S | `analysis/holonet_threshold_demo.py`; `analysis/holonet_ft_threshold.py` | `data/holonet_threshold_demo.json`; `data/holonet_ft_threshold.json` | perfect-syndrome curve bends below break-even; repeated measurement restores noisy case | Monte Carlo / model; full circuit-level implementation pending. |
| Qutrit teleportation | E | `analysis/holonet_teleport_demo.py` | `data/holonet_teleport_demo.json` | fidelity 1 for all 9 outcomes | Small exact state-vector demonstration. |
| Self-reproduction / quine fixed point | E | `analysis/holonet_quine.py` | `data/holonet_quine_demo.json` | byte-identical child/grandchild | Von Neumann software notion, not biological claim. |
| Consensus tolerance | S/E | `analysis/holonet_consensus_demo.py` | `data/holonet_consensus_demo.json` | five Byzantine nodes survived; six breaks | Simulated adversary model; formal network proof still separate. |
| Holevo qutrit/OAM boundary | E/C/P | `analysis/w33_io_boundary.py`; demonstrator protocol | `data/w33_io_boundary.json` | `log2(3)` accounting and three-mode alphabet | Physical OAM implementation pending. |
| Packet energy: 72 trits -> 144 host bits | E | `analysis/w33_packet_energy.py` | `data/w33_packet_energy.json` | packet field sum equals 72; binary envelope 144 bits | Traffic accounting, not joule measurement. |
| Retro firmware exports | E | `analysis/w33_holonet_retro_export.py` | `artifacts/holonet_asm/*` | 4004/6502/Z80-style listings verify all ordered pairs | Abstract target listings; no cycle-accurate vendor claim. |
| Firmware-to-fabric accounting `2160 = 30 x 72` | E | `analysis/w33_holonet_firmware_fabric_profile.py` | `data/w33_holonet_firmware_fabric_profile.json` | mirror atlas and Witting admission arithmetic pass | Cross-layer accounting, not throughput. |
| Performance face | S/E | `analysis/holonet_bench.py`; `holonet bench` | `data/holonet_bench.json` | deterministic op counts pass; timings reported as host-relative | Python timing is a floor, not hardware ceiling. |
| Photonic contextuality demonstrator | P | `holonet_demonstrator_protocol_v1.tex`; raw-shot validator/estimators | raw JSONL + estimator outputs | `S>36` and CF consistent with `1/10` | First physical falsifier; no full Holonet build implied. |
| Standard Model / E6 / weak-angle identifications | C | `analysis/w33_physics_bridge.py`; claim-tier spine | `data/w33_physics_bridge.json` | arithmetic ledger matches stated integers | Postdiction/identification unless a dynamical derivation exists. |
| K3 / spectral action / gravity bridge | C/F | `analysis/w33_gravity_spectral_action.py`; `analysis/w33_propinquity_reduction.py` | `data/w33_gravity_spectral_action.json`; `data/w33_propinquity_reduction.json` | spectral moments and named open theorems recorded | Continuum convergence and positivity remain open. |
| Planetary computer / infrastructure applications | F | `holonet_practical_implications.tex` | companion paper | structurally motivated roadmap | Not a built network or proven production protocol. |

## Reader path

1. **Run the VM:** `holonet verify`.
2. **Audit the datasheet:** `holonet audit`.
3. **Measure the classical host:** `holonet bench`.
4. **Read the machine paper:** `holonet_machine.tex`.
5. **Falsify the first physical layer:** `holonet_demonstrator_protocol_v1.tex`.
6. **Grade the grand claims:** `holonet_claim_tiers.tex` and `analysis/BT1907_photonic_holonet_claim_tier_refactor.md`.

## Rule for future claims

Every new claim should enter this ledger with one of the five tiers.  If it has no witness, it cannot be labelled exact.  If it has no physical run, it cannot be labelled physically demonstrated.  If it is an arithmetic match to known measured values, it must say postdiction/identification until a dynamical derivation is supplied.
