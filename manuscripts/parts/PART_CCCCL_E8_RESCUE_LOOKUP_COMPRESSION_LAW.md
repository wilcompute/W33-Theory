# PART CCCCL — E8 Rescue Lookup Compression Law

This part compresses the rescue computation to a constant-time lookup on the
pair invariant

$$
d = a\cdot b
$$

for doubled E8 roots.

## Closed-form law

If $R(a,b)$ is the number of third references $c$ that satisfy the
$24/108/108$ feasibility condition, then

$$
R(a,b)=
\begin{cases}
126, & |d|=8,\\
234, & |d|=4,\\
240, & d=0.
\end{cases}
$$

## Pair-count structure

Unordered pairs (including diagonal) satisfy:

$$
\#(d=8)=240,\; \#(d=-8)=120,\; \#(d=\pm4)=6720\;\text{each},\; \#(d=0)=15120.
$$

## What this achieves

It replaces expensive triple-class rescue evaluation with a direct lookup map
from one scalar invariant $d$.

## Honesty boundary

This part certifies the lookup law with canonical representatives and deterministic
direct checks; it does not brute-force direct rescue counts for all 28,920 pairs.
