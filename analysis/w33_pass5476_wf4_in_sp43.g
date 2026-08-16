# Passes 5476-5479 -- is W(F4) a subgroup of Sp(4,3), and where do 96/192/384 land?
Sp43 := Sp(4,3);;
PSp43 := PSp(4,3);;
WF4 := GO(1,4,3);;
# Sp(4,3) acts on the 40 points of PG(3,3); that action IS W(3,3)'s point set.
orbs := Orbits(Sp43, NormedRowVectors(GF(3)^4), OnLines);;

# Does Sp(4,3) contain a subgroup isomorphic to W(F4)?  Search by order first.
cc := ConjugacyClassesSubgroups(Sp43);;
o1152 := Filtered(cc, c -> Size(Representative(c)) = 1152);;
o96  := Filtered(cc, c -> Size(Representative(c)) = 96);;
o192 := Filtered(cc, c -> Size(Representative(c)) = 192);;
o384 := Filtered(cc, c -> Size(Representative(c)) = 384);;
o576 := Filtered(cc, c -> Size(Representative(c)) = 576);;
isoWF4 := Filtered(o1152, c -> IsomorphismGroups(Representative(c), WF4) <> fail);;

repo := GAPInfo.SystemEnvironment.W33_REPO;;
f := OutputTextFile(Concatenation(repo, "/data/_gap_w33f4.json"), false);;
SetPrintFormattingStatus(f, false);;
AppendTo(f, "{\n");
AppendTo(f, "  \"Sp43_order\": ", Size(Sp43), ",\n");
AppendTo(f, "  \"PSp43_order\": ", Size(PSp43), ",\n");
AppendTo(f, "  \"WF4_order\": ", Size(WF4), ",\n");
AppendTo(f, "  \"index_if_subgroup\": ", Size(Sp43)/Size(WF4), ",\n");
AppendTo(f, "  \"point_orbit_sizes\": ", List(orbs, Length), ",\n");
AppendTo(f, "  \"n_classes_order_1152\": ", Length(o1152), ",\n");
AppendTo(f, "  \"n_classes_iso_WF4\": ", Length(isoWF4), ",\n");
AppendTo(f, "  \"n_classes_order_96\": ", Length(o96), ",\n");
AppendTo(f, "  \"n_classes_order_192\": ", Length(o192), ",\n");
AppendTo(f, "  \"n_classes_order_384\": ", Length(o384), ",\n");
AppendTo(f, "  \"n_classes_order_576\": ", Length(o576), ",\n");
if Length(isoWF4) > 0 then
  H := Representative(isoWF4[1]);;
  po := Orbits(H, NormedRowVectors(GF(3)^4), OnLines);;
  AppendTo(f, "  \"WF4_in_Sp43\": true,\n");
  AppendTo(f, "  \"WF4_orbits_on_40_points\": ", List(po, Length), "\n");
else
  AppendTo(f, "  \"WF4_in_Sp43\": false,\n");
  AppendTo(f, "  \"WF4_orbits_on_40_points\": []\n");
fi;
AppendTo(f, "}\n");
CloseStream(f);;
