# Passes 2960–2966 — physical observer, coherent M36, dihedral OAM curvature, and reversible compilation

## Evidence ladder

- **Exact finite mathematics:** Passes 2960, 2962, 2965, and 2966.
- **Exact for stated circuit/noise models:** Pass 2961.
- **Configurable engineering model:** Pass 2963; all supplied profiles are synthetic.
- **Exact reversible gate network:** Pass 2964; physical Toffoli decomposition and placed hardware remain open.
- **Pending observed evidence:** Icarus simulation, Yosys/nextpnr placement, canonical blueprint/site integration, and three-PDF builds.

## Pass 2960 — minimum-incidence realization of the optimal fifteen-probe observer

The exact distance-four observer factors through the ternary single-parity-check code `[5,4,2]_3` with linear forms

```text
x0, x1, x2, x3, x0+x1+x2+x3.
```

All sixteen systematic witnesses are monomially equivalent. Sharing each linear form across its three affine support offsets reduces linear-form incidence from `24` to `8`, an exact factor of three. Only one four-trit parity mixer is non-native; a balanced tree uses three ternary adders at depth two. The pair-distance histogram remains `{4:810, 6:810, 8:1215, 10:405}`.

A structural reversible decoder recovers the four systematic trits with eight NOT and eight CNOT operations. The fifth triplet remains a parity syndrome.

## Pass 2961 — coherent, correlated, and flagged-leakage M36 analysis

Across the 189 single-location Pauli axes of the compiled deep-M36 branch, the exact quadratic susceptibility spectrum is

```text
0^14, (1/18)^66, (2/27)^41, (1/6)^22, (2/9)^46.
```

Common systematic Hadamard-axis coefficients are `7/18`, `7/54`, and `7/18` for X, Y, and Z. The complete two-location Pauli census contains 16,497 events, typed by CX-CX, CX-H, H-CX, and H-H location pairs in the frozen certificate.

For an adversarial leakage event at any of the seventeen circuit locations and a leakage flag of efficiency `eta_flag`, the first-order undetected-bad-output bound is

```text
p_bad <= 34(1-eta_flag) ell + O(ell^2).
```

This is not a detector calibration or coherent-leakage threshold.

## Pass 2962 — all spreads carry the same nonabelian gauge curvature

All 36 spreads of the current `W(3,3)` realization were enumerated. Every spread has the same 120 triangle-holonomy census:

```text
60 transpositions + 60 double transpositions.
```

After tree gauge fixing, the 36 residual chords split `18+18` between the same two cycle types and generate an order-eight group with element-order profile `1^1 2^5 4^2`. Therefore the holonomy group is `D4`, not `Q8`.

The sign projection has 60 odd and 60 even triangles and satisfies all 210 tetrahedral Bianchi checks. Its parity projection is an edge coboundary; the surviving obstruction is genuinely nonabelian `D4` curvature.

## Pass 2963 — configurable ten-by-four optical channel model

The simulator combines:

1. coherent nearest-neighbour coupling on a ten-mode OAM ring;
2. a four-slot Fourier multiport with Gaussian phase error;
3. insertion loss and detector efficiency;
4. independent dark counts;
5. an explicit click/erasure policy.

The analytic slot law is

```text
P_slot_correct = 1/4 + (3/4) exp(-sigma_phi^2).
```

The four committed profiles are ideal and three deliberately synthetic engineering stress profiles. They are not predictions for a fabricated Holonet. Published OAM and temporal-mode sorters justify modeling crosstalk, phase error, loss, and mode-dependent fidelity as independent engineering variables; their reported numbers are not merged into a claimed device calibration.

## Pass 2964 — explicit reversible compiler

The generic 8,192-state completion has a transposition floor of 5,072 and an optimized star upper bound of 39,472 multi-controlled swaps. Exploiting the valid-subspace arithmetic

```text
R = 40r + a = (r << 5) + (r << 3) + a
```

produces an explicit 199-gate network:

```text
120 Toffoli + 79 CNOT.
```

The network was exhaustively checked on all `81*40=3240` valid inputs. It retains the inputs, writes the twelve-bit joint rank, and returns all twenty-four scratch bits to zero.

The logical thermodynamic ledger is therefore:

- reversible gates: zero mandatory erasure bits;
- clean scratch after uncomputation: zero mandatory reset bits;
- eventual joint-rank reset: `log2(3240)=11.6617780978` bits;
- one-error record: `h2(p)+p log2(15)` bits.

Finite-time energy remains implementation- and protocol-dependent.

## Pass 2965 — outside-box curvature pilot code

For one arbitrary nonidentity `S4` permutation inserted on one edge of one spread triangle, the exact census contains

```text
120 triangles * 3 edge positions * 23 faults = 8280 cases.
```

Pilot coverage is:

```text
one pilot:   18/23,
two pilots:  22/23,
three pilots: 1.
```

Three distinct pilot slots are necessary and sufficient. Two pilots miss exactly the transposition exchanging the two unobserved slots.

## Pass 2966 — outside-box anti-symplectic phase transducer

Define

```text
K(x0,x1,x2,x3) = (x1,x0,x3,x2).
```

Then `K^2=I` and `K^T J K=-J`. The same finite-field phase

```text
sigma(x,p)=x^T J p
```

simultaneously implements:

- the W33 commutation/adjacency test `sigma=0`;
- the route-dependent qutrit phase `omega^sigma`;
- the affine-support observer triplet;
- phase-chirality reversal under `K`.

Across all `81*40=3240` frame-route pairs, phases 0, 1, and 2 each occur 1,080 times. Every nonzero frame has exactly thirteen zero-phase routes. On the family-zero M36 labels, `K` swaps ray 5 label `(mu,nu)=(1,2)` to ray 7 label `(2,1)`. This is exact label covariance, not a substitute for the physical distillation circuit.

## Reproduction

```bash
python analysis/bt2960_2966_physical_compiler.py
pytest -q tests/test_bt2960_bt2966_physical_compiler.py
python tools/w33_pass2963_oam_channel_simulator.py
```

The compressed analysis entrypoint supports

```bash
python analysis/bt2960_2966_physical_compiler.py --materialize-source /tmp/bt2960_2966_readable.py
```

The dedicated evidence workflow is responsible for RTL simulation, synthesis/place-and-route, canonical integration, and PDF compilation. No observed hardware or build claim is inferred before that workflow completes.
