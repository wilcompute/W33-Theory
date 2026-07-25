#############################################################################
# Pass 542 -- the Z/9 signed-cycle census is an equivariant Hjelmslev lift.
#
# GAP owns every computation in this witness.  The source constructs the
# reduction exact sequence, the primitive/deep antipodal-pair bundle, the
# congruence-kernel translation action, and the cosetwise signed-cycle table.
#############################################################################

ROOT := DirectoryCurrent();
OUT := Filename(ROOT, "data/w33_pass542_z9_hjelmslev_lift.json");

ModN := function(x,n)
  return x mod n;
end;

NegVec := function(v,n)
  return List(v,x->(-x) mod n);
end;

ScaleVec := function(a,v,n)
  return List(v,x->(a*x) mod n);
end;

MatVec := function(g,v,n)
  return [ (g[1][1]*v[1]+g[1][2]*v[2]) mod n,
           (g[2][1]*v[1]+g[2][2]*v[2]) mod n ];
end;

MatMul2 := function(g,h,n)
  return List([1..2],i->List([1..2],j->
    Sum([1..2],k->g[i][k]*h[k][j]) mod n));
end;

InverseSL2 := function(g,n)
  return [[g[2][2] mod n,(-g[1][2]) mod n],
          [(-g[2][1]) mod n,g[1][1] mod n]];
end;

Identity2 := function(n)
  return [[1 mod n,0],[0,1 mod n]];
end;

SL2Matrices := function(n)
  local ans,a,b,c,d;
  ans := [];
  for a in [0..n-1] do
    for b in [0..n-1] do
      for c in [0..n-1] do
        for d in [0..n-1] do
          if (a*d-b*c) mod n=1 then Add(ans,[[a,b],[c,d]]); fi;
        od;
      od;
    od;
  od;
  return ans;
end;

ReduceMatrix := function(g)
  return List(g,row->List(row,x->x mod 3));
end;

PairClass := function(v,n)
  local nv;
  nv := NegVec(v,n);
  if v<nv then return v; fi;
  return nv;
end;

PairReps := function(n)
  local reps,a,b,v;
  reps := [];
  for a in [0..n-1] do
    for b in [0..n-1] do
      if not (a=0 and b=0) then
        v := [a,b];
        if v=PairClass(v,n) then Add(reps,v); fi;
      fi;
    od;
  od;
  Sort(reps);
  return reps;
end;

ActPair := function(pair,g,n)
  return PairClass(MatVec(g,pair,n),n);
end;

UnitsMod := function(n)
  return Filtered([0..n-1],a->Gcd(a,n)=1);
end;

ProjectiveClass := function(v,n)
  return Minimum(List(UnitsMod(n),a->ScaleVec(a,v,n)));
end;

ProjectiveReps := function(n)
  local vectors,a,b;
  vectors := [];
  for a in [0..n-1] do
    for b in [0..n-1] do
      if Gcd(Gcd(a,b),n)=1 then AddSet(vectors,ProjectiveClass([a,b],n)); fi;
    od;
  od;
  return vectors;
end;

ActProjective := function(point,g,n)
  return ProjectiveClass(MatVec(g,point,n),n);
end;

PairToP1Z9 := function(pair)
  return ProjectiveClass(pair,9);
end;

ReduceP1Z9 := function(point)
  return ProjectiveClass(List(point,x->x mod 3),3);
end;

PrimitiveBase := function(pair)
  return ProjectiveClass(List(pair,x->x mod 3),3);
end;

DeepBase := function(pair)
  return ProjectiveClass(List(pair,x->QuoInt(x,3) mod 3),3);
end;

CountFibres := function(domain,map,codomain)
  return List(codomain,y->Number(domain,x->map(x)=y));
end;

KernelParameter := function(k)
  local I;
  I := Identity2(9);
  return List([1..2],i->List([1..2],j->
    QuoInt((k[i][j]-I[i][j]) mod 9,3) mod 3));
end;

