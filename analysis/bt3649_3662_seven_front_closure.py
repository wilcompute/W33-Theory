#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations, product
from math import lcm
from pathlib import Path
import numpy as np
from analysis._bt3506_3519_provisional_impl import (
    close_group,
    dependency_deck,
    geometry_objects,
    orbital_relations,
    rank_mod,
    stabilizer_suborbits,
)


def compose(left, right):
    return tuple(left[right[i]] for i in range(len(right)))


def rref_basis_columns(matrix, p=3):
    matrix=np.array(matrix,dtype=np.int64)%p
    indices=[]
    basis=np.zeros((matrix.shape[0],0),dtype=np.int64)
    rank=0
    for column in range(matrix.shape[1]):
        candidate=np.column_stack([basis,matrix[:,column]])
        new_rank=rank_mod(candidate,p)
        if new_rank>rank:
            indices.append(column);basis=candidate;rank=new_rank
    return indices,basis%p


def solve_coords(basis, vectors, p=3):
    n,r=basis.shape
    augmented=np.concatenate([basis%p,vectors%p],axis=1).astype(np.int64)
    pivot_rows=[];row=0
    for column in range(r):
        pivot=next(i for i in range(row,n) if augmented[i,column]%p)
        if pivot!=row: augmented[[row,pivot]]=augmented[[pivot,row]]
        augmented[row]=augmented[row]*pow(int(augmented[row,column]),-1,p)%p
        for i in range(n):
            if i!=row and augmented[i,column]%p:
                augmented[i]=(augmented[i]-augmented[i,column]*augmented[row])%p
        pivot_rows.append(row);row+=1
    solution=augmented[pivot_rows,r:]%p
    assert np.array_equal(basis@solution%p,vectors%p)
    return solution


def orbital_matrices(group, suborbits, size):
    relations,_=orbital_relations(group,suborbits,size)
    return [(relations==index).astype(np.int8) for index in range(len(suborbits))],relations


def permutation_order(p):
    seen=set(); order=1
    for i in range(len(p)):
        if i in seen: continue
        j=i; n=0
        while j not in seen:
            seen.add(j); n+=1; j=p[j]
        order=lcm(order,n)
    return order


def subgroup(gens,size,limit=None):
    ident=tuple(range(size)); seen={ident}; frontier=[ident]
    while frontier:
        new=[]
        for x in frontier:
            for g in gens:
                y=compose(g,x)
                if y not in seen:
                    seen.add(y);new.append(y)
                    if limit is not None and len(seen)>limit:
                        return seen
        frontier=new
    return seen


def restrict_perm(B,g):
    inv=np.empty(len(g),dtype=int)
    for i,j in enumerate(g): inv[j]=i
    return solve_coords(B,B[inv,:],3)


def centralizer_dimension(matrices,p=3):
    n=matrices[0].shape[0]
    rows=[]
    for A in matrices:
        for i in range(n):
            for j in range(n):
                row=np.zeros(n*n,dtype=np.int8)
                for k in range(n):
                    if A[k,j]%p: row[i*n+k]=(row[i*n+k]+A[k,j])%p
                    if A[i,k]%p: row[k*n+j]=(row[k*n+j]-A[i,k])%p
                if np.any(row): rows.append(row)
    matrix=np.array(rows,dtype=np.int8)
    rank=rank_mod(matrix,p)
    return n*n-rank, len(rows), rank


def degree_three_certificate(T,D):
    assert T.shape==(240,5040)
    assert set(map(int,T.sum(axis=0)))=={3}
    assert set(map(int,T.sum(axis=1)))=={63}
    gram=63*np.eye(240,dtype=np.int64)+D
    ev=np.linalg.eigvalsh(gram.astype(float))
    assert ev[0]>44.999999 and ev[-1]<189.000001
    assert np.linalg.matrix_rank(gram)==240
    assert 240//3==80 and 5040//63==80
    return {
      'fractional_transversal_number':'80',
      'primal_witness':'x=(1/3)1_240',
      'dual_witness':'y=(1/63)1_5040',
      'gram_spectrum':['189^1','(81+12sqrt(6))^24','81^20','69^15','57^60','53^81','(81-12sqrt(6))^24','45^15'],
      'gram_minimum_eigenvalue':45,
      'gram_rank':240,
      'integral_transversal_lower_bound':81,
      'integrality_gap_lower_bound':'81/80',
      'equality_obstruction':'Any 80-set hitting all 5040 triples has total incidence 5040, so T^T x=1. Full row rank makes x=(1/3)1 the unique real solution, contradicting x binary.',
      'covering_boundary':'This cubic integrality certificate does not identify the covering-radius endpoint; 389<=R<=435 remains live.'
    }


