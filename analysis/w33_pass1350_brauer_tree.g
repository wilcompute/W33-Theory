# Pass 1350: exact characteristic-5 block and Brauer-tree census for W(E6)=U4(2).2.
# This uses CTblLib's genuine ordinary and Brauer character tables.
LoadPackage("ctbllib");

T := CharacterTable("U4(2).2");;
if T = fail then Error("ordinary table U4(2).2 unavailable"); fi;
M := BrauerTable(T, 5);;
if M = fail then Error("5-modular Brauer table U4(2).2 unavailable"); fi;
BI := BlocksInfo(M);;
ORD := Irr(T);;
BRAUER_IRR := IBr(M);;

out := OutputTextFile("data/w33_pass1350_u42d2_char5_blocks.json", false);;
SetPrintFormattingStatus(out, false);;
AppendTo(out, "{\"schema\":\"w33.pass1350.u42d2.char5.blocks.v1\",\"group\":\"U4(2).2\",\"group_order\":", String(Size(T)), ",\"prime\":5,\"blocks\":[");
for i in [1..Length(BI)] do
  b := BI[i];;
  D := DecompositionMatrix(M, i);;
  if i > 1 then AppendTo(out, ","); fi;
  AppendTo(out, "{\"number\":", String(i));
  AppendTo(out, ",\"defect\":", String(b.defect));
  AppendTo(out, ",\"ordinary_positions\":", String(b.ordchars));
  AppendTo(out, ",\"ordinary_degrees\":", String(List(b.ordchars, j -> ORD[j][1])));
  AppendTo(out, ",\"brauer_positions\":", String(b.modchars));
  AppendTo(out, ",\"brauer_degrees\":", String(List(b.modchars, j -> BRAUER_IRR[j][1])));
  AppendTo(out, ",\"decomposition_matrix\":", String(D));
  if IsBound(b.brauertree) then
    AppendTo(out, ",\"brauer_tree\":", String(b.brauertree));
  else
    AppendTo(out, ",\"brauer_tree\":null");
  fi;
  AppendTo(out, "}");
od;
AppendTo(out, "]}");
CloseStream(out);

Print("PASS 1350: wrote data/w33_pass1350_u42d2_char5_blocks.json\n");
QUIT_GAP(0);
