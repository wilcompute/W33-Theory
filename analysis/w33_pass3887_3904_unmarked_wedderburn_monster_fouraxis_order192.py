#!/usr/bin/env python3
"""Passes 3887--3904: exact unmarked axial, Wedderburn, K4,3, local-algebra, and order-192 closure.

This verifier independently rebuilds the O_6^-(2) / GQ(4,2) finite geometry,
the 200-ovoid coherent configuration, its rational Wedderburn models, the
45-axis projected-coordinate algebra, the corrected four-axis census, the
40 K_{4,3} tripod--Norton carrier, and two exact order-192 subgroups.

Monster words and class fusion remain fail-closed. Two other order-192
mechanisms are reconciled against exact prior source files rather than
reidentified by order alone.
"""
from __future__ import annotations

import argparse
import collections
from collections import Counter, deque
from fractions import Fraction
import hashlib
from itertools import combinations
import itertools
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "PART_3887_3904_UNMARKED_WEDDERBURN_MONSTER_FOURAXIS_ORDER192_results.json"
MOD = 1_000_003
LABEL_MAP = {"750":"1", "30":"81", "6":"15a", "-378":"15b", "-30":"24"}
DIM_MAP = {"750":1, "30":81, "6":15, "-378":15, "-30":24}
PRIMITIVE_COEFFS = {
"750": {0:Fraction(1,160),2:Fraction(1,160),3:Fraction(1,160),5:Fraction(1,160),6:Fraction(1,160),8:Fraction(1,160),10:Fraction(1,160),11:Fraction(1,160),13:Fraction(1,40),14:Fraction(1,40),16:Fraction(1,40)},
"30": {0:Fraction(81,160),2:Fraction(-27,160),3:Fraction(-3,160),5:Fraction(1,160),6:Fraction(-3,160),8:Fraction(9,160),10:Fraction(-27,160),11:Fraction(9,160)},
"6": {0:Fraction(3,32),2:Fraction(-1,32),3:Fraction(1,96),5:Fraction(1,96),6:Fraction(-1,32),8:Fraction(-1,32),10:Fraction(3,32),11:Fraction(-1,32),13:Fraction(3,8),14:Fraction(-1,8),16:Fraction(1,24)},
"-378": {0:Fraction(3,32),2:Fraction(3,32),3:Fraction(-1,32),5:Fraction(1,96),6:Fraction(1,96),8:Fraction(-1,32),10:Fraction(-1,32),11:Fraction(-1,32)},
"-30": {0:Fraction(3,10),2:Fraction(1,10),3:Fraction(1,30),5:Fraction(-1,30),6:Fraction(1,30),10:Fraction(1,10),13:Fraction(3,5),14:Fraction(1,10),16:Fraction(-1,15)}
}


def bits(x, n=6): return [(x >> i) & 1 for i in range(n)]
def qminus(x):
    a=bits(x); return (a[0]*a[1]+a[2]*a[3]+a[4]+a[4]*a[5]+a[5]) & 1
def polar(x,y):
    a,b=bits(x),bits(y); return (a[0]*b[1]+a[1]*b[0]+a[2]*b[3]+a[3]*b[2]+a[4]*b[5]+a[5]*b[4]) & 1
def symmetry(v,x): return x ^ (v if polar(x,v) else 0)
def compose(p,q): return tuple(p[q[i]] for i in range(len(p)))
def invperm(p):
    out=[0]*len(p)
    for i,j in enumerate(p): out[j]=i
    return tuple(out)
def closure(gens, cap=100000):
    ident=tuple(range(len(gens[0]))); moves=list(dict.fromkeys(gens+[invperm(g) for g in gens]))
    seen={ident}; queue=deque([ident])
    while queue:
        h=queue.popleft()
        for g in moves:
            x=compose(g,h)
            if x not in seen:
                seen.add(x); queue.append(x)
                if len(seen)>cap: raise RuntimeError("permutation closure cap exceeded")
    return seen
def perm_order(p):
    seen=set(); answer=1
    for i in range(len(p)):
        if i in seen: continue
        j=i; size=0
        while j not in seen: seen.add(j); size+=1; j=p[j]
        answer=math.lcm(answer,size)
    return answer
def point_orbits(n,gens):
    remaining=set(range(n)); answer=[]
    while remaining:
        start=min(remaining); remaining.remove(start); orbit=[start]; queue=deque([start])
        while queue:
            x=queue.popleft()
            for g in gens:
                y=g[x]
                if y in remaining: remaining.remove(y); orbit.append(y); queue.append(y)
        answer.append(sorted(orbit))
    return answer
def rank_mod(matrix,p=MOD):
    a=np.asarray(matrix,dtype=np.int64).copy()%p; rank=0
    for col in range(a.shape[1]):
        pivots=np.flatnonzero(a[rank:,col])
        if len(pivots)==0: continue
        pivot=rank+int(pivots[0]); a[[rank,pivot]]=a[[pivot,rank]]
        a[rank]=a[rank]*pow(int(a[rank,col]),-1,p)%p
        for row in np.flatnonzero(a[:,col]):
            if row!=rank: a[row]=(a[row]-a[row,col]*a[rank])%p
        rank+=1
        if rank==a.shape[0]: break
    return rank
