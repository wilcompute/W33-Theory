# Passes 12199–12204: no three-generation interpolation on either family

Claude track. Producer: `analysis/w33_pass12199_to_12204_no_three_generation_interpolation.py`. Drivers:
`analysis/search_drivers_12199/`.

## 12199: Z2×Z6-I, the second interpolating family

The Scherk–Schwarz translations live on plane 1 (Pass 12177). The census covers all 29 SUSY Standard Models:

| (even, odd) net quark generations | parents |
|---|---|
| (0, 3) | 19 |
| (1, 2) | 7 |
| (−1, 4) | 2 |
| (2, 1) | 1 |

- **Method:** the same exact method as 12180, with the non-SUSY geometry planes 1↔2 swapped.
- **Control:** the V0-independent total holds in 10/10 parents.
- **Results:**
  - 160 admissible interpolations (8 parents × 20 V0).
  - 4 exact Bose–Fermi degeneracies, all in SM_2572, which has (1, 2): at most 2 generations survive.
  - Every admissible parent is (1, 2) or (−1, 4).

## 12199b: the refined triviality lemma

Pass 12180c showed a translation needs W_2t ∈ Γ. **That is not sufficient.** The translation is a symmetry (pairing
fixed points with identical spectra) only if every product of W_2t with the shifts and Wilson lines is even.

This was tested on all 11 Γ-valued plane-1 directions: "all products even" holds exactly when "paired-sector net even"
holds, 11/11. The three apparent exceptions to pairing (SM_680, SM_1577, SM_9, each with net 3 in paired sectors) are
exactly the odd-product cases. For SM_680 the net 3 was confirmed by the independent non-SUSY engine. Their 40
interpolation runs are excluded.

## 12200: generation placement on Z6-II

With a Γ-valued direction, the paired-sector net is even in all 128 parents, with 0 violations. One apparent violation
was an artefact: a label shared by two base files, fixed by keying on base + label. All 103 such parents have
(even, odd) = (1, 2).

## 12201: order-4 Witten shifts do not help

The W_2t condition does not involve V0 (V0 − V0 = 0). So no Witten shift of any order rescues SM_2751.

SM_2751's Wilson-line variants with a trivial direction:

| variants | count |
|---|---|
| tried | 300 |
| consistent orbifolds | 86 |
| Standard Models | **0** |
| fail modular invariance | 214 |

Control: the unmodified SM_2751 passes the same tool as a Standard Model.

## 12202: twisted 10_H

No analytic proof was obtained. The evidence remains the sample of 0/238 (12182).

## 12203: the native Narain point admits no Scherk–Schwarz translation

The native C3×C3 of 12194–12198 is integral, preserves η and has order 3. Its common fixed space on L/2L is **0**; each
single C3 fixes 2 dimensions. An interpolation radius at the native point requires breaking the symmetry to one C3.
This is consistent with 12198's statement that the native symmetry fixes zero moduli.

## 12204: synthesis

On both W(3,3) families that admit interpolation, Bose–Fermi degeneracy occurs (3/1400 on Z6-II, 4/160 on Z2×Z6-I).
It never comes with three generations.
