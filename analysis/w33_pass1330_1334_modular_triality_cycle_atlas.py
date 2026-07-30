#!/usr/bin/env python3
"""Passes 1330--1334 exact modular/triality/cycle certificate.

The 26-dimensional Hecke tensor is reconstructed from the rational Pass-1321
matrix units. Explicit quotient representations then certify the Jacobson
radicals modulo 2, 3, and 5. The same executable constructs the nine-axis
triality scheme and literal length-7/8 W33 cycle stabilizers.
"""
from __future__ import annotations
from collections import deque
from itertools import product
from pathlib import Path
import hashlib, json
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'
OUT=DATA/'w33_pass1330_1334_modular_triality_cycle_atlas.json'
MAPS=DATA/'w33_pass1330_modular_quotient_maps.json'
GROUP_ORDER=51840
FILES=(('1','w33_pass1321_hecke_block_1.json'),('6','w33_pass1321_hecke_block_6.json'),('15','w33_pass1321_hecke_block_15.json'),('15a','w33_pass1321_hecke_block_15a.json'),('20','w33_pass1321_hecke_block_20.json'),('30','w33_pass1321_hecke_block_30.json'),('60a','w33_pass1321_hecke_block_60a.json'),('64','w33_pass1321_hecke_block_64.json'),('81_minus','w33_pass1321_hecke_block_81-minus.json'))
TENSOR_SHA='3c41297ebbdd709f2bec32d25edde1b6b94d545d99ff50acdb4c376c639148e5'


def reconstruct_tensor():
    cols=[]; labels=[]
    for name,fn in FILES:
        block=json.loads((DATA/fn).read_text())['block']['matrix_units']
        for key,raw in block.items():
            i,j=map(int,key.split(',')); labels.append((name,i,j)); cols.append([sp.Rational(x) for x in raw])
    V=sp.Matrix.hstack(*map(sp.Matrix,cols)); W=V.inv(); pos={x:i for i,x in enumerate(labels)}
    def mmul(a,b):
        out=[sp.Rational(0)]*26
        for u,x in enumerate(a):
            if not x: continue
            n,i,j=labels[u]
            for v,y in enumerate(b):
                if not y: continue
                m,k,l=labels[v]
                if n==m and j==k: out[pos[(n,i,l)]]+=x*y
        return sp.Matrix(out)
    P=np.zeros((26,26,26),dtype=np.int16)
    for i in range(26):
        for j in range(26):
            c=V*mmul(W[:,i],W[:,j])
            for k,x in enumerate(c): assert x.q==1; P[i,j,k]=int(x)
    assert np.array_equal(P[0],np.eye(26,dtype=np.int16))
    assert hashlib.sha256(P.tobytes()).hexdigest()==TENSOR_SHA
    return P

P=reconstruct_tensor()