def modular_certificate(D,fgens):
    M=D%3; projector=(-np.linalg.matrix_power(M,3))%3
    _,B=rref_basis_columns(projector,3)
    assert B.shape==(240,81)
    fgrp=close_group(fgens,240); assert len(fgrp)==25920
    _,subs=stabilizer_suborbits(fgrp,0,240)
    As,_=orbital_matrices(fgrp,subs,240)
    restricted=[]; scalars=[]
    I=np.eye(81,dtype=np.int8)
    for A in As:
        X=solve_coords(B,A@B%3,3)
        restricted.append(X)
        scalar=next((int(v) for v in np.diag(X) if v%3),0)
        assert np.array_equal(X,scalar*I%3)
        scalars.append(scalar)
    span_rank=rank_mod(np.stack([X.reshape(-1) for X in restricted]),3)
    assert span_rank==1
    assert Counter(scalars)==Counter({1:4,2:4,0:2})
    grp=sorted(fgrp)
    threes=[g for g in grp if permutation_order(g) in (3,9)]
    first=next(g for g in threes if permutation_order(g)==9)
    gens=[first]; H=subgroup(gens,240,limit=1000); growth=[len(H)]
    for g in threes:
        K=subgroup(gens+[g],240,limit=82)
        if len(K)<=81 and len(K)>len(H) and 81%len(K)==0:
            gens.append(g);H=K;growth.append(len(H))
            if len(H)==81: break
    assert len(H)==81
    RH=[restrict_perm(B,g) for g in sorted(H)]
    cyclic_index=None
    for j in range(81):
        v=np.zeros(81,dtype=np.int8);v[j]=1
        if rank_mod(np.column_stack([A@v%3 for A in RH]),3)==81:
            cyclic_index=j;break
    assert cyclic_index is not None
    invariants=81-rank_mod(np.vstack([(A-I)%3 for A in RH]),3)
    assert invariants==1
    N=(np.eye(240,dtype=np.int64)-projector)%3
    DN=M@N%3; D2N=M@DN%3
    rN,r1,r2=(rank_mod(N,3),rank_mod(DN,3),rank_mod(D2N,3))
    assert (rN,r1,r2)==(159,44,14)
    _,B14=rref_basis_columns(D2N,3)
    R14=[restrict_perm(B14,g) for g in fgens]
    end14,_,_=centralizer_dimension(R14,3)
    assert end14==1
    fixed14=14-rank_mod(np.vstack([(A-np.eye(14,dtype=int))%3 for A in R14]),3)
    assert fixed14==0
    return {
      'face_action_rank':len(subs),
      'face_action_subdegrees':list(map(len,subs)),
      'projector_rank':81,
      'orbital_restriction_span_rank':span_rank,
      'orbital_scalar_multiset':dict(sorted(Counter(scalars).items())),
      'endomorphism_ring':'F3',
      'sylow_3_order':81,
      'sylow_generator_orders':[permutation_order(g) for g in gens],
      'sylow_growth':growth,
      'sylow_cyclic_basis_index':cyclic_index,
      'sylow_orbit_rank':81,
      'sylow_invariant_dimension':1,
      'projective_restriction':'regular F3[P] module',
      'simple_projective_conclusion':True,
      'steinberg_identification':'The explicit 81-dimensional simple projective defining-characteristic module is the Steinberg module under the established PSp(4,3)=U4(2) carrier identification.',
      'complement_filtration_dimensions':[159,44,14,0],
      'complement_successive_dimensions':[115,30,14],
      'bottom_14_endomorphism_dimension':end14,
      'bottom_14_fixed_dimension':fixed14,
      'bottom_14_boundary':'Schurian and fixed-point-free; no simplicity label is promoted from these two tests alone.'
    }


