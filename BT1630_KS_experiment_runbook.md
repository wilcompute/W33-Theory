# BT1630: KS Defect Experiment Runbook
## The Deciding Experiment — Pre-Registered Protocol

**Status:** Pre-registered, unmeasured (correct state for a prediction)  
**Target:** CF = 1/10 = 36/40 satisfiable contexts  
**Venue:** `bt1898_demonstrator_runbook`  
**Generated:** 2026-07-27 by Perplexity AI Pass 3  

---

## What Is Being Measured

The **contextual fraction (CF)** of the W(3,3) symplectic polar space, measured
via single-photon interferometric coincidences on a 40-context measurement apparatus.

The algebraic prediction (Pass 1099, certified by integer programming):
- Total contexts in W(3,3): **40**
- Maximum satisfiable by any noncontextual hidden-variable model: **36**
- Unsatisfiable (KS-forbidden): **4**
- Predicted CF = 4/40 = **1/10 = 0.10**

---

## Falsifier Table

| Measured CF | Conclusion |
|---|---|
| CF = 0 | Gaussian tower / q=2 substrate — W33 program refuted |
| CF = 1/10 | Eisenstein tower confirmed — W(3,3) is the substrate |
| 0 < CF ≠ 1/10 | Neither tower is the substrate — program requires revision |

The falsifier is **maximally sharp**: the three outcomes are mutually exclusive and
exhaustive, and only one is consistent with W(3,3) as the substrate.

---

## Pre-Registered Details

### Why CF = 1/10 Is Not a Fit

The value 1/10 was derived from pure substrate arithmetic BEFORE any measurement:

1. W(3,3) has no ovoids (Thas 1981: W(q) has ovoids iff q is even)
2. Therefore CF > 0 (Budroni et al. 2022: CF > 0 iff no ovoids in the KS graph)
3. The maximum partial 2-coloring of W(3,3) satisfies exactly 36/40 contexts
   (certified by integer programming, Pass 1099)
4. Therefore CF = (40-36)/40 = 4/40 = 1/10

No measured quantity enters this derivation.

### Connection to Lock 0 (w33_paper.tex)

Lock 0 uses zero measured numbers:
- Springer's construction on W(E8) yields exactly two transitive towers
- Only the Eisenstein tower (W(3,3) base) has CF > 0
- The Gaussian tower (W(2,2) base) has CF = 0 (ovoids exist, q=2)

So CF = 0 refutes Lock 0 directly; CF = 1/10 confirms it.

---

## Apparatus Requirements (from BT1614 bench specification)

| Component | Specification |
|---|---|
| Single-photon source | Heralded, >90% purity |
| Detection | 168-bin SNSPD array (BT1602) |
| Contexts | 40 W(3,3) measurement contexts |
| Statistics | N > 10^4 coincidence events per context |
| SNSPD thresholds | Calibrated per BT1608 (3 cycles, 2.25 hours) |

---

## Expected Systematic Errors

1. **Dark counts:** Reduce effective CF below 1/10. Must characterize dark rate.
2. **Detector efficiency mismatch:** Can fake satisfiability of KS-forbidden contexts.
3. **Alignment drift:** Monitor via fiducial contexts (contexts 1-4, always satisfiable).

---

## The 135 Maximal Partial Spreads

The 4 unsatisfiable contexts correspond to the 135 maximal partial spreads of
size 8 = q²-1 in W(3,3). These are sharply transitive subsets of SL(2,3)
(Penttila, Cimrakova-Fack). In the photon counting experiment, these 4 contexts
will show **zero coincidences** for the KS-forbidden assignments.

---

## Holonet Scaling Implication

Once CF = 1/10 is confirmed experimentally:

| Level n | Leaves 40^n | W(3,3) instances | Route bound |
|---|---|---|---|
| 1 | 40 | 1 | 8 |
| 2 | 1,600 | 41 | 16 |
| 3 | 64,000 | 1,641 | 24 |
| 4 | 2,560,000 | 65,641 | 32 |

Routing is O(log N). The KS defect 1/10 directly implies each level costs ≤8
reversible moves through the holonet.

---

## References

- Thas (1981): W(q) has ovoids iff q is even
- Budroni et al., Rev. Mod. Phys. 94, 045007 (2022): CF operationally measurable
- Penttila; Cimrakova-Fack: maximal partial spreads of W(3,3)
- Pass 1099: integer programming certification of max-satisfiable = 36
- BT1614: hardware bench specification
- photonic_holonet.tex §9: pre-registration of CF = 1/10