AddMat2 := function(a,b,n)
  return List([1..2],i->List([1..2],j->(a[i][j]+b[i][j]) mod n));
end;

AddVec := function(a,b,n)
  return List([1..Length(a)],i->(a[i]+b[i]) mod n);
end;

Det2 := function(a,n)
  return (a[1][1]*a[2][2]-a[1][2]*a[2][1]) mod n;
end;

IsZeroMat2 := function(a)
  return ForAll(a,row->ForAll(row,x->x=0));
end;

ProjectiveMatLine := function(a)
  local flat,negative,chosen;
  flat := Flat(a);
  negative := List(flat,x->(2*x) mod 3);
  chosen := Minimum([flat,negative]);
  return [[chosen[1],chosen[2]],[chosen[3],chosen[4]]];
end;

KernelBaseOfNilpotent := function(a,points)
  return First(points,r->MatVec(a,r,3)=[0,0]);
end;

OrientedLift := function(pair)
  local red,base;
  red := List(pair,x->x mod 3);
  base := ProjectiveClass(red,3);
  if red=base then return pair; fi;
  return NegVec(pair,9);
end;

FibreCoordinate := function(pair)
  local v,base,t;
  v := OrientedLift(pair);
  base := List(v,x->x mod 3);
  t := List([1..2],i->QuoInt((v[i]-base[i]) mod 9,3) mod 3);
  return [base,t];
end;

SignedActionData := function(g,n,reps)
  local gi,perm,signs,i,u,r;
  gi := InverseSL2(g,n);
  perm := [];
  signs := [];
  for i in [1..Length(reps)] do
    u := MatVec(gi,reps[i],n);
    r := PairClass(u,n);
    Add(perm,Position(reps,r));
    if u=r then Add(signs,1); else Add(signs,-1); fi;
  od;
  return [perm,signs];
end;

ShellCycleData := function(g,reps)
  local dat,perm,signs,seen,i,j,cycle,net,shell,posP,posD,negP,negD;
  dat := SignedActionData(g,9,reps);
  perm := dat[1]; signs := dat[2];
  seen := [];
  posP := 0; posD := 0; negP := 0; negD := 0;
  for i in [1..Length(reps)] do
    if not i in seen then
      j := i; cycle := []; net := 1;
      while not j in cycle do
        Add(cycle,j); AddSet(seen,j);
        net := net*signs[j];
        j := perm[j];
      od;
      if reps[i][1] mod 3=0 and reps[i][2] mod 3=0 then
        shell := "deep";
      else
        shell := "primitive";
      fi;
      if shell="primitive" and net=1 then posP := posP+1;
      elif shell="primitive" then negP := negP+1;
      elif net=1 then posD := posD+1;
      else negD := negD+1;
      fi;
    fi;
  od;
  return rec(posP:=posP,posD:=posD,negP:=negP,negD:=negD);
end;

ClosureSizeAtMost24 := function(gens,n)
  local expanded,elements,index,x,g,y;
  expanded := ShallowCopy(gens);
  for g in gens do Add(expanded,InverseSL2(g,n)); od;
  elements := [Identity2(n)];
  index := 1;
  while index<=Length(elements) do
    x := elements[index];
    for g in expanded do
      y := MatMul2(x,g,n);
      if not y in elements then
        Add(elements,y);
        if Length(elements)>24 then return 25; fi;
      fi;
    od;
    index := index+1;
  od;
  return Length(elements);
end;

GeneratedSubgroupElements := function(gens,n)
  local expanded,elements,index,x,g,y;
  expanded := ShallowCopy(gens);
  for g in gens do Add(expanded,InverseSL2(g,n)); od;
  elements := [Identity2(n)];
  index := 1;
  while index<=Length(elements) do
    x := elements[index];
    for g in expanded do
      y := MatMul2(x,g,n);
      if not y in elements then Add(elements,y); fi;
    od;
    index := index+1;
  od;
  return Set(elements);
end;