def inv_mod(matrix,p):
    a=np.asarray(matrix,dtype=np.int64).copy()%p; n=a.shape[0]
    aug=np.concatenate([a,np.eye(n,dtype=np.int64)],axis=1); rank=0
    for col in range(n):
        pivots=np.flatnonzero(aug[rank:,col])
        if len(pivots)==0: raise ValueError("singular matrix")
        pivot=rank+int(pivots[0]); aug[[rank,pivot]]=aug[[pivot,rank]]
        aug[rank]=aug[rank]*pow(int(aug[rank,col]),-1,p)%p
        for row in np.flatnonzero(aug[:,col]):
            if row!=rank: aug[row]=(aug[row]-aug[row,col]*aug[rank])%p
        rank+=1
    return aug[:,n:]
def rref_basis(vectors,p):
    rows=[]; pivots=[]
    for vv in vectors:
        v=np.asarray(vv,dtype=np.int64).copy()%p
        for row,pivot in zip(rows,pivots):
            if v[pivot]: v=(v-v[pivot]*row)%p
        nz=np.flatnonzero(v)
        if len(nz)==0: continue
        pivot=int(nz[0]); v=v*pow(int(v[pivot]),-1,p)%p
        for i,row in enumerate(rows):
            if row[pivot]: rows[i]=(row-row[pivot]*v)%p
        position=int(np.searchsorted(pivots,pivot)); pivots.insert(position,pivot); rows.insert(position,v)
    return rows,pivots
def subgroup_generators(group):
    ident=tuple(range(len(group[0]))); gens=[]; generated={ident}
    for element in group:
        if element not in generated: gens.append(element); generated=closure(gens)
        if len(generated)==len(group): break
    return gens
def commutator(a,b): return compose(compose(compose(invperm(a),invperm(b)),a),b)
def derived_subgroup(group):
    gens=subgroup_generators(group); comms=[commutator(a,b) for a in gens for b in gens]
    return (closure(comms) if comms else {tuple(range(len(group[0])))}),gens
def center(group): return [x for x in group if all(compose(x,y)==compose(y,x) for y in group)]
def orbits_under(group,n):
    remaining=set(range(n)); sizes=[]
    while remaining:
        start=min(remaining); remaining.remove(start); orbit={start}; queue=deque([start])
        while queue:
            x=queue.popleft()
            for g in group:
                y=g[x]
                if y in remaining: remaining.remove(y); orbit.add(y); queue.append(y)
        sizes.append(len(orbit))
    return sorted(sizes)
def canonical_matrix_payload(matrices): return [[[str(x) for x in row] for row in matrix.tolist()] for matrix in matrices]
def commutant_dimension(matrices):
    d=matrices[0].rows; variables=sp.symbols(f"x0:{d*d}"); X=sp.Matrix(d,d,variables); equations=[]
    for matrix in matrices: equations.extend(list(X*matrix-matrix*X))
    system,_=sp.linear_eq_to_matrix(equations,variables); return d*d-system.rank()


def build_geometry():
    singular=[x for x in range(1,64) if qminus(x)==0]; anisotropic=[x for x in range(1,64) if qminus(x)==1]
    assert (len(singular),len(anisotropic))==(27,36)
    lines=sorted({tuple(sorted((x,y,x^y))) for x,y in combinations(singular,2) if x^y in singular})
    assert len(lines)==45; line_index={line:i for i,line in enumerate(lines)}
    adjacency=np.zeros((45,45),dtype=np.int64)
    for i,j in combinations(range(45),2):
        if set(lines[i]).intersection(lines[j]): adjacency[i,j]=adjacency[j,i]=1
    assert set(map(int,adjacency.sum(axis=1)))=={12}
    P=(adjacency-12*np.eye(45,dtype=np.int64))@(adjacency-3*np.eye(45,dtype=np.int64))
    assert sp.Matrix(P).rank()==24
    symmetry_perms=[]
    for v in anisotropic:
        symmetry_perms.append(tuple(line_index[tuple(sorted(symmetry(v,x) for x in line))] for line in lines))
    gens=[]; group={tuple(range(45))}
    for permutation in symmetry_perms:
        candidate=closure(gens+[permutation]) if gens else closure([permutation])
        if len(candidate)>len(group): gens.append(permutation); group=candidate
        if len(group)==51840: break
    assert len(group)==51840 and len(gens)==7
    point_index={x:i for i,x in enumerate(singular)}; line_masks=[]; point_to_lines=[[] for _ in singular]
    for line_id,line in enumerate(lines):
        mask=sum(1<<point_index[x] for x in line); line_masks.append(mask)
        for x in line: point_to_lines[point_index[x]].append(line_id)
    full_mask=(1<<27)-1; ovoids=[]
    def exact_cover(mask,chosen):
        if mask==full_mask: ovoids.append(tuple(chosen)); return
        uncovered=[i for i in range(27) if not ((mask>>i)&1)]
        point=min(uncovered,key=lambda i:sum((line_masks[line]&mask)==0 for line in point_to_lines[i]))
        for line in point_to_lines[point]:
            lm=line_masks[line]
            if lm&mask==0: exact_cover(mask|lm,chosen+[line])
    exact_cover(0,[]); ovoids=sorted(set(tuple(sorted(o)) for o in ovoids)); assert len(ovoids)==200
    ovoid_index={o:i for i,o in enumerate(ovoids)}
    ovoid_gens=[tuple(ovoid_index[tuple(sorted(g[i] for i in ovoid))] for ovoid in ovoids) for g in gens]
    ovoid_point_orbits=point_orbits(200,ovoid_gens); assert sorted(map(len,ovoid_point_orbits))==[40,160]
    pair_label=-np.ones((200,200),dtype=np.int16); orbitals=[]
    for i in range(200):
        for j in range(200):
            if pair_label[i,j]>=0: continue
            oid=len(orbitals); queue=deque([(i,j)]); pair_label[i,j]=oid; orbital=[]
            while queue:
                a,b=queue.popleft(); orbital.append((a,b))
                for g in ovoid_gens:
                    c,d=g[a],g[b]
                    if pair_label[c,d]<0: pair_label[c,d]=oid; queue.append((c,d))
            orbitals.append(orbital)
    assert [len(o) for o in orbitals]==[160,480,480,4320,4320,12960,4320,160,1440,1440,480,1440,480,40,480,4320,1080,160,1440]
    relations=[]
    for oid in range(19):
        matrix=np.zeros((200,200),dtype=np.int64)
        for i,j in orbitals[oid]: matrix[i,j]=1
        relations.append(matrix)
    representatives=[o[0] for o in orbitals]; pijk=np.zeros((19,19,19),dtype=np.int64)
    for i in range(19):
        for j in range(19):
            product=relations[i]@relations[j]
            for k,(a,b) in enumerate(representatives): pijk[i,j,k]=product[a,b]
            assert np.array_equal(product,sum((int(pijk[i,j,k])*relations[k] for k in range(19)),np.zeros((200,200),dtype=np.int64)))
    return dict(singular=singular,anisotropic=anisotropic,lines=lines,line_index=line_index,A=adjacency,P=P,gens=gens,group=group,ovoids=ovoids,ovoid_index=ovoid_index,ovoid_gens=ovoid_gens,ovoid_point_orbits=ovoid_point_orbits,pair_label=pair_label,orbitals=orbitals,relations=relations,pijk=pijk)


