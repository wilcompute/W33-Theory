# Pass7581-7588: actual sporadic character restrictions onto the E8/W33 carrier.
# Uses only stored CTblLib character tables and stored class fusions.
# Pass7893 rerun marker: force the exact master workflow after the Leech/V20 reconciliation.
# Pass8217 rerun marker: execute after the H27 parabolic and Q+(3,3) residue welds.
# Pass8641 rerun marker: execute after the diagonal-triality and ninefold-residue frontier.
LoadPackage("ctbllib");;

B:=CharacterTable("B");;
U:=CharacterTable("O8+(3).S4");;
O:=CharacterTable("O8+(3)");;
E:=CharacterTable("O8+(2)");;
L:=CharacterTable("(3xU4(2)):2");;
M:=CharacterTable("M");;
H:=CharacterTable("(3^2:2xO8+(3)).S4");;

A:=function(msg,c) if not c then Error(Concatenation("Pass7581 failed: ",msg)); fi; end;;
A("orders",Size(L)=155520 and Size(E)=174182400 and Size(U)=118852315545600);;

fUB:=GetFusionMap(U,B);; A("U->B fusion",fUB<>fail);;
fOU:=GetFusionMap(O,U);; A("O->U fusion",fOU<>fail);;
fEO:=GetFusionMap(E,O);; A("E->O fusion",fEO<>fail);;
fLE:=GetFusionMap(L,E);; A("L->E fusion",fLE<>fail);;
fHM:=GetFusionMap(H,M);; A("H->M fusion",fHM<>fail);;

# Compose the full leaf-stabilizer embedding into the Baby Monster.
fOB:=CompositionMaps(fUB,fOU);;
fEB:=CompositionMaps(fOB,fEO);;
fLB:=CompositionMaps(fEB,fLE);;
A("composed leaf fusion length",Length(fLB)=NrConjugacyClasses(L));;

chiB:=First(Irr(B),x->x[1]=4371);; A("Baby 4371 exists",chiB<>fail);;
chiL:=ClassFunction(L,chiB{fLB});;
multL:=List(Irr(L),psi->ScalarProduct(L,chiL,psi));;
A("leaf restriction integral",ForAll(multL,IsInt) and ForAll(multL,x->x>=0));;
compL:=Filtered([1..Length(multL)],i->multL[i]<>0);;
tripL:=List(compL,i->[i,multL[i],Irr(L)[i][1]]);;
A("leaf dimensions sum",Sum(tripL,x->x[2]*x[3])=4371);;

# Intermediate restrictions, retained to localize where constituents split.
chiU:=ClassFunction(U,chiB{fUB});;
multU:=List(Irr(U),psi->ScalarProduct(U,chiU,psi));;
compU:=Filtered([1..Length(multU)],i->multU[i]<>0);;
tripU:=List(compU,i->[i,multU[i],Irr(U)[i][1]]);;
A("U dimensions sum",Sum(tripU,x->x[2]*x[3])=4371);;

chiE:=ClassFunction(E,chiB{fEB});;
multE:=List(Irr(E),psi->ScalarProduct(E,chiE,psi));;
compE:=Filtered([1..Length(multE)],i->multE[i]<>0);;
tripE:=List(compE,i->[i,multE[i],Irr(E)[i][1]]);;
A("E dimensions sum",Sum(tripE,x->x[2]*x[3])=4371);;

# Independent Monster-local restriction: smallest nontrivial Monster irrep to
# the actual maximal subgroup H=(3^2:2 x O8+(3)).S4 used in Pass7501.
chiM:=First(Irr(M),x->x[1]=196883);; A("Monster 196883 exists",chiM<>fail);;
chiH:=ClassFunction(H,chiM{fHM});;
multH:=List(Irr(H),psi->ScalarProduct(H,chiH,psi));;
A("Monster restriction integral",ForAll(multH,IsInt) and ForAll(multH,x->x>=0));;
compH:=Filtered([1..Length(multH)],i->multH[i]<>0);;
tripH:=List(compH,i->[i,multH[i],Irr(H)[i][1]]);;
A("Monster dimensions sum",Sum(tripH,x->x[2]*x[3])=196883);;

Print("PASS7581_STATUS=PASS\n");
Print("BABY_TO_O8P3S4=",tripU,"\n");
Print("BABY_TO_O8P2=",tripE,"\n");
Print("BABY_TO_LEAF=",tripL,"\n");
Print("BABY_LEAF_HAS_81=",ForAny(tripL,x->x[3]=81),"\n");
Print("MONSTER_TO_MAXIMAL=",tripH,"\n");
QUIT;
