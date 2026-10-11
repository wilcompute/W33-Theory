# Pass 11912: the W(3,3) entangling modulus is the family Wilson line

Producer: `analysis/w33_pass11912_entangling_modulus_is_the_wilson_line.py`
Certificate: `data/w33_pass11912_entangling_modulus_is_the_wilson_line.json`
Regression: `tests/test_w33_pass11912.py`
Track: Claude.

## The identity

**Setting.** The two-qutrit magnetized home: flux 3 on each torus of T⁴ with Siegel modulus Ω, in toy units Ω = 6 ×
physical (Pass 11906). Families are the eigenspace of a Wilson-line Pauli on torus 2 (Pass 11900), so a family has a
fixed class a and a family label c. With a localised Higgs the couplings are genus-2 thetas, and

  Θ[(α₁, α₂)](0, Ω) = Σ_n e^{iπ(n+α₂)²Ω₂₂} θ[α₁]((n+α₂)Ω₁₂, Ω₁₁).

This holds **exactly** (≤ 3.5·10⁻¹⁶ over 12 random cases).

**Gaussian regime.** For large Im Ω₂₂, the term with n + α₂ closest to 0 dominates. The family texture is then the
one-qutrit texture of Passes 11904–11907 with Wilson-line argument

  **z_eff = (ã/3)·Ω₁₂**, where ã ∈ {0, ±1} represents the class a.

**Consequences.**
* **a = 0** (left and right families in the same Pauli class): z_eff = 0, so the light pair is locked. This is the
  magnetized analogue of the heterotic local-10 lock (11900, 11903).
* **a = 1 or 2**: the off-diagonal (entangling, W(3,3)) complex-structure modulus **acts as a continuous Wilson line**.
  a = 2 gives −Ω₁₂/3, the mirror of a = 1, with identical masses.

## The up hierarchy without a Wilson line

The hierarchy point of Passes 11904/11906 is Ω₁₁ = 25.25i with Im z = 1.523. It is reached at **Im Ω₁₂ = 4.57 (a = 1)**,
with no Wilson line:

| Im Ω₂₂ | agreement with the one-qutrit texture | m_c/m_t | m_u/m_c |
|---|---|---|---|
| 8 | poor (3.3) | | |
| 16 | 7.6·10⁻⁴ | | |
| 30 | 3·10⁻¹⁰ | 3.61·10⁻³ | 1.69·10⁻³ |

Positivity of Im Ω requires only Im Ω₂₂ > Im Ω₁₂²/Im Ω₁₁ ≈ 0.83, so the Gaussian regime is consistent.

## Why it matters

**From Wilson line to complex structure.** The Wilson-line dynamics of Passes 11907 and 11909 becomes complex-structure
dynamics.

**Flux stabilisation.** In type IIB, complex-structure moduli are stabilised at tree level by three-form fluxes
(Giddings–Kachru–Polchinski).

**What this allows.** The hierarchy point can therefore be fixed by flux quanta. It need not come from the radiative
balance that Pass 11909 showed requires a top-sector cancellation.

**Status.** This is a route, not a constructed flux vacuum.

**The W(3,3) reading.** The same modulus that carries the W(3,3) entangling structure (the off-diagonal Kähler/Siegel
modulus of Passes 11897–11900) generates the family hierarchy offset. It does so only for families whose left and right
fields sit in different Pauli eigenclasses.

## Side result (recorded, no claim)

A small second-class Higgs admixture in the down sector gives Cabibbo-sized mixing, but no structural
Gatto–Sartori–Tonin relation and no V_cb:
* the correlation between log V_us and log √(m_d/m_s) is 0.11 over 400 random admixtures;
* the ratio V_us/√(m_d/m_s) has median 0.78 and spread 0.36;
* V_cb = 0.

## Not established

* **No flux vacuum.** No flux vacuum with (Ω₁₁, Ω₁₂) ≈ (25.25i, 4.57i) in toy units, i.e. (4.21i, 0.76i) physical, is
  exhibited.
* **Up/down areas.** The up-versus-down area mismatch of Pass 11910 is not resolved by this mechanism alone.

## Prior art

* Siegel theta decomposition (classical; Mumford, *Tata Lectures*).
* Giddings–Kachru–Polchinski (2002).
* Cremades–Ibáñez–Marchesano.
* Corpus: 11869, 11897–11900, 11904–11910.
