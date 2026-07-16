# Pass 358: exact GAP integrity audit of the 2026-07-15 GitHub batch.
#
# This witness separates three groups of order 51840, identifies the ordinary
# complex Weil sectors in CTblLib, closes their outer-stable envelope, restores
# the Chandler--Sin--Xiang p=5 polynomial, settles the q=7 order question, and
# checks the order mismatch in the proposed reflection-to-transvection map.

OUT358 := "data/w33_pass358_github_batch_integrity_audit.json";;

Assert358 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass358 assertion failed: ", label));
  fi;
end;;

Bool358 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

Main358 := function()
  local tableSp, tableW, tableOuter, irrSp, irrW, irrOuter,
        indicatorsSp, indicatorsW, fusions, fusion, values10, values8,
        restricted10, restricted8, multiplicities10, multiplicities8,
        support10, support8, groupSp, p, trace5, determinant5,
        discriminant5, order3089, field3, zero3, one3, unipotent,
        omega, checks, names, stream, name;

  Assert358("CTblLib loads",LoadPackage("ctbllib")<>fail);

  tableSp := CharacterTable("2.U4(2)");
  tableW := CharacterTable("W(E6)");
  tableOuter := CharacterTable("2.U4(2).2");
  irrSp := Irr(tableSp);
  irrW := Irr(tableW);
  irrOuter := Irr(tableOuter);
  indicatorsSp := Indicator(tableSp,2);
  indicatorsW := Indicator(tableW,2);

  fusions := PossibleClassFusions(tableSp,tableOuter);
  fusion := fusions[1];

  values10 := List([1..Length(fusion)],position -> irrOuter[3][fusion[position]]);
  restricted10 := ClassFunction(tableSp,values10);
  multiplicities10 := List(irrSp,character ->
    ScalarProduct(tableSp,restricted10,character));
  support10 := Filtered([1..Length(multiplicities10)],position ->
    multiplicities10[position]<>0);

  values8 := List([1..Length(fusion)],position -> irrOuter[26][fusion[position]]);
  restricted8 := ClassFunction(tableSp,values8);
  multiplicities8 := List(irrSp,character ->
    ScalarProduct(tableSp,restricted8,character));
  support8 := Filtered([1..Length(multiplicities8)],position ->
    multiplicities8[position]<>0);

  groupSp := Sp(4,3);
  p := 5;
  trace5 := p*(p+1)^2/2;
  determinant5 := -p^2*(p+1)^2*(2*p^2-13*p+2)/36;
  discriminant5 := trace5^2-4*determinant5;
  order3089 := OrderMod(2,3089);

  field3 := GF(3);
  zero3 := Zero(field3);
  one3 := One(field3);
  unipotent := [
    [one3,one3,zero3,zero3],
    [zero3,one3,zero3,zero3],
    [zero3,zero3,one3,zero3],
    [zero3,zero3,-one3,one3]
  ];
  omega := [
    [zero3,zero3,one3,zero3],
    [zero3,zero3,zero3,one3],
    [-one3,zero3,zero3,zero3],
    [zero3,-one3,zero3,zero3]
  ];

  checks := rec();
  checks.sp_table_order_is_51840 := Size(tableSp)=51840;
  checks.we6_table_order_is_51840 := Size(tableW)=51840;
  checks.outer_signed_table_order_is_103680 := Size(tableOuter)=103680;
  checks.sp_center_has_order_2 := Length(ClassPositionsOfCentre(tableSp))=2;
  checks.we6_center_is_trivial := Length(ClassPositionsOfCentre(tableW))=1;
  checks.sp_has_one_linear_character := Number(irrSp,character -> Degree(character)=1)=1;
  checks.we6_has_two_linear_characters := Number(irrW,character -> Degree(character)=1)=2;
  checks.sp_matrix_group_is_perfect := IsPerfectGroup(groupSp);
  checks.sp_matrix_group_center_has_order_2 := Size(Center(groupSp))=2;
  checks.we6_characters_are_all_real_orthogonal := ForAll(indicatorsW,value -> value=1);

  checks.degree5_pair_is_2_3 := List(irrSp{[2,3]},Degree)=[5,5];
  checks.degree4_pair_is_21_22 := List(irrSp{[21,22]},Degree)=[4,4];
  checks.degree5_pair_is_conjugate :=
    Position(irrSp,ComplexConjugate(irrSp[2]))=3 and
    Position(irrSp,ComplexConjugate(irrSp[3]))=2;
  checks.degree4_pair_is_conjugate :=
    Position(irrSp,ComplexConjugate(irrSp[21]))=22 and
    Position(irrSp,ComplexConjugate(irrSp[22]))=21;
  checks.weil_pairs_have_fs_zero :=
    indicatorsSp{[2,3,21,22]}=[0,0,0,0];
  checks.weil_pairs_have_conductor_3 :=
    List(irrSp{[2,3,21,22]},Conductor)=[3,3,3,3];
  checks.degree5_center_is_plus := irrSp[2][2]=5 and irrSp[3][2]=5;
  checks.degree4_center_is_minus := irrSp[21][2]=-4 and irrSp[22][2]=-4;
  checks.sp_has_no_degree3_irreducible :=
    not 3 in List(irrSp,Degree);

  checks.outer_fusion_is_unique := Length(fusions)=1;
  checks.outer_10_restricts_to_5_plus_5 :=
    support10=[2,3] and multiplicities10[2]=1 and multiplicities10[3]=1;
  checks.outer_8_restricts_to_4_plus_4 :=
    support8=[21,22] and multiplicities8[21]=1 and multiplicities8[22]=1;
  checks.outer_10_and_8_are_real :=
    Indicator(tableOuter,[irrOuter[3]],2)=[1] and
    Indicator(tableOuter,[irrOuter[26]],2)=[1];

  checks.csx_p5_trace_is_90 := trace5=90;
  checks.csx_p5_determinant_is_325 := determinant5=325;
  checks.csx_p5_discriminant_is_6800 := discriminant5=6800;
  checks.claimed_8449_square_is_off_by_one := 8449^2=71385601;
  checks.q7_candidate_is_prime := IsPrimeInt(3089);
  checks.q7_order_is_772 := order3089=772;
  checks.q7_order_is_not_1544 := order3089<>1544;

  checks.symplectic_unipotent_preserves_form :=
    TransposedMat(unipotent)*omega*unipotent=omega;
  checks.symplectic_unipotent_has_order_3 := Order(unipotent)=3;
  checks.symplectic_unipotent_is_not_an_involution := unipotent^2<>IdentityMat(4,field3);

  names := RecNames(checks);
  Assert358("all checks",ForAll(names,name -> checks.(name)));

  stream := OutputTextFile(OUT358,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass358.github_batch_integrity.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"the exact correction is Sp(4,3)=2.U4(2), W(E6)=U4(2).2, Weil 9=5+4, and B5 has roots 45+-10sqrt(17)\",\n");
  WriteAll(stream,"  \"group_ledger\": {\n");
  WriteAll(stream,"    \"PSp(4,3)\": \"U4(2), order 25920\",\n");
  WriteAll(stream,"    \"Sp(4,3)\": \"2.U4(2), order 51840, center C2, perfect\",\n");
  WriteAll(stream,"    \"W(E6)\": \"U4(2).2 = PGSp(4,3), order 51840, center trivial, abelianization C2\"\n");
  WriteAll(stream,"  },\n");
  WriteAll(stream,"  \"weil_9\": {\n");
  WriteAll(stream,"    \"split\": \"5+4\",\n");
  WriteAll(stream,"    \"degree5_pair\": [2,3],\n");
  WriteAll(stream,"    \"degree4_pair\": [21,22],\n");
  WriteAll(stream,"    \"frobenius_schur\": [0,0,0,0],\n");
  WriteAll(stream,"    \"outer_real_envelope\": \"18=10+8 restricts as (5a+5b)+(4a+4b)\"\n");
  WriteAll(stream,"  },\n");
  WriteAll(stream,"  \"transfer_p5\": {\n");
  WriteAll(stream,"    \"polynomial\": \"x^2-90x+325\",\n");
  WriteAll(stream,"    \"roots\": \"45+-10sqrt(17)\",\n");
  WriteAll(stream,"    \"discriminant\": 6800\n");
  WriteAll(stream,"  },\n");
  WriteAll(stream,"  \"q7_order\": {\"prime\": 3089, \"ord_2\": 772, \"near_maximal_target\": 1544, \"passes_target\": false},\n");
  WriteAll(stream,"  \"retractions\": [\n");
  WriteAll(stream,"    \"Sp(4,3) is W(E6) or W(E6)/Z2 is PSp(4,3)\",\n");
  WriteAll(stream,"    \"the q=3 Weil carrier has conjugate 6- and 3-dimensional constituents\",\n");
  WriteAll(stream,"    \"det(B5)=35697025 with complex eigenvalues and discriminant=-8449^2\",\n");
  WriteAll(stream,"    \"the q=7 order question remains open\",\n");
  WriteAll(stream,"    \"E6 simple reflections can map to characteristic-3 symplectic transvections\"\n");
  WriteAll(stream,"  ],\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool358(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass358 status=PASS checks=",Length(names)," output=",OUT358,"\n");
end;;

Main358();;
QUIT;
