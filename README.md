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
* **Run the public prediction surface:** `python exploration/w33_predictions.py`
* **Run the closure companion:** `python exploration/w33_predictions_v45_closure.py`
* **Run the test suite:** `python -m pytest tests/` (1000+ tests)
* **View the paper:** `main.tex` contains the complete mathematical paper
* **Browse the website:** [wilcompute.github.io/W33-Theory](https://wilcompute.github.io/W33-Theory/)

## Falsifiable Predictions

1. **Sum(m_nu) = 59 meV** (testable by DESI DR2, Euclid, CMB-S4)
2. **n_s = 29/30 = 0.96667** (testable by CMB-S4, LiteBIRD)
3. **r = 1/300 = 0.00333** (testable by LiteBIRD)
4. **H_0 = 70 km/s/Mpc** (consistent with SH0ES/Planck average)
5. **Axion mass ~ 6 microeV** (testable by ADMX, HAYSTAC)
6. **Proton lifetime > 10^44 yr** (consistent with Super-K bound)

## Exact closure packets

A major recent shift is that the repo now contains **closure packets**, not just isolated successful formulas.

### Inflation closure

The repaired inflation sector is one exact packet with one graph-fixed e-fold count:

- `N = E/mu = 240/4 = 60`
- `N = 2(v - Phi_4) = 2(40 - 10) = 60`

So the two derivations are the same statement:

- `E = 2 mu (v - Phi_4)`

and the observables close exactly:

- `n_s = 29/30`
- `r = 1/300`
- `dn_s/dlnk = -1/1800`
- `n_T = -1/2400`
- `f_NL = -1/72`

with exact relations

- `r = 3(1 - n_s)^2`
- `dn_s/dlnk = -r/6`
- `n_T = -r/8`
- `f_NL = -5(1 - n_s)/12`

### Mass-sector closure

After the light-quark repair, the fermion packet also closes algebraically:

- `(m_s/m_b)/(m_c/m_t) = q`
- `(m_u/m_c)/(m_d/m_s) = 1/(v - Phi_4) = 1/30`
- `m_s/m_c = 1/(2 Phi_6) = 1/14`
- `m_u/m_d = Phi_6/g = 7/15`

So the same `30` that appears in the inflation bridge reappears inside the repaired light-quark packet.

### Lepton-sector closure

The charged-lepton packet also collapses to exact denominators:

- `m_mu/m_tau = 1/(k+q+lam) = 1/17`
- `m_e/m_mu = 1/(alpha^-1 + v + nn + lam) = 1/206`
- `m_e/m_tau = 1/3502`

with

- `206 = 137 + 40 + 27 + 2 = alpha^-1 + v + nn + lam`

So the electron denominator is a direct **fine-structure + geometry** combination.

## What is proven vs. conjectured

**Proven mathematical facts:**
- W(3,3) uniqueness via C1-C7 (symbolic proofs)
- PSp(4,3) = W(E6) (standard group isomorphism)
- Payne derivation -> SRG(27,10,1,5) (computational proof at 4 base points)
- 27 = 16 + 10 + 1 under SO(10) (branching rule)
- Z3 Yukawa selection rule: 0/162 violations (exact)
- 40 = 1 + 15 + 24 multiplicity-free, V_15 = adjoint (ATLAS)
- Inflation closure bridge `N = E/mu = 2(v-Phi_4) = 60` (exact)
- Mass and lepton closure identities in `tests/test_mass_sector_closure_v46.py` and `tests/test_lepton_sector_closure_v48.py`

**Open questions:**
- Why alpha^(-1) = Gaussian norm of Ihara-gauge vector (spectral action proof needed)
- Why sin^2(theta_W) = q/Phi_3 gives the low-energy value directly
- Higgs VEV direction (optimized, not uniquely determined)
- 3 generations from Z3 grading (algebraically true, needs physical axiom)
- Physical interpretation of why the same `v - Phi_4 = 30` bridge appears in both inflation and light-quark closure

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
