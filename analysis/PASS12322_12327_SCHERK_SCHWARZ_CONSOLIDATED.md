# Passes 12322–12327: the Scherk–Schwarz statement, consolidated

Claude track. Producer: `analysis/w33_pass12322_to_12327_scherk_schwarz_consolidated.py`.

**12316 withdrawn.** The bicharacter gives the e6 phase of a winding-w state as ½(V_h·λ + wλ²) ≡ ½V_h·λ, because λ² is even. So the
half-integer momentum shift of the Witten-twisted states is the same for every winding: a lattice Wilson line is not a freely acting
translation. There is no (w = 1, n = 0) state.

**Small-R channels (12322).** Levels are matched by L_int = R_int − n·w, with n ∈ ℤ + ½.

| sector (right vacuum) | channel | needs L_int | exact L_min | status |
|---|---|---|---|---|
| Witten θ², θ⁴ (−1/6) | n·w = ½, at R = √(α′/2) | −2/3 | −1/3 | closed |
| Witten untwisted (−½) | n·w = 0, ½ | −½, −1 | 0 (control: the 10D SO(16)² tachyon-freedom) | closed |
| winding along e5 (coset V0 + W5) | w₅ = 1, n₅ = 0 | −½ | −½ | open: tachyonic for R₅ < √2·√α′ (parent and brother) |

**Consolidated statement (12323), for the SM_810 lineage.**

- **Computed:**
  - the zero-winding spectrum is tachyon-free (engine solver);
  - the right-moving vacua;
  - the momentum shift (bicharacter, validated 232/232 and 124/124 pre-registered);
  - the exact level minima.
- **Argued:** the circle mass formula. The projections of winding states are not computed.
- **Result:**
  - **tachyonic for R₆ > 0.61√α′**;
  - no tachyon channel for R₆ < 0.61√α′;
  - R₅ ≳ 1.41√α′ is required.
- **Open:**
  - the one-loop potential in this string-scale window (the n_F − n_B = −222 proxy is a large-R estimate and does not apply here);
  - k_Y = 8/3.

## Other results

- **12324:** 99 of the 1399 parents are tachyon-free; none is a three-generation left-right model.
- **12325:** the twelve Z2×Z6-I brothers are all excluded: nine by renormalisable QL d^c, one with no cubic Yukawa, two by textures.
- **12326 (user decisions):**
  - The main checkout was fast-forwarded. 68 blockers went to a backup: 65 identical up to whitespace, 3 testbenches different.
  - The bug report stays in the repo, unsent.