ConjugateBy := function(g,x,n)
  return MatMul2(MatMul2(g,x,n),InverseSL2(g,n),n);
end;

IncrementCollected := function(table,key)
  local pos;
  pos := PositionProperty(table,x->x[1]=key);
  if pos=fail then Add(table,[key,1]);
  else table[pos][2] := table[pos][2]+1; fi;
end;

PairOrbitSize := function(group,point,n)
  return Length(Set(List(group,g->ActPair(point,g,n))));
end;

PairStabilizerSize := function(group,point,n)
  return Number(group,g->ActPair(point,g,n)=point);
end;

#############################################################################
# A. Exact sequence and complete splitting test.
#############################################################################

G9 := SL2Matrices(9);
G3 := SL2Matrices(3);
I9 := Identity2(9);
I3 := Identity2(3);
K := Filtered(G9,g->ReduceMatrix(g)=I3);
Kparams := List(K,KernelParameter);

S3 := [[0,2],[1,0]];
T3 := [[1,1],[0,1]];
SLifts := Filtered(G9,g->ReduceMatrix(g)=S3);
TLifts := Filtered(G9,g->ReduceMatrix(g)=T3);
splittingPairs := [];
for s in SLifts do
  for t in TLifts do
    if ClosureSizeAtMost24([s,t],9)=24 then Add(splittingPairs,[s,t]); fi;
  od;
od;
complementSubgroups := Set(List(splittingPairs,pair->
  GeneratedSubgroupElements(pair,9)));
firstComplement := complementSubgroups[1];
kernelConjugateComplements := Set(List(K,k->
  Set(List(firstComplement,h->ConjugateBy(k,h,9)))));
adjointConjugationLaw := ForAll(firstComplement,h->ForAll(K,k->
  KernelParameter(ConjugateBy(h,k,9))=
    MatMul2(MatMul2(ReduceMatrix(h),KernelParameter(k),3),
      InverseSL2(ReduceMatrix(h),3),3)));
centerG9 := Filtered(G9,g->ForAll(G9,h->
  MatMul2(g,h,9)=MatMul2(h,g,9)));
complementActionKernel := Filtered(firstComplement,h->ForAll(K,k->
  ConjugateBy(h,k,9)=k));

#############################################################################
# B. The 36 -> 12 -> 4 cover and the four-point deep shell.
#############################################################################

pairs9 := PairReps(9);
primitivePairs := Filtered(pairs9,v->not (v[1] mod 3=0 and v[2] mod 3=0));
deepPairs := Filtered(pairs9,v->v[1] mod 3=0 and v[2] mod 3=0);
p1z9 := ProjectiveReps(9);
p1f3 := ProjectiveReps(3);
fibres36to12 := CountFibres(primitivePairs,PairToP1Z9,p1z9);
fibres12to4 := CountFibres(p1z9,ReduceP1Z9,p1f3);
fibres36to4 := CountFibres(primitivePairs,PrimitiveBase,p1f3);

coverEquivariant := ForAll(G9,g->
  ForAll(primitivePairs,p->
    PairToP1Z9(ActPair(p,g,9))=ActProjective(PairToP1Z9(p),g,9)) and
  ForAll(p1z9,x->
    ReduceP1Z9(ActProjective(x,g,9))=
      ActProjective(ReduceP1Z9(x),ReduceMatrix(g),3)));

deepEquivariant := ForAll(G9,g->ForAll(deepPairs,d->
  DeepBase(ActPair(d,g,9))=
    ActProjective(DeepBase(d),ReduceMatrix(g),3)));

#############################################################################
# C. The kernel is sl_2(F_3)^+ and acts by fibre translations.
#############################################################################

kernelTranslationLaw := ForAll(K,k->ForAll(primitivePairs,p->
  FibreCoordinate(ActPair(p,k,9))[1]=FibreCoordinate(p)[1] and
  FibreCoordinate(ActPair(p,k,9))[2]=
    AddVec(FibreCoordinate(p)[2],
      MatVec(KernelParameter(k),FibreCoordinate(p)[1],3),3)));

