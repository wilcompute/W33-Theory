# Projective class vs W33 phase alignment

Inputs:
- `data/_workbench/02_geometry/W33_line_phase_map.csv`
- `data/_toe/coupling_20260110/W33_lines_to_projective_quartets.csv`

Outputs:
- `data/_workbench/02_geometry/projective_class_phase_alignment.csv`
- `data/_workbench/02_geometry/projective_sector_phase_alignment.csv`
- `data/_workbench/02_geometry/projective_m_phase_alignment.csv`

Global phase distribution:
- k mod 6 counts: {"0": 196, "1": 60, "2": 36, "3": 60, "4": 36, "5": 60}
- k mod 3 counts: {"0": 256, "1": 96, "2": 96}

Most phase-biased projective classes (by k mod 6 KL to global):
- sec1_m1: k6_dom=0 (frac=0.4324), kl=0.025899, entropy=2.2556
- sec3_m0: k6_dom=0 (frac=0.4324), kl=0.025899, entropy=2.2556
- sec0_m1: k6_dom=0 (frac=0.4122), kl=0.015336, entropy=2.3157
- sec1_m2: k6_dom=0 (frac=0.4122), kl=0.015336, entropy=2.3157
- sec2_m0: k6_dom=0 (frac=0.4527), kl=0.01473, entropy=2.2172
- sec2_m1: k6_dom=0 (frac=0.4296), kl=0.008732, entropy=2.2515
