# BT923 — Reconciling the two Euler/index pictures of the W(3,3) complex

**Status: PROVEN (`analysis/bt923_dirac_index_euler.py`, data `data/bt923_dirac_index_euler.json`)**

> **Not a new breakthrough — a reconciliation.** The repo already documents
> (index.html) the Euler characteristics χ = −40 = −v (truncated shell) and
> χ = −80 = −2v (full clique complex), a 480-dim Dirac/Hodge operator with
> chirality + index theorem + McKean–Singer supertrace −80, and the
> generation index ind(D)=q=3. BT923 adds **one** genuinely-new thing: the
> explicit bridge between the truncated 2-complex (BT921) and the documented
> full clique complex, identifying the b₂ = 40 obstruction with the BT862
> line module. Everything else below is a rederivation kept for the spectral
> triple's self-containedness.

Equipping the BT921 finite spectral triple with the chirality grading and
computing its index — and reconciling it with the existing 480-dim picture.

## The theorems

- **T1 — even (Z₂-graded) spectral triple.** Equip H = C₀⊕C₁⊕C₂ with the
  chirality grading γ = +1 on even cochains (C₀, C₂), −1 on odd (C₁). Then
  γ² = 1 and **γD = −Dγ** (D = d+d* shifts cochain degree by ±1): the
  Hodge–Dirac is an even, Z₂-graded operator — a genuine even spectral triple.
- **T2 — index = Euler characteristic = −v.** By McKean–Singer the index is
  the γ-trace over the harmonic forms (the homology, BT921):

  ```text
  ind(D) = (b₀ + b₂) − b₁ = (1 + 40) − 81 = −40
         = χ = 40 − 240 + 160 = −v.
  ```

  The Dirac index equals the Euler characteristic of the W(3,3) 2-complex,
  which is exactly **−v = −40** (already in index.html as the truncated-shell χ).
- **T3** — so the substrate vertex count v = 40 is *minus the index* of its
  Hodge–Dirac operator; the odd sector b₁ = 81 (the Steinberg matter register)
  dominates, so the matter register drives the index.

## The genuinely-new piece: reconciling the two complexes

The repo carries two Euler/Dirac pictures of W(3,3) that were never explicitly
bridged:

| complex | f-vector | homology b | χ | Dirac |
| --- | --- | --- | --- | --- |
| truncated 2-complex (BT921/923) | (40, 240, 160) | (1, **81**, **40**) | −v = −40 | 440-dim |
| full clique complex (index.html) | (40, 240, 160, 40) | (1, 81, 0, 0) | −2v = −80 | 480-dim, supertrace −80 |

The bridge (verified in the script): the 40 lines, taken as K₄-tetrahedra
(3-cells), give a boundary D₃ of **rank 40 — all 40 independent**. Adding them
to the 2-complex therefore:

- **kills b₂ exactly: 40 → 0**, and
- **doubles |χ|: −v → −2v.**

And the b₂ = 40 that the tetrahedra fill is precisely the **BT862 line module**
(H₂ = the sign-twisted 40-dim line module). So the two documented Euler numbers
are one complex with/without its 40 line-cells, and the 40-cell jump is the
line module getting filled. The truncated picture (−v, b₂ = 40 = line module)
exposes the matter/line content as homology; the clique picture (−2v, b₂ = 0)
fills it. This is the only new content here; the chirality/index-theorem/
McKean–Singer machinery itself is already in the repo.

## Rederived (for the spectral triple's self-containedness)

The even grading γ (γ²=1, γD=−Dγ) and the McKean–Singer identity
ind(D) = (b₀+b₂)−b₁ = χ = −v are recomputed here on the BT921 2-complex Dirac
so the spectral triple (BT892 spectral action, BT921 spectrum, this grading) is
self-contained; these facts already appear in index.html for the 480-dim
clique-complex Dirac (supertrace −80) and as ind(D)=q=3 (generation index).

## Open

- The Connes first-order condition [[D,a],b°]=0 for the W(3,3) algebra
  representation (the remaining real-spectral-triple axiom).
- The curved-4D continuum / spectral-action asymptotics (the EH coefficient).
