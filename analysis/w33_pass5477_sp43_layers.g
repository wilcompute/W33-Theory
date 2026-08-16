Sp43 := Sp(4,3);;
WF4 := GO(1,4,3);;
cc := ConjugacyClassesSubgroups(Sp43);;
pick := function(n) return List(Filtered(cc, c -> Size(Representative(c)) = n), Representative); end;;
repo := GAPInfo.SystemEnvironment.W33_REPO;;
f := OutputTextFile(Concatenation(repo, "/data/_gap_sp43layers.json"), false);;
SetPrintFormattingStatus(f, false);;
AppendTo(f, "{");
for n in [96, 192, 384, 576, 1152] do
  reps := pick(n);
  AppendTo(f, " \"order_", n, "\": [");
  for i in [1..Length(reps)] do
    AppendTo(f, "{\"structure\": \"", StructureDescription(reps[i]),
             "\", \"orbits_on_40\": ", List(Orbits(reps[i], NormedRowVectors(GF(3)^4), OnLines), Length),
             ", \"iso_WF4\": ", IsomorphismGroups(reps[i], WF4) <> fail, "}");
    if i < Length(reps) then AppendTo(f, ", "); fi;
  od;
  AppendTo(f, "],");
od;
AppendTo(f, " \"WF4_structure\": \"", StructureDescription(WF4), "\"}");
CloseStream(f);;
