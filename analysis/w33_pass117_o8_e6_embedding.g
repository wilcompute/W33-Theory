# Pass 98 -- explicit W(E6) < O+_8(2):2 stabilizer chain.

F := GF(2);;
G := GO(1, 8, 2);;
V := Filtered(AsList(F^8), v -> not IsZero(v));;
orbits := Orbits(G, V, OnRight);;
iso := First(orbits, o -> Length(o) = 135);;
ani := First(orbits, o -> Length(o) = 120);;

a := ani[1];;
H := Stabilizer(G, a, OnRight);;
suborbits := Orbits(H, ani, OnRight);;
pairOrbit := First(suborbits, o -> Length(o) = 56);;
b := pairOrbit[1];;
K := Stabilizer(H, b, OnRight);;

L := SimpleLieAlgebra("E", 6, Rationals);;
WE6 := WeylGroup(RootSystem(L));;

Print("ambient_order=", Size(G), "\n");
Print("ambient_structure=", StructureDescription(G), "\n");
Print("isotropic_orbit=", Length(iso), "\n");
Print("anisotropic_orbit=", Length(ani), "\n");
Print("anisotropic_subdegrees=", List(suborbits, Length), "\n");
Print("ordered_pair_orbit=", Size(G) / Size(K), "\n");
Print("pair_stabilizer_order=", Size(K), "\n");
Print("pair_stabilizer_structure=", StructureDescription(K), "\n");
Print("weyl_e6_order=", Size(WE6), "\n");
Print("pair_stabilizer_iso_weyl_e6=", not IsomorphismGroups(K, WE6) = fail, "\n");
Print("weyl_e6_orbits_on_anisotropic=", SortedList(List(Orbits(K, ani, OnRight), Length)), "\n");
Print("weyl_e6_orbits_on_isotropic=", SortedList(List(Orbits(K, iso, OnRight), Length)), "\n");
QUIT;
