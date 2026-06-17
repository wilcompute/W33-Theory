# BT1282 -- Recovery Packet Reproducibility Section

## Purpose

BT1282 adds a final paper-side reproducibility note for the finite Clifford recovery packet.

## Section files

```text
analysis/BT1282_recovery_packet_reproducibility_section.tex
paper/sections/sec_bt1282_recovery_packet_reproducibility.tex
```

## Companion integrator

```text
tools/integrate_bt1282_recovery_packet_insert.py
```

The helper copies the BT1282 analysis TeX into the paper sections directory and inserts the section into the preprint when run.

## Paper content

The section points to:

1. The recovery packet index.
2. The strict polar-path certificate.
3. The machine verifier.
4. The claim that the recovery packet is machine-checkable, not only stated as prose.

## Boundary

The paper section and companion integrator were pushed. A direct CI workflow edit to add the BT1282 companion integrator was blocked by the connector safety layer during this turn, so CI wiring should be retried in the next safe patch pass.
