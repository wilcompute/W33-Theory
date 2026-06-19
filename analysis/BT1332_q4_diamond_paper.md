# BT1332 -- Q4 Diamond Machine-Audited Paper

## Purpose

BT1332 writes and compiles a professional LaTeX paper from the BT1326 master synthesis, BT1327 audit, BT1328 epoch repair, and BT1331 certificate.

## Title

```text
The W33 HoloNet Q4 Diamond: A Machine-Audited Master Synthesis with Rolling-Epoch Repair
```

## Local build products

```text
w33_q4_diamond_machine_audited_synthesis.tex
w33_q4_diamond_machine_audited_synthesis.pdf
```

## Build

```text
pdflatex, two passes
9 pages
```

## Main correction carried into paper

```text
10980 = 3*3660
```

by rolling chart-phase closure:

```text
3660 = 6*540 + 180
180 = 540/3
3*180 = 540
```

The paper explicitly rejects the false derivation:

```text
10980 = lcm(3660,1620)
```

because the literal lcm is 98820.

## Certificate boundary

The paper separates claims into exact arithmetic, structural theorem, simulation gate, and engineering gate. Exact arithmetic and the repaired epoch are certificate-backed; the threshold and chip footprint remain separate simulation/engineering gates.