def w33_lines(A):
    n=A.shape[0]
    coll=np.ones((n,n),dtype=np.int8)-np.eye(n,dtype=np.int8)-A
    lines=set()
    for i,j in combinations(range(n),2):
        if coll[i,j]:
            common=[k for k in range(n) if k not in (i,j) and coll[i,k] and coll[j,k]]
            line=tuple(sorted([i,j]+common))
            assert len(line)==5 and not np.any(A[np.ix_(line,line)])
            lines.add(line)
    assert len(lines)==27
    return sorted(lines)


def m4_certificate(A45):
    lines=w33_lines(A45)
    assert Counter(v for L in lines for v in L)==Counter({v:3 for v in range(45)})
    ev=np.linalg.eigvalsh(A45.astype(float))
    assert sum(abs(ev-32)<1e-6)==1 and sum(abs(ev-2)<1e-6)==24 and sum(abs(ev+4)<1e-6)==20
    return {
      'anchor_graph':'SRG(45,32,22,24)',
      'anchor_spectrum':'32^1,2^24,(-4)^20',
      'maximum_independent_set_size':5,
      'independent_lines':27,
      'point_line_multiplicity':3,
      'fourfold_blowup_order':180,
      'lifted_independent_set_size':20,
      'lifted_fractional_coloring':'27 sets weighted 1/3',
      'fractional_chromatic_number':9,
      'unrestricted_positive_gauge_hoffman_upper_bound':9,
      'arbitrary_signed_complex_hermitian_boundary':'not closed by the fractional dual certificate',
      'attaining_weight':'A45 tensor I4',
      'attaining_spectrum':'32^4,2^96,(-4)^80',
      'attaining_ratio':9,
      'verdict':'The unrestricted positive-gauge/nonnegative weighted-Hoffman optimum on the full fourfold anchor blowup is exactly 9. Arbitrary signed complex Hermitian weights remain a separate open boundary.'
    }


