# Pass 1075 companion: irreducible character table of the exact matrix group.
# This is intentionally separate from the native Python class fingerprint.
LoadPackage("ctbllib");
G := GeneralSymplecticGroup(4,3);
Print("size=",Size(G),"\n");
ct := CharacterTable(G);
Print("identifier=",Identifier(ct),"\n");
Print("classes=",NrConjugacyClasses(G),"\n");
Print("sizes=",SizesConjugacyClasses(ct),"\n");
Print("degrees=",List(Irr(ct),chi->chi[1]),"\n");
