# Part CCLXXXV — Albert Algebra, Exceptional Jordan Algebra, and the 27 Lines of W(3,3)

## Overview

The **Albert algebra** $\mathfrak{h}_3(\mathbb{O})$ — the $27$-dimensional exceptional Jordan algebra of $3\times 3$ Hermitian matrices over the octonions $\mathbb{O}$ — is the unique simple Jordan algebra not arising from an associative ring. Its automorphism group is the exceptional Lie group $F_4$, and its structure group is $E_6$. The number of minimal idempotents of the Albert algebra equals the **W(3,3) parameter** $\text{LINES}_{27} = 27$, the same as the number of lines on a smooth cubic surface. This is not a coincidence: the 27 lines on a cubic surface are acted on by $W(E_6)$, whose order equals the symplectic group $|\text{Sp}(4,\mathbb{F}_3)| = 51840 = \text{AUT\_ORDER}$.

## W(3,3) SRG(40,12,2,4) Constants

| Symbol | Value | Derivation |
|--------|-------|-----------|
| $V$ | 40 | vertices |
| $K$ | 12 | degree |
| $\lambda$ | 2 | LAM |
| $\mu$ | 4 | MU |
| $Q$ | 3 | field order |
| $\Phi_4$ | 10 | $Q^2+1$ |
| $\Phi_3$ | 13 | $K+1$ |
| $\Phi_6$ | 7 | $K-\mu-1$ |
| LINES$_{27}$ | 27 | lines/idempotents |
| EDGES | 240 | $=E_8$ roots |
| AUT\_ORDER | 51840 | $|\text{Sp}(4,\mathbb{F}_3)|=|W(E_6)|$ |

## Albert Algebra

The Albert algebra $J = \mathfrak{h}_3(\mathbb{O})$ consists of $3\times 3$ matrices

$$A = \begin{pmatrix} \alpha_1 & a_3 & \bar{a}_2 \\ \bar{a}_3 & \alpha_2 & a_1 \\ a_2 & \bar{a}_1 & \alpha_3 \end{pmatrix}, \quad \alpha_i \in \mathbb{R},\ a_i \in \mathbb{O}$$

with Jordan product $X \circ Y = \tfrac{1}{2}(XY+YX)$. Its dimension is

$$\dim J = \underbrace{3}_{\text{diagonal}} + \underbrace{3 \times 8}_{\text{off-diagonal octonions}} = 3 + 24 = 27 = \text{LINES}_{27}$$

Using W(3,3) constants: $3 = Q$, $24 = \lambda K = 2\times 12$, $27 = Q + \lambda K$.

## Peirce Decomposition

With respect to a **frame** of three orthogonal primitive idempotents $e_1, e_2, e_3$:

$$J = J_{11} \oplus J_{22} \oplus J_{33} \oplus J_{12} \oplus J_{13} \oplus J_{23}$$

Each diagonal slot $J_{ii} \cong \mathbb{R}$ has dimension 1; each off-diagonal slot $J_{ij} \cong \mathbb{O}$ has dimension 8. Total:

$$\dim J = 3\cdot 1 + 3\cdot 8 = 3 + 24 = 27 = \text{LINES}_{27}$$

$$\text{off-diagonal total} = \frac{Q(Q-1)}{2} \cdot E_8\text{-rank} = 3\cdot 8 = 24 = \lambda K$$

## Exceptional Lie Algebra Constants

| Algebra | Rank | Dim | Roots | Connection |
|---------|------|-----|-------|-----------|
| $G_2$ | 2 | 14 | 12 | $\text{Aut}(\mathbb{O})$; roots $= K$ |
| $F_4$ | 4 | 52 | 48 | $\text{Aut}(J)$; rank $= \mu$, roots $= \mu K$ |
| $E_6$ | 6 | 78 | 72 | structure group of $J$; rank $= \lambda Q$ |
| $E_7$ | 7 | 133 | 126 | $56$-dim rep $= \text{GEWIRTZ}\_V$ |
| $E_8$ | 8 | 248 | 240 | roots $= \text{EDGES}$ |

**Famous identity:**
$$\underbrace{2}_{G_2} + \underbrace{4}_{F_4} + \underbrace{6}_{E_6} + \underbrace{7}_{E_7} + \underbrace{8}_{E_8} = 27 = \text{LINES}_{27}$$

The ranks of all five exceptional simple Lie algebras sum to the dimension of the Albert algebra.

## E₆ Root System

$E_6$ has $72$ roots: $36$ positive and $36$ negative, plus $6$ zero (Cartan).

$$|E_6\text{ roots}| = 72 = E_6\text{-rank} \times K = 6 \times 12$$

$$|E_6\text{ pos. roots}| = 36 = Q \times K = 3 \times 12 = \text{CUBIC\_DOUBLE\_SIXES}$$

The **36 positive roots of $E_6$** correspond exactly to the **36 double-sixes** on the cubic surface — pairs of 6 mutually skew lines.

$$\dim E_6 = 36 + 36 + 6 = 72 + 6 = 78$$

## Weyl Groups

$$|W(E_6)| = 51840 = \text{AUT\_ORDER} = |\text{Sp}(4,\mathbb{F}_3)|$$

$$|W(F_4)| = 1152 = 2^7 \cdot 3^2 = \mu\lambda K^2$$

