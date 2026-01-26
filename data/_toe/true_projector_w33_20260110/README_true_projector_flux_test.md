# True Hermitian W33 projector test (rank-1) — flux toggle

## Projector model
For each W33 line L with clock-state mask M_L (size 8 for rainbow, 2 for monochrome, 24 for hub line),
define a normalized complex vector φ_L ∈ C^24:
- component on clock state k: φ_L[k] = ω^(pos_in_Z6(k) mod 3) * sgn(k), if k ∈ M_L else 0
- ω = exp(2π i / 3)
- sgn(k)=+1 for pos_in_Z6<3 and -1 for pos_in_Z6≥3 (breaks central e* swap symmetry)
- normalize φ_L

Measurement for node×clock state ψ(t) ∈ C^(59×24):
p_L(t) = Σ_node |⟨φ_L, ψ_node(t)⟩|^2  (i.e., I_node ⊗ |φ_L⟩⟨φ_L|)

Stability metric: S_L = mean_t p_L(t) / std_t p_L(t) with ddof=1 over 9 times t=0..2 step 0.25.

## Flux toggle
Flux case uses H_transport with defect edges labeled e*.
No-flux case toggles the 4 delta4 edges to identity (e* → e), leaving all other edge labels unchanged.

## Scan parameters
λ ∈ [0.4..0.56] step 0.01 (17 values)
μ ∈ [0.75, 1.25, 1.75]
Seed: ψ(0) = |node0⟩ ⊗ |clock_state0⟩
Compare only lines L ∈ [22, 8, 17] (your boundary trio).

## Outcomes (winner changes)
Number of (λ,μ) grid points where winner differs under flux toggle: 7 / 51

Switchpoints:
- Flux: [{'mu': 1.75, 'lambda_switch': 0.46, 'from': 22, 'to': 17}]
- No-flux: [{'mu': 0.75, 'lambda_switch': 0.41, 'from': 22, 'to': 17}]

See CSVs for full tables and per-point winner differences.
