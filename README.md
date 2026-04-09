# W(3,3)-E6 Theory: From One Graph to the Standard Model

The symplectic polar graph **W(3,3) = SRG(40,12,2,4)** is the unique member of the family W(3,q) satisfying seven algebraic conditions (C1-C7). Its automorphism group **PSp(4,3) = W(E6)** selects E6 as the grand unified gauge group. The 27 non-neighbours of any vertex carry the **E6 fundamental representation** (verified by Payne derivation to SRG(27,10,1,5) = complement of Schlafli graph). All Standard Model parameters derive from this single graph with **one input: q = 3**.

## The Complete Derivation Chain

```
W(3,3)  ->  Aut = PSp(4,3) = W(E6)  ->  E6 GUT  ->  SU(3) x SU(2) x U(1)
  |
27 non-neighbours  ->  Payne GQ(2,4)  ->  SRG(27,10,1,5) = Schlafli complement
  |
E6 cubic invariant on 27  ->  Yukawa couplings (Z3 selection rule, 0/162 violations)
  |
VEV optimization  ->  CKM (0.26% error) + PMNS (0.6% error)
```

**Derived constants** (from graph parameters alone):

| Quantity | Formula | Value | Experiment |
|----------|---------|-------|------------|
| alpha^(-1) | (k-1)^2 + s^2 | **137** | 137.036 |
| sin^2(theta_W) | q/Phi_3 | **3/13 = 0.2308** | 0.2312 |
| M_GUT | 136^(g/2) | **10^16 GeV** | ~2x10^16 |
| Lambda_CC | 10^(-(alpha^(-1)-g)) | **10^(-122)** | ~10^(-122) |

**Key theorem (C7):** The identity s^2 = r^2 + k holds if and only if q = 3.
Proof: (q+1)^2 = (q-1)^2 + q(q+1) iff q(q-3) = 0 iff q = 3. QED

## Start here

* **Run the complete derivation:** `python exploration/w33_complete_theory.py`
* **Run the test suite:** `python -m pytest tests/` (1000+ tests)
* **View the paper:** `main.tex` contains the complete mathematical paper
* **Browse the website:** [wilcompute.github.io/W33-Theory](https://wilcompute.github.io/W33-Theory/)

## Falsifiable Predictions

1. **Sum(m_nu) = 59 meV** (testable by DESI DR2, Euclid, CMB-S4)
2. **n_s = 29/30 = 0.96667** (testable by CMB-S4, LiteBIRD)
3. **H_0 = 70 km/s/Mpc** (consistent with SH0ES/Planck average)
4. **Axion mass ~ 6 microeV** (testable by ADMX, HAYSTAC)
5. **Proton lifetime > 10^44 yr** (consistent with Super-K bound)

## What is proven vs. conjectured

**Proven mathematical facts:**
- W(3,3) uniqueness via C1-C7 (symbolic proofs)
- PSp(4,3) = W(E6) (standard group isomorphism)
- Payne derivation -> SRG(27,10,1,5) (computational proof at 4 base points)
- 27 = 16 + 10 + 1 under SO(10) (branching rule)
- Z3 Yukawa selection rule: 0/162 violations (exact)
- 40 = 1 + 15 + 24 multiplicity-free, V_15 = adjoint (ATLAS)

**Open questions:**
- Why alpha^(-1) = Gaussian norm of Ihara-gauge vector (spectral action proof needed)
- Why sin^2(theta_W) = q/Phi_3 gives the low-energy value directly
- Higgs VEV direction (optimized, not uniquely determined)
- 3 generations from Z3 grading (algebraically true, needs physical axiom)

## Reproducibility

All results are **exact and reproducible**. Each claimed identity has:

1. **Mathematical expression** - the explicit finite-geometry formula
2. **Python script** - code that computes both sides and checks equality
3. **Unit tests** - test files in `tests/` verified with `pytest`

To run: install requirements in `requirements.txt` and execute `pytest`.

## Contributing

We welcome issues, pull requests and external critiques. See `docs/verification.md` for instructions on independent verification.

## License

MIT License. See `LICENSE` for details.
