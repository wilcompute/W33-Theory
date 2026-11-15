#!/usr/bin/env python3
"""Exact sparse two-stage Kraus factorization of the full 40->27 four-copy
W33 map. NO numpy/scipy/networkx required: independent incidence replay.

Use the existing 45 eight-ray supports as canonical upstream evidence.
Nonedge pairs are uniquely those among 8-ray supports occurring exactly
once globally; all W33 graph edges occur in three supports.
U: 270 octet-pair mediator channels x 22680 distinct four-ray inputs.
B: 27 cubic-line labels x 270 mediators; each mediator belongs to one
five-octet clique, each label has ten mediator channels.
M = B U, with EXACT ||U||²=264, ||B||²=10, ||M||²=2640.
"""
import json
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"data"/"toe_20261115_apartment_octet_e6_27_45_dictionary.json"
OUT=ROOT/"data"/"toe_20261115_E6_270mode_two_stage_quantum_compiler.json"

def run():
  old=json.loads(SRC.read_text(encoding="utf8"))
  octets=[tuple(map(int,x)) for x in old["45_component_supports_in_our_point_indices"]]
  assert len(octets)==45 and len(set(octets))==45
  assert all(len(o)==8 and len(set(o))==8 for o in octets)
  pair_owner=defaultdict(list)
  for i,o in enumerate(octets):
    for p in combinations(o,2):pair_owner[p].append(i)
  pair_hist=Counter(len(v) for v in pair_owner.values())
  assert pair_hist=={1:540,3:240}
  nonedges=[[] for _ in range(45)]
  for p,owners in pair_owner.items():
    if len(owners)==1:nonedges[owners[0]].append(p)
  assert all(len(ps)==12 for ps in nonedges)
  support=[frozenset(o) for o in octets]
  edges=[(i,j) for i,j in combinations(range(45),2) if not(support[i]&support[j])]
  assert len(edges)==270
  neighbors=[set() for _ in range(45)]
  for i,j in edges:neighbors[i].add(j);neighbors[j].add(i)
  assert all(len(s)==12 for s in neighbors)
  # Backtracking 5-clique generation, no C(45,5) brute-force.
  cliques=[]
  def extend(tup,cands):
    if len(tup)==5:
      cliques.append(tuple(tup));return
    for index,x in enumerate(cands):
      extend(tup+[x],[y for y in cands[index+1:] if y in neighbors[x]])
  extend([],list(range(45)))
  assert len(cliques)==27 and all(len(x)==5 for x in cliques)
  edge_owner=defaultdict(list)
  for ell,clique in enumerate(cliques):
    for e in combinations(clique,2):edge_owner[e].append(ell)
  assert len(edge_owner)==270 and all(len(v)==1 for v in edge_owner.values())
  assert set(edge_owner)==set(edges)
  E={pair:i for i,pair in enumerate(edges)}
  four=defaultdict(list)
  for k,(i,j) in enumerate(edges):
    for p in nonedges[i]:
      for q in nonedges[j]:
        s=tuple(sorted(p+q))
        assert len(set(s))==4
        four[s].append(k)
  counts=Counter(len(v) for v in four.values())
  assert len(four)==22680 and counts=={1:6480,2:16200}
  diag=[0]*270
  degree=[0]*270
  overlap=Counter()
  G=[[0]*27 for _ in range(27)]
  for s,meds in four.items():
    ls=[edge_owner[edges[k]][0] for k in meds]
    for i in meds:
      diag[i]+=1
      degree[i]+=len(meds)
    if len(meds)==2:
      overlap[tuple(sorted(meds))]+=1
    for a in ls:
      for b in ls:G[a][b]+=1
  assert set(diag)=={144} and set(degree)=={264}
  assert sum(G[l][l] for l in range(27))==27*1440
  assert all(G[l][l]==1440 for l in range(27))
  A=[[int(len(set(cliques[i])&set(cliques[j]))==1) if i!=j else 0
      for j in range(27)] for i in range(27)]
  assert all(sum(row)==10 for row in A)
  assert all(G[i][j]==(1440 if i==j else 24 if A[i][j] else 60)
             for i in range(27) for j in range(27))
  assert all(sum(row)==2640 for row in G)
  # Every degree-two quartet is a two-rail edge of the 270-vertex
  # overlap graph; two different quartets duplicate each graph edge.
  # The 270 graph is 60-regular, with 27 ten-vertex independent fibers.
  assert all(v==2 for v in overlap.values())
  assert len(overlap)==8100 and 2*len(overlap)==16200
  for i,j in overlap:
    assert edge_owner[edges[i]]!=edge_owner[edges[j]]
  # The norm-one singular vector yields a special, ENTANGLED four-photon
  # state with 100% success. Amplitude is m(S)/sqrt(71280), where
  # m(S) is 1 or 2, never on repeated-occupation Fock states.
  assert 6480+4*16200==27*2640==71280
  # UUT is symmetric PSD, nonnegative with row sum264:
  # largest eigenvalue is 264 exactly. BBT=10I from disjoint
  # ten-edge line fibers. Uniform vectors saturate both norms.
  eigen={"uniform_1":2640,"schlafli_20":1344,"schlafli_dark_6":1560}
  assert 1440+10*24+16*60==eigen["uniform_1"]
  assert 1440+24-2*60==eigen["schlafli_20"]
  assert 1440-5*24+4*60==eigen["schlafli_dark_6"]
  result={
    "status":"EXACT_OPTIMAL_TWO_STAGE_W33_E6_270_MEDIATOR_KRAUS_FACTORIZATION",
    "upstream":"data/toe_20261115_apartment_octet_e6_27_45_dictionary.json",
    "nonedge_pair_unique_support_count":540,
    "graph_edge_triple_support_count":240,
    "octet_pair_mediator_modes":270,"four_distinct_point_inputs":22680,
    "final_cubic_line_modes":27,
    "first_stage_binary_U_shape":[270,22680],
    "first_stage_column_decomposition_hist":{"1":6480,"2":16200},
    "UUT_diagonal":144,"UUT_constant_row_sum":264,
    "UUT_lambda_max_exact":264,
    "UUT_offdiagonal_nonzero_entry_hist":{
      str(k):v for k,v in sorted(Counter(overlap.values()).items())},
    "UUT_offdiagonal_pairs_with_positive_overlap":len(overlap),
    "mediator_overlap_graph":"270 vertices, 60-regular, 8100 edges, each collision pair realized by precisely 2 distinct quartet inputs; each 10-element cubic-line fiber independent",
    "norm_one_singular_resource_fourphoton_amplitudes":"For every quartet S with decomposition m(S)=1 or 2: amplitude m(S)/sqrt(71280); all repeated-occupation basis amplitudes zero",
    "perfect_entangled_fourphoton_input_yields_success_probability":1,
    "perfect_entangled_fourphoton_input_output":"uniform |+27>=(1/sqrt(27))*sum_{ell=1}^{27}|ell>",
    "perfect_source_not_a_fourfold_tensor_power":True,
    "perfect_source_nonnormalization_trap":"The source is explicitly normalized because 6480*1^2+16200*2^2=71280; it is not any |psi>^tensor4 because all repeated-occupation Fock amplitudes vanish.",
    "B_B_transpose_exact":"10 I27",
    "second_stage_line_mediators_each":10,
    "M_M_transpose_diagonal":1440,
    "M_M_transpose_adjacent":24,
    "M_M_transpose_nonadjacent":60,
    "M_M_transpose_eigenvalues":eigen,
    "first_stage_success":"K1 = U/sqrt(264) acts on Sym4(C40) to C270; contractive",
    "second_stage_success":"K2 = B/sqrt(10) acts on C270 to C27; coisometry",
    "composition":"K2 K1 = (BU)/sqrt(2640) exactly the normalized one-step K",
    "no_extra_postselection_penalty_due_to_two_stages":True,
    "physical_compilation_stage2":"27 disjoint groups of 10 single-register modes, a ten-port coherent Fourier combiner per group; retain uniform port, discard orthogonal outputs.",
    "physical_compilation_stage1":"Sparse four-photon occupation -> 270-ancilla-mode contraction; requires genuinely multiphoton entangling measurement or quantum simulation; no passive linear optics circuit supplied.",
    "scope":"Exact incidence and operator-norm theorem. Stage2 optical passive interferometer on a virtual 270-mode single-excitation register is plausible; creating that register from four photon copies in stage1 remains uncompiled."
  }
  OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
  return result
if __name__=="__main__":
  d=run()
  print("PASS",d["status"],"intermediate",d["octet_pair_mediator_modes"],
        "U norm2",d["UUT_lambda_max_exact"],flush=True)
