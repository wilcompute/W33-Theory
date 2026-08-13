#!/usr/bin/env python3
"""Pass5052-5055: resolve the 200-cover coherent configuration geometrically."""
from __future__ import annotations
import itertools,json,sys
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np, networkx as nx
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from analysis.w33_pass4992_4999_common import build_base

O52=ROOT/'data/PART_W33_PASS5052_200_COVER_ORBITAL_DICTIONARY.json'
O53=ROOT/'data/PART_W33_PASS5053_COVER_GRAM_RECONSTRUCTS_W33.json'
O54=ROOT/'data/PART_W33_PASS5054_OVERLAP6_DIRECTED_EDGE_CARRIER.json'
O55=ROOT/'data/PART_W33_PASS5055_POINT_FLAG_V24_SUBFRAMES.json'

def exact_covers(T):
    through=[[] for _ in range(27)]
    for i,t in enumerate(T):
        for x in t: through[x].append(i)
    out=[]
    def bt(ch,rem):
        if not rem:
            if len(ch)==9: out.append(tuple(sorted(ch)))
            return
        if len(ch)>=9:return
        x=min(rem,key=lambda q:sum(set(T[i])<=rem for i in through[q]))
        for i in through[x]:
            S=set(T[i])
            if S<=rem:bt(ch+[i],rem-S)
    bt([],set(range(27)))
    out=sorted(set(out)); assert len(out)==200
    return out

def build_labels(b,covers):
    T=b['tritangents'];M=b['M'];DS=b['DS'];spreads=b['spreads'];iso=b['iso_ds_sp'];L=b['L']
    AT=nx.Graph();AT.add_nodes_from(range(45))
    for i,j in itertools.combinations(range(45),2):
        if len(set(T[i])&set(T[j]))==1:AT.add_edge(i,j)
    indep=[frozenset(s) for s in itertools.combinations(range(45),3)
           if all(not AT.has_edge(*e) for e in itertools.combinations(s,2))]
    circuits={}
    for A in indep:
        common=set(range(45))
        for a in A: common&=set(AT.neighbors(a))
        for Bt in itertools.combinations(sorted(common-A),3):
            B=frozenset(Bt)
            if all(not AT.has_edge(*e) for e in itertools.combinations(B,2)):
                key=tuple(sorted((tuple(sorted(A)),tuple(sorted(B)))))
                circuits[key]=(A,B)
    assert len(circuits)==120
    line_circs=defaultdict(list)
    for A,B in circuits.values():
        six=sorted(A|B);miss=[d for d in range(36) if M[six,d].sum()==0];assert len(miss)==3
        common=set.intersection(*(set(spreads[iso[d]]) for d in miss));assert len(common)==1
        line_circs[next(iter(common))].append((A,B))
    assert len(line_circs)==40 and {len(v) for v in line_circs.values()}=={3}
    ci={c:i for i,c in enumerate(covers)};cover_lines=defaultdict(list);bits_of={};cover_of={}
    for q in range(40):
        for bits in itertools.product((0,1),repeat=3):
            U=set()
            for bit,(A,B) in zip(bits,line_circs[q]):U|=set(A if bit==0 else B)
            k=ci[tuple(sorted(U))];cover_lines[k].append(q);bits_of[(q,k)]=bits;cover_of[(q,bits)]=k
    assert Counter(map(len,cover_lines.values()))==Counter({1:160,4:40})
    pcover={};special_point={}
    for k,qs in cover_lines.items():
        if len(qs)!=4:continue
        z=set(L[qs[0]])
        for q in qs[1:]:z&=set(L[q])
        assert len(z)==1;p=next(iter(z));pcover[p]=k;special_point[k]=p
    assert len(pcover)==40
    fcover={}
    for k,qs in cover_lines.items():
        if len(qs)!=1:continue
        q=qs[0];bits=bits_of[(q,k)];opp=cover_of[(q,tuple(1-x for x in bits))]
        p=special_point[opp];assert p in L[q];fcover[(p,q)]=k
    assert len(fcover)==160
    return pcover,fcover

