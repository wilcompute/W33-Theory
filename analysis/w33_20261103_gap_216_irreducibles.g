# Exact complex character decomposition of both 216-coset S5 actions of PSp4(3).
# Distinguishes two conjugacy classes; no numerical eigenvalue fitting.
G:=PSp(4,3);;
tbl:=CharacterTable(G);;
irr:=Irr(G);;
max:=MaximalSubgroupClassReps(G);;
# S5 is not maximal in PSp4(3), but lies in the index-36 S6 maximal.
sixes:=Filtered(max,H->Size(H)=720);;
fives:=[];;
for S in sixes do
 for H in MaximalSubgroupClassReps(S) do
  if Size(H)=120 then Add(fives,H); fi;
 od;
od;;
res:=[];;
for H in fives do
  chi:=PermutationCharacter(G,H);;
  mult:=MatScalarProducts(irr,[chi])[1];;
  deg:=List(irr, x->x[1]);;
  Add(res,rec(sizeH:=Size(H),idH:=IdGroup(H),mult:=mult,degrees:=deg,character:=ValuesOfClassFunction(chi),
       dimension:=Sum([1..Length(irr)],i->mult[i]*deg[i])));
od;
out:=Concatenation(GAPInfo.SystemEnvironment.W33_REPO,"/data/w33_20261103_gap_216_irreducibles.txt");;
PrintTo(out,"Group=",Size(G),"\nMaximalS5=",Length(fives),"\n");;
for r in res do
 AppendTo(out,"S5 IdGroup=",r.idH,"\n");
 AppendTo(out,"Degrees=",r.degrees,"\n");
 AppendTo(out,"Multiplicities=",r.mult,"\n");
 AppendTo(out,"Dimension=",r.dimension,"\n");
 AppendTo(out,"Conjugacy character=",r.character,"\n");
od;
QUIT;
