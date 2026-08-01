# Passes 1615-1616 -- emit the machine-checkable certificate as JSON.
# Same construction as w33_pass1615_1616_the_chirality_is_not_removable.g and
# w33_pass1616_completeness_and_the_cancelling_signs.g; this file only serialises.

Sp4 := Sp(4,3);;
J   := InvariantBilinearForm(Sp4).matrix;;
N   := Normalizer(GL(4,3), Sp4);;
pts := AsSortedList(Orbit(N, NormedRowVector(One(GF(3)) * [1,0,0,0]), OnLines));;
hom := ActionHomomorphism(N, pts, OnLines);;
G   := Image(hom);;  D := DerivedSubgroup(G);;

edges := [];;
for i in [1..40] do for j in [i+1..40] do
  if IsZero(pts[i] * J * pts[j]) then Add(edges, [i,j]); fi;
od; od;

SignedTrace := function(g)
  local t, e, a, b;  t := 0;
  for e in edges do
    a := e[1]^g; b := e[2]^g;
    if a = e[1] and b = e[2] then t := t + 1;
    elif a = e[2] and b = e[1] then t := t - 1; fi;
  od;
  return t;
end;;

ccl := ConjugacyClasses(G);;  reps := List(ccl, Representative);;
vals := List(reps, SignedTrace);;
chi := ClassFunction(G, vals);;  irr := Irr(G);;
eps := First(irr, x -> x[1] = 1 and x <> TrivialCharacter(G));;
tw  := chi * eps;;
A   := AutomorphismGroup(G);;
blocks := Filtered([1..Length(irr)], k -> ScalarProduct(chi, irr[k]) <> 0);;
sep := Filtered([1..Length(ccl)], c -> vals[c] <> tw[c]);;
canc := Filtered([1..Length(ccl)],
          c -> vals[c] = tw[c] and
               ForAny(blocks, k -> irr[k][c] <> (irr[k]*eps)[c]));;
irrD := Irr(D);;
d30  := Filtered([1..Length(irrD)], t -> irrD[t][1] = 30);;

fh := OutputTextFile("C:/Repos/Theory of Everything/data/w33_pass1615_1616_chirality.json", false);;
SetPrintFormattingStatus(fh, false);   # GAP otherwise wraps at 80 cols with a
                                       # backslash -- an illegal JSON escape.
Pr := function(s) AppendTo(fh, s); end;;
Pr("{\n");
Pr(Concatenation("  \"group_order\": ", String(Size(G)), ",\n"));
Pr(Concatenation("  \"derived_order\": ", String(Size(D)), ",\n"));
Pr(Concatenation("  \"aut_order\": ", String(Size(A)), ",\n"));
Pr(Concatenation("  \"is_complete\": ",
   String(Size(A) = Size(G) and IsTrivial(Centre(G))), ",\n"));
Pr(Concatenation("  \"dim_signed_edge_module\": ", String(vals[1]), ",\n"));
Pr("  \"constituents\": [");
Pr(JoinStringsWithSeparator(List(blocks, k -> Concatenation(
   "{\"irr\": ", String(k), ", \"degree\": ", String(irr[k][1]),
   ", \"eps_stable\": ", String(irr[k]*eps = irr[k]), "}")), ", "));
Pr("],\n");
Pr(Concatenation("  \"V_is_chiral\": ", String(tw <> chi), ",\n"));
Pr("  \"separating_classes\": [");
Pr(JoinStringsWithSeparator(List(sep, c -> Concatenation(
   "{\"class\": ", String(c), ", \"element_order\": ", String(Order(reps[c])),
   ", \"size\": ", String(Size(ccl[c])), ", \"chi\": ", String(vals[c]),
   ", \"inner\": ", String(reps[c] in D), "}")), ", "));
Pr("],\n");
Pr(Concatenation("  \"cancelling_classes\": ", String(canc), ",\n"));
Pr(Concatenation("  \"n_separating\": ", String(Length(sep)),
   ", \"n_cancelling\": ", String(Length(canc)), ",\n"));
Pr(Concatenation("  \"psp_degree30_irrs\": ", String(d30), ",\n"));
Pr("  \"degree30_and_60_restrictions\": [");
Pr(JoinStringsWithSeparator(List(Filtered([1..Length(irr)],
   k -> irr[k][1] in [30,60]), k -> Concatenation(
   "{\"irr\": ", String(k), ", \"degree\": ", String(irr[k][1]),
   ", \"psp30_constituents\": ", String(Filtered(d30,
       t -> ScalarProduct(RestrictedClassFunction(irr[k], D), irrD[t]) <> 0)),
   ", \"eps_stable\": ", String(irr[k]*eps = irr[k]), "}")), ", "));
Pr("]\n}\n");

CloseStream(fh);
Print("wrote data/w33_pass1615_1616_chirality.json\n");
QUIT;
