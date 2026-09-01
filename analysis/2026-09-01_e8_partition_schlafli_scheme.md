# The 27 E8 completion partitions carry the cubic-surface Schlaefli incidence

## Exact theorem

The selected E8/W33 lift contains 45 distinguished orthogonal `D4+D4` packets. The previous completion theorem groups them into 27 five-packs; every five-pack partitions the full 240-root shell into ten selected `D4` subsystems.

Treat those 27 ten-`D4` decompositions as vertices and join two when they share a `D4+D4` packet. Then:

- every pair of partitions shares either `0` or `2` selected `D4` blocks;
- `135` unordered pairs share `2` blocks and `216` share none;
- every partition has degree `10`;
- adjacent pairs have exactly `1` common neighbour;
- nonadjacent pairs have exactly `5` common neighbours.

Therefore the partition-overlap graph is

\[
\boxed{\operatorname{SRG}(27,10,1,5)},
\]

the line-intersection graph of the 27 lines on a smooth cubic surface. Its complement is the usual Schlaefli graph

\[
\boxed{\operatorname{SRG}(27,16,10,8)}.
\]

The packet layer reappears exactly as the triangle layer. Every one of the 45 selected `D4+D4` packets lies in three completion partitions, those three vertices form a triangle, and the graph has exactly 45 triangles. Conversely every graph triangle comes from exactly one packet. Thus the classical cubic-surface dictionary is realized internally in the selected E8 partition catalogue:

\[
\boxed{
27\text{ cubic lines}
\leftrightarrow
27\text{ ten-}D_4\text{ E8 partitions},
}
\]

\[
\boxed{
45\text{ tritangent planes}
\leftrightarrow
45\text{ common }D_4\oplus D_4\text{ packet blocks}.
}
\]

Incidence is literal containment: a tritangent/packet belongs to a cubic-line/partition exactly when its two selected `D4` blocks are members of that partition.

## Important boundary

All 27 decompositions partition the **same** 240-root E8 shell, so saying two partitions “intersect in 48 roots” would be wrong: their underlying root sets are identical. The invariant is common **partition blocks**. Adjacent partitions share one 48-root packet block, i.e. two `D4` blocks; nonadjacent partitions share no selected `D4` block.

## Reproducer

```bash
python analysis/w33_20260901_e8_partition_schlafli_scheme.py
```

Frozen output:

```text
data/PART_W33_20260901_E8_PARTITION_SCHLAFLI_SCHEME.json
```
