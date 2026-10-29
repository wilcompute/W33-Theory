# Passes 12373–12376: a targeted Witten-shift search

Claude track. Producer: `analysis/w33_pass12373_to_12376_targeted_witten_shift_search.py`. Drivers: `analysis/search_drivers_12373/`
(`newv0.py` scan, `filt.py` radius filters, `vet.py`/`vet_pairs.py`/`vet_loose.py` exotics and hypercharge).

This follows the closure of the 99-parent sample (12368). The question there was whether new models, rather than new tests, would help.

## 12373: enumeration

All admissible Witten shifts were enumerated for the SUSY parents of the five three-doublet lineages:

| quantity | number |
|---|---|
| admissible shifts | 111108 (the earlier construction tried ≤ 400 per parent) |
| sampled (3000 per parent) | 15000 |
| strict-consistent | 7391 |
| tachyon-free at the orbifold point | 2141 |
| **three net (3,2) doublets** | **202** (all five parents; the whole 99-parent sample had 17) |

## 12374: radius filters

| large radius | small radius | models |
|---|---|---|
| clean | clean | **27** |
| clean | tachyonic | 75 |
| tachyonic | clean | 47 |
| tachyonic | tachyonic | 53 |

So the radius obstruction found in 12363–12368 is **not generic**.

Of the 102 models that are safe at large radius, 43 have chiral states charged under both the SM group and a hidden non-abelian factor.
Those are fatal for every hypercharge.

## 12375: hypercharge

For the other 59 (27 of them clean at every tested radius), no three-generation hypercharge exists:

- not in the base search;
- not in any of the 65 SU(3)×SU(2) pairings with three net doublets;
- not in the relaxed search so far. Its coverage is recorded in the certificate, and the run continues.

**Mechanism** (diagnosed on SM_574_c420):

- The gauge group is SU(3)×SU(2)×SU(3)′×SU(2)′.
- The second pair carries its own chiral (3,2)-type matter: a **twin sector**.
- The quark and colour conditions can be met only by giving the twin matter visible hypercharge.
- With a hypercharge-neutral hidden sector, the problem is infeasible. SM_574 (12364) fails the same way.

## 12376: synthesis and open questions

**Synthesis.** Radius stability is achievable. In this family the failure is the twin sector, which the visible hypercharge cannot avoid.

**Open:**

1. A twin-Standard-Model reading, with visible Y plus a twin Y′ (two U(1)s), and its phenomenology (mirror/twin matter).
2. The untwisted winding channels.
3. The 96108 unsampled shifts.
