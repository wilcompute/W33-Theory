# Pass 1079 CORRECTION: recount the orbital pairing with a test that is not vacuous.
#
# Pass 1079 reported "all 32 orbitals self-paired".  That check was a TAUTOLOGY:
#
#     if p <> fail and 1 in Orbit(Stabilizer(FR, rep), 1 ^ (p^0)) then
#
# `p^0` is the IDENTITY permutation, so `1 ^ (p^0)` is 1, and the condition reads
# "is 1 in the orbit of 1?" -- true for every rep.  The correct test sat in the
# `else` branch and was therefore never reached.
#
# The parallel track's Pass 1082/1091 independently reports an `innerTranspose`
# involution on the 32 orbitals with 12 fixed points and 20 moved (10 pairs).
# That contradicts "all 32 self-paired", and they are right: a self-paired orbital
# is one where some g maps the ordered pair (1, rep) to (rep, 1), which is exactly
# the `else` branch that never ran.
#
# This script recomputes the pairing with only the correct test and prints the
# counts so the two tracks can be compared as data.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
DIAG := Concatenation(REPO, "/data/w33_pass1079_pairing_recount.txt");;

Main := function()
  local S, J, pts, act, P, lines, sp, L, i, j, spreads, onpt, FindSpreads,
        frames, lineAct, PL, frAct, FR, stab, subs, rep, k,
        selfPaired, nonSelfPaired, selfSizes, nonSizes, stream;

  S := Sp(4,3);
  J := InvariantBilinearForm(S).matrix;
  pts := NormedRowVectors(GF(3)^4);
  act := ActionHomomorphism(S, pts, OnLines);
  P := Image(act);

  lines := [];
  for sp in Subspaces(GF(3)^4, 2) do
    L := BasisVectors(Basis(sp));
    if IsZero(L[1] * J * L[2]) then
      Add(lines, Set(Filtered([1..40], k -> pts[k] in sp)));
    fi;
  od;
  lines := Set(lines);
  onpt := List([1..40], p2 -> Filtered([1..40], li -> p2 in lines[li]));

  spreads := [];
  FindSpreads := function(chosen, used)
    local pmin, li;
    if Length(used) = 40 then Add(spreads, Set(chosen)); return; fi;
    pmin := First([1..40], x -> not (x in used));
    for li in onpt[pmin] do
      if IsEmpty(Intersection(lines[li], used)) then
        FindSpreads(Concatenation(chosen, [li]), Union(used, lines[li]));
      fi;
    od;
  end;;
  FindSpreads([], []);

  frames := [];
  for i in [1..40] do
    for j in [i+1..40] do
      if IsEmpty(Intersection(lines[i], lines[j])) then Add(frames, [i,j]); fi;
    od;
  od;

  lineAct := ActionHomomorphism(P, lines, OnSets);
  PL := Image(lineAct);
  frAct := ActionHomomorphism(PL, frames, OnSets);
  FR := Image(frAct);
  stab := Stabilizer(FR, 1);
  subs := Orbits(stab, [1..540]);

  # THE ONLY CORRECT TEST: the orbital through (1, rep) is self-paired iff some
  # group element carries the ORDERED pair (1, rep) to (rep, 1).
  selfPaired := 0; nonSelfPaired := 0; selfSizes := []; nonSizes := [];
  for k in [1..Length(subs)] do
    rep := subs[k][1];
    if rep = 1 then
      selfPaired := selfPaired + 1; Add(selfSizes, Length(subs[k]));
    elif RepresentativeAction(FR, [1, rep], [rep, 1], OnTuples) <> fail then
      selfPaired := selfPaired + 1; Add(selfSizes, Length(subs[k]));
    else
      nonSelfPaired := nonSelfPaired + 1; Add(nonSizes, Length(subs[k]));
    fi;
  od;

  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, Concatenation("rank = ", String(Length(subs)), "\n"));
  WriteAll(stream, Concatenation("self-paired = ", String(selfPaired), "\n"));
  WriteAll(stream, Concatenation("non-self-paired = ", String(nonSelfPaired), "\n"));
  WriteAll(stream, Concatenation("pairs among non-self-paired = ",
    String(nonSelfPaired / 2), "\n"));
  WriteAll(stream, Concatenation("orbital-pair count = ",
    String(selfPaired + nonSelfPaired / 2), "\n"));
  WriteAll(stream, Concatenation("self-paired sizes = ", String(SortedList(selfSizes)), "\n"));
  WriteAll(stream, Concatenation("non-self-paired sizes = ", String(SortedList(nonSizes)), "\n"));
  CloseStream(stream);

  Print("rank=", Length(subs), " self=", selfPaired, " nonself=", nonSelfPaired,
        " pairs=", selfPaired + nonSelfPaired / 2, "\n");
end;;

Main();;
QUIT;
