Read("artifacts/edge_perms.g");
Gedge := Group(List(EDGE_PERMS, PermList));
G := PSp(4,3);
classes := ConjugacyClassesSubgroups(G);
Sn := SymmetricGroup(240);

matches := [];
checked := 0;
count := Length(classes);
for c in classes do
  checked := checked + 1;
  H := Representative(c);
  if Index(G,H) = 240 then
    action := Action(G, RightCosets(G,H), OnRight);
    if IsConjugate(Sn, action, Gedge) = true then
      Add(matches, checked);
    fi;
  fi;
od;

out := "{\"classes_checked\":";
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

PrintTo("artifacts/psp43_index240_actions.json", out);
Print("Wrote artifacts/psp43_index240_actions.json\n");
