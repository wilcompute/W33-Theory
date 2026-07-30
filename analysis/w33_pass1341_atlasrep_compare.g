# Pass 1341: genuine GAP/AtlasRep/Repsn comparison surface.
#
# The Python certificate freezes a literal rational 20-dimensional model for
# Atlas-standard generators c,d of W(E6)=U4(2).2. This GAP program independently
# affords every degree-20 Atlas character and freezes image sizes, generator
# orders, and CTblLib rows. Equality is character-level (basis independent),
# not a claim that two arbitrary afforded bases are byte-identical.

SizeScreen([10000,10000]);
Assert1341 := function(label, condition)
    if not condition then Error(Concatenation("Pass 1341 failed: ",label)); fi;
    Print("PASS: ",label,"\n");
end;

Assert1341("AtlasRep loaded",LoadPackage("atlasrep")=true);
Assert1341("CTblLib loaded",LoadPackage("ctbllib")=true);
Assert1341("TomLib loaded",LoadPackage("tomlib")=true);
Assert1341("Repsn loaded",LoadPackage("repsn")=true);

G:=AtlasGroup("U4(2).2");
Assert1341("Atlas group exists",G<>fail);
Assert1341("Atlas group order 51840",Size(G)=51840);

tbl:=CharacterTable("U4(2).2");;
irrTbl:=Irr(tbl);;
pos20:=Filtered([1..Length(irrTbl)],i->irrTbl[i][1]=20);;
Assert1341("three degree-20 CTblLib rows",Length(pos20)=3);

irrG:=Irr(G);;
pos20G:=Filtered([1..Length(irrG)],i->irrG[i][1]=20);;
Assert1341("three degree-20 Atlas-group rows",Length(pos20G)=3);

records:=[];;
for i in pos20G do
    rho:=IrreducibleAffordingRepresentation(irrG[i]);;
    Assert1341(Concatenation("affording representation ",String(i)),
        IsAffordingRepresentation(irrG[i],rho));
    mats:=List(GeneratorsOfGroup(G),g->Image(rho,g));;
    Assert1341(Concatenation("20x20 matrices ",String(i)),
        ForAll(mats,m->DimensionsMat(m)=[20,20]));
    Add(records,rec(
        character_position:=i,
        image_order:=Size(Image(rho)),
        generator_orders:=List(mats,Order),
        traces:=List(mats,TraceMat)
    ));
od;

tom:=TableOfMarks("U4(2).2");;
orders:=OrdersTom(tom);;
permchars:=PermCharsTom(tbl,tom);;
rows432:=Filtered([1..Length(orders)],i->orders[i]=120 and permchars[i][1]=432);;
rows480:=Filtered([1..Length(orders)],i->orders[i]=108 and permchars[i][1]=480);;
mult432:=List(rows432,i->List(pos20,j->ScalarProduct(permchars[i],irrTbl[j])));;
mult480:=List(rows480,i->List(pos20,j->ScalarProduct(permchars[i],irrTbl[j])));;
Assert1341("432 carrier has degree-20 multiplicity three",
    ForAny(mult432,x->SortedList(x)=[0,0,3]));
Assert1341("480 carrier has degree-20 multiplicity one",
    ForAny(mult480,x->SortedList(x)=[0,0,1]));

Print("RESULT degree20_table_positions=",pos20,"\n");
Print("RESULT afforded_records=",records,"\n");
Print("RESULT index432_records=",List([1..Length(rows432)],i->[rows432[i],mult432[i]]),"\n");
Print("RESULT index480_records=",List([1..Length(rows480)],i->[rows480[i],mult480[i]]),"\n");
Print("PASS 1341 COMPLETE\n");
QUIT_GAP(0);
