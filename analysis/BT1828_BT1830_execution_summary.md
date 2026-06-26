# BT1828-BT1830 execution summary

Executed the three next moves after BT1827.

## BT1828 — P,G,E Hamiltonian Realization Theorem

BT1827 solved the cyclic-residue term

```text
C = winding / phase-slip syndrome.
```

BT1828 realizes the remaining BT1824 terms as explicit commuting local Hamiltonian/syndrome projector sums over the finite fibre

```text
Z3 x (Z2)^2
```

encoded as 12 symbols.

For a table `T_i,j,s` and ordered local triple `(x0,x1,x2)`, with

```text
x_r = 4*strand_r + quartet_r,
```

the realized terms are:

```text
H_P = sum_r 1[strand_r != target_r(T_i,j,s)]
H_G = popcount(q0 xor q1 xor q2 xor chi(i,j,s))
H_E = sum_r 1[quartet_r != quartet_{r+1}] on the K4 quartet
H_C = winding(x0,x1,x2)=C_BT1824/12
```

All four are diagonal computational-basis projector sums, hence commute exactly.

Verified spectra over all 27 table labels:

```text
P : 0^64, 1^384, 2^768, 3^512
G : 0^432, 1^864, 2^432
E : 0^108, 2^972, 3^648
C : 0^12, 1^1056, 2^660
```

Boundary: this proves the finite syndrome Hamiltonian; it is not yet a chip-level loss model.

## BT1829 — Phase-Slip Simulator

Built a deterministic finite-state simulator for the BT1827/BT1828 winding term.

Noise rule:

```text
move one coordinate by ±1 on C12, rejecting collisions.
```

Two seeded 4096-step walks were run:

```text
w=2 start (0,1,2): 4096/4096 steps stayed in w=2
w=1 start (0,11,1): 4096/4096 steps stayed in w=1
```

The exhaustive graph check proves every collision-free edge preserves winding.

The shortest controlled phase-slip path changing winding is:

```text
(0,1,2) -> (0,1,1) -> (0,2,1)
```

with profile:

```text
distinct, w=2
double collision, w=1
distinct, w=1
```

So a winding change requires the collision / phase-slip boundary.

## BT1830 — Photonic Syndrome Compiler

Lowered the finite Hamiltonian into a photonic syndrome compiler IR.

Registers:

```text
S0,S1,S2 : qutrit strand path registers
Q0,Q1,Q2 : D4 glue quartet registers
R : C12 ring / winding register
```

Terms:

```text
P0,P1,P2       : qutrit mismatch projectors
G0,G1          : D4 parity-bit ancillas
E01,E12,E20    : K4 equality-vs-edge interferometers
Cwind          : C12 winding readout
Cslip01,12,20  : collision / phase-slip guards
```

Resource counts:

```text
3 qutrit sorters
3 D4 quartet registers
2 D4 parity ancillas
3 K4 equality interferometers
1 C12 ring winding readout
3 phase-slip collision guards
```

The compiler factor graph is bipartite, covers every term, and has:

```text
19 nodes
19 edges
```

Boundary: this is a finite IR/compiler spec, not yet a fabricated hardware layout with loss and detector budgets.

## Files

```text
analysis/bt1828_pge_hamiltonian_realization.py
data/bt1828_pge_hamiltonian_realization.json

analysis/bt1829_phase_slip_simulator.py
data/bt1829_phase_slip_simulator.json

analysis/bt1830_photonic_syndrome_compiler.py
data/bt1830_photonic_syndrome_compiler.json

analysis/BT1828_BT1830_execution_summary.md
```