kernelOrbitSizes := [];
kernelStabilizerSizes := [];
fibreStabilizerLines := [];
fibre := fail;
stabilizer := fail;
nonzeroParameter := fail;
for base in p1f3 do
  fibre := Filtered(primitivePairs,p->PrimitiveBase(p)=base);
  Add(kernelOrbitSizes,PairOrbitSize(K,fibre[1],9));
  Add(kernelStabilizerSizes,PairStabilizerSize(K,fibre[1],9));
  stabilizer := Filtered(K,k->ActPair(fibre[1],k,9)=fibre[1]);
  nonzeroParameter := First(List(stabilizer,KernelParameter),
    A->not IsZeroMat2(A));
  Add(fibreStabilizerLines,[base,ProjectiveMatLine(nonzeroParameter)]);
od;

nilpotentParameterLines := Set(List(Filtered(Kparams,A->
  not IsZeroMat2(A) and Det2(A,3)=0),ProjectiveMatLine));
nilpotentKernelBases := List(nilpotentParameterLines,A->
  [KernelBaseOfNilpotent(A,p1f3),A]);

#############################################################################
# D. Cosetwise explanation of the Pass-540 coefficients.
#############################################################################

cycleRows := List(G9,g->[g,ShellCycleData(g,pairs9)]);
jointProfile := [];
for row in cycleRows do
  IncrementCollected(jointProfile,[row[2].posP,row[2].posD]);
od;
Sort(jointProfile,function(a,b)
  if a[1][1]=b[1][1] then return a[1][2]<b[1][2]; fi;
  return a[1][1]<b[1][1];
end);
jointProfileFlat := List(jointProfile,x->[x[1][1],x[1][2],x[2]]);

quotientDeepProfile := [];
d0CosetsUniform := true;
d2CosetsUniform := true;
identityKernelProfile := [];
identityKernelTypeProfile := [];
for h in G3 do
  lifts := Filtered(cycleRows,row->ReduceMatrix(row[1])=h);
  deepCount := lifts[1][2].posD;
  IncrementCollected(quotientDeepProfile,deepCount);
  liftPrimitiveProfile := Collected(List(lifts,row->row[2].posP));
  if deepCount=0 then
    d0CosetsUniform := d0CosetsUniform and liftPrimitiveProfile=[[0,27]];
  elif deepCount=2 then
    d2CosetsUniform := d2CosetsUniform and
      liftPrimitiveProfile=[[6,9],[8,9],[12,9]];
  elif h=I3 then
    identityKernelProfile := liftPrimitiveProfile;
    for row in lifts do
      A := KernelParameter(row[1]);
      if IsZeroMat2(A) then atype := "zero";
      elif Det2(A,3)=0 then atype := "nonzero_nilpotent";
      else atype := "invertible"; fi;
      IncrementCollected(identityKernelTypeProfile,[atype,row[2].posP]);
    od;
  fi;
od;
Sort(quotientDeepProfile);
Sort(identityKernelTypeProfile,function(a,b) return a[1]<b[1]; end);

allFixedSum := Sum(cycleRows,row->9^(row[2].posP+row[2].posD));
primitiveFixedSum := Sum(cycleRows,row->9^row[2].posP);
deepFixedSum := Sum(cycleRows,row->9^row[2].posD);
fullFixedSum := Sum(Filtered(cycleRows,row->
  row[2].negP=0 and row[2].negD=0),
  row->8^(row[2].posP+row[2].posD));

allOrbits := QuoInt(allFixedSum,Length(G9));
primitiveOrbits := QuoInt(primitiveFixedSum,Length(G9));
deepOrbits := QuoInt(deepFixedSum,Length(G9));
fullOrbits := QuoInt(fullFixedSum,Length(G9));

#############################################################################
# E. Checks and certificate.
#############################################################################

