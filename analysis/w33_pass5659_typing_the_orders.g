# Passes 5659-5662: type the orders instead of matching them.
#   5659  Which degree-12 action does the Reye 12 carry?
#   5660  How many TRANSITIVE degree-12 groups of order 576 exist at all?
#   5661  Type every constructible 576 and 1152 in this corpus by SmallGroup id.
#   5662  Does the 7-side ever meet the {2,3}-side?
LoadPackage("grape");;
BinaryXor2 := function(a,b)
  local i,r; r:=0;
  for i in [0..7] do
    if ((QuoInt(a,2^i) mod 2) + (QuoInt(b,2^i) mod 2)) mod 2 = 1 then r := r + 2^i; fi;
  od;
  return r;
end;;

inc := EvalString(StringFile("c:/Repos/Theory of Everything/data/tmp_reye16_levi.json"));;
n := 28;;
adj := List([1..n], i -> []);;
for e in inc do
  Add(adj[e[1]+1], e[2]+17);
  Add(adj[e[2]+17], e[1]+1);
od;;
levi := Graph(Group(()), [1..n], OnPoints,
              function(x,y) return y in adj[x]; end, true);;
A := AutomorphismGroup(levi);;
Print("Aut(Levi) order ", Size(A), " id ", IdSmallGroup(A), "\n");

# --- 5659: the induced action on the 12 configuration POINTS (nodes 17..28) -----
orbs := Orbits(A, [1..28]);;
Print("orbits on the Levi: ", List(orbs, Length), "\n");
twelve := First(orbs, o -> Length(o) = 12);;
sixteen := First(orbs, o -> Length(o) = 16);;
act12 := Action(A, twelve, OnPoints);;
act16 := Action(A, sixteen, OnPoints);;
Print("action on the 12 : order ", Size(act12), ", transitive ",
      IsTransitive(act12), ", faithful ", Size(act12) = Size(A), "\n");
Print("action on the 16 : order ", Size(act16), ", transitive ",
      IsTransitive(act16), ", faithful ", Size(act16) = Size(A), "\n");
st := Stabilizer(act12, 1);;
Print("point stabiliser of the 12: order ", Size(st), "  ",
      StructureDescription(st), "  id ", IdSmallGroup(st), "\n");
Print("TransitiveIdentification of the 12-action: ",
      TransitiveIdentification(act12), "\n");

# --- 5660: all transitive degree-12 groups of order 576 -------------------------
cands := Filtered([1..NrTransitiveGroups(12)],
                  k -> Size(TransitiveGroup(12,k)) = 576);;
Print("\ntransitive groups of degree 12 with order 576: ", Length(cands),
      "  -> ", cands, "\n");
W := WeylGroup(RootSystem(SimpleLieAlgebra("F",4,Rationals)));;
QW := W / Centre(W);;
Print("W(F4)/Z id = ", IdSmallGroup(QW), "\n");
for k in cands do
  T := TransitiveGroup(12,k);
  Print("   T12_", k, "  id ", IdSmallGroup(T),
        "   =~ W(F4)/Z : ", IdSmallGroup(T) = IdSmallGroup(QW), "\n");
od;

# --- 5661: type every constructible 576 / 1152 ---------------------------------
Print("\n--- typing the constructible orders ---\n");
S4wrS2 := WreathProduct(SymmetricGroup(4), SymmetricGroup(2));;
q4adj := List([1..16], i -> []);;
for i in [0..15] do
  for b in [0,1,2,3] do
    Add(q4adj[i+1], BinaryXor2(i, 2^b) + 1);
  od;
od;;
q4 := Graph(Group(()), [1..16], OnPoints,
            function(x,y) return y in q4adj[x]; end, true);;
tbl := [ [ "W(F4)", W ], [ "W(F4)/Z", QW ], [ "S4 wr S2", S4wrS2 ],
         [ "Aut(Reye Levi)", A ], [ "Aut(Q4)", AutomorphismGroup(q4) ],
         [ "Reye 12-action", act12 ], [ "Reye 16-action", act16 ] ];;
for p in tbl do
  Print("   ", p[1], ": order ", Size(p[2]), " id ", IdSmallGroup(p[2]), "\n");
od;

# --- 5662: does the 7-side meet the {2,3}-side? --------------------------------
Print("\n--- the 7-side ---\n");
L := PSL(2,7);;
Print("|PSL(2,7)| = ", Size(L), " = 2^3 * 3 * 7, id ", IdSmallGroup(L), "\n");
Print("576 * 7 = ", 576*7, "\n");
Print("does W(F4)/Z have order divisible by 7 : ", Size(QW) mod 7 = 0, "\n");
Print("does PSL(2,7) have a subgroup of order 576 : ",
      576 <= Size(L), "\n");
# The smallest group containing both as subgroups must have order divisible by
# lcm(576,168) and by 7.
Print("lcm(|W(F4)/Z|,|PSL(2,7)|) = ", Lcm(576,168), "\n");
Print("smallest symmetric group containing both: S12 has order ",
      Factorial(12), ", divisible by 576 and 168: ",
      (Factorial(12) mod 576 = 0) and (Factorial(12) mod 168 = 0), "\n");
QUIT;
