# TOE86 — All five TOE85 continuations: orbit-pair census, equivariant maps, temporal null, integral homology, physical gate routing

**15 October 2026.** Exact and synthetic computations performed on a clean worktree from current W33-Theory `master`. All five fronts are executable, independently testable certificates. TOE83 (H27-invariant Schläfli CSS code) and TOE85 (16D H2 relation module) are inputs. These results **do not demonstrate** a Theory of Everything, physical temporal ordering, emergent spacetime, a device demonstration, or fault tolerance.

## Front I — Classify all 468 admissible H27 square-orbit pairs

Reconstruct the 27 Heisenberg addresses, 45 tritangent triangles, 135 oriented edges and 1080 squares. The squares split into 40 H27 orbits of 27. Exactly 468 of the 780 two-orbit choices eliminate all 135 binary weight-two X supports (TOE83 condition).

Enumerate all 432 candidate automorphisms of H27 from independent noncentral generator images; precisely **48** preserve the five selected cyclic tritangent directions. This extends the regular 27-element H27 action to an explicitly verified group of order **27 x 48 = 1296** (point stabilizer 48). This is the *subgroup-direction-preserving normalizer considered here*, not a claim that this is the entire Schläfli/W(E6) automorphism group. Its action on all 40 orbit labels and all 468 admissible pairs is exact. The pairs form **13 orbits/classes**.

| Admissible pairs | face rank F2 | binary logical k | face rank F3 | ternary logical k |
|---:|---:|---:|---:|---:|
| 36 | 83 | 26 | 83 | 26 |
| 72 | 95 | 14 | 95 | 14 |
| 360 | 97 | 12 | 95 | 14 |

Each of the 13 class representatives was independently reconstructed over F3, and the center plus one element from **each** of the four projective Pauli directions was evaluated on both H1 and H2. In all 13 classes, H1 and H2 select the same **unique** noncentral direction by minimal rank(g-I). This extends to all 468 pairs by the verified automorphism transport. The actual choice of direction changes under pair selection / transport and is **not an absolute time direction**.

- For rank-83 pairs: H1 ternary four-direction ranks are a permutation of `[16,17,17,17]`, H2 `[8,10,10,10]`.
- For rank-97 rational pairs: H1 ternary ranks `[8,9,9,9]`, H2 `[1,2,2,2]`.
- This joint selection survives a substantial change in homology dimension and integral torsion structure.

## Front II — Rigorous equivariant maps H2 -> H1

Build H1(F3) as the quotient of 109 independently oriented fundamental graph cycles by 83 face boundaries. Construct exact 26x26 actions of all 27 H27 elements and verify all 729 group multiplication identities. Build the 16x16 H2(F3) action on the integral face-relation kernel (as in TOE85).

The intertwiner `T:H2 -> H1` satisfies `rho_H1(x) T = T rho_H2(x)` and similarly for the independent noncentral generator y. This gives exactly **832 equations in 416 unknowns**, with **rank 396** over F3, hence

```
dim_F3 Hom_{H27}(H2(F3), H1(F3)) = 416 - 396 = 20.
```

One explicit nonzero intertwiner with nine nonzero basis coefficients is frozen, and its commutation with **all 27** H27 elements is verified. This proves existence of equivariant maps, not an intrinsically selected or geometrically local connecting map: the chain boundary `d2` itself vanishes on H2 by definition. Choosing a map within a 20-dimensional Hom space requires an additional condition or physical principle.

## Front III — Falsifiable quantum qutrit time-transfer null

Fix a qutrit clock eigenbasis of the `A={(0,b,c)}` commuting Heisenberg subgroup. Build a trusted two-time CPTP channel with visibility `v`:

```
E_v(rho) = v rho + (1-v) sum_{j=0}^2 P_j rho P_j
```

where the P_j are the rank-one clock-basis projectors. The `v=0` case is an entanglement-breaking, measure-and-reprepare null; `v>0` retains coherence. Both preserve every clock eigenbasis input and have identical classical transitions on those tests. Their distinction requires a coherence probe or normalized Choi tomography.

For an equal superposition of clock eigenstates, the return probability is `p(v)=(1+2v)/3`; normalized Choi partial-transpose negativity is **v**, computed from its eigenvalues. At `v=0.25`, predictions are `p=0.5`, `negativity=0.25`; the null has `p=1/3`, `negativity=0`.

Pre-registered synthetic 256-shot Bernoulli test, accept alternative for >=110 returns: exact false-positive probability `0.0008211891321355085` and alternative power `0.9897152744791732`. An electronics-sham null predicts 1/3. This rules out the **specific** measure/reprepare model under trusted preparation and measurement assumptions if the stipulated results occur. It does **not** prove non-Markovianity, device-independent temporal entanglement, indefinite causal ordering, or an arrow of time.

