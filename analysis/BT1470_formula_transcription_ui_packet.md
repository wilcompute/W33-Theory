# BT1470 Formula Transcription UI Packet

Fill `formula_raw` from the rendered equation image, then translate it into `parser_expr` using BT1464 aliases.

Allowed parser aliases: `Phi`, `phi`, `phi5`, `delta_g`, `a_e`, `Schwinger`, `ratio_12_13`, `alpha`, `pi`, `sqrt`.

| eq | source context | formula image ref | formula_raw | parser_expr | target_class | residual | claim_tier |
|---:|---|---|---|---|---|---|---|
| 49 | g-factor section; golden-mean representation | Otto paper equation (49) |  |  | g_over_2 or delta_g or a_e |  | blocked_pending_transcription |
| 50 | g-factor section; series expansion | Otto paper equation (50) |  |  | delta_g or a_e |  | blocked_pending_transcription |
| 64 | vortex section; icosahedron/quartic radius relation | Otto paper equation (64) |  |  | delta_g or structural |  | blocked_pending_transcription |
| 65 | vortex section; 12/13 half-turn ratio | Otto paper equation (65) |  |  | ratio_12_13 or delta_g |  | blocked_pending_transcription |
| 66 | vortex section; modified Schwinger alpha/pi | Otto paper equation (66) |  |  | Schwinger or delta_g |  | blocked_pending_transcription |

Audit workflow:
1. Fill `formula_raw` exactly from the equation image.
2. Convert to `parser_expr` using BT1464 aliases.
3. Run `python tools/bt1464_formula_parser_upgrade.py` or the residual runner.
4. Promote claim tier only if residual and derivation checks pass.
