LoadPackage("grape");;
WF4 := GO(1,4,3);;
subs := Filtered(ConjugacyClassesSubgroups(WF4), c -> Size(Representative(c)) = 576);;
repo := GAPInfo.SystemEnvironment.W33_REPO;;
f := OutputTextFile(Concatenation(repo, "/data/_gap_sub576.json"), false);;
SetPrintFormattingStatus(f, false);;
AppendTo(f, "{");
AppendTo(f, " \"n_classes_of_order_576_subgroups\": ", Length(subs), ",");
AppendTo(f, " \"structures\": [");
for i in [1..Length(subs)] do
  AppendTo(f, "\"", StructureDescription(Representative(subs[i])), "\"");
  if i < Length(subs) then AppendTo(f, ", "); fi;
od;
AppendTo(f, "],");
AppendTo(f, " \"centres\": [");
for i in [1..Length(subs)] do
  AppendTo(f, Size(Centre(Representative(subs[i]))));
  if i < Length(subs) then AppendTo(f, ", "); fi;
od;
AppendTo(f, "],");
AppendTo(f, " \"deriveds\": [");
for i in [1..Length(subs)] do
  AppendTo(f, Size(DerivedSubgroup(Representative(subs[i]))));
  if i < Length(subs) then AppendTo(f, ", "); fi;
od;
AppendTo(f, "]}");
CloseStream(f);;
