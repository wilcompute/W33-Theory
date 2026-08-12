#!/usr/bin/env python3
"""Pass5002-5004: correct the global 85-reader erasure distance, diagonalize
the 270-octahedron real frame by natural carriers, and prove the residual C3
origin requires external symmetry breaking.
"""
from __future__ import annotations
import itertools,json,sys
from collections import Counter
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis.w33_pass4992_4999_common import build_base,gf2_rank_int,gf2_rank_matrix

O2=ROOT/'data/PART_W33_PASS5002_CORRECTED_85_READER_ERASURE_DISTANCE.json'
O3=ROOT/'data/PART_W33_PASS5003_OCTAHEDRON_REAL_MODULE_DECOMPOSITION.json'
O4=ROOT/'data/PART_W33_PASS5004_C3_TORSOR_ORIGIN_NOGO.json'

def bmask(row):return sum((int(x)&1)<<i for i,x in enumerate(row))
def rank_modp(A,p=101):
    A=np.array(A,dtype=object);m,n=A.shape;r=0
    A=[[int(A[i,j])%p for j in range(n)] for i in range(m)]
    for c in range(n):
        k=next((i for i in range(r,m) if A[i][c]),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r];iv=pow(A[r][c],-1,p);A[r]=[(x*iv)%p for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                f=A[i][c];A[i]=[(A[i][j]-f*A[r][j])%p for j in range(n)]
        r+=1
        if r==m:break
    return r

def no_dep_gf2(masks,maxk):
    for k in range(2,maxk+1):
        for S in itertools.combinations(range(len(masks)),k):
            if gf2_rank_int(masks[i] for i in S)<k:return False,(k,S)
    return True,None

def main()->int:
    b=build_base();C=b['C'].astype(int);M=b['M'].astype(int);L=b['L'];W=b['W'];T=b['tritangents'];G27=b['G27']
    # --------------------------------------------------------------- Pass5002
    Lraw=C.T;Traw=M
    Lc=4*Lraw-np.ones((40,36),dtype=int)
    Tc=3*Traw-2*np.ones((45,36),dtype=int)
    assert np.max(np.abs(Lc@Tc.T))==0 and (np.linalg.matrix_rank(Lc),np.linalg.matrix_rank(Tc))==(15,20)
    # Exact centered support minima: modulo a prime, full row rank proves rational independence.
    line_dep4=[]
    for k in (2,3,4):
        bad=[]
        for S in itertools.combinations(range(40),k):
            if rank_modp(Lc[list(S)])<k:bad.append(S)
        if k<4:assert not bad
        else:line_dep4=bad;assert len(bad)==40
    for k in (2,3,4):
        assert all(rank_modp(Tc[list(S)])==k for S in itertools.combinations(range(45),k))
    pencils=[tuple(j for j,Lj in enumerate(L) if p in Lj) for p in range(40)]
    assert set(line_dep4)==set(pencils)
    assert all(np.all(Lc[list(P)].sum(0)==0) for P in pencils)
    # Raw line/tritangent rows have no dependency through support five; F2-full-rank is an exact lower certificate.
    lm=[bmask(row) for row in Lraw];tm=[bmask(row) for row in Traw]
    assert no_dep_gf2(lm,5)[0] and no_dep_gf2(tm,5)[0]
    support6=set()
    for p,q in W.edges():
        P,Q=set(pencils[p]),set(pencils[q]);assert len(P&Q)==1
        s=frozenset(P^Q);assert len(s)==6
        coeff=np.zeros(40,dtype=int)
        for x in P:coeff[x]+=1
        for x in Q:coeff[x]-=1
        assert np.all(coeff@Lraw==0);support6.add(s)
    assert len(support6)==240
    # Mixed support <=8 is impossible: projection onto the mutually orthogonal centered sectors
    # forces nonzero line and tritangent coefficient blocks to be centered dependencies separately.
    # Their exact support minima are 4 and >=5, hence any mixed relation has support >=9.
    # Preserve the pure-tritangent support-eight family from Pass4998.
    AT=nx.Graph();AT.add_nodes_from(range(45))
    for i,j in itertools.combinations(range(45),2):
        if len(set(T[i])&set(T[j]))==1:AT.add_edge(i,j)
    stars=[frozenset(j for j,t in enumerate(T) if x in t) for x in range(27)]
    tri8={stars[a]^stars[q] for a,q in G27.edges()};assert len(tri8)==135 and {len(x) for x in tri8}=={8}
    out2={
      'pass':5002,'supersedes_global_claim':'Pass4993 exact erasure distance 8',
      'reader':'R=[C^T;M], 85x36, rank36','exact_global_erasure_distance':6,'guaranteed_erasure_tolerance':5,
      'line_centered_dependencies':{'minimum_support':4,'count':40,'identification':'the four W33 line sensors through each W33 point'},
      'minimum_raw_dependencies':{'support':6,'count':240,'pure_line':True,
        'identification':'difference of the two four-line point pencils for a collinear W33 point pair; equivalently one support for each of the 240 W33 point-graph edges'},
      'exact_lower_certificate':{'raw_line_no_dependency_support_2_through_5':True,'raw_tritangent_no_dependency_support_2_through_5':True},
      'mixed_support8':{'exist':False,'reason':'centered line and tritangent row spaces are orthogonal; a mixed dependency projects to a centered dependency in each block. Exact minima are 4 on the line block and at least5 on the tritangent block, so every mixed dependency has support at least9.'},
      'pure_tritangent_support8':{'count':135,'status':'Pass4998 family remains valid as the pure-tritangent minimum, not the global minimum'},
      'theorem':'The global 85-reader erasure distance is 6, not 8. There are exactly 240 canonical six-line failures obtained by subtracting the four-line pencil relations of collinear W33 points, and no dependency of support at most5. There are no mixed line/tritangent support-eight cocircuits. Pass4998 remains correct only as the pure-tritangent support-eight classification.',
      'boundary':'This correction changes the global fault-tolerance statement: every five-sensor erasure is safe; some six-line erasures fail.'}
    O2.write_text(json.dumps(out2,indent=2,sort_keys=True)+'\n')

    # --------------------------------------------------------------- Pass5003
    pair_items=sorted(b['pair_to_res'].items());E=b['E']
    O=np.zeros((270,360),dtype=np.uint8);Bds=np.zeros((270,36),dtype=int);Bpair=np.zeros((270,45),dtype=int)
    for r,(bp,items) in enumerate(pair_items):
        a,q=bp;Bpair[r,a]=Bpair[r,q]=1
        U=[d for d in range(36) if M[a,d]==M[q,d]==0];assert len(U)==6;Bds[r,U]=1
        z=0
        for m,V in items:z^=m
        x=z
        while x:
            lb=x&-x;O[r,lb.bit_length()-1]=1;x^=lb
    Gram=O.astype(int)@O.astype(int).T;X=(Gram==3).astype(int);np.fill_diagonal(X,0)
    ev,V=np.linalg.eigh(X.astype(float));spec=Counter(int(round(x)) for x in ev)
    assert spec==Counter({-4:150,2:84,8:15,14:20,32:1})
    assert (np.linalg.matrix_rank(O.astype(float)),gf2_rank_matrix(O))==(120,90)
    def projrank(B,lam):
        ix=np.where(np.isclose(ev,float(lam),atol=1e-8))[0]
        return int(np.linalg.matrix_rank(V[:,ix].T@B,tol=1e-8))
    dsprof={str(l):projrank(Bds,l) for l in (-4,2,8,14,32)}
    assert dsprof=={'-4':0,'2':0,'8':15,'14':20,'32':1}
    pairprof={str(l):projrank(Bpair,l) for l in (-4,2,8,14,32)}
    assert pairprof=={'-4':20,'2':24,'8':0,'14':20,'32':1}
    assert np.linalg.matrix_rank(Bds)==36 and gf2_rank_matrix(Bds)==35
    out3={
      'pass':5003,'octahedron_set':270,'share3_graph_spectrum':{'32':1,'14':20,'8':15,'2':84,'-4':150},
      'edge_frame':{'real_rank':120,'GF2_rank':90,'active_real_spectral_space':'1 + 20 + 15 + 84'},
      'natural_spread_carrier_map':{'matrix':'270 octahedra x 36 double-sixes missed by the tritangent pair','real_rank':36,'GF2_rank':35,
        'spectral_projection_ranks':dsprof,'identification':'its real image is exactly the 32,14,8 eigenspaces = 1+20+15'},
      'natural_tritangent_endpoint_map':{'matrix':'270 intersecting tritangent pairs x 45 tritangents','real_rank':45,
        'spectral_projection_ranks':pairprof,'V20_to_active20':'projecting endpoint incidence to the eigenvalue14 eigenspace gives an explicit rank20 equivariant map'},
      'active84':'the remaining eigenvalue2 active space after the canonical 1+20+15 spread image','real_dimension':84,
      'Hodge120_test':'NO real equivariant identification with the Pass1487 coexact 30+90 carrier: the octahedral real row space contains a one-dimensional invariant constant vector, while coexact 30+90 has no trivial constituent.',
      'degree90_test':'The binary rank90 is a modular rank, not a real 90-dimensional spectral constituent; no real degree90 block occurs in the octahedral active decomposition.',
      'theorem':'The 120-dimensional real octahedral edge-frame image has the canonical invariant decomposition 1+20+15+84. The first 36 dimensions are the explicit image of the 36-spread/double-six permutation carrier, while the tritangent endpoint carrier projects equivariantly and with rank20 onto the active 20. The remaining active sector has dimension84. This rules out identifying real rank120 with the coexact 30+90 module and rules out reading the binary rank90 as the real degree90 constraint irrep.',
      'boundary':'The 84-dimensional eigenspace may decompose further as a group module; this pass identifies it spectrally and by complement but does not assert irreducibility.'}
    O3.write_text(json.dumps(out3,indent=2,sort_keys=True)+'\n')

    # --------------------------------------------------------------- Pass5004
    prev=json.loads((ROOT/'data/PART_W33_PASS4994_RESIDUAL_C3_AFFINE_GAUGE.json').read_text())
    P=prev['PSp_point_line_stabilizer'];F=prev['full_PGSp_point_line_stabilizer']
    assert (P['order'],P['image_order'],P['kernel_order'])==(162,3,54)
    assert (F['order'],F['image_order'],F['kernel_order'])==(324,6,54)
    out4={
      'pass':5004,'residual_triple':'one of the four point-indexed AG(2,3) completion packets after choosing a base-line point',
      'PSp_action':{'stabilizer_order':162,'image':'C3 regular/transitive','kernel_order':54,'fixed_completion_count':0},
      'PGSp_action':{'stabilizer_order':324,'image':'S3 transitive','kernel_order':54,'fixed_completion_count':0},
      'equivariant_origin_selector_exists':False,
      'proof':'Any intrinsic PSp-equivariant selector must be fixed by the stabilizer of the chosen line and point. Its quotient C3 acts regularly on the three completions, so no completion is fixed. Adding the outer PGSp/Witting C2 enlarges the image to S3 and still creates no fixed point.',
      'Witting_phase_role':'The finite Witting outer sign supplies the C2 reflection parity S3/C3; it orients the torsor but does not choose a C3 origin.',
      'external_reference_requirement':{'to_choose_origin_under_PSp':'break the order162 stabilizer to its order54 kernel','to_choose_origin_under_full_PGSp':'one completion has stabilizer order108; choosing both origin and outer orientation leaves order54'},
      'hardware_reading':'An OAM/time-bin phase convention can choose an origin only as calibration/reference data that breaks the intrinsic C3 symmetry. No reference-free finite-geometric origin exists.',
      'theorem':'The residual qutrit triple is a genuine torsor: there is no intrinsic PSp- or PGSp-equivariant choice of zero. Witting phase supplies reflection parity but cannot supply the missing C3 origin. A physical compiler must therefore carry an external phase/time-bin/OAM reference (or equivalent symmetry-breaking datum) if it wants named states 0,1,2.',
      'boundary':'This is a group-action no-go for intrinsic labeling. It does not say which laboratory reference is optimal or identify the finite outer sign with spacetime CP.'}
    O4.write_text(json.dumps(out4,indent=2,sort_keys=True)+'\n')
    return 0
if __name__=='__main__':raise SystemExit(main())