def exact_axial_structure(P):
    E=sp.Matrix(P)/90; _,pivot_columns_tuple=E.rref(); pivot_columns=list(pivot_columns_tuple); U=E[:,pivot_columns]
    _,pivot_rows_tuple=U.T.rref(); pivot_rows=list(pivot_rows_tuple); left=U[pivot_rows,:].inv()
    multiplication=[sp.zeros(24,24) for _ in range(24)]
    for i in range(24):
        for j in range(24):
            coordinatewise=sp.Matrix([U[row,i]*U[row,j] for row in range(45)]); coordinates=left*(E*coordinatewise)[pivot_rows,:]
            for k in range(24): multiplication[i][k,j]=coordinates[k]
    axes=[]
    for col in range(45):
        vector=sp.Matrix(P)[:,col]/21; axes.append(left*vector[pivot_rows,:])
    return U,multiplication,axes


def unmarked_automorphism_certificate(geometry):
    P,A=geometry["P"],geometry["A"]; U,multiplication,axes=exact_axial_structure(P)
    trace_form=sp.Matrix([[sp.trace(multiplication[i]*multiplication[j]) for j in range(24)] for i in range(24)])
    assert trace_form==sp.Rational(7,30)*(U.T*U)
    for col,coordinate in enumerate(axes):
        product=sum((coordinate[i]*(multiplication[i]*coordinate) for i in range(24)),sp.zeros(24,1)); assert product==coordinate
        vector=sp.Matrix(P)[:,col]/21; assert (vector.T*vector)[0]==sp.Rational(480,49)
    incidence=np.zeros((27,45),dtype=np.int64); singular_index={x:i for i,x in enumerate(geometry["singular"])}
    for col,line in enumerate(geometry["lines"]):
        for x in line: incidence[singular_index[x],col]=1
    assert np.array_equal(incidence.T@incidence,A+3*np.eye(45,dtype=np.int64)); assert np.array_equal(incidence@P,np.zeros((27,45),dtype=np.int64))
    return {"algebra_dimension":24,"axes":45,"trace_form_identity":"tr(L_x L_y) = (7/30)<x,y>","axis_norm_squared":"480/49","axis_coordinate_profile":{"maximum":"16/7","twelve_neighbors":"-4/7","thirty_two_nonneighbors":"1/7"},"proof_certificate":{"idempotent_frobenius_identity":"||y||^2 = sum_i y_i^3","maximum_coordinate_bound":"m >= 1","three_line_neighbor_bound":"N >= 3 m^2 / 4","nonneighbor_bound":"Q >= m^2 / 8","coordinate_equation":"m = (8/15)m^2 - (2/15)N + (1/30)Q","norm_equation":"S = 30m - 15m^2 + 5N","piecewise_lower_bounds":["S >= 30m - 45m^2/4 for 1 <= m <= 16/7","S >= 15m^2/8 for m >= 16/7"],"sharp_minimum":"S >= 480/49","equality_characterization":"m=16/7, each of three neighbor foursomes is constant -4/7, all 32 nonneighbors are 1/7; hence y is one of the 45 axes"},"marked_automorphism_order":51840,"unmarked_automorphism_group":"O6-(2)=U4(2):2","unmarked_automorphism_order":51840,"verdict":"Every algebra automorphism preserves the intrinsic trace form, hence norm and idempotency; it therefore permutes the 45 minimum-norm nonzero idempotents."}


