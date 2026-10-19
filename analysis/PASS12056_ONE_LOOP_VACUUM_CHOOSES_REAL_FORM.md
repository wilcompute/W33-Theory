# Pass 12056: the one-loop vacuum chooses the real form

* **Producer:** `analysis/w33_pass12056_one_loop_vacuum_chooses_real_form.py` (5/5 checks)
* **Certificate:** `data/w33_pass12056_one_loop_vacuum_chooses_real_form.json`
* **Regression:** `tests/test_w33_pass12056.py`
* **Track:** Claude. Reservation `991a8435c`.
* **Continues:** 12052-12055. **Connects:** to the corpus vacua 11884-11892.

## Root-level dictionary (exact, checked)

In the root model of 12052:

* **A2(p).** The fibre over a point p is an A2 root system.
* **E6(p).** The roots orthogonal to that fibre are **exactly the fibres over the 12 points collinear with p**: 72 roots,
  rank 6, closed. This is the corpus statement "a point of W(3,3) is E6 x SU(3)" (11887-11889).
* **D4 + D4.** The fibres over a tensor factorisation H1 + H2 are D4(H1) + D4(H2): 24 + 24 roots, rank 4 each, closed
  and mutually orthogonal. This is the corpus statement "factorisation -> D4 x D4".

## Theorem (exact, all 40 points and all 45 factorisations)

For an inner involution theta_h, the maximal compact subalgebra k contains the Cartan and the even roots.

**(a) Point vacuum.** The trinification vacuum at p has centraliser e6(p) + h, with the family A2(p) broken to its
Cartan.
* **Containment:** the involutions whose k contains it are **exactly the three clock involutions at p**. No split
  involution contains it.
* **The family su(2):** each of the three keeps exactly one su(2) of A2(p), one per tick line.

**(b) Factorisation vacuum.** For d4 + d4 + h, the involutions containing it are **exactly the three split involutions
at that factorisation**. No clock involution contains it.

## Reading

**Which vacuum the matter selects.** The corpus vacuum phase diagram (11890-11892) answers this:
* **Bosonic Coleman-Weinberg loops** select a point (trinification).
* **Periodic adjoint fermions** in the Hosotani completion select a tensor factorisation.

**What that means for the real form.**
* **Bosonic loops choose one time.** The vacuum is the clock form E8(-24), anchored at the selected point, where that
  point's tick is central (12053).
* **Periodic adjoint fermions choose the split form.**

So the action asked for after 12055 is the Coleman-Weinberg potential of the E8 Higgs, which the corpus already has.

**The chain.**

| pass | result |
|---|---|
| 12052 | Real forms are two-qutrit structures. |
| 12053 | The tick is central in its real form. |
| 12054 | A Landau condensate has an event phase next to a split phase. |
| 12055 | The microscopic tick model is in the event phase. |
| 12056 | The one-loop vacuum chooses which phase, by its matter content. |

## Scope

* **What is shown:** root-level containment in the 12052 root model.
* **What is taken from the corpus:** the identification of the corpus vacua with E6(p) x A2(p) and D4 x D4. It is not
  re-derived here in the sl9 + Lambda^3 model.
* **Fermions:** charged fermions are excluded from the bosonic vacuum, as in 11884.

## What is not new

* E8 > E6 x A2 and E8 > D4 x D4.
* The real forms of E8.
* The corpus vacua and dictionary.
