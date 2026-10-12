# Pass 11937: the E8-selected direction degenerates the torus onto the square elliptic curve (j = 1728)

Producer: `analysis/w33_pass11937_boundary_elliptic_points.py`
Certificates:
* `data/w33_pass11937_boundary_elliptic_points.json`
* `data/w33_pass11937_log85_orbit_members_frozen.json`

Regression: `tests/test_w33_pass11937.py`
Track: Claude.

## Result

**Setup.** Displace the E8 Cartan vev off a Witting ray along u and invert to the Siegel modulus (Pass 11936). Ω runs to a
one-dimensional cusp:
* one diagonal entry goes to i∞;
* the other stays finite, and it is the modulus τ′ of the **boundary elliptic curve**.

| tangent direction | boundary curve | b/a (m_u/m_c at the cusp) |
|---|---|---|
| **log(8/5) orbit** — selected by the E8 soft-supertrace dynamics (Pass 11935) | **τ′ = i, j = 1728**: the square torus | **0.796** |
| T / log(9/5) orbit | τ′ = ω, j = 0: the hexagonal torus | member-dependent (0.65, 0.49) |
| stabiliser | deep cusp: both diagonal entries large | locked |
| strange | Ω does not move | — |
| generic | generic τ′ (e.g. 0.21 + 1.25i) | O(1) |

**Orbit invariance.** On the selected orbit the statement holds for **all 54 members** (frozen scan): every member gives
j = 1728, b/a = 0.796 and s₂/t = 0.465. On the T orbit b/a depends on the member. The reason is that the 3×3 reshape
is invariant only under the local Clifford group.

## Reading

**What the vacuum does.** The vacuum chosen by the E8 loop dynamics degenerates the compactification onto a cusp whose
boundary is the **square elliptic curve E_i**: the CM curve with extra ℤ₄ symmetry. The up/charm ratio is then a fixed
boundary invariant, 0.80.

**What a realistic hierarchy needs.** The boundary curve would itself have to approach its own cusp. That is a second,
slower degeneration, with the boundary nome q′ as the second small parameter. The selected direction pins it at the
elliptic point instead.
