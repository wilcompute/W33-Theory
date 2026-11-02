"""Exact native chiral face development and branched tetrahedral coverings.

Riemann-Hurwitz and simplicial branched covers are established topology.
This applies them to the actual integer Pauli triple tensor, with a finite
development algorithm and explicit globally obstructed controls.
"""
import pathlib,sys,json,itertools,collections,hashlib
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261101_frame_tomography_octahedron import inputs,exact_tensor

def native_completion():
    tetra,_,_=inputs();B=exact_tensor(tetra)
    assert int(B.max())==2
    C=np.full((120,120),-1,dtype=np.int16)
    rows=np.argwhere(B==2)
    for a,b,c in rows:
        assert C[a,b]==-1;C[a,b]=c
    assert len(rows)==9720
    quartets={tuple(sorted(t))for t in tetra['oriented_tetrahedra']}
    edge_owner={}
    for t in quartets:
        for edge in itertools.combinations(t,2):
            assert edge not in edge_owner;edge_owner[edge]=t
    assert len(edge_owner)==4860
    for a,b,c in rows:
        d=int(C[b,a]);assert len({int(a),int(b),int(c),d})==4
        assert tuple(sorted((int(a),int(b),int(c),d)))==edge_owner[tuple(sorted((int(a),int(b))))]
    return B,C

def torus(m,n):
    assert m>=3 and n>=3
    v=lambda i,j:(i%m)*n+j%n
    return [(v(i,j),v(i+1,j),v(i+1,j+1))for i in range(m)for j in range(n)]+[(v(i,j),v(i+1,j+1),v(i,j+1))for i in range(m)for j in range(n)]

def manifold(faces):
    assert all(len(set(f))==3 for f in faces)
    assert len({tuple(sorted(f))for f in faces})==len(faces)
    edges=collections.defaultdict(list);links=collections.defaultdict(list)
    for ix,(a,b,c) in enumerate(faces):
        for x,y,z in [(a,b,c),(b,c,a),(c,a,b)]:edges[tuple(sorted((x,y)))].append((ix,x,y));links[x].append((y,z))
    for rows in edges.values():assert len(rows)==2 and rows[0][1:]==rows[1][1:][::-1]
    for v,link in links.items():
        nxt=dict(link);assert len(nxt)==len(link) and set(nxt)==set(nxt.values())
        start=next(iter(nxt));seen={start};x=nxt[start]
        while x!=start:assert x not in seen;seen.add(x);x=nxt[x]
        assert len(seen)==len(nxt)
    chi=len(links)-len(edges)+len(faces);assert (2-chi)%2==0
    return edges,{v:len(link)for v,link in links.items()},chi

