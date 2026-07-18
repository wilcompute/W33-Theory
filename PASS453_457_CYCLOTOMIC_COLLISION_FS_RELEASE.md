# Passes 453–457 — cyclotomic, collision, and FS release

This release resolves or sharply narrows all five questions inherited from Pass 447.

1. **Cyclotomic covariance:** the q=5 square-root-five coefficient field is forced by the real fifth cyclotomic field.
2. **q=7 falsifier:** the quadratic atlas disappears and is replaced by the real cubic seventh cyclotomic field of discriminant 49.
3. **FS closure:** both faithful degree-three representations on both extraspecial groups have ordinary indicator 0 and canonical twisted indicator +1.
4. **Collision anatomy:** three of four sampled collisions are orbit repeats; the fourth is a nonisomorphic, cospectral, Smith-identical pair.
5. **Formal geometry:** Lean now proves the shifted-span orthogonal containment that was the named post-Pass-447 boundary.

The combined message is corrective rather than decorative:

\[
\boxed{
\sqrt5\text{ at }q=5\text{ is cyclotomic};\quad
q=7\text{ is cubic};\quad
\text{spectrum+Smith is still incomplete};\quad
\text{FS does not split exp-3/exp-9}.}
\]

All Python certificates and the focused regression suite pass locally. The Lean source is structurally audited; remote compilation is not claimed until GitHub Actions exposes a completed run.
