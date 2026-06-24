# BT1694-BT1696 - Dark Relic, Braiding Boundary, and dS/CFT Time Arrow

This packet promotes the loose dark-sector scripts into a bounded theorem layer.
The important correction is not another numerical match; it is a branch cut.
The tens-of-GeV hidden-SU(4) dark-hadron branch cannot be treated as a
strongly coupled symmetric WIMP relic. It must be read as an asymmetric dark
matter branch if it is kept at the E8-scale confinement mass.

## BT1694 - Asymmetric Relic Ratio

Using the geometric strong-annihilation estimate

```text
<sigma v> ~ pi / m^2
```

and the usual thermal relic cross section, the symmetric relic mass is
approximately 35 TeV. That is over a thousand times heavier than the local
tens-of-GeV hidden-SU(4) branch. The promoted theorem is therefore:

```text
symmetric WIMP-like freeze-out is rejected for this branch
dark matter is a dark baryon/asymmetric relic
```

The exact substrate ratio is

```text
Omega_DM = mu/g = 4/15
Omega_b  = lambda/(v+1) = 2/41
Omega_DM/Omega_b = 82/15 = 5.4666...
```

This matches the observed cosmic-coincidence scale without deriving a detector
cross section. With equal visible and dark asymmetries, the same number is the
dark-proton/proton mass ratio; with a smaller dark asymmetry, it accommodates the
heavier tens-of-GeV hidden hadron.

## BT1695 - D(2T) Is the Protected Braiding Backbone, Not Universality Alone

The exact finite computation is:

```text
2T = SL(2,3), |2T| = 24
conjugacy classes = 7
D(2T) anyons = sum_C k(C_G(c)) = 42
lcm(flux orders) = 12 = k
derived series orders = 24, 8, 2, 1
```

So the dark clock is a real topological clock: the modular T period is the W33
degree. But the same certificate proves the correct boundary. Since 2T is
solvable, the packet refuses to promote "D(2T) braiding alone is universal."
The architecture remains:

```text
finite D(2T) braiding backbone + Hesse/T or Wigner-negative magic = universality
```

This aligns the dark anyon result with the existing contextuality-fuel and
Hesse/T ports instead of competing with them.

## BT1696 - The Time Arrow Is the dS/CFT Boundary Flow

For d = mu = 4, de Sitter boundary weights obey

```text
Delta = (d-1)/2 +/- sqrt((d-1)^2/4 - m^2)
threshold = 9/4
```

The W33 Laplacian masses split as

```text
0^1      -> complementary vacuum mode
10^24    -> principal-series matter/boundary mode
16^15    -> principal-series bulk-isometry mode
```

The finite Heawood thermal clock is mixed, with positive von Neumann entropy.
The promoted interpretation is bounded: the exact theorem is the finite mode
classification plus mixed-clock entropy; the physics reading is the dS/CFT-style
non-unitary boundary flow. In the architecture, time's arrow is no longer an
extra postulate. It is the same expanding holographic boundary that carries the
dark/bulk SU(4) branch.

## Sources and Guardrails

- Kaplan, Luty, and Zurek, "Asymmetric Dark Matter", arXiv:0901.4117.
- Strominger, "The dS/CFT Correspondence", arXiv:hep-th/0106113.
- Mochon, "Anyons from non-solvable finite groups are sufficient for universal
  quantum computation", arXiv:quant-ph/0206128.

These sources are used as guardrails. The verified payload remains the finite
W33 computations in the three scripts and JSON certificates.

## Verification

```bash
python3 analysis/bt1694_dark_asymmetric_relic_ratio.py
python3 analysis/bt1695_dark_anyon_braiding_gate_boundary.py
python3 analysis/bt1696_dscft_time_arrow_modes.py
python3 -m pytest --noconftest -q tests/test_bt1694_bt1696_dark_braiding_dscft_relic.py
```
