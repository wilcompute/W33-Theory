# Pass 12638: the E7 regions are scalene three-qubit triples; one reflection is Kramers, chirality and odd triality; cube channels; certificates

Claude track. All scripts are in `analysis/`, with JSON in `data/`. Continues Passes 12634–12637. Codex coordination proposal: `analysis/HANDOFF_CLAUDE_TO_CHAT_20261106.md` (8234ecb25).

**Not a theory of everything.**

## Item 2: the E7 pezzotopes are scalene triples of three-qubit maximal commuting sets (`w33_e7_facet_test.py`)

**Dictionary** (E7 ↔ three qubits): roots mod 2 ↔ the 63 points of W(5,2), collinear iff the Picard intersection number is even. 7A1 frames ↔ the 135 Lagrangian planes. A7 subsystems ↔ O⁺ forms, with the A7's 28 roots as the non-singular points.

**Test on the explicit E7 region** of Early, Geiger, Panizzut, Sturmfels and Yun (their eqs. (35)–(39); 10 A1, 12 A2, 9 A3×2, 3 A7):
- the planes totally singular for all three A7 facets are **2**, meeting in a line;
- the planes containing 6 of the 10 A1-facet roots are a **unique** one;
- **these three planes have pairwise 0, 1 and 3 common roots (intersection dimensions 0, 1, 2): a scalene triple.**

The construction uses only facet data and the W(5,2) geometry, so it respects W(E7), whose −1 acts trivially mod 2. Regions form one W(E7)-orbit of 60,480, and scalene triples form one Sp(6,2)-orbit of 60,480 with stabiliser exactly S4 (Pass 12637). The equivariant map regions → triples is therefore a bijection.

> **The 60,480 regions of the real moduli space of marked degree-2 del Pezzo surfaces (E7 pezzotopes) are the scalene triples of three-qubit maximal commuting sets** (Lagrangian planes of W(5,2) with pairwise intersections of dimension 0, 1, 2).

The first naive test failed: the planes singular for all three A7's alone are 2, not 3. That failure is recorded. The full triple needs the A1 data as well. **Status:** exact on the explicit region, and transported by equivariance. A region-by-region atlas check is proposed to Codex.

## Item 4 + creative 3: one reflection, four roles (`w33_triality_chirality_element.py`, `w33_reflection_is_kramers.py`)

- **Triality.** For every D4 (45) and root α (36), s_α preserves the D4 iff α ∈ D4 (540/540). It then acts on the three frames as a **transposition fixing α's frame**. Each root lies in exactly 15 D4's.
- **Kramers.** All 36 reflections act on the 40 points of W(3,3) as **fixed-point-free involutions**, each fixing the 10 lines of its root's spread. Pass 12523 showed that the fixed-point-free outer involutions are exactly the 36 Kramers reversals, and reflections lie in the outer coset. **So s_α = θ.**

> **The Weyl reflection s_α in a double-six root is, at once:**
> - **the Kramers reversal θ of that double-six;**
> - **the chirality flip of the pezzotope pairs over its codewords (Pass 12636);**
> - **odd triality (a transposition) on the three entangled MUB classes of the 15 factorisations whose D4 contains α (Pass 12637).**

## Item 3: the cube channels (`w33_cube_channels.py`)

For all 2160 cusp facets (432 × 5):
- the 6 neighbouring roots are 2 from each A2 factor of the cusp's A2³;
- the facet has 8 vertices;
- its 3 opposite pairs are exactly the 3 A2 factors.

**Each cube residue is a product of three two-point amplitudes, one per A2 factor (Steiner trihedral pair) of the context.** Together with Pass 12637 (root facets = 6-point φ³ amplitudes whose particles are the six lines of a six), both kinds of facet residue now have two-qutrit labels.

## Item 1: the strong-unextendibility certificate (`w33_strong_umub_certificate.py`, `w33_strong_umub_sos.py`)

- **Pure-state Pauli-weight identity** Σ_u a_u ω^{[u,v]} = 9·a_v: verified (pure 2×10⁻¹⁵, mixed control 4.8).
- **LP relaxation:** feasible for all 432 pentads, so it **cannot decide**; the identity is necessary but loses phases. Controls are feasible.
- **Zero-forcing on the purity equation:** inconclusive. Every forced zero keeps at least 2 surviving products.
- **SOS/SDP lower bound:** see below.

