# Forty Points: reconcile the two-sided Weyl convention

Reading the PDF's opening pages found a notation mismatch in Theorem3.1. Its definition used `P_u=X^(u1) Z^(u2)`, but its phase formula and proof used the clock-first bracket. With the stated `ZX=omega XZ`, the direct witness `XZ=omega^2 ZX` refutes the displayed positive bracket for that shift-first definition.

The cited `analysis/w33_20260924_temporal_su9_e8_compiler.py` already defines `P_u=Z^(u1) X^(u2)` and verifies the displayed phase law on all81^2 label pairs. The executable result is not retracted. The minimal correction is to make the paper use its compiler's clock-first definition, explicitly noting that the two label coordinates are reversed relative to Section2. The theorem's formula and right-action explanation then hold as written.

`w33_20261102_two_sided_phase_convention.py` independently compares both conventions on all6,561 ordered pairs. The shift-first convention disagrees with the displayed phase on4,320 pairs; the clock-first convention agrees on all pairs. Exact exponent counts are0:2241,1:2160,2:2160. Five regressions also verify row-vectorisation on every matrix unit and the explicit X/Z witness.

A global reversal of the symplectic form preserves its zero pairs, so this does not change the W33 commutation graph, its spectrum or the dimensional compiler claims. It matters for labelled oriented phases, which is why a convention must be named rather than inferred from a graph. No new physical result or new general Weyl-algebra identity is claimed.

Reading scope in this continuation: PDF pages1-16 and137-140 were read as extracted text. The full215-page paper and original full weekly-commit corpus remain incomplete. The corrected PDF is rebuilt from TeX and the affected page is visually checked; this is not a full layout review of all215 pages.
