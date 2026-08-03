from __future__ import annotations
import sys,itertools,collections,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
import numpy as np
import networkx as nx
sys.path.insert(0,str(Path(__file__).resolve().parent))
import w33_pass2553_pgsp_orbitals as r

G=r.actions(); rel,reps,sizes=r.orbitals(G)
print('group',len(G),'rank',len(reps))
pts=sorted({r.norm(v) for v in itertools.product(range(3),repeat=4) if any(v)}); pi={p:i for i,p in enumerate(pts)}
A=np.zeros((40,40),dtype=np.int8)
for i,j in itertools.combinations(range(40),2):
    if r.symp(pts[i],pts[j])==0:A[i,j]=A[j,i]=1
edges=[(i,j) for i,j in itertools.combinations(range(40),2) if A[i,j]]; ei={e:i for i,e in enumerate(edges)}
lines=set()
for i,j in edges:
    a=np.array(pts[i]);b=np.array(pts[j])
    lines.add(tuple(sorted({pi[r.norm((u*a+v*b)%3)] for u,v in itertools.product(range(3),repeat=2) if u or v})))
lines=sorted(lines)
frames=[(a,b) for a,b in itertools.combinations(range(40),2) if set(lines[a]).isdisjoint(lines[b])]
match=[]
for a,b in frames:
    mm=[]
    for x in lines[a]:
        ys=[y for y in lines[b] if A[x,y]]; assert len(ys)==1
        mm.append(tuple(sorted((x,ys[0]))))
    match.append(tuple(sorted(mm)))
assert len(frames)==540 and len(edges)==240
H=nx.Graph();H.add_nodes_from(range(540))
for i in range(540):
  for j in range(i+1,540):
    if int(rel[i,j]) in (13,16):H.add_edge(i,j)
comps=[tuple(sorted(c)) for c in nx.connected_components(H)]
assert len(comps)==45 and set(map(len,comps))=={12}
V4={(0,1,2,3),(1,0,3,2),(2,3,0,1),(3,2,1,0)}
def parity(p):return sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2
def compose(p,q):return tuple(p[q[i]] for i in range(4))
def coset_id(p):return tuple(sorted(compose(p,v) for v in V4))
records=[]; parity_counts=collections.Counter(); frame_to_block={f:k for k,C in enumerate(comps) for f in C};local_parts=[]
for bi,C in enumerate(comps):
    ec=collections.Counter(e for f in C for e in match[f]);assert len(ec)==16 and set(ec.values())=={3}
    used=set(x for e in ec for x in e); omitted=sorted(set(range(40))-used);assert len(used)==32 and len(omitted)==8
    O=nx.Graph();O.add_nodes_from(omitted);O.add_edges_from((x,y) for x,y in itertools.combinations(omitted,2) if A[x,y])
    assert nx.is_bipartite(O) and O.number_of_edges()==16 and set(dict(O.degree()).values())=={4}
    col=nx.bipartite.color(O);sides=sorted([tuple(sorted(x for x in omitted if col[x]==c)) for c in (0,1)]);L,R=sides;ri={x:i for i,x in enumerate(R)}
    perms={}
    for f in C:
        la,lb=frames[f];groups=collections.defaultdict(list)
        for x in omitted:
            pa=[y for y in lines[la] if A[x,y]];pb=[y for y in lines[lb] if A[x,y]];assert len(pa)==len(pb)==1;groups[(pa[0],pb[0])].append(x)
        assert len(groups)==4 and sorted(map(len,groups.values()))==[2,2,2,2]
        mp={}
        for pair,xs in groups.items():
            assert len(set(xs)&set(L))==1 and len(set(xs)&set(R))==1
            u=next(iter(set(xs)&set(L)));v=next(iter(set(xs)&set(R)));mp[u]=v
        p=tuple(ri[mp[u]] for u in L);assert sorted(p)==list(range(4));perms[f]=p
    assert len(set(perms.values()))==12;ph={parity(p) for p in perms.values()};assert len(ph)==1;par=next(iter(ph));parity_counts[par]+=1
    cosets=collections.defaultdict(list)
    for f,p in perms.items():cosets[coset_id(p)].append(f)
    assert len(cosets)==3 and sorted(map(len,cosets.values()))==[4,4,4]
    cosetparts={tuple(sorted(v)) for v in cosets.values()}
    H7=nx.Graph();H7.add_nodes_from(C);H7.add_edges_from((a,b) for a,b in itertools.combinations(C,2) if int(rel[a,b])==16)
    r7parts={tuple(sorted(c)) for c in nx.connected_components(H7)};assert cosetparts==r7parts and sorted(map(len,r7parts))==[4,4,4]
    for a,b in itertools.combinations(C,2):
        same=any(a in D and b in D for D in r7parts);assert int(rel[a,b])==(16 if same else 13)
    parts=sorted(r7parts);local_parts.append(parts)
    records.append({'block':bi,'frames':list(C),'omitted_k44_sides':[list(L),list(R)],'matching_edge_count':len(ec),'matching_edge_multiplicity':3,'permutation_parity':'even' if par==0 else 'odd','permutations':{str(f):list(perms[f]) for f in C},'v4_cosets':[list(x) for x in parts]})
