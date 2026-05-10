# Part CCCXXVIII — Bottom Yukawa $y_b(\overline{\rm MS}, m_b) = q/(\mu+1)^3 = 3/125$

**Bridge:** `exploration/PART_CCCXXVIII_BOTTOM_YUKAWA_BRIDGE.py` — 17/17 Verified
**Tests:** `tests/test_bottom_yukawa_cccxxviii.py` — 17/17 pass
**Results:** `PART_CCCXXVIII_bottom_yukawa_results.json`

---

## 1. Headline result

The Standard Model bottom-quark Yukawa coupling, $\overline{\rm MS}$
scheme at the b-quark mass scale $m_b \approx 4.18$ GeV, admits a
clean W(3,3) closed form:

$$
\boxed{\;
y_b(\overline{\rm MS},\,m_b) \;=\; \dfrac{q}{(\mu+1)^3} \;=\; \dfrac{3}{125}.
\;}
$$

The numerator $q = 3$ is the Master Equation prime; the denominator
$(\mu+1)^3 = 125$ is the cube of the smallest small-prime above
$\{\lambda, q\}$ in the W(3,3) Bernoulli tower.

---

## 2. Comparison with PDG 2024

| quantity | W(3,3) | measured | $z$ |
|---|---:|---:|---:|
| $y_b(\overline{\rm MS}, m_b)$ | $3/125 = 0.02400$ | $0.02401 \pm 0.00017$ | $+0.05$ |
| $m_b(\overline{\rm MS})$      | $4.179$ GeV       | $4.18 \pm 0.03$ GeV    | $-0.05$ |

**Both within $0.05\sigma$.**

---

## 3. The mirrored cube structure with the top Yukawa

The two heaviest quark Yukawas now have W(3,3) closed forms of
mirrored cube structure:

| | W(3,3) form | numerator | denominator |
|---|---|---|---|
| Top    | $y_t({\rm pole})^3 = v/(v+1)$    | $v = 40$   | $v + 1 = 41$    |
| Bottom | $y_b(\overline{\rm MS}) = q/(\mu+1)^3$ | $q = 3$    | $(\mu+1)^3 = 125$ |

**Top:** Yukawa is *cubed*, denominator is linear ($v+1$).
**Bottom:** Yukawa is *linear*, denominator is *cubed* ($(\mu+1)^3$).

The cube shifts between numerator and denominator across the two
quarks. This is suggestive of a $\mathrm{SU}(3)$ colour structure —
each quark Yukawa entering with three colour components — but I do
not yet have a structural derivation, only the empirical pattern.

---

## 4. Cross-link with CCCXXV

The integer $\mu+1 = 5$ already appeared in CCCXXV as the denominator
of the CKM Wolfenstein parameter $\bar\rho$:

$$
\bar\rho \;=\; \!\left(\dfrac{\lambda}{\mu+1}\right)^{\!2} \;=\; \dfrac{4}{25}.
$$

The bottom Yukawa $y_b$ uses the *cube* of the same $\mu+1$:

$$
y_b \;=\; \dfrac{q}{(\mu+1)^3} \;=\; \dfrac{3}{125}.
$$

So $\mu + 1 = 5$ recurs in the W(3,3) fingerprint of:

* CKM $\bar\rho$ (squared) — CP-violation apex (CCCXXV);
* bottom-quark Yukawa (cubed) — heavy-quark hierarchy (CCCXXVIII).

---

## 5. Updated empirical inventory

With CCCXXVIII the count of within-$1\sigma$ W(3,3) closures rises
to **nine dimensionless plus three dimensional**:

**Dimensionless (9):**
$Q$ (CCCXXII), $\sin^2\theta_W$ (CCCXXIII), $\lambda_H$ (CCCXXIV),
$\lambda, A, \bar\rho, \bar\eta$ (CCCXXV), $y_t^3$ (CCCXXVI), $y_b$ (CCCXXVIII).

**Dimensional from $v_{\rm EW}$ alone (3):**
$m_H = v\sqrt{13/50}$, $m_t = (v/\sqrt{2})(40/41)^{1/3}$,
$m_b = (3/125)\,v/\sqrt{2}$.

The two heaviest quarks (top, bottom) and the Higgs are now all
dimensionful predictions of $v_{\rm EW}$ alone.

---

## 6. Honest boundary

* $\overline{\rm MS}$ at $m_b$ scheme. Pole-mass $y_b({\rm pole})
  \approx 0.0275$ differs from $3/125 = 0.024$ by $\sim 14\%$ due to
  the well-known b-quark renormalon shift.
* The W(3,3) prediction is at $\overline{\rm MS}$ at $m_b$.
  Running to other scales gives different numerical values;
  the *boundary* value is at the b-quark mass.
* The exact $m_b$ extraction from heavy-quark expansion has
  $\pm 30$ MeV uncertainty; the W(3,3) prediction tracks the
  central value to better than that.

---

## 7. Decisive identity

$$
\boxed{\;
y_b(\overline{\rm MS},\,m_b) \;=\; \dfrac{q}{(\mu+1)^3}
\quad\Longleftrightarrow\quad
m_b \;=\; \dfrac{3\,v_{\rm EW}}{125\sqrt{2}} \;=\; 4.179\ \text{GeV}.
\;}
$$

A single small W(3,3) integer ratio fixes the second-heaviest quark
mass to $0.05\sigma$ of the PDG world average.

---

## 8. One-line summary

$$
\boxed{\;
y_b \;=\; \dfrac{q}{(\mu+1)^3} \;=\; \dfrac{3}{125}
\quad\Rightarrow\quad
m_b \;=\; 4.179\ \text{GeV}.
\;}
$$
