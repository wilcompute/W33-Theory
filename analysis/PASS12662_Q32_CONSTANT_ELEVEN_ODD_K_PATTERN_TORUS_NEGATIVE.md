# Pass 12662: at q = 32 the best value found is the stabiliser value 11; five annealing seeds support (q+1)/3; the torus-orbit explanation fails

Claude track. Follows Pass 12661. **Not a theory of everything.**

## 1. Stabiliser minimum, more seeds (`w33_regulus_odd_k_structure.py`)

Annealing over Lagrangians, 240 s per seed:

| q | seeds | steps per seed | best |M ∩ C| | (q+1)/3 |
|---|---|---|---|---|
| 8 | 2 | 11.3 million | 3, 3 | 3 |
| 32 | 3 | about 6 million | 11, 11, 11 | 11 |

- q = 8 is exact (Pass 12661, exhaustive). q = 32 is annealing evidence only.
- A random walk over Lagrangians shows |M ∩ C| is **always odd** (q = 2 … 32, tens of thousands of samples each), with lowest values 1, 1, 3, 1, 11.
- In the best Lagrangians each covered point lies on a different regulus line: 3 lines of 9 at q = 8, and 11 lines of 33 at q = 32.

## 2. c₃₂ from the stabiliser state (`w33_regulus_c32_from_stabiliser.py`)

The stabiliser state of the weight-11 Lagrangian was built in the CZ model (d·F = 11.000000, matching the count), then perturbed and re-optimised.

| q | start | perturbation sizes | outcomes |
|---|---|---|---|
| 8 (control) | weight-3 stabiliser state | 0.02 to 0.4, 30 runs | 20 reach **2.498509**; the rest stop at 2.685, 2.703, 2.757, 2.849 or stay at 3 |
| 32 | weight-11 stabiliser state | 0.02 to 0.4, 10 runs | **all return to 11.000000** |

- At q = 8 the stabiliser state is unstable and the known non-stabiliser minimum is recovered, so the method can see a better state when one is nearby.
- At q = 32 the stabiliser state is a robust local minimum. Random starts (Pass 12659) only reached 15.16.
- **Best value found: c₃₂ = 11**, i.e. min F ≈ 11/1024 for the 33 regulus bases in dimension 1024. This is an upper bound with local-stability evidence, not a proof of global minimality.

**Constants as they now stand:**

| q | c_q = d·min F | best stabiliser value | status |
|---|---|---|---|
| 2 | 1 | 1 | proved |
| 4 | 1 | 1 | numerical; validated lower bound 0.704 |
| 8 | 2.498509 | 3 (exact) | numerical, non-stabiliser |
| 16 | 1 | 1 | numerical |
| 32 | ≤ 11 | ≤ 11 | best found |

So q = 8 is the only case seen where a non-stabiliser state wins.

## 3. Character-sum data and a failed explanation

For a Lagrangian M, the polar form of Tr(s·Q) on M is ω(s·u, v), so its radical is M ∩ s⁻¹M. With S(s) = Σ_{v∈M} χ(s·Q(v)), |M ∩ C| = (1/q)·Σ_s S(s) − 1 and |S(s)| ∈ {0, q·2^{ρ_s/2}}, ρ_s = dim(M ∩ sM).

| q | radical dimensions ρ_s (s ∉ F₂) | values of S(s) |
|---|---|---|
| 8 | 2 for all six s | −16 (×2), 0 (×5), 64 (s = 0) |
| 32 | 0 (×12), 2 (×18) | −64 (×8), −32 (×10), 0 (×9), 32 (×2), 64 (×2), 1024 (s = 0) |

- Arithmetic alone does not forbid a one-point Lagrangian for odd k (all ρ_s = 0 with negative sign would give it), so the obstruction is structural.
- **Tested and rejected:** "the hit lines are an orbit of a cyclic group of order (q+1)/3 in PGL(2,q)". At q = 32 none of the 32,736 elements of PGL(2,32) has the eleven hit lines as an orbit. (At q = 8 the test is vacuous, since PGL(2,8) is 3-transitive.)
- The conjecture m*(q) = (q+1)/3 for odd k stands on q = 2, 8 (exact) and q = 32 (annealing), without an explanation.

## Not attempted this pass

- Exhaustive search at q = 32 (the level enumeration would handle subspaces of a 2²⁰-point space).
- Closed form of 2.498509 through the 16-dimensional code space.
- Exact rational certificate for the type B bound.

## Open

- Prove |M ∩ C| is odd and m*(q) = (q+1)/3 for odd k.
- Is 11 the global minimum at q = 32?
