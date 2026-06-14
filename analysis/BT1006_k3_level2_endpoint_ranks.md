# BT1006 — K3_16 level-2 endpoint ranks

BT1006 directly verifies the endpoint rank targets from BT1005 for the level-2
edgewise K3_16 complex.

## Input

```text
f-vector = [2776, 45120, 152960, 184320, 73728]
```

## Endpoint checks

```text
one-skeleton components = 1
rank d1 = 2776 - 1 = 2775
```

For the top boundary:

```text
top dual components = 1
tetrahedron incidence counts = {2: 184320}
boundary tetrahedra = 0
rank d4 = 73728 - 1 = 73727
```

Both endpoint targets are hit:

```text
d1 target = 2775
d4 target = 73727
```

## Reading

The two endpoint ranks are no longer just topology-derived targets. They are
directly verified by connectivity and top-dual connectivity. The remaining K3
level-2 work is the two middle ranks:

```text
d2 target = 42345
d3 target = 110593
```

## Witnesses

```text
analysis/bt1006_k3_level2_endpoint_ranks.py
data/bt1006_k3_level2_endpoint_ranks.json
```
