# BT931 — Canonicality stress test

BT931 stress-tests the BT928/BT929 chain-to-E8 map across random valid homology-basis choices.

## Run

```text
trials = 512
seed = 1
```

For every trial, the script:

1. chooses a random invertible F2 change of homology basis;
2. recomputes the source symplectic normal form;
3. maps into the BT926 vertex E8 target;
4. checks mod-2 isometry, integral determinant, and positivity.

## Results

- All 512 maps are mod-2 isometries.
- All 512 lifted 0/1 maps are unimodular and positive-definite in the vertex E8 target.
- Determinant counts: `-1`: 265, `+1`: 247.
- Support sum varies from 76 to 116, mean 96.3984375.
- Best seen support/balance profile:

```text
sum = 76, spread = 8, sorted profile = [6, 6, 6, 10, 10, 10, 14, 14]
```

## Conclusion

Positivity and unimodularity are not enough to select a canonical map: the maps all remain valid. The next selector must use a secondary criterion such as support energy and balance.

## Witness

```text
analysis/bt931_canonicality_stress_test.py
data/bt931_canonicality_stress_test.json
```
