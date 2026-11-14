# Pass 12661: the best stabiliser value for the F₈ regulus is exactly 3 (exhaustive); q = 32 gives 11; the pattern (q+1)/3 for odd k

Claude track. Follows Pass 12660. **Not a theory of everything.**

## 1. Exhaustive: no Lagrangian meets the F₈ quadric in one or two points (`w33_regulus_stabiliser_exhaustive2.py`)

On a stabiliser state of a Lagrangian M, d·F = |M ∩ {Q = 0}| (non-zero points). Write the vectors as 2×2 matrices m = [[x₁, x₂], [z₂, z₁]] over F_q, so Q = det m. The group SL(2,q) × SL(2,q), acting by m ↦ g·m·hᵀ, preserves Q and ω and is transitive on the covered points (checked: one orbit of 567 at q = 8).

**Method.** Fix the covered point c = E₁₁. Enumerate, level by level, the isotropic subspaces containing c whose only covered point is c:
- level 2 is reduced modulo the stabiliser of c (169 Schreier generators);
- each higher level adds one admissible vector and is de-duplicated by its sorted span.

| run | level-2 classes | dim 3 | dim 4 | dim 5 | dim 6 (Lagrangians) | time |
|---|---|---|---|---|---|---|
| q = 8, exactly one covered point | 16 | 2,301 | 15,944 | 3,672 | **0** | 23 s |
| q = 8, exactly two covered points | 3 | 465 | 3,087 | 882 | **0** | 5 s |
| q = 4, exactly one (control) | 4 | 15 | 3 (dim 4 = Lagrangian) | | **3 found** | 0 s |
| q = 4, exactly two | 1 | 6 | 0 | | 0 | 0 s |

- **No stabiliser state of the F₈ regulus has d·F < 3.** Annealing (Pass 12660) finds 3, so the stabiliser minimum is **exactly 3**.
- The numerical minimum over all states is 2.498509 < 3 (Pass 12658). So **non-stabiliser states are strictly better at q = 8**; this is now an exhaustive statement on the stabiliser side and a numerical one on the other.
- The earlier backtracking attempt (`w33_regulus_stabiliser_exhaustive.py`) timed out undecided after 4.58 million nodes; it revisited subspaces. It is kept as the record.
- The "exactly two" mode has no positive control (none exists at q = 4 either).

## 2. q = 32 (`w33_regulus_stabiliser_minimum.py 400 5`, `w33_regulus_constants_q16_q32.py`)

- Annealing over Lagrangians at q = 32 (ten qubits, 1.83 million steps): best stabiliser value **11**.
- The random-start optimiser of Pass 12659 returned 15.164 with 16 starts, all different (15.16 to 15.18). That is above the stabiliser value, so it did **not** find the minimum. It is withdrawn as an estimate; what stands is **c₃₂ ≤ 11**.

## 3. The pattern

| q | k | best stabiliser value m* | status |
|---|---|---|---|
| 2 | 1 | 1 | exact |
| 4 | 2 | 1 | exact (a one-point Lagrangian exists) |
| 8 | 3 | 3 | exact (exhaustive lower bound, annealed witness) |
| 16 | 4 | 1 | exact (found) |
| 32 | 5 | ≤ 11 | annealing |

**Conjecture.** m*(q) = 1 for k even and **(q + 1)/3 for k odd** (1, 3, 11 for q = 2, 8, 32). This rests on three data points, the last an upper bound. For odd k, 3 divides q + 1, so the q + 1 regulus lines split evenly into thirds; no explanation is offered here.

The true constants satisfy c_q ≤ m*(q), with equality numerically for q = 2, 4, 16 and strict inequality at q = 8.

## Open

- Prove m*(q) for odd k; find c₃₂ with a better optimiser (start from the weight-11 stabiliser states).
- The closed form of c₈ = 2.498508646688.