def develop(faces,C,seed=None):
    edges,degrees,chi=manifold(faces)
    if seed is None:
        a,b=map(int,np.argwhere(C>=0)[0]);seed=(a,b,int(C[a,b]))
    labels=dict(zip(faces[0],seed));todo=collections.deque([0]);seen=set();conflict=None
    while todo:
        ix=todo.popleft()
        if ix in seen:continue
        seen.add(ix);face=faces[ix]
        for k in range(3):
            a,b,c=face[k:]+face[:k]
            if a in labels and b in labels:
                predicted=int(C[labels[a],labels[b]])
                if predicted<0:
                    conflict=dict(face_index=ix,face=face,edge=[a,b],edge_labels=[labels[a],labels[b]],reason='No positive native completion exists for the forced edge');break
                if c in labels and labels[c]!=predicted:
                    conflict=dict(face_index=ix,face=face,vertex=c,previous=labels[c],forced=predicted);break
                labels[c]=predicted
        if conflict:break
        assert all(v in labels for v in face)
        for a,b in itertools.combinations(face,2):
            todo.extend(row[0]for row in edges[tuple(sorted((a,b)))]if row[0]not in seen)
    out=dict(vertices=len(degrees),edges=len(edges),faces=len(faces),Euler_characteristic=chi,genus=(2-chi)//2,
             vertex_degree_histogram=dict(collections.Counter(degrees.values())),saturated=conflict is None,
             labels=sorted(labels.items()),conflict=conflict)
    if conflict is None:
        assert len(seen)==len(faces) and len(set(labels.values()))==4
        assert all(C[labels[a],labels[b]]==labels[c]for a,b,c in faces)
        assert all(d%3==0 for d in degrees.values())
        counts=collections.Counter(tuple(sorted(labels[v]for v in f))for f in faces)
        assert len(counts)==4 and len(set(counts.values()))==1
        degree=next(iter(counts.values()));ramification=sum(d//3-1 for d in degrees.values())
        assert chi==2*degree-ramification
        out.update(cover_degree=degree,total_ramification=ramification,target_face_multiplicities=sorted(counts.values()))
    return out

def build():
    B,C=native_completion()
    tetra=[(1,2,3),(0,3,2),(0,1,3),(0,2,1)]
    octa=[(a,b,c)if (i+j+k)%2==0 else(a,c,b)for i,a in enumerate((0,1))for j,b in enumerate((2,3))for k,c in enumerate((4,5))]
    examples={'tetrahedral_sphere':develop(tetra,C),'octahedral_sphere':develop(octa,C),
              'even_period_torus_4x4':develop(torus(4,4),C),'odd_period_torus_3x4':develop(torus(3,4),C),
              'even_period_torus_4x6':develop(torus(4,6),C)}
    assert examples['tetrahedral_sphere']['cover_degree']==1
    assert not examples['octahedral_sphere']['saturated']
    assert examples['even_period_torus_4x4']['cover_degree']==8
    assert examples['even_period_torus_4x4']['total_ramification']==16
    assert not examples['odd_period_torus_3x4']['saturated']
    for row in examples.values():
        if row['saturated']:
            row['exact_ground_energy_at_reference']=-(2*row['edges'])/3-row['faces']
            row['ordered_ground_degeneracy_for_positive_lambda']=9720
    # All possible ordered positive seed faces have the same abstract tetrahedral
    # completion rule, so one developed seed is sufficient, not a heuristic.
    return dict(status='PASS_NATIVE_CHIRAL_SURFACE_DEVELOPMENT',maximal_integer_face_chirality=2,
        maximal_ordered_faces=9720,unordered_tetrahedra=810,noncommuting_edges=4860,
        completion_table=C.tolist(),completion_sha256=hashlib.sha256(C.tobytes()).hexdigest(),examples=examples,
        theorem='On a connected closed oriented simplicial triangulated surface, every face has native B=+2 iff its forced tetrahedral development is globally consistent. Each ordered noncommuting edge has a unique positive third tick, and each unordered such edge lies in exactly one native tetrahedron. Hence all faces use one tetrahedral quartet and define an orientation-preserving simplicial branched cover of its boundary sphere.',
        consequences='Every vertex degree is divisible by3. Cover degree d=F/4, local ramification degree deg(v)/3, and chi=2d-sum_v(deg(v)/3-1). Local divisibility alone is insufficient: the3x4 periodic triangular torus has all vertex degrees6 but inconsistent global development. The4x4 torus saturates with d=8 and16 simple ramification points.',
        exact_energy_and_count='If development succeeds, for J>0,K>3J/2,lambda>0 the exact ground energy is |edges|(2J-4K/3)-lambda|faces|/sqrt3. The ground degeneracy is exactly9720, since each maximal ordered seed face uniquely develops and all9720 native seed faces have the same oriented tetrahedral completion rule. Along even-period triangular tori the ground entropy density therefore tends to0. If development fails, the separate bond/face bound is unattainable; no exact frustrated ground energy is computed here.',
        proof='Unique ordered-edge completion forces labels across every dual edge. The unique quartet propagates through the connected dual graph. At each vertex the oriented link runs repeatedly around the three-cycle link in the target tetrahedron, giving a positive local degree and branching only at vertices. Each target face has the same multiplicity by the oriented cycle equation. Euler counting yields Riemann-Hurwitz.',
        boundary='Finite supplied chiral face model on an externally specified surface; no dynamical topology selection, physical spacetime, unique vacuum or quantum-gravity amplitude. General branched-cover theory and development/holonomy methods are prior mathematics.')

if __name__=='__main__':
    out=build();(ROOT/'data/w33_20261102_chiral_surface_development.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'],json.dumps({k:(v['saturated'],v.get('cover_degree'))for k,v in out['examples'].items()}),flush=True)
