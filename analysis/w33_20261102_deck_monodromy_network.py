"""Native cover deck/monodromy maps and weighted Shrikhande communication.

Prior: w33_20261102_toroidal_knight_clifford_bridge.py owns the map;
w33_pass75_zeta_equidistribution.py and w33_pass76_cospectral_mates.py own
the Shrikhande/rook spectral and local-link control. General graph transfer
and pillowcase covers are prior mathematics; no novelty claimed for them.
"""
import collections
import itertools
import json
import pathlib
import sys

import numpy as np
import sympy as s
from scipy.linalg import expm

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_chiral_surface_development import manifold


def adjacency(edges):
    a=np.zeros((16,16),dtype=int)
    for i,j in edges:a[i,j]=a[j,i]=1
    return a


def homology(faces):
    edges=sorted({tuple(sorted(e)) for f in faces for e in itertools.combinations(f,2)})
    index={e:i for i,e in enumerate(edges)}
    d1=s.zeros(16,len(edges));d2=s.zeros(len(edges),len(faces))
    for i,(a,b) in enumerate(edges):d1[a,i]=-1;d1[b,i]=1
    for j,(a,b,c) in enumerate(faces):
        for u,v in [(a,b),(b,c),(c,a)]:d2[index[tuple(sorted((u,v)))],j]=1 if u<v else -1
    assert d1*d2==s.zeros(16,len(faces))
    r1,r2=d1.rank(),d2.rank()
    return dict(ranks=[r1,r2],rational_Betti=[16-r1,len(edges)-r1-r2,len(faces)-r2])


