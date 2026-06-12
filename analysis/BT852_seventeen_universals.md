# BT852 — The Seventeen Universals vs the Substrate: Aut(Tomotope) Is a Universal Polytope Group

**Status: PROVEN (GAP + python, `analysis/bt852_seventeen_universals.py`, GAP witness `.tmp/gap_bt852_universal_groups.g`, classification source Hartley math/0310429 full text)**

Hartley's complete classification of rank-4 locally projective polytopes
(17 universal, 9 nondegenerate, 441 quotients) is now read case-by-case
against the substrate. Three discoveries.

## The classification, condensed (nondegenerate cases)

| type | universal | group | order | notes |
| --- | --- | --- | --- | --- |
| {3,5,3} | {{3,5}₅,{5,3}₅} = **11-cell** | L₂(11) | 660 | no proper quotients |
| {3,5,3} | mixed (icosa + hemi-dodeca) | — | — | **DOES NOT EXIST**: the construction closes into the 11-cell |
| {5,3,5} | {{5,3}₅,{3,5}₅} = **57-cell** | L₂(19) | 3420 | no proper quotients |
| {5,3,5} | {{5,3},{3,5}₅} mixed (+ dual) | **J₁ × L₂(19)** | 600415200 | 145 quotients, incl. a J₁ polytope |
| {4,3,4} | {{4,3},{3,4}₃} (+ dual) | 2³⋊S₄ | **192** | 4 quotients (cube-quotient pattern) |
| {4,3,4} | {{4,3}₃,{3,4}₃} | ((2⁴):C3):C2 | **96** | **no proper quotients** |
| {4,3,5} | {{4,3},{3,5}₅} = 2^I (+ dual) | 2⁶⋊A₅ | 3840 | 80 cubes, 64 vertices, 70 quotients |

## T1 — The tomotope's group IS a universal polytope group

GAP: **Aut(tomotope) ≅ Γ({{4,3}₃, {3,4}₃})** — the group of the *only
doubly-projective* {4,3,4} universal (hemicube facets, hemioctahedron =
hemicross vertex figures), which like the 11-cell and 57-cell has **no
proper quotients**. Identical order profiles {1:1, 2:27, 3:32, 4:36} (=
Pillar 70's P group; structure ((2⁴):C₃):C₂, consistent with Pillar 87's
Z₂⁴ 2-core and S₃ quotient). Moreover the case-10 group is exactly
**C₂ × Aut(tomotope), order 192 = the tomotope's flag count** — Pillar 70's
"numerological" 192 now has a structural reading: it is the order of the
{{4,3},{3,4}₃} universal group, whose central Z₂ kills into the tomotope's
symmetry.

The resonance is sharp: the tomotope's projective cells are hemioctahedra =
hemicrosses, and its symmetry group is the group of the universal polytope
built entirely from hemicubes and hemicrosses. The middleware is symmetry-
twinned with the projective member of the {4,3,4} family.

## T2 — Icosahedral mixing is forbidden; dodecahedral mixing is sporadic

The classification's strangest asymmetry, now in the corpus: a polytope with
icosahedral facets and hemi-dodecahedral vertex figures **does not exist**
(gluing hemi-icosahedra three per edge under dodecahedral closure *is* the
11-cell), while the dodecahedral mix exists and is enormous (J₁ × L₂(19)).
On the substrate side this matches the compass chirality data: the
hemi-icosahedral side (K₆, hidden 6-set) is rigid, the hemi-dodecahedral
side (Petersen, faces) comes in chiral pairs with room to mix.

## T3 — The chart-compass universal: 2^I

Case 13, {{4,3},{3,5}₅} = McMullen–Schulte's 2^I twisting over the
hemi-icosahedron: **cube facets** (the holonet's Q₃ charts!) and
**hemi-icosahedral vertex figures** (the compass cells!), with vertex set
**F₂⁶ = the F₂ register space on the hemi-icosahedron's 6 vertices** — the
substrate's hidden 6-set. The universal completion of (chart, compass)
local data has group 2⁶⋊A₅, order 3840; both 3840 and its index-2 quotient
1920 fail Lagrange against 25920. The chart-compass amalgam is blocked from
Sp(4,3) exactly like the GC ladder — one more confirmation that the
substrate keeps universal local data while refusing every universal
completion.

## Open

- The 80 = 2×40 cube facets of 2^I: is there a natural 2:1 map from its
  facets to the substrate's 40 points / 40 lines (the duality double
  cover)?
- Case-10's 4 quotients mirror the cube's 4 quotients (cube, digonal prism,
  hemicube, {2,3}); locate the tomotope's cover architecture (BT831) along
  this quotient pattern.
- The J₁ polytope of type {{5,3},{3,5}₅} (one of the 145 quotients):
  Livingstone-graph shadow, 266 = 2·7·19.
