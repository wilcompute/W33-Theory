# Passes 12310–12315: the candidate's fractional states clear the space-group rule, but its radius and its k_Y do not

Claude track. Producer: `analysis/w33_pass12310_to_12315_vacuum_potential_unification.py`.

| pass | result |
|---|---|
| 12310 | Left-right scan over all 2797 census dumps (pooled, no timeouts): **15** Scherk–Schwarz brothers give three chiral generations without chiral fractional charge. All 15 are V0 variants of **one** parent, SM_20260917_810; every brother is tachyon-free (each parent has 8 or 16 tachyonic states), and every one has n_F − n_B = −222. No other lineage among the 1399 models qualifies (within the T3R + Y′ ansatz). |
| 12311 | Under the **full** space-group rule (point group, Witten label, and fixed-point translations on the SU(3)²×SU(2)² lattice), all 48 fractional Weyl fermions pair up, at singlet degree 1–2. Control: the rule is live (an e5 shift rejects 134/134 pairs; an e1 shift is absorbed). Not imposed: the non-SUSY vertex rule; the vacuum itself. |
| 12312 | Scherk–Schwarz proxy V ≃ ξ(n_F − n_B)/R⁴: the candidate has n_F − n_B = 604 − 826 = **−222**, so the radius is pushed **inward**, toward the region R₆ < 1.63√α′ where its tachyon returns. Proxy only. |
| 12313 | With SM running, unification needs k_Y ≈ 1.23–1.29; **8/3 is far off**, and adding light matter moves the ratio the wrong way unless SU(2)-charged matter dominates. Open obstruction. |
| 12314 | Audit: every corpus tachyon count with the non-SUSY engine reads `T_NFIELDS` (the full tachyonic configuration, which the verbose solver confirms). No older claim is affected. |

**Synthesis.** The candidate keeps what it had:

- three chiral generations;
- no chiral fractional charge;
- liftable fractional states, now under the full space-group rule.

But two physical obstructions now stand against it:

- the radius runs into its tachyonic region (proxy level);
- k_Y = 8/3 does not unify.