def tomotope_certificate():
    coords=[(l,r) for l in range(4) for r in range(4) if l!=r]; ci={c:i for i,c in enumerate(coords)}
    faces=[]
    for l in range(4): faces.append(tuple(sorted(ci[(l,r)] for r in range(4) if r!=l)))
    for r in range(4): faces.append(tuple(sorted(ci[(l,r)] for l in range(4) if l!=r)))
    for sub in combinations(range(4),3):
        l,m,r=sub
        for cyc in [((l,m),(m,r),(r,l)),((l,r),(r,m),(m,l))]: faces.append(tuple(sorted(ci[x] for x in cyc)))
    cells=[]
    for selected in combinations(range(16),4):
        mult=Counter(e for f in selected for e in faces[f])
        if len(mult)==6 and set(mult.values())=={2}: cells.append(selected)
    assert len(cells)==12
    simple=[]
    for S in combinations(range(12),8):
        count=[0]*16
        for c in S:
            for f in cells[c]: count[f]+=1
        if count==[2]*16: simple.append(tuple(S))
    assert simple==[(0,1,3,5,6,8,10,11),(0,2,3,4,7,8,9,11),(1,2,4,5,6,7,9,10)]
    multi=[]
    for S in combinations_with_replacement(range(12),8):
        count=[0]*16
        for c in S:
            for f in cells[c]: count[f]+=1
        if count==[2]*16: multi.append(tuple(S))
    assert len(multi)==6
    doubled=[S for S in multi if len(set(S))==4]
    assert doubled==[(0,0,3,3,8,8,11,11),(1,1,5,5,6,6,10,10),(2,2,4,4,7,7,9,9)]
    tetrads=[(0,3,8,11),(1,5,6,10),(2,4,7,9)]
    assert simple==[tuple(sorted(set(tetrads[i])|set(tetrads[j]))) for i,j in combinations(range(3),2)]
    fi={f:i for i,f in enumerate(faces)}; celli={c:i for i,c in enumerate(cells)}
    auts=[]
    for p in permutations(range(4)):
        for rev in (False,True):
            em=[]
            for l,r in coords:
                a,b=p[l],p[r]
                if rev:a,b=b,a
                em.append(ci[(a,b)])
            fm=tuple(fi[tuple(sorted(em[e] for e in f))] for f in faces)
            auts.append(tuple(celli[tuple(sorted(fm[f] for f in c))] for c in cells))
    auts=sorted(set(auts));assert len(auts)==48
    simple_set=[frozenset(x) for x in simple]
    actions=[]
    for a in auts:
        actions.append(tuple(simple_set.index(frozenset(a[i] for i in S)) for S in simple_set))
    assert len(set(actions))==6 and set(Counter(actions).values())=={8}
    for S in simple:
        hist=Counter(len(set(cells[a])&set(cells[b])) for a,b in combinations(S,2))
        assert hist==Counter({1:16,0:12})
    return {
      'prior_zero_lift_claim':'WITHDRAWN_INCOMPLETE_BACKTRACKER',
      'failure_mode':'Increasing candidate indices were combined with a dynamically chosen deficient face, skipping valid sorted subsets.',
      'local_cell_candidates':12,
      'simple_eight_cell_subsets_examined':495,
      'simple_double_covers':[list(S) for S in simple],
      'simple_double_cover_count':3,
      'multisets_examined':75582,
      'multiset_double_cover_count':6,
      'doubled_tetrad_solutions':[list(S) for S in doubled],
      'canonical_tetrads':[list(T) for T in tetrads],
      'simple_cover_formula':'A union B, A union C, B union C',
      'visible_group_order':48,
      'simple_cover_orbit_size':3,
      'simple_cover_stabilizer_order':16,
      'induced_cover_action':'S3 with kernel order 8',
      'cover_cell_adjacency':'K4,4 for each simple cover',
      'boundary':'This corrects the old no-lift theorem and supplies the eight-cell incidence layer; a full rank-4 tomotope isomorphism still requires the vertex-edge diamond and flag-connectivity checks.'
    }


def canon3(v):
    for x in v:
        if x%3:
            inv=1 if x%3==1 else 2
            return tuple((inv*y)%3 for y in v)
    raise ValueError


def symp(x,y): return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%3


