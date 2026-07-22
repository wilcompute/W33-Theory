# Pass 562 — derive the five fibre types from invariant tensors

For each exact level set

`S_(a,b,c) = {s : (e3(s),e4(s),e5(s)) = (a,b,c)}`,

the geometry is recovered directly from transforms of its invariant-tensor indicator:

- `dim T(S) = 12 - rank(span supp Walsh(1_S))`;
- affine-hull dimension is 12 minus the rank of characters whose Walsh coefficient has magnitude `|S|`;
- the Boolean Möbius transform of `1+1_S` gives the principal-generator degree.

These formulas reproduce the exact type census

`(16,4,4,1,8)^1`, `(40,11,1,20,9)^44`, `(40,11,2,10,9)^48`, `(80,8,4,5,8)^3`, `(80,12,1,40,8)^2`.

Thus the five types are consequences of the `A5` invariant-tensor level sets, not merely labels attached after a separate geometric census.
