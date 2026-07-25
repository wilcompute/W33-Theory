# Pass 1022 diagnostic build: compute and emit the section-obstruction data
# before applying any theorem-level assertion. This version exists on the CI
# verification branch so GAP batch-mode errors cannot hide the last completed
# stage. The final master version restores the fail-closed assertion firewall.

REPO1022 := GAPInfo.SystemEnvironment.W33_REPO;;
OUT1022 := Concatenation(REPO1022, "/data/w33_pass1022_equivariant_section_obstruction.json");;
PROBE1022 := Concatenation(REPO1022, "/data/w33_pass1022_probe.txt");;
PrintTo(PROBE1022, "Pass1022 probe start\n");;

Probe1022 := function(message)
  AppendTo(PROBE1022, message, "\n");
end;;

Bool1022 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

FixedRoots1022 := function(J, fibre)
  local gens;
  gens := GeneratorsOfGroup(J);
  return Filtered(fibre, r -> ForAll(gens, g -> r ^ g = r));
end;;

AdmitsSection1022 := function(J, fibres)
  local orbs, orb, fibre, st;
  orbs := Orbits(J, fibres, OnSets);
  for orb in orbs do
    fibre := orb[1];
    st := Stabilizer(J, fibre, OnSets);
    if Length(FixedRoots1022(st, fibre)) = 0 then return false; fi;
  od;
  return true;
end;;

