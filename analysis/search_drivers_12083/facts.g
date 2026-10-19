S:=Sp(4,3);;
Print("Sp(4,3) perfect: ",DerivedSubgroup(S)=S,"\n");
W:=696729600;; Print("|W(E8)| = ",W," = ",Collected(Factors(W)),"\n");
A:=3^4*Size(S);; Print("|ASp(4,3)| = ",A,"  divides |W(E8)|: ",W mod A = 0,"\n");
G32:=DirectProduct(CyclicGroup(3),S);;
cl:=ComplementClassesRepresentatives(G32,Image(Embedding(G32,1)));;
Print("complement classes of the central 3 in 3 x Sp(4,3): ",Length(cl),"\n");
QUIT;
