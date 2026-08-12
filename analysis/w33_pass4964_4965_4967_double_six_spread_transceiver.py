#!/usr/bin/env python3
"""Passes 4964,4965,4967 — double-six/spread bridge and two derived probes.

4964: construct the unique W(E6)=PGSp(4,3)-equivariant bijection between the
      36 cubic-surface double-sixes and the 36 spreads of W(3,3).
4965: transport the 120 Steiner triangles through that bijection.  Each W33 line
      lies in nine spreads, canonically partitioned into three Steiner triples;
      the local four-overlap graph is K_{3,3,3}.
4967: reinterpret line-spread incidence as a canonical double-six/line matrix C.
      It transmits exactly the 1+15 line sector and complements point incidence Z,
      giving 18I=3Z^TZ+C^TC-3J and a full-rank point+double-six readout.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque,defaultdict
from pathlib import Path
import numpy as np,networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT64=ROOT/'data/PART_W33_PASS4964_DOUBLE_SIX_SPREAD_EQUIVARIANT_BRIDGE.json'
OUT65=ROOT/'data/PART_W33_PASS4965_STEINER_LOCAL_NINE_SPREAD_CHART.json'
OUT67=ROOT/'data/PART_W33_PASS4967_POINT_DOUBLE_SIX_COMPLETE_TRANSCEIVER.json'

def Q6(v):
    a,c,d,e,f,g=v;return (a*c+d*e+f+f*g+g)&1
def add2(a,b):return tuple(x^y for x,y in zip(a,b))
def polar(a,b):return Q6(add2(a,b))^Q6(a)^Q6(b)
def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def closure(gens,n):
    I=tuple(range(n));S={I};D=deque([I])
    while D:
        a=D.popleft()
        for g in gens:
            z=comp(g,a)
            if z not in S:S.add(z);D.append(z)
    return S
def canon3(v):
    v=np.array(v,dtype=int)%3;j=next(i for i,x in enumerate(v) if x)
    return tuple(int(x) for x in (v*pow(int(v[j]),-1,3))%3)
def pair_closure(genA,genB,n=36):
    I=tuple(range(n));S={(I,I)};D=deque([(I,I)])
    while D:
        a,b=D.popleft()
        for ga,gb in zip(genA,genB):
            z=(comp(ga,a),comp(gb,b))
            if z not in S:S.add(z);D.append(z)
    return S

def main()->int:
    # Cubic-surface 27-line model, 36 double-sixes and PSp generators.
    vecs=[v for v in itertools.product((0,1),repeat=6) if any(v)]
    sing=[v for v in vecs if Q6(v)==0];nons=[v for v in vecs if Q6(v)==1];si={v:i for i,v in enumerate(sing)}
    trans=[tuple(si[add2(x,v) if polar(x,v) else x] for x in sing) for v in nons]
    gp=[];S={tuple(range(27))}
    for g in [comp(trans[0],t) for t in trans[1:]]:
        T=closure(gp+[g],27)
        if len(T)>len(S):gp.append(g);S=T
        if len(S)==25920:break
    assert len(S)==25920 and len(closure(gp+[trans[0]],27))==51840
    qp=[sum(bit<<i for i,bit in enumerate(v)) for v in sing]
    p27=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    l27=[tuple(i for i,P in enumerate(p27) if x in P) for x in qp]
    G27=nx.Graph();G27.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if set(l27[i])&set(l27[j]):G27.add_edge(i,j)
    C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G27)) if len(c)==6]
    DS=set()
    for A,B in itertools.combinations(C6,2):
        if A&B:continue
        H=G27.subgraph(A|B)
        if H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):DS.add(frozenset(A|B))
    DS=sorted(DS,key=lambda x:tuple(sorted(x)));assert len(DS)==36;di={S:i for i,S in enumerate(DS)}
    H36=nx.Graph();H36.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H36.add_edge(i,j)
    assert H36.number_of_edges()==360 and set(dict(H36.degree()).values())=={20}
    st=sorted(t for t in itertools.combinations(range(36),3)
      if all(H36.has_edge(*e) for e in itertools.combinations(t,2)) and len(DS[t[0]]&DS[t[1]]&DS[t[2]])==0)
    assert len(st)==120;sti={t:i for i,t in enumerate(st)}
    DP=[];SP=[]
    for g in gp:
        dp=tuple(di[frozenset(g[x] for x in D)] for D in DS);DP.append(dp)
        SP.append(tuple(sti[tuple(sorted(dp[i] for i in t))] for t in st))

    # Steiner pair orbitals -> forty Q43/W33-line fibers.
    seen=set();orbits=[]
    for p in itertools.combinations(range(120),2):
        if p in seen:continue
        O={p};seen.add(p);D=deque([p])
        while D:
            a=D.popleft()
            for op in SP:
                b=tuple(sorted((op[a[0]],op[a[1]])))
                if b not in O:O.add(b);seen.add(b);D.append(b)
        orbits.append(sorted(O))
    R1,R2,R3,R4=sorted(orbits,key=len);assert list(map(len,(R1,R2,R3,R4)))==[120,1620,2160,3240]
    FG=nx.Graph();FG.add_nodes_from(range(120));FG.add_edges_from(R1)
    fibers=sorted([sorted(c) for c in nx.connected_components(FG)]);assert len(fibers)==40
    fi={x:i for i,F in enumerate(fibers) for x in F};fiber_index={frozenset(F):i for i,F in enumerate(fibers)}
    Q=nx.Graph();Q.add_nodes_from(range(40))
    for a,b in R3:Q.add_edge(fi[a],fi[b])
    assert Q.number_of_edges()==240 and set(dict(Q.degree()).values())=={12}
    FP=[]
    for op in SP:FP.append(tuple(fiber_index[frozenset(op[x] for x in F)] for F in fibers))

    # The 36 maximum cocliques are the 36 W33 spreads.
    spreads=sorted([frozenset(c) for c in nx.find_cliques(nx.complement(Q)) if len(c)==10],key=lambda s:tuple(sorted(s)))
    assert len(spreads)==36;spi={S:i for i,S in enumerate(spreads)}
    SprP=[tuple(spi[frozenset(p[i] for i in S)] for S in spreads) for p in FP]

    # Full outer element and actions.
    gout=trans[0]
    dpout=tuple(di[frozenset(gout[x] for x in D)] for D in DS)
    spout=tuple(sti[tuple(sorted(dpout[i] for i in t))] for t in st)
    fpout=tuple(fiber_index[frozenset(spout[x] for x in F)] for F in fibers)
    sprout=tuple(spi[frozenset(fpout[i] for i in S)] for S in spreads)
    paired=pair_closure(DP+[dpout],SprP+[sprout]);assert len(paired)==51840

    # Unique equivariant bijection from a base stabilizer fixed point.
    stab0=[(a,b) for a,b in paired if a[0]==0];assert len(stab0)==1440
    fixed=[s for s in range(36) if all(b[s]==s for a,b in stab0)];assert len(fixed)==1;s0=fixed[0]
    bridge={}
    for a,b in paired:
        d=a[0];s=b[s0]
        if d in bridge:assert bridge[d]==s
        bridge[d]=s
    assert len(bridge)==36 and len(set(bridge.values()))==36
    assert all(bridge[dpout[d]]==sprout[bridge[d]] for d in range(36))
    cross=Counter()
    for i,j in itertools.combinations(range(36),2):cross[(len(DS[i]&DS[j]),len(spreads[bridge[i]]&spreads[bridge[j]]))]+=1
    assert cross==Counter({(6,1):360,(4,4):270})
    chars=Counter()
    for a,b in paired:
        fa=sum(i==a[i] for i in range(36));fb=sum(i==b[i] for i in range(36));assert fa==fb;chars[fa]+=1
    assert sum(chars.values())==51840

    out64={'pass':4964,
      'group':{'name':'W(E6) = PGSp(4,3) on these finite carriers','order':51840,'derived_PSp_order':25920},
      'carriers':{'double_sixes':36,'W33_spreads':36,'point_stabilizer_order':1440},
      'permutation_character_fixed_point_census':{str(k):v for k,v in sorted(chars.items())},
      'base_double_six_stabilizer_fixed_spreads':1,
      'equivariant_bijection':{'exists':True,'unique':True,'extends_across_outer_involution':True},
      'pair_relation_transport':{'double_six_intersection_6_to_spread_overlap_1':360,'double_six_intersection_4_to_spread_overlap_4':270},
      'theorem':'There is a unique W(E6)=PGSp(4,3)-equivariant bijection from the 36 cubic-surface double-sixes to the 36 spreads of W(3,3). It sends the 360 double-six pairs meeting in six cubic lines to the 360 spread pairs meeting in one W33 line, and the 270 four-intersection pairs to the 270 four-overlap spread pairs. Thus the double-six SRG(36,20,10,12) is exactly the one-overlap graph on W33 spreads.',
      'boundary':'The bijection is between the two 36-element finite G-sets; it does not identify the 12 cubic-surface lines inside a double-six with the 10 W33 lines inside its image spread element-by-element.'}
    OUT64.write_text(json.dumps(out64,indent=2,sort_keys=True)+'\n')

    # Pass4965: every Steiner triangle becomes a triple of spreads with one common W33 line.
    line_to=[]
    byline=defaultdict(list)
    for t in st:
        ss=tuple(sorted(bridge[d] for d in t));common=set.intersection(*(set(spreads[s]) for s in ss));assert len(common)==1
        q=next(iter(common));assert q==fi[sti[t]]
        byline[q].append(ss)
    assert len(byline)==40 and set(map(len,byline.values()))=={3}
    for q,trips in byline.items():
        parts=[set(x) for x in trips];inc={s for s,S in enumerate(spreads) if q in S}
        assert len(inc)==9 and set.union(*parts)==inc and sum(map(len,parts))==9
        assert all(not (a&b) for a,b in itertools.combinations(parts,2))
        # within parts overlap=1; across parts overlap=4 -> local A4 graph K3,3,3.
        for P in parts:
            assert all(len(spreads[i]&spreads[j])==1 for i,j in itertools.combinations(P,2))
        for P,R in itertools.combinations(parts,2):
            assert all(len(spreads[i]&spreads[j])==4 for i in P for j in R)
    out65={'pass':4965,'W33_lines':40,'spreads_through_each_line':9,'Steiner_triangles':120,
      'Steiner_triangles_per_W33_line':3,'canonical_partition_per_line':'9 spreads = 3 + 3 + 3',
      'local_four_overlap_graph':'K3,3,3','local_one_overlap_graph':'3 disjoint K3',
      'theorem':'Transporting the 120 cubic-surface Steiner triangles through the Pass4964 double-six/spread bijection yields a canonical local nine-spread chart at every W33 line. Each Steiner triangle maps to three spreads whose common intersection is exactly its associated W33 line. The three Steiner triangles in each fiber partition all nine spreads through that line into three disjoint triples; four-overlap occurs exactly across different triples, so the local four-overlap graph is K_{3,3,3}.',
      'boundary':'The 3+3+3 partition is canonical under the finite incidence bridge. Calling it a physical qutrit port chart is an interpretation, not part of the theorem.'}
    OUT65.write_text(json.dumps(out65,indent=2,sort_keys=True)+'\n')

    # Pass4967: double-six x W33-line incidence C and complementary point channel Z.
    Cq=np.zeros((36,40),dtype=int)
    for d in range(36):Cq[d,list(spreads[bridge[d]])]=1
    assert set(map(int,Cq.sum(1)))=={10} and set(map(int,Cq.sum(0)))=={9}
    Ads=nx.to_numpy_array(H36,nodelist=range(36),dtype=int)
    assert np.array_equal(Cq@Cq.T,4*np.ones((36,36),dtype=int)+6*np.eye(36,dtype=int)-3*Ads)
    assert np.linalg.matrix_rank(Cq)==16

    pts=sorted({canon3(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    J4=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%3
    Wg=nx.Graph();Wg.add_nodes_from(range(40))
    for a,b in itertools.combinations(range(40),2):
        if int(np.array(pts[a])@J4@np.array(pts[b]))%3==0:Wg.add_edge(a,b)
    wlines=sorted({tuple(sorted(c)) for c in nx.find_cliques(Wg) if len(c)==4});assert len(wlines)==40
    Qstd=nx.Graph();Qstd.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if set(wlines[i])&set(wlines[j]):Qstd.add_edge(i,j)
    qmap=next(nx.algorithms.isomorphism.GraphMatcher(Q,Qstd).isomorphisms_iter())
    C=np.zeros((36,40),dtype=int)
    for d in range(36):
        for q in spreads[bridge[d]]:C[d,qmap[q]]=1
    Z=np.zeros((40,40),dtype=int)
    for j,L in enumerate(wlines):Z[list(L),j]=1
    I=np.eye(40,dtype=int);J40=np.ones((40,40),dtype=int)
    assert np.array_equal(3*(Z.T@Z)+(C.T@C)-3*J40,18*I)
    stacked=np.vstack([Z,C]);assert np.linalg.matrix_rank(stacked)==40
    out67={'pass':4967,
      'matrices':{'Z_point_by_line':[40,40],'C_double_six_by_line':[36,40],'stacked':[76,40]},
      'double_six_line_channel':{'row_weight':10,'column_weight':9,'rank':16,
        'double_six_gram':'CC^T=4J+6I-3A_DS','nonzero_sector':'1+15','line_side_dark_sector':'24'},
      'point_line_channel':{'rank':25,'nonzero_sector':'1+24','line_side_dark_sector':'15'},
      'exact_reconstruction_identity':'18 I_40 = 3 Z^T Z + C^T C - 3 J_40',
      'stacked_rank':40,
      'theorem':'After the canonical Pass4964 identification of double-sixes with spreads, line-spread incidence becomes a canonical 36x40 double-six/line matrix C. C transmits exactly the constant plus 15-dimensional W33-line sector while point incidence Z transmits constant plus 24. Together [Z;C] has full rank 40 and satisfies 18I=3Z^TZ+C^TC-3J, giving exact reconstruction of every W33-line coordinate from point and double-six readouts.',
      'prior_art_credit':'The spread-line Gram spectrum is Part CXXVI and the point+spread complementarity is Pass4958. The new content is the canonical replacement of anonymous spread rows by cubic-surface double-sixes via Pass4964.',
      'boundary':'This is a finite linear transceiver identity. It supplies no continuum field, coupling, or device normalization.'}
    OUT67.write_text(json.dumps(out67,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passes':[4964,4965,4967],'bridge_unique':True,'local_chart':'K3,3,3','stacked_rank':40},indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
