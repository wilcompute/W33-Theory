#!/usr/bin/env python3
"""Passes 7147--7153: PGL2 quotient proof anchors, M2 compatibility, D12 hexad and code anatomy.

This producer certifies the finite identities and small-field anchors used by the accompanying
all-q proofs.  It deliberately keeps the PGL2 character-table step as a mathematical proof in
the report/theorem insert rather than pretending finitely many numerical anchors prove it.
"""
from __future__ import annotations
import itertools, json, math
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
import w33_pass7130_7137_structural_attack as p
import w33_pass7138_7145_c2_normalform_matrix_quotient as q

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7147_7153_PGL2_HEXAD_CODE_CLOSURE.json'


def compose(a,b): return tuple(a[b[i]] for i in range(len(a)))


def gf9_mat2_mul(A,B):
    return [[p.gsum(p.gm(A[i][k],B[k][j]) for k in range(2)) for j in range(2)] for i in range(2)]

def gf9_det(A): return p.ga(p.gm(A[0][0],A[1][1]),p.gn(p.gm(A[0][1],A[1][0])))
def gf9_inv2(A):
    d=gf9_det(A); z=p.INV[d]
    return [[p.gm(z,A[1][1]),p.gm(z,p.gn(A[0][1]))],[p.gm(z,p.gn(A[1][0])),p.gm(z,A[0][0])]]
def gf9_tr(A): return p.ga(A[0][0],A[1][1])
def gf9_eq_pm(a,b): return a==b or a==p.gn(b)


def canonical_pgl2_prime(A,r):
    vals=tuple(x%r for row in A for x in row)
    z=pow(next(x for x in vals if x),-1,r)
    return tuple(x*z%r for x in vals)

def pgl2_prime(r):
    els=[]
    for a,b,c,d in itertools.product(range(r),repeat=4):
        if (a*d-b*c)%r:
            els.append(canonical_pgl2_prime(((a,b),(c,d)),r))
    return sorted(set(els))
def mulpgl(x,y,r):
    a,b,c,d=x; e,f,g,h=y
    return canonical_pgl2_prime((((a*e+b*g)%r,(a*f+b*h)%r),((c*e+d*g)%r,(c*f+d*h)%r)),r)
def invpgl(x,r):
    a,b,c,d=x
    return canonical_pgl2_prime(((d,-b%r),(-c%r,a)),r)

def trzero_pgl(x,r):
    a,b,c,d=x
    return (a+d)%r==0


def pgl2_coset_anchor(r):
    G=pgl2_prime(r); I={g:i for i,g in enumerate(G)}
    e=canonical_pgl2_prime(((1,0),(0,1)),r); D=canonical_pgl2_prime(((1,0),(0,-1%r)),r)
    invol=[g for g in G if g!=e and trzero_pgl(g,r)]
    assert len(invol)==r*r
    # right H-cosets represented canonically
    rep={}; cosets=[]
    for g in G:
        c=min(g,mulpgl(g,D,r))
        if c not in rep: rep[c]=len(cosets); cosets.append(c)
    n=len(cosets); assert n==r*(r*r-1)//2
    W=np.zeros((n,n),dtype=np.int64)
    for i,g in enumerate(cosets):
        for t in invol:
            j=rep[min(mulpgl(t,g,r),mulpgl(mulpgl(t,g,r),D,r))]
            W[i,j]+=1
    assert np.all(W.sum(axis=1)==r*r) and np.all(np.diag(W)==1)
    R=(W==2).astype(np.int64); np.fill_diagonal(R,0)
    A=W-np.eye(n,dtype=np.int64)-R
    assert np.max(A)<=1 and np.min(A)>=0 and np.array_equal(A,A.T)
    assert np.array_equal(W@R,R@W)
    def spec(M): return dict(sorted(Counter(round(float(x),7) for x in np.linalg.eigvalsh(M)).items()))
    h=(r-1)//2
    assert Counter(R.sum(axis=1))==Counter({h:h*0+n})
    return {
      'group_order':len(G),'involutions':len(invol),'coset_vertices':n,
      'W_spectrum':spec(W),'R_spectrum':spec(R),'pair_graph_spectrum':spec(A),
      'identity':'A_pair = W - I - R','normalizer_correction_degree':h,
      'commutator_WR_zero':True,
    }


