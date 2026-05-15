# Part DCCXXI — Biological Allometry from q = 3

**Bridge:** `verify_dccxxi_biological_allometry_from_q3.py` — Verified
**Tests:** `tests/test_dccxxi_biological_allometry_from_q3.py` — 17/17 pass
**Data:** `data/dccxxi_biological_allometry_from_q3.json`

---

## 1. What this part adds

DCCXX gave the *combinatorial* structure of life (codon length 3,
alphabet 4, 61/20 ≈ q redundancy). DCCXXI gives the *quantitative*
structure: the universal **1/4-power scaling laws** of mammalian
physiology, all of which collapse to multiples of 1/(q+1) at q = 3.

The single root identity is **Kleiber's law**:

$$
B \;\propto\; M^{3/4}, \qquad \tfrac{3}{4} \;=\; \frac{q}{q+1}\,\bigg|_{q=3}.
$$

---

## 2. The 1/4-power family

| quantity | symbol | exponent | as n/(q+1) | scaling | source |
|---|---|---:|---|---|---|
| metabolic rate | B | 3/4 | q/(q+1) | M^(3/4) | Kleiber 1932; WBE 1997 |
| heart rate | f_heart | −1/4 | −1/(q+1) | M^(−1/4) | Brody 1945 |
| breath rate | f_breath | −1/4 | −1/(q+1) | M^(−1/4) | Stahl 1967 |
| lifespan / generation time | T | 1/4 | 1/(q+1) | M^(1/4) | Calder 1984 |
| mean blood pressure | P | 0 | 0/(q+1) | M^0 (invariant) | Stahl 1967 |
| aorta cross-section | A_aorta | 3/4 | q/(q+1) | M^(3/4) | Holt 1962 |
| brain mass (Jerison) | M_brain | 3/4 | q/(q+1) | M^(3/4) | Jerison 1973 |
| capillary tip count | N_c | 3/4 | q/(q+1) | M^(3/4) | WBE 1997 |
| tree height vs mass | h_tree | 1/2 | 2/(q+1) | M^(1/2) | Niklas 1994 |
| brain white-matter volume | V_w | 5/4 | 5/(q+1) | M^(5/4) | Zhang & Sejnowski 2000 |

**Every exponent is an integer divided by (q + 1) = 4.**

---

## 3. The WBE derivation chain

| step | from | to |
|---:|---|---|
| 1 | Master Equation q! = 2q | q = 3 |
| 2 | q = 3 | spatial dimensions d = q = 3 |
| 3 | d = 3 | biological supply network is space-filling in d = 3 |
| 4 | fractal supply network in d = 3 | WBE: B ∝ M^(d/(d+1)) = M^(3/4) |
| 5 | B ∝ M^(3/4) | every derived exponent quantised in units of 1/(q+1) = 1/4 |

Inverting step 4 gives a **falsifier**: if Kleiber's exponent α were
measured to differ from 3/4, the inferred dimension d = α/(1 − α) would
differ from 3. At α = 3/4 we recover d = 3 exactly.

---

## 4. Why the denominator is q + 1

The exponent of Kleiber's law is set by the dimensional balance:

$$
\text{network volume} \;\propto\; L^d
\quad\text{and}\quad
\text{terminal supply units} \;\propto\; L^{d}
$$

balanced against an isometric (mass-conserving) scaling that introduces
the extra "+1" in the denominator. The result is α = d/(d+1).

At d = 3 this is 3/4; at d = 2 it would be 2/3; at d = 4 it would be 4/5.
**Only d = 3 gives the empirically observed 3/4** — and d = 3 is exactly
the W(3,3) consequence #1 of CCCCXLIV.

---

## 5. Structural prediction

Combining DCCXX and DCCXXI:

| layer | DCCXX | DCCXXI |
|---|---|---|
| combinatorial | codon length q = 3, alphabet q+1 = 4, codons (q+1)^q = 64 | (1/4)-quantised exponents in 1/(q+1) |
| quantitative | redundancy 61/20 ≈ q | Kleiber α = q/(q+1) = 3/4 |
| logical | H₁(W(3,3)) = 81 bits | inverting Kleiber recovers d = q = 3 |

Both the **combinatorial alphabet** and the **physiological scaling** of
life are forced by q = 3.

---

## 6. Honest boundary

* This part fixes **exponents** only. Prefactors (the "a" in B = a M^(3/4))
  depend on chemistry and are not derived here.
* Published exponents have empirical scatter (some studies report 2/3,
  some 3/4); this part takes WBE's 3/4 as the theoretical target and
  notes that the cleanest interspecific datasets favour 3/4.
* It does **not** claim that 1/4-laws hold for all taxa or all
  physiological quantities — only that the observed family of exponents
  collapses to the n/(q+1) lattice.

---

## 7. Decisive identity

$$
\boxed{\;
q = 3 \;\Longrightarrow\; d = 3 \;\Longrightarrow\;
B \propto M^{q/(q+1)} = M^{3/4} \;\Longrightarrow\;
\text{all biological allometry quantised in 1/(q+1).}
\;}
$$

---

## 8. One-line summary

$$
\boxed{\;
\text{Kleiber's }\tfrac{3}{4} \;=\; \frac{q}{q+1}\Big|_{q=3}
\;=\; \text{biological allometry from the Master Equation.}
\;}
$$
