# BT1476 Rendered Equation Acquisition Plan

This is the deterministic checklist for acquiring Otto equations (49), (50), (64), (65), and (66).

| eq | section | visible anchor | image target | residual targets | claim gate |
|---:|---|---|---|---|---|
| 49 | gyromagnetic correction factor | golden-mean anomalous factor prose | equation image immediately after anchor prose | delta_g,a_e,g_over_2 | blocked until formula image transcribed |
| 50 | gyromagnetic correction factor | series expansion accurate to tenth decimal prose | equation image immediately after series prose | delta_g,a_e | blocked until formula image transcribed |
| 64 | quantum vortex structure | icosahedron/golden-quartic/circumsphere prose | equation image for icosahedral numerical interpretation | delta_g,structural | blocked until formula image transcribed |
| 65 | quantum vortex structure | 12 slings to 13 half-turns prose | equation image involving 12/13 ratio and exponent | ratio_12_13,delta_g | blocked until formula image transcribed |
| 66 | quantum vortex structure | modified Schwinger alpha/pi prose | equation image for modified Schwinger relation | Schwinger,delta_g | blocked until formula image transcribed |

Workflow:
1. Acquire rendered equation image from PDF or page screenshot.
2. Transcribe into `formula_raw` exactly.
3. Convert to `parser_expr` using BT1464 aliases.
4. Run BT1461/BT1464 residual audit.
5. Promote only if the BT1469 claim DAG allows the dependency edge.
