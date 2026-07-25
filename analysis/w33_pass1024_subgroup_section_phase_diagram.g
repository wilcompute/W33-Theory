# Pass 1024: exact subgroup phase diagram for equivariant sections.
#
# The property "admits an equivariant section" is hereditary under passage to
# subgroups. This permits an exact branch-and-bound search down maximal-subgroup
# classes: once an admissible group is found, none of its descendants can improve
# its order; once a queued group is no larger than the current optimum, none of
# its descendants can improve it either.
#
# The search deduplicates by K-conjugacy and terminates only when every possible
# larger subgroup has been adjudicated. It therefore returns the exact maximum
# order of an admissible subgroup, not a random sample.

Read("analysis/w33_e8_c6_bundle_common.g");;

REPO1024 := GAPInfo.SystemEnvironment.W33_REPO;;
OUT1024 := Concatenation(REPO1024, "/data/w33_pass1024_subgroup_section_phase_diagram.json");;

Assert1024 := function(label, condition)
  if not condition then Error(Concatenation("Pass1024 assertion failed: ",label)); fi;
end;;

OrbitProfile1024 := function(group, fibres)
  return SortedList(List(Orbits(group,fibres,OnSets),Length));
end;;

SeenConjugate1024 := function(K, seen, group)
  return ForAny(seen, other -> Size(other)=Size(group) and IsConjugate(K,other,group));
end;;

UpdateHistogram1024 := function(histogram, order, admits, containsCenter)
  local row;
  row := First(histogram,item -> item[1]=order);
  if row=fail then
    row := [order,0,0,0,0];
    Add(histogram,row);
  fi;
  row[2] := row[2]+1;
  if admits then row[3] := row[3]+1; else row[4] := row[4]+1; fi;
  if containsCenter then row[5] := row[5]+1; fi;
end;;

JsonBool1024 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

