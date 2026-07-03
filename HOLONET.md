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
| `py -3 analysis/holonet_bench.py` | the performance face: **deterministic op counts** (7 mod-3 ops/route, μ=4) + host-relative throughput (`holonet bench`) |
| `py -3 analysis/w33_doily_mermin.py` | two contextualities separated on W(2): **sign-contextual (Mermin–Peres, exact F₂ obstruction + 6-line certificate) yet selection-noncontextual (ovoid)** — the control arm's CF=0 is the selection statistic only |
| `py -3 analysis/w33_realization_dimension.py` | why one photon in C⁴: **W(2) has NO complete-basis realization in C³** (μ=3 rays can't fit a 1-dim orthocomplement); q=3 is the smallest realizable **and** smallest contextual order |
| `py -3 analysis/w33_contextuality_tax.py` | the contextuality tax: **exhaustive proof that every optimal KS failure set is one movable point-star** (exactly 40, one per point); deficit = q+1 (odd) / 0 (even) — the OS escalation budget = the 9^t spend = **1/10 of the fabric** |

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
