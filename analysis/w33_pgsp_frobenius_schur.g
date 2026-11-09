# Pass 12642: Frobenius-Schur indicators of PGSp(4,q) and PSp(4,q), q = 3, 5 (GAP; run: gap -q analysis/w33_pgsp_frobenius_schur.g)
for q in [3,5] do
  S := Sp(4,q); F := InvariantBilinearForm(S).matrix; a := PrimitiveRoot(GF(q)); D := fail;
  for t in Tuples(Filtered(Elements(GF(q)), x -> not IsZero(x)), 4) do
    M := DiagonalMat(t);
    if M * F * TransposedMat(M) = a * F then D := M; break; fi;
  od;
  if D = fail then Print("no diagonal similitude q=", q, "\n"); continue; fi;
  C := Group(Concatenation(GeneratorsOfGroup(S), [D]));
  G := Action(C, NormedRowVectors(GF(q)^4), OnLines);
  T := CharacterTable(G); ind := Indicator(T, 2);
  Print("q=", q, " |PGSp|=", Size(G), " irreps=", Length(ind), " FS +1/0/-1: ", [Number(ind, x->x=1), Number(ind, x->x=0), Number(ind, x->x=-1)], "\n");
  P := Action(S, NormedRowVectors(GF(q)^4), OnLines); ip := Indicator(CharacterTable(P), 2);
  Print("q=", q, " |PSp|=", Size(P), " FS +1/0/-1: ", [Number(ip, x->x=1), Number(ip, x->x=0), Number(ip, x->x=-1)], "\n");
od;
QUIT;