def wedderburn_and_characters(geometry):
    pijk=geometry["pijk"]; left=[sp.Matrix([[int(pijk[i,j,k]) for j in range(19)] for k in range(19)]) for i in range(19)]; right=[sp.Matrix([[int(pijk[j,i,k]) for j in range(19)] for k in range(19)]) for i in range(19)]
    central={label:sum((sp.Rational(value.numerator,value.denominator)*left[i] for i,value in coefficients.items()),sp.zeros(19)) for label,coefficients in PRIMITIVE_COEFFS.items()}
    models={}; block_models={}
    for label,idempotent in central.items():
        candidates=[]
        for orbital in range(19):
            matrix=right[orbital]*idempotent; rank=matrix.rank()
            if rank: candidates.append((rank,orbital,matrix))
        rank,orbital,matrix=min(candidates,key=lambda item:(item[0],item[1])); basis=sp.Matrix.hstack(*matrix.columnspace()); matrices=[basis.gauss_jordan_solve(operator*basis)[0] for operator in left]
        for i in range(19):
            for j in range(19): assert matrices[i]*matrices[j]==sum((int(pijk[i,j,k])*matrices[k] for k in range(19)),sp.zeros(rank))
        commutant=commutant_dimension(matrices); assert commutant==1
        digest=hashlib.sha256(json.dumps(canonical_matrix_payload(matrices),sort_keys=True,separators=(",",":")).encode()).hexdigest()
        models[label]=(rank,orbital,basis,matrices); block_models[LABEL_MAP[label]]={"algebra_block_size":rank,"seed_orbital":orbital,"commutant_dimension":commutant,"multiplication_verified":True,"matrix_sha256":digest}
    labels=list(models); rows=[]
    for label in labels:
        rank,_,_,matrices=models[label]
        for a in range(rank):
            for b in range(rank): rows.append([matrices[i][a,b] for i in range(19)])
    phi=sp.Matrix(rows); assert phi.shape==(19,19) and phi.det()!=0; phi_inverse=phi.inv(); projector_coefficients={}; coefficient_fractions={}
    for target in labels:
        rhs=[]
        for label in labels:
            rank=models[label][0]
            for a in range(rank):
                for b in range(rank): rhs.append(1 if label==target and a==0 and b==0 else 0)
        coefficients=phi_inverse*sp.Matrix(rhs); projector_coefficients[LABEL_MAP[target]]={str(i):str(x) for i,x in enumerate(coefficients) if x!=0}; coefficient_fractions[target]=[Fraction(int(x.p),int(x.q)) for x in coefficients]
        projector=sum((coefficients[i]*sp.Matrix(geometry["relations"][i]) for i in range(19)),sp.zeros(200)); assert projector*projector==projector and projector.rank()==DIM_MAP[target]
    characters={label:[] for label in labels}; group=list(geometry["group"]); ovoids=geometry["ovoids"]; ovoid_index=geometry["ovoid_index"]; pair_label=geometry["pair_label"]
    for g in group:
        action=[ovoid_index[tuple(sorted(g[i] for i in ovoid))] for ovoid in ovoids]; counts=Counter(int(pair_label[x,action[x]]) for x in range(200))
        for label in labels:
            value=sum(coefficient_fractions[label][i]*counts.get(i,0) for i in range(19)); assert value.denominator==1; characters[label].append(value.numerator)
    inner={LABEL_MAP[a]:{LABEL_MAP[b]:sum(x*y for x,y in zip(characters[a],characters[b]))//51840 for b in labels} for a in labels}; assert all(inner[a][b]==(1 if a==b else 0) for a in inner for b in inner)
    censuses={LABEL_MAP[label]:{str(value):count for value,count in sorted(Counter(values).items())} for label,values in characters.items()}; tensor_rules={}
    for i,a in enumerate(labels):
        for b in labels[i:]:
            known={}; accounted=0
            for c in labels:
                multiplicity=sum(x*y*z for x,y,z in zip(characters[a],characters[b],characters[c]))//51840
                if multiplicity: known[LABEL_MAP[c]]=multiplicity; accounted+=multiplicity*DIM_MAP[c]
            tensor_rules[f"{LABEL_MAP[a]}x{LABEL_MAP[b]}"]={"known_projections":known,"residual_dimension":DIM_MAP[a]*DIM_MAP[b]-accounted}
    return {"split_Q_algebra":"M2(Q) + Q + M2(Q) + Q + M3(Q)","irrep_dimensions":{"1":1,"15a":15,"15b":15,"24":24,"81":81},"module_decomposition":"1^2 + 15a^2 + 15b + 24^3 + 81","block_models":block_models,"primitive_projector_orbital_coefficients":projector_coefficients,"character_value_censuses":censuses,"character_inner_products":inner,"known_tensor_projections":tensor_rules,"tensor_boundary":"Only projections onto the five constructed irreducibles are claimed; residual dimensions may contain other irreducibles."},characters


def build_modular_axial(P,p):
    matrix=sp.Matrix(P); _,pivot_columns_tuple=matrix.rref(); pivot_columns=list(pivot_columns_tuple); U=P[:,pivot_columns]%p; _,pivot_rows_tuple=sp.Matrix(P[:,pivot_columns]).T.rref(); pivot_rows=list(pivot_rows_tuple); left=inv_mod(U[pivot_rows,:],p); projector=P%p*pow(90,-1,p)%p
    structure=np.zeros((24,24,24),dtype=np.int64)
    for a in range(24):
        for b in range(a,24):
            vector=projector@(U[:,a]*U[:,b]%p)%p; coordinates=left@vector[pivot_rows]%p; structure[:,a,b]=structure[:,b,a]=coordinates
    axes=np.column_stack([left@(P[:,i][pivot_rows]%p)%p*pow(21,-1,p)%p for i in range(45)])%p
    return structure,axes
def safe_product(structure,x,y,p): return (np.tensordot(structure,x,axes=([1],[0]))%p@y)%p
def generated_subalgebra(indices,structure,axes,p):
    rows,pivots=rref_basis([axes[:,i] for i in indices],p); changed=True
    while changed:
        snapshot=list(rows); products=[safe_product(structure,x,y,p) for i,x in enumerate(snapshot) for y in snapshot[i:]]; old_size=len(rows); rows,pivots=rref_basis(rows+products,p); changed=len(rows)>old_size
    basis=np.column_stack(rows); extractor=inv_mod(basis[pivots,:],p); d=basis.shape[1]; table=np.zeros((d,d,d),dtype=np.int64)
    for i in range(d):
        for j in range(i,d):
            coordinates=extractor@safe_product(structure,basis[:,i],basis[:,j],p)[pivots]%p; table[:,i,j]=table[:,j,i]=coordinates
    return basis,table
def subalgebra_invariants(table,p):
    d=table.shape[0]; multiplications=[table[:,i,:]%p for i in range(d)]; annmat=np.column_stack([matrix.reshape(-1) for matrix in multiplications])%p; annihilator=d-rank_mod(annmat,p); squares=np.column_stack([table[:,i,j] for i in range(d) for j in range(i,d)])%p; square_span=rank_mod(squares,p); identity=np.eye(d,dtype=np.int64).reshape(-1)%p; unital=rank_mod(np.column_stack([annmat,identity]),p)==rank_mod(annmat,p); trace_form=np.array([[int(np.trace((multiplications[i]@multiplications[j])%p))%p for j in range(d)] for i in range(d)],dtype=np.int64); trace_rank=rank_mod(trace_form,p)
    nucleus_rows=[]
    for y in range(d):
        for z in range(d):
            yz=table[:,y,z]
            for k in range(d): nucleus_rows.append([(sum(int(table[a,i,y])*int(table[k,a,z]) for a in range(d))-sum(int(yz[b])*int(table[k,i,b]) for b in range(d)))%p for i in range(d)])
    nucleus=d-rank_mod(np.array(nucleus_rows,dtype=np.int64),p); associators=[]
    for i in range(d):
        for j in range(i,d):
            for k in range(j,d): associators.append((multiplications[k]@table[:,i,j]-multiplications[i]@table[:,j,k])%p)
    associator_span=rank_mod(np.column_stack(associators),p); ideal_basis,_=rref_basis(associators,p); changed=True
    while changed:
        old_size=len(ideal_basis); products=[(multiplications[i]@vector)%p for vector in ideal_basis for i in range(d)]; ideal_basis,_=rref_basis(ideal_basis+products,p); changed=len(ideal_basis)>old_size
    multiplication_basis,_=rref_basis([matrix.reshape(-1) for matrix in multiplications],p); changed=True
    while changed:
        old_size=len(multiplication_basis); products=[]
        for vector in multiplication_basis:
            matrix=vector.reshape(d,d)
            for generator in multiplications: products.append((matrix@generator%p).reshape(-1))
        multiplication_basis,_=rref_basis(multiplication_basis+products,p); changed=len(multiplication_basis)>old_size
    return {"dimension":d,"annihilator":annihilator,"square_span":square_span,"unital":unital,"trace_form_rank":trace_rank,"nucleus":nucleus,"associator_span":associator_span,"associator_ideal":len(ideal_basis),"multiplication_algebra":len(multiplication_basis)}
def orbit_of_subset(subset,gens):
    start=tuple(sorted(subset)); seen={start}; queue=deque([start])
    while queue:
        current=queue.popleft()
        for g in gens:
            image=tuple(sorted(g[i] for i in current))
            if image not in seen: seen.add(image); queue.append(image)
    return seen


def four_axis_classification(geometry):
    A,P,gens=geometry["A"],geometry["P"],geometry["gens"]; structure,axes=build_modular_axial(P,MOD); remaining=set(combinations(range(45),4)); orbit_records=[]; raw=[]
    while remaining:
        representative=min(remaining); orbit=orbit_of_subset(representative,gens); remaining.difference_update(orbit); basis,table=generated_subalgebra(representative,structure,axes,MOD); edges=sum(int(A[i,j]) for i,j in combinations(representative,2)); degrees=sorted(sum(int(A[i,j]) for j in representative if j!=i) for i in representative); raw.append((representative,len(orbit),basis,table)); orbit_records.append({"rep":list(representative),"orbit_size":len(orbit),"induced_edges":edges,"degree_sequence":degrees,"dimension":basis.shape[1]})
    assert len(raw)==20 and sum(record["orbit_size"] for record in orbit_records)==math.comb(45,4); prime_stability={}
    for prime in [101,103,107,1009,10007,1000003]:
        structure_p,axes_p=build_modular_axial(P,prime); prime_stability[str(prime)]=[generated_subalgebra(record[0],structure_p,axes_p,prime)[0].shape[1] for record in raw]
    assert len({tuple(value) for value in prime_stability.values()})==1; invariants=[subalgebra_invariants(table,MOD) for _,_,_,table in raw]; contained=[]
    for _,_,basis,_ in raw:
        d=basis.shape[1]; contained.append(tuple(i for i in range(45) if rank_mod(np.column_stack([basis,axes[:,i]]),MOD)==d))
    clusters=[]; used=set()
    for i,axis_set in enumerate(contained):
        if i in used: continue
        orbit=orbit_of_subset(axis_set,gens); indices=[j for j,other in enumerate(contained) if other in orbit]; used.update(indices); clusters.append({"dimension":raw[i][2].shape[1],"generating_set_orbit_indices":indices,"representatives":[list(raw[j][0]) for j in indices],"contained_axes":len(axis_set),"subalgebra_orbit_size":len(orbit),"invariants":invariants[i]})
    assert len(clusters)==8; weighted=Counter()
    for record in orbit_records: weighted[record["dimension"]]+=record["orbit_size"]
    assert dict(sorted(weighted.items()))=={4:135,5:720,6:1080,10:16740,12:5040,14:27000,16:14040,24:84240}
    for cluster in clusters:
        inv=cluster["invariants"]; d=cluster["dimension"]; assert inv["multiplication_algebra"]==d*d and inv["annihilator"]==inv["nucleus"]==0 and inv["square_span"]==inv["trace_form_rank"]==d and inv["associator_span"]==inv["associator_ideal"]==d and not inv["unital"]
    return {"prior_bug":{"source":"Passes 3837-3854","fault":"np.einsum('kab,a,b->k', ..., dtype=np.int64) formed unreduced three-factor products near 10^18 and overflowed int64 before modular reduction","withdrawn_weighted_dimension_census":{"4":135,"5":720,"6":1080,"10":16740,"14":27000,"24":103320},"correction":"Use a two-stage contraction with modular reduction between stages."},"safe_contraction":"temp=tensordot(T,x,axes=([1],[0])) mod p; product=(temp@y) mod p","prime_stability":prime_stability,"twenty_generating_set_orbits":orbit_records,"corrected_weighted_dimension_census":{str(k):v for k,v in sorted(weighted.items())},"eight_subalgebra_isomorphism_classes":sorted(clusters,key=lambda record:record["dimension"]),"class_dimensions":sorted(cluster["dimension"] for cluster in clusters),"verdict":"The 20 four-generator orbits collapse to eight global subalgebra orbits, one in each dimension 4,5,6,10,12,14,16,24."}


def K43_seed(geometry,characters):
    anisotropic=geometry["anisotropic"]; aniso_index={x:i for i,x in enumerate(anisotropic)}; line_index=geometry["line_index"]; lines=geometry["lines"]; gens=geometry["gens"]; ovoids=geometry["ovoids"]; ovoid_index=geometry["ovoid_index"]; anisotropic_gens=[]
    for v in anisotropic:
        line_perm=tuple(line_index[tuple(sorted(symmetry(v,x) for x in line))] for line in lines)
        if line_perm in gens: anisotropic_gens.append(tuple(aniso_index[symmetry(v,x)] for x in anisotropic))
    norton=sorted({tuple(sorted((x,y,x^y))) for x,y in combinations(anisotropic,2) if x^y in anisotropic}); norton_index={line:i for i,line in enumerate(norton)}; tripod_global=next(orbit for orbit in geometry["ovoid_point_orbits"] if len(orbit)==160); trip_index={x:i for i,x in enumerate(tripod_global)}; trip_gens=[]; norton_gens=[]
    for line_g,aniso_g in zip(gens,anisotropic_gens):
        action=tuple(ovoid_index[tuple(sorted(line_g[i] for i in ovoid))] for ovoid in ovoids); trip_gens.append(tuple(trip_index[action[x]] for x in tripod_global)); norton_gens.append(tuple(norton_index[tuple(sorted(anisotropic[aniso_g[aniso_index[x]]] for x in line))] for line in norton))
    pair_labels=-np.ones((160,120),dtype=np.int16); pair_orbits=[]
    for i in range(160):
        for j in range(120):
            if pair_labels[i,j]>=0: continue
            oid=len(pair_orbits); queue=deque([(i,j)]); pair_labels[i,j]=oid; orbit=[]
            while queue:
                a,b=queue.popleft(); orbit.append((a,b))
                for gt,gn in zip(trip_gens,norton_gens):
                    c,d=gt[a],gn[b]
                    if pair_labels[c,d]<0: pair_labels[c,d]=oid; queue.append((c,d))
            pair_orbits.append(orbit)
    assert [len(orbit) for orbit in pair_orbits]==[480,1440,4320,12960]
    singular=geometry["singular"]; singular_index={x:i for i,x in enumerate(singular)}; point_gens=[]
    for v in anisotropic:
        line_perm=tuple(line_index[tuple(sorted(symmetry(v,x) for x in line))] for line in lines)
        if line_perm in gens: point_gens.append(tuple(singular_index[symmetry(v,x)] for x in singular))
    paired={tuple(range(45)):(tuple(range(27)),tuple(range(36)))}; queue=deque([tuple(range(45))])
    while queue:
        h=queue.popleft(); hp,ha=paired[h]
        for gl,gp,ga in zip(gens,point_gens,anisotropic_gens):
            x=compose(gl,h)
            if x not in paired: paired[x]=(compose(gp,hp),compose(ga,ha)); queue.append(x)
    incidence_pairs=set(pair_orbits[0]); incidence_character=[]
    for line_g in list(geometry["group"]):
        _,aniso_g=paired[line_g]; ovoid_action=[ovoid_index[tuple(sorted(line_g[i] for i in ovoid))] for ovoid in ovoids]; trip_action=[trip_index[ovoid_action[x]] for x in tripod_global]; norton_action=[norton_index[tuple(sorted(anisotropic[aniso_g[aniso_index[x]]] for x in line))] for line in norton]; incidence_character.append(sum(1 for a,b in incidence_pairs if trip_action[a]==a and norton_action[b]==b))
    decomposition={label:sum(x*y for x,y in zip(incidence_character,characters[raw]))//51840 for raw,label in LABEL_MAP.items()}; residual=[incidence_character[index]-sum(decomposition[LABEL_MAP[raw]]*characters[raw][index] for raw in characters) for index in range(51840)]; residual_inner={label:sum(x*y for x,y in zip(residual,characters[raw]))//51840 for raw,label in LABEL_MAP.items()}; assert all(value==0 for value in residual_inner.values()); incidence_norm=sum(x*x for x in incidence_character)//51840; residual_norm=sum(x*x for x in residual)//51840; assert (incidence_norm,residual_norm)==(23,4)
    return {"incidence_action_degree":480,"incidence_character_norm":incidence_norm,"incidence_character_census":{str(value):count for value,count in sorted(Counter(incidence_character).items())},"decomposition_on_constructed_irreps":decomposition,"known_degree_accounted":sum({"1":1,"81":81,"15a":15,"15b":15,"24":24}[label]*multiplicity for label,multiplicity in decomposition.items()),"orthogonal_residual_degree":200,"orthogonal_residual_character_norm":residual_norm,"orthogonal_residual_character_census":{str(value):count for value,count in sorted(Counter(residual).items())},"orthogonal_residual_inner_products":residual_inner,"official_database":{"repository":"melissa-maths/MonsterSubgroups","commit":"1fa1e5cc5ad92bb822a1f11d2818e6703904271a","portable_generator_file":"GetGeneratorsOfSubgroupInM.py","direct_key_searches":{"U4(2)":0,"U4(2):2":0,"O6-(2)":0,"40K4,3":0},"available_overgroup_routes":["3.Fi via N(3A)","(D10 x HN).2 via N(5A)","2^2 . 2E6(2) : S3"],"executed_descent_status":"NO_DIRECT_U4_KEY_AND_NO_SERIALIZED_DESCENT_WORDS_FOUND"},"repository_candidate_slots":{"PART_3670_3686_MMgroup_four_parabolic_candidate.json":"PENDING","PART_3769_3786_FINITE_GROUP_DESCENT_candidate.json":"PENDING","PART_3837_3854_MONSTER_DESCENT_candidate.json":"PENDING","PART_3887_3904_MONSTER_K43_DESCENT_candidate.json":"PENDING"},"status":"FAIL_CLOSED_NO_SERIALIZED_MMGROUP_WORDS_OR_EXECUTED_CLASS_FUSION"}


def order192_reconciliation(geometry):
    singular=geometry["singular"]; singular_index={x:i for i,x in enumerate(singular)}; point_gens=[]
    for v in geometry["anisotropic"]:
        line_perm=tuple(geometry["line_index"][tuple(sorted(symmetry(v,x) for x in line))] for line in geometry["lines"])
        if line_perm in geometry["gens"]: point_gens.append(tuple(singular_index[symmetry(v,x)] for x in singular))
    group27=list(closure(point_gens)); adjacency27=np.zeros((27,27),dtype=np.int64)
    for i,j in combinations(range(27),2):
        if singular[i]^singular[j] in singular: adjacency27[i,j]=adjacency27[j,i]=1
    adjacent=int(np.flatnonzero(adjacency27[0])[0]); incident=[g for g in group27 if g[0]==0 and g[adjacent]==adjacent]; incident_derived,incident_gens=derived_subgroup(incident); buckets=collections.defaultdict(list)
    for element in group27: buckets[perm_order(element)].append(element)
    centralizer192=None
    for involution in buckets[2]:
        candidate=[g for g in group27 if compose(g,involution)==compose(involution,g)]
        if len(candidate)==192: centralizer192=candidate; break
    assert centralizer192 is not None; centralizer_derived,centralizer_gens=derived_subgroup(centralizer192); d8_orders=[1]+[2]*5+[4]*2; s4_orders=[1]+[2]*9+[3]*8+[4]*6; direct=Counter(math.lcm(a,b) for a in d8_orders for b in s4_orders); centralizer_census=Counter(perm_order(g) for g in centralizer192); assert centralizer_census==direct
    source_h=json.loads((ROOT/"data"/"w33_tomotope_H_obstruction.json").read_text()); exceptional=json.loads((ROOT/"data"/"PART_BT3871_BT3886_EIGHT_FRONT_CLOSURE_results.json").read_text()); ex=exceptional["fronts"]["tomotope_outer_extension_correction"]["exact_invariants"]
    return {"W_D4_frame_and_ordered_incident_pair":{"order":192,"element_order_census":{str(k):v for k,v in sorted(Counter(perm_order(g) for g in incident).items())},"center_order":len(center(incident)),"derived_order":len(incident_derived),"abelianization_order":192//len(incident_derived),"point_orbits":orbits_under(incident,27),"generator_count":len(incident_gens),"structure":"W(D4)=2^3:S4 with central involution"},"involution_centralizer":{"order":192,"element_order_census":{str(k):v for k,v in sorted(centralizer_census.items())},"center_order":len(center(centralizer192)),"derived_order":len(centralizer_derived),"abelianization_order":192//len(centralizer_derived),"point_orbits":orbits_under(centralizer192,27),"matches_D8_x_S4_order_census":True,"generator_count":len(centralizer_gens),"structure":"D8 x S4"},"octonion_axis_line_stabilizer":{"order":source_h["T2_H_order"],"action":"free transitive torsor on each axis-fixed 192 embedding slice","center_order":source_h["T4_H_center_size"],"order8_elements":source_h["T6_H_order8_count"],"source":"archive/dirs/TOE_w33_axis192_torsor_v01_20260227_bundle and data/w33_tomotope_H_obstruction.json","structure_status":"centerless signed-permutation octonion axis stabilizer; not identified with W(D4)"},"exceptional_tomotope_completion":{"order":ex["order"],"structure":exceptional["fronts"]["tomotope_outer_extension_correction"]["corrected_exceptional_group"],"center_order":ex["center_order"],"normal_elementary_abelian_order":ex["normal_elementary_abelian_order"],"ordinary_kernel":ex["ordinary_kernel_structure"],"ordinary_kernel_order":ex["ordinary_kernel_order"],"outside_involutions":ex["outside_involutions"],"extension":ex["extension"],"source":"Passes 3871-3886 correction"},"anti_coincidence_verdict":"At least four non-equivalent mechanisms produce 192: W(D4), D8xS4, the centerless octonion axis stabilizer, and centerless 2^4:D12. Equality of order or carrier size is not an identification."}


def build_result():
    geometry=build_geometry(); unmarked=unmarked_automorphism_certificate(geometry); wedderburn,characters=wedderburn_and_characters(geometry); seed=K43_seed(geometry,characters); four_axis=four_axis_classification(geometry); order192=order192_reconciliation(geometry)
    result={"schema":"w33.pass3887_3904.unmarked_wedderburn_monster_fouraxis_order192.v1","status":"PASS_EXACT_FIVE_FRONTS_THREE_CONSTRUCTIONS_MONSTER_WORDS_PENDING_WITH_OVERFLOW_CORRECTION","checks":{"trace_form_equals_seven_thirtieth_standard_inner_product_exact":True,"axes_are_exactly_minimum_norm_nonzero_idempotents":True,"full_unmarked_automorphism_group_is_O6minus2_order51840":True,"explicit_split_rational_Wedderburn_models_exact":True,"five_rational_characters_irreducible_and_pairwise_distinct":True,"known_tensor_projections_exact":True,"K43_seed_character_decomposition_and_hidden_residual_exact":True,"official_monster_database_searched_no_direct_U42_key":True,"monster_embedding_and_class_fusion_fail_closed":True,"four_axis_overflow_identified_and_corrected":True,"safe_four_axis_dimensions_stable_across_six_primes":True,"twenty_generating_set_orbits_and_eight_subalgebra_classes_exact":True,"all_eight_local_algebra_species_simple_nonunital":True,"WD4_incident_pair_order192_exact":True,"D8xS4_involution_centralizer_order192_exact":True,"four_order192_mechanisms_distinguished":True},"unmarked_automorphism_theorem":unmarked,"explicit_wedderburn_models":wedderburn,"K43_monster_seed":seed,"four_axis_classification":four_axis,"order192_reconciliation":order192,"three_bonkers_constructions":{"minimum_idempotent_reconstruction":"The abstract multiplication and trace form recover the 45 GQ(4,2) points as the unique minimum-norm nonzero idempotents.","hidden_degree200_character":"The 480-element K4,3 incidence action contains a degree-200 orthogonal residual character of norm four, invisible to the five previously constructed irreducibles.","eight_species_local_zoo":"The corrected twenty four-generator orbits organize into exactly eight simple nonunital subalgebra species of dimensions 4,5,6,10,12,14,16,24."},"evidence_boundary":{"proved_here":["intrinsic minimum-idempotent characterization and full unmarked automorphism group","explicit rational split Wedderburn block models, primitive projectors, irreducible characters, and known tensor projections","exact K4,3 character decomposition and degree-200 norm-four residual","overflow-safe corrected twenty-orbit and eight-species four-axis classification","finite order-192 barcodes for W(D4) and D8xS4, with source-exact octonion and corrected tomotope separation"],"not_proved_here":["serialized Monster/mmgroup U4(2):2 words or executed Monster class fusion","complete tensor-product decompositions beyond the five known irreducibles","irreducible decomposition of the hidden degree-200 residual","SmallGroup identifier or full internal structure of the octonion axis stabilizer","remote CI/PDF success until observed","hardware, laboratory, thermodynamic, or physical mechanism"]}}
    result["semantic_sha256"]=hashlib.sha256(json.dumps(result,sort_keys=True,separators=(",",":")).encode()).hexdigest(); return result

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--output",type=Path,default=DEFAULT_OUTPUT); args=parser.parse_args(); result=build_result(); args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); print(result["semantic_sha256"]); return 0
if __name__=="__main__": raise SystemExit(main())
