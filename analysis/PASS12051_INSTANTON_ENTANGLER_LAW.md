# Pass 12051: an instanton-sized entangler

* **Producer:** `analysis/w33_pass12051_instanton_entangler_law.py` (4/4 checks)
* **Certificate:** `data/w33_pass12051_instanton_entangler_law.json`
* **Regression:** `tests/test_w33_pass12051.py`
* **Driver:** `analysis/search_drivers_12045/instlaw.py`
* **Track:** Claude. Reservation `d2822a5cc`.

## The law

In the mirror (IIA) reading of magnetized branes, the theta moduli are complexified Kahler moduli. An entangler made by
a worldsheet instanton spanning both tori scales as exp(-pi(y1 + y2)). Test the parameter-free form

  eps_sector = C * exp(-pi(Im tau1 + Im tau2)),

with **one universal C**.

* **Up home:** C_u = 1.34 +- 5%. The up hierarchy is |q| up to an O(1) factor, so eps_u ~ 1/180 is not mysterious once
  Im tau ~ 0.87.
* **Down homes in the corpus:** C_d/C_u = 3.6 (12005), 10.4 (12007), **1.12 (branch A)**, and 2.5e4-2.5e5 (branches
  B, C, D, G).

## The overdetermined test

Impose the law on the 12045 geometric-row down system, with C = C_u e^eta and eta a nuisance at 5.3%. That leaves 6
residuals against 5 free parameters plus eta: **one degree of freedom**.

* **Branch A:** chi^2 = 1.33 (comparator errors) and 1.73 (lattice precision). All pulls are below about 1 sigma and
  eta = 0.03. **The law passes.**
* **Multistart:** 90 starts per error set, 60 of them broad. The best solutions are branch A and its symmetry images
  only.
* **Look-elsewhere:** the chance that one of seven branches lands within about 12% of the law is roughly 0.15-0.2.

## The conflict

Branch A is excluded by the charged leptons under the 12007 shared matching. At the constrained solution m_mu/m_tau is
x0.31 and m_e/m_mu is x7.9. Since kappa only rescales m_e, no Clebsch rescues it. The leptons favour branch C, which
violates the law by 2.5e4. **No branch satisfies both.**

## Reading

**What works.** A single worldsheet-instanton law makes the quark sector of the geometric row overdetermined, and it
fits.

**What doesn't.** The branch it selects cannot carry the charged leptons. Either the lepton sector has its own structure
(consistent with 12045-12047), or the law is a coincidence on branch A.

**What remains.** The law itself would need an actual instanton computation in a model.

## What is not new

* Worldsheet-instanton Yukawas: Cremades-Ibanez-Marchesano; Cvetic-Papadimitriou.