## Item 5: coordination with Codex

The proposal is in the handoff file. Codex takes the exact certificates (rounding the strong-unextendibility SOS, and the atlas-wide E7 bijection); Claude takes the bridges. Codex's packets are cited, not duplicated.

## Creative 1 + 2: smallest strongly unextendible sets, and the other rungs (`w33_strong_umub_census.py`; numerical)

min F = min over unit v of Σ_e(|⟨e|v⟩|² − 1/d)². A value above 0 means no vector is unbiased to all the bases. All controls (subsets of complete sets) are about 10⁻¹⁸.

| system | weakly unextendible Pauli sets | min F of the smallest |
|---|---|---:|
| two qubits, d = 4 | sizes {5: 6, **3: 20**} | **0.2500** |
| three qubits, d = 8 | sizes {9: 960, **5: 24,192**} | **0.1250** |
| two qutrits, d = 9 | sizes {10: 36, 8: 135, **5: 432**} | **0.1471** (size 8: 0.4444) |

- **No 4-set of disjoint W(3,3) lines is strongly unextendible.** There are 5 PSp(4,3)-orbits of sizes 270, 6480, 540, 1080 and 1080, covering subsets of spreads and of pentads, and every one has min F ≈ 10⁻¹⁸. **The pentads are the smallest strongly unextendible Pauli-class MUB sets in d = 9.**
- On the qubit rungs, the smallest weakly unextendible sets also appear strongly unextendible, with minima of exactly 1/d. The qutrit pentad's 0.14711 is not 1/9, so no closed form is claimed.
- Whether Mandayam et al.'s d = 4 three-sets were already known to be strongly unextendible was not checked.

## Addendum: the certificate is in, plus the rungs, time-reversal channels, and the ladder note

**Item 1 is proved** (`w33_strong_umub_hermitian_sos.py`). F(v) = (v⊗v)† M (v⊗v) is a Hermitian (2,2)-form, and on Sym²(C⁹) its representing operator is unique. The best Hermitian-SOS bound is therefore δ* = λ_min(P_S M P_S).
- **All 432 pentads: δ* = 1/9**, so F(v) ≥ |v|⁴/9 > 0 and **every pentad is strongly unextendible**.
- **All 135 size-8 sets: δ* = 4/9**, equal to their numerical minimum, so the bound is tight.
- Controls (4 spread bases; the pentad's 4-subsets) give −4/9, as they must for extendible sets.
- Rigour: the basis vectors are exact to 2×10⁻¹⁴, giving a crude Weyl margin of 3.9×10⁻⁹. A fully exact version would rebuild H with exact stabiliser states over Q(ω).
- Pass 12637's numerical minimum 0.14711 is consistent with this (≥ 1/9). The general SOS attempt in `w33_strong_umub_sos.py` was stopped as too large; it is superseded.

**Item 3: the rungs** (`w33_sos_rungs.py`). δ*·d is 1 for the two-qubit 3-sets (tight: min F = 1/4, so **proved strongly unextendible**) and 1 for the two-qutrit pentads (not tight). For the three-qubit 5-sets δ* = −5/8: the Hermitian relaxation fails, and their strong unextendibility (numerical min 1/8) needs a higher-degree certificate.

**Item 2: E8.** No region count for the real moduli of degree-1 del Pezzo surfaces exists in the literature found, so no test is possible. A method is suggested: sign patterns over W(E8) chambers, as the other track did for E6.

**Item 4: time reversal on the channels** (`w33_kramers_channels.py`, all 216 codewords).
- The left and right pezzotopes over a codeword share no facets.
- Their 30 channels are the codeword's 10 contexts plus **exactly the 20 roots not orthogonal to α**, i.e. the roots θ = s_α moves.
- θ maps the left channels onto the right ones.
- The θ-fixed roots (α and its orthogonal A5, 16 in all) are never channels.
- The canonical-form ratio of a chiral pair is the other track's (3dd4b78cb).

**Item 5: the ladder note** is `analysis/NOTE_POSITIVE_GEOMETRY_QUDIT_LADDER.md`. Prior art for the E7 root ↔ three-qubit dictionary: Cerchiai and van Geemen (arXiv:1003.4255) and Lévay–Saniga–Vrana. The region-level statement is this pass's.