checks := rec();
checks.sl2_z9_order_648 := Length(G9)=648;
checks.reduction_image_is_sl2_f3_order_24 := Set(List(G9,ReduceMatrix))=Set(G3);
checks.reduction_kernel_order_27 := Length(K)=27;
checks.kernel_parameters_are_all_traceless :=
  Length(Set(Kparams))=27 and ForAll(Kparams,A->(A[1][1]+A[2][2]) mod 3=0);
checks.kernel_parameter_is_additive := ForAll(K,k->ForAll(K,l->
  KernelParameter(MatMul2(k,l,9))=
    AddMat2(KernelParameter(k),KernelParameter(l),3)));
checks.kernel_is_abelian := ForAll(K,k->ForAll(K,l->
  MatMul2(k,l,9)=MatMul2(l,k,9)));
checks.kernel_has_exponent_three := ForAll(K,k->
  MatMul2(MatMul2(k,k,9),k,9)=I9);
checks.standard_reductions_generate_sl2_f3 :=
  ClosureSizeAtMost24([S3,T3],3)=24;
checks.each_standard_generator_has_27_lifts :=
  Length(SLifts)=27 and Length(TLifts)=27;
checks.complete_complement_scan_finds_split := Length(splittingPairs)=27;
checks.twenty_seven_distinct_complements := Length(complementSubgroups)=27;
checks.each_complement_maps_isomorphically_to_sl2_f3 :=
  ForAll(complementSubgroups,H->Length(H)=24 and
    Set(List(H,ReduceMatrix))=Set(G3) and Length(Intersection(H,K))=1);
checks.kernel_conjugation_is_transitive_on_complements :=
  kernelConjugateComplements=complementSubgroups;
checks.complement_action_on_kernel_is_adjoint := adjointConjugationLaw;
checks.sl2_z9_center_has_order_two := Length(centerG9)=2;
checks.complement_adjoint_action_kernel_has_order_two :=
  Length(complementActionKernel)=2;
checks.complement_adjoint_action_kernel_is_total_center :=
  Set(complementActionKernel)=Set(centerG9);
checks.complement_adjoint_image_has_order_twelve :=
  QuoInt(Length(firstComplement),Length(complementActionKernel))=12;
checks.antipodal_shell_is_36_plus_4 :=
  Length(pairs9)=40 and Length(primitivePairs)=36 and Length(deepPairs)=4;
checks.projective_cover_sizes_are_36_12_4 :=
  Length(primitivePairs)=36 and Length(p1z9)=12 and Length(p1f3)=4;
checks.first_cover_is_three_sheeted := Set(fibres36to12)=[3];
checks.second_cover_is_three_sheeted := Set(fibres12to4)=[3];
checks.composite_cover_is_nine_sheeted := Set(fibres36to4)=[9];
checks.deep_shell_is_bijective_with_p1_f3 :=
  Set(List(deepPairs,DeepBase))=Set(p1f3);
checks.cover_is_sl2_z9_equivariant := coverEquivariant;
checks.deep_copy_is_equivariant := deepEquivariant;
checks.kernel_fixes_deep_shell_pointwise :=
  ForAll(K,k->ForAll(deepPairs,d->ActPair(d,k,9)=d));
checks.kernel_translation_law := kernelTranslationLaw;
checks.kernel_is_transitive_on_each_nine_fibre := Set(kernelOrbitSizes)=[9];
checks.kernel_fibre_stabilizers_have_order_three := Set(kernelStabilizerSizes)=[3];
checks.four_fibre_stabilizers_are_four_nilpotent_lines :=
  Length(nilpotentParameterLines)=4 and
  Set(List(fibreStabilizerLines,row->row[2]))=nilpotentParameterLines;
checks.nilpotent_line_kernel_is_the_deep_base :=
  ForAll(fibreStabilizerLines,row->
    KernelBaseOfNilpotent(row[2],p1f3)=row[1]);
