# Independent finite-group homology control for the Klein-link quotient.
# This checks the group terms, not the homology of the seven-manifold itself.
if LoadPackage("hap") <> true then Error("HAP is required"); fi;
g := Group((1,2,3,4,5,6,7,8,9,10,11),
           PermList(List([0..10], a -> (9*a mod 11)+1)));;
if Size(g) <> 55 or IsAbelian(g) then Error("Wrong F55 group"); fi;
r := ResolutionFiniteGroup(g, 5);;
c := TensorWithIntegers(r);;
hs := List([1..4], n -> Homology(c, n));;
if hs <> [[5],[],[5],[]] then Error("Unexpected integral group homology"); fi;
Print("PASS F55 order=", Size(g), " H1..H4=", hs, "\n");
QUIT;
