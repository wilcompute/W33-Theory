# Pass 12055: deriving the condensate -- the tick model chooses one event at every temperature

* **Producer:** `analysis/w33_pass12055_microscopic_tick_model.py` (5/5 checks)
* **Certificate:** `data/w33_pass12055_microscopic_tick_model.json`
* **Regression:** `tests/test_w33_pass12055.py`
* **Track:** Claude. Reservation `17e7065ba`.
* **Continues:** 12052-12054.

## Model (no couplings put in by hand)

**The ticks.** A tick is the Clifford transvection U = sum_k w^(k^2) Pi_k(p) on two qutrits. Pauli conjugation shifts k,
so there are 3 ticks per point and **120 in all**, the same count as the clock involutions of Theorem 7.3.
* **Generator:** U = exp(2 pi i h/3), with the **positive** generator h = I - Pi_k(p).
* **Condensate:** with rates phi >= 0, H(phi) = sum phi_a h_a.
* **Free energy:** F_T(phi) = -T log Tr exp(-H/T).

## Results

1. **The ticks are what they should be.** The 120 ticks are Clifford, have order 3 and satisfy
   U = I + (w - 1)(I - Pi_k(p)).
2. **Zero temperature.** A single tick has a 3-dimensional zero-energy space. Two ticks have at most 1: none at the same
   point or at non-collinear points, and 1 at collinear points.
3. **Theorem (concavity).** F_T is concave in the rates. So at fixed total rate (the simplex) its minimum is a **single
   tick at every temperature**. Checked by 90 midpoint tests and by random interior points.
4. **The L2 sphere.** Here too the global minimum is a single tick at all T tried (0.02-2). At low T, F -> -T log 3.
5. **Contrast: signed Pauli fields.** They reach the bound E = -4 on an **isotropic line**, the stabiliser state of a
   commuting context, while a single point gives only -1. The minimiser set is degenerate.

## Reading

**Where the derived couplings land.** The Landau couplings of 12054 are now derived for this model, and they put it in
the one-event phase. Concretely:
* the condensate is one tick;
* by 12052-12053, one tick fixes the clock real form E8(-24) and is central in its symmetry group.

**The reason.** Tick generators are positive, so the free energy is concave in their rates.

**Events versus contexts.** Observables (signed Pauli fields) choose measurement contexts instead. Events are what the
dynamics chooses.

## Scope and prior art

* **Scope:** this two-qutrit model. The fixed-rate statement is a theorem; the L2 statement is numerical.
* **Not new:** convexity of log-partition functions.

## What remains

An action for the tick rates themselves.
