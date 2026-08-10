# Erratum to Pass 1830 — the four fixed lines do determine the 270-class

**Superseding result:** Pass 4722, `analysis/w33_pass4721_4724_support12_involution_square_root_cover.py`.

Historical Pass 1830 correctly found an inner involution class of size 270 whose elements fix zero W33 points and four pairwise-disjoint W33 lines. It then reported that the orbit of the four-line set had size 2,880 and concluded that the set did not determine the class.

That orbit computation was not on W33 lines.

In `analysis/w33_pass1830_name_the_270.g`, the group is constructed as

```gap
G := Image(ActionHomomorphism(N, pts, OnLines));
```

so `G` is a permutation group on the 40 **point positions**. The variable `fix`, however, is a set of **line indices**. The later call

```gap
Orbit(G, Set(fix), OnSets)
```

therefore reinterprets the same integers `1..40` as point labels. It does not compute the induced action on the set of 40 W33 lines.

Pass 4722 constructs that induced line action explicitly. The inner involution census is

\[
315=270+45,
\]

with fixed-line profile

\[
4^{270}\oplus16^{45}.
\]

The 270 four-fixed-line sets are distinct, form one `PSp(4,3)` orbit with stabilizer 96, and are exactly the 270 four-line residues obtained from the support-12 disjointness triangles. Hence the corrected conclusion is:

\[
\boxed{\text{the four fixed W33 lines do determine the size-270 inner involution class.}}
\]

The historical file is retained for provenance; its 2,880 orbit and the resulting “object unknown” conclusion are withdrawn.
