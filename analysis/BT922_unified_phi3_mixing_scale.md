# BT922 — The Unified Φ₃ Mixing Scale (hard open #1, unification)

**Status: PROVEN (`analysis/bt922_unified_phi3_mixing_scale.py`, data `data/bt922_unified_phi3_mixing_scale.json`)**

BT920 gave the lepton (PMNS) mixing as tribimaximal deformed by 1/Φ₃. BT922
adds the quark (CKM) side and unifies: **both fermion-mixing sectors are
governed by the single scale Φ₃ = q²+q+1 = 13.**

## The two sectors, one scale

**Quark (CKM):** the Cabibbo angle is the q/Φ₃ rotation,

```text
tan θ_C = q/Φ₃ = 3/13   (sin θ_C = q/√(Φ₃²+q²) = 3/√178)
```

matching observed |V_us|/|V_ud| = 0.2304 to **0.18%**.

**Lepton (PMNS):** tribimaximal deformed by 1/Φ₃ (BT920),

```text
sin²θ₁₂ = (1/3)(1 − 1/Φ₃) = 4/13     sin²θ₂₃ = (1/2)(1 + 1/Φ₃) = 7/13
sin²θ₁₃ = λ/(Φ₆Φ₃) = 2/91
```

## The quark/lepton dichotomy as one scale, two regimes

| sector | base mixing | deformation | scale |
| --- | --- | --- | --- |
| quark (CKM) | identity | q/Φ₃ rotation | Φ₃ = 13 |
| lepton (PMNS) | tribimaximal | 1/Φ₃ deformation | Φ₃ = 13 |

Quark mixing is **small** (a rotation by arctan(q/Φ₃) ≈ 13° off the identity);
lepton mixing is **large** (a deformation off the already-large tribimaximal).
The famous quark/lepton mixing dichotomy — CKM near-identity vs PMNS near-TBM
— is here two regimes of *one* scale Φ₃: the quarks sit near the identity and
rotate by q/Φ₃, the leptons sit at the S₃-symmetric tribimaximal point and
deform by 1/Φ₃.

The scale **Φ₃ = q²+q+1 = 13** is the third cyclotomic value — the number of
points in PG(2,3), and the Singer C₁₃ clock (BT807). So the fermion
flavor-mixing scale is the substrate's Φ₃ structure; both the quark rotation
and the lepton deformation are measured in units of 1/Φ₃.

## Reading

This unifies hard-open-#1 across quarks and leptons: the entire
fermion-mixing sector — four CKM quantities and three PMNS angles — is
controlled by the single substrate scale Φ₃ = 13, with the quark sector a
q/Φ₃ rotation off the identity and the lepton sector a 1/Φ₃ deformation off
the S₃-symmetric tribimaximal point. The remaining open piece (why the scale
is exactly Φ₃, from the within-grade profile) is now a *single* question for
both sectors, not seven separate angle fits.

## Open

- Derive the scale Φ₃ as the flavor-breaking ratio from the within-grade
  (q²=9) profile — one derivation now suffices for all of CKM + PMNS.
- Why quark = rotation-off-identity but lepton = deformation-off-TBM (the
  Dirac vs Majorana / the up-down vs charged-neutral structure).
