# BT891 — The CKM/PMNS Texture Is Forced by the Derived Grading (#1)

**Status: PROVEN (machine-verified, `analysis/bt891_yukawa_texture_from_grading.py`, data `data/bt891_yukawa_texture_from_grading.json`)**

The CKM/PMNS structure re-founded on the *derived* grading. Where Pillars
65–68 fitted the Yukawa tensor, BT875 derived the Z₃ grading — so the texture
is now forced, not assumed.

## The theorems

- **T1:** the cubic coupling T on the matter shell (support = the 36
  within-shell tritangent triples) is **grade-homogeneous** in the R-eigenbasis
  (9+9+9): zero grade-violating entries — T[i,j,k] = 0 unless
  g_i+g_j+g_k ≡ 0 (mod 3), confirming BT875 at the tensor level.
- **T2:** a Higgs VEV of grade g_H gives a Yukawa matrix Y(g_H) supported on
  exactly the generation pairs with g_a+g_b ≡ −g_H — a **circulant texture**,
  one per Higgs grade:

```text
g_H = 0 → couples (0,0),(1,2),(2,1)
g_H = 1 → couples (0,2),(1,1),(2,0)
g_H = 2 → couples (0,1),(1,0),(2,2)
```

- **T3:** up-type and down-type Yukawas built from Higgs of **different**
  grades have misaligned circulant textures, so **nonzero CKM mixing is
  forced**; same-grade Higgs → aligned eigenbases → no mixing. The CKM/PMNS
  *pattern* is the up-vs-down Higgs grade offset; the exact *angles* are set by
  the within-grade Higgs profile (the residual input).

## Reading

The fermion mixing matrices are not free — their *structure* is the derived
Z₃ grade arithmetic. Each Higgs grade selects a circulant 3×3 generation
coupling (a Z₃ Clebsch-Gordan channel), the up and down sectors couple through
possibly-different grades, and the misalignment of their textures is the CKM
(quarks) / PMNS (leptons) matrix. This makes the *existence and pattern* of
quark/lepton mixing a theorem of the substrate (the grade offset), reducing
the free input to the within-grade Higgs profile — the part Pillar 66
optimized (CKM error 0.00255). The grading that was previously fitted is now
derived (BT874/875), so the texture skeleton is first-principles.

## Open

- The exact CKM angles: re-run the Pillar-66 optimization with the texture
  *constrained* to the BT891 circulant pattern (fewer free parameters,
  derived skeleton).
- The CP phase as the relative phase between the up and down circulant
  channels (a genuine Z₃ phase, tying to BT878's charge-conjugation).
