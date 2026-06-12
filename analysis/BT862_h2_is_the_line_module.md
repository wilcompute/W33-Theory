# BT862 — H₂ Is the Sign-Twisted Line Module: The Homological Dictionary Completes

**Status: PROVEN (full character sweep over all 25920 elements, `analysis/bt862_h2_is_the_line_module.py`, data `data/bt862_h2_is_the_line_module.json`)**

Closing BT861's open. H₂ of the W(3,3) 2-complex has dimension 40 — one
generator per line, since each line's K₄ carries 4 triangles forming a
tetrahedron boundary (a 2-sphere, hence a 2-cycle).

**Refutation en route:** H₂ is *not* the plain permutation module on lines
(pointwise character mismatch, despite matching norm 3). A symmetry fixing a
line setwise acts on its tetrahedron-boundary 2-cycle by the **parity of the
induced permutation of its 4 points** (the S₄-action on H₂(S²) is the
determinant). Verified for every group element:

```text
chi_H2(g) = Σ over setwise-fixed lines of sign(g restricted to the line)
⟨chi_H2, chi_H2⟩ = 3      (three irreducible constituents, sign-twisted rank-3)
```

## The completed homological dictionary

| homology | dim | module | machine reading |
| --- | --- | --- | --- |
| H₀ | 1 | trivial | the vacuum pole |
| H₁ | 81 | **Steinberg** (BT861) | the protected matter register = QECC logical space |
| H₂ | 40 | **sign-twisted line module** | the *oriented* timetable carrier |

The 2-complex of the substrate computes the entire machine: vacuum below,
Steinberg memory in the middle, and an orientation-sensitive copy of the
40 contexts on top — the top homology remembers not just *which* contexts
exist but their chirality under symmetry, feeding the orientation bits of
the chirality ledger (BT857).

## Open

- Decompose the sign-twisted line module into its 3 irreducibles (degrees?)
  and compare with the plain line module's 1+15+24.
- Mod-3 homology of the same complex (the code is over F₃): Steinberg mod 3
  is the projective cover story — compute dims.
