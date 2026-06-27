# BT1895 — Demonstrator vs Fault-Tolerant Stack Compiler

BT1895 separates the uploaded Holonet build into two build targets.

## Source anchors

```text
build sheet components:       lines 2085-2091
parameter-free witnesses:     lines 2093-2115
two-layer distinction:        lines 3075-3084
fault-tolerant CV stack:      lines 3086-3098
remaining hardware blockers:  lines 3099-3112
```

## Target A — single-photon demonstrator

Role:

```text
ideal unencoded logical layer and parameter-free witness machine
```

Components:

```text
heralded single-photon source
polarizing beam splitter
symmetric 3-port tritter
0/tau/2tau delay ladder
bin-synchronous electro-optic modulator
polarization rotator at arccos(-2/3)
single-photon detectors
```

Certifies:

```text
Sp(4,3) gate-set logic
routing network
trace-Choi and contextual witnesses
finite Witting transaction accounting
```

Hard boundary:

```text
a single photon has fixed photon number and cannot carry a many-photon GKP grid state
```

So the demonstrator is not the fault-tolerant machine.

## Target B — fault-tolerant CV machine

Role:

```text
GKP(D4) inner code composed with [[240,81,4]]_3 outer Steinberg code
```

Stack:

```text
240 squeezed modes
120 D4 GKP pairs
240 GKP qutrits
[[240,81,4]]_3 outer Steinberg code
81 logical qutrits
```

Remaining physical blockers:

```text
threshold squeezed light
GKP qutrit state generation
degree-3 E6 non-Gaussian resource
programmable beamsplitter / phase / squeeze network
homodyne readout
```

## Compiler verdict

Keep the single-photon Holonet demonstrator and the fault-tolerant CV machine as separate build targets.

```text
single photon = finite logic demonstrator
GKP(D4) o Steinberg = fault-tolerant machine
```

Boundary: build-roadmap compiler only; not a lab bill of materials, threshold proof, or hardware performance claim.
