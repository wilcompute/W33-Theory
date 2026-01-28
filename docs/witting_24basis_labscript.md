# 24‑Basis KS Lab Script

## Required inputs
- MZI schedule: docs/witting_24basis_mzi_schedule.md
- Waveplate schedule (deg): docs/witting_24basis_waveplates_deg.md

## Target inequality
Noncontextual bound: **23 / 24**
Quantum prediction: **24 / 24**

## Measurement steps

### Basis B00
Rays: [0, 8, 16, 36]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r0: e0
- r8: (0,1,-w^0,w^1)/sqrt3
- r16: (0,1,-w^1,w^0)/sqrt3
- r36: (0,1,-w^2,w^2)/sqrt3

### Basis B01
Rays: [0, 12, 20, 28]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r0: e0
- r12: (0,1,-w^0,w^2)/sqrt3
- r20: (0,1,-w^1,w^1)/sqrt3
- r28: (0,1,-w^2,w^0)/sqrt3

### Basis B02
Rays: [1, 5, 25, 33]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r1: e1
- r5: (1,0,-w^0,-w^0)/sqrt3
- r25: (1,0,-w^1,-w^2)/sqrt3
- r33: (1,0,-w^2,-w^1)/sqrt3

### Basis B03
Rays: [1, 13, 21, 29]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r1: e1
- r13: (1,0,-w^0,-w^2)/sqrt3
- r21: (1,0,-w^1,-w^1)/sqrt3
- r29: (1,0,-w^2,-w^0)/sqrt3

### Basis B04
Rays: [2, 10, 18, 38]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r2: e2
- r10: (1,-w^0,0,w^1)/sqrt3
- r18: (1,-w^1,0,w^0)/sqrt3
- r38: (1,-w^2,0,w^2)/sqrt3

### Basis B05
Rays: [2, 14, 22, 30]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r2: e2
- r14: (1,-w^0,0,w^2)/sqrt3
- r22: (1,-w^1,0,w^1)/sqrt3
- r30: (1,-w^2,0,w^0)/sqrt3

### Basis B06
Rays: [3, 11, 19, 39]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r3: e3
- r11: (1,w^0,w^1,0)/sqrt3
- r19: (1,w^1,w^0,0)/sqrt3
- r39: (1,w^2,w^2,0)/sqrt3

### Basis B07
Rays: [4, 5, 6, 7]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r4: (0,1,-w^0,w^0)/sqrt3
- r5: (1,0,-w^0,-w^0)/sqrt3
- r6: (1,-w^0,0,w^0)/sqrt3
- r7: (1,w^0,w^0,0)/sqrt3

### Basis B08
Rays: [4, 21, 22, 23]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r4: (0,1,-w^0,w^0)/sqrt3
- r21: (1,0,-w^1,-w^1)/sqrt3
- r22: (1,-w^1,0,w^1)/sqrt3
- r23: (1,w^1,w^1,0)/sqrt3

### Basis B09
Rays: [5, 18, 19, 36]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r5: (1,0,-w^0,-w^0)/sqrt3
- r18: (1,-w^1,0,w^0)/sqrt3
- r19: (1,w^1,w^0,0)/sqrt3
- r36: (0,1,-w^2,w^2)/sqrt3

### Basis B10
Rays: [6, 11, 16, 17]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r6: (1,-w^0,0,w^0)/sqrt3
- r11: (1,w^0,w^1,0)/sqrt3
- r16: (0,1,-w^1,w^0)/sqrt3
- r17: (1,0,-w^1,-w^0)/sqrt3

### Basis B11
Rays: [6, 15, 28, 29]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r6: (1,-w^0,0,w^0)/sqrt3
- r15: (1,w^0,w^2,0)/sqrt3
- r28: (0,1,-w^2,w^0)/sqrt3
- r29: (1,0,-w^2,-w^0)/sqrt3

