# Pass 12050: where can the small entangler ε = Ω₁₂ come from?

* **Producer:** `analysis/w33_pass12050_entangler_origin.py` (3/3 checks)
* **Certificate:** `data/w33_pass12050_entangler_origin.json`
* **Regression:** `tests/test_w33_pass12050.py`
* **Track:** Claude. Reservation `53ebd807e`.

## Why

**The open question.** The up hierarchy needs ε ≈ 0.0055, close to the product locus.
* **12048:** canonical potentials repel that locus.
* **12049:** it would be explained if Ω₁₂ were an SU(5)-restoring Wilson line.

This pass checks the two standard string mechanisms against that.

## (i) Heterotic continuous Wilson lines: they rescale planes, they do not entangle them

Kobayashi–Lebedev (hep-th/0303009, eqs. 33–36; read for this pass) compute twisted Yukawas in abelian ℤ_N orbifolds
with T² ⊕ T² ⊕ T² and continuous Wilson lines.

**Result.** A Wilson line a_i in plane i enters only through T_i + κ(T_i + T̄_i) a_i ā_i. That is a per-plane rescaling,
i.e. a **diagonal** period-matrix entry. This holds for the standard embedding and for their block non-standard
embeddings.

**Consequences.**
* An off-diagonal Ω₁₂ would need a gauge block shared between planes, which is outside their class. Even then it would
  be ∝ a₁ā₂, whose zero set is not the restoration locus.
* So **12049's identification has no home in the computed heterotic class.**
* K-L also find that heterotic Wilson lines give **no CP phases** in Yukawas, unlike open strings. The 12045
  CP-in-a-Wilson-line row therefore belongs to the open-string (magnetized) reading of 11942, consistent with it.

## (ii) Magnetized fluxes: Humbert surfaces, but with large integers

**The mechanism.** In the magnetized reading Ω₁₂ is complex structure. Fluxes stabilise complex structure through the
(1,1) condition: each extra (1,1) class confines Ω to a Humbert surface

  aτ₁ + bε + cτ₂ + d(ε² − τ₁τ₂) + e = 0,  Δ = b² − 4ac − 4de.

**The product locus.** It is Δ = 1.

**The search.**
* **Space:** all integers with |b| ≤ 4000 and |d| ≤ 60.
* **Tolerance:** y ± 0.007 (from the Weber invariant) and δ ± 3% (from m_c/m_t).
* **Point:** the symmetric CP up home τ = 1 + 0.8745i, ε = 0.00552i.

**Result.** The **minimal discriminant** is 23,716 at 1σ, 22,500 at 2σ and 21,025 at 3σ. It is attained by the linear
relation **ε = (τ − 1)/b with b ≈ 150 ≈ y/δ**. So flux stabilisation can place the up home there, but only with flux
integers of order 150. The product locus is about 33σ away.

## Reading

**What fails.** Neither standard mechanism gives the near-product hierarchy naturally:
* heterotic Wilson lines rescale the planes instead of entangling them;
* fluxes need integers of order 1/ε.

**What remains open.** With 12048, what keeps ε ≈ 1/150 is now the sharpest open question of the flavour chain.
12049's threshold matching remains a conditional coherence with no known string home.

## Scope and prior art

* **Scope:**
  * Kobayashi–Lebedev's class only (abelian orbifolds, factorisable planes);
  * the symmetric CP-locus up home;
  * one extra flux class.
* **Not new:**
  * Kobayashi–Lebedev;
  * flux (1,1) stabilisation of complex structure (Antoniadis–Kumar–Maillard and others);
  * Humbert singular relations.
