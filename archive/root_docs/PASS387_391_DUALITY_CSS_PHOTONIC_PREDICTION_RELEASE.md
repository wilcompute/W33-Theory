# Passes 387–391: duality, matrix release, CI, photonic dry run, and prediction discipline

## Scope reconstructed from the July 17 master history

This packet was built against the eight commits from July 17, 2026, not against
the stale Pass 102–106 package.

The live sequence is:

- Pass 368: Eisenstein rank-parity law and the \(E_6/2E_6\) 27.
- Pass 369: the 27 is a regular Heisenberg torsor; \(K_{12}\) built from the hexacode.
- Pass 370: the W33 and \(E_6\) 27s are one torsor; the abelian option is refuted.
- Pass 371: naturality closes at the one-qutrit Clifford group.
- Pass 372: the 27-match is quantum but not geometric; the rim is not a torsor.
- Passes 373–380: the triangle-boundary MLUT, four phase sheets, the \(D_8\)
  phase-compatible normalizer, and the minimal external phase lift.
- Passes 381–385: explicit reviewed header binding, a reversible 48-state
  logic-switch controller, the \(C_6\) versus \(S_3\) control boundary, and
  coordinate-fold/stress-orbit obstructions.
- Pass 386: the geometric gap between the two 27-geometries is exactly the
  central qutrit phase fibre; the bulk is distance-regular and the odd-\(q\)
  rim obstruction globalizes.

The common lesson of those commits is that a recurring equality of cardinalities
does not supply a canonical type swap, phase section, or physical identification.
Passes 387–391 turn that lesson into explicit finite certificates and release
policy.

## Pass 387 — the canonical W/Q map is a duality, not an isomorphism

The script enumerates both generalized quadrangles from first principles.

For a totally isotropic W33 line \(L=\langle u,v\rangle\), let
\(p_{ij}=u_i v_j-u_j v_i\). Symplectic isotropy gives \(p_{13}=-p_{02}\).
The Klein relation therefore reduces to

\[
p_{01}p_{23}+p_{02}^{2}+p_{03}p_{12}=0,
\]

the parabolic quadric \(Q(4,3)\) in five projective coordinates. Thus

\[
L\longmapsto[p_{01},p_{02},p_{03},p_{12},p_{23}]
\]

is a bijection from the 40 W33 lines to the 40 \(Q(4,3)\) points. Each W33
point is sent to the four images of its incident lines, and those four images
form one \(Q(4,3)\) line. All \(40\times40\) incidences are checked with the
direction reversed.

The certificate then computes an exact type-preserving obstruction:

\[
\alpha(\text{W33 point graph})=7,\qquad
\alpha(\text{\(Q(4,3)\) point graph})=10.
\]

So the models are canonically incidence anti-isomorphic, while no point-to-point,
line-to-line incidence isomorphism exists. This is the explicit Plücker
realization missing from the earlier duality-defect result.

Artifacts:

- `analysis/w33_pass387_pluecker_duality_certificate.py`
- `data/w33_pass387_pluecker_duality_certificate.json`

## Pass 388 — actual GF(3) stabilizer matrices, released and hashed

The canonical edge-chain code is emitted as literal Matrix Market files:

\[
H_X=d_1\in\mathbb F_3^{40\times240},\qquad
H_Z=d_2^T\in\mathbb F_3^{160\times240}.
\]

Both have 480 nonzero entries. The release verifier checks

\[
H_XH_Z^T=0,\qquad
\operatorname{rank} H_X=39,\qquad
\operatorname{rank} H_Z=120,
\]

and therefore

\[
k=240-39-120=81.
\]

The distance proof is also release-locked:

- no support-one or support-two X cocycle exists; the weight-three star witness
  is a cocycle outside \(\operatorname{row}(H_X)\), so \(d_X=3\);
- every graph triangle is one of the 160 2-faces, excluding non-boundary
  Z logicals below weight four; the committed 4-cycle is a non-boundary cycle,
  so \(d_Z=4\).

The result is exactly

\[
[[240,81,3]]_3,\qquad d_X=3,\ d_Z=4.
\]

Committed matrix hashes:

