# Passes 4648–4655 executed outcomes

Canonical collision-free continuation after Passes 4640–4647. All eight fronts are materialized on `master` with frozen certificates, focused regression, an exact-evidence workflow, a shared theorem insert in all three maintained manuscripts, and registered public card/page surfaces.

## 4648 — the 72-dimensional dark sheet sector is a tensor module
For the canonically aligned three spread sheets, the cubic-line coupling is `[R R R]`. Its 72-dimensional sheet-difference kernel is exactly

`Std_2(S3_sheet) tensor Q[36_spreads]`.

Since the 36-spread permutation module restricts to PSp as `1+20+15`, the dark sector restricts as `2*(1+20+15)`. Adding the bright 15-dimensional kernel of `R` gives the full 87-dimensional kernel

`1^2 + 20^2 + 15^3`.

The sheet S3 character on that full kernel is `(87,15,-21)` on identity / transposition / 3-cycle. On the dark sector the C3 cycle has minimal polynomial `x^2+x+1`, splitting over C as `36_omega + 36_omega^2`.

## 4649 — full D4 triality closure, and W33 reconstructs itself from conjugate-subgroup intersections
The explicit split-octonion triality on the W33-derived plus-type V8 was lifted to the complete 405-object D4 outer building. Two triality-conjugate embedded PSp(4,3) copies already generate the type-preserving group of order

`174182400 = |Omega_8^+(2)|`.

Adjoining order-three triality gives order `522547200 = |Omega_8^+(2):3|`; adjoining split-octonion conjugation gives

`1045094400 = |Omega_8^+(2):S3|`,

with `sigma tau sigma=tau^-1`.

Pairwise triality-conjugate PSp copies intersect in order 216; all three intersect in a nonabelian order-6 S3. The order-216 pairwise intersection fixes pointwise exactly three nonsingular vectors forming one anisotropic F2 two-plane. Its PSp orbit has 40 planes, which are pairwise disjoint on nonzero vectors and partition all 120 nonsingular vectors as `40 x 3`. Two planes have either 3 or 9 polar-orthogonal cross-pairs; total cross-orthogonality yields exactly `SRG(40,12,2,4)`.

Pass4654 below identifies this 40-plane geometry action-theoretically with W33 points.

## 4650 — the apartment six-sheet cover globally factors as C2 then S3
For `G=PSp(4,3)`, let C be the core of an apartment stabilizer K in its selected-line stabilizer H. The subgroup orders are

`|C|=8 < |K|=16 < |N_H(K)|=32 < |H|=96`.

Since `H/C=D12`, `K/C` is a reflection, and its normalizer in D12 is V4. Therefore

`1620 apartments -> 810 selected point-line flags -> 270 selected lines`

factors as a regular 2:1 cover with global deck group C2 followed by a nonregular 3:1 map with monodromy S3. The composite local monodromy is D12. The central half-turn is therefore an honest global deck involution swapping the two apartment lifts over every selected point-line flag. A nonzero H1 class is deliberately not asserted until a specific connected flag graph/complex is chosen.

## 4651 — a new [135,16,30] code whose minimum shell is the W33 spread carrier
For the selected `135_6–270_3` incidence matrix N, the binary left relation code is exactly

`ker_F2(N^T) = [135,16,30]_2`.

The complete 65,536-word enumerator has exactly 36 minimum words of weight 30. Every pair of minimum supports meets in 6 coordinates, every one of the 135 coordinates lies in 8 minimum words, and a minimum-word stabilizer has order 720 and fixes exactly one W33 spread. Hence the 36 minimum words are explicitly the W33 spread G-set.

The selected point and line critical-group orders are

`2^150 * 3^166 * 5^23`

and

`2^284 * 3^436 * 5^23`,

with `(2,3,5)` p-ranks `(62,74,23)` and `(164,164,23)`. A full reduced-Laplacian Smith form is not claimed.

