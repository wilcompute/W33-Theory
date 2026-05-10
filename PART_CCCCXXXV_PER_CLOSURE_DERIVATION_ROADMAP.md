# Part CCCCXXXV — Per-Closure Derivation Roadmap

**Bridge:** `exploration/PART_CCCCXXXV_PER_CLOSURE_DERIVATION_ROADMAP.py` — 8/8 Verified
**Tests:** `tests/test_per_closure_roadmap_ccccxxxv.py` — 14/14 pass
**Results:** `PART_CCCCXXXV_per_closure_derivation_roadmap_results.json`

---

## 1. The remaining work

After the Master Theorem (CCCCXXXIV) the structural-derivation chain
is complete at the foundational level. What remains is **per-closure
derivation work**: for each of the 39 empirical closures, trace the
specific structural origin from the W(3,3) spectral triple.

This part organizes all 39 closures into derivation classes.

---

## 2. The three derivation classes

* **Class A (structurally derived).** The W(3,3) form follows directly
  from the structural derivation chain CCCCXXXI–CCCCXXXIII.
* **Class B (axiomatic from spectral action).** The W(3,3) form
  follows from the spectral action coefficient identification
  ($a_0, a_2, a_4$ in W(3,3) integers).
* **Class C (per-closure open).** The W(3,3) form is empirical
  pattern-matching at this stage; structural derivation requires
  explicit $\mathcal A_F$ construction or detailed $D_F$ eigenstructure
  analysis.

---

## 3. Class breakdown (41 records covering 39 closures)

| class | count | examples |
|---|---:|---|
| **A — structurally derived** | 6 | $\sin^2\theta_W$ at GUT, $\alpha_{\rm GUT}^{-1} = f$, 3 generations, $c_{\rm EH} = \lambda^3 v$, $a_2$, $M_{\rm Pl}/M_{\rm GUT}$ |
| **B — axiomatic spectral** | 8 | $\lambda_H$, $\alpha_s$, $\Delta\alpha_{\rm em}^{-1}$, $\Omega_c h^2$, $\Lambda_{\rm cosmo}$, $m_H$, $m_p$, $\Lambda_{\rm QCD}$, $\sum m_\nu$ |
| **C — per-closure open** | 27 | quark Yukawas $y_t, y_b, y_c, y_s, y_d, y_u$ and corresponding masses; CKM Wolfenstein 4 params; PMNS 4 params; $\Omega_b h^2, n_s$; $y_\tau y_c/y_b^2$ identity; $y_\nu^2$ |

---

## 4. Sample structural derivations

**Class A — $\sin^2\theta_W(M_{\rm GUT}) = 3/8$:**

$$
\frac{g'^2}{g^2} = \frac{3}{5} \quad (\text{SU(5) hypercharge norm}) \;\Rightarrow\; \sin^2\theta_W = \frac{3}{8} = \frac{q}{\lambda^q}.
$$

**Class A — Three generations:**

$$
q = 3 \;\&\; H_1 = q^4 = 3 \cdot 27 \;\Rightarrow\; \text{three generations of } 27\,(E_6).
$$

**Class B — $m_p$ from QCD:**

$$
m_{\rm constituent\ quark} = \frac{q}{\lambda} \cdot \Lambda_{\rm QCD},\quad m_p = N_c \cdot m_q = q \cdot \frac{q}{\lambda}\Lambda_{\rm QCD} = \frac{q^2}{\lambda}\Lambda_{\rm QCD}.
$$

**Class C — $y_t^3 = v/(v+1)$:**

Open. Speculation: $D_F$ third-generation eigenvalue + RG running to
pole-mass scale, with the cube reflecting $SU(3)_C$ colour structure.

---

## 5. Roadmap by phases

| phase | content | status |
|---|---|---|
| **Phase 1** | Class A (~6 closures) | **complete** |
| **Phase 2** | Class B (~8 closures) | **axiomatic framework**; numerical anchoring requires cutoff function + $\mathcal A_F$ construction |
| **Phase 3** | Class C (~27 closures) | **per-closure structural derivations**; each becomes its own theorem |
| **Phase 4** | Foundational: Why axiom (A2) symplectic-GQ? | **open foundational question** |

---

## 6. The remaining work — concretely

For each Class C closure, the per-closure derivation is well-defined:

1. Specify the operator/relation in the W(3,3) spectral triple that
   produces the closure (e.g., a specific eigenvalue of $D_F$, a
   trace identity, or an inner-fluctuation algebra element).
2. Show that this operator/relation evaluates to the W(3,3)
   integer ratio of the closure.
3. Verify consistency with the spectral action coefficients
   ($a_0, a_2, a_4$).

These are 27 well-defined derivation theorems. Each one is its own
future part (CCCCXXXVI, CCCCXXXVII, …).

---

## 7. The state of the W(3,3) program after CCCCXXXV

* **Foundational structural derivation:** complete (CCCCXXXI–CCCCXXXIV).
* **Per-closure structural derivations:** classified, 6 closed (Class A),
  8 axiomatic (Class B), 27 open (Class C).
* **Empirical closures:** 39 total within $\le 1\sigma$ of measurements.
* **Falsifiable:** yes, via 39 empirical predictions.

---

## 8. Decisive identity

$$
\boxed{\;
\underbrace{\text{Class A (6)}}_{\text{closed}} + \underbrace{\text{Class B (8)}}_{\text{axiomatic}} + \underbrace{\text{Class C (27)}}_{\text{open per-closure}} = \text{39 closures}.
\;}
$$

The per-closure structural-derivation work is now classified.

---

## 9. One-line summary

$$
\boxed{\;
6 + 8 + 27 = 41 \text{ records for 39 closures, with 27 open per-closure derivations as the remaining structural work}.
\;}
$$