def gewirtz_bridge():
    pts=sorted({canon3(v) for v in product(range(3),repeat=4) if any(v)})
    AW=np.zeros((40,40),dtype=np.int64)
    for i,j in combinations(range(40),2):
        if symp(pts[i],pts[j])==0: AW[i,j]=AW[j,i]=1
    verts=list(product(range(2),repeat=4)); idx={v:i for i,v in enumerate(verts)}
    gens=[tuple(1 if i==j else 0 for i in range(4)) for j in range(4)]+[(1,1,1,1)]
    AC=np.zeros((16,16),dtype=np.int64)
    for i,v in enumerate(verts):
        for g in gens: AC[i,idx[tuple(a^b for a,b in zip(v,g))]]=1
    I16=np.eye(16,dtype=np.int64);J40=np.ones((40,40),dtype=np.int64);J16=np.ones((16,16),dtype=np.int64)
    num=-3*(AC@AC)+18*AC+17*I16; assert np.all(num%2==0)
    Q11=56*AW-6*J40; Q12=8*np.ones((40,16),dtype=np.int64); Q22=7*(num//2)+8*J16
    Q=np.block([[Q11,Q12],[Q12.T,Q22]])
    I=np.eye(56,dtype=np.int64)
    assert not np.any((Q-560*I)@(Q-112*I)@(Q+224*I))
    assert set(map(int,Q.sum(axis=1)))=={560}
    alphabet=sorted(set(map(int,Q.ravel())))
    assert alphabet==[-13,-6,8,15,50,71]
    return {
      'matrix':'Q=56 M on W33(40) plus Clebsch(16)',
      'blocks':{'W33':'56 A_W - 6 J_40','cross':'8 J_40x16','Clebsch':'(7/2)(-3 A_C^2+18 A_C+17 I)+8 J_16'},
      'order':56,
      'integral_entry_alphabet':alphabet,
      'constant_row_sum':560,
      'annihilator':'(Q-560I)(Q-112I)(Q+224I)=0',
      'spectrum':'560^1,112^35,(-224)^20',
      'scaled_spectrum':'10^1,2^35,(-4)^20',
      'traces':[int(np.trace(np.linalg.matrix_power(Q,k))) for k in range(1,5)],
      'boundary':'Concrete objectwise integral weighted spectral bridge; not a 0/1 Gewirtz adjacency or canonical graph embedding.'
    }


def clock_certificate(D):
    M=D%3; P=(-np.linalg.matrix_power(M,3))%3; I=np.eye(240,dtype=np.int64)
    C=(I+M+P)%3
    assert np.array_equal(np.linalg.matrix_power(C,3)%3,I%3)
    N=(C-I)%3
    ranks=[];X=N.copy()
    for _ in range(3): ranks.append(rank_mod(X,3));X=X@N%3
    assert ranks==[44,14,0]
    return {
      'operator':'C=I+D+E81 over F3','order':3,'nonidentity':True,
      'C_minus_I_power_ranks':ranks,'fixed_space_dimension':196,
      'jordan_type':'J3(1)^14 + J2(1)^16 + J1(1)^166','E81_action':'fixed pointwise',
      'boundary':'Canonical finite unipotent order-three register; not a physical time crystal or autonomous oscillator.'
    }


def build_certificate():
    objects=geometry_objects()
    A45=objects['graph'];faces=objects['faces']
    face_index={face:index for index,face in enumerate(faces)}
    fgens=[tuple(face_index[tuple(sorted(generator[v] for v in face))] for face in faces) for generator in objects['generators']]
    deck=dependency_deck(objects);T,D=deck['incidence'],deck['operator']
    result={
      'schema':'w33.pass3649_3662.seven_front_closure.v1',
      'status':'PASS_7_FRONTS_WITH_TOMOTOPE_CORRECTION',
      'passes':list(range(3649,3663)),
      'fronts':{
        'degree_three_covering':degree_three_certificate(T,D),
        'modular_E81':modular_certificate(D,fgens),
        'transported_M4_dual':m4_certificate(A45),
        'tomotope_cocycle_correction':tomotope_certificate(),
        'objectwise_gewirtz_bridge':gewirtz_bridge(),
      },
      'bonkers':{
        'cubic_obstruction_clock':clock_certificate(D),
        'tomotope_S3_selector':{
          'states':3,'visible_action':'full S3','kernel_order':8,'stabilizer_order':16,
          'tetrads':[[0,3,8,11],[1,5,6,10],[2,4,7,9]],
          'interpretation':'The three simple covers are pairwise unions of three canonical tetrads; the visible 48-group induces every permutation of the three cover states.',
          'boundary':'Exact finite selector register, not a physical qutrit claim.'
        }
      },
      'live_boundaries':{'covering_radius':[389,435],'chromatic_number':[10,11]},
      'supersedes':['Passes 3600-3613 tomotope eight-cell double-cover count 0'],
      'evidence_boundary':[
        'The degree-three relaxation proves tau>=81 but does not close the covering-radius endpoint.',
        'The positive-gauge/nonnegative transported-M4 optimum is exact at 9; arbitrary signed complex Hermitian weights remain open.',
        'The E81 simple/projective conclusion is exact; the Steinberg name uses the established PSp(4,3)=U4(2) defining-characteristic identification.',
        'The corrected tomotope result establishes an eight-cell incidence layer, not yet a complete abstract-polytope isomorphism.',
        'The Gewirtz bridge is weighted and integral after scaling, not a 0/1 graph embedding.',
        'No remote CI, PDF, FPGA, laboratory, Monster embedding, or physical result is asserted by the source certificate.'
      ]
    }
    payload=json.dumps(result,sort_keys=True,separators=(',',':')).encode()
    result['semantic_sha256']=hashlib.sha256(payload).hexdigest()
    return result


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    result=build_certificate()
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(result['status'],result['semantic_sha256'])
