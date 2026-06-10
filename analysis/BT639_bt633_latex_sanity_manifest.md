# BT639 — BT633 LaTeX Sanity Manifest

BT639 extends the paper-pipeline guardrail for the BT633 E2/WG2 phase-packet insert.

Expected files:

- `analysis/BT633_e2_wg2_phase_packet_insert.tex`
- `paper/sections/sec_bt633_e2_wg2_phase_packet.tex`
- `paper/w33_preprint.tex`

Expected preprint input line:

```tex
\input{sections/sec_bt633_e2_wg2_phase_packet}
```

Expected BT633 content markers:

- `duad--phase carrier`
- `P_{77}`
- `P_{-3}`
- `15_+\oplus15_-`
- `J^2=-I`
- `(iJ)^2=+I`

The direct legacy-verifier patch was blocked by the connector safety layer, so this manifest records the BT633 static sanity target without mutating the larger checker. The intended static check is: source exists, section copy exists, the preprint input line appears once, display math delimiters are balanced, and the six markers above are present in the section copy.
