# Pass 12074: the (T, g) phase diagram of the tick condensate

Claude track. Continues 12068.

## Exact ingredients

- The 120 tick projectors sum to 40 I. So the spread state, and the three ticks of any one point, have H = (2/3) I and
  **F_u = 2/3 − T log 9**.
- Single tick: Z₁ = 3 + 6e^(−1/T). Context: Z₄ = 1 + 8e^(−3/(4T)).
- The 13-tick star (the four contexts through one tick) has spectrum {(15 − 3√5)/26, (9/13)⁷, (15 + 3√5)/26}.
- Every phase has mean energy 2/3. So at high T the gaps are set by variances: Var₁ = 2/9, Var₄ = 1/18, Var_u = 0.

## Phase boundaries

| Boundary | Formula | T → 0 | High T |
|---|---|---|---|
| single \| context | g₄ = (4/3)(F₄ − F₁) | → 0 | ~ 1/(9T) |
| context \| spread | g_u = (120/29)(F_u − F₄) | → 80/29 | ~ 10/(87T) |

## Results

- **The context window never closes.** g_u > g₄ on T ∈ [0.01, 5], and g_u/g₄ → 30/29 at high T.
- **Below T\* = 1.39,** the context beats every structured candidate in its window.
- **Above T\*,** the 13-tick star enters between the context and spread phases.

## Reading

At low T a capacity cost produces a sharp sequence: one event → one measurement context → spread. The context phase is
wide, up to g = 80/29.

## Scope

This model and the candidates listed. The region above the star phase is not mapped.

Producer: `analysis/w33_pass12074_phase_diagram_of_the_tick_condensate.py`.
