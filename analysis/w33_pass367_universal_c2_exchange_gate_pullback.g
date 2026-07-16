# Pass 367: four apparently different exchange/gate C2 quotients admit one
# synchronized fiber product, but not one common C2 action.  The affine
# QR-137 residue extension is nonsplit and forces every odd lift in the
# pullback to have order at least eight.

LoadPackage("atlasrep");;

OUT367 := "data/w33_pass367_universal_c2_exchange_gate_pullback.json";;

Assert367 := function(label,condition)
  if not condition then
    Error(Concatenation("Pass367 assertion failed: ",label));
  fi;
end;;

Bool367 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

QPlus367 := function(vector)
  return vector[1]*vector[2]+vector[3]*vector[4]+vector[5]*vector[6];
end;;

Polar367 := function(left,right)
  return QPlus367(left+right)+QPlus367(left)+QPlus367(right);
end;;

QMinus367 := function(vector,direction)
  return QPlus367(vector)+Polar367(direction,vector);
end;;

Transvection367 := function(direction,form)
  return ImmutableMatrix(GF(2),IdentityMat(6,GF(2))+
    (form*TransposedMat([direction]))*[direction]);
end;;

Main367 := function()
  local field2,zero,one,form,direction,vectors,nonsingular,
        we6,we6Even,we6OddInvolution,outerWeil,outerWeilEven,
        outerWeilOddInvolutions,shift137,multiplier3,multiplier9,
        affineFull,affineEven,affineOddElements,affineOddOrders,affineOdd8,
        sqrt2,had,identity2,pauliX,pauliZ,realGenerators,realClifford,
        targetC2,hadamardCharacter,realEven,realOddInvolution,
        evenKernelOrder,pullbackOrder,minimumOddOrder,checks,names,name,
        stream,position;

  # Factor A: W(E6)=O-(6,2), with sign quotient and simple-reflection split.
  field2 := GF(2);
  zero := Zero(field2);
  one := One(field2);
  form := NullMat(6,6,field2);
  for position in [1,3,5] do
    form[position][position+1] := one;
    form[position+1][position] := one;
  od;
  direction := [zero,zero,zero,zero,one,one];
  vectors := Tuples([zero,one],6);
  nonsingular := Filtered(vectors,vector ->
    QMinus367(vector,direction)=one);
  we6 := Group(List(nonsingular,vector -> Transvection367(vector,form)));
  we6Even := DerivedSubgroup(we6);
  we6OddInvolution := First(GeneratorsOfGroup(we6),element ->
    not element in we6Even);

  # Factor B: the outer Weil envelope 2.U4(2).2 and its inner subgroup.
  outerWeil := AtlasGroup("2.U4(2).2");
  outerWeilEven := DerivedSubgroup(outerWeil);
  outerWeilOddInvolutions := Filtered(ConjugacyClasses(outerWeil),class ->
    not Representative(class) in outerWeilEven and
    Order(Representative(class))=2);

  # Factor C: C137:C136 and the quadratic-residue C137:C68 kernel.
  # The odd coset has orders 8 or 136 and contains no involution.
  shift137 := PermList(List([0..136],entry -> ((entry+1) mod 137)+1));
  multiplier3 := PermList(List([0..136],entry -> ((3*entry) mod 137)+1));
  multiplier9 := multiplier3^2;
  affineFull := Group(shift137,multiplier3);
  affineEven := Group(shift137,multiplier9);
  affineOddElements := Filtered(Elements(affineFull),element ->
    not element in affineEven);
  affineOddOrders := Set(List(affineOddElements,Order));
  affineOdd8 := multiplier3^17;

  # Factor D: real two-qubit Clifford H parity.
  sqrt2 := Sqrt(2);
  had := [[1/sqrt2,1/sqrt2],[1/sqrt2,-1/sqrt2]];
  identity2 := IdentityMat(2,Rationals);
  pauliX := [[0,1],[1,0]];
  pauliZ := [[1,0],[0,-1]];
  realGenerators := List([
    KroneckerProduct(had,identity2),
    KroneckerProduct(identity2,had),
    KroneckerProduct(pauliX,identity2),
    KroneckerProduct(identity2,pauliX),
    KroneckerProduct(pauliZ,identity2),
    KroneckerProduct(identity2,pauliZ),
    [[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]
  ],matrix -> ImmutableMatrix(CF(8),matrix));
  realClifford := Group(realGenerators);
  targetC2 := Group((1,2));
  hadamardCharacter := GroupHomomorphismByImages(realClifford,targetC2,
    realGenerators,[(1,2),(1,2),(),(),(),(),()]);
  realEven := Kernel(hadamardCharacter);
  realOddInvolution := realGenerators[1];

  # For four surjections epsilon_i:G_i->C2, the synchronized pullback has
  # even kernel product K_i and two parity fibers.  It exists canonically
  # as a grading; the affine factor prevents a section C2->F.
  evenKernelOrder := Size(we6Even)*Size(outerWeilEven)*
    Size(affineEven)*Size(realEven);
  pullbackOrder := 2*evenKernelOrder;
  minimumOddOrder := Lcm([Order(we6OddInvolution),
    Order(Representative(outerWeilOddInvolutions[1])),
    Order(affineOdd8),Order(realOddInvolution)]);

  checks := rec();
  checks.we6_extension_orders_are_51840_25920 :=
    Size(we6)=51840 and Size(we6Even)=25920;
  checks.we6_quotient_is_c2 := AbelianInvariants(we6/we6Even)=[2];
  checks.we6_extension_splits_by_involution :=
    Order(we6OddInvolution)=2 and not we6OddInvolution in we6Even;
  checks.outer_weil_extension_orders_are_103680_51840 :=
    Size(outerWeil)=103680 and Size(outerWeilEven)=51840;
  checks.outer_weil_quotient_is_c2 :=
    AbelianInvariants(outerWeil/outerWeilEven)=[2];
  checks.outer_weil_has_one_odd_involution_class :=
    Length(outerWeilOddInvolutions)=1;
  checks.affine_extension_orders_are_18632_9316 :=
    Size(affineFull)=18632 and Size(affineEven)=9316;
  checks.affine_even_subgroup_is_normal_index_two :=
    IsNormal(affineFull,affineEven) and Index(affineFull,affineEven)=2;
  checks.affine_odd_coset_orders_are_8_or_136 := affineOddOrders=[8,136];
  checks.affine_odd_coset_has_no_involution :=
    not ForAny(affineOddElements,element -> Order(element)=2);
  checks.affine_has_explicit_odd_order_eight_element :=
    Order(affineOdd8)=8 and not affineOdd8 in affineEven;
  checks.real_clifford_extension_orders_are_2304_1152 :=
    Size(realClifford)=2304 and Size(realEven)=1152;
  checks.real_hadamard_parity_is_surjective :=
    Size(Image(hadamardCharacter))=2;
  checks.real_extension_splits_by_hadamard_involution :=
    Order(realOddInvolution)=2 and not realOddInvolution in realEven;
  checks.even_fiber_is_direct_product_of_four_kernels :=
    evenKernelOrder=14420554127769600;
  checks.synchronized_pullback_order_is_exact :=
    pullbackOrder=28841108255539200;
  checks.odd_pullback_has_explicit_order_eight_tuple :=
    minimumOddOrder=8;
  checks.no_odd_pullback_element_can_be_an_involution :=
    Minimum(affineOddOrders)=8;
  checks.universal_c2_grading_is_nonsplit :=
    not ForAny(affineOddElements,element -> Order(element)=2);

  names := RecNames(checks);
  Assert367("all checks",ForAll(names,name -> checks.(name)));
  stream := OutputTextFile(OUT367,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass367.universal_c2_exchange_gate_pullback.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"four exchange/gate parities synchronize in one C2-graded fiber product, but the QR affine factor proves that no common involutory C2 action exists\",\n");
  WriteAll(stream,"  \"factors\": [{\"name\":\"W(E6) sign\",\"orders\":[51840,25920],\"split\":true},{\"name\":\"outer Weil parity\",\"orders\":[103680,51840],\"split\":true},{\"name\":\"QR-137 residue character\",\"orders\":[18632,9316],\"split\":false},{\"name\":\"real Clifford H parity\",\"orders\":[2304,1152],\"split\":true}],\n");
  WriteAll(stream,"  \"pullback_exact_sequence\": \"1 -> PSp(4,3) x 2.U4(2) x (C137:C68) x W(F4) -> F -> C2 -> 1\",\n");
  WriteAll(stream,"  \"even_kernel_order\": 14420554127769600,\n");
  WriteAll(stream,"  \"pullback_order\": 28841108255539200,\n");
  WriteAll(stream,"  \"odd_order_obstruction\": {\"QR_odd_orders\":[8,136],\"minimum_pullback_odd_order\":8,\"odd_involution_exists\":false},\n");
  WriteAll(stream,"  \"boundary\": \"The construction unifies the four quotients as one parity grading and categorical fiber product. It proves they cannot be unified as one split C2 action: any odd tuple projects to the QR odd coset, which has no involution.\",\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool367(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass367 status=PASS checks=",Length(names)," output=",OUT367,"\n");
end;;

Main367();;
QUIT;
