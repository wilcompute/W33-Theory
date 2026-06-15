# BT1046 — Controlled nonzero heavy-sector Phi ansatz

BT1046 extends BT1043 beyond the minimal harmonic-only extension by introducing
formal sector amplitudes on each `Delta_1` eigensector.

## Sector ansatz

```text
Phi | eigensector(lambda) = a_lambda * normalized weakslot Higgs block
```

Sectors:

| sector | lambda | dim | amplitude |
| --- | ---: | ---: | --- |
| harmonic | 0 | 81 | a0 |
| boundary | 4 | 120 | a4 |
| r-sector | 10 | 24 | a10 |
| s-sector | 16 | 15 | a16 |

## Formal traces

Let

```text
h2 = |phi1|^2 + |phi2|^2.
```

Then:

```text
tr_240(Phi^2)
= 54 a0^2 h2 + 80 a4^2 h2 + 16 a10^2 h2 + 10 a16^2 h2
```

```text
tr_240(Phi^4)
= 54 a0^4 h2^2 + 80 a4^4 h2^2 + 16 a10^4 h2^2 + 10 a16^4 h2^2
```

```text
tr_240(Delta_1 Phi^2)
= 320 a4^2 h2 + 160 a10^2 h2 + 160 a16^2 h2
```

## Uniform amplitude case

If all sector amplitudes are set to 1:

```text
tr_240(Phi^2)          = 160 h2
tr_240(Phi^4)          = 160 h2^2
tr_240(Delta_1 Phi^2) = 640 h2
```

## Boundary

This is a controlled ansatz, not a derived physical Yukawa/heavy-sector coupling.
It gives the first nonzero mixed-trace formula without inserting empirical
parameters.

## Witnesses

```text
analysis/bt1046_heavy_sector_phi_ansatz.py
data/bt1046_heavy_sector_phi_ansatz.json
```