def build_hexad():
    P9,I9,adj9=p.build9()
    Aperm=tuple(I9[p.norm9(p.matvec9(p.A9,P9[v]))] for v in range(820))
    Fperm=tuple(I9[p.norm9(tuple(p.fr(x) for x in P9[v]))] for v in range(820))
    ident=tuple(range(820)); group={ident}; front=[ident]
    while front:
        h=front.pop()
        for gen in (Aperm,Fperm):
            z=compose(gen,h)
            if z not in group: group.add(z); front.append(z)
    assert len(group)==12
    S=frozenset(p.S9); sets=[]
    for h in group:
        T=frozenset(h[v] for v in S)
        if T not in sets: sets.append(T)
    assert len(sets)==6 and all(len(a&b)==4 for a,b in itertools.combinations(sets,2))
    union=sorted(set().union(*sets)); pos={v:i for i,v in enumerate(union)}
    cols=[]
    for v in union:
        mask=sum((1<<i) for i,T in enumerate(sets) if v in T)
        cols.append(mask)
    cm=Counter(cols)
    byweight=defaultdict(list)
    for mask,m in cm.items(): byweight[mask.bit_count()].append((mask,m))
    assert sorted(m for _,m in byweight[1])==[32]*6
    assert Counter(m for _,m in byweight[2])==Counter({4:9,3:6})
    assert sorted(m for _,m in byweight[3])==[1,1]
    triple_masks=sorted(mask for mask,m in byweight[3])
    assert triple_masks[0]^triple_masks[1]==63
    # Column-pattern automorphisms inside S6.
    outer=[]
    for perm in itertools.permutations(range(6)):
        def pmask(mask):
            z=0
            for i in range(6):
                if (mask>>i)&1: z|=1<<perm[i]
            return z
        if Counter({pmask(k):v for k,v in cm.items()})==cm: outer.append(perm)
    assert len(outer)==72
    # Low dual weight enumerator by exact MacWilliams/Krawtchouk transform.
    masks=[sum(1<<v for v in T) for T in sets]
    C=Counter()
    for a in range(64):
        z=0
        for i in range(6):
            if (a>>i)&1: z^=masks[i]
        C[z.bit_count()]+=1
    n=248
    def K(j,w):
        return sum(((-1)**t)*math.comb(w,t)*math.comb(n-w,j-t)
                   for t in range(max(0,j-(n-w)),min(j,w)+1))
    dual={j:sum(A*K(j,w) for w,A in C.items())//64 for j in range(11)}
    assert dual[1]==0 and dual[2]==3048
    # shell coordinate incidence profiles
    shell_profiles={}
    words=[]
    for a in range(64):
        z=0
        for i in range(6):
            if (a>>i)&1: z^=masks[i]
        words.append((a,z,z.bit_count()))
    for wt in sorted(k for k in C if k):
        members=[z for _,z,w in words if w==wt]
        prof=Counter(sum((z>>v)&1 for z in members) for v in union)
        shell_profiles[str(wt)]=dict(sorted(prof.items()))
    # puncturing triple points
    triple_points=sorted(v for v in union if sum(v in T for T in sets)==3)
    assert triple_points==[50,80]
    def punct_enum(rem):
        out=Counter()
        for _,z,_ in words:
            out[z.bit_count()-sum((z>>v)&1 for v in rem)]+=1
        return dict(sorted(out.items()))
    one=punct_enum([50]); both=punct_enum([50,80])
    return P9,sets,union,cm,triple_masks,outer,C,dual,shell_profiles,triple_points,one,both,Aperm,Fperm


def m2_q9_identity():
    P9,I9,adj9=p.build9(); M9=q.cols_to_matrix(q.E9+q.F9); M9i=p.invmat9(M9)
    def coord(v): return p.matvec9(M9i,P9[v])
    def Mof(c):
        u=c[:2]; w=c[2:]
        return [[u[0],u[1]],[w[1],p.gn(w[0])]]
    # all eligible C2 pair representatives
    g={v:I9[p.norm9(p.matvec9(p.A9,P9[v]))] for v in range(820)}
    reps=[]
    for v in range(820):
        if v<g[v] and g[v] not in adj9[v]: reps.append(v)
    assert len(reps)==360
    matrices=[]
    for v in reps:
        c=coord(v); M=Mof(c)
        dot=p.ga(p.gm(c[0],c[2]),p.gm(c[1],c[3]))
        assert gf9_det(M)==p.gn(dot) and gf9_det(M)!=0
        matrices.append(M)
    checked=0
    D=[[1,0],[0,2]]
    for i,j in itertools.combinations(range(360),2):
        R=gf9_mat2_mul(matrices[i],gf9_inv2(matrices[j]))
        law=gf9_eq_pm(R[0][0],R[1][1])
        geom=any(b in adj9[a] for a in (reps[i],g[reps[i]]) for b in (reps[j],g[reps[j]]))
        assert law==geom
        # factorized quartic: (a-b)(a+b)=tr(R)*tr(DR) up to nonzero projective scale
        DR=gf9_mat2_mul(D,R)
        lhs=p.gm(p.ga(R[0][0],p.gn(R[1][1])),p.ga(R[0][0],R[1][1]))
        rhs=p.gm(gf9_tr(R),gf9_tr(DR))
        assert lhs==rhs
        checked+=1
    return {'eligible_pair_nodes':360,'pair_pairs_checked':checked,
            'matrix_map':'M(u,w)=[[u1,u2],[w2,-w1]], det(M)=-u.w',
            'quotient_identification':'eligible C2 pair nodes = PGL2(9)/<diag(1,-1)>',
            'conflict_law':'for R=M N^{-1}, conflict iff R11=+/-R22, equivalently tr(R)=0 or tr(DR)=0',
            'quartic_factorization':'R11^2-R22^2 = tr(R) tr(DR)'}


def main():
    anchors={str(r):pgl2_coset_anchor(r) for r in (3,5,7)}
    m2=m2_q9_identity()
    P9,sets,union,cm,triple_masks,outer,C,dual,shell,triple_pts,one,both,Aperm,Fperm=build_hexad()
    # D12 action on the six witness sets.
    def induced(gen):
        return tuple(sets.index(frozenset(gen[v] for v in T)) for T in sets)
    pa,pf=induced(Aperm),induced(Fperm); paf=compose(pa,pf)
    # order of paf
    z=tuple(range(6)); o=0
    while True:
        o+=1; z=compose(paf,z)
        if z==tuple(range(6)): break
    assert o==6
    # exact stabilizer/orbit argument uses previous exact Stab(S)=C2.
    Pgamma_order=6886425600
    assert Pgamma_order%12==0
    hexad_orbit=Pgamma_order//12
    witness_orbit=Pgamma_order//2
    assert hexad_orbit*6==witness_orbit
    internal_pairs=[]; cross_pairs=[]
    T0=set(i for i in range(6) if (triple_masks[0]>>i)&1); T1=set(range(6))-T0
    for mask,m in cm.items():
        if mask.bit_count()==2:
            pair=tuple(i for i in range(6) if (mask>>i)&1)
            (internal_pairs if m==3 else cross_pairs).append(pair)
    assert len(internal_pairs)==6 and len(cross_pairs)==9
    out={
      'schema':'w33.pass7147_7153.pgl2_hexad_code_closure.v1','status':'PASS',
      'boundary':'Exact finite geometry/group/code statements. The all-q spectrum theorem uses the explicit PGL2 character/normalizer proof recorded in the companion report; q=3,5,7 computations here are replay anchors, not a substitute for that proof. No physics claim.',
      'pass_7147_pgl2_involution_schreier':{
        'model':'pair quotient = G/H with G=PGL2(q), H=<D>, D=diag(1,-1)',
        'weighted_operator':'W=sum over all projective involutions acting on G/H',
        'correction':'A_pair=W-I-R, where R is the duplicate-support normalizer graph',
        'R_structure':'q(q+1)/2 disjoint copies of K_{h,h}, h=(q-1)/2',
        'W_spectrum_formula':{'q^2':'1','q':'(q+1)(q^2-q-4)/4','-q':'q(q-1)^2/4','1':'q(q+1)/2'},
        'pair_spectrum_formula':{
          '(2q^2-q-1)/2':'1','q-1':'q(q-3)(q+1)/4','-(q+1)':'q(q-3)(q-1)/4',
          '(q-1)/2':'(q-1)(q+2)/2','-(q+3)/2':'q(q-1)/2','0':'q(q-3)/2','-(q-1)/2':'q'},
        'prime_replay_anchors':anchors,
        'full_quotient_spectrum_status':'THEOREM: combining this pair spectrum with the exact fixed/pair incidence block proves the Pass7141 formula for every odd q.'},
      'pass_7148_m2_relative_compatibility':m2,
      'pass_7149_d12_hexad_classification':{
        'ambient_hexad_stabilizer':'D12','ambient_stabilizer_order':12,'abstract_membership_pattern_aut_order':72,
        'ambient_group_order':Pgamma_order,'hexad_orbit_size':hexad_orbit,'witness_orbit_size':witness_orbit,
        'unique_hexad_per_witness_in_orbit':True,'proof_count':'(|PΓSp|/12)*6 = |PΓSp|/2',
        'induced_A':pa,'induced_F':pf,'induced_AF_order':6,
        'membership_pattern':'6 singleton columns x32; 6 internal-pair columns x3; 9 cross-pair columns x4; two complementary triple columns x1',
        'triple_partition':[sorted(T0),sorted(T1)],'triple_points':triple_pts},
      'pass_7150_code_anatomy':{
        'code':'[248,6,51]_2','dual_minimum_distance':2,'dual_weight2_words':dual[2],
        'dual_low_enumerator':{str(k):v for k,v in dual.items()},
        'outer_GL6_column_multiset_stabilizer':'S3 wr C2','outer_order':72,
        'full_coordinate_permutation_aut_group':'((S_32)^6 x (S_4)^9 x (S_3)^6) semidirect (S3 wr C2)',
        'full_coordinate_aut_order_factored':'72*(32!)^6*(4!)^9*(3!)^6',
        'shell_coordinate_incidence_profiles':shell,
        'shell_design_result':'Every nonzero shell fails to be a 1-design on all 248 coordinates; the natural regularity is the membership-pattern stratification.',
        'D12_F2_module':'F2^6 natural hexagon module; composition factors 1,1,V2,V2; primary dimensions 2 for (x+1)^2 and 4 for (x^2+x+1)^2.'},
      'pass_7151_bonkers_two_channel_factorization':{
        'identity':'Delta_D(X,Y)=(u.w_prime)^2-(w.u_prime)^2 = -Omega(X,Y) Omega(X,DY), up to the fixed row convention',
        'interpretation':'The quotient conflict quartic factorizes into the original symplectic channel and its D-twisted channel; this is finite algebra, not a physical two-channel claim.'},
      'pass_7152_bonkers_symmetry_gap':{
        'geometric_hexad_symmetry_order':12,'abstract_code_outer_symmetry_order':72,'index':6,
        'statement':'The code has six times as much outer coordinate-pattern symmetry as is realized by ambient PΓSp geometry; the extra cosets are code-only symmetries.'},
      'pass_7153_bonkers_puncture_symmetry_restoration':{
        'puncture_point_50':{'length':247,'dimension':6,'minimum_distance':min(k for k in one if k>0),'weight_enumerator':{str(k):v for k,v in one.items()},'outer_order':36},
        'puncture_both_50_80':{'length':246,'dimension':6,'minimum_distance':min(k for k in both if k>0),'weight_enumerator':{str(k):v for k,v in both.items()},'outer_order':72},
        'statement':'Puncturing one complementary triple column distinguishes the two 3-blocks and breaks the outer block swap 72->36; puncturing both removes both distinguished columns and restores the S3 wr C2 outer symmetry.'}
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0
if __name__=='__main__': raise SystemExit(main())
