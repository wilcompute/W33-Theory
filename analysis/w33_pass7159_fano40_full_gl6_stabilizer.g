# Pass7159 second addendum: hidden linear symmetry of the 40-point binary complement.
#
# The 23 selected nonzero vectors of F2^6 are all wt1, all wt2 and two
# complementary wt3 vectors.  Their 40-point complement is (7x7)-(3x3).
# Compute the FULL setwise stabilizer in GL6(2), not merely the visible
# coordinate S3 wr C2, and test whether its induced degree-40 action is the
# W33 point action / U4(2) action from Pass1021.

repo:=GAPInfo.SystemEnvironment.W33_REPO;;
out:=Concatenation(repo,"/data/PART_W33_PASS7159_FANO40_FULL_GL6_STABILIZER.json");;
F:=GF(2);;
V:=F^6;;
vecs:=Filtered(Elements(V),v->v<>Zero(V));;
# Canonical integer mask for a row vector.
Mask:=v->Sum([1..6],i->Int(v[i])*2^(i-1));;
PosByMask:=[];; for i in [1..Length(vecs)] do PosByMask[Mask(vecs[i])+1]:=i; od;
WeightBits:=x->Number([0..5],i->QuoInt(x,2^i) mod 2=1);;
T0mask:=2^(2-1)+2^(4-1)+2^(5-1);; T1mask:=63-T0mask;;
selMasks:=Filtered([1..63],x->WeightBits(x)<=2 or x=T0mask or x=T1mask);;
compMasks:=Difference([1..63],selMasks);;
selPts:=Set(List(selMasks,x->PosByMask[x+1]));;
compPts:=Set(List(compMasks,x->PosByMask[x+1]));;
if Length(selPts)<>23 or Length(compPts)<>40 then Error("23+40 split failed"); fi;

GL:=GL(6,2);;
# Convert matrix generators to permutations of the 63 nonzero row vectors.
PermOfMat:=function(M)
  return PermList(List(vecs,v->Position(vecs,v*M)));
end;;
G63:=Group(List(GeneratorsOfGroup(GL),PermOfMat));;
if Size(G63)<>Size(GL) then Error("GL6 action not faithful"); fi;
Stab:=Stabilizer(G63,selPts,OnSets);;
if Set(compPts)<>Difference([1..63],Set(selPts)) then Error("complement mismatch"); fi;

# Induced faithful action on the 40 complement points.
K40:=Image(ActionHomomorphism(Stab,compPts,OnPoints));;
orbs:=SortedList(List(Orbits(K40,[1..40]),Length));;
trans:=Length(orbs)=1;
subdegrees:=[];; rank:=0;;
if trans then
  subdegrees:=SortedList(List(Orbits(Stabilizer(K40,1),[1..40]),Length));
  rank:=Length(subdegrees);
fi;

# Build exact W33 point action for permutation-conjugacy testing when possible.
S:=Sp(4,3);; pts3:=NormedRowVectors(GF(3)^4);;
P40:=Image(ActionHomomorphism(S,pts3,OnLines));;
S40:=SymmetricGroup(40);;
conjP:=false;;
if Size(K40)=Size(P40) then conjP:=IsConjugate(S40,K40,P40); fi;
N40:=Normalizer(S40,P40);;
conjFull:=false;;
if Size(K40)=Size(N40) then conjFull:=IsConjugate(S40,K40,N40); fi;

# If there is a 12-suborbit, build its orbital graph and certify SRG parameters.
srgok:=false;; lam:=fail;; mu:=fail;; degree:=fail;;
if trans and 12 in subdegrees then
  O:=First(Orbits(Stabilizer(K40,1),[1..40]),x->Length(x)=12);
  adj:=List([1..40],i->Set(List(O,t->t^RepresentativeAction(K40,1,i))));
  degree:=Length(adj[1]);; srgok:=ForAll(adj,x->Length(x)=degree);;
  for i in [1..40] do
    for j in [i+1..40] do
      c:=Length(Intersection(adj[i],adj[j]));
      if j in adj[i] then
        if lam=fail then lam:=c; elif lam<>c then srgok:=false; fi;
      else
        if mu=fail then mu:=c; elif mu<>c then srgok:=false; fi;
      fi;
    od;
  od;
fi;

Bool:=x->if x then return "true"; else return "false"; fi; end;;
stream:=OutputTextFile(out,false);; SetPrintFormattingStatus(stream,false);;
AppendTo(stream,"{\n");
AppendTo(stream," \"schema\":\"w33.pass7159.fano40_full_gl6_stabilizer.v1\",\n");
AppendTo(stream," \"status\":\"PASS\",\n");
AppendTo(stream," \"GL6_2_order\":",String(Size(G63)),",\n");
AppendTo(stream," \"setwise_stabilizer_order\":",String(Size(Stab)),",\n");
AppendTo(stream," \"induced_order_on_40\":",String(Size(K40)),",\n");
AppendTo(stream," \"orbit_sizes_on_40\":[",JoinStringsWithSeparator(List(orbs,String),","),"],\n");
AppendTo(stream," \"transitive\":",Bool(trans),",\n");
AppendTo(stream," \"subdegrees\":[",JoinStringsWithSeparator(List(subdegrees,String),","),"],\n");
AppendTo(stream," \"rank\":",String(rank),",\n");
AppendTo(stream," \"conjugate_to_PSp4_3_point_action\":",Bool(conjP),",\n");
AppendTo(stream," \"conjugate_to_full_W33_aut_action\":",Bool(conjFull),",\n");
AppendTo(stream," \"valency12_orbital_srg\":{\"exists\":",Bool(degree=12),",\"strongly_regular\":",Bool(srgok),",\"lambda\":",String(lam),",\"mu\":",String(mu),"},\n");
AppendTo(stream," \"boundary\":\"This is the full F2-linear stabilizer of the concrete 23/40 projective split. A positive permutation conjugacy is an object-level binary model of the W33 point action; a mere equality of orders or orbit sizes is not promoted without the conjugacy test.\"\n");
AppendTo(stream,"}\n"); CloseStream(stream);;
Print("Pass7159 full GL6 stabilizer |Stab|=",Size(Stab)," induced=",Size(K40)," orbits=",orbs," subdegrees=",subdegrees," conjP=",conjP," conjFull=",conjFull,"\n");
QUIT;