block_perms=[]
for g in G:
    p=[]
    for C in comps:
        im={frame_to_block[g[f]] for f in C};assert len(im)==1;p.append(next(iter(im)))
    block_perms.append(tuple(p))
block_action=set(block_perms);stab_idx=[i for i,p in enumerate(block_perms) if p[0]==0];parts0=local_parts[0];part_actions=set();frame_actions=set()
for gi in stab_idx:
    g=G[gi];pa=[]
    for C in parts0:
        im={next(j for j,D in enumerate(parts0) if g[f] in D) for f in C};assert len(im)==1;pa.append(next(iter(im)))
    part_actions.add(tuple(pa));frame_actions.add(tuple(g[f] for f in comps[0]))
quotient_profiles=collections.Counter()
for i,j in itertools.combinations(range(45),2):quotient_profiles[tuple(sorted(collections.Counter(int(rel[a,b]) for a in comps[i] for b in comps[j]).items()))]+=1
out={'schema':'w33.pass2553.rank9_octet_a4_v4_decoder.v1','status':'PASS_RANK9_BLOCK_TOWER_DECODED_AS_45_K44_OCTETS_TIMES_A4_OVER_V4','carrier':540,'theorem':'Each of the 45 canonical twelve-frame imprimitivity blocks is attached to an omitted geometric K4,4 on eight W33 points. Its twelve frames induce exactly one parity half of the 24 perfect matchings of that K4,4, hence form an A4 torsor. Relation 16 is equality of the three V4 cosets in A4, giving three K4 graphs, while relation 13 joins distinct cosets, giving K4,4,4; their union is K12.','block_model':{'blocks':45,'frames_per_block':12,'local_object':'one parity half of Match(K4,4) = A4 torsor','normal_subgroup':'V4','quotient':'A4/V4 = C3','relation_16':'3 K4','relation_13':'K4,4,4','union':'K12'},'parity_block_counts':{'even':parity_counts[0],'odd':parity_counts[1]},'group_action':{'pgsp_or_effective_action_order':len(G),'induced_block_action_order':len(block_action),'block_orbit_size':len({p[0] for p in block_action}),'block_stabilizer_order':len(stab_idx),'induced_three_part_action_order':len(part_actions),'induced_three_part_permutations':[list(x) for x in sorted(part_actions)],'induced_local_frame_action_order':len(frame_actions)},'quotient_relation_profile_count':len(quotient_profiles),'quotient_relation_profiles':[{'histogram':[[a,b] for a,b in k],'block_pairs':v} for k,v in sorted(quotient_profiles.items())],'records':records,'checks':{'45_blocks':len(comps)==45,'12_frames_each':all(len(C)==12 for C in comps),'all_omitted_graphs_K44':True,'all_local_matchings_distinct_12':True,'all_local_matchings_one_parity':sum(parity_counts.values())==45,'all_relation16_v4_cosets':True,'all_relation13_cross_cosets':True,'block_action_transitive':len({p[0] for p in block_action})==45,'local_part_action_transitive':len({p[0] for p in part_actions})==3}}
base=dict(out);out['sha256_without_hash_field']=hashlib.sha256(json.dumps(base,sort_keys=True,separators=(',',':')).encode()).hexdigest();json.dump(out,open(ROOT/'data/w33_pass2553_rank9_octet_a4_v4_decoder.json','w'),indent=2,sort_keys=True)
