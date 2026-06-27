# BT1897 — 2048 Guard-Envelope Source Verifier

BT1897 resolves the source status of the guard-envelope formula.

## Uploaded-source status

In the uploaded `photonic_holonet.tex` source used for BT1893-BT1895, I did not find the exact statement:

```text
2048 = 1600 + 448
```

So BT1894 correctly refused to promote it as a statement already present in that uploaded source.

## Repo-source status

The formula is present in the repo artifacts BT1649/BT1650.

BT1649 states:

```text
2^11 = 2048 time bins
2048 - 1600 = 448 = 7*64 guard bins
per Fano point: 24 dark references + 24 loss probes + 16 parity overflow
```

BT1648-BT1650 states:

```text
2^11 = 2048
2048 - 1600 = 448 = 7*64
```

and assigns each Fano guard page as:

```text
24 dark-reference guards
24 loss-probe guards
16 parity-overflow guards
```

## Arithmetic check

```text
2^11 = 2048
2048 - 1600 = 448
448 = 7 * 64
64 = 24 + 24 + 16
```

## Publication rule

The guard-envelope theorem may be cited as a repo-derived BT1649/BT1650 result.  It should not be described as already contained in the uploaded Holonet TeX unless a patch is inserted.

Boundary: source verifier only; no new optical timing calibration is claimed.