- \(H_X\): `b5d3becc40fca552be6427976e73275a3f71b2914741edaddf13ead792ec034d`
- \(H_Z\): `ee43d7dfbdfdb27f5d060c180a6a66e0afc8c73b20cfaa3bb48eb6e73ca0972e`

Artifacts:

- `analysis/w33_pass388_css_matrix_release.py`
- `matrices/w33_HX_40x240_GF3.mtx`
- `matrices/w33_HZ_160x240_GF3.mtx`
- `data/w33_pass388_css_matrix_release.json`

## Pass 389 — GitHub Actions release gate

`.github/workflows/pass387-391-release.yml` regenerates every deterministic
artifact and fails on drift. It then runs the focused regression suite and the
live paper claims-ledger checker.

The gate covers:

1. Plücker duality and the \(7\) versus \(10\) obstruction.
2. Matrix content, ranks, commutation, distances, and hashes.
3. The blinded Choi-visibility dry-run bundle.
4. Prediction-registry schema and contamination rules.
5. Current paper-ledger integrity.

## Pass 390 — blinded Choi protocol executed as a synthetic dry run

No laboratory raw counts are present in the repository, so a physical experiment
cannot honestly be claimed. Instead, the complete preregistered pipeline was
executed on deterministic synthetic counts with gate labels hidden until after
analysis.

The frozen ideal targets are

\[
V(I)=1,\qquad V(X)=V(Z)=0,\qquad V(F_3)=\frac13.
\]

The dry run uses four phase settings, 8 independent replicates per gate,
3,000 shots per phase, a separately stored blind key, and declared mode-overlap
and dark-count dilution. The corrected estimates were

\[
\begin{array}{c|c|c}
\text{gate}&\widehat V&95\%\ \text{interval}\\\hline
I&0.99667&[0.99252,1.00082]\\
X&-0.00004&[-0.00963,0.00954]\\
Z&-0.00027&[-0.00886,0.00833]\\
F_3&0.33495&[0.32297,0.34694].
\end{array}
\]

All preregistered dry-run tolerances pass. The result file explicitly records

```text
physical_experiment_completed = false
study_type = synthetic_dry_run_not_physical_data
```

so these counts validate the analysis machinery only. A real test must freeze
this code and replace only the timestamped raw-count, blind-key, and calibration
exports.

Artifacts:

- `analysis/w33_pass390_blinded_choi_visibility_dry_run.py`
- `data/w33_pass390_choi_visibility_raw_counts.json`
- `data/w33_pass390_choi_visibility_blind_key.json`
- `data/w33_pass390_choi_visibility_results.json`

## Pass 391 — out-of-sample physics registry

The registry gives every physics formula a prospective eligibility status,
fixed data freeze, uncertainty propagation, explicit null family, multiplicity
rule, and no-tuning policy.

Its most important result is negative but necessary: most existing numerical
matches are retrospective and cannot receive out-of-sample credit.

- The static \(\alpha^{-1}(0)\) match is marked ineligible because the target
  was known during formula selection.
- \(3/8\) for the weak angle is a conditional unification benchmark, not a
  unique discriminator unless scale and thresholds are frozen.
- \(3/13\), the CKM/PMNS formulas, and mass relations are retrospective until
  evaluated against a named future holdout release with the complete searched
  formula family counted.
- The Choi-visibility vector is the only currently clean prospective entry,
  and remains `preregistered_not_physically_run`.

Artifacts:

- `analysis/w33_pass391_prediction_registry.py`
- `data/w33_prediction_registry_v1.json`

## New architectural synthesis

The July 17 work and this packet now expose the same boundary at four levels.

1. **Geometry:** W33 and \(Q(4,3)\) have a canonical role-reversing Plücker
   duality, but the \(7/10\) invariant blocks an internal type swap.
2. **Quantum code:** the protected 81 is homology of a typed chain complex,
   not a free-standing 81-dimensional classical carrier.
3. **Control:** phase and sequence clocks coexist, but the header binding remains
   reviewed external ABI data rather than a consequence of finite geometry.
4. **Physics:** a numerical match is not a prediction until its section,
   calibration, null family, and data freeze are supplied externally and
   prospectively.

That is a stronger unification than another numerical coincidence: the missing
ingredient is consistently a **section of a typed finite bundle**, and the
repository now has executable guards preventing that section from being
silently promoted to geometry or physics.
