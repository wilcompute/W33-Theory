# BT1001 — Full-degree heat-supertrace estimator stack

BT1001 extends BT997 from the K3_16 middle-degree heat trace to an all-degree
estimator stack for CP2_9 and K3_16.

## Baseline

| seed | chain dimensions | Betti | chi |
| --- | ---: | ---: | ---: |
| CP2_9 | [45, 414, 1236, 1440, 576] | [1, 0, 1, 0, 1] | 3 |
| K3_16 | [136, 2640, 9440, 11520, 4608] | [1, 0, 22, 0, 1] | 24 |

Exact supertrace targets:

```text
CP2_9: 3 for t = 0.01, 0.05, 0.1, 1.0
K3_16: 24 for t = 0.01, 0.05, 0.1, 1.0
```

Large-time degreewise limits:

```text
CP2_9: [1, 0, 1, 0, 1]
K3_16: [1, 0, 22, 0, 1]
```

## K3 middle-degree input from BT997

```text
t=0.01: 8730.448450900843
t=0.05: 6517.153579984
t=0.1 : 4689.188846613879
t=1.0 : 315.2835608902251
```

## Production plan

1. Run CP2_9 all degrees as a fast estimator validation.
2. Run K3_16 degrees 0, 1, 3, 4.
3. Combine with BT997 degree-2 estimates.
4. Check the alternating heat-supertrace against chi at each t.

## Boundary

BT1001 is the estimator stack and manifest. It does not claim that all K3_16
ordinary heat traces have already been computed; BT997 computed the middle-degree
production target, and BT1001 defines the full-degree completion path.

## Witnesses

```text
analysis/bt1001_full_heat_supertrace_estimator_stack.py
data/bt1001_full_heat_supertrace_estimator_stack.json
```
