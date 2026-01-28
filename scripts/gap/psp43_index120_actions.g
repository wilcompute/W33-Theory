Read("artifacts/we6_line_perms.g");
Gline := Group(List(WE6_LINE_PERMS, PermList));
G := PSp(4,3);
classes := ConjugacyClassesSubgroups(G);
Sn := SymmetricGroup(120);

matches := [];
checked := 0;
for c in classes do
  checked := checked + 1;
  H := Representative(c);
  if Index(G,H) = 120 then
    action := Action(G, RightCosets(G,H), OnRight);
    if IsConjugate(Sn, action, Gline) = true then
      Add(matches, checked);
    fi;
  fi;
od;

out := "{\"index120_classes_checked\":";
out := Concatenation(out, String(checked));
out := Concatenation(out, ",\"match_count\":");
out := Concatenation(out, String(Length(matches)));
out := Concatenation(out, ",\"matches\":[");
for i in [1..Length(matches)] do
  out := Concatenation(out, String(matches[i]));
  if i < Length(matches) then
    out := Concatenation(out, ",");
  fi;
od;
out := Concatenation(out, "]}");

PrintTo("artifacts/psp43_index120_actions.json", out);
Print("Wrote artifacts/psp43_index120_actions.json\n");
