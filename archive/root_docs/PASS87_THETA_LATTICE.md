# Pass 87 — Construction A lattice of C₂(W): theta series as a weight-20 modular form

**Status: PASS** — witness `w33_pass87_theta_lattice.py` (5/5 checks), test
`tests/test_pass87_theta_lattice.py` (4/4). Self-contained (sympy).

The capstone of the code arc (Pass 85/86): the code → lattice → modular form bridge (Gleason;
Broué–Enguehard). The Construction A lattice Λ_C = { x ∈ ℤ⁴⁰ : x mod 2 ∈ C₂(W) } has theta series

`Θ_{Λ_C}(q) = Σ_{x∈Λ_C} q^{|x|²} = W_C(f₀, f₁)`, f₀ = Σ_{k even} q^{k²}, f₁ = Σ_{k odd} q^{k²},

the code's weight enumerator evaluated at the two coordinate theta constants. Since C₂(W) = [40,16,8]
is **doubly-even self-orthogonal**, Λ_C is an **even lattice of rank 40** and Θ is a **modular form
of weight 20** (level 4). Computed exactly from the Pass 85 enumerator:

`Θ(q) = 1 + 80q⁴ + 14640q⁸ + 5403840q¹² + 1301706800q¹⁶ + 90075980640q²⁰ + …`

## Key facts
- **Minimal vectors: 80 of norm 4** (the ±2eᵢ, = 2n), no vectors of norm 1,2,3.
- **The q⁸ coefficient encodes the E₆ geometry:** 14640 = 3120 (two ±2 coords) + **11520 = 45 × 2⁸**,
  i.e. the 45 tritangent planes reappear as the norm-8 minimal codeword vectors of the lattice.
- Weight 20 = 40/2 — a genuine modular form; the theta constants f₀,f₁ (≈ θ₃,θ₂) are the E₈/E₄
  building blocks.

## The completed arithmetic tower of W(3,3)
```
graph W(3,3)
  -> Ihara zeta / RH (Ramanujan) / functional equation / class number formula   (Pass 73-74, 83)
  -> critical group = class group; Sunada-Gassmann pair                          (Pass 82, 84)
  -> binary code C_2(W) = [40,16,8], dual [40,24]  (E6: 45; E8: 240)             (Pass 85-86)
  -> even lattice rank 40 + weight-20 modular form                                (this pass)
```
Grounded in the literature: Crnković–Maksimović (self-orthogonal codes from SRG(40,12,2,4));
Gleason / Broué–Enguehard (modular forms from codes).

## Files
- `w33_pass87_theta_lattice.py`, `.json` — witness + certificate (5 checks).
- `tests/test_pass87_theta_lattice.py` — 4 assertions.
