# PG(3,2) / W(3,2) continuation: symplectic transport + lift diagnostics

## Symplectic form and isotropic lines

- Using J = [[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]] on F2^4.

- Enumerated 15 isotropic (totally isotropic 2D subspace) lines.

## Point sets (supports)

- tomotope supports: |S|=10 (10 distinct).

- missing-cap supports: ['0001', '0011', '0100', '0110', '1000'].

- apex-cap supports (sec0_m2 completion family): ['1001', '1011', '1100', '1110', '1111'].

## Symplectic map M

- Found M in Sp(4,2) mapping missing-cap -> apex-cap:

```
1 1 0 1
1 0 1 1
1 0 1 0
1 1 1 0
```

## Effect of M on the tomotope 10-set

- Intersection profile with isotropic lines stays the same: {0: 0, 1: 4, 2: 7, 3: 4}.

- But the specific full isotropic lines change. See `tomotope10_full_lines.csv` vs `tomotope10_mapped_by_M_full_lines.csv`.

## Z3-hyperplane fiber structure vs symplectic transport

- Hyperplane solutions (27) fiber over support patterns with sizes: 10×1, 4×3, 1×5.

- The symplectic action on supports does **not** preserve fiber sizes in general; under this M, 1111 (fiber 5) maps to 1101 (fiber 3).

## Exceptional triangle (4,-4)

- Unmatched triple is exactly the sector-0 phase-axis {sec0_m0,sec0_m1,sec0_m2} supported on tomotope points {14-,24-,34-}.
