# PART CCCLIII — Eigenspace Projectors and Gram Matrices in W(3,3)

## Overview

W(3,3) is an SRG(40, 12, 2, 4) with adjacency spectrum $\{12^1, 2^{24}, (-4)^{15}\}$. Its adjacency algebra (Bose-Mesner algebra) is spanned by three idempotent projectors $E_0, E_r, E_s$:

$$I = E_0 + E_r + E_s, \qquad A = k E_0 + r E_r + s E_s$$

These are the **eigenspace projectors** onto the three eigenspaces of $A$. All entries are exact rationals computable from the SRG parameters alone.

## Projector Entries

Using the Bose-Mesner linear system, every entry of each projector is determined by:
- **Diagonal** $(i=j)$: $\quad (E_l)_{ii} = m_l / V$
- **Adjacent** $(A_{ij}=1)$: solve $r \cdot x + s \cdot y = 1 - k/V$ and $x+y = -1/V$
- **Non-adjacent** $(A_{ij}=0, i \neq j)$: solve $r \cdot x + s \cdot y = -k/V$ and $x+y=-1/V$

| Entry type | $E_0$ | $E_r$ | $E_s$ |
|---|---|---|---|
| Diagonal $(i=j)$ | $\frac{1}{40}$ | $\frac{3}{5}$ | $\frac{3}{8}$ |
| Adjacent $(i \sim j)$ | $\frac{1}{40}$ | $\frac{1}{10}$ | $-\frac{1}{8}$ |
| Non-adjacent $(i \not\sim j)$ | $\frac{1}{40}$ | $-\frac{1}{15}$ | $\frac{1}{24}$ |

### Verification

**Partition of identity** (each column of each row type sums correctly):

$$\frac{1}{40} + \frac{3}{5} + \frac{3}{8} = \frac{1}{40} + \frac{24}{40} + \frac{15}{40} = 1 \checkmark$$

$$\frac{1}{40} + \frac{1}{10} + \left(-\frac{1}{8}\right) = \frac{1}{40} + \frac{4}{40} - \frac{5}{40} = 0 \checkmark$$

$$\frac{1}{40} + \left(-\frac{1}{15}\right) + \frac{1}{24} = \frac{3}{120} - \frac{8}{120} + \frac{5}{120} = 0 \checkmark$$

**Bose-Mesner reconstruction of $A$** (adjacent case):

$$k \cdot \frac{1}{40} + r \cdot \frac{1}{10} + s \cdot \left(-\frac{1}{8}\right) = \frac{12}{40} + \frac{2}{10} - \frac{-4}{8} = \frac{3}{10} + \frac{1}{5} + \frac{1}{2} = 1 \checkmark$$

## Angle Sets

The distinct entry values of $E_r$ form the **angle set** of the eigenspace:

$$\mathcal{A}(E_r) = \left\{\frac{3}{5},\ \frac{1}{10},\ -\frac{1}{15}\right\}$$

These are related to the **spherical code** interpretation: embedding $V=40$ unit vectors in $\mathbb{R}^{24}$ (the $r$-eigenspace) gives a code with inner products from $\mathcal{A}(E_r)$.

## Physics Bridge

| Mathematical fact | Physics interpretation |
|---|---|
| $\mathrm{rank}(E_r) = 24 = \mathrm{MULT\_R}$ | $=$ dimension of SU(5) adjoint |
| $\mathrm{rank}(E_s) = 15 = \mathrm{MULT\_S}$ | $=$ dimension of SU(5) matter rep $\bar{5} \oplus 10$ |
| $(E_r)_{\text{adj}} \times V = 4 = \mathrm{MU} = \mathrm{ABS\_S}$ | Eigenspace-adjacency scaling |
| Denominator of $(E_r)_{\text{non-adj}} = 15 = \mathrm{MULT\_S}$ | Cross-spectrum denominator identity |

## Verification

27 checks, all pass (PASS 27/27).

Groups:
1. Diagonal entries (5 checks)
2. Adjacent off-diagonal entries (5 checks)
3. Non-adjacent off-diagonal entries (5 checks)
4. Partition of identity (5 checks)
5. Row sums (2 checks)
6. Physics connections (5 checks)

## File Index

| File | Description |
|---|---|
| `exploration/PART_CCCLIII_EIGENSPACE_PROJECTORS_BRIDGE.py` | Bridge: eigenspace projectors, 27/27 checks |
| `tests/test_eigenspace_projectors_cccliii.py` | Tests: 64 tests, all pass |
| `PART_CCCLIII_eigenspace_projectors_results.json` | Results JSON |
| `PART_CCCLIII_EIGENSPACE_PROJECTORS_BRIDGE.md` | This file |
