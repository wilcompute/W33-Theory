# WRF Flow-Pattern Memory Findings

Date: 2026-06-03

Status: exploratory research note. This is intentionally not folded into
`witting_architecture_v2.tex` yet.

## Short Finding

The user's intuition is technically promising if it is framed as **pattern-addressed
flow**, not as ordinary volatile memory. In that model, the physical substrate is
always moving, while the "stored datum" is the stable invariant of a bounded trace:
a canonical cycle, attractor, spectrum, stationary envelope, or receipt-bearing
computation trace.

The key architectural move is:

```text
static datum at address A
    becomes
canonical invariant of a repeatable flow pattern P, with CID = H(canon(P))
```

This is a natural fit for WRF because UOR already says an object should be identified
by what it is rather than where it is. The flow-pattern extension would say that a
process can also be identified by the invariant of the trace it repeatedly emits.
That makes "memory" a certified pattern of motion, not a passive cell.

## External Architecture Scan

The outside hardware trend is already moving away from static CPU/memory separation:

- SambaNova's RDU dataflow architecture maps AI models to operation graphs and streams
  activations through a pipeline to reduce memory movement:
  <https://sambanova.ai/products/dataflow-architecture>
- Groq's LPU architecture uses compiler-controlled deterministic execution, on-chip
  SRAM as primary storage, and precisely scheduled chip-to-chip arrival:
  <https://home.cloud.groq.io/lpu-architecture>
- IBM NorthPole explicitly blurs the compute/memory boundary by eliminating off-chip
  memory during inference and presenting externally as an active memory chip:
  <https://research.ibm.com/publications/neural-inference-at-the-frontier-of-energy-space-and-time>
- Cerebras Weight Streaming disaggregates parameter storage from wafer-scale compute
  while scheduling weights as a stream:
  <https://www.cerebras.ai/press-release/cerebras-systems-announces-worlds-first-brain-scale-artificial-intelligence-solution>
- SambaNova SN40L combines streaming dataflow with a three-tier memory system to attack
  the AI memory wall:
  <https://arxiv.org/abs/2405.07518>
- Reservoir computing treats nonlinear dynamics as the computational resource; the
  readout observes the reservoir trace rather than storing every intermediate state:
  <https://arxiv.org/abs/2307.15092>
- Recent dynamic physical reservoir work emphasizes sparse physical networks whose
  internal nonlinear dynamics maintain useful temporal behavior:
  <https://arxiv.org/abs/2505.16813>
- Memristive in-memory computing attacks the von Neumann communication bottleneck by
  computing inside memory arrays:
  <https://link.springer.com/article/10.1007/s12200-022-00025-4>

None of those sources proves WRF. The useful connection is architectural: industry is
already converging on movement-as-compute, compute-near-memory, deterministic dataflow,
and physical dynamics. WRF can make that convergence referenceable by giving the trace
itself a UOR-addressable invariant.

## Repo Anchors

The current repo already has exact finite machinery that looks like flow-pattern memory:

- W33 directed transport: 40 vertices, 240 edges, and 480 directed edges.
- Hashimoto nonbacktracking flow: each directed state has 11 legal continuations.
- Doob/Parry/KMS loop conditioning: closed paths are not just paths; they are trace
  objects under a closure boundary.
- QEC Ouroboros ledger: `480 = 240 + 240` splits accepted bonds from heralded
  return/syndrome slots.
- Closure clock: `G=(1/2)S`, `G^6=0`, finite impulse depth 5.
- Toroidal Markov transport: a 7+1 state flow relaxes to a uniform stationary envelope
  with count resolution by 4 ticks and probability-packet resolution by 7 ticks.
- Local UOR Framework checkout: version 6.3.0, 16 namespaces, 218 classes, 446
  properties, and 846 named individuals; the framework includes content addressing,
  computation traces, certificates, state, and conformance gates.

## Probe Results

Script: `papers/dahn_asi_toe/wrf_flow_pattern_probe.py`

Output: `papers/dahn_asi_toe/wrf_flow_pattern_probe_results.json`

The probe rebuilds W(3,3) directly over projective `F_3^4`, constructs the 480-state
nonbacktracking carrier, adds a deterministic local routing rule, canonicalizes
cycle orbits, and checks the existing Markov/closure-clock analogues.