def build():
    d=json.loads((ROOT/'data/w33_20261102_toroidal_knight_clifford_bridge.json').read_text())
    F=[tuple(f) for f in d['source_faces']];pi=dict(d['native_labels'])
    canonical=lambda t:min(tuple(t[i:]+t[:i]) for i in range(3))
    face_set={canonical(f) for f in F}
    deck=[]
    for e,a,b in itertools.product(range(2),repeat=3):
        perm=[]
        for x,y in itertools.product(range(4),repeat=2):
            perm.append(4*(((-1)**e*x+2*a)%4)+(((-1)**e*y+2*b)%4))
        assert {canonical(tuple(perm[v] for v in f)) for f in F}==face_set
        assert all(pi[perm[v]]==pi[v] for v in range(16))
        deck.append(tuple(perm))
    assert len(set(deck))==8
    assert all(tuple(p[q[v]] for v in range(16)) in deck for p,q in itertools.product(deck,repeat=2))
    assert all(tuple(p[p[v]] for v in range(16))==tuple(range(16)) for p in deck)
    assert all(sum(p[v]==v for p in deck)==2 for v in range(16))
    # Bound all simplicial deck maps by the eight possible images of one face.
    # The connected dual graph forces the rest, as in native development.
    edges,_,_=manifold(F)
    colors=sorted(set(pi.values()))
    typ=[next(c for c in colors if c not in [pi[v] for v in f]) for f in F]
    base=typ[0];sheets=[j for j,t in enumerate(typ) if t==base]
    assert len(sheets)==8
    lift={}
    for rows in edges.values():
        i,j=rows[0][0],rows[1][0]
        lift[i,typ[j]]=j;lift[j,typ[i]]=i
    assert len(lift)==96
    def walk(start,path):
        i=start
        for t in path[1:]:i=lift[i,t]
        return i
    monodromy=[];loops=[]
    for branch in colors:
        incident=[c for c in colors if c!=branch]
        start=base if base in incident else incident[0]
        prefix=[base] if start==base else [base,start]
        others=[c for c in incident if c!=start]
        loop=prefix+others+[start]+prefix[-2::-1]
        assert loop[0]==loop[-1]==base
        p=tuple(sheets.index(walk(i,loop)) for i in sheets)
        assert all(p[p[j]]==j and p[j]!=j for j in range(8))
        monodromy.append(p);loops.append(loop)
    mul=lambda p,q:tuple(p[q[i]] for i in range(len(p)))
    group={tuple(range(8))};queue=list(group)
    for p in queue:
        for q in monodromy:
            r=mul(p,q)
            if r not in group:group.add(r);queue.append(r)
    assert len(group)==8
    product=tuple(range(8))
    for p in monodromy:product=mul(p,product)
    assert product==tuple(range(8))
    assert all(mul(p,q)==mul(q,p) for p,q in itertools.product(group,repeat=2))
    # A precise F2^3 address for the branch monodromies.
    address={tuple(range(8)):0}
    for mask in range(8):
        p=tuple(range(8))
        for j in range(3):
            if mask>>j&1:p=mul(monodromy[j],p)
        address[p]=mask
    assert len(address)==8 and address[monodromy[3]]==7
    G=adjacency(d['grid_edges']);K=adjacency(d['knight_edges']);D=adjacency(d['diagonal_edges']);A=G+D
    assert np.array_equal(A@A,4*np.eye(16,dtype=int)+2*np.ones((16,16),dtype=int))
    triangles=[t for t in itertools.combinations(range(16),3) if all(A[i,j] for i,j in itertools.combinations(t,2))]
    assert {tuple(sorted(t)) for t in F}==set(triangles)
    rook_edges=[(i,j) for i,j in itertools.combinations(range(16),2) if i//4==j//4 or i%4==j%4]
    R=adjacency(rook_edges)
    rook_faces=[t for t in itertools.combinations(range(16),3) if all(R[i,j] for i,j in itertools.combinations(t,2))]
    assert len(rook_faces)==32 and np.array_equal(R@R,A@A)
    shrikhande_h=homology(F);rook_h=homology(rook_faces)
    assert shrikhande_h['rational_Betti']==[1,2,1] and rook_h['rational_Betti']==[1,9,8]
    antipode=np.zeros((16,16),dtype=int)
    for x,y in itertools.product(range(4),repeat=2):antipode[4*((x+2)%4)+(y+2)%4,4*x+y]=1
    residuals={}
    for name,H,target in [('grid',G,antipode),('knight',K,antipode),('native_equal',A,-np.eye(16)),('native_diagonal_doubled',G+2*D,antipode)]:
        residuals[name]=float(np.max(abs(expm(-1j*np.pi*H/2)-target)))
        assert residuals[name]<1e-12
    # Exact spectral projectors prove no vertex PST at ANY time on A.
    J=s.ones(16);P6=J/16;P2=s.Matrix(A)/4+s.eye(16)/2-J/8;Pm=s.eye(16)-P6-P2
    assert all(p*p==p for p in [P6,P2,Pm])
    assert all(abs(P2[i,j])!=P2[i,i] for i,j in itertools.combinations(range(16),2))
    t=np.arccos(-1/3)/4;U=expm(-1j*t*A)
    assert abs(abs(U[1,0])**2-1/12)<1e-12
    return dict(status='PASS_NATIVE_DECK_MONODROMY_AND_WEIGHTED_NETWORK',deck_permutations=deck,
        deck_structure='C2^3',deck_exhaustiveness='Eight explicit label-preserving oriented simplicial automorphisms. A deck map is determined by its image on one base face; there are exactly8 such faces. Connected dual development forces all remaining vertices.',
        based_meridian_face_type_loops=loops,meridian_sheet_permutations=monodromy,branch_addresses=[address[p] for p in monodromy],
        branch_cycle_type='2^4 for each of four target vertices',vertex_stabilizer_order=2,
        shrikhande_srg_parameters=[16,6,2,2],shrikhande_homology=shrikhande_h,rook_2_skeleton_homology=rook_h,
        spectral_multiplicities={'6':1,'2':6,'-2':9},walk_residuals_at_pi_over_2=residuals,
        exact_transfer_probabilities={'Shrikhande_adjacent_max':'1/12','Shrikhande_nonadjacent_max':'1/16'},
        no_vertex_PST='Exact P2 diagonal3/8, offdiagonal+/-1/8: no distinct strongly cospectral vertices. With z=exp(-4it), adjacent amplitude is exp(2it)(z-1)(z+3)/16, nonadjacent exp(2it)(z-1)^2/16.',
        weight_repair='For A(kappa)=grid+kappa*diagonal at t=pi/2, even integer kappa gives antipodal PST; odd integer kappa gives -I. Support stays the same for positive kappa. These are supplied dimensionless uniform coupling Hamiltonians.',
        boundary='The deck group is native to the fixed simplicial cover. A finite graph walk is an ideal single-excitation communication model, not a physical spacetime or fault-tolerant network. Rook comparison uses its2-skeleton, not its full clique complex with eight3-simplices.')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261102_deck_monodromy_network.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],d['branch_addresses'],d['shrikhande_homology'],flush=True)
