# Pass 11919: the tilt modulus — fluxes are Humbert singular relations, and the forced zero is a non-simple abelian surface

Producer: `analysis/w33_pass11919_tilt_modulus_humbert.py`
Certificate: `data/w33_pass11919_tilt_modulus_humbert.json`
Regression: `tests/test_w33_pass11919.py`
Track: Claude. This pass answers the stabilisation question left open by Pass 11917: what fixes the tilt y in
Ω = x + yN₁?

## 1. A flux is a singular relation

A block flux N, i.e. one in the dx∧dy block, is (1,1) exactly when NΩ = ΩN. Write Ω = [[τ₁, τ₂], [τ₂, τ₃]]. The
condition is then Humbert's singular relation

  **−N₁₂ τ₁ + (N₁₁ − N₂₂) τ₂ + N₁₂ τ₃ = 0**,  with discriminant Δ = (N₁₁ − N₂₂)² + 4N₁₂² = (tr N)² − 4 det N.

* Checked on 200 random integer fluxes. On the slice Ω = x + yN the relation holds to 10⁻¹². A non-scalar
  perturbation off the slice always violates it.
* **For a det-3 dual pair, Δ = m² − 12.**

## 2. The forced zero is non-simplicity

**The index form.** On the dual-pair slice the integral block fluxes are u + vN₁. Their index form is

  **det(u + vN₁) = u² + m·uv + 3v²**  (checked symbolically).

Its discriminant is m² − 12 = Δ.

**The criterion.** The surface contains an elliptic curve exactly when there is a zero-index flux. That holds exactly
when the form is isotropic, i.e. when Δ is a square. Since (m − k)(m + k) = 12 forces **m = 4** (checked for m < 400),
the only cases are the A₂ and x² + 3y² pairs.

**The zero-index fluxes are Pass 11917's mod-3 frame lines:**

| pair | zero-index fluxes | image lines |
|---|---|---|
| A₂ | A₂ − 1, A₂ − 3 | (1, 1) and (1, −1) |
| x² + 3y² | diag(0, 2), diag(−2, 0) | (0, 1) and (1, 0) |

**The theorem.** Combined with Pass 11917, *the first-generation down/electron zero is forced for every modulus if and
only if the flux forces the compactification abelian surface to be non-simple.*

**The other pairs.** For m = 5 and m = 7 (Δ = 13, 37) the slice is a Hilbert modular surface for Q(√13) or Q(√37), and
its generic member is simple. There the zero sits only on the diagonal τ₊ = τ₋, where the surface is E × E.

| pair | Δ | slice |
|---|---|---|
| A₂, x² + 3y² | 4 | a product (non-simple) for every modulus |
| (1, ±1, 4) | 13 | Hilbert modular surface of Q(√13) |
| (3, ±3, 4) | 37 | Hilbert modular surface of Q(√37) |

## 3. The Galois involution swaps the 10 and the 5̄

**On Z[N₁].** The Galois involution of Z[N₁] sends N₁ ↦ m − N₁ = N₂ (Cayley–Hamilton).

**On the lattice.** It is realised by the lattice rotation R, since RᵀNR = adj N. R maps (N₁₀, N₅, x + yN₁) to
(N₅, N₁₀, x + yN₂). Checked on the full Yukawa spectra to 3·10⁻⁹.

**What it means for the tilt.**
* At y = 0, R is an automorphism of the torus that exchanges the two SU(5) flux sectors.
* Because 10 ≠ 5̄, it is not a symmetry of the model.
* So no symmetry protects y = 0, and none forbids it.

## 4. Fluxes do not make the tilt small

**Block fluxes kill it.** Any further block flux outside Q[N₁] leaves only the scalars as common commutant: dimension
1, checked for four slices × three extra fluxes. Such a flux forces y = 0 and so **restores m_d = 0**.

**Oblique fluxes fix it, but at O(1).** A nonzero tilt needs oblique fluxes: Humbert relations with a det Ω term. These
cut the Hilbert surface in modular curves and CM points. Such loci fix y at arithmetic values of order one, not small
ones.

**The conclusion.** The tilt is a genuine modulus. Fluxes cannot make it parametrically small, and no symmetry pins
it. Its value is dynamical; Pass 11918 asks what values the data would need.

## Prior art

These are classical and cited, not claimed:
* Humbert (1899), singular relations and Humbert surfaces.
* Néron–Severi groups of abelian surfaces; non-simple ⟺ isotropic NS class (Birkenhake–Lange, *Complex Abelian
  Varieties*).
* Hilbert modular surfaces and the diagonal (Hirzebruch–Zagier).
* Magnetic fluxes fixing complex structure: Antoniadis–Maillard 2004; Blumenhagen–Lüst–Taylor 2003 (hep-th/0303016);
  Kumar–Mukhopadhyay–Ray (hep-th/0605083).

New here: the link to the Yukawa zero of Passes 11916–11917. The forced zero is equivalent to Δ = m² − 12 being a
square, the zero-index fluxes are the mod-3 frame, and the Galois involution is the 10 ↔ 5̄ exchange.