Main1022 := function()
  local roots, v, i, j, si, sj, m, k, ReflPerm, simples, rootIndex,
        W, cox, omega, C, K, negPerm, unitGroup, block6, fibres, fibre,
        hom40, baseKernel, L, H, fibreHom, monodromy, fixedByL,
        Z, sylow5, sylow5Orbits, sylow5Semiregular,
        checks, names, stream, name, allPass, monodromyStructure;

  roots := [];
  for i in [1..8] do
    for j in [i+1..8] do
      for si in [1,-1] do
        for sj in [1,-1] do
          v := ListWithIdenticalEntries(8, 0);
          v[i] := 2*si; v[j] := 2*sj;
          Add(roots, v);
        od;
      od;
    od;
  od;
  for m in [0..255] do
    v := List([0..7], k -> (-1)^(QuoInt(m, 2^k) mod 2));
    if Number(v, x -> x = -1) mod 2 = 0 then Add(roots, v); fi;
  od;
  Probe1022(Concatenation("roots=", String(Length(roots))));

  rootIndex := function(x) return Position(roots, x); end;
  ReflPerm := function(r)
    return PermList(List(roots, x -> rootIndex(x - ((x * r) / 4) * r)));
  end;
  simples := [
    [ 1,-1,-1,-1,-1,-1,-1, 1], [ 2, 2, 0, 0, 0, 0, 0, 0],
    [-2, 2, 0, 0, 0, 0, 0, 0], [ 0,-2, 2, 0, 0, 0, 0, 0],
    [ 0, 0,-2, 2, 0, 0, 0, 0], [ 0, 0, 0,-2, 2, 0, 0, 0],
    [ 0, 0, 0, 0,-2, 2, 0, 0], [ 0, 0, 0, 0, 0,-2, 2, 0] ];
  W := Group(List(simples, ReflPerm));
  Probe1022(Concatenation("W=", String(Size(W))));

  cox := Product(List(simples, ReflPerm));
  omega := cox ^ 10;
  C := Centralizer(W, omega);
  K := DerivedSubgroup(C);
  Probe1022(Concatenation("cox=", String(Order(cox)), " C=", String(Size(C)),
    " K=", String(Size(K))));

  negPerm := PermList(List(roots, x -> rootIndex(-x)));
  unitGroup := Group(cox ^ 5);
  Probe1022(Concatenation("unitGroup=", String(Size(unitGroup)), " ",
    StructureDescription(unitGroup)));

  block6 := First(AllBlocks(K), b -> Length(b) = 6);
  Probe1022(Concatenation("block6=", String(block6)));
  fibres := Blocks(K, [1..240], block6);
  fibre := First(fibres, b -> 1 in b);
  Probe1022(Concatenation("fibres=", String(Length(fibres)), " fibre=", String(fibre)));

  hom40 := ActionHomomorphism(K, fibres, OnSets);
  baseKernel := Kernel(hom40);
  Probe1022(Concatenation("baseKernel=", String(Size(baseKernel))));

  L := Stabilizer(K, fibre, OnSets);
  H := Stabilizer(K, 1);
  Probe1022(Concatenation("L=", String(Size(L)), " H=", String(Size(H)),
    " H<=L=", Bool1022(IsSubgroup(L, H))));

  fibreHom := ActionHomomorphism(L, fibre, OnPoints);
  monodromy := Image(fibreHom);
  monodromyStructure := StructureDescription(monodromy);
  fixedByL := FixedRoots1022(L, fibre);
  Probe1022(Concatenation("monodromy=", String(Size(monodromy)), " ",
    monodromyStructure, " fixed=", String(fixedByL), " kernel=",
    String(Size(Kernel(fibreHom)))));

  Z := Center(K);
  sylow5 := SylowSubgroup(K, 5);
  sylow5Orbits := Orbits(sylow5, fibres, OnSets);
  sylow5Semiregular := ForAll(sylow5Orbits, orb -> Length(orb) = 5);
  Probe1022(Concatenation("Z=", String(Size(Z)), " Sylow5=", String(Size(sylow5)),
    " orbits=", String(SortedList(List(sylow5Orbits, Length)))));

  checks := rec();
  checks.root_stabiliser_order_216 := Size(H) = 216;
  checks.point_stabiliser_order_1296 := Size(L) = 1296;
  checks.local_index_is_six := IsSubgroup(L, H) and Index(L, H) = 6;
  checks.root_stabiliser_is_normal_in_point_stabiliser := IsNormal(L, H);
  checks.phase_action_has_order_six := Size(monodromy) = 6;
  checks.phase_action_is_cyclic := IsCyclic(monodromy);
  checks.phase_action_is_transitive := IsTransitive(monodromy, [1..6]);
  checks.phase_action_is_regular := Size(monodromy) = 6 and IsTransitive(monodromy, [1..6]);
  checks.phase_kernel_is_root_stabiliser := Kernel(fibreHom) = H;
  checks.point_stabiliser_has_no_fixed_phase := Length(fixedByL) = 0;
  checks.no_full_equivariant_section := not AdmitsSection1022(K, fibres);
  checks.base_kernel_is_central_involution := Size(baseKernel) = 2 and
    baseKernel = Z and baseKernel = Group(negPerm);
  checks.central_involution_is_free_upstairs := ForAll([1..240], i -> i ^ negPerm <> i);
  checks.center_subgroup_is_obstructed := not AdmitsSection1022(Z, fibres);
  checks.sylow5_has_order_five := Size(sylow5) = 5;
  checks.sylow5_is_semiregular_on_base := sylow5Semiregular;
  checks.sylow5_admits_section := AdmitsSection1022(sylow5, fibres);
  checks.unit_group_centralises_K := ForAll(GeneratorsOfGroup(K),
    g -> Comm(g, cox ^ 5) = One(K));

  names := RecNames(checks);
  allPass := ForAll(names, name -> checks.(name));
  Probe1022(Concatenation("allPass=", Bool1022(allPass), " checks=", String(checks)));

  stream := OutputTextFile(OUT1022, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, Concatenation("  \"schema\": \"w33.pass1022.equivariant_section_obstruction.gap.v1\",\n  \"status\": \"", If(allPass, "PASS", "DIAGNOSTIC_FAIL"), "\",\n"));
  WriteAll(stream, "  \"headline\": \"Six-phase equivariant section obstruction diagnostic\",\n");
  WriteAll(stream, "  \"exact_sequence\": {\n");
  WriteAll(stream, Concatenation("    \"root_stabiliser_order\": ", String(Size(H)), ",\n"));
  WriteAll(stream, Concatenation("    \"point_stabiliser_order\": ", String(Size(L)), ",\n"));
  WriteAll(stream, Concatenation("    \"quotient_order\": ", String(Size(monodromy)), ",\n"));
  WriteAll(stream, Concatenation("    \"quotient_structure\": \"", monodromyStructure, "\"\n  },\n"));
  WriteAll(stream, "  \"section_obstruction\": {\n");
  WriteAll(stream, Concatenation("    \"full_group_admits_section\": ", Bool1022(AdmitsSection1022(K, fibres)), ",\n"));
  WriteAll(stream, Concatenation("    \"fixed_phases_under_point_stabiliser\": ", String(Length(fixedByL)), "\n  },\n"));
  WriteAll(stream, "  \"witnesses\": {\n");
  WriteAll(stream, Concatenation("    \"center_C2_admits_section\": ", Bool1022(AdmitsSection1022(Z, fibres)), ",\n"));
  WriteAll(stream, Concatenation("    \"Sylow5_admits_section\": ", Bool1022(AdmitsSection1022(sylow5, fibres)), ",\n"));
  WriteAll(stream, Concatenation("    \"Sylow5_base_orbit_lengths\": ", String(SortedList(List(sylow5Orbits, Length))), "\n  },\n"));
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n  \"checks\": {\n"));
  for name in names do
    WriteAll(stream, Concatenation("    \"", name, "\": ", Bool1022(checks.(name))));
    if name <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Probe1022("certificate written");
  Print("Pass1022 diagnostic status=", If(allPass, "PASS", "DIAGNOSTIC_FAIL"), "\n");
end;;

Main1022();;
QUIT;
