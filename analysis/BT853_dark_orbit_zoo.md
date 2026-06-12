# BT853 — The Dark Orbit Zoo, Complete

**Status: PROVEN (machine-verified, `analysis/bt853_dark_orbit_zoo.py`, data `data/bt853_dark_orbit_zoo.json`)**

BT847 left four of the six A₅-orbits on the pentad core's 190 dark-line pairs
unidentified. All six are now named:

| orbit | graph on the 20 dark lines | line geometry | identity |
| --- | --- | --- | --- |
| 10 | perfect matching (10 × K₂) | all **skew** | **10 dark charts** — a canonical chart-pairing of the dark lines |
| 30 | **5 × K₄** | all skew | partition into **5 skew tetrads** (4-line partial spreads) |
| 30 | **5 × K₄** | all skew | the **chiral twin** partition |
| 30 | connected, 3-regular, girth 5 | all skew | **dodecahedron** (BT847) |
| 30 | connected, 3-regular, girth 5 | all skew | chiral twin dodecahedron (BT847) |
| 60 | connected, 6-regular | all **meeting** (1 point) | the dark intersection graph |

Checks: skew pairs 10+30+30+30+30 = 130, meeting pairs 60, total 190 = C(20,2) ✓.

## Reading

The dark sector is now fully structured hardware:

- a canonical **matching into 10 charts** (routing glue made entirely of dark
  lines — the lit sector's chart double cover (BT845) has a dark twin);
- **two chiral partitions into five skew tetrads** — the dark analogue of the
  lit pentads (5 disjoint lines) is 5 *tetrads* of 4 disjoint lines, echoing
  the residual tetrahedral carriers of BT798–801 (transversal K₄s);
- the **chiral dodecahedron pair** (BT847);
- one 6-regular intersection frame (the only orbit where dark lines meet).

Every A₅-orbit of the dark sector is now a named machine component: charts,
tetrad pentads (×2, chiral), dodecahedra (×2, chiral), and the meeting frame.

## Open

- The 5 tetrads of one partition vs the 5 charts of the core's deleted
  matching (BT845): is there a canonical bijection (tetrad ↔ chart)?
- Do the 10 dark charts of the matching orbit land in the BT845 double
  cover's fiber over this core?
