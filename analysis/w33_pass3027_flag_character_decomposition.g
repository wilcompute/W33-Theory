# Pass 3027: exact decomposition of the 6480-flag permutation character.
# Requires GAP. CTblLib is not required because the explicit permutation group and
# explicit V4 flag stabilizer are supplied. Fail if any frozen invariant changes.

g1 := (2,3,4)(8,9,10)(11,13,12)(17,18,19)(20,22,21)(26,27,28)(29,31,30)(35,36,37)(38,40,39);
g2 := (1,4,3)(6,12,9)(7,10,13)(15,21,18)(16,19,22)(24,30,27)(25,28,31)(33,39,36)(34,37,40);
g3 := (14,23,32)(15,24,33)(16,25,34)(17,26,35)(18,27,36)(19,28,37)(20,29,38)(21,30,39)(22,31,40);
g4 := (2,9,12)(3,10,11)(4,8,13)(14,24,34)(15,25,32)(16,23,33)(17,37,27)(18,35,28)(19,36,26);
g5 := (5,32,23)(6,34,24)(7,33,25)(8,38,26)(9,40,27)(10,39,28)(11,35,29)(12,37,30)(13,36,31);
G := Group([g1,g2,g3,g4,g5]);
if Size(G) <> 25920 then Error("PSp(4,3) order drift"); fi;

h1 := (1,14)(2,5)(3,32)(4,23)(6,20)(7,17)(9,38)(10,26)(12,29)(13,35)(18,33)(19,25)(21,24)(22,34)(27,39)(31,37);
h2 := (2,20)(3,22)(4,21)(5,6)(8,30)(9,29)(10,31)(11,40)(12,38)(13,39)(15,16)(23,24)(26,37)(27,35)(28,36)(32,34);
H := Group([h1,h2]);
if Size(H) <> 4 or StructureDescription(H) <> "C2 x C2" then Error("flag stabilizer drift"); fi;
if not IsSubgroup(G,H) then Error("H is not a subgroup of G"); fi;

pi := PermutationCharacter(G,H);
if DegreeOfCharacter(pi) <> 6480 then Error("flag character degree drift"); fi;
if ScalarProduct(pi,pi) <> 1770 then Error("commutant dimension drift"); fi;

irr := Irr(G);
mult := List(irr,chi -> ScalarProduct(pi,chi));
records := Filtered([1..Length(irr)],i -> mult[i] <> 0);
Print("degree=",DegreeOfCharacter(pi),"\n");
Print("commutant=",ScalarProduct(pi,pi),"\n");
Print("nonzero constituents [index,degree,multiplicity]:\n");
for i in records do
  Print([i,DegreeOfCharacter(irr[i]),mult[i]],"\n");
od;
Print("dimension check=",Sum(records,i -> DegreeOfCharacter(irr[i])*mult[i]),"\n");