checks.eight_nonzero_nilpotents_are_two_per_projective_line :=
  Number(Kparams,A->not IsZeroMat2(A) and Det2(A,3)=0)=8 and
  ForAll(nilpotentParameterLines,line->
    Number(Kparams,A->not IsZeroMat2(A) and Det2(A,3)=0 and
      ProjectiveMatLine(A)=line)=2);
checks.quotient_deep_positive_cycle_profile :=
  quotientDeepProfile=[[0,15],[2,8],[4,1]];
checks.deep_zero_cosets_explain_405 := d0CosetsUniform;
checks.deep_two_cosets_split_nine_nine_nine := d2CosetsUniform;
checks.identity_coset_profile_is_18_8_1 :=
  identityKernelProfile=[[12,18],[18,8],[36,1]];
checks.kernel_rank_types_explain_18_8_1 :=
  Set(identityKernelTypeProfile)=Set([
    [["invertible",12],18],
    [["nonzero_nilpotent",18],8],
    [["zero",36],1]
  ]);
checks.joint_profile_recovers_pass540 := jointProfileFlat=[
  [0,0,405],[6,2,72],[8,2,72],[12,2,72],
  [12,4,18],[18,4,8],[36,4,1]
];
checks.all_section_burnside_count_recovers_pass540 :=
  allOrbits=228100045392509153077600971330057241;
checks.full_support_burnside_count_recovers_pass540 :=
  fullOrbits=2051277771273019233341050472890368;
checks.primitive_shell_orbit_count_recovers_pass540 :=
  primitiveOrbits=34766048680461690760220142047341;
checks.deep_shell_orbit_count_recovers_pass540 := deepOrbits=301;

checkNames := SortedList(RecNames(checks));
status := ForAll(checkNames,name->checks.(name));
statusText := "FAIL";
if status then statusText := "PASS"; fi;
splitText := "NONSPLIT";
if Length(splittingPairs)>0 then splitText := "SPLIT"; fi;
exitCode := 1;
if status then exitCode := 0; fi;

out := OutputTextFile(OUT,false);
SetPrintFormattingStatus(out,false);
Emit := function(arg)
  WriteAll(out,Concatenation(List(arg,String)));
end;

Emit("{\n");
Emit("  \"schema\":\"w33.pass542.z9_hjelmslev_lift.v1\",\n");
Emit("  \"status\":\"",statusText,"\",\n");
Emit("  \"exact_sequence\":{\n");
Emit("    \"sequence\":\"1 -> sl_2(F_3)^+ -> SL(2,Z/9) -> SL(2,F_3) -> 1\",\n");
Emit("    \"orders\":[27,648,24],\n");
Emit("    \"kernel_structure\":\"C3^3, parametrized by A |-> I+3A with tr(A)=0\",\n");
Emit("    \"splitting_verdict\":\"",splitText,"\",\n");
Emit("    \"splitting_test\":\"All 27 lifts of each of the standard generators S,T of SL(2,3) were paired (729 pairs). A complement would be generated by one such pair and have order 24.\",\n");
Emit("    \"complement_generating_pairs\":",Length(splittingPairs),",\n");
Emit("    \"distinct_complements\":",Length(complementSubgroups),",\n");
Emit("    \"first_complement_generators\":",String(splittingPairs[1]),",\n");
Emit("    \"center_order\":",Length(centerG9),",\n");
Emit("    \"complement_action_kernel_order\":",Length(complementActionKernel),",\n");
Emit("    \"adjoint_action_image_order\":",
  QuoInt(Length(firstComplement),Length(complementActionKernel)),",\n");
