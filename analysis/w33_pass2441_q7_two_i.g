# Pass 2441 -- the representation-theoretic half of the two-i incompatibility at q=7.
# Geometric half proved for all odd q by the parallel track (Passes 2088-2089).
# Question: does sigma_S (outer, non-square multiplier) FUSE the complex-conjugate
# character pairs of PSp(4,q) for q = 7 and q = 11, exactly as measured at q = 3?

Print("=== Pass 2441: two-i incompatibility, representation half, q = 3,7,11 ===\n\n");

test := function(nm, inner, outer)
  local ti, to, n, fused, i, c, cc, ind, orb, nreal, ncls;
  ti := CharacterTable(inner);
  to := CharacterTable(outer);
  if ti = fail or to = fail then
    Print(nm, " : character table unavailable\n"); return;
  fi;
  n := Irr(ti);
  ncls := Length(n);
  # non-real irreducibles of the INNER group
  nreal := Filtered([1..ncls], i -> ComplexConjugate(n[i]) <> n[i]);
  Print(nm, "\n");
  Print("  |inner|            : ", Size(ti), "\n");
  Print("  irreducibles       : ", ncls, "\n");
  Print("  NON-REAL irreds    : ", Length(nreal), "   (Gow: nonzero iff q = 3 mod 4)\n");
  if Length(nreal) = 0 then
    Print("  -> no phase to lose; nothing to fuse.\n\n"); return;
  fi;
  Print("  their degrees      : ", Set(nreal, i -> n[i][1]), "\n");
  # Does the outer group fuse them?  A non-real irr of the inner group extends to
  # the outer group iff it is fixed by the outer automorphism; it FUSES with its
  # conjugate iff it is not.  Count by comparing induced characters.
  fused := [];
  for i in nreal do
    ind := InducedClassFunction(n[i], to);
    # irreducible induction <=> the outer automorphism moves n[i]
    if ScalarProduct(to, ind, ind) = 1 then Add(fused, i); fi;
  od;
  Print("  non-real irreds FUSED by the outer coset : ", Length(fused),
        " of ", Length(nreal), "\n");
  if Length(fused) = Length(nreal) then
    Print("  -> EVERY complex character is fused.  sigma_S destroys the phase.  CONFIRMED\n\n");
  elif Length(fused) = 0 then
    Print("  -> NONE fused.  the phase SURVIVES the outer coset.  REFUTED at this q\n\n");
  else
    Print("  -> PARTIAL.  some survive.  claim needs restating.\n\n");
  fi;
end;

test("q = 3   PSp(4,3) < PGSp(4,3)", "S4(3)", "S4(3).2");
test("q = 5   PSp(4,5) < PGSp(4,5)", "S4(5)", "S4(5).2");
test("q = 7   PSp(4,7) < PGSp(4,7)", "S4(7)", "S4(7).2");
test("q = 11  PSp(4,11) < PGSp(4,11)", "S4(11)", "S4(11).2");

Print("=== done ===\n");
QUIT;