### Basis B12
Rays: [8, 23, 25, 26]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r8: (0,1,-w^0,w^1)/sqrt3
- r23: (1,w^1,w^1,0)/sqrt3
- r25: (1,0,-w^1,-w^2)/sqrt3
- r26: (1,-w^1,0,w^2)/sqrt3

### Basis B13
Rays: [9, 19, 22, 28]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r9: (1,0,-w^0,-w^1)/sqrt3
- r19: (1,w^1,w^0,0)/sqrt3
- r22: (1,-w^1,0,w^1)/sqrt3
- r28: (0,1,-w^2,w^0)/sqrt3

### Basis B14
Rays: [9, 24, 31, 34]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r9: (1,0,-w^0,-w^1)/sqrt3
- r24: (0,1,-w^1,w^2)/sqrt3
- r31: (1,w^2,w^0,0)/sqrt3
- r34: (1,-w^2,0,w^1)/sqrt3

### Basis B15
Rays: [10, 11, 20, 21]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r10: (1,-w^0,0,w^1)/sqrt3
- r11: (1,w^0,w^1,0)/sqrt3
- r20: (0,1,-w^1,w^1)/sqrt3
- r21: (1,0,-w^1,-w^1)/sqrt3

### Basis B16
Rays: [11, 14, 24, 25]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r11: (1,w^0,w^1,0)/sqrt3
- r14: (1,-w^0,0,w^2)/sqrt3
- r24: (0,1,-w^1,w^2)/sqrt3
- r25: (1,0,-w^1,-w^2)/sqrt3

### Basis B17
Rays: [12, 33, 34, 39]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r12: (0,1,-w^0,w^2)/sqrt3
- r33: (1,0,-w^2,-w^1)/sqrt3
- r34: (1,-w^2,0,w^1)/sqrt3
- r39: (1,w^2,w^2,0)/sqrt3

### Basis B18
Rays: [13, 16, 31, 38]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r13: (1,0,-w^0,-w^2)/sqrt3
- r16: (0,1,-w^1,w^0)/sqrt3
- r31: (1,w^2,w^0,0)/sqrt3
- r38: (1,-w^2,0,w^2)/sqrt3

### Basis B19
Rays: [13, 19, 26, 32]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r13: (1,0,-w^0,-w^2)/sqrt3
- r19: (1,w^1,w^0,0)/sqrt3
- r26: (1,-w^1,0,w^2)/sqrt3
- r32: (0,1,-w^2,w^1)/sqrt3

### Basis B20
Rays: [14, 15, 36, 37]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r14: (1,-w^0,0,w^2)/sqrt3
- r15: (1,w^0,w^2,0)/sqrt3
- r36: (0,1,-w^2,w^2)/sqrt3
- r37: (1,0,-w^2,-w^2)/sqrt3

### Basis B21
Rays: [17, 30, 32, 35]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r17: (1,0,-w^1,-w^0)/sqrt3
- r30: (1,-w^2,0,w^0)/sqrt3
- r32: (0,1,-w^2,w^1)/sqrt3
- r35: (1,w^2,w^1,0)/sqrt3

### Basis B22
Rays: [18, 24, 27, 29]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r18: (1,-w^1,0,w^0)/sqrt3
- r24: (0,1,-w^1,w^2)/sqrt3
- r27: (1,w^1,w^2,0)/sqrt3
- r29: (1,0,-w^2,-w^0)/sqrt3

### Basis B23
Rays: [25, 28, 35, 38]

Prepare basis via MZI or waveplates, then measure counts
for the four designated outcomes.

- r25: (1,0,-w^1,-w^2)/sqrt3
- r28: (0,1,-w^2,w^0)/sqrt3
- r35: (1,w^2,w^1,0)/sqrt3
- r38: (1,-w^2,0,w^2)/sqrt3

## Scoring
For each basis, mark satisfied if exactly one designated outcome occurs.
Sum S across 24 bases and compare to bound.