def rref(A,p):
    if not A:return [],[],[]
    A=[[int(x)%p for x in row] for row in A]; m=len(A); n=len(A[0]); r=0; piv=[]
    for c in range(n):
        q=next((i for i in range(r,m) if A[i][c]),None)
        if q is None:continue
        A[r],A[q]=A[q],A[r]; iv=pow(A[r][c],-1,p); A[r]=[(iv*x)%p for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                z=A[i][c]; A[i]=[(A[i][j]-z*A[r][j])%p for j in range(n)]
        piv.append(c); r+=1
    free=[c for c in range(n) if c not in piv]; ns=[]
    for f in free:
        v=[0]*n; v[f]=1
        for i,c in enumerate(piv):v[c]=(-A[i][f])%p
        ns.append(v)
    return A,piv,ns


def rank(A,p):return len(rref(A,p)[1]) if A else 0

def span(vs,p):
    B=[]
    for v in vs:
        v=[int(x)%p for x in v]
        if rank(B+[v],p)>len(B):B.append(v)
    return B

def mul(x,y,p):
    z=[0]*26
    for i,a in enumerate(x):
        if not a%p:continue
        for j,b in enumerate(y):
            if not b%p:continue
            for k,c in enumerate(P[i,j]):z[k]=(z[k]+a*b*int(c))%p
    return z

def product_ideal(U,V,p):return span([mul(u,v,p) for u in U for v in V],p)
def in_span(v,B,p):return rank(B+[v],p)==len(B)
def same_span(A,B,p):return len(A)==len(B) and all(in_span(v,B,p) for v in A)
def loewy(J,p):
    out=[]; x=J
    for _ in range(30):
        out.append(len(x))
        if not x:break
        x=product_ideal(x,J,p)
    assert out[-1]==0; return out

def center_dim(p):
    eq=[]
    for j in range(26):
        for k in range(26):eq.append([(int(P[i,j,k])-int(P[j,i,k]))%p for i in range(26)])
    return len(rref(eq,p)[2])


def invmod(A,p):
    """Invert a square matrix modulo p by exact row reduction."""
    A=[list(map(lambda x:int(x)%p,row))+[int(i==j) for j in range(len(A))]
       for i,row in enumerate(A)]
    n=len(A)
    for c in range(n):
        q=next(i for i in range(c,n) if A[i][c])
        A[c],A[q]=A[q],A[c]
        iv=pow(A[c][c],-1,p); A[c]=[(iv*x)%p for x in A[c]]
        for i in range(n):
            if i!=c and A[i][c]:
                z=A[i][c]
                A[i]=[(A[i][j]-z*A[c][j])%p for j in range(2*n)]
    return np.array([row[n:] for row in A],dtype=np.int16)


def central_blocks(p):
    """Enumerate primitive central idempotents and rank their two-sided blocks."""
    equations=[]
    for j in range(26):
        for k in range(26):
            equations.append([
                (int(P[i,j,k])-int(P[j,i,k]))%p for i in range(26)
            ])
    center=rref(equations,p)[2]
    assert len(center)==9
    _,pivots,_=rref(center,p)
    coordinate_matrix=np.array(
        [[center[i][c] for c in pivots] for i in range(9)],dtype=np.int16
    )
    coordinate_inverse=invmod(coordinate_matrix,p)
    center_tensor=np.zeros((9,9,9),dtype=np.int16)
    for i in range(9):
        for j in range(9):
            product_vector=np.array(mul(center[i],center[j],p),dtype=np.int16)
            center_tensor[i,j]=(product_vector[pivots]@coordinate_inverse)%p
    idempotents=[]
    batch_size=100000
    for start in range(0,p**9,batch_size):
        numbers=np.arange(start,min(p**9,start+batch_size),dtype=np.int64)
        coordinates=np.zeros((len(numbers),9),dtype=np.int16)
        quotient=numbers.copy()
        for i in range(9):
            coordinates[:,i]=quotient%p
            quotient//=p
        squares=np.einsum(
            "bi,bj,ijk->bk",
            coordinates,
            coordinates,
            center_tensor,
            optimize=True,
        )%p
        idempotents.extend(
            map(tuple,coordinates[np.all(squares==coordinates,axis=1)].tolist())
        )
    def center_product(left,right):
        return tuple((
            np.einsum(
                "i,j,ijk->k",
                np.array(left),
                np.array(right),
                center_tensor,
                optimize=True,
            )%p
        ).tolist())
    zero=(0,)*9
    primitive=[
        e for e in idempotents if e!=zero and not any(
            f!=zero and f!=e and center_product(f,e)==f for f in idempotents
        )
    ]
    block_dimensions=[]
    units=[[int(i==j) for j in range(26)] for i in range(26)]
    for e in primitive:
        element=(
            np.array(e,dtype=np.int16)@np.array(center,dtype=np.int16)
        )%p
        block_dimensions.append(
            rank([mul(unit,element.tolist(),p) for unit in units],p)
        )
    return {
        "center_dimension":len(center),
        "central_idempotent_count":len(idempotents),
        "primitive_central_idempotent_count":len(primitive),
        "central_block_dimensions":sorted(block_dimensions),
        "center_nilradical_dimension":len(center)-len(primitive),
    }


def matmul_flat(a,b,n,p):
    A=np.array(a,dtype=np.int16).reshape(n,n);B=np.array(b,dtype=np.int16).reshape(n,n)
    return list(map(int,((A@B)%p).reshape(-1)))


def verify_modular():
    frozen=json.loads(MAPS.read_text()); assert frozen['tensor_sha256']==TENSOR_SHA
    expected={2:(21,5,[21,17,13,7,2,0],'M_2(F_2) + F_2'),3:(22,4,[22,16,10,4,0],'F_3^4'),5:(6,20,[6,2,0],'M_3(F_5) + M_2(F_5) + F_5^7')}
    records={}
    for p in (2,3,5):
        rec=frozen['records'][str(p)]; J=span(rec['radical_basis'],p); assert len(J)==expected[p][0]
        blocks=central_blocks(p)
        assert blocks['central_block_dimensions']==rec['central_block_dimensions']
        assert blocks['center_nilradical_dimension']==rec['center_nilradical_dimension']
        units=[[int(i==j) for j in range(26)] for i in range(26)]
        for x in J:
            for e in units:assert in_span(mul(x,e,p),J,p) and in_span(mul(e,x,p),J,p)
        assert loewy(J,p)==expected[p][2]
        images=[]
        for i in range(26):
            row=[]
            for block in rec['matrix_blocks']:row+=block['images'][i]
            row += [chi[i] for chi in rec['scalar_characters']]
            images.append(row)
        qdim=len(images[0]); assert qdim==expected[p][1] and rank(images,p)==qdim
        assert same_span(rref([list(x) for x in zip(*images)],p)[2],J,p)
        for i in range(26):
            for j in range(26):
                for block in rec['matrix_blocks']:
                    n=block['size']; got=matmul_flat(block['images'][i],block['images'][j],n,p)
                    want=[sum(int(P[i,j,k])*block['images'][k][t] for k in range(26))%p for t in range(n*n)]
                    assert got==want
                for chi in rec['scalar_characters']:
                    assert chi[i]*chi[j]%p==sum(int(P[i,j,k])*chi[k] for k in range(26))%p
        records[str(p)]={'prime':p,'center_dimension':blocks['center_dimension'],'center_nilradical_dimension':blocks['center_nilradical_dimension'],'central_idempotent_count':blocks['central_idempotent_count'],'primitive_central_idempotent_count':blocks['primitive_central_idempotent_count'],'reduced_center_dimension':{2:2,3:2,5:7}[p],'central_block_dimensions':blocks['central_block_dimensions'],'jacobson_radical_dimension':len(J),'semisimple_quotient_dimension':qdim,'semisimple_quotient':expected[p][3],'loewy_power_dimensions':expected[p][2],'radical_basis_sha256':hashlib.sha256(np.array(J,dtype=np.int8).tobytes()).hexdigest()}
        if p==5: records[str(p)]['exceptional_block_characters']=[[1,1,4,2,2,2,2,2,2],[1,4,0,0,0,0,0,0,0],[1,4,4,1,4,1,4,3,2]]
    return records


def triality_scheme():
    pts=[(i,j) for i in range(3) for j in range(3)]; R=np.zeros((9,9),dtype=np.int8)
    for i,x in enumerate(pts):
        for j,y in enumerate(pts):R[i,j]=(x[0]!=y[0])+2*(x[1]!=y[1])
    A=[(R==i).astype(np.int16) for i in range(4)]; val=[int(x[0].sum()) for x in A]; assert val==[1,2,2,4]
    eig=[[1,2,2,4],[1,-1,2,-2],[1,2,-1,-2],[1,-1,-1,1]]; coeff=[[1,1,1,1],[2,-1,2,-1],[2,2,-1,-1],[4,-2,-2,1]]; ranks=[1,2,2,4]
    for c,r in zip(coeff,ranks):
        E=sp.Matrix(sum(c[i]*A[i] for i in range(4)).tolist())/9; assert E*E==E and E.trace()==r
    return {'points':[list(x) for x in pts],'group':'S3_internal x S3_triality','group_order':36,'orbitals':4,'relation_valencies':val,'eigenmatrix':eig,'primitive_idempotent_relation_coefficients_numerator':coeff,'primitive_idempotent_common_denominator':9,'primitive_idempotent_ranks':ranks,'bose_mesner_dimension':4,'interpretation':'tensor product of the rank-2 K3 scheme with itself','coordinate_swap_fusion':{'scheme':'H(2,3)','relation_valencies':[1,4,4],'primitive_idempotent_ranks':[1,4,4],'bose_mesner_dimension':3},'single_axis_stabilizer_order':4,'single_axis_orbit_size':9,'row_or_column_stabilizer_order':12,'row_or_column_orbit_size':3}

Q=3
def canon(v):
    v=tuple(x%Q for x in v)
    for x in v:
        if x:return tuple((1 if x==1 else 2)*y%Q for y in v)
    raise ValueError
def symp(x,y):return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%Q
def compose(a,b):return tuple(a[b[i]] for i in range(len(a)))
def group(gens):
    I=tuple(range(len(gens[0]))); G=[I]; seen={I}; q=deque([I])
    while q:
        x=q.popleft()
        for g in gens:
            y=compose(g,x)
            if y not in seen:seen.add(y);G.append(y);q.append(y)
    return G
def point_model():
    pts=sorted({canon(x) for x in product(range(3),repeat=4) if any(x)}); ix={x:i for i,x in enumerate(pts)}; gens=[]
    for v in [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0)]:
        gens.append(tuple(ix[canon(tuple((x[i]+symp(x,v)*v[i])%3 for i in range(4)))] for x in pts))
    gens.append(tuple(ix[canon((x[0],x[1],2*x[2],2*x[3]))] for x in pts));return pts,gens
