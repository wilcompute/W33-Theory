# The Holonet Machine — Quickstart

[![holonet](https://github.com/wilcompute/W33-Theory/actions/workflows/holonet-ci.yml/badge.svg)](https://github.com/wilcompute/W33-Theory/actions/workflows/holonet-ci.yml)

**Run a universal computer that is also its own network and memory, on the machine in front of you.**

The Holonet is a finite architecture built on the symplectic generalized quadrangle
**W(3,3) = GQ(3,3) = SRG(40,12,2,4)**, in which the processor, the network, and the memory are *one
object*: routing a packet is applying a gate is reading memory. Its classical layer (the Clifford
formalism) is polynomial-time, so the whole architecture — everything but the priced quantum advantage —
runs as software on any computer. This file gets you from zero to a verified, running holonet node in
about five minutes.

> Honest framing in one line: the *architecture of life* (compute, construct, correct, route,
> self-reproduce) is classically emulable and runs here; only the quantum **advantage** is a priced
> resource (classical emulation cost `9^t` for `t` non-Clifford "magic" gates).

## Public reader paths

- **Run it:** install the CLI and run `holonet verify`, `holonet audit`, and `holonet bench`.
- **Audit it:** read `docs/holonet_theorem_ledger.md`, the public claim-to-witness map.
- **Falsify it:** read `holonet_demonstrator_protocol_v1.tex`, the first physical contextuality protocol.
- **Grade it:** read `analysis/BT1907_photonic_holonet_claim_tier_refactor.md`, the claim-tier spine for separating exact architecture, simulation, physical protocol, physics identification, and frontier applications.

---

## 1. Requirements

- Python 3.9+
- `numpy`, `scipy`, `networkx` (for the contextuality / threshold witnesses)

```bash
pip install numpy scipy networkx
```

## 2. Install the `holonet` command (optional)

```bash
pip install -e .          # from the repo root; provides the `holonet` console command
holonet verify            # self-test the whole stack -> PASS/FAIL
```

Without installing, every command also works directly:

```bash
py -3 analysis/holonet_cli.py verify
```

## 3. The five-minute tour

```bash
holonet info                 # the datasheet (processor / network / memory / clock / ...)
holonet route 0001 0010      # route a packet: address IS the route, <= 2 hops, mu=4 multipath
holonet correct              # run a [[5,1,3]]_3 error-correction cycle  -> fidelity 1
holonet teleport             # teleport a qutrit A->B (no-cloning)       -> fidelity 1
holonet reproduce            # splice a W(3,3) child (von Neumann self-reproduction)
holonet verify               # 7 stack checks -> ALL PASS
holonet audit                # re-derive every layer's headline constant from q=3 -> 16 checks, ALL PASS
holonet bench                # the performance face: op counts (forced) + host-relative throughput
holonet bench --compare      # table-free address routing vs a classical table-routed baseline (1170 B -> 0)
holonet bench --compare --scale  # the table-free win grows with q: routing state -> infinity vs 0, hops stay 2
holonet uor                  # content-addressed VM cert, local UOR runtime, OS replay, SHACL shapes
holonet uor --live           # same path plus bounded live UOR proof/SHACL probes
```

`holonet verify` should end with **`ALL PASS — this machine is a working holonet node.`**

`holonet audit` is the stronger statement: it recomputes (does not store) the headline constant of
*every* architectural layer — the network `SRG(40,12,2,4)` / diameter 2 / `λ₂ = 2` / bisection 100, the
processor runtime `51840 = 24·2160 = |W(E6)|` and its 40 line-contexts, the contextuality (max partial
ovoid 7, max satisfiable contexts 36/40 → `CF = 1/10`, CSW `χ = 10 > 7`), the magic robustness 3, the
distance-3 break-even and Byzantine bound 5, the Holevo capacity `log₂3`, the 7-op minimal forwarding,
and the ternary tax `2/log₂3` — straight from the single integer **q = 3**, and reports one pass/fail
ledger. The device specification is its own audit: there is no separate trusted checker.

## 4. The runnable witnesses (each prints its own result + writes `data/*.json`)

The machine, executed:

| Run | What it demonstrates |
|---|---|
| `py -3 analysis/holonet_node.py` | the universal VM: network + processor + magic dial + self-reproduction |
| `py -3 analysis/holonet_qec_demo.py` | the memory **corrects** every single-qutrit error to fidelity 1 |
| `py -3 analysis/holonet_teleport_demo.py` | two nodes **teleport** a state (fidelity 1, all 9 outcomes) |
| `py -3 analysis/holonet_quine.py` | the node **reproduces** itself (a verified quine fixed point) |
| `py -3 analysis/holonet_quantum_packet.py` | a quantum packet delivered across the fabric |
| `py -3 analysis/holonet_consensus_demo.py` | leaderless consensus, 1/3-per-round, **5-Byzantine / 11-crash** |
| `py -3 analysis/holonet_threshold_demo.py` | the fault-tolerance curve: `P_L ~ A p^2`, break-even `p_th = 1/A` |
| `py -3 analysis/holonet_ft_threshold.py` | circuit-level: repeated measurement **restores** the threshold |
| `py -3 analysis/holonet_scorecard.py` | plots the threshold + contextuality figure (`holonet_scorecard.png`) |
| `py -3 analysis/w33_minimal_architecture.py` | the node runs on a **mod-3 ALU + ~100 bytes** (a ternary VM) |
| `py -3 analysis/w33_instance_architecture_map.py` | explicit W(3,3) instance map: points = sites/registers/addresses, lines = K4 buses, spreads = global clock frames, spread graph = scheduler; routing table compresses from **1170 B to 0** |
| `py -3 analysis/w33_recursive_instance_compression.py` | recursive instance law: `40^n` leaves, `I_n=(40^n-1)/39` W33 instances, route depth `8n`, commit clock `4(7^n-1)`, and at level 6 **122,879,999,970 routing bytes** / **190,726,564,056 listed control bytes** avoided while the mirror bus remains at `1/4` utilization |
| `python3 analysis/w33_fractal_microvm_runtime.py` | executable recursive state DAG: level 6 denotes **105,025,641 network VMs + 4,096,000,000 addressable leaves = 4,201,025,641 stateful VMs** represented by seven uniform node blobs; the fresh send writes seven path states plus one receipt, while execution writes seven path states; 19/19 checks |
| `python3 analysis/holobox.py --help` | HoloBox lifecycle CLI: build, inspect, verify, addressed run, routed send, fork, and route over one immutable leaf/network loader contract |
| `gap -q -b analysis/w33_fractal_microvm_routing.g` | independent 7/7 GAP route certificate: W33 diameter 2 and logical `2n` line-bus bound; distinct from the older chart-aware `8n = (3+5)n` lowering |
| `gap -q analysis/w33_pass4936_chamber_packet_matrix_units.g` | exact 20/20 chamber logic certificate: the rank-48 packet is literally `M₂(Q)` on a two-state multiplicity coordinate repeated over 24 representation lanes; complete `HP`/`HL` selector families compress to packet reflections, but no individual selector intertwiner or physical qubit is claimed |
| `gap -q -b analysis/w33_pass4937_adjoint_dual_number_controller.g` | exact 30/30 finite control-plane target: `F₃¹⁰ ⋊ PGSp(4,3)` acts by `v ↦ vA_g+w`, its 59,049 offsets have 17 symmetry classes, and it is separated by its trivial center from the equal-order dual-number symplectic group; no HoloBox opcode is implemented |
| `python3 analysis/w33_pass4870_steiner_w33_quadratic_bridge.py` | exact Steiner three-cover: 120 triangles form forty intrinsic three-element fibers, W33 adjacency lifts to complete `K₃,₃`, and the first equivariant Steiner-to-adjoint maps form a two-dimensional quadratic Hom space; no preferred map or coupling is selected |
| `python3 analysis/w33_pass4873_two_order1440_extensions.py` | fail-closed group check: marked-residue `S₆×C₂` and duad–syntheme `Aut(S₆)` both have order 1440 but are nonisomorphic, separated by centers `2/1`, involutions `151/111`, and the presence of 360 order-eight elements only in the latter |
| `python3 analysis/w33_pass4874_steiner_w33_association_scheme.py` | complete four-class scheme on the 120 Steiner triangles: valencies `1,2,27,36,54`, W33 fiber-constant sector `1+24+15`, and transverse sector `20+60`; the relations are canonical, but naming points inside each three-element fiber remains gauge data |
| `py -3 analysis/w33_component_execution_simulator.py` | runnable component trace: projective address -> symplectic route -> unique K4 line bus -> spread-clock frame -> durable commit marker |
| `py -3 analysis/w33_wrapped_program_control_comparison.py` | wraps real commands and compares conventional control tables to generated W33 packet control; the demo wraps sum-of-squares and Rule-110 with **0 persistent routing-state bytes** |
| `py -3 analysis/w33_q6_tomotope_recursive_packet_abi.py` | fuses Q6-style body routing, the **48**-tick tomotope body, **2160** mirror slots, and the recursive `40^n` packet ABI while keeping `40^n` leaf packets distinct from `I_n` internal W33 instances |
| `py -3 analysis/w33_component_browser_demo.py` | generates `docs/w33_component_browser_demo.html`, a clickable point-to-point demo: pick source/destination and watch route, K4 bus, spread clock, and commit update |
| `py -3 analysis/w33_python_bytecode_packet_lifter.py` | disassembles Python functions and maps each bytecode op into a W33 packet route plus Q6/tomotope body slot; sample lifter covers sum-of-squares and Rule-110 |
| `py -3 analysis/w33_binary_object_loader.py` | reversible object loader: arbitrary bytes -> six-trit digits -> 81-trit W33-addressed pages -> exact bytes again |
| `py -3 analysis/w33_packet_vm.py` | executes the lifted bytecode packet stream and checks that routed dynamic packet events reproduce the source results |
| `py -3 analysis/w33_device_port_model.py` | models USB-style control/bulk/interrupt/isochronous endpoints as typed W33 boundary packets with payload roundtrips |
| `py -3 analysis/w33_universal_program_object_pipeline.py` | end-to-end wrapper witness: program bytes, packet VM execution, device ports, and output bytes all share one W33 ABI |
| `py -3 analysis/w33_tiny_risc_packet_isa.py` | fixed-width binary ISA object: 40 program bytes load as W33 trit pages and execute 38 routed packet events to produce `140` |
| `py -3 analysis/w33_interactive_os_port_demo.py` | deterministic OS replay: keyboard command, disk object load, tiny-RISC execution, and serial output all use W33 port packets |
| `py -3 analysis/w33_program_compression_economics.py` | payload/control economics: six-trit bytes expand on binary hosts, while generated W33 topology avoids persisted route/control tables |
| `py -3 analysis/w33_stack_bytecode_adapter.py` | WASM-like stack bytecode object: 69 bytes lower into 23 tiny-RISC ops and run as 114 routed packet events to produce `140` |
| `py -3 analysis/w33_os_replay_browser_demo.py` | generates `docs/w33_os_replay_browser_demo.html`, a clickable OS replay over keyboard/disk/serial W33 packets |
| `py -3 analysis/w33_workload_economics_sweep.py` | workload-level economics: one session, 10 objects, 40 events, and 100 mixed sessions with generated-control savings up to `510400` bytes |
| `py -3 analysis/w33_chain_operator_spectral_completion.py` | resolves the `G40 = 2I-A` boundary: `G40` is rank 16, the missing exact integral channel is `R40 = 20I+5A-2J` with rank 24, and `G40+R40` is full-rank |
| `py -3 analysis/w33_packet_chain_profile.py` | profiles stack-bytecode VM traffic against `(G40,R40)`: 199 route hops carry aggregate bill `G40=1194`, `R40=5970`, `H40=7164` |
| `py -3 analysis/w33_bose_mesner_chain_calculus.py` | promotes the chain audit to the full integer channel basis `U40=J`, `R40=20I+5A-2J`, `S40=8I-4A+J`, with `U40/40+R40/30+S40/24=I` and `G40=(S40-U40)/4` |
| `py -3 analysis/w33_channel_aware_multipath_scheduler.py` | tests all `1080` two-hop ordered pairs and `4320` relay options: channel bill and spread-clock cost are invariant, while greedy line-bus balancing tightens load from `36..180` to `50..58` around ideal `54` |
| `py -3 analysis/w33_perfect_multipath_balancer.py` | proves the full two-hop workload admits a perfect relay certificate: `1080*2/40 = 54`, and every one of the `40` W33 line buses is used exactly `54` times |
| `py -3 analysis/w33_perfect_route_selector_runtime.py` | packs the perfect relay certificate as a `270`-byte runtime selector; direct routes add `12` line uses, so the full nonidentity all-pairs workload balances every line bus at `66` |
| `py -3 analysis/w33_reversal_symmetric_route_selector.py` | halves the selector to `135` bytes by choosing one relay per unordered nonlocal pair: every line hits `27`, both time directions give `54`, and direct routes close `66 = 12 + 2*27` |
| `py -3 analysis/w33_line_relay_balanced_route_selector.py` | strengthens the `135`-byte selector: the unordered line buses are `{27:40}` and relay cores hit the forced split `{13:20,14:20}` while the full line law stays `{66:40}` |
| `py -3 analysis/w33_selector_equivariance_obstruction.py` | proves the local obstruction to a deterministic fully equivariant relay formula: an order-`576` symplectic subgroup has ordered-pair stabilizer `24`, transitive on the four relays |
| `py -3 analysis/w33_line_pair_factorization_scheduler.py` | turns the selector into a bus timetable: `540 = 27*20` unordered routes factor into `27` conflict-free frames, each using all `40` W33 line buses exactly once |
| `py -3 analysis/w33_balanced_selector_runtime_adapter.py` | exposes the balanced `135`-byte selector as a runtime route API with generated direct routes, shared reversal relays, and full all-pairs line load `{66:40}` |
| `py -3 analysis/w33_selector_tomotope_orientation_quotient.py` | aligns the selector ladder with the Q6/tomotope ABI: `135 -> 540 -> 1080 -> 2160 = 45*48`, recorded as a quotient/factor bridge rather than an unproved isomorphism |
| `py -3 analysis/w33_toroidal_h6_66_bridge.py` | verifies the new scheduler `66` is exactly the `h=6` complete-adjacency edge count `E(K12)=66`, with Csaszar-type `(12,66,44)` and Szilassi-type dual `(44,66,12)` |
| `py -3 analysis/w33_gc_operation_66_bridge.py` | checks the local Grünbaum-Coxeter table: maximal expanded 11-cell starts at `66`, omnitruncated 11-cell starts at `660=10*66=|PSL(2,11)|`, and tomotope expansion/omni sit at `48/96` |
| `py -3 analysis/w33_scheduler_economics_benchmark.py` | level `1..8` economics chart: conventional routing/control tables versus generated W33 control, including level-8 `305,162,502,564,056` listed control bytes avoided |
| `py -3 analysis/w33_vm_speedup.py` | efficiency by matching: zero routing table, the von Neumann gap eliminated |
| `py -3 analysis/w33_tritcpu_emulator.py` | the router as a **22-instruction program on an emulated 4-bit CPU** (Intel 4004) |
| `py -3 analysis/w33_ternary_energy.py` | the ternary-vs-binary **encoding tax** (1.26×, 25% wasted states) |
| `py -3 analysis/w33_holonet_asm.py` | a tiny holonet assembler: 4-bit target plus **6502-style 8-bit target** with MUL/MOD synthesized |
| `py -3 analysis/w33_holonet_retro_export.py` | exports deterministic **4004 / 6502 / Z80-style listings** plus golden traces |
| `py -3 analysis/w33_packet_energy.py` | the per-packet traffic bill: **72 trits -> 144 binary host bits** for the minimal control packet |
| `py -3 analysis/w33_holonet_firmware_fabric_profile.py` | firmware-to-fabric accounting: **2160 = 30 × 72**, with `13/40` Witting admission and `117/5` expected trits/query |
| `py -3 analysis/w33_master_audit.py` | the machine audits itself: **16 layer constants re-derived from q=3** in one pass/fail ledger (`holonet audit`) |
| `py -3 analysis/w33_audit_qscan.py` | the parity law across **W(q) for q=2,3,4** (q=4 = GF(4)): **CF = 0 for even q, 1/(q²+1) for odd q** — contextual iff q is odd, **parity not primality** (`--deep` adds q=5) |
| `py -3 analysis/w33_ovoid_construct.py` | the explicit **noncontextual control model**: constructs & verifies the **W(2) 5-ray / W(4) 17-ray ovoid** (CF=0); q=3 has none — the demonstrator's control arm |
| `py -3 analysis/holonet_control_arm.py` | the **two-arm discriminator**: the same estimators (`bt1901`/`bt1904`) return **CF≈1/10 (q=3) vs CF≈0 (even q)** on the two fixtures — runnable end-to-end |
| `py -3 analysis/w33_doily_mermin.py` | two contextualities separated on W(2): **sign-contextual (Mermin–Peres, exact F₂ obstruction + 6-line certificate) yet selection-noncontextual (ovoid)** — the control arm's CF=0 is the selection statistic only |
| `py -3 analysis/w33_realization_dimension.py` | why one photon in C⁴: **W(2) has NO complete-basis realization in C³** (μ=3 rays can't fit a 1-dim orthocomplement); q=3 is the smallest realizable **and** smallest contextual order |
| `py -3 analysis/w33_contextuality_tax.py` | the contextuality tax: **exhaustive proof that every optimal KS failure set is one movable point-star** (exactly 40, one per point); deficit = q+1 (odd) / 0 (even) — the OS escalation budget = the 9^t spend = **1/10 of the fabric** |
| `py -3 analysis/w33_spread_star_anatomy.py` | the spread side of the tax: **36 spreads re-counted independently** (exact cover, 9 per line); every spread meets every star once → **every spread runs at exactly 9/10 under any optimum**; exactly **20 optima per center (800 total)**, defect loading always uniform (c,c,c,c), c∈{2,3,4} — double occupancy is the minimal class |
| `py -3 analysis/w33_tax_orbits.py` | the tax orbits: **the 800 optima are four PSp(4,3) orbits (360+40+360+40)** — the machine's one group (25920 on points; 51840 is the double cover) moves the defect's ground states transitively; **queue invariant**: zero escalation imbalance across all 800; `--deep` probes q=5 (spectrum {q−1,q,q+1}, capped) |
| `py -3 analysis/w33_perp_states.py` | the perp states: **the canonical 40-orbit IS the deleted perps Γ(p)** (flip = full perp, a geometric hyperplane); **the GQ axiom is the optimality proof** (q=2..5), so the spectrum {q−1,q,q+1} = {grounds, deleted perp, full perp}; 9 grounds stabilizer-transitive, out-triples = **centric triads partitioning the 27 non-neighbors** |
| `py -3 analysis/w33_ground_affine_plane.py` | the affine plane law: per center the optima close **exhaustively at 2(q²+1)** (20 at q=3, **52 at q=5**); the q² grounds form **AG(2,q)** — neighbors = lines, **defect lines = parallel classes**; grounds are the all-centers-in-perp triads (**no optimizer needed**); at q=3 the plane is the **Hesse configuration = the single-qutrit phase space**, its 4 MUB striations = the 4 defect contexts |
| `py -3 analysis/w33_interrupt_controller.py` | the interrupt controller (VM-track fusion): **closed-form vector table** ground(T) = T + (Γ(p) − T⊥); **migration price law** — re-vector in place = 6 rays, **edge migration = 3** (the 8 cheap channels sit at the ground's own center quad); 2100-event run with **every tax theorem held as a runtime invariant** |
| `py -3 analysis/w33_packet_vm_kernel.py` | mode-2 execution with a real kernel: the lifted TritCPU router runs **through the interrupt controller** — 1600/1600 outputs identical, 46,400 line-legal hops, escalations priced, relocations at exactly 3 rays |
| `py -3 analysis/w33_defect_aware_placement.py` | defect-aware paging: the 27-point safe zone **is** the AG(2,3) phase directory; **page bill law** — a constant 9 points per relocation (edges win strictly); re-keying is all-or-nothing (6 triples intact / 3 rebuild) |
| `py -3 analysis/w33_defect_walk_telemetry.py` | the walking defect: **quad-constrained nearest-neighbor walk** (100% of 1023 steps in the pre-move center quad, edges only, 3 rays), emitted as a spread-clock JSONL trace |
| `py -3 analysis/w33_kernel_dynamics.py` | kernel dynamics: the defect walk is **uniformly stationary** (360 grounds 8-regular + connected; gap 0.32, mix ~23); **re-keying is addressed** (rebuilt triples = the AG-line of the old center, quads meet in exactly {old center}); a live pipeline runs programs+pages+walk; and **the fabric logs itself** — 150/150 relocation origins decode from 3 markers + geometry, no interrupt log |
| `py -3 analysis/w33_scheduler_audit_backend.py` | wires Pass 66's self-logging into the parallel track's **BT1808 scheduler**: all **480 directed edges origin-decode uniquely** (3 rebuilt quads meet in exactly the departing center), a 400-step scheduler walk replays edge-for-edge from markers, and all 1440 rows become **geometrically auditable** |
| `py -3 analysis/w33_cheap_channel_spectrum.py` | the exact mixing time: the 360-ground cheap-channel graph is **rank-8 (not SRG)**, spectrum `{8,(1±√97)/2,3,1,−1,−3,−4}` proved by integer trace moments; **exact spectral gap (15−√97)/16** |
| `py -3 analysis/w33_page_bill_unification.py` | **one law, two proofs**: my safe-zone overlap (Pass 65) and their TD(4,3) churn (BT1809/1816) are the same nine points for all 1560 moves; the {3:6,0:3} vs {2:9} split is the **line-vs-transversal** dichotomy of the AG(2,3) directory |
| `py -3 analysis/w33_phase_space_bundle_wigner_accounting.py` | the phase-space bundle: **40 nodes × 9 grounds = one 360-state PSp(4,3) orbit** with stabilizer 72, rank 15, subdegrees `[1,3,4,8,8,24×8,72,72]`; center gluing spectrum separates same/collinear/non-collinear fibers; local Strange-state Wigner fuel is **one −1/3 phase point + eight +1/6 points**, L1 = 5/3, mana = log(5/3), so the negative site has **360 global placements** |
| `py -3 analysis/holonet_bench.py` | the performance face: **deterministic op counts** (7 mod-3 ops/route, μ=4) + host-relative throughput (`holonet bench`) |
| `py -3 analysis/holonet_wrap.py --optimize ... -- <cmd>` | wraps any classical command in a Holonet packet envelope and now compiles that envelope under `active-ticks` or `clock-slots`; the Rule-110 demo is `8/13` active-policy ticks/slots versus `7/7` clock-policy ticks/slots |
| `py -3 analysis/holonet_vm_demo_launcher.py` | one-button VM demo: interface proof, substrate stub, side-channel suite, and the same wrapped Rule-110 command run under both scheduler policies |
| `py -3 analysis/holonet_uor_mock_runtime.py` | local UOR-shaped runtime for all 9 advertised adapter stages while public POST access is blocked |
| `py -3 analysis/holonet_os_scheduler.py` | replayable Holonet OS tick trace: 33 packets dispatched in 8 conflict-free spread ticks |
| `py -3 analysis/w33_spread_contextual_microkernel_bridge.py` | stricter line-context microkernel: 36 spreads = KS ceiling 36, the 4-context deficit localizes as a movable point-star double-occupancy defect, 56 hop-line ops, 14 active execution ticks |
| `py -3 analysis/w33_line_context_compiler.py` | compiler from wrapped packets to packet DAG, hop-line DAG, and verified spread-clock microcode; venv SciPy certifies the 14-active-tick optimum and emits a 15-slot clock-native schedule |
| `py -3 analysis/w33_defect_spread_tensor.py` | 1440-slot colored defect/spread bus: row equalities reconstruct W(3,3), spread overlap graph has spectrum `{15, 3^15, -3^20}` |
| `py -3 analysis/w33_spread_clock_graph.py` | 36-frame clock graph: spread 4-overlap is `SRG(36,15,6,6)`; 8 OS ticks embed in 10 slots, the 14-tick optimum in 22 slots, and the clock-native schedule in 15 slots |
| `py -3 analysis/w33_clock_policy_stress.py` | active-vs-clock-native policy stress: certified 14/22 vs 15/15 anchor, then repeated wrapper DAGs `1x..6x` stay connector-free and save 8, 15, 21, 25, 25, 38 clock slots |
| `py -3 analysis/w33_packet_latency_benchmark.py` | packet-completion latency, not just total slots: certified one-copy row has clock-native finishing `28/33` packets earlier; deterministic `1x..4x` rows finish `23,52,80,106` packets earlier |
| `py -3 analysis/holonet_uor_shacl_shape_check.py` | Holonet-UOR certificate shape validation, with optional live UOR SHACL witness probing |
| `py -3 analysis/holonet_uor_browser_demo.py` | browser replay at `docs/holonet_uor_os_replay.html`: OS ticks, active-optimal microkernel, expanded clock walk, clock-native microkernel, and a clickable SVG 36-frame clock inspector |

The physics/computer-science core:

| Run | What it shows |
|---|---|
| `py -3 analysis/w33_contextual_fraction.py` | the contextual fraction **1/10** derived from no-ovoid geometry |
| `py -3 analysis/w33_ks_inequality.py` | the noncontextual inequality: classical **S ≤ 36** vs quantum **40** |
| `py -3 analysis/holonet_ks_experiment.py` | the bench test simulated: clears the bound at 5σ with ~840 photons |
| `py -3 analysis/w33_magic_dial.py` | the quantum advantage executed: signed Monte Carlo, cost `~9^t` |
| `py -3 analysis/w33_isa_encoding.py` | the ISA: Clifford opcode group `Sp(4,3) = 51840 = \|W(E6)\|` + 1 cubic |
| `py -3 analysis/w33_one_group_machine.py` | one group `W(E6)` = processor = network = memory = readout |
| `py -3 analysis/w33_architecture_capstone.py` | the full datasheet + falsifiable-prediction table |

## 5. The test suite

```bash
python -m pytest tests/test_holonet_vm.py -q     # 13 exact checks of the VM
```

## 6. Where the architecture is written up

- **`photonic_holonet.tex`** — the full theory (physics + machine), the canonical paper.
- **`holonet_machine.tex`** — the standalone, submission-grade *Machine* paper (the computer-engineering
  arc as one coherent document).
- **`holonet_practical_implications.tex`** — the implications paper (data centers, decentralized compute,
  virtual machines, energy, and the frontier applications).
- **`holonet_demonstrator_protocol_v1.tex`** — the first physical falsifier: a tabletop Witting/KS contextuality protocol for measuring `CF = 1/10`.
- **`holonet_parity_control.tex`** — the **positive control arm**: the same apparatus on an even-order fabric (W(2)/W(4)) must read `CF = 0`, turning the test into a two-arm discriminator (ships with the explicit ovoid model).
- **`docs/holonet_theorem_ledger.md`** — the public theorem/audit ledger mapping each claim to its witness, output, tier, pass condition, and boundary.
- **`analysis/BT1907_photonic_holonet_claim_tier_refactor.md`** — the claim-tier refactor spine for keeping exact, simulated, physical, identified, and speculative claims separate.
- **`docs/index.html`** — the interactive results index.
- **`docs/holonet.html`** — the interactive **playground**: route a packet, drive the Clifford
  register, run the contextuality witness, and reproduce a node, all live in the browser (no install).

## 7. One honest paragraph

Everything in §3–§5 is classical, exact, and runs today: the routing and Clifford layer are exact,
the error correction and teleportation are exact small state-vector simulations, the consensus and
threshold are Monte-Carlo runs, and the contextuality numbers (α = 7, the 36/40 bound, the 1/10
fraction) are computed from the W(3,3) geometry. The quantum **advantage** is the one thing a laptop
cannot supply — it is the priced `9^t` dial, executed here only for small `t` via the quasiprobability
simulator. The `[[5,1,3]]_3` code is a runnable stand-in for the substrate's `[[66,8,3]]_3` (same
distance-3 mechanism, different size). No physical photonic build exists yet; the first milestone is the
benchtop contextuality test (`holonet_ks_experiment.py`), decided by a few hundred photons.

> One photon. One PBS. One tritter. One EOM. One loop. Measure 1/10.
