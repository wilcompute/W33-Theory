# Passes 12126–12130: charge quantisation versus k_Y, Yukawa sizes, exotic masses, A8 mixing, full one-loop vacuum

Claude track. Producer: `analysis/w33_pass12126_to_12130_charges_masses_vacuum.py`. Drivers and frozen outputs:
`analysis/search_drivers_12126/`. This continues 12121–12125 and cites 11095–11106 throughout.

## 12126: the canonical hypercharge is absent, and fraction-free hypercharges cost k_Y ≥ 17/3

**Relaxed search.** Y is restricted to the Cartan of the parent so(10), orthogonal to SU(3)_c and SU(2)_L. This 2-plane
contains the k_Y = 5/3 direction. Exotics may carry any charge, as long as they are vector-like.

- No member of the plane gives the SM spectrum in any of the five models (27–74 candidates each).
- Control: the same evaluator accepts every strict solution of 12121.
- So the 12121 statement "k_Y never 5/3" is not an artefact of its strict search.
- Reason: the generation's u^c and d^c have no component in the so(10) plane. They are not SO(10)-16 components.

**Charge quantisation.**

- Fraction-free three-generation hypercharges exist in 4 of the 5 models (11, 22, 4 and 14 of them; none in S002).
  Fraction-free means no fractionally charged state anywhere in the massless spectrum.
- **All of them have k_Y ∈ {17/3, 29/3, 41/3, …} = 5/3 + 4n, with n ≥ 1.**
- Every difference of two fraction-free hypercharges is integral on every state and has even norm (383/383 pairs). So
  they form a coset, and k_Y ≡ 5/3 (mod 4).
- The smaller values (11/3, 13/3, 14/3) always come with fractional charges.

**The trade-off.** The A8 models of 11095 have k_Y = 5/3 but 144 fractional colourless states. Here, a fraction-free
spectrum costs k_Y ≥ 17/3. This refines the generic statement already cited in 11024 (Schellekens 1990: fractional
charges are the price of a hypercharge not GUT-embedded at level one). The mod-4 coset law is observed in these models;
it is not proved in general.

## 12127: the size of S002's rank-one Yukawas

- Every up-type and down-type coupling has the form U×T2×T1, with the u^c or d^c and the Higgs at **the same fixed
  point**. The couplings are therefore unsuppressed, of gauge strength.
- The up-type Higgs fields sit at the 3 fixed points with first-torus label 0.
- The down-type Higgs fields sit at the other 6 (label 1 or 2).
- Up and down Higgs fields are distinct scalars; no pair is conjugate.

So y_t ~ y_b ~ g, and **m_t/m_b = v_u/v_d** is a ratio of vevs on geometrically separated fixed points. The
chiral-to-vector-like mixing factor cancels in the ratio. The hierarchy is not predicted; it is moved into the vacuum.

## 12128: exotic masses at trilinear order

**Method.** Mass terms ψψ⟨s⟩ from SM-singlet scalars, subject to all selection rules. The rank is the numerical rank at
random couplings, which is an **upper bound** on the true rank, so the light counts below are lower bounds.

**T115**, under its minimal-k_Y hypercharge, has no fractional charge at all.

| class | lifted at trilinear order | still massless |
|---|---|---|
| vector-like d^c pair | yes | — |
| lepton-doublet pairs | 4 of 6 | 2 |
| charged-singlet pairs | 28 of 33 | 5 |

**S002** leaves 41 pairs light, including fractional charges −5/3, 1/3 and 2/3. Higher-order couplings are not examined.

## 12129: the 104 A8 models of 11095 have no mixing channel for the up sector

Measured on their own hypercharge (nsosm; the Y column is located by the fields labelled q):

| quantity | result |
|---|---|
| net quark doublets | 3, in 104/104 |
| vector-like Y = 1/6 doublets | none, in all 104 |
| vector-like u^c | none, in all 104 |
| vector-like d^c pairs | 95/104 |
| vector-like (3,2)_{∓5/6} pairs (X/Y-boson quantum numbers) | 41/104 |

This confirms the 11098 statement. The top–charm degeneracy of those models cannot be lifted by renormalisable mixing;
only the down sector has a mixing channel.

A first pass that read Y from a fixed U(1) slot found an apparent "3 vector-like ū" in one model. That model's Y sits
in a different slot. Corrected.

## 12130: the vacuum energy

**Correction.** The field dumps omit the U(1) gauge bosons, as 11106 found for 11099. So N_B − N_F gains 2N_U1.

| set | corrected N_B − N_F |
|---|---|
| range over the 75 models | [−432, −160] |
| the four left-right models | −372, −336, −300, −264 |
| T115 | −260 |
| SO(10) parents of 12117 | −672 … −480 |

The values of 12117 and 12123 are superseded by these. The sign is unchanged.

**Full one-loop integral.** This uses the 11106 engine: all 36 sectors, Narain lattice with Wilson lines, 27 fixed points
× 24 coset images. It is evaluated at T_WL = 2i, T* = ρ, with Λ₄ = −½M⁴I.

| model | I_β | I_twisted | Λ₄/M⁴ |
|---|---|---|---|
| control: 11106 model 2 | -1241.0 | -74.3 | **657.6** (11106: 657.6) |
| S002 | -1274.5 | -80.7 | **677.6** |

**Result.** The left-right three-generation model S002 has a **positive** one-loop vacuum energy at this point, beyond
the massless term, like the A8 models. Scope: a single moduli point, with the dilaton tadpole remaining. The moduli
potential and the tachyon onset of 11106/11107 are not scanned for S002.
