"""Actual q=3 frame and q=5 Petersen stabilizers are explicitly isomorphic.

Exhaust the old Sp(4,3) construction, identify the actual27-point action,
then solve the central sign equations and verify all1920 Cayley products.
"""
import pathlib,sys,json,itertools,time,hashlib
import numpy as np,networkx as nx
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11177_perfect_gates_tritangent as T
import w33_pass11156_perfect_spacetime_gates as G
from w33_20261031_signed_cubic_lift import solve2

def build():
    _,facs=T.factorisations();facs=sorted(facs,key=lambda f:sorted(sorted(P)for P in f));octets=[frozenset().union(*f)for f in facs]
    A=nx.Graph();A.add_nodes_from(range(45));A.add_edges_from((i,j)for i,j in itertools.combinations(range(45),2)if not octets[i]&octets[j])
    frames=sorted(tuple(sorted(c))for c in nx.find_cliques(A)if len(c)==5);assert len(frames)==27
    selected=frozenset(frames[0]);partition={octets[i]for i in selected};oid={o:i for i,o in enumerate(octets)};fid={frozenset(f):i for i,f in enumerate(frames)}
    pts=np.array(T.PTS);actions={};representatives={}
    whole=G.sp43();assert len(whole)==51840
    for S in whole:
        raw=pts@S.T%3;first=np.argmax(raw!=0,axis=1);raw=raw*raw[np.arange(40),first,None]%3;pp=[T.PID[tuple(v)]for v in raw]
        if {frozenset(pp[i]for i in octets[j])for j in selected}!=partition:continue
        fp=[oid[frozenset(pp[i]for i in o)]for o in octets];perm=tuple(fid[frozenset(fp[i]for i in f)]for f in frames)
        actions[tuple(map(int,S.flat))]=perm
        canonical=S*next(int(x)for x in S.flat if x)%3;representatives[perm]=canonical
    assert len(actions)==1920 and len(representatives)==960
    FG=nx.Graph();FG.add_nodes_from(range(27));FG.add_edges_from((i,j)for i,j in itertools.combinations(range(27),2)if set(frames[i])&set(frames[j]))
    old=json.loads((ROOT/'data/w33_20261031_petersen_stabilizer.json').read_text());cubic=json.loads((ROOT/'data/w33_20261031_signed_cubic_lift.json').read_text())
    WG=nx.Graph();WG.add_nodes_from(range(27));WG.add_edges_from((a,b)for t in cubic['coefficient_rows']for a,b in itertools.combinations(t['triple'],2))
    for H in (FG,WG):nx.set_node_attributes(H,{i:int(i==0)for i in H},'anchor')
    mapping=next(nx.isomorphism.GraphMatcher(WG,FG,node_match=lambda a,b:a['anchor']==b['anchor']).isomorphisms_iter());mi={v:k for k,v in mapping.items()}
    q3gens=[]
    for gen in cubic['signed_generators']:
        p=gen['permutation'];transported=tuple(mapping[p[mi[i]]]for i in range(27));assert transported in representatives;q3gens.append(representatives[transported])
    q5gens=[np.array(M)for M in old['symplectic_matrix_generators']];key=lambda M:tuple(map(int,M.flat));I=np.eye(4,dtype=int)
    words={key(I):(I,0)};queue=[I];equations=[]
    for B in queue:
        C,bits=words[key(B)]
        for j,(g,h)in enumerate(zip(q5gens,q3gens)):
            D=g@B%5;E=h@C%3;newbits=bits^(1<<j);k=key(D)
            if k not in words:words[k]=(E,newbits);queue.append(D)
            else:
                F,oldbits=words[k];sign=0 if np.array_equal(E,F)else 1;assert sign==0 or np.array_equal(E,-F%3)
                equations.append((newbits^oldbits,sign))
    assert len(queue)==1920
    C,bits=words[key(-I%5)];sign=0 if np.array_equal(C,-I%3)else 1;assert sign==0 or np.array_equal(C,I)
    equations.append((bits,sign));solution=solve2(equations,6);assert solution is not None
    corrected=[(-1)**b*M%3 for b,M in zip(solution,q3gens)]
    images={key(I):I};todo=[I];edges=0
    for B in todo:
        for g,h in zip(q5gens,corrected):
            D=g@B%5;E=h@images[key(B)]%3;k=key(D);edges+=1
            if k not in images:images[k]=E;todo.append(D)
            else:assert np.array_equal(E,images[k])
    assert len(images)==1920 and len({key(M)for M in images.values()})==1920
    assert np.array_equal(images[key(-I%5)],-I%3)
    pairs=sorted((list(k),list(key(M)))for k,M in images.items())
    return dict(status='PASS_EXACT_CROSS_FIELD_STABILIZER_ISOMORPHISM',
        ambient_q3_group_order=51840,q3_frame_stabilizer_order=1920,q5_set_stabilizer_preimage_order=1920,projective_order=960,
        q3_symplectic_form=G.J.tolist(),q3_point_coordinates=[list(map(int,p))for p in T.PTS],
        selected_q3_frame_octets=[sorted(octets[i])for i in frames[0]],all_q3_frame_octets=[[sorted(octets[i])for i in f]for f in frames],
        q5_weight_to_q3_frame=[int(mapping[i])for i in range(27)],
        q3_corrected_matrix_generators=[M.tolist()for M in corrected],q5_matrix_generators=[M.tolist()for M in q5gens],
        canonical_q3_generator_sign_corrections=solution,all_Cayley_edges_checked=edges,
        central_minus_identity_maps_to_minus_identity=True,
        correspondence_sha256=hashlib.sha256(json.dumps(pairs,separators=(',',':')).encode()).hexdigest(),
        meaning='The actual q3 factorisation-frame stabilizer and q5 Petersen-set stabilizer preimage are isomorphic, preserving the central involution and the transported27-point projective action. This also transports the exact complex SU4 lift to the q3 frame subgroup.',
        prior='Pass11185 owns q3 frame counts; the preceding packet owns the actual q5 group/SU4 matrices. This supplies the cross-field generator map and all-product verification, not a count-based identification.',
        boundary='The1920 groups have a central involution and are not the center-free W(D5). The full ambient Sp(4,3) and Sp(4,5) are not identified. No quantum tick-clock bijection, physical E6 phase lift or spacetime follows.')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261031_cross_field_stabilizers.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['all_Cayley_edges_checked'])
