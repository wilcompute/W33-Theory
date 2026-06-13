# BT882 — The Gauge Connection: Flat Along Edges, Curved on the Matter Graph

**Status: PROVEN (machine-verified, `analysis/bt882_gauge_connection_flat_on_edges.py`, data `data/bt882_gauge_connection.json`)**

The dynamics frontier of the gauge arc. BT881 made the 40 points the space of
local gauge groups, each centered on a generation Z₃ = ⟨R_p⟩. The gauge
connection — how adjacent local frames relate — is the holonomy subgroup
⟨R_p, R_{p'}⟩, and it has a clean dichotomy.

## The theorems

- **T1:** for **collinear** (adjacent) points p, p' — the 12 = k edge-partners
  — the generation transvections commute (symp(p,p')=0), so
  **⟨R_p, R_{p'}⟩ = Z₃ × Z₃** (order 9, abelian). The gauge connection is
  **flat along the 240 W(3,3) edges**.
- **T2:** for **non-collinear** points — the 27 = q^q non-edge partners (the
  matter shell) — **⟨R_p, R_{p'}⟩ = SL(2,3) = 2T** (order 24, profile
  {1:1, 2:1, 3:8, 4:6, 6:8}, the binary tetrahedral / 24-cell group). The
  connection is **curved across non-edges**, with holonomy 2T.
- **T3:** the gauge **curvature lives exactly on the matter graph Q** (the
  non-collinearity graph, BT870's dual-gravity graph): flat gauge directions
  = the 240 collinear edges, curved (2T-holonomy) directions = the
  27-per-point matter shell.

## Reading

The gauge connection on the substrate's 40-local-gauge-group bundle is **flat
along collinearity and curved along non-collinearity**:

- collinear (same line, the gauge/causal directions) → commuting generation
  symmetries → zero curvature (echoing BT741's flat F₂⁴ register and the
  flat-bundle theme);
- non-collinear (the matter shell) → holonomy 2T = the binary tetrahedral
  group = the 24-cell symmetry → curvature.

So **curvature = non-collinearity = matter**, and the curved sector is exactly
Q, the graph whose spanning-tree gravity (BT873, τ(Q) = 2⁶⁶·3³⁹·5²³) carries
the gauge dimension. The gauge holonomy being 2T (the 24-cell / binary
tetrahedral group, the project's recurring polar-pair group, BT810/869) ties
the curvature to the same 24-cell that appears as the polar-pair stabilizer
and the chirality involution's centralizer. Gauge flatness, causal
collinearity, and the matter sector are one trichotomy; the curvature is the
24-cell.

## The closed arc (BT858–882)

- **kinematics:** spacetime = 40 local gauge groups (BT881), each
  SU(3)×SU(2)×U(1) centered on generations (BT876/880);
- **matter:** Steinberg register, 3 generations, flavor S₃, Yukawa texture,
  chirality/parity/C (BT861–879);
- **gravity:** spanning-tree / Ihara-zeta partition functions (BT870/872/873);
- **dynamics (now):** the gauge connection — flat on edges, 2T-curved on the
  matter graph (BT882).

## Open

- The full holonomy around a triangle/apartment (composing edge-flat and
  non-edge-curved transports): the substrate's curvature 2-form.
- 2T holonomy on the 27 matter shell vs the 600-cell/icosahedral structure
  of BT808 — is the gauge curvature the same 2T that sits in the spread
  stabilizers?