## 4652 — weighted Holonet routing is Pareto, not scalar
For a common per-hop power-transmission factor `0<eta<1`, the exact shell polynomials prove the strict mean destination-delivery hierarchy

`W33 > selected135 > selected270 > Levi160`.

Conversely, selected270 has strictly larger aggregate delivered-destination score than each of the other three for every `0<eta<=1`. Thus W33 is the compact loss/latency optimum per destination, while the 270-router is the aggregate-address-throughput/connectivity extreme. Component-loss examples in the verifier mix published platforms deliberately and are sensitivity anchors only, not a demonstrated integrated Holonet stack.

## 4653 — characteristic three destroys the semisimple bright/dark sheet Fourier split
Away from characteristic three, the three-sheet permutation module splits canonically into the bright trivial line and the dark sum-zero plane using `J/3` and `I-J/3`. In characteristic three, `(1,1,1)` itself lies in the sum-zero plane, `J^2=0`, and the S3 module has nonsplit filtration

`trivial | sign | trivial`.

Thus `[R R R]` still factors through the trivial quotient by the sum-zero plane, but there is no S3-equivariant bright section. This is a modular representation obstruction, not a generation/phase claim.

## 4654 — the 40 triality-intersection planes are W33 points, not W33 lines
The base anisotropic plane from Pass4649 has setwise stabilizer order 648 and pointwise stabilizer order 216. In the original W33 action that order-648 stabilizer fixes exactly one W33 point and no W33 line. Consequently `gP0 -> gp0` is a well-defined PSp-equivariant 40-to-40 bijection. Under it, total polar orthogonality between anisotropic planes is exactly W33 point collinearity.

This explicitly preserves the odd-q point/line inequivalence instead of identifying two 40-count carriers.

## 4655 — the selected geometry internally reconstructs the Schlaefli/double-six incidence
This outside-box front pivoted after a stronger internal relation appeared. Compare the 27 degree-27 maximal singular generators with the 36 minimum supports of the new `[135,16,30]` code. Removing zero, each generator has 15 singular points and each codeword support has 30. Every intersection has size 0 or 6, with exact census

`0^432, 6^540`.

Declare incidence when the intersection is zero. The resulting 27x36 matrix has row degree 16, column degree 12, rational rank 21, and obeys

`RR^T = 10 I27 + 2 A27 + 6 J27`,

`R^T R = 6 I36 - 2 A36 + 6 J36`,

`3 A27 R + R A36 = 20 J`.

It reconstructs `SRG(27,10,1,5)` and `SRG(36,15,6,6)` exactly. Combined with the action-level identifications of Pass4640 and Pass4651, this is the Schlaefli-line/double-six carrier reconstructed from the selected geometry's own maximal singular objects and binary code, without importing the classical labels.

## Integration and evidence
- Executable witnesses: `analysis/w33_pass4648_dark_sheet_module.py` through `analysis/w33_pass4655_internal_schlafli_from_selected_code.py`.
- Frozen certificates: `data/PART_W33_PASS4648_*` through `data/PART_W33_PASS4655_*`.
- Regression: `tests/test_w33_pass4648_4655_dark_triality_code_routing.py`.
- Focused workflow: `.github/workflows/w33_pass4648_4655_dark_triality_code_routing.yml`.
- Shared manuscript theorem: `analysis/PASS4648_4655_dark_triality_code_routing_insert.tex`, inserted in `w33_paper.tex`, `photonic_holonet.tex`, and `holonet_machine_blueprint.tex`.
- Public card/page: `analysis/PASS4648_4655_dark_triality_code_routing_index_insert.html` and `docs/triality-self-reconstruction-code-routing.html`, registered in the public frontier manifest.
- `docs/index.html` was not rewritten directly because the GitHub connector truncates that giant file; publication uses the established registered-card route.

Evidence discipline: all promoted statements are finite group, incidence, module, coding, critical-group, cover, or symbolic routing statements. No particle, generation, gauge-field, optical-phase, or measured hardware-performance identification follows from them alone.
