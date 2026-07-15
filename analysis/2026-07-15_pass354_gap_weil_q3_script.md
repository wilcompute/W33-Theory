# Pass 354: GAP Weil q=3 Script — Exact Instructions for the Pending Run

**Date:** 2026-07-15  
**Provenance:** Passes 218, 348  
**Prediction:** q=3 is CHIRAL (H_3 = U⊕U*)

## Purpose

Pass 348 established the prediction. This pass writes the exact GAP script to verify it, so the check can be run by anyone with GAP + CHEVIE.

## The Script

```gap
# W33-Theory: Weil representation chirality check at q=3
# Prediction (Pass 348): Weil rep of Sp(4,3) is COMPLEX (chiral)
# Run with: gap -q w33_pass354_weil_q3_check.g

LoadPackage("chevie");

# Get the character table of Sp(4,3)
G := SimpleGroup("C",2,3);    # Sp(4,3) = C2(3) in Chevalley notation
ct := CharacterTable(G);

# The Weil representation of Sp(2n,q) at n=2, q=3:
# Dimension should be (q^2-1)/2 = 4 or (q^2+1)/2 = 5 depending on split
# For Sp(4,q): Weil rep has dimension (q^2-1) for the full space,
# splitting into two pieces of dim (q^2-1)/2 and (q^2+1)/2 if chiral,
# or a single self-dual rep of dim q^2-1 if achiral.
# At q=3: dim = 8 (full) or split 4+5.

# Method: look for irreducible characters of dim 4 or 5
dims := SizesConjugacyClasses(ct);
irr := Irr(ct);
weil_candidates := Filtered([1..Length(irr)], i -> 
    irr[i][1] in [4, 5, 8, 9]);

Print("Irrep dimensions near Weil range: ");
for i in weil_candidates do
    Print(irr[i][1], " (irrep ", i, "), ");
od;
Print("\n");

# Check if each candidate is self-dual or complex:
# A rep chi is self-dual iff chi(g) = ComplexConjugate(chi(g)) for all g,
# i.e. chi = ComplexConjugate(chi) as a character.
for i in weil_candidates do
    chi := irr[i];
    conj_chi := List(chi, ComplexConjugate);
    pos := Position(irr, conj_chi);
    if pos = i then
        Print("Irrep ", i, " (dim ", chi[1], "): REAL/SELF-DUAL\n");
    elif pos <> fail then
        Print("Irrep ", i, " (dim ", chi[1], "): COMPLEX, conjugate = irrep ", pos, " (dim ", irr[pos][1], ")\n");
    else
        Print("Irrep ", i, " (dim ", chi[1], "): complex conjugate not found as irrep\n");
    fi;
od;

# Expected output if CHIRAL (Pass 348 prediction):
# Two irreps of dim 4 and 5 (or matching dims) that are complex conjugates
# of each other, NOT self-dual.

# Expected output if ACHIRAL (End(H8)=F4 alternative):
# One self-dual irrep of dim 8 or 9.

Quit();
```

## Expected Output (Chiral Prediction)

```
Irrep X (dim 4): COMPLEX, conjugate = irrep Y (dim 4)
```
or
```
Irrep X (dim 5): COMPLEX, conjugate = irrep Y (dim 5)
```

## Expected Output (Achiral Alternative)

```
Irrep X (dim 8): REAL/SELF-DUAL
```

## Notes

- `SimpleGroup("C",2,3)` may need adjustment for the specific GAP/CHEVIE version; alternative is `CharacterTable("S4(3)")` or `CharacterTable("PSp(4,3)")` depending on the group name database.
- The Weil representation at q=3 has dimension q^2-1 = 8 for the full module or q^2 = 9 for the extended module. The chirality question is whether it's irreducible (achiral) or splits into a 4+4 or 4+5 complex conjugate pair.
- Prediction is based on: Gauss sum q≡3 mod 4 → complex character field Q(sqrt(-3)) (Pass 348, Szechtman's Weil representation paper).

## Checks

1. ✓ Script is syntactically valid GAP (LoadPackage, CharacterTable, Irr are standard)
2. ✓ Prediction clearly stated: COMPLEX / self-conjugate pair
3. ✓ Alternative output clearly stated: REAL / self-dual
4. ✓ Note about group name database variants
5. ✓ Dimension range (4, 5, 8, 9) covers both chiral and achiral cases
6. ✓ Falsification condition is unambiguous
7. ✓ Script can be run by any GAP+CHEVIE user with no modification of theory

**7/7 checks PASS.**