def main():
    b=build_base();T=b['tritangents'];W=b['W'];L=b['L'];covers=exact_covers(T)
    pcover,fcover=build_labels(b,covers);S=[set(c) for c in covers]
    def ov(a,b):return len(S[a]&S[b])
    # Pass5052: exact geometric dictionary of all 19 ordered orbitals.
    d52={
      'pass':5052,'status':'PASS','fibers':{'point_covers':40,'flag_covers':160},'ordered_orbitals':19,
      'PP':[
       {'relation':'identity','subdegree':1,'cover_overlap':9},
       {'relation':'distinct collinear points','subdegree':12,'cover_overlap':3},
       {'relation':'noncollinear points','subdegree':27,'cover_overlap':1}],
      'PF_from_point_p_to_flag_rq':[
       {'relation':'p=r','subdegree':4,'cover_overlap':0},
       {'relation':'p on q and p!=r','subdegree':12,'cover_overlap':6},
       {'relation':'p collinear r but p not on q','subdegree':36,'cover_overlap':0},
       {'relation':'p noncollinear r','subdegree':108,'cover_overlap':2}],
      'FP_from_flag_rq_to_point_p':[
       {'relation':'p=r','subdegree':1,'cover_overlap':0},
       {'relation':'p on q and p!=r','subdegree':3,'cover_overlap':6},
       {'relation':'p collinear r but p not on q','subdegree':9,'cover_overlap':0},
       {'relation':'p noncollinear r','subdegree':27,'cover_overlap':2}],
      'FF_from_flag_pq_to_flag_rs':[
       {'relation':'same flag','subdegree':1,'cover_overlap':9,'weyl_length':0},
       {'relation':'same line q=s, p!=r','subdegree':3,'cover_overlap':3,'weyl_length':1},
       {'relation':'same point p=r, q!=s','subdegree':3,'cover_overlap':0,'weyl_length':1},
       {'relation':'target point r lies on source line q, s!=q','subdegree':9,'cover_overlap':0,'weyl_length':2},
       {'relation':'source point p lies on target line s, q!=s','subdegree':9,'cover_overlap':0,'weyl_length':2},
       {'relation':'source/target points collinear on a third line; q,s disjoint','subdegree':27,'cover_overlap':3,'weyl_length':3},
       {'relation':'source/target lines meet in a third point; p,r noncollinear','subdegree':27,'cover_overlap':4,'weyl_length':3},
       {'relation':'opposite flags: p,r noncollinear and q,s disjoint','subdegree':81,'cover_overlap':1,'weyl_length':4}],
      'theorem':'The 19 Pass5018 orbitals are exactly the natural point/flag relative-position relations of W(3,3); cover-tritangent intersection is constant on every orbital.'}
    # Verify every dictionary entry by direct enumeration.
    cp=Counter();cf=Counter();cff=Counter()
    for p in range(40):
      for r in range(40):
       lab='identity' if p==r else ('distinct collinear points' if W.has_edge(p,r) else 'noncollinear points')
       cp[(lab,ov(pcover[p],pcover[r]))]+=1
      for (r,q),k in fcover.items():
       if p==r:lab='p=r'
       elif p in L[q]:lab='p on q and p!=r'
       elif W.has_edge(p,r):lab='p collinear r but p not on q'
       else:lab='p noncollinear r'
       cf[(lab,ov(pcover[p],k))]+=1
    for (p,q),a in fcover.items():
      for (r,s),c in fcover.items():
       if p==r and q==s:lab='same flag'
       elif q==s:lab='same line q=s, p!=r'
       elif p==r:lab='same point p=r, q!=s'
       elif r in L[q]:lab='target point r lies on source line q, s!=q'
       elif p in L[s]:lab='source point p lies on target line s, q!=s'
       elif W.has_edge(p,r):lab='source/target points collinear on a third line; q,s disjoint'
       elif set(L[q])&set(L[s]):lab='source/target lines meet in a third point; p,r noncollinear'
       else:lab='opposite flags: p,r noncollinear and q,s disjoint'
       cff[(lab,ov(a,c))]+=1
    assert sorted(x['subdegree'] for x in d52['PP'])==[1,12,27]
    for x in d52['PP']:assert cp[(x['relation'],x['cover_overlap'])]==40*x['subdegree']
    for x in d52['PF_from_point_p_to_flag_rq']:assert cf[(x['relation'],x['cover_overlap'])]==40*x['subdegree']
    for x in d52['FF_from_flag_pq_to_flag_rs']:assert cff[(x['relation'],x['cover_overlap'])]==160*x['subdegree']
    O52.write_text(json.dumps(d52,indent=2,sort_keys=True)+'\n')
    # Pass5053: raw Gram alone reconstructs fibers, point graph, lines and every flag.
    order=[pcover[p] for p in range(40)]+[fcover[(p,q)] for p in range(40) for q in range(40) if p in L[q]]
    G=np.array([[ov(a,c) for c in order] for a in order],dtype=int)
    hist=[dict(sorted(Counter(map(int,row)).items())) for row in G]
    hp={0:40,1:27,2:108,3:12,6:12,9:1};hf={0:31,1:81,2:27,3:30,4:27,6:3,9:1}
    assert all(h==hp for h in hist[:40]) and all(h==hf for h in hist[40:])
    Ap=(G[:40,:40]==3).astype(int);np.fill_diagonal(Ap,0)
    assert np.array_equal(Ap,nx.to_numpy_array(W,nodelist=range(40),dtype=int))
    rows_flags=[(p,q) for p in range(40) for q in range(40) if p in L[q]]
    for j,(p,q) in enumerate(rows_flags,40):
      tri=set(np.flatnonzero(G[j,:40]==6));assert len(tri)==3 and tri==set(L[q])-{p}
      Ks=[set(c) for c in nx.find_cliques(W) if len(c)==4 and tri<=set(c)];assert len(Ks)==1 and Ks[0]-tri=={p}
    d53={'pass':5053,'status':'PASS','Gram_shape':[200,200],'entry_values':[0,1,2,3,4,6,9],
      'row_histogram_point':hp,'row_histogram_flag':hf,
      'reconstruction':['row histogram separates 40 point-covers from 160 flag-covers','overlap 3 on the 40-fiber is exactly W33 collinearity','maximal K4s recover the 40 W33 lines','for flag F_(p,q), its three overlap-6 point rows are q\\{p}; their unique K4 completion recovers q and p'],
      'theorem':'The integer 200-cover Gram matrix reconstructs the full W33 point-line incidence geometry and the canonical labeling of all 160 flag-covers, up to automorphism.'}
    O53.write_text(json.dumps(d53,indent=2,sort_keys=True)+'\n')
    # Pass5054: Gram value 6 is precisely the 480 directed-edge/cube carrier.
    H=nx.Graph();H.add_nodes_from(range(200))
    for p in range(40):
      for j,(r,q) in enumerate(rows_flags,40):
       if G[p,j]==6:H.add_edge(p,j)
    assert H.number_of_edges()==480 and nx.is_connected(H)
    assert {H.degree(p) for p in range(40)}=={12} and {H.degree(j) for j in range(40,200)}=={3}
    for p in range(40):
      for j,(r,q) in enumerate(rows_flags,40):assert (H.has_edge(p,j)==(p in L[q] and p!=r))
    spec=np.linalg.eigvalsh(nx.to_numpy_array(H,dtype=float));rounded=Counter(round(float(x)) for x in spec)
    assert rounded==Counter({0:120,4:24,-4:24,2:15,-2:15,6:1,-6:1})
    d54={'pass':5054,'status':'PASS','extraction_rule':'cross-fiber Gram entry = 6','vertices':200,'edges':480,
      'degree_profile':{'point_covers':12,'flag_covers':3},'canonical_edge':'P_p -- F_(r,q) iff p in q and p!=r; equivalently directed W33 edge r->p on q',
      'spectrum':{'6':1,'4':24,'2':15,'0':120,'-2':15,'-4':24,'-6':1},
      'theorem':'The Pass5020 glued-cube/directed-edge carrier is recoverable directly as the overlap-6 cross-fiber graph of the 200-cover Gram.'}
    O54.write_text(json.dumps(d54,indent=2,sort_keys=True)+'\n')
    # Pass5055: the two fibers independently form tight frames for the same tritangent V24.
    Up=np.array([[1 if t in S[pcover[p]] else 0 for t in range(45)] for p in range(40)],dtype=int)
    flags=rows_flags;Uf=np.array([[1 if t in S[fcover[f]] else 0 for t in range(45)] for f in flags],dtype=int)
    At=np.zeros((45,45),dtype=int)
    for i,j in itertools.combinations(range(45),2):
      if len(set(T[i])&set(T[j]))==1:At[i,j]=At[j,i]=1
    H24=15*np.eye(45,dtype=int)-5*At+np.ones((45,45),dtype=int) # =30 P24
    Wp=5*Up-np.ones_like(Up);Wf=5*Uf-np.ones_like(Uf)
    assert np.array_equal(Wp.T@Wp,10*H24) and np.array_equal(Wf.T@Wf,40*H24)
    assert np.linalg.matrix_rank(Wp)==24 and np.linalg.matrix_rank(Wf)==24
    cross=Wp@Wf.T;ev=np.linalg.eigvalsh((cross@cross.T).astype(float));assert sum(np.isclose(ev,360000))==24 and sum(np.isclose(ev,0))==16
    d55={'pass':5055,'status':'PASS','integer_centering':'W=5U-J','point_frame':{'vectors':40,'rank':24,'row_norm_squared':180,'frame_operator':'Wp^T Wp = 10(15I-5A_trit+J) = 300 P24'},
      'flag_frame':{'vectors':160,'rank':24,'row_norm_squared':180,'frame_operator':'Wf^T Wf = 40(15I-5A_trit+J) = 1200 P24'},
      'cross_transform':{'rank':24,'nonzero_squared_singular_value':360000,'multiplicity':24},
      'theorem':'The 40 point-covers and 160 flag-covers are separately equal-norm tight frames for the same canonical tritangent V24; their frame bounds differ by exactly 4, matching the fiber-size ratio.'}
    O55.write_text(json.dumps(d55,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'5052':d52,'5053':d53,'5054':d54,'5055':d55},indent=2,sort_keys=True))
if __name__=='__main__':main()
