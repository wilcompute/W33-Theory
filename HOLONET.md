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
```

`holonet verify` should end with **`ALL PASS — this machine is a working holonet node.`**

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
- **`docs/index.html`** — the interactive results index.

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
