# Pass 8041 -- is the qubit tower canonical? Census every 2-power class of 2.Co1.
#
# The tower L/2L -> L/(I-J)L -> L/(I-M)L needs J with pure support Phi_4^12 and M with pure
# support Phi_8^6. If several conjugacy classes qualify, the tower is a CHOICE; if one does,
# it is canonical. The character table settles it exhaustively, class by class, the same way
# Pass 8035 settled the order-9 question.
#
# DECODING. For an element of 2-power order in the 24-dimensional representation write the
# eigenvalue multiset as a copies of 1, b of -1, c blocks of Phi_4 and d blocks of Phi_8.
# Primitive 4th roots sum to 0 and primitive 8th roots sum to 0, each Phi_8 block squares to
# a Phi_4 block (sum 0) and each Phi_4 block squares to -1 twice, so
#
#     chi(1)   = a + b + 2c + 4d = 24
#     chi(g)   = a - b
#     chi(g^2) = a + b - 2c
#     chi(g^4) = a + b + 2c - 4d
#
# and the two pure cases are Phi_4^12 = (0,0,12,0) and Phi_8^6 = (0,0,0,6). Centraliser
# orders are reported too: they are what the tower's symmetry group actually is.

repo := GAPInfo.SystemEnvironment.W33_REPO;;
log  := Concatenation(repo, "/analysis/_co0_2power_classes.txt");;
PrintTo(log, "2-power classes of 2.Co1 in the 24-dimensional representation\n");

t := CharacterTable("2.Co1");;
irr := Irr(t);;
ords := OrdersClassRepresentatives(t);;
cents := SizesCentralizers(t);;
p2 := PowerMap(t, 2);;
deg24 := Filtered([1..Length(irr)], i -> DegreeOfCharacter(irr[i]) = 24);;
AppendTo(log, "degree-24 characters: ", Length(deg24), "\n");

chi := irr[deg24[1]];;
for o in [2, 4, 8] do
  AppendTo(log, "=== order ", o, " ===\n");
  npure := 0;
  for k in [1..Length(ords)] do
    if ords[k] = o then
      g1 := chi[k];
      g2 := chi[p2[k]];
      g4 := chi[p2[p2[k]]];
      # a-b = g1 ; a+b-2c = g2 ; a+b+2c-4d = g4 ; a+b+2c+4d = 24
      d := (24 - g4) / 8;
      apb2c := 24 - 4 * d;
      c := (apb2c - g2) / 4;
      apb := g2 + 2 * c;
      a := (apb + g1) / 2;
      b := apb - a;
      AppendTo(log, "  class ", k, " centraliser ", cents[k],
               "  chi ", g1, " ", g2, " ", g4,
               "  -> (a,b,c,d) = (", a, ",", b, ",", c, ",", d, ")");
      if a = 0 and b = 0 and (c = 12 or d = 6) and (c = 0 or d = 0) then
        AppendTo(log, "   *** PURE ***");
        npure := npure + 1;
      fi;
      AppendTo(log, "\n");
    fi;
  od;
  AppendTo(log, "  pure classes of order ", o, ": ", npure, "\n");
od;

QUIT;
