# Pass 8030 -- export a fixed-point-free order-3 element of Co0 = 2.Co1.
#
# WHY. Pass 8022-8029 corrected a filter of mine that had deleted rungs of the Leech
# quotient tower for a reason that was never about the form. The same filter deleted d=3.
# But analysis/w33_complex_leech_suzuki_chain.py already records that Leech HAS a
# fixed-point-free order-3 automorphism -- that is exactly what makes the COMPLEX Leech
# lattice a rank-12 Z[omega] module with Aut = 6.Suz. So the d=3 rung should be real, and
# the purity theorem (other lane, Pass7973-7980) predicts the quotient is F_3^12, i.e.
# W(11,3): SIX QUTRITS.
#
# THE TEST, and why it is cheap. Wanted: char poly Phi_3^12. Since the representation is
# 24-dimensional and deg Phi_3 = 2, it is enough that the MINIMAL polynomial be Phi_3, i.e.
#
#     W^2 + W + I = 0
#
# which is a matrix identity, not a 24x24 determinant. That is far cheaper than testing
# det(I-W) = 3^12 on every candidate, and it implies it.
#
# TWO TRAPS, both paid for already and not repeated:
#   * GAP's String() line-wraps with a trailing backslash that can split a TOKEN; a minus
#     sign left at a line end parses away and silently flips a sign. Write FLAT via
#     OutputTextFile with SetPrintFormattingStatus false.
#   * GAP's working directory is NOT the repo, so a relative OutputTextFile silently
#     returns fail. Build absolute paths from W33_REPO. And stdout does not survive the
#     hand-off, so every diagnostic goes to the log file.

repo := GAPInfo.SystemEnvironment.W33_REPO;;
log  := Concatenation(repo, "/analysis/_co0_M3_log.txt");;
PrintTo(log, "start\n");

LoadPackage("atlasrep");;
gens := AtlasGenerators("2.Co1", 9).generators;;
AppendTo(log, "generators ", Length(gens), " dim ", Length(gens[1]), "\n");

I24 := IdentityMat(24);;
found := fail;;
rs := RandomSource(IsMersenneTwister, 20260823);;

i := 0;;
while i < 6000 and found = fail do
  i := i + 1;
  w := One(gens[1]);
  for j in [1..10] do
    w := w * gens[Random(rs, [1..Length(gens)])];
  od;
  o := Order(w);
  if o mod 3 = 0 then
    x := w^(o/3);
    if x * x + x + I24 = 0 * I24 then
      found := x;
      AppendTo(log, "FOUND at word ", i, " trace ", TraceMat(x), "\n");
    fi;
  fi;
  if i mod 250 = 0 then
    AppendTo(log, "  searched ", i, "\n");
  fi;
od;

if found = fail then
  AppendTo(log, "NONE found in 6000 words\n");
else
  AppendTo(log, "det(I-W) ", DeterminantMat(I24 - found), " want ", 3^12, "\n");
  f := OutputTextFile(Concatenation(repo, "/analysis/_co0_M3.txt"), false);;
  SetPrintFormattingStatus(f, false);
  for r in found do
    for c in r do
      PrintTo(f, c, " ");
    od;
    PrintTo(f, "\n");
  od;
  CloseStream(f);
  AppendTo(log, "wrote _co0_M3.txt\n");
fi;

QUIT;
