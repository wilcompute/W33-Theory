# Pass 10950 — the clock Albert algebra: Lorentz so(1,9), a Weyl spinor, and matter parity as a 2π rotation

Producer: `analysis/w33_pass10950_clock_albert_lorentz_spinor.py`
Certificate: `data/w33_pass10950_clock_albert_lorentz_spinor.json`
Regression: `tests/test_w33_pass10950_clock_albert_lorentz_spinor.py`

Pass 10949 built, from the committed executable E8 bracket, the 27-dimensional
Euclidean Jordan algebra `A` of the clock real form (the Hermitian Jordan triple of
E7(-25) on `p+ = {a8 = 0, a7 = +1}`, with the tripotent of a canonical triad frame).
This pass computes its symmetry algebras exactly, and finds that the repository's
matter parity has a clean meaning inside it.

## 1. Automorphisms and structure group

- `Der(A) = span [L_x, L_y]` has dimension **52**; every basis element is a
  derivation; its trace form is **negative definite (0,52)** — compact F4.
- `str0(A) = Der(A) + L(traceless)` has dimension **78**; the generating identity
  `[D, L_x] = L_{Dx}` holds for all 52 × 27 pairs; its trace form has inertia
  **(26, 52)**, signature −26 — **E6(−26)**, the reduced structure group of the
  Euclidean Albert algebra.

So the clock real form carries the octonionic (division-algebra) Albert structure:
`Aut = F4(−52)`, `Str0 = E6(−26)`, exactly as in Baez's real magic square.

## 2. The Lorentz algebra of a primitive idempotent

For the frame idempotent `c` the Peirce spaces are `A1 = Rc`, `A_{1/2}` (16), `A0`
(10), with time `u = e − c`.

- `Der_c(A) = {D : Dc = 0}` is **36**-dimensional and compact: `spin(9)`.
- Adding the nine boosts `L_y` (y in `A0`, trace-orthogonal to `u`; each kills `c`)
  gives a **45**-dimensional algebra. It preserves `A0`, preserves the Peirce-0
  determinant (inertia **(1, 9)**) infinitesimally, and its image in `gl(A0)` is
  45-dimensional: it is the full Lie algebra of the Lorentzian form, **so(1,9)**.
- On the Peirce 16 its commutant is one-dimensional: an absolutely irreducible real
  16, the **Majorana–Weyl spinor** of `so(1,9)`.

## 3. A 3+1 split

Take time `u`, the frame direction `s0 = e_{g2} − e_{g3}`, and one Hermitian complex
line `{e_a + s e_b, i(e_a − s e_b)}` of `J23` (i27 labels 18, 25) — a complex
subalgebra `C ⊂ O` supplied by the complex structure of `p+` itself. The
subalgebra of `so(1,9)` preserving this 4-space and its 6-dimensional complement
is **21**-dimensional (`so(1,3) + so(6)`), and its commutant on the 16 is
two-dimensional and contains a complex structure. Hence
`16 = (2,4) + conjugate` under `sl(2,C) + su(4)`: one Pati–Salam spinor multiplet,
by the standard branching now certified on the executable basis.

## 4. Matter parity is the Peirce symmetry — the 2π rotation of Spin(9)

The repository's `Q_psi` certificate (`w33_qpsi_matter_parity_e8_d8_bridge.json`)
records `27 = 16_1 + 10_{−2} + 1_4` and the triad pattern
`40 × (−2,1,1) + 5 × (−2,−2,4)`. For **every one of the 27 coordinate idempotents**,
the Peirce charge

```text
Q = 6 L_c − 2   (Peirce 1 → 4, Peirce 1/2 → 1, Peirce 0 → −2)
```

reproduces that spectrum, conserves charge on all 45 triads, and gives exactly that
triad pattern. Matter parity `(−1)^Q` is then the Peirce symmetry
`U_{2c−e} = 2L_s² − L_{s∘s}`: it is an automorphism of `A`, `+1` on `A1` and `A0`,
`−1` on the Peirce 16. Numerically, `exp(2π D)` for the single-plane rotation
`D = [L_{s0}, L_z]` in `spin(9)` equals `U_{2c−e}` to `2.7 × 10^{−15}`.

**Reading.** The same `27 = 1 + 10 + 16` that the GUT reading calls
`SO(10)` singlet/Higgs/matter is, in the clock real form, scalar/Lorentz-vector/
Weyl-spinor of `Spin(1,9)`, and matter parity is the spinor sign — the 2π
rotation. In the compact E6 of the |3| Levi (Pass 10949) the same idempotent
stabiliser is the compact `Spin(10)`: the two readings are two real forms of one
complex branching.

## Scope

The identification of the repository's `Q_psi` with `6L_c − 2` holds up to the
`W(E6)`-transitive choice of coordinate idempotent (the `Q_psi` certificate itself
lives in a different root gauge). `so(1,9)` here is the stabiliser of an idempotent
inside `E6(−26)`; it is not derived to be the Lorentz group of physical spacetime,
and the Pati–Salam statement is a branching fact, not gauge dynamics, chirality
selection, or masses.

Prior art: `w33_qpsi_matter_parity_e8_d8_bridge.json` (the `Q_psi` data);
commit `5419c27` (`27 = 1+10+16`, `W(D5)` stabiliser); count-level `SU(4)`
readings in `BREAKTHROUGH_DCCLXXXVII.md` and `scripts/w33_exact_sector_physics.py`.
External: Faraut–Korányi; Baez, *The Octonions* (2002); Manogue–Dray–Wilson,
JMP 63 (2022); Baez–Huerta (2010).

Rediscovery guard: the only flagged compound, `e7+levi`, points to the same files
read and cited in `analysis/PASS10949_FREUDENTHAL_QUASICONFORMAL_CLOCK_CONE.md`
(`analysis/BT1720_BT1723_repo_mining_execution.md`,
`analysis/PASS7376_7384_deep_followup.md`, and the parent
`analysis/w33_20260925_hesse_clock_e8_gradings.py`); none builds F4, E6(−26),
so(1,9) or the Peirce symmetry.