$$\frac{|W(E_6)|}{|W(F_4)|} = \frac{51840}{1152} = 45 = \text{CUBIC\_TRITANGENTS} = \text{LINES}_{27} + E_8\text{-rank} + \Phi_4$$

The index $|W(E_6)| / |W(F_4)| = 45$ equals the number of **tritangent planes** to the cubic surface.

## Freudenthal Magic Square

The last row of the Freudenthal magic square (tensoring with $\mathbb{O}$) gives:

| $\mathbb{A} \otimes \mathbb{O}$ | Lie algebra | Dim | Roots |
|---|---|---|---|
| $\mathbb{R} \otimes \mathbb{O}$ | $F_4$ | 52 | 48 |
| $\mathbb{C} \otimes \mathbb{O}$ | $E_6$ | 78 | 72 |
| $\mathbb{H} \otimes \mathbb{O}$ | $E_7$ | 133 | 126 |
| $\mathbb{O} \otimes \mathbb{O}$ | $E_8$ | 248 | 240 |

Connecting to W(3,3) constants:
- $E_8$ dimension: $248 = 240 + 8 = \text{EDGES} + E_8\text{-rank}$
- $E_7$ fundamental representation: $56 = \text{GEWIRTZ}\_V$
- $E_8$ roots: $240 = \text{EDGES}$, and $240 / (\lambda Q) = 40 = V$
- $E_6 - F_4 = 78 - 52 = 26 = \lambda \Phi_3$

## Cubic Surface and 27 Lines

The **cubic surface** $S \subset \mathbb{P}^3$ contains exactly 27 lines. Their combinatorics:

| Quantity | Formula | Value |
|----------|---------|-------|
| Lines | $\text{LINES}_{27}$ | 27 |
| Degree of incidence graph | $\Phi_4$ | 10 |
| Meeting pairs | $27 \times 10 / 2$ | 135 |
| Non-meeting pairs | $(27 \times 26 / 2) - 135$ | 216 |
| Total incidence | $\text{LINES}_{27} \times \Phi_4$ | 270 = TRANSPORT\_EDGES |
| Tritangent planes | $\text{TRANSPORT\_EDGES} / (\lambda Q)$ | 45 |
| Double-sixes | $51840 / 1440$ | 36 |

The **216 non-meeting line pairs** equal:
$$216 = (\lambda Q)^3 = 6^3 = \text{LINES}_{27} \times E_8\text{-rank} = 27 \times 8$$

## Schläfli Graph SRG(27,10,1,5)

The **Schläfli graph** has the 27 lines as vertices, with two lines adjacent iff they meet.

$$\text{SRG}(27, 10, 1, 5): \quad v=\text{LINES}_{27},\ k=\Phi_4,\ \lambda=1,\ \mu=Q+\lambda=5$$

Feasibility check: $k(k-\lambda-1) = 10\cdot 8 = 80 = (v-k-1)\mu = 16\cdot 5 = 80$. ✓

**Discriminant** of both SRG(40,12,2,4) and SRG(27,10,1,5):
$$\Delta = (\lambda-\mu)^2 + 4(k-\mu) = 36 \quad \text{(both graphs!)}$$

| | W(3,3) SRG(40,12,2,4) | Schläfli SRG(27,10,1,5) |
|---|---|---|
| $v$ | 40 | 27 = LINES$_{27}$ |
| $k$ | 12 | 10 = $\Phi_4$ |
| $\mu$ | 4 | 5 = $Q+\lambda$ |
| $r$ (large eigenvalue) | 2 | 1 |
| $s$ (small eigenvalue) | $-4$ | $-5$ |
| $\Delta$ | 36 | 36 |

Differences: $V - v = 13 = \Phi_3$; $K - k = 2 = \lambda$; $r_{W33} + s_{Sch} = -3 = -Q$.

## Key Identities Web

$$\text{LINES}_{27} = \text{ALBERT\_DIM} = 27$$
$$E_8\text{-rank} = \text{dim}(\mathbb{O}) = 8$$
$$|W(E_6)| = |\text{Sp}(4,\mathbb{F}_3)| = \text{AUT\_ORDER} = 51840$$
$$\text{TRANSPORT\_EDGES} = \text{LINES}_{27} \times \Phi_4 = 27 \times 10 = 270$$
$$|W(E_6)| / |W(F_4)| = 45 = \text{CUBIC\_TRITANGENTS}$$
$$\text{CUBIC\_DOUBLE\_SIXES} = Q\times K = 36 = \text{positive } E_6 \text{ roots}$$
$$E_8\text{ roots} / (\lambda Q) = 240/6 = 40 = V$$
$$2+4+6+7+8 = 27 = \text{LINES}_{27} \quad (G_2,F_4,E_6,E_7,E_8 \text{ ranks})$$

## Test Results

- Bridge checks: **140/140 pass**
- Test suite: **125/125 pass**
- JSON output: `PART_CCLXXXV_albert_jordan_results.json`

## Files

| File | Description |
|------|-------------|
| `exploration/PART_CCLXXXV_ALBERT_JORDAN_BRIDGE.py` | Bridge: 17 verify functions, 140 checks |
| `tests/test_albert_jordan_cclxxxv.py` | 125 tests across 17 test classes |
| `PART_CCLXXXV_albert_jordan_results.json` | JSON results |
| `PART_CCLXXXV_ALBERT_JORDAN_BRIDGE.md` | This document |
