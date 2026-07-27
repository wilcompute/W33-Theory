"""BT1628: The Two 540s -- Disambiguation Rule and Corpus Audit

W(3,3) has TWO distinct G-sets of size 540 that are NOT conjugate:

  1. LINE-nonedge 540: pairs of lines (= points of W(3,3)'s dual) that are NOT
     collinear. These are the frames/cubes/skew-pairs. Stabiliser = C2xS4 (order 48).
     SmallGroup [48,48] = O_h.

  2. POINT-nonedge 540: pairs of points that are NOT collinear. Stabiliser =
     ((C4xC2):C2):C3 (order 48). SmallGroup [48,?]. DIFFERENT from O_h.

Both have identical orbit arithmetic: 51840 = 540 x 2 x 48.
Nothing distinguishes them by order alone. Context is required.

All passes about frames, cubes, the Steinberg module, and the filter theorem
operate on the LINE-nonedge 540. The point-nonedge 540 appears in the
Kochen-Specker context graph construction.

Canonical token vocabulary:
  {540:line-nonedge}   = frames/cubes/skew-pairs
  {540:point-nonedge}  = noncollinear point pairs
"""

G_PSp43 = 25920   # |PSp(4,3)|
G_WE6   = 51840   # |W(E6)| = |PSp(4,3).2|

line_nonedge_540 = {
    "size": 540,
    "description": "pairs of lines (frames/cubes/skew-pairs) that are not collinear",
    "stabiliser_name": "C2 x S4 = O_h",
    "stabiliser_order": 48,
    "SmallGroup_ID": "[48,48]",
    "orbit_check": 51840 // (540 * 48),  # = 2 (double-counts directed pairs)
    "relevant_passes": ["1079", "1082", "1100", "1101", "1110", "1117", "1125"],
    "context": "frame module pi_540, Steinberg module, filter theorem, S3 controller"
}

point_nonedge_540 = {
    "size": 540,
    "description": "pairs of points that are not collinear",
    "stabiliser_name": "((C4xC2):C2):C3",
    "stabiliser_order": 48,
    "SmallGroup_ID": "[48,?] -- DIFFERENT from [48,48]",
    "orbit_check": 51840 // (540 * 48),  # = 2 (same arithmetic, different group)
    "relevant_passes": ["KS context graph construction"],
    "context": "Kochen-Specker graph, contextual fraction measurement"
}

print("── The Two 540s of W(3,3) ──")
print()
print("1. LINE-nonedge 540 (frames/cubes/skew-pairs):")
for k, v in line_nonedge_540.items():
    print(f"   {k:25s} = {v}")
print()
print("2. POINT-nonedge 540 (noncollinear point pairs):")
for k, v in point_nonedge_540.items():
    print(f"   {k:25s} = {v}")

print()
print("── Orbit arithmetic check ──")
print(f"Line-nonedge:  51840 / (540 x 48) = {51840 // (540*48)}  (= 2, valid double-count)")
print(f"Point-nonedge: 51840 / (540 x 48) = {51840 // (540*48)}  (= 2, same arithmetic)")
print("IDENTICAL orbit arithmetic -- this is WHY they were confused.")

print()
print("── Disambiguation rule ──")
print("When citing '540' in corpus analysis, ALWAYS specify:")
print("  {540:line-nonedge}   for frames/cubes/skew-pairs (Steinberg / filter context)")
print("  {540:point-nonedge}  for noncollinear point pairs (KS / CF context)")
print()
print("Passes 1079, 1082, 1100, 1101 are ALL about the LINE-nonedge 540.")
print("Any file citing these passes but referencing 'the 540' without qualifier")
print("is AMBIGUOUS and should be tagged during corpus audit.")

print()
print("── check_stale_boundaries.py self-test tokens ──")
print("  Token 1: polar-pair@4   (BT810 open question, closed by BT811)")
print("  Token 2: polar-pair@40  (BT810 open question, closed by BT811)")
print("Widening tolerance = build failure.")

print("\nBT1628 COMPLETE.")
