# Passes 12466–12473: d = 2q in line variables, minimal even line sets, and where a k_Y ≈ 1.3 string model must come from

Claude track. Producer: `analysis/w33_pass12466_to_12473_dual_lines_even_sets_ky_floor.py`. Drivers: `analysis/search_drivers_12466` and
`12468`.

## 12466: the remaining case of d = 2q, in line variables

**Reduction.** Kernel words are sums N y of an even number of lines. By the k-line lemma (12460), a word of weight below 2q needs at least
q + 2 lines in *every* representation. So it can be searched for with lines as the variables, with the line count bounded below.

**Model.** CP-SAT with native XOR: for each point p, s_p is the XOR of y over the lines through p.

| case | result |
|---|---|
| q = 3, weight 4 | infeasible (control) |
| q = 3, weight 6 | found: 2 lines, a kernel word (control) |
| q = 5, weights 6–8, at least 7 lines | UNKNOWN after 600 s |

The line encoding is no stronger than the point encoding of 12450, so CP-SAT is not the q = 7 lever in either set of variables.

## 12467: minimal even line sets

An *even* line set covers every point an even number of times: it is a word of ker₂ N. In the remaining case of d = 2q, a minimal
representation Y covers every point outside S evenly, with |S| < 2q. So Y is within fewer than 2q odd points of an even line set, and how
small even line sets can be is the structural input.

Exact MILP minima:

| q | minimum even line set | 2(q + 1) | every optimum covers points |
|---|---|---|---|
| 2 | 6 (the grid) | 6 | 0 or 2 times |
| 3 | **10** | 8 | 0 or 2 times |
| 5 | **20** | 12 | 0 or 2 times |
| 7 | ≤ 40 (time limit, upper bound only) | 16 | 0 or 2 times |

- **At q = 2 (control)** the minimum is a grid sub-quadrangle of order (q, 1). The lines of W(2) are regular.
- **For odd q** the minimum exceeds 2(q + 1). That fits the conjecture that W(q), whose lines are not regular for q odd, has no (q, 1)
  grid sub-quadrangle. [C]
- **Pattern** [C]: 10 and 20 equal 5(q − 1) at q = 3, 5. The q = 7 incumbent of 40 neither confirms nor refutes the predicted 30.
- **The proof strategy this suggests** [C]: show that a line set within fewer than 2q odd points of evenness is forced to contain a large
  even set, then use the lower bound on even sets. This is not done here.

## 12468–12470: the k_Y window and where a unifying model must come from

**Two cited facts:**

- **12131:** every *fraction-free* hypercharge has k_Y = 5/3 + 4n. This is Schellekens' self-duality argument.
- **12154:** non-SUSY running from the heterotic scale needs k_Y ≈ 1.29.

**So [proved from the two]:** a viable model of this class needs **1 ≤ k_Y < 5/3**. The lower limit 1 is the conformal-weight bound for
e^c. Below 5/3 the string spectrum *must* contain fractionally charged states, so those states must be massive. That is the SM_2541
mechanism (12451), but it is needed at a smaller k_Y.

**Floors computed from the spectrum alone (SM_2541):**

- **Single-field bound:** Cauchy–Schwarz for one e^c gives k_Y ≥ 2/|P_U|². It is exactly **1** in all 52 models and in the SM_2913
  control, so it carries no information.
- **One-generation floor:** take the least-norm hypercharge over every choice of representatives (Q, u^c, d^c, L, e^c), both signs,
  anomaly-free. This is computed exactly with a closed-form rank-one update over 161,436 consistent choices. The result is **1.187** in all
  52 models.
- **Reading:** the geometry does *not* forbid k_Y ≈ 1.3 for a single generation.

**Three generations, c22:**

- **The 1/6 menu, exhaustive:** there are exactly **6** three-generation hypercharges, with minimum **11/3**.
- **Capped search:** I added a necessary L1 cap, Σ|t_j| ≤ 4√(K/2) for k_Y ≤ K. At K = 5/3 the capped enumeration finds only one solution,
  with k_Y = 17/3, and then becomes infeasible. **Proved:** no three-generation hypercharge of c22 has k_Y ≤ 5/3 in this menu. Control: at
  K = 4 the cap keeps the true solutions.
- **The 1/18 menu (|Y| ≤ 2):** the solver time limit was reached, so this is **open**.

**Where to look next.** The obstruction is not the geometry of one generation, which reaches 1.19. It is the joint three-generation and
vector-like constraints in the 1/6 charge menu. A model with k_Y < 5/3 needs exotic charges outside multiples of 1/6. So the next search
must use the wider menu (1/18 or finer) with the k_Y cap, on parents whose one-generation floor is below 1.3.

## 12473: synthesis

- **d = 2q:** the remaining case is now a statement about line sets close to even sets. For odd q, the smallest even sets are 10 and 20
  lines at q = 3, 5, compared with the 2(q + 1) a grid would give.
- **Strings:** unification forces 1 ≤ k_Y < 5/3, and hence liftable fractional states. SM_2541's single generation would allow
  k_Y = 1.19, but its three generations in the 1/6 menu cannot go below 11/3. The search must move to finer charge menus.