Summary of the successful run:

| Check | Result |
| --- | --- |
| W33 vertices | 40 |
| W33 edges | 240 |
| Directed nonbacktracking states | 480 |
| SRG parameters | `(40,12,2,4)` |
| Nonbacktracking branch count | `11` for all 480 directed states |
| Functional flow attractors | 2 attractors |
| Cycle lengths | 15 and 16 |
| Largest basin | 339 of 480 states, about 70.625 percent |
| Selected cycle CID | `8cbe04bd8b7107facc8d1f4b` |
| CID stability | invariant under rotation and reversal |
| Markov active-count horizon | 4 ticks |
| Markov probability-packet horizon | 7 ticks |
| Closure-clock nilpotence | `G^6=0`, impulse depth 5 |
| UOR local anchor | Framework v6.3.0 parsed successfully |

The nontrivial result is the CID stability. A moving trace can be sampled at a different
phase and still recover the same canonical pattern address. This is the seed of a
hardware/software memory primitive:

```text
write(pattern)  = inject/control a local flow until it locks to the target attractor
read(flow)      = sample enough of the trace to recover canon(pattern)
address(flow)   = H(canon(pattern))
compute(A, B)   = couple two flow cells and canonicalize the emergent output trace
repair(flow)    = route deviations through a return/syndrome channel until the invariant returns
```

## Proposed Primitive: Encapsulated Flow Cell

An **Encapsulated Flow Cell** is a bounded local dynamical system:

```text
x_{t+1} = F_theta(x_t, u_t, s_t)
P       = canon(trace(x_0, x_1, ..., x_T))
CID     = H(P)
```

where:

- `x_t` is the moving physical/software state;
- `theta` is the tile-local routing/programming configuration;
- `u_t` is external input;
- `s_t` is syndrome/receipt/control feedback;
- `P` is the canonical trace invariant;
- `CID` is the UOR-style reference to the pattern.

This differs from a cache line or register because the cell is never "at rest." The
stable object is the equivalence class of the trace under allowed symmetries such as
time shift, reversal, gauge, or finite control-plane relabeling.

## Hardware Interpretation

Possible physical forms:

- photonic or RF ring/waveguide loops whose phase-coded circulating pattern is the datum;
- memristive or spintronic reservoirs whose attractor class is the datum;
- wafer-scale packet loops where a closed routing trace is the datum;
- network-switch fabric loops where the repeating BIER/Oko path class is the datum;
- W33/Witting tiles where the directed-edge carrier provides the finite routing alphabet.

The WRF-specific hardware idea is not just "dataflow." It is **referenceable dataflow**:
the trace has a canonical object identity, a scheduler, a receipt, a finality event, and
an economic envelope.

## Software Interpretation

The software stack can model the same primitive before custom hardware exists:

- UOR records the canonical trace witness and content-derived address.
- HLIX schedules the projection that maintains or transforms the flow.
- Oko finalizes state transitions and prevents conflicting pattern claims.
- Smart Assets meter the sustained flow, not merely a one-time file write.
- The W33 control plane supplies compact routing constants: `40`, `240`, `480`, `11`,
  `39+120+81`, `480=240+240`, and `0->81->162->81->0`.

## What Still Needs Work

This should not enter the paper as a mature architecture claim until at least four
things are tested:

1. **Write protocol.** How does software reliably inject a target pattern into a noisy
   flow cell?
2. **Noise model.** What perturbations preserve the canonical invariant, and what
   perturbations require QEC-style return routing?
3. **Coupling algebra.** What is the exact operation law when two flow cells interact?
4. **Capacity accounting.** How many distinguishable stable trace classes exist under
   realistic read windows and error margins?

The current probe supports the direction, not the full architecture. The strongest next
experiment is a capacity/noise harness: enumerate many W33 local routing rules, measure
cycle count, basin size, minimum trace distance between CIDs, and recovery after random
state perturbations.

## Paper Boundary

Do not add this to `witting_architecture_v2.tex` yet as final prose. The safe current
language is:

> Exploratory WRF research is testing whether future WRF memory can be represented as
> referenceable trace invariants rather than static cells.

The stronger language:

> WRF memory is encapsulated flow whose stable pattern is the stored datum.

should wait until the write/noise/coupling/capacity harness exists.
