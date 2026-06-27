# BT1896-BT1898 summary

Executed BT1896-BT1898 after the Holonet paper/source read and BT1893-BT1895 audit.

## BT1896

Added a residual-language clarification patch:

```text
papers/BT1896_holonet_residual_language_patch.tex
```

It separates finite machine closure from physical-continuum closure and gives the safe public statement:

```text
finite machine-complete architecture, with remaining physical/continuum identifications classified
```

## BT1897

Verified the source trail for the guard envelope.

The exact formula was not found in the uploaded Holonet TeX pass, but it is present in repo artifacts BT1649/BT1650:

```text
2^11 = 2048
2048 - 1600 = 448 = 7*64
64 = 24 dark + 24 loss + 16 parity
```

So the guard-envelope theorem may be cited as repo-derived, but it needs an insert before being treated as part of the uploaded Holonet paper body.

## BT1898

Added the single-photon demonstrator runbook:

```text
data/bt1898_demonstrator_runbook.json
analysis/BT1898_demonstrator_runbook.md
```

It specifies components, run sequence, raw data columns, witness targets, and pass/fail criteria for the unencoded single-photon demonstrator.

Witness targets:

```text
contextual fraction = 1/10
pump Chern = 2
accepted logical rate = 13/40
physical frame split = 160 diagonal + 480 off-diagonal
```

Boundary: language patch, source verifier, and demonstrator runbook only; no residual solution, hardware threshold, or GKP fault-tolerant build is claimed.
