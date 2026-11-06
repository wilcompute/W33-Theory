from __future__ import annotations
import itertools,json
D4=[(a,b) for a in range(4) for b in range(2)];I=(0,0);FAULTS=[g for g in D4 if g!=I]
def mul(g,h):
 a,b=g;c,d=h;return ((a+(-1 if b else 1)*c)%4,(b+d)%2)
def inv(g):
 a,b=g;return ((-((-1 if b else 1)*a))%4,b)
V=range(10);EDGES=list(itertools.combinations(V,2));TRIS=list(itertools.combinations(V,3))
SCHEDULE=[(0,1,3),(0,2,9),(0,3,7),(0,4,5),(0,4,7),(0,4,8),(0,5,6),(0,6,9),(1,2,3),(1,2,6),(1,4,6),(1,4,8),(1,5,8),(1,5,9),(1,7,9),(2,3,4),(2,3,8),(2,4,7),(2,5,9),(2,6,7),(2,8,9),(3,5,9),(3,6,8),(3,6,9),(3,7,9),(4,8,9),(5,6,7),(5,7,8)]
SEL=[TRIS.index(t) for t in SCHEDULE]
def directed(edge,g,u,v):
 if (u,v)==edge:return g
 if (v,u)==edge:return inv(g)
 return I
def syndrome(hyp,selected=SEL):
 out=[]
 for ti in selected:
  i,j,k=TRIS[ti];p=I
  for u,v in ((i,j),(j,k),(k,i)):
   q=I
   for e,g in hyp:q=mul(directed(e,g,u,v),q)
   p=mul(q,p)
  out.append(p)
 return tuple(out)
H=[tuple()];H.extend(((e,g),) for e in EDGES for g in FAULTS);H.extend(((e,g),(f,h)) for e,f in itertools.combinations(EDGES,2) for g in FAULTS for h in FAULTS)
assert len(H)==48826;syn=[syndrome(h) for h in H];assert len(set(syn))==len(H)
CENTRAL=(2,0);supports=[()]+[(e,) for e in EDGES]+list(itertools.combinations(EDGES,2));cs=[syndrome(tuple((e,CENTRAL) for e in supp)) for supp in supports];assert len(set(cs))==len(cs)==1036
inc=[sum(1 for t in SCHEDULE if set(e).issubset(t)) for e in EDGES]
out={'schema':'w33.pass3004.d4_two_edge_schedule.v1','status':'COMPLETE_EXACT_28_TRIANGLE_CONSTRUCTION','fault_model':'no fault or one/two undirected K10 edges, each carrying one of seven nonidentity D4 elements; reverse edge carries inverse','hypotheses':len(H),'triangle_count':len(SCHEDULE),'schedule':[list(t) for t in SCHEDULE],'full_group_valued_syndromes_unique':True,'central_r2_supports_weight_le_2_unique':True,'central_support_count':len(supports),'edge_incidence_histogram':{str(k):inc.count(k) for k in sorted(set(inc))},'improvement_over_predecessor':{'old_triangle_count':29,'new_triangle_count':28,'saved_fraction':'1/29'},'optimality':'27 was searched by deterministic/local separation runs without a witness, but impossibility is not proved; the exact minimum remains in [23,28]. The lower endpoint is the proved single-edge incidence bound, while the central r^2 restriction supplies only the weaker binary information bound 2^m >= 1036.','boundary':'Exact discrete D4 permutation faults. Coherent partial faults, optical loss, and detector erasure are outside this theorem.'}
print(json.dumps(out,indent=2,sort_keys=True))
