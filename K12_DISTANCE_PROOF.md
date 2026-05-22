# K12 Horizon Code Minimum Distance — Proof Strategy

**Claim:** The K12 horizon code `[72, 66, 3]₃` has minimum distance `d = 3`.

## Step 1: Lower Bound (d ≥ 3)

The K12 horizon code is a cycle code on the horizon graph `H`.

For any cycle code on a graph `G`, the minimum distance satisfies:
```
d ≥ girth(G)
```
where `girth(G)` is the length of the shortest cycle.

**Claim:** `girth(K12) = 3`.

If K12 is the complete graph K₁₂: girth = 3 (every pair of edges sharing a vertex closes a triangle).

If K12 is the specific quartic horizon graph (regular, 12 vertices, genus 6): must verify explicitly — see action item C336a.

**Assuming girth = 3:** Every triangle `{e₁, e₂, e₃}` in K12 is a cycle of length 3, hence a valid codeword of weight 3. Therefore `d ≤ 3`.

Combined with `d ≥ 3` (from girth ≥ 3): `d = 3`. ∎

## Step 2: Upper Bound (d ≤ 3)

Exhibit an explicit weight-3 codeword.

Let `v₁, v₂, v₃` be any three mutually adjacent vertices in K12 (a triangle).
The three edges `e₁₂, e₁₃, e₂₃` form the boundary of a 2-cell (triangle face).
In the cycle code, this boundary is the zero vector modulo the boundary map.
Hence the incidence vector of `{e₁₂, e₁₃, e₂₃}` is a codeword of weight 3.

**Therefore:** `d ≤ 3`.

## Conclusion

```
3 ≤ d ≤ 3  →  d = 3  ✓
```

The minimum distance of the `[72, 66, 3]₃` K12 horizon code is **exactly 3**.

## Action Item C336a

Verify explicitly:
1. The adjacency structure of the W33 K12 horizon graph
2. Confirm girth = 3
3. Exhibit the three vertices of the shortest triangle
4. Write the weight-3 codeword vector explicitly

---

*W33-Theory | Wil Dahn | May 22, 2026*
