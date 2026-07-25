# Pass 1022 diagnostic certificate.
#
# This branch intentionally emits every computed invariant before deciding which
# theorem statement survives. GAP batch mode can exit zero after an internal
# Error(), so the diagnostic certificate must be written without a final assert.

REPO1022 := GAPInfo.SystemEnvironment.W33_REPO;;
OUT1022 := Concatenation(REPO1022, "/data/w33_pass1022_equivariant_section_obstruction.json");;

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
        checks, names, stream, name, allPass, status, monodromyStructure;

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
  cox := Product(List(simples, ReflPerm));
  omega := cox ^ 10;
  C := Centralizer(W, omega);
  K := DerivedSubgroup(C);

  negPerm := PermList(List(roots, x -> rootIndex(-x)));
  unitGroup := Group(cox ^ 5);

  block6 := First(AllBlocks(K), b -> Length(b) = 6);
  fibres := Blocks(K, [1..240], block6);
  fibre := First(fibres, b -> 1 in b);
  hom40 := ActionHomomorphism(K, fibres, OnSets);
  baseKernel := Kernel(hom40);

  L := Stabilizer(K, fibre, OnSets);
  H := Stabilizer(K, 1);
  fibreHom := ActionHomomorphism(L, fibre, OnPoints);
  monodromy := Image(fibreHom);
  monodromyStructure := "order6_noncyclic";
  if Size(monodromy) = 6 and IsCyclic(monodromy) then
    monodromyStructure := "C6";
  fi;
  fixedByL := FixedRoots1022(L, fibre);

  Z := Center(K);
  sylow5 := SylowSubgroup(K, 5);
  sylow5Orbits := Orbits(sylow5, fibres, OnSets);
  sylow5Semiregular := ForAll(sylow5Orbits, orb -> Length(orb) = 5);

  checks := rec();
  checks.root_count_240 := Length(roots) = 240;
  checks.WE8_order := Size(W) = 696729600;
  checks.coxeter_order_30 := Order(cox) = 30;
  checks.K_order_51840 := Size(K) = 51840;
  checks.unit_group_order_six := Size(unitGroup) = 6;
  checks.forty_fibres_of_six := Length(fibres) = 40 and
    ForAll(fibres, b -> Length(b) = 6);
  checks.root_stabiliser_order_216 := Size(H) = 216;
  checks.point_stabiliser_order_1296 := Size(L) = 1296;
  checks.root_stabiliser_is_subgroup_of_point_stabiliser := IsSubgroup(L, H);
  checks.local_index_is_six := IsSubgroup(L, H) and Index(L, H) = 6;
  checks.root_stabiliser_is_normal_in_point_stabiliser := IsNormal(L, H);
  checks.phase_action_has_order_six := Size(monodromy) = 6;
  checks.phase_action_is_cyclic := IsCyclic(monodromy);
  checks.phase_action_is_transitive := IsTransitive(monodromy, [1..6]);
  checks.phase_action_is_regular := Size(monodromy) = 6 and
    IsTransitive(monodromy, [1..6]);
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
  status := "DIAGNOSTIC_FAIL";
  if allPass then status := "PASS"; fi;

  stream := OutputTextFile(OUT1022, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, Concatenation("  \"schema\": \"w33.pass1022.equivariant_section_obstruction.diagnostic.gap.v1\",\n  \"status\": \"", status, "\",\n"));
  WriteAll(stream, "  \"raw\": {\n");
  WriteAll(stream, Concatenation("    \"root_count\": ", String(Length(roots)), ",\n"));
  WriteAll(stream, Concatenation("    \"WE8_order\": ", String(Size(W)), ",\n"));
  WriteAll(stream, Concatenation("    \"K_order\": ", String(Size(K)), ",\n"));
  WriteAll(stream, Concatenation("    \"fibre_count\": ", String(Length(fibres)), ",\n"));
  WriteAll(stream, Concatenation("    \"fibre_size\": ", String(Length(fibre)), ",\n"));
  WriteAll(stream, Concatenation("    \"root_stabiliser_order\": ", String(Size(H)), ",\n"));
  WriteAll(stream, Concatenation("    \"point_stabiliser_order\": ", String(Size(L)), ",\n"));
  WriteAll(stream, Concatenation("    \"H_is_subgroup_of_L\": ", Bool1022(IsSubgroup(L, H)), ",\n"));
  WriteAll(stream, Concatenation("    \"H_is_normal_in_L\": ", Bool1022(IsNormal(L, H)), ",\n"));
  WriteAll(stream, Concatenation("    \"monodromy_order\": ", String(Size(monodromy)), ",\n"));
  WriteAll(stream, Concatenation("    \"monodromy_structure\": \"", monodromyStructure, "\",\n"));
  WriteAll(stream, Concatenation("    \"monodromy_transitive\": ", Bool1022(IsTransitive(monodromy, [1..6])), ",\n"));
  WriteAll(stream, Concatenation("    \"fibre_kernel_order\": ", String(Size(Kernel(fibreHom))), ",\n"));
  WriteAll(stream, Concatenation("    \"fixed_roots_under_L\": ", String(fixedByL), ",\n"));
  WriteAll(stream, Concatenation("    \"base_kernel_order\": ", String(Size(baseKernel)), ",\n"));
  WriteAll(stream, Concatenation("    \"center_order\": ", String(Size(Z)), ",\n"));
  WriteAll(stream, Concatenation("    \"Sylow5_base_orbit_lengths\": ", String(SortedList(List(sylow5Orbits, Length))), "\n"));
  WriteAll(stream, "  },\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n  \"checks\": {\n"));
  for name in names do
    WriteAll(stream, Concatenation("    \"", name, "\": ", Bool1022(checks.(name))));
    if name <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);

  Print("Pass1022 diagnostic status=", status, " checks=", Length(names), "\n");
end;;

Main1022();;
QUIT;
