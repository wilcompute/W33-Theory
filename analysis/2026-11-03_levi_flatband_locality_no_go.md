# 2026-11-03 — Levi flat-band locality obstruction across GF(2), GF(3), GF(4), GF(5)

**Status:** machine-verified finite mathematics for four fields; symbolic derivation for generalized quadrangles of order (q,q). This is not a derivation of general relativity, matter dispersion, a spacetime metric, a physical particle mass, or a TOE.

## Why this front

The current W33 project uses an 81-dimensional Hodge/Kirchhoff cycle sector as a protected information carrier. Prior owners established the W33 Levi graph (80 vertices, 160 edges), the 160-flag line graph, the exact radial projector with coefficients (81,-27,9,-3,1), and folded-Hashimoto propagation compressed to a parity-dependent scalar. Other November 3 work has already checked the linear spin-2 constraint closure on an imposed flat lattice. The missing physical question is whether **protected topology can itself support dispersive local quantum dynamics**.

Our new audit asks precisely: (i) does the W33 projector follow a broader q-family; (ii) what does a genuinely local flag defect do to the protected subspace; (iii) does a projected local defect remain physically local; and (iv) can onsite disorder preserve the entire protected cycle space without an extra nonlocal correction?

Related existing repo files: `analysis/w33_levi_kirchhoff_cycle_projector.py`, `analysis/w33_levi_flag_association_scheme.py`, `analysis/bt621_higher_folded_hashimoto_sector_scan.py`, `analysis/2026_11_03_local_spin2_hamiltonian_closure.py`, and `analysis/2026-11-03_six_nongeometric_toe_frontiers.md`. This is **not** a duplicate assertion that the protected sector has dimension 81; it derives and tests its local-perturbation response across distinct fields.

## Exact generalized-quadrangle family

Let `q` be a prime power, `W(3,q)` the classical rank-two symplectic generalized quadrangle, and `L_q` its bipartite point-line incidence (Levi) graph. Standard GQ incidence counts imply:

```text
points = lines = (q+1)(q²+1) = v
Levi vertices = 2v
Levi edges (flags) = (q+1)v = E = (q+1)²(q²+1)
Levi beta_1 = E - 2v + 1 = q^4.
```

Thus the existing `q=3` protected rank 81 is the q^4 special case, the same power that appears as the Steinberg degree for the type-C2 finite building. This is an **exact rank/count identity**, not evidence that q or a universe's dimension is dynamically selected.

Let `X_q` be the line graph of `L_q` (so its `E` vertices are the Levi flags). It is distance regular with valencies and intersection array:

```text
distance d                  0      1       2       3       4
shell size k_d              1     2q     2q²     2q³     q⁴
diagonal kernel numerator  q⁴    -q³      q²      -q       1

b=(2q,q,q,q), c=(1,1,1,2)
and for d=1,2,3: a_d=q-1; a_4=2q-2.
```

For its distance-`d` zero-one matrix `A_d`, define

```text
K_q = q⁴ A_0 - q³ A_1 + q² A_2 - q A_3 + A_4.
```

**Claim (and elementary derivation):**

```text
P_cycle = K_q/E
P_cycle²=P_cycle;  rank(P_cycle)=q⁴
A_X P_cycle = -2 P_cycle.
```

The line-graph adjacency `A_X=U^T U-2I` for unsigned vertex-edge incidence `U` of the bipartite Levi graph. The oriented incidence `D` has the same kernel as `U` because the Levi graph is bipartite. The `-2` eigenspace is therefore precisely `ker(D)` of dimension `q⁴`.

For a fixed base flag, the distance-regular intersection recurrence has `2q` first neighbors; at levels 1–3 the neighbor counts toward the previous/same/next shell are `1,q-1,q`; at level 4 they are `2,2q-2,0`. Substituting `k_d=(-q)^(4-d)` into the three-term recurrence yields `A_X K_q=-2K_q` **in every shell**. In a distance-regular graph each distance matrix is polynomial in `A_X`, so `K_q` acts scalarly on its `-2` eigenspace and vanishes on the others. Its diagonal is `q⁴`, hence `tr(K_q)=Eq⁴` and its sole nonzero eigenvalue is `E`. This proves `K_q²=E K_q`.

No lattice spacing or physical time appears in this proof.

## Independent field enumerations

A standalone symplectic-vector implementation normalizes `PG(3,q)` representatives, constructs all totally isotropic two-planes, extracts Levi flags and their 4-distance line graph, and audits `A K=-2K`, incidence annihilation, shell distributions and Hodge idempotence.

The `q=4` run uses actual `GF(4)=GF(2)[omega]/(omega²+omega+1)`, not the nonfield ring `Z/4Z`. `q=2,3` check the **complete integer matrix identity** `K²=EK`; `q=4,5` check deterministic basis-column and vector witnesses together with the symbolic proof above. All q values check all flag-base shell counts and every base-shell intersection profile.

| q | Points | Flags | Flat-band rank `q⁴` | p = q⁴/E | leakage/splitting |
|---|---:|---:|---:|---:|---:|
| 2 | 15 | 45 | 16 | 16/45 | sqrt(29/16) |
| 3 | 40 | 160 | 81 | 81/160 | sqrt(79/81) |
| 4 | 85 | 425 | 256 | 256/425 | 13/16 |
| 5 | 156 | 936 | 625 | 625/936 | sqrt(311/625) |

