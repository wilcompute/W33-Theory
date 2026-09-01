# Exact MeatAxe comparison of the doubled-D4 H1_48 and canonical chamber
# Omega48.  Deliberately no Cohomolo call: the previous 576-dimensional Hom
# module exceeded the stock Cohomolo MDIM ceiling after all MeatAxe steps had
# succeeded.  This freezes the representation theorem independently.
Read("analysis/PART_W33_20260901_BINARY48_MATRICES.g");;

OUT := "data/PART_W33_20260901_BINARY48_MEATAXE_ONLY.json";;
F := GF(2);;
G := Group(PermGens40);;
if Size(G) <> 25920 then Error("binary48: generators do not give PSp(4,3)"); fi;
ToF := m -> ImmutableMatrix(F,List(m,r -> List(r,x -> x * One(F))));;
Amats := List(Amats,ToF);; Bmats := List(Bmats,ToF);;
Hmats := List(Hmats,ToF);; Cmats := List(Cmats,ToF);;

Amod := GModuleByMats(Amats,F);; Bmod := GModuleByMats(Bmats,F);;
Hmod := GModuleByMats(Hmats,F);; Cmod := GModuleByMats(Cmats,F);;
cfA := MTX.CompositionFactors(Amod);; cfB := MTX.CompositionFactors(Bmod);;
cfH := MTX.CompositionFactors(Hmod);; cfC := MTX.CompositionFactors(Cmod);;
dA := SortedList(List(cfA,MTX.Dimension));; dB := SortedList(List(cfB,MTX.Dimension));;
dH := SortedList(List(cfH,MTX.Dimension));; dC := SortedList(List(cfC,MTX.Dimension));;
isoHC := MTX.IsomorphismModules(Hmod,Cmod) <> fail;;
isoAB := MTX.IsomorphismModules(Amod,Bmod) <> fail;;
subH := SortedList(List(MTX.BasesSubmodules(Hmod),Length));;
subC := SortedList(List(MTX.BasesSubmodules(Cmod),Length));;

# Hom(B,A) is the module whose H^1 is Ext^1(B,A).  MeatAxe decomposition is
# feasible even though stock Cohomolo refuses the whole 576-dimensional module.
homMats := List([1..Length(Amats)], i ->
  KroneckerProduct(TransposedMat(Inverse(Bmats[i])),Amats[i]));;
homMats := List(homMats,ToF);;
homMod := GModuleByMats(homMats,F);;
homCF := MTX.CompositionFactors(homMod);;
homDims := SortedList(List(homCF,MTX.Dimension));;

Bool := function(x) if x then return "true"; else return "false"; fi; end;;
IntList := function(xs) return Concatenation("[",JoinStringsWithSeparator(List(xs,String),","),"]"); end;;
stream := OutputTextFile(OUT,false);; SetPrintFormattingStatus(stream,false);;
WriteAll(stream,"{\n");
WriteAll(stream,"  \"schema\":\"w33.20260901.binary48-meataxe-only.v1\",\n");
WriteAll(stream,"  \"status\":\"PASS\",\n");
WriteAll(stream,Concatenation("  \"groupOrder\":",String(Size(G)),",\n"));
WriteAll(stream,Concatenation("  \"compositionFactorDimensions\":{\"A24\":",IntList(dA),",\"B24\":",IntList(dB),",\"H1_48\":",IntList(dH),",\"Omega48\":",IntList(dC),"},\n"));
WriteAll(stream,Concatenation("  \"moduleIsomorphism\":{\"H1_equals_Omega48\":",Bool(isoHC),",\"A24_equals_B24\":",Bool(isoAB),"},\n"));
WriteAll(stream,Concatenation("  \"submoduleDimensions\":{\"H1_48\":",IntList(subH),",\"Omega48\":",IntList(subC),"},\n"));
WriteAll(stream,Concatenation("  \"homBA\":{\"dimension\":576,\"compositionFactorDimensions\":",IntList(homDims),"},\n"));
WriteAll(stream,"  \"ext\":{\"dimensionComputed\":false,\"lowerBoundFromIndependentNonsplitExtension\":1,\"reasonFullCohomoloDeferred\":\"stock Cohomolo MDIM ceiling on the 576-dimensional Hom(B24,A24) module\"},\n");
WriteAll(stream,"  \"theorem\":\"MeatAxe decides the exact F2 module comparison of H1_48 and Omega48 and decomposes Hom(B24,A24) without invoking Cohomolo. The independent explicit splitting-equation certificate proves Ext^1(B24,A24) is nonzero, hence dimension at least one; its exact dimension remains open.\",\n");
WriteAll(stream,"  \"boundary\":\"Composition-factor dimensions alone do not name modular irreducible species. Whole-module isomorphism is reported separately by MeatAxe. No Ext dimension is guessed from the nonsplit witness.\"\n");
WriteAll(stream,"}\n"); CloseStream(stream);;
Print("BINARY48_MEATAXE_ONLY isoHC=",isoHC," isoAB=",isoAB," cfH=",dH," cfC=",dC," homCF=",homDims,"\n");
QUIT;
