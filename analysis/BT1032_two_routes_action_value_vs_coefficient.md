# BT1032 — Two routes to R3's gravity term, and an honest refinement of BT1031

**Status: honest refinement + synthesis. Sharpens what each R3 route closes.**
Script `analysis/bt1032_two_routes_action_value_vs_coefficient.py`, data
`data/bt1032_two_routes_action_value_vs_coefficient.json`.

## The distinction BT1031 glossed

BT1031 reduced R3's spectral-action convergence to propinquity convergence of
the edgewise tower, via Latrémolière's continuity of action functionals. Probing
the inductive-sequence framework (arXiv:2301.00274) surfaced a distinction that
matters physically:

| object | what it is | which route closes it |
| --- | --- | --- |
| spectral-action **value** `S(Λ)=Tr f(D²/Λ²)` | a number at *fixed* cutoff Λ | spectral / **propinquity** (BT1031) |
| Einstein–Hilbert **coefficient** `a₂ ~ (1/6)∫R` | an *asymptotic* (Λ→∞) expansion coefficient of `S(Λ)` | geometric / **Regge–CMS** (BT986) |

Latrémolière's theorem gives `D_n → D` (propinquity) ⟹ `S_n(Λ) → S(Λ)` at
**fixed Λ**. The EH coefficient lives in the **Λ→∞** limit, so extracting it
needs the refinement limit (`n→∞`) and the cutoff limit (`Λ→∞`) to **commute** —
which fixed-Λ continuity does not assert.

## Why the limits don't commute (decisive toy)

Circle Laplacian, eigenvalues `{k²}`, truncated at `|k|≤n`:

- **(a) fixed n, t→0:** the heat trace *saturates* at `2n+1` — a truncated
  spectrum has **no** continuum short-time singularity (no Weyl `√(π/t)`).
- **(b) fixed t, n→∞:** the action *value* converges to the continuum
  (e.g. `t=0.1 → 5.605 = √(π/0.1)`; `t=0.01 → 17.725`). ← the propinquity
  statement.
- **(c)** the asymptotic *coefficient* `a₀ = √(π/t)` appears only in the order
  `n→∞` **then** `t→0`. At fixed `n` it is absent (a). So **(b) ≠ (c)**:
  fixed-cutoff convergence is not asymptotic-coefficient convergence.

This is the same `n ↔ Λ` (UV) interchange flagged in BT983/BT990 — now pinned
to the precise object it obstructs (the asymptotic coefficient, not the value).

## The geometric route bypasses it

The Regge deficit-angle curvature is a **per-level local** quantity; Cheeger–
Müller–Schrader gives `[Regge curvature]_n → ∫R` directly as `n→∞`, with **no
cutoff limit at all**. So the EH **coefficient** `a₂ = (1/6)∫R` is obtained as a
clean single limit — and BT986 already verified `[Regge]_n → ∫R` on the sphere
(exact by discrete Gauss–Bonnet, deficits → 0). Newton's constant — the
physically decisive coefficient — therefore converges by the geometric route.

## Synthesis: R3's gravity term, supported from both sides

- **EH coefficient** `(1/6)∫R`: closed by **Regge/CMS** on the shape-regular
  edgewise tower (per-level, no interchange; BT986 verified).
- **Full spectral-action value** at each cutoff: closed by the **propinquity**
  (BT1031; action-functional continuity is a theorem).
- The only *purely-spectral* residual is the asymptotic-coefficient
  **uniformity** (the `n ↔ Λ` interchange) — and it is *bypassed* by the
  geometric route, so it does not block the physical EH coefficient.

## Net status of R3 (honest)

R3's gravitational term is now robustly supported: the EH **coefficient**
converges geometrically (CMS/Regge, BT986), and the full spectral-action
**value** converges spectrally (propinquity, BT1031), each on the shape-regular
edgewise tower. The remaining genuinely-open piece is the *uniform* (asymptotic)
spectral statement — needed only if one insists on deriving the coefficient from
the spectral action rather than the (equivalent, rigorous) Regge curvature.
This corrects BT1031's slight overstatement: the propinquity closes the action
*value*, not by itself the EH *coefficient*.

## Sources

- Latrémolière, *Continuity of the Spectrum… for the Spectral Propinquity*,
  Math. Ann. (2023), [arXiv:2112.11000](https://arxiv.org/abs/2112.11000).
- Latrémolière, *Convergence of inductive sequences of spectral triples…*,
  Adv. Math. 437 (2024), [arXiv:2301.00274](https://arxiv.org/abs/2301.00274).
- Cheeger–Müller–Schrader, *On the curvature of piecewise flat spaces*,
  Commun. Math. Phys. 92 (1984) 405.