## The locality obstruction

**1. A symmetry-respecting adjacency polynomial has zero dispersion inside the protected band.**

For any `H=h(A_X)`, the whole protected cycle sector satisfies:

```text
H P_cycle = h(-2) P_cycle.
```

Every protected wavefunction accumulates only a common dynamical phase. This cannot generate distinct speeds, dispersion, or a causal cone **within this band**. This is a conditional no-go for polynomial-in-adjacency dynamics, not for every imaginable local multi-particle Hamiltonian.

**2. A single local defect produces a calculable protection-vs-dynamics conflict.**

Put `V=lambda |e><e|` at one flag. Let `P=P_cycle`, `Q=I-P`, and `p=P_ee=q⁴/E`. Then:

```text
P V P = lambda (P|e>)(<e|P)       rank one
nonzero in-band eigenvalue = lambda p
||Q V P|| = |lambda| sqrt[p(1-p)]
cut-leakage/in-band-shift = sqrt[(1-p)/p].
```

For W33's `q=3`, the first-order in-band eigenvalue is `(81/160)lambda`, while the band-cut mixing is `(sqrt(81*79)/160)|lambda|`; their ratio is `sqrt(79/81)=0.98758`. The local defect is **not** protected when it creates dynamics.

A quantitative unitary control uses `H=A_X+0.25 V` and `psi=P|e>/sqrt(p)`. For short time `t`,

```text
Prob(cut at t) = 0.25² * (81/160)*(79/160) * t² + higher orders.
```

At `t=0.005,0.01,0.02`, the measured probabilities follow the analytic leading coefficient with relative errors under 0.001. This is finite single-particle quantum-walk dynamics on the **provided** graph, not an experiment.

**3. Exact projection converts a local defect into a dense operator.**

The W33 projected flag vector `P|e>` has nonzero entries on every one of the 160 flag positions, with squared-norm fractions by distance shell

```text
d : 0        1        2        3        4
w : 81/160   54/160   18/160   6/160   1/160.
```

More generally, the normalized radial probabilities are

```text
(q⁴,2q³,2q²,2q,1)/E.
```

Thus `P V P` has nonzero matrix elements between *every* pair of flags. A local microscopic perturbation can induce an explicitly **nonlocal** projected effective operator.

**4. No nonconstant onsite potential preserves the entire protected cycle space.**

For arbitrary diagonal `V=diag(v_e)`:

```text
[V,P]_{ef} = (v_e-v_f) P_{ef}.
```

All `P_{ef}` are nonzero, since `(-q)^{4-d}/E !=0` for every finite q and every possible distance. Hence

```text
[V,P]=0 iff all v_e are equal.
```

This is a strict onsite-potential no-go. It does **not** exclude specially engineered off-diagonal local Hamiltonians that preserve the cycle space; it says those cannot be obtained just by varying onsite flag energies.

**5. Local nearest-neighbor bond perturbation: two split modes and two leakage channels.**

For `q=3`, choose adjacent flags `e,f` and `V=|e><f|+|f><e|`. The radial projector has `P_ee=81/160`, `P_ef=-27/160`. Therefore `PVP` has nonzero eigenvalues

```text
+54/160 and -108/160
```

while `QVP` has nonzero singular values

```text
sqrt[(54/160)(106/160)] ≈ 0.47286
sqrt[(108/160)(52/160)] ≈ 0.46837.
```

This independently demonstrates that nontrivial **strictly one-hop** perturbations are accompanied by cut-sector mixing. The unperturbed line-graph adjacency is still cycle-preserving but flat in the cycle sector.

## Interpretation and next discriminator

The W33 81-cycle space is a mathematically exact and potentially useful **memory/code subspace**, but flatness plus local perturbation leakage means it is not automatically a self-sufficient physical spacetime or a propagating matter/gravity sector.

A viable TOE dynamics must supply more than the abstract Hodge projector: a local microscopic interaction whose *full* spectrum admits a controlled low-energy sector with a derived scale, propagating modes, and quantitative leakage suppression. It could use additional sectors, projective phases, gauge constraints, or interacting many-body dynamics, but those are **new mechanisms to build and falsify**, not results of the current calculation.

## Execution

```powershell
python analysis/2026_11_03_levi_flatband_locality_tradeoff.py
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
python -m pytest -q -o addopts='' tests/test_20261103_levi_flatband_locality_tradeoff.py
```

Outputs: `data/2026_11_03_levi_flatband_locality_tradeoff.json`.

## External work checked

- Leykam, *Flat bands, sharp physics* (2024): https://link.springer.com/article/10.1007/s43673-023-00113-3 . Existing literature on flat-band localization and perturbative fragility.
- Danieli et al., *Flat band fine-tuning and its photonic applications* (2024): https://doi.org/10.1515/nanoph-2024-0135 . Existing tight-binding and photonic flat-band construction/perturbations.
- Song et al., *Observation of compact localized states in synthetic Floquet-Lieb topological photonic lattices* (2025): https://www.nature.com/articles/s42005-025-02138-6 . Distinguishes photonic hardware demonstrations from our abstract Hodge spectrum.

This packet claims **no priority** over known generalized quadrangle geometry, Hodge projection, flat-band graph identities, or Schur's lemma; the useful contribution is an executable, multi-field protection/locality/dynamics decision test tied to the repository's specific substrate claim.
