# Flavor currents exclude the bifundamental threshold's direct ultraviolet route

The bifundamental threshold generates the desired W33 mixed cubic at tree level. Its proposed supersymmetric ultraviolet route faces two exact obstructions. For the stated cubic superpotential, no unitary fixed point can have both gauge factors active, whether the alternating cubic is present or absent. With only E6 interacting, the branch without the alternating cubic is also excluded. In the remaining E6-only branch, both mass operators needed for the threshold are irrelevant if they survive as chiral primaries. The tests allow the standard accidental corrections from free chiral operators and assume the elementary field and current description. [The exact mediator threshold](2026-11-13_mixed_mediator_threshold.md) · [Known supersymmetric product-group fixed points](https://arxiv.org/abs/1709.06953)

## Cubic support and exact currents

At the fixed-point test set both dimensionful inputs to zero. Keep the two mixed terms `Z1 A X+` and `Z0 A U`, where X+ is proportional to X0+X1 and U is the added fundamental bifundamental. The added conjugate D has no cubic coupling. If present, the signed alternating cubic couples `X+,X−,X2`, where X− is proportional to X0−X1. In either support the unpaired X− and X2 have an exact species SU(2). Its symmetry forces their scalar R charges to agree.

Let `p=R(X+)`, `q=R(U)`, `r=R(A)`, and let u be the common unpaired X charge. With both gauge factors active, the anomaly equations are `3Σ+4r=21` and `9Σ+5R(S)=66`, where Σ sums the seven bifundamental charges. The mixed cubics require `R(Z1)=2−r−p` and `R(Z0)=2−r−q`. The alternating cubic, when active, imposes `u=1−p/2`. In either case `R(S)=(3+12r)/5`. The E6 condition alone gives

```text
R(D) = 1+p+2r/3       with the alternating cubic
R(D) = 3+2r/3−2u      without the alternating cubic.
```

For each nonzero conserved flavor current F, the microscopic Weyl anomaly trace `Tr R F²` must be strictly negative. When an operator O with trial charge below 2/3 becomes free, its correction is `(2/3−R_trial(O)) Tr_O F²≥0`. Including free operators therefore strengthens the necessary sign. A derivative of the trial charge chart with respect to an independent coordinate defines a conserved flavor generator that preserves the cubic and gauge constraints. The unpaired species Cartan F has charges +1 and −1 on X− and X2. [Current positivity](https://arxiv.org/abs/hep-th/0304128) · [Free-field correction](https://arxiv.org/abs/hep-th/0308071)

## A contradiction with both gauge factors active

The q current acts on U and Z0 with opposite charges and has trace `−81r`, so r is strictly positive. With the alternating cubic the unpaired SU(2) Cartan trace is `−81p`, and the p current gives `(243/4)p−27r`. Hence `0<p<4r/9`. The independent current `∂p+∂r−(1/2)∂q` has trace

```text
−(3/100)(1275p−733r−4732).
```

Since `1275·4/9 < 733`, this trace is positive throughout the required region. Without the alternating cubic the unpaired Cartan trace is `162(u−1)`, so `u<1`. The u current has trace `216r−486u+486>0`. These contradictions exclude both choices without needing a chiral-ring census. In the branch without the alternating cubic, all currents in the contradiction are neutral on S, so the same proof holds when only E6 is active.

## Both threshold masses fail the relevance test in the E6-only branch

The rank-changing input multiplies `D X2`, whose scalar R charge exceeds two by `p/2+2r/3` with the alternating cubic and `1−u+2r/3` without it. These gaps are positive by the q current and the unpaired Cartan, even if the family gauge coupling is zero. If this input vanishes, the mass term DU alone removes the U pairing and leaves only rank one in the inherited low-energy mixed coupling.

For the alternating cubic with E6 alone, the spectator is free and the `∂r` variation can leave S neutral. The same combined current now has trace `165−153p/4−465r/4`. Negativity and `p<4r/9` force `r>660/533`. In particular, the R gap of `D X2` is strictly larger than 440/533.

The mediator's ordinary mass DU is also irrelevant in this branch. Take the Schur complement of the q current in the two-current anomaly matrix for q and r, keeping the spectator neutral. Write `x=(2q+r−2)/r`. Negativity of that matrix gives

```text
p > (4+r+27 r x²)/60.
```

Since `R(DU)−2=p+r/6+r x/2`, the bound completes to a square and gives

```text
R(DU)−2 > 1/15 + r[2/45 + (9/20)(x+5/9)²] > 973/7995.
```

These are strict relevance tests near the specified massless fixed point. A chiral primary of R charge R has dimension 3R/2, and a removed chiral-ring class supplies no independent superpotential direction.

## A conditional family-only obstruction

With only the family factor active, A is a gauge singlet, so `r≥2/3` if it survives as an interacting chiral primary with the stated cubic couplings. Now `d=R(D)` is an independent coordinate and `R(S)=(66−9Σ)/5`. The d current assigns D charge one and S charge −9/5. Its trace is

```text
(81/25)(7d+36r+18p−11)   with the alternating cubic
(81/25)(7d+36r−36u+25)   without the alternating cubic.
```

The unpaired species current still requires p>0 or u<1, respectively. In each case negative trace forces `d<−13/7`. A family antibaryon built from three D fields has trial R charge 3d and d-current charge three. It is nonzero on a classical F- and D-flat configuration. Set all other fields to zero and take the three family columns of D orthonormal. This fully breaks the family gauge group. If one such antibaryon survives in the quantum chiral ring, its free-field correction adds `9(2/3−3d)`. The corrected trace is strictly positive over the required region for either cubic choice. The family-only branch is therefore excluded under these two quantum-primary assumptions. Changes to the cubic support, new interacting accidental currents, and thresholds involving other fields remain open.

With both gauge factors inactive, the elementary chiral fields are gauge-singlet local operators in the ungauged matter theory. Unitarity and the charge-two condition for any active cubic would force its three fields to saturate the free bound, incompatible with a genuine interacting cubic. In the Gaussian limit the two gauge coefficients are −39 and −93 for this inventory, so weak gauging is marginally irrelevant toward the infrared for both factors.

Run `python analysis/toe_20261113_bifundamental_mediator_uv.py` from the repository root. [Exact output](../data/toe_20261113_bifundamental_mediator_uv.json)