Main1024 := function()
  local data, K, Z, H, pair, triple, fibre, P, T, L, trivial,
        sylow2, sylow3, sylow5, normalizer5, distinguished,
        maximalClasses, maximalRows, group, queue, seen, histogram,
        bestOrder, bestGroups, uniqueBest, initialAdmissible, index, sizes,
        candidate, admits, containsCenter, children, processed, nodeLimit,
        checks, names, stream, name, row;

  data := BuildE8C6Bundle102x();
  K := data.K;
  Z := data.center;
  pair := First(data.pairs,block -> 1 in block);
  triple := First(data.triples,block -> 1 in block);
  fibre := First(data.fibres,block -> 1 in block);
  H := Stabilizer(K,1);
  P := Stabilizer(K,pair,OnSets);
  T := Stabilizer(K,triple,OnSets);
  L := Stabilizer(K,fibre,OnSets);
  trivial := TrivialSubgroup(K);
  sylow2 := SylowSubgroup(K,2);
  sylow3 := SylowSubgroup(K,3);
  sylow5 := SylowSubgroup(K,5);
  normalizer5 := Normalizer(K,sylow5);

  distinguished := [
    ["trivial",trivial], ["center_C2",Z], ["root_stabilizer_H",H],
    ["pair_stabilizer_P",P], ["triple_stabilizer_T",T],
    ["point_stabilizer_L",L], ["Sylow2",sylow2], ["Sylow3",sylow3],
    ["Sylow5",sylow5], ["normalizer_Sylow5",normalizer5],
    ["derived_L",DerivedSubgroup(L)], ["derived_P",DerivedSubgroup(P)],
    ["derived_T",DerivedSubgroup(T)]
  ];

  initialAdmissible := Filtered(distinguished,row ->
    AdmitsPointSection102x(row[2],data.fibres));
  bestOrder := Maximum(List(initialAdmissible,row -> Size(row[2])));
  bestGroups := Filtered(List(initialAdmissible,row -> row[2]),
    group -> Size(group)=bestOrder);

  maximalClasses := MaximalSubgroupClassReps(K);
  maximalRows := List(maximalClasses,group -> [
    Size(group), Index(K,group), AdmitsPointSection102x(group,data.fibres),
    IsSubgroup(group,Z), OrbitProfile1024(group,data.fibres)
  ]);

  queue := ShallowCopy(maximalClasses);
  seen := [K];
  histogram := [];
  processed := 0;
  nodeLimit := 5000;

  while Length(queue)>0 do
    sizes := List(queue,Size);
    index := Position(sizes,Maximum(sizes));
    candidate := Remove(queue,index);
    if not SeenConjugate1024(K,seen,candidate) then
      Add(seen,candidate);
      if Size(candidate)>=bestOrder then
        processed := processed+1;
        if processed>nodeLimit then Error("Pass1024 node limit exceeded"); fi;
        admits := AdmitsPointSection102x(candidate,data.fibres);
        containsCenter := IsSubgroup(candidate,Z);
        UpdateHistogram1024(histogram,Size(candidate),admits,containsCenter);
        if admits then
          if Size(candidate)>bestOrder then
            bestOrder := Size(candidate);
            bestGroups := [candidate];
          elif Size(candidate)=bestOrder then
            Add(bestGroups,candidate);
          fi;
        elif Size(candidate)>bestOrder then
          children := MaximalSubgroupClassReps(candidate);
          Append(queue,children);
        fi;
      fi;
    fi;
  od;

  uniqueBest := [];
  for group in bestGroups do
    if not SeenConjugate1024(K,uniqueBest,group) then Add(uniqueBest,group); fi;
  od;
  bestGroups := uniqueBest;

  Sort(histogram,function(left,right) return left[1]>right[1]; end);

  checks := rec();
  checks.trivial_group_admits_section := AdmitsPointSection102x(trivial,data.fibres);
  checks.center_C2_is_a_minimal_obstruction :=
    not AdmitsPointSection102x(Z,data.fibres) and Size(Z)=2;
  checks.Sylow5_positive_witness_survives :=
    Size(sylow5)=5 and AdmitsPointSection102x(sylow5,data.fibres);
  checks.full_group_is_obstructed := not AdmitsPointSection102x(K,data.fibres);
  checks.maximal_subgroup_classes_were_found := Length(maximalClasses)>0;
  checks.maximal_rows_cover_all_maximal_classes := Length(maximalRows)=Length(maximalClasses);
  checks.branch_and_bound_processed_nodes := processed>0 and processed<=nodeLimit;
  checks.search_queue_exhausted := Length(queue)=0;
  checks.best_order_is_attained :=
    Length(bestGroups)>0 and ForAll(bestGroups,group ->
      Size(group)=bestOrder and AdmitsPointSection102x(group,data.fibres));
  checks.no_processed_larger_admissible_class_was_missed :=
    ForAll(histogram,row -> row[1]<=bestOrder or row[3]=0);
  checks.center_containment_is_sufficient_for_obstruction_on_registry :=
    ForAll(Concatenation(maximalClasses,List(distinguished,row -> row[2])),group ->
      not IsSubgroup(group,Z) or not AdmitsPointSection102x(group,data.fibres));
  checks.admissibility_is_hereditary_on_best_examples :=
    ForAll(bestGroups,group -> ForAll(MaximalSubgroupClassReps(group),subgroup ->
      AdmitsPointSection102x(subgroup,data.fibres)));

  names := RecNames(checks);
  Assert1024("all checks",ForAll(names,name -> checks.(name)));

  stream := OutputTextFile(OUT1024,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass1024.subgroup_section_phase_diagram.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"An exact maximal-subgroup branch-and-bound search determines the largest Sp(4,3) subgroups that admit a phase section. The central C2 supplies a minimal obstruction, and every center-containing class in the maximal and distinguished registry is obstructed.\",\n");
  WriteAll(stream,Concatenation("  \"maximal_class_count\": ",String(Length(maximalClasses)),",\n"));
  WriteAll(stream,"  \"maximal_classes\": [\n");
  for index in [1..Length(maximalRows)] do
    row := maximalRows[index];
    WriteAll(stream,Concatenation("    {\"order\":",String(row[1]),
      ",\"index\":",String(row[2]),",\"admits_section\":",JsonBool1024(row[3]),
      ",\"contains_center\":",JsonBool1024(row[4]),
      ",\"base_orbits\":",String(row[5]),"}"));
    if index<Length(maximalRows) then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  ],\n");
  WriteAll(stream,"  \"distinguished_registry\": [\n");
  for index in [1..Length(distinguished)] do
    row := distinguished[index];
    group := row[2];
    WriteAll(stream,Concatenation("    {\"name\":\"",row[1],"\",\"order\":",String(Size(group)),
      ",\"admits_section\":",JsonBool1024(AdmitsPointSection102x(group,data.fibres)),
      ",\"contains_center\":",JsonBool1024(IsSubgroup(group,Z)),
      ",\"base_orbits\":",String(OrbitProfile1024(group,data.fibres)),"}"));
    if index<Length(distinguished) then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  ],\n");
  WriteAll(stream,"  \"exact_optimum\": {\n");
  WriteAll(stream,Concatenation("    \"largest_admissible_order\": ",String(bestOrder),",\n"));
  WriteAll(stream,Concatenation("    \"conjugacy_classes_at_optimum\": ",String(Length(bestGroups)),",\n"));
  WriteAll(stream,Concatenation("    \"optimal_base_orbit_profiles\": ",String(List(bestGroups,group -> OrbitProfile1024(group,data.fibres))),",\n"));
  WriteAll(stream,Concatenation("    \"processed_conjugacy_classes\": ",String(processed),",\n"));
  WriteAll(stream,"    \"proof_method\": \"hereditary admissibility plus descending maximal-subgroup branch-and-bound\"\n");
  WriteAll(stream,"  },\n");
  WriteAll(stream,Concatenation("  \"order_histogram_rows\": ",String(histogram),",\n"));
  WriteAll(stream,"  \"histogram_columns\": [\"order\",\"classes_processed\",\"admissible\",\"obstructed\",\"contain_center\"],\n");
  WriteAll(stream,"  \"minimal_obstruction_witness\": {\"order\":2,\"group\":\"Z(Sp(4,3))=C2\",\"reason\":\"trivial on the base and antipodal upstairs\"},\n");
  WriteAll(stream,"  \"boundary\": \"The optimum is exact. The statement that the center is a minimal obstruction does not claim it is the only K-conjugacy class of obstructed involution subgroups.\",\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool102x(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass1024 status=PASS checks=",Length(names)," bestOrder=",bestOrder,
    " processed=",processed," output=",OUT1024,"\n");
end;;

Main1024();;
QUIT;
