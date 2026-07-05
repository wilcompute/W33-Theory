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
| Parity law: contextual iff `q` odd, `CF=1/(q^2+1)`, scan `q=2,3,4` (GF(4)) | E | `analysis/w33_audit_qscan.py` | `data/w33_audit_qscan.json` | even `q` (2,4) ovoid/CF 0; odd `q` (3,5) no ovoid/CF `1/(q^2+1)`; `q=4` even composite (parity not primality) | Scans sister geometries `q<=4` by default (`--deep` adds `q=5`), not every finite polar space. |
| Explicit even-`q` ovoid (noncontextual control model) | E | `analysis/w33_ovoid_construct.py` | `data/w33_ovoid_construct.json` | `W(2)` 5-ray and `W(4)` 17-ray ovoid each meets every context once and is a cap; `q=3` admits none | Finite construction; the predicted data for the demonstrator's control arm, not a physical run. |
| Sign vs selection contextuality separated on `W(2)` | E | `analysis/w33_doily_mermin.py` | `data/w33_doily_mermin.json` | Pauli sign system unsatisfiable over `F_2` (minimal 6-line Mermin-Peres certificate) while the selection system is satisfied by the ovoid | The parity law's `CF=0` concerns the selection statistic only; the even fabric stays sign-contextual. |
| No complete-basis realization of `W(2)` in `C^3` | E | `analysis/w33_realization_dimension.py` | `data/w33_realization_dimension.json` | `mu=3` distinct rays cannot fit the 1-dim orthocomplement of a non-collinear pair; `q=3` unobstructed (Witting exists, cited); `q=4` open | Counting theorem with verified inputs; `q=3` is the smallest realizable and smallest contextual order. |
| Contextuality tax: every optimal KS failure set is one movable point-star | E | `analysis/w33_contextuality_tax.py` | `data/w33_contextuality_tax.json` | exhaustive ILP + no-good-cut enumeration terminates at exactly 40 failure sets, each the 4 lines through one point, all 40 centers realized; deficit = `q+1` (odd) / 0 (even) | Underwrites the scheduler arc's `36 spreads / movable point-star defect` bridge structurally; no canonical assignment-to-spread bijection claimed. |
| Spread side of the tax: 36 spreads (independent count), 9/10 service rate, uniform defect loading | E | `analysis/w33_spread_star_anatomy.py` | `data/w33_spread_star_anatomy.json` | exact-cover enumeration gives 36 spreads / 9 per line; spread-star intersection = 1 (all pairs) so every spread runs 9/10 under any optimum; exactly 20 optima per center (800 total), occupancy always uniform `(c,c,c,c)`, `c` in {2,3,4}, lit spectrum {11,12,13} | Double occupancy is the minimal class of optima; complete defect/spread incidence re-verified from the scheduler arc's tensor observation. |
| Tax orbits: the 800 optima are four `PSp(4,3)` orbits `360+40+360+40` | E | `analysis/w33_tax_orbits.py` | `data/w33_tax_orbits.json` | transvection closure on points has order 25920 = 51840/2 (double cover distinct, per the spine's warning); 20 center-0 optima generate all 800; (center lit?, load c) a complete orbit invariant; queue invariant global (zero imbalance, spectrum {2,3,4}) | q=5 probe (`--deep`) capped at 40 optima: uniform loading persists, spectrum {4,5,6} = {q-1,q,q+1} — suggestive family law, not exhaustive. |
| Perp states: the canonical 40-orbit is the deleted perps; the GQ axiom is the optimality proof | E | `analysis/w33_perp_states.py` | `data/w33_perp_states.json` | special optimum = `Gamma(p)` exactly (unique per center); flip = full perp (geometric hyperplane); axiom + perp loading (q, q+1) verified at q=2,3,4,5, explaining the spectrum {q-1,q,q+1}; nine ground states stabilizer-transitive (order 648), out-triples = centric triads (common perp 4) partitioning the 27 non-neighbors | Standard GQ objects newly identified with the Pass 58/59 optima; Schlafli-adjacent facts recorded as computed invariants only. |
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
5. **Falsify the first physical layer:** `holonet_demonstrator_protocol_v1.tex`, with its positive control in `holonet_parity_control.tex` (the even-`q` arm that must read `CF=0`).
6. **Grade the grand claims:** `holonet_claim_tiers.tex` and `analysis/BT1907_photonic_holonet_claim_tier_refactor.md`.

## Rule for future claims

Every new claim should enter this ledger with one of the five tiers.  If it has no witness, it cannot be labelled exact.  If it has no physical run, it cannot be labelled physically demonstrated.  If it is an arithmetic match to known measured values, it must say postdiction/identification until a dynamical derivation is supplied.
