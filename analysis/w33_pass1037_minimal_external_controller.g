# Pass 1037: classify the minimal external orientation controller.
REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1037_minimal_external_controller.json");;
Assert37 := function(label,cond) if not cond then Error(Concatenation("Pass1037 failed: ",label)); fi; end;;
Bool37 := function(v) if v then return "true"; fi; return "false"; end;;

Main37 := function()
  local roots,v,i,j,si,sj,m,k,rootIndex,ReflPerm,simples,W,cox,w,C,N,Wplus,
        normalizerN,cosets,cosetAction,isMaxEven,simpleOrders,checks,names,
        stream,tag,r,G;
  roots := [];
  for i in [1..8] do for j in [i+1..8] do
    for si in [1,-1] do for sj in [1,-1] do
      v := ListWithIdenticalEntries(8,0); v[i]:=2*si; v[j]:=2*sj; Add(roots,v);
    od; od;
  od; od;
  for m in [0..255] do
    v := List([0..7],k->(-1)^(QuoInt(m,2^k) mod 2));
    if Number(v,x->x=-1) mod 2=0 then Add(roots,v); fi;
  od;
  Assert37("240 roots",Length(roots)=240);
  rootIndex := function(x) return Position(roots,x); end;
  ReflPerm := function(r) return PermList(List(roots,x->rootIndex(x-((x*r)/4)*r))); end;
  simples := [
    [1,-1,-1,-1,-1,-1,-1,1],[2,2,0,0,0,0,0,0],[-2,2,0,0,0,0,0,0],
    [0,-2,2,0,0,0,0,0],[0,0,-2,2,0,0,0,0],[0,0,0,-2,2,0,0,0],
    [0,0,0,0,-2,2,0,0],[0,0,0,0,0,-2,2,0] ];
  W := Group(List(simples,ReflPerm));
  Assert37("W(E8) order",Size(W)=696729600);
  cox := Product(List(simples,ReflPerm)); w := cox^10;
  C := Centralizer(W,w); N := Normalizer(W,Group(w)); Wplus := DerivedSubgroup(W);
  normalizerN := Normalizer(W,N);

  # A subgroup H is maximal in G exactly when the transitive coset action G/H is
  # primitive.  This avoids optional convenience predicates and gives an exact
  # core-GAP certificate on the 1120 right cosets of N in W(E8)^+.
  cosets := RightCosets(Wplus,N);
  cosetAction := Action(Wplus,cosets,OnRight);
  isMaxEven := IsPrimitive(cosetAction,[1..Length(cosets)]);

  simpleOrders := [];
  for r in List(simples,ReflPerm) do
    G := Group(Concatenation(GeneratorsOfGroup(N),[r])); Add(simpleOrders,Size(G));
  od;
  checks := rec();
  checks.WE8_order_is_696729600 := Size(W)=696729600;
  checks.rotation_subgroup_has_index_two := Size(Wplus)=348364800 and Index(W,Wplus)=2;
  checks.centraliser_order_is_155520 := Size(C)=155520;
  checks.eisenstein_normaliser_order_is_311040 := Size(N)=311040;
  checks.N_lies_in_rotation_subgroup := IsSubgroup(Wplus,N);
  checks.coset_action_degree_is_1120 := Length(cosets)=1120;
  checks.N_is_maximal_in_rotation_subgroup := isMaxEven;
  checks.N_is_self_normalising_in_WE8 := normalizerN=N;
  checks.all_simple_reflections_generate_full_WE8_with_N := Set(simpleOrders)=[696729600];
  checks.abstract_split_controller_lower_bound_is_622080 := 2*Size(N)=622080;
  checks.embedded_reflection_controller_is_full_WE8 := isMaxEven and normalizerN=N and Set(simpleOrders)=[Size(W)];
  names := RecNames(checks); Assert37("all checks",ForAll(names,tag->checks.(tag)));
  stream := OutputTextFile(OUT,false); SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass1037.minimal_external_controller.gap.v2\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"The minimal abstract detached orientation controller is a split external C2, giving N x C2 of order 622080. Inside W(E8), N is self-normalising and maximal in the even Weyl subgroup, so adjoining any orientation-reversing element generates all W(E8), order 696729600.\",\n");
  WriteAll(stream,Concatenation("  \"orders\": {\"N\":",String(Size(N)),",\"N_times_C2\":",String(2*Size(N)),",\"Wplus\":",String(Size(Wplus)),",\"WE8\":",String(Size(W)),"},\n"));
  WriteAll(stream,Concatenation("  \"coset_action_degree\": ",String(Length(cosets)),",\n"));
  WriteAll(stream,Concatenation("  \"coset_action_primitive\": ",Bool37(isMaxEven),",\n"));
  WriteAll(stream,Concatenation("  \"N_self_normalising\": ",Bool37(normalizerN=N),",\n"));
  WriteAll(stream,Concatenation("  \"N_maximal_in_Wplus\": ",Bool37(isMaxEven),",\n"));
  WriteAll(stream,Concatenation("  \"simple_reflection_extension_orders\": ",String(simpleOrders),",\n"));
  WriteAll(stream,"  \"classification\": {\n");
  WriteAll(stream,"    \"detached_hardware\": \"N x C2, order 622080, is the order-minimal abstract split extension\",\n");
  WriteAll(stream,"    \"embedded_in_WE8\": \"W(E8), order 696729600\",\n");
  WriteAll(stream,"    \"reason\": \"The 1120-point coset action of W(E8)^+ on W(E8)^+/N is primitive, so N is maximal in W(E8)^+. N is also self-normalising in W(E8). Any odd element therefore enlarges the even part beyond N, hence to W(E8)^+, and its odd coset gives all W(E8).\"\n");
  WriteAll(stream,"  },\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for tag in names do
    WriteAll(stream,Concatenation("    \"",tag,"\": ",Bool37(checks.(tag))));
    if tag<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  },\n");
  WriteAll(stream,"  \"boundary\": \"N x C2 is an abstract detached controller, not a subgroup of W(E8). The embedded statement is exact inside W(E8).\"\n");
  WriteAll(stream,"}\n"); CloseStream(stream);
  Print("Pass1037 PASS N=",Size(N)," Wplus=",Size(Wplus)," W=",Size(W)," cosets=",Length(cosets),"\n");
end;;
Main37();;
QUIT;
