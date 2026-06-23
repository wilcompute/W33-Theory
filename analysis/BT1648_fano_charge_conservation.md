# BT1648 Fano Charge-Conservation Law

BT1648 explains the `80x9 + 88x10 = 1600` usage profile as a conserved Fano charge:

```text
80 unanchored fuel bins * 9
+ 40 same-anchored fuel bins * (9 fuel + 1 same-ray control)
+ 48 compatible reserve bins * 10
= 1600 frames
```

Equivalently, the seven Fano lines split as `5` gate lines and `2` reserve lines:

```text
5*(16*9 + 8*10) + 2*(24*10) = 1600.
```
