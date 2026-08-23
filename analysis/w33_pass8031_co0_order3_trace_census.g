# Pass 8031 -- diagnostic: which order-3 classes does random word search actually reach?
#
# Pass 8030 found no element with W^2+W+I = 0 in 6000 random words. That is an INCOMPLETE
# SEARCH, not an absence proof, and the distinction has cost this repo real passes before.
# The fixed-point-free order-3 automorphism of Leech certainly exists -- it is what makes
# the complex Leech lattice a rank-12 Z[omega] module with Aut = 6.Suz.
#
# So: census the TRACES of the order-3 elements the search does reach. The fixed-point-free
# class has trace -12 (twelve conjugate pairs of primitive cube roots, each summing to -1).
# If -12 never appears, random words are not reaching that class and class representatives
# are needed; if it appears rarely, the search simply needs to be longer.

repo := GAPInfo.SystemEnvironment.W33_REPO;;
log  := Concatenation(repo, "/analysis/_co0_M3_census.txt");;
PrintTo(log, "order-3 trace census\n");

LoadPackage("atlasrep");;
gens := AtlasGenerators("2.Co1", 9).generators;;
I24 := IdentityMat(24);;
rs := RandomSource(IsMersenneTwister, 777);;

traces := [];;
n3 := 0;;
best := fail;;
i := 0;;
while i < 4000 do
  i := i + 1;
  w := One(gens[1]);
  for j in [1..10] do
    w := w * gens[Random(rs, [1..Length(gens)])];
  od;
  o := Order(w);
  if o mod 3 = 0 then
    x := w^(o/3);
    n3 := n3 + 1;
    t := TraceMat(x);
    Add(traces, t);
    if t = -12 and best = fail then
      best := x;
      AppendTo(log, "trace -12 first seen at word ", i, "\n");
      AppendTo(log, "  minpoly test W^2+W+I = 0 : ", x * x + x + I24 = 0 * I24, "\n");
    fi;
  fi;
od;

AppendTo(log, "words ", i, "  order-3 elements ", n3, "\n");
AppendTo(log, "distinct traces ", SortedList(Set(traces)), "\n");
for t in SortedList(Set(traces)) do
  AppendTo(log, "  trace ", t, " count ", Number(traces, s -> s = t), "\n");
od;

if best <> fail then
  AppendTo(log, "det(I-W) ", DeterminantMat(I24 - best), " want ", 3^12, "\n");
  f := OutputTextFile(Concatenation(repo, "/analysis/_co0_M3.txt"), false);;
  SetPrintFormattingStatus(f, false);
  for r in best do
    for c in r do
      PrintTo(f, c, " ");
    od;
    PrintTo(f, "\n");
  od;
  CloseStream(f);
  AppendTo(log, "wrote _co0_M3.txt\n");
else
  AppendTo(log, "trace -12 NOT reached by random words\n");
fi;

QUIT;