Emit("    \"semidirect_product\":\"SL(2,Z/9) = sl_2(F3)^+ semidirect SL(2,3), with the quotient complement acting by conjugation through the adjoint action\",\n");
Emit("    \"pass192_same_orders_nonidentification\":\"Pass 192 has the same order vector [27,648,24] for a different exact sequence: the W33 line stabilizer maps onto S4 through its faithful tetrahedral action. Here the quotient is SL(2,3), its central C2 is the kernel of the adjoint action, and the action image has order 12 (A4). Equal order vectors do not identify the extensions.\"\n");
Emit("  },\n");
Emit("  \"hjelmslev_cover\":{\n");
Emit("    \"sizes\":[36,12,4],\n");
Emit("    \"maps\":\"primitive antipodal pairs -> P1(Z/9) -> P1(F3)\",\n");
Emit("    \"fibre_sizes\":[3,3],\n");
Emit("    \"composite_fibre_size\":9,\n");
Emit("    \"deep_points\":",String(deepPairs),",\n");
Emit("    \"deep_bases\":",String(List(deepPairs,DeepBase)),",\n");
Emit("    \"fibre_stabilizer_lines\":",String(fibreStabilizerLines),",\n");
Emit("    \"nilpotent_kernel_lines\":",String(nilpotentKernelBases),",\n");
Emit("    \"kernel_action\":\"I+3A fixes the deep copy pointwise and sends ([r],t) to ([r],t+Ar) on every primitive nine-fibre; each fibre is one kernel orbit with stabilizer C3.\"\n");
Emit("  },\n");
Emit("  \"coset_cycle_theorem\":{\n");
Emit("    \"quotient_deep_positive_cycles\":",String(quotientDeepProfile),",\n");
Emit("    \"deep_zero_cosets\":\"15 quotient elements times 27 lifts give coefficient 405 and primitive positive-cycle count 0\",\n");
Emit("    \"deep_two_cosets\":\"Each of 8 quotient elements has primitive positive-cycle counts 6,8,12 on 9 lifts each, giving coefficients 72,72,72\",\n");
Emit("    \"identity_coset_kernel_types\":",String(identityKernelTypeProfile),",\n");
Emit("    \"joint_positive_cycle_profile\":",String(jointProfileFlat),",\n");
Emit("    \"burnside_polynomial\":\"405+72*U^6*V^2+72*U^8*V^2+72*U^12*V^2+18*U^12*V^4+8*U^18*V^4+U^36*V^4\"\n");
Emit("  },\n");
Emit("  \"burnside_recovery\":{\n");
Emit("    \"all_sections\":\"",9^40,"\",\n");
Emit("    \"all_orbits\":\"",allOrbits,"\",\n");
Emit("    \"full_support_sections\":\"",8^40,"\",\n");
Emit("    \"full_support_orbits\":\"",fullOrbits,"\",\n");
Emit("    \"primitive_shell_orbits\":\"",primitiveOrbits,"\",\n");
Emit("    \"deep_shell_orbits\":",deepOrbits,"\n");
Emit("  },\n");
Emit("  \"theorem\":\"The Pass-540 Z/9 signed-cycle census is the Burnside evaluation of an equivariant two-stage Hjelmslev lift. The congruence kernel is additive sl_2(F3), the extension splits with 27 kernel-conjugate complements and adjoint quotient action, the primitive shell is a 9-sheet affine bundle over the same P1(F3) carried by the four deep pairs, and kernel rank types plus quotient signed-cycle types force every coefficient of the bivariate Burnside polynomial.\",\n");
Emit("  \"boundary\":\"This is an exact finite group-action theorem. It derives orbit counts and shell structure; it does not classify characteristic-polynomial images over Z/9 or identify this congruence kernel with the distinct central-character kernels in the conductor tower.\",\n");
Emit("  \"checks\":{\n");
for i in [1..Length(checkNames)] do
  name := checkNames[i];
  Emit("    \"",name,"\":",checks.(name));
  if i<Length(checkNames) then Emit(","); fi;
  Emit("\n");
od;
Emit("  }\n");
Emit("}\n");
CloseStream(out);

Print("Pass 542 Z/9 Hjelmslev lift: ",statusText," (",
  Number(checkNames,name->checks.(name)),"/",Length(checkNames),")\n");
Print("Exact sequence splitting verdict: ",
  splitText,"\n");
Print("Burnside orbits: ",allOrbits,"; full support: ",fullOrbits,"\n");

QUIT_GAP(exitCode);
