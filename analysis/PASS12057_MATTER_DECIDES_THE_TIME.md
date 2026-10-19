# Pass 12057: matter decides the time

* **Producer:** `analysis/w33_pass12057_matter_decides_the_time.py` (5/5 checks)
* **Certificate:** `data/w33_pass12057_matter_decides_the_time.json`
* **Regression:** `tests/test_w33_pass12057.py`
* **Drivers:** `analysis/search_drivers_12057/`
* **Track:** Claude. Reservation `f9d73a0b0`.
* **Continues:** 12056. **Uses:** 11884 and 11892.

## Setting

On the E8-Higgs Cartan every one-loop angular potential is a combination a F + b G, where:
* F = sum e^2 log e and G = sum e log e;
* a is the boson-fermion imbalance: bosonic loops give a > 0, adjoint fermions a < 0, and SUSY a = 0;
* b is the soft scalar mass^2, to first order.

**Competing vacua** (these agree with the 11892 certificate):

| vacuum | F | G | massless vectors |
|---|---|---|---|
| Witting ray: a W(3,3) point, trinification, **one time** (12056) | -6 log 3 | -18 log 3 | 24 |
| C10 point | -6.2303 | -21.8539 | 0 |
| F-maximum (cusp) | -6.2266 | -21.768 | 4 |

## Phase map on the (a, b) circle

The map comes from a scan at 15 deg plus spot checks.

**One time (the Witting point):** theta = 0 and theta in [~190, 360] deg. That is **b <= 0**, with either a >= 0 or
|b| > ~0.18 |a|, which covers about half of all matter contents.

**Positive soft mass.** For any b > 0, the Witting ray stays stationary but is no longer a minimum. The vacuum deforms
continuously off the point toward C10: at 8 deg it has 0 massless vectors and lies below Witting.
* **A correction to my own estimate:** the naive two-pattern crossing (9.86 deg) is not the boundary. The boundary is
  b = 0 exactly.
* **Link to the hierarchy:** by 11891 the displacement is the family-hierarchy parameter, eps ~ delta.

**The other phases.**
* **C10:** about 15-165 deg.
* **Intermediate:** a phase with 10 massless vectors at 188 deg.
* **F-maximum:** at 180 deg.
* **Fermion-side edge of one time:** in (188, 193) deg, consistent with the F-max / Witting crossing at 190.4 deg.

## Reading

**When the theory has one time:**
* bosonic loops give it;
* any negative soft mass gives it, unless fermions dominate by more than about 5:1;
* with SUSY, breaking along the D-flat direction **requires** m^2_soft < 0, so SUSY breaking lands on one time
  automatically.

**What the 11892 table assumes.** Its C10 entry (m^2 > 0) needs an independent radial stabiliser: with only a positive
soft mass, the origin is the vacuum.

## Companion result

The 2026-10-19 tick-frame note (`analysis/2026-10-19_tick_operator_frame_majorization.md`, commits 0fcbd55af and
74cfc92d6) proves 12055's single-tick selection for every fixed l_p (p >= 1) by majorization. 12055 had that only
numerically for l_2. The note's firewall -- that an event subspace alone does not fix the E8 real form without a
specified coupling -- is what 12056-12057 address: the coupling is the physical one-loop vacuum.

## Scope

* **Soft mass:** first order.
* **Fermions:** adjoint-type, whose spectrum equals the vector spectrum.
* **Potential:** angular only, with |x| fixed.
* **Twisted sectors:** not included.
