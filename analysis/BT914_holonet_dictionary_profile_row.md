# BT914 — Holonet Dictionary Profile Row

BT914 integrates the BT897--BT913 profile package into the paper-facing physics-to-architecture dictionary.

## Integrator

```text
tools/integrate_bt914_holonet_dictionary_row.py
```

It idempotently adds the row:

| object | physics reading | architecture reading |
|---|---|---|
| profile multiplicity \(9\cdot\mathbf2\) | CKM/PMNS/Koide coordinate layer | four profile planes plus sentinel |

## Paragraph added by the integrator

The dictionary patch explains:

\[
\mathbb C^9=(2+2+2+2)+1.
\]

The four two-planes carry

\[
\frac9{178},\quad \frac4{13},\quad \frac2{91},\quad \frac7{13},
\]

and the final \(+1\) is a sentinel/provenance coordinate. It is not a sterile generation.

## Boundary

The row belongs in the Photonic Holonet dictionary because it links one integer package to two readings:

- physics: CKM/PMNS/Koide coordinate layer;
- architecture: profile planes plus sentinel monitor.

## Witness

```text
tools/integrate_bt914_holonet_dictionary_row.py
data/PART_BT914_HOLONET_DICTIONARY_ROW_results.json
```