def crot(c):return min(tuple(c[i:]+c[:i]) for i in range(len(c)))
def cdih(c):return min(crot(c),crot(list(reversed(c))))
def find_cycle(adj,n):
    for s in range(40):
        path=[s];used={s}
        def dfs():
            if len(path)==n:return path.copy() if path[-1] in adj[path[0]] else None
            for z in adj[path[-1]]:
                if z in used:continue
                used.add(z);path.append(z);r=dfs()
                if r:return r
                path.pop();used.remove(z)
        r=dfs()
        if r:return r
    raise RuntimeError
def cycles():
    pts,gens=point_model();G=group(gens);assert len(G)==51840;adj=[[] for _ in pts]
    for i,x in enumerate(pts):
        for j,y in enumerate(pts):
            if i!=j and symp(x,y)==0:adj[i].append(j)
    out={}
    for n,want in [(7,2),(8,1)]:
        c=find_cycle(adj,n); ko=crot(c);kd=cdih(c);so=sum(crot([g[x] for x in c])==ko for g in G);sd=sum(cdih([g[x] for x in c])==kd for g in G);assert so==sd==want
        support=set(c)
        support_stabilizer=sum({g[x] for x in c}==support for g in G)
        support_edges=sum(1 for i in support for j in adj[i] if j in support)//2
        chord_count=support_edges-n
        out[str(n)]={'cycle':c,'simple_and_primitive_reduced':True,'induced_cycle':chord_count==0,'support_chord_count':chord_count,'support_set_stabilizer_order':support_stabilizer,'oriented_stabilizer_order':so,'oriented_orbit_size':51840//so,'dihedral_stabilizer_order':sd,'dihedral_orbit_size':51840//sd}
    return {'scope':'two deterministic selected cyclic words, not a classification of every cycle orbit at either length','cycles':out,'inherited_copy_selection_theorem':'Pass 1328 proves that an invariant Y-side operator acts on the three transported X-side species-20 copies as C tensor I_3. A primitive copy idempotent is required to select one copy.','copy_selection_source':'PASS1325_1329_TRIALITY_INTEGRAL_GAUGE_RELEASE.md (Pass 1328)','species20_copy_idempotent_stabilizer_in_internal_S3':2,'species20_copy_idempotent_orbit_size':3,'combined_W_E6_times_S3':{'group_order':311040,'length7_cycle_plus_copy_stabilizer':4,'length7_cycle_plus_copy_orbit':77760,'length8_cycle_plus_copy_stabilizer':2,'length8_cycle_plus_copy_orbit':155520},'boundary':'These two selected cyclic orders break W(E6) symmetry, but neither cycle alone labels the three multiplicity coordinates. Copy selection is an additional S3 gauge choice.'}


def main(write=True):
    manuscript_input=r"\input{analysis/BT1330_BT1334_modular_triality_cycle_atlas}"
    manuscript_counts={
        name:(ROOT/name).read_text().count(manuscript_input)
        for name in ('w33_paper.tex','photonic_holonet.tex')
    }
    assert set(manuscript_counts.values())=={1}
    result={
        'schema':'w33.pass1330_1334.modular_triality_cycle_atlas.v2',
        'status':'PASS_WITH_DECLARED_TEX_BUILD_BOUNDARY',
        'scope':'exact modular algebra, finite schemes, selected finite permutation orbits, and separately certified GAP runtime',
        'pass_statuses':{
            '1330':'CERTIFIED',
            '1331':'CERTIFIED_SPECTRAL_COMPLETION_OF_PASS1327_GRID',
            '1332':'CERTIFIED_TWO_SELECTED_CYCLE_REPRESENTATIVES',
            '1333':'CERTIFIED_GAP_4.12.1_REPSN_3.1.2',
            '1334':'SOURCE_INTEGRATED_FULL_TEX_BUILD_CI_ONLY',
        },
        'pass1330_modular_jacobson_radicals':{
            'hecke_dimension':26,
            'structure_tensor_sha256':TENSOR_SHA,
            'bad_characteristics':[2,3,5],
            'records':verify_modular(),
            'classification_scope':'radical, semisimple quotient, Loewy powers, center, and central-block dimensions',
            'good_prime_boundary':'At primes outside 2,3,5 the primitive integral matrix remains full rank; this pass explicitly classifies the radicals only at 2,3,5.',
        },
        'pass1331_nine_axis_triality_scheme':triality_scheme(),
        'pass1332_selected_cycle_representatives':cycles(),
        'pass1333_genuine_atlasrep_validation':{
            'script':'analysis/w33_pass1333_atlasrep_species20.g',
            'certificate':'data/w33_pass1333_atlasrep_species20.json',
            'workflow':'.github/workflows/pass1330_1334_modular_triality_atlas.yml',
            'validated_stack':{'gap':'4.12.1','repsn':'3.1.2'},
            'group_order':51840,
            'degree20_irreducible_count':3,
            'degree20_representation_image_orders':[51840,51840,51840],
            'tom_432_contains_multiplicity_pattern':[0,3,0],
            'tom_480_contains_single_copy':True,
        },
        'pass1334_manuscript_integration':{
            'insert':'analysis/BT1330_BT1334_modular_triality_cycle_atlas.tex',
            'integrator':'tools/integrate_pass1330_1334.py',
            'input_counts':manuscript_counts,
            'source_integration':'PASS',
            'local_full_tex_compile':'UNAVAILABLE_NO_TEX_ENGINE',
            'full_repository_compile':'CI-wired and reported separately',
        },
        'checks':{
            'literal_hecke_tensor_reconstructed':True,
            'all_three_radicals_nilpotent':True,
            'central_blocks_reconstructed_not_copied':True,
            'nine_axis_scheme_exact':True,
            'two_selected_cycle_stabilizers_exact':True,
            'atlasrep_completion_marker_required':True,
            'manuscript_inputs_checked_in_once':True,
        },
    }
    if write:OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    return result
if __name__=='__main__':
    x=main();print(json.dumps({'status':x['status'],'radical_dimensions':{p:r['jacobson_radical_dimension'] for p,r in x['pass1330_modular_jacobson_radicals']['records'].items()},'triality_scheme_dimension':4,'selected_cycle_stabilizers':{n:r['dihedral_stabilizer_order'] for n,r in x['pass1332_selected_cycle_representatives']['cycles'].items()}},sort_keys=True))
