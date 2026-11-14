# Pass 1023: factor the Pass-1022 C6 obstruction into its coprime layers.
#
# The 240-root bundle has both invariant intermediate quotients
#
#   240 roots -> 120 antipodal pairs -> 40 Eisenstein lines
#   240 roots ->  80 omega triples   -> 40 Eisenstein lines.
#
# This certificate computes both stabilizer chains and proves that every
# nontrivial layer has regular local monodromy and no full K-equivariant section.

Read("analysis/w33_e8_c6_bundle_common.g");;

REPO1023 := GAPInfo.SystemEnvironment.W33_REPO;;
OUT1023 := Concatenation(REPO1023, "/data/w33_pass1023_c6_factor_obstruction.json");;

Assert1023 := function(label, condition)
  if not condition then Error(Concatenation("Pass1023 assertion failed: ", label)); fi;
end;;

Main1023 := function()
  local data, K, pair, triple, fibre, pairsInFibre, triplesInFibre,
        H, P, T, L, rootPairHom, pairFibreHom, rootTripleHom,
        tripleFibreHom, phaseHom, checks, names, stream, name;

  data := BuildE8C6Bundle102x();
  K := data.K;
  pair := First(data.pairs, block -> 1 in block);
  triple := First(data.triples, block -> 1 in block);
  fibre := First(data.fibres, block -> 1 in block);
  pairsInFibre := ConstituentBlocks102x(fibre, data.pairs);
  triplesInFibre := ConstituentBlocks102x(fibre, data.triples);

  H := Stabilizer(K, 1);
  P := Stabilizer(K, pair, OnSets);
  T := Stabilizer(K, triple, OnSets);
  L := Stabilizer(K, fibre, OnSets);

  rootPairHom := ActionHomomorphism(P, pair, OnPoints);
  pairFibreHom := ActionHomomorphism(L, pairsInFibre, OnSets);
  rootTripleHom := ActionHomomorphism(T, triple, OnPoints);
  tripleFibreHom := ActionHomomorphism(L, triplesInFibre, OnSets);
  phaseHom := ActionHomomorphism(L, fibre, OnPoints);

  checks := rec();
  checks.substrate_counts_are_240_120_80_40 :=
    Length(data.roots)=240 and Length(data.pairs)=120 and
    Length(data.triples)=80 and Length(data.fibres)=40;
  checks.each_six_fibre_is_three_pairs_and_two_triples :=
    Length(pairsInFibre)=3 and Length(triplesInFibre)=2 and
    Sum(pairsInFibre, Length)=6 and Sum(triplesInFibre, Length)=6;
  checks.stabilizer_orders_are_216_432_648_1296 :=
    [Size(H),Size(P),Size(T),Size(L)] = [216,432,648,1296];
  checks.H_is_normal_in_P_T_and_L :=
    IsNormal(P,H) and IsNormal(T,H) and IsNormal(L,H);
  checks.P_and_T_are_normal_in_L := IsNormal(L,P) and IsNormal(L,T);
  checks.sign_layer_index_is_two := Index(P,H)=2;
  checks.qutrit_layer_index_is_three := Index(L,P)=3;
  checks.omega_layer_index_is_three := Index(T,H)=3;
  checks.residual_sign_index_is_two := Index(L,T)=2;
  checks.root_to_pair_monodromy_is_regular_C2 :=
    Size(Image(rootPairHom))=2 and IsCyclic(Image(rootPairHom)) and
    IsTransitive(Image(rootPairHom),[1..2]);
  checks.pair_to_fibre_monodromy_is_regular_C3 :=
    Size(Image(pairFibreHom))=3 and IsCyclic(Image(pairFibreHom)) and
    IsTransitive(Image(pairFibreHom),[1..3]);
  checks.root_to_triple_monodromy_is_regular_C3 :=
    Size(Image(rootTripleHom))=3 and IsCyclic(Image(rootTripleHom)) and
    IsTransitive(Image(rootTripleHom),[1..3]);
  checks.triple_to_fibre_monodromy_is_regular_C2 :=
    Size(Image(tripleFibreHom))=2 and IsCyclic(Image(tripleFibreHom)) and
    IsTransitive(Image(tripleFibreHom),[1..2]);
  checks.full_phase_monodromy_is_regular_C6 :=
    Size(Image(phaseHom))=6 and IsCyclic(Image(phaseHom)) and
    IsTransitive(Image(phaseHom),[1..6]);
  checks.root_pair_kernel_is_H := Kernel(rootPairHom)=H;
  checks.pair_fibre_kernel_is_P := Kernel(pairFibreHom)=P;
  checks.root_triple_kernel_is_H := Kernel(rootTripleHom)=H;
  checks.triple_fibre_kernel_is_T := Kernel(tripleFibreHom)=T;
  checks.no_K_section_roots_to_pairs := not AdmitsPointSection102x(K,data.pairs);
  checks.no_K_section_pairs_to_fibres :=
    not AdmitsBlockSection102x(K,data.fibres,data.pairs);
  checks.no_K_section_roots_to_triples := not AdmitsPointSection102x(K,data.triples);
  checks.no_K_section_triples_to_fibres :=
    not AdmitsBlockSection102x(K,data.fibres,data.triples);
  checks.center_is_exact_sign_kernel :=
    Size(data.center)=2 and data.center=Group(data.neg) and
    Kernel(ActionHomomorphism(K,data.pairs,OnSets))=data.center;
  checks.C2_and_C3_projections_are_both_nonzero :=
    checks.no_K_section_roots_to_pairs and checks.no_K_section_pairs_to_fibres;
  checks.coprime_phase_orders_reconstruct_six :=
    Gcd(2,3)=1 and 2*3=6 and Size(Image(phaseHom))=6;

  names := RecNames(checks);
  Assert1023("all checks", ForAll(names, name -> checks.(name)));

  stream := OutputTextFile(OUT1023, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1023.c6_factor_obstruction.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"The C6 phase obstruction factors into independent nonzero sign-C2 and qutrit-C3 projections. Both intermediate bundles have regular local monodromy and neither admits a full Sp(4,3)-equivariant section.\",\n");
  WriteAll(stream, "  \"counts\": {\"roots\":240,\"antipodal_pairs\":120,\"omega_triples\":80,\"base_points\":40},\n");
  WriteAll(stream, "  \"sign_then_qutrit_chain\": {\n");
  WriteAll(stream, "    \"tower\": \"240 roots -> 120 antipodal pairs -> 40 Eisenstein lines\",\n");
  WriteAll(stream, Concatenation("    \"stabilizer_orders\": ",String([Size(H),Size(P),Size(L)]),",\n"));
  WriteAll(stream, "    \"exact_indices\": [2,3],\n");
  WriteAll(stream, "    \"local_monodromy\": [\"C2 regular\",\"C3 regular\"],\n");
  WriteAll(stream, "    \"sections\": [false,false]\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"qutrit_then_sign_chain\": {\n");
  WriteAll(stream, "    \"tower\": \"240 roots -> 80 omega triples -> 40 Eisenstein lines\",\n");
  WriteAll(stream, Concatenation("    \"stabilizer_orders\": ",String([Size(H),Size(T),Size(L)]),",\n"));
  WriteAll(stream, "    \"exact_indices\": [3,2],\n");
  WriteAll(stream, "    \"local_monodromy\": [\"C3 regular\",\"C2 regular\"],\n");
  WriteAll(stream, "    \"sections\": [false,false]\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"verdict\": {\n");
  WriteAll(stream, "    \"C2_projection_nonzero\": true,\n");
  WriteAll(stream, "    \"C3_projection_nonzero\": true,\n");
  WriteAll(stream, "    \"coefficient_decomposition\": \"C6 = C2 x C3 by the Chinese remainder theorem\",\n");
  WriteAll(stream, "    \"boundary\": \"This is a direct-product decomposition of the phase coefficient and its projected section obstructions; it does not assert that the nonabelian extension L over H splits.\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool102x(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass1023 status=PASS checks=",Length(names)," output=",OUT1023,"\n");
end;;

Main1023();;
QUIT;