## Front IV — Integral Smith forms and homology torsion

Compute the full **exact integer** Smith normal form of the 135x99 oriented face-boundary matrix for all 13 orbit representatives, not a floating-point matrix rank. Over Z, `im d1` is free, so torsion in `coker d2` is exactly torsion in H1. Results:

| Pairs | rank_Z(d2) | nonunit invariant factors | H1(Z) | H2(Z) |
|---:|---:|---|---|---|
| 36 | 83 | none | Z^26 | Z^16 |
| 360 | 97 | [3,3] | Z^12 + (Z/3)^2 | Z^2 |
| 72 | 97 | [6,6] | Z^12 + (Z/6)^2 | Z^2 |

The Smith factors explain the characteristic-dependent dimensions (a pair of 3-torsion factors lowers rank by two mod3; factors 6 lower rank by two both mod2 and mod3). The TOE83 selected orbit pair remains torsion-free, confirming TOE85's modular representation difference there is **not caused by homological torsion**.

## Front V — Exact signed physical Clifford permutations

For Heisenberg generator x=(1,0,0), y=(0,1,0), and center z=(0,0,1), compile the signed permutation of the **135 edge qutrits** from oriented chain geometry. Local `j -> -j` basis inversion is a qutrit Clifford gate; edge permutations decompose into SWAPs.

Each generator consists of 45 disjoint 3-cycles, so the all-to-all SWAP lower bound `135 - 45 = 90` is attained. For a fixed 135-wire *linear nearest-neighbor* hardware layout, generate and verify an explicit odd-even transposition routing schedule; its adjacent SWAP count equals the exact inversion count, which is optimal for this wire order. The reported layer counts are valid schedules, not certified minimum depth.

| Generator | unrestricted SWAPs (optimal) | adjacent SWAPs (optimal on fixed line) | odd-even layers | orientation inversions |
|---|---:|---:|---:|---:|
| x | 90 | 4,740 | 120 | 54 |
| y | 90 | 1,828 | 65 | 30 |
| z | 90 | 498 | 24 | 18 |

Verify every complete signed permutation has order three and induces a permutation of all 99 face checks, consistent with TOE85. This is a theoretical circuit compiler for ideal qudit wires, **not** a physical implementation, FT threshold, detector/readout protocol, or optics layout. Local qutrit inversions do not automatically guarantee fault tolerance.

## Source files and verification

- `analysis/w33_20261015_toe86_geometry_integral_routing.py` — exact normalizer, pair census, selected integral SNF, physical routing
- `analysis/w33_20261015_toe86_pair_polarization.py` — independent F3 H1/H2 rank selection for all 13 symmetry classes
- `analysis/w33_20261015_toe86_pair_integral.py` — exact integral Smith form for all 13 classes
- `analysis/w33_20261015_toe86_hom_intertwiners.py` — all-729-equivariant 20D Hom computation and frozen witness
- `analysis/w33_20261015_toe86_qutrit_temporal_null.py` — validated CPTP null/alternative and binomial test
- `data/w33_20261015_toe86_*.json` — exact integer certificates plus floating-point synthetic quantum witness
- `tests/test_w33_20261015_toe86_all_five_fronts.py` and CI workflow

Reproduce with:

```bash
python -m analysis.w33_20261015_toe86_geometry_integral_routing
python -m analysis.w33_20261015_toe86_hom_intertwiners
python -m analysis.w33_20261015_toe86_pair_polarization
python -m analysis.w33_20261015_toe86_pair_integral
python -m analysis.w33_20261015_toe86_qutrit_temporal_null
python -m pytest -q tests/test_w33_20261015_toe86_all_five_fronts.py
```

## Five independent next experiments

1. Derive a conceptual theorem forcing the joint H1/H2 rank-selector agreement from group-ring exact sequences, or exhibit an admissible three-orbit counterexample.
2. Classify all 13 orbit-pair symmetry classes as modular modules (Loewy layers, extension quivers, characteristic-2 simple multiplicities), not just by Hom rank.
3. Build fault-aware syndrome-extraction and correlated-error simulation on a physically specified qudit coupling graph; establish meaningful circuit-level noise thresholds or no-go bounds.
4. Test the qutrit temporal witness under SPAM error, drift, loss, leakage and adversarial measure/reprepare controls, with preregistered confidence intervals and no unwarranted time-arrow inference.
5. Examine whether the `Z/3` versus `Z/6` torsion dichotomy has a natural geometric realization via cubic-surface incidence, E6 Weyl subgroups or nontrivial integral local-system holonomy.
