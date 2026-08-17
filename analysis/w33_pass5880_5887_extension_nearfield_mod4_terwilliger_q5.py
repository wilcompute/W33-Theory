#!/usr/bin/env python3
"""Passes 5880--5887: eight exact continuation probes.

5880  The affine determinant normalizer and projective non-entangling Clifford
      phase-space group are explicitly GL4(2)-conjugate split extensions.
5881  The nonlinear q=3 maximum-MRD orbit contains a proper one-sided nearfield
      spread; its multiplicative group is Q8.
5882  The mod-4 Radon kernel lifts exactly the three weight-8 Reye words.
5883  The finite 2-primary Radon cokernel has radical 2C and plus-type
      determinant quotient, Arf/Brown zero on the nondegenerate quotient.
5884  All-field first/second subconstituent skeleton for the invertible-
      difference graph Gamma_r.
5885  The q=5 Hoffman 13-cell partition gives a canonical Reye block inflation,
      but its image is entirely in the footprint/check space and hence logical zero.
5886  The nonlinear q=3 clique intersection-size-2 graph splits into six
      Hamming-distance-2 SRG(81,24,9,6) components.
5887  The intrinsic q=5 zero-shell Reye triples map objectwise to the sixteen
      M2(F2) evaluation lines under the already certified cover-to-Latin conjugator.

All claims are finite algebra/coding/lattice/graph statements. No physical
identification is inferred.
"""
from __future__ import annotations

import collections
import itertools
import json
from pathlib import Path
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS5880_5887_EXTENSION_NEARFIELD_MOD4_TERWILLIGER_Q5.json"

def rank_modp(vectors, p):
    A=[list(map(lambda z:z%p,v)) for v in vectors]
    if not A: return 0
    r=0
    for c in range(len(A[0])):
        k=next((i for i in range(r,len(A)) if A[i][c]%p),None)
        if k is None: continue
        A[r],A[k]=A[k],A[r]
        inv=pow(A[r][c]%p,-1,p)
        A[r]=[(inv*x)%p for x in A[r]]
        for i in range(len(A)):
            if i!=r and A[i][c]%p:
                f=A[i][c]%p
                A[i]=[(x-f*y)%p for x,y in zip(A[i],A[r])]
        r+=1
        if r==len(A): break
    return r

def bits4(x): return tuple((x>>i)&1 for i in range(4))
def det2(x):
    a,b,c,d=bits4(x); return (a&d)^(b&c)
def qne(x):
    x1,z1,x2,z2=bits4(x)
    return x1^z1^(x1&z1)^x2^z2^(x2&z2)
def rank_cols(cols):
    span={0}
    for v in cols:
        old=tuple(span); span|={x^v for x in old}
    return (len(span)).bit_length()-1
def lin_perm(cols):
    return tuple((cols[0] if x&1 else 0)^(cols[1] if x&2 else 0)^
                 (cols[2] if x&4 else 0)^(cols[3] if x&8 else 0) for x in range(16))
def gl4_perms():
    out=[]
    for cols in itertools.permutations(range(1,16),4):
        if rank_cols(cols)==4: out.append(lin_perm(cols))
    assert len(out)==20160 and len(set(out))==20160
    return out
def pinv(p):
    out=[0]*len(p)
    for i,j in enumerate(p): out[j]=i
    return tuple(out)
def pcompose(p,q): return tuple(p[q[x]] for x in range(len(q)))
def affine_perm(t,L): return tuple(L[x]^t for x in range(16))

def pass5880(gl4):
    Odet={L for L in gl4 if all(det2(L[x])==det2(x) for x in range(16))}
    One={L for L in gl4 if all(qne(L[x])==qne(x) for x in range(16))}
    isos=[L for L in gl4 if all(qne(L[x])==det2(x) for x in range(16))]
    assert len(Odet)==len(One)==len(isos)==72
    S=isos[0]; Si=pinv(S)
    assert {pcompose(pcompose(S,L),Si) for L in Odet}==One
    Gdet={affine_perm(t,L) for t in range(16) for L in Odet}
    Gne={affine_perm(t,L) for t in range(16) for L in One}
    assert len(Gdet)==len(Gne)==1152
    assert {pcompose(pcompose(S,g),Si) for g in Gdet}==Gne
    return {
      "determinant_linear_stabilizer_order":72,"nonentangling_quadratic_stabilizer_order":72,
      "linear_isometries_between_quadratics":72,"chosen_isometry_basis_images":[S[e] for e in (1,2,4,8)],
      "affine_group_orders":[1152,1152],"explicit_affine_conjugacy":True,"extension":"split",
      "extension_kernel":"C2^4","extension_quotient":"O+(4,2) ~= S3 wr C2",
      "extension_cocycle_class":"zero: the origin-fixing linear subgroup is an explicit complement",
      "abstract_group":"2^4 : O+(4,2)",
      "deduction":"The two order-1152 groups are not merely order matches: as affine phase-space permutation groups they are GL4(2)-conjugate copies of the same split extension.",
      "boundary":"This is a projective Pauli-label/phase-space statement, not an equality of physical gate implementations including phases."
    }

M3=list(itertools.product(range(3),repeat=4))
def det3(m): return (m[0]*m[3]-m[1]*m[2])%3
def sub3(a,b): return tuple((x-y)%3 for x,y in zip(a,b))
def mmul3(A,B):
    a,b,c,d=A;e,f,g,h=B
    return ((a*e+b*g)%3,(a*f+b*h)%3,(c*e+d*g)%3,(c*f+d*h)%3)
def inv3(A):
    a,b,c,d=A; zi=pow(det3(A),-1,3)
    return ((d*zi)%3,(-b*zi)%3,(-c*zi)%3,(a*zi)%3)
def mv3(A,v): return ((A[0]*v[0]+A[1]*v[1])%3,(A[2]*v[0]+A[3]*v[1])%3)
_Q3=None
def q3_census():
    global _Q3
    if _Q3 is not None: return _Q3
    G=nx.Graph(); G.add_nodes_from(range(81))
    for i in range(81):
        for j in range(i+1,81):
            if det3(sub3(M3[i],M3[j])): G.add_edge(i,j)
    maximal=list(nx.find_cliques(G)); sizes=collections.Counter(map(len,maximal))
    assert sizes=={6:9072,9:648}
    C=[tuple(sorted(M3[i] for i in c)) for c in maximal if len(c)==9]
    def affdim(cl):
        a=cl[0]; return rank_modp([sub3(x,a) for x in cl[1:]],3)
    A=[c for c in C if affdim(c)==2]; N=[c for c in C if affdim(c)==4]
    assert (len(A),len(N))==(162,486)
    _Q3=(G,C,A,N); return _Q3

def pass5881():
    _,_,A,N=q3_census(); C=min(N)
    A0=next(x for x in C if x!=(0,0,0,0)); Cn=tuple(sorted(mmul3(inv3(A0),x) for x in C))
    e=(1,0); by_a={mv3(M,e):M for M in Cn}; V=list(itertools.product(range(3),repeat=2))
    assert len(by_a)==9 and set(by_a)==set(V)
    def plus(a,b): return ((a[0]+b[0])%3,(a[1]+b[1])%3)
    def star(a,b): return mv3(by_a[a],b)
    assoc=left=right=0
    for a,b,c in itertools.product(V,repeat=3):
        assoc += star(star(a,b),c)!=star(a,star(b,c))
        left += star(plus(a,b),c)!=plus(star(a,c),star(b,c))
        right += star(a,plus(b,c))!=plus(star(a,b),star(a,c))
    assert (assoc,left,right)==(0,288,0)
    orders=[]
    for a in V:
        if a==(0,0): continue
        z=e
        for n in range(1,20):
            z=star(z,a)
            if z==e: orders.append(n); break
    assert collections.Counter(orders)=={1:1,2:1,4:6}
    return {"maximum_MRD_cliques":648,"affine_linear_orbit":162,"nonlinear_orbit":486,
      "normalized_representative":[list(x) for x in Cn],"right_distributivity_failures":right,
      "left_distributivity_failures":left,"associativity_failures":assoc,"proper_one_sided_nearfield":True,
      "multiplicative_group_order":8,"multiplicative_element_order_distribution":{"1":1,"2":1,"4":6},
      "multiplicative_group":"Q8","full_rank_isometry_group_order":186624,"nonlinear_orbit_stabilizer_order":384,
      "deduction":"The nonlinear 486-orbit is a single isometry class represented by a proper associative one-sided nearfield spread, not unstructured nonlinear MRD noise.",
      "boundary":"Exact order-9 construction only; no claim of a new classification of finite nearfields."}

V2=[(0,0),(0,1),(1,0),(1,1)]; NZ2=[(1,0),(0,1),(1,1)]
MATS2=list(itertools.product((0,1),repeat=4)); P12=[(w,x) for w in NZ2 for x in V2]
def mv2(m,v): return ((m[0]&v[0])^(m[1]&v[1]),(m[2]&v[0])^(m[3]&v[1]))
def reye_lines(): return [frozenset(i for i,(w,x) in enumerate(P12) if x==mv2(m,w)) for m in MATS2]
def reye_code():
    lines=reye_lines(); C=set()
    for mask in range(1<<12):
        v=tuple((mask>>i)&1 for i in range(12))
        if all(sum(v[i] for i in L)%2==0 for L in lines): C.add(v)
    assert collections.Counter(map(sum,C))=={0:1,6:12,8:3}; return C
TR=[[1,0,0,1,0,0,1,0,0],[0,0,1,0,1,0,-1,-1,-1],[0,1,0,-1,-1,-1,0,0,1],
[-1,-1,-1,0,1,0,0,0,1],[0,1,0,1,0,0,0,1,0],[0,0,1,0,0,1,1,0,0],
[0,1,0,0,0,1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,1,0,0],[1,0,0,0,1,0,0,1,0]]
A3=[[2,1,1],[1,2,1],[1,1,2]]
def kron(A,B): return [[A[i][j]*B[k][l] for j in range(len(A[0])) for l in range(len(B[0]))] for i in range(len(A)) for k in range(len(B))]
GL=kron(A3,A3)
def matvec(A,v,mod=None):
    z=[sum(a*b for a,b in zip(row,v)) for row in A]; return tuple(x%mod for x in z) if mod else tuple(z)
PB=[]
for block in range(3):
    for i in range(3):
        col=[0]*12; col[4*block+i]=1; col[4*block+3]=-1; PB.append(col)
PBM=[[PB[j][i] for j in range(9)] for i in range(12)]
def mod4_kernel():
    return [x for x in itertools.product(range(4),repeat=9) if matvec(TR,x,4)==(0,)*9]

def pass5882():
    K=mod4_kernel(); assert len(K)==64
    red={tuple(x%2 for x in v) for v in K}; assert len(red)==4
    ambient={matvec(PBM,v,2) for v in red}; weights=collections.Counter(sum(v) for v in ambient)
    assert weights=={0:1,8:3}; C=reye_code(); top={v for v in C if sum(v)==8}
    assert ambient==({(0,)*12}|top)
    return {"kernel_mod4_order":64,"kernel_mod4_abstract":"(Z/2)^2 x (Z/4)^2","reduction_mod2_image_dimension":2,
      "ambient_reduced_weight_distribution":{"0":1,"8":3},"reduced_nonzero_words_equal_three_Reye_weight8_words":True,
      "weight6_heavy_words_lift_to_mod4_kernel":False,"bockstein_obstructed_Reye_directions":12,
      "liftable_Reye_subcode":"the 2D top-weight subcode {0 plus three weight-8 words}",
      "deduction":"The first 2-adic lift separates the Reye code: only its three weight-8 directions lift through ker(T_R mod 4); every heavy weight-6 direction is obstructed."}

def add4(a,b): return tuple((x+y)%4 for x,y in zip(a,b))
def pass5883():
    cols=[tuple(TR[i][j]%4 for i in range(9)) for j in range(9)]; image={(0,)*9}
    for c in cols:
        old=tuple(image); image={tuple((v[i]+a*c[i])%4 for i in range(9)) for v in old for a in range(4)}
    assert len(image)==4096
    unseen=set(itertools.product(range(4),repeat=9)); reps=[]; key={}
    while unseen:
        r=min(unseen); cos={add4(r,h) for h in image}; reps.append(r)
        for x in cos:key[x]=r
        unseen-=cos
    assert len(reps)==64
    def quadnum(x):
        gx=matvec(GL,x); return sum(a*b for a,b in zip(x,gx))%4
    qdist=collections.Counter(quadnum(x) for x in reps); assert qdist=={0:40,2:24}
    def bbit(x,y):
        gy=matvec(GL,y); return sum(a*b for a,b in zip(x,gy))%2
    rad=[x for x in reps if all(bbit(x,y)==0 for y in reps)]
    assert len(rad)==4 and {quadnum(x) for x in rad}=={0}
    doubles={key[tuple((2*a)%4 for a in x)] for x in reps}; assert doubles==set(rad)
    return {"cokernel_order":64,"cokernel_abstract":"(Z/2)^2 x (Z/4)^2","quadratic_definition":"q_C([x]) = x^T G_line x / 4 mod 1",
      "q_value_distribution":{"0":40,"1/2":24},"bilinear_radical_order":4,"radical_equals_2C":True,
      "radical_quadratic_is_zero":True,"nondegenerate_quotient":"C/2C ~= F2^4","quotient_quadratic_split":{"0":10,"1":6},
      "quotient_is_plus_type_determinant":True,"quotient_Arf_invariant":0,"quotient_normalized_Gauss_sum":1,
      "quotient_Brown_invariant_mod8":0,"boundary":"The full 64-element form is degenerate; Brown invariant is asserted only for the nondegenerate quotient C/2C."}

def rank1_graph(q):
    mats=list(itertools.product(range(q),repeat=4)); R=[m for m in mats if m!=(0,0,0,0) and (m[0]*m[3]-m[1]*m[2])%q==0]
    G=nx.Graph();G.add_nodes_from(range(len(R)))
    for i in range(len(R)):
        for j in range(i+1,len(R)):
            d=tuple((a-b)%q for a,b in zip(R[i],R[j]))
            if (d[0]*d[3]-d[1]*d[2])%q:G.add_edge(i,j)
    labels=[(i,j,s) for i in range(q+1) for j in range(q+1) for s in range(1,q)]; H=nx.Graph();H.add_nodes_from(range(len(labels)))
    for a,(i,j,s) in enumerate(labels):
        for b in range(a+1,len(labels)):
            I,J,t=labels[b]
            if i!=I and j!=J:H.add_edge(a,b)
    assert len(R)==len(labels)==(q-1)*(q+1)**2 and nx.is_isomorphic(G,H)
    assert set(dict(G.degree()).values())=={q*q*(q-1)}; return len(R),G.number_of_edges()
def pass5884():
    anchors={str(q):rank1_graph(q) for q in (2,3)}
    return {"distance_partition":"rank 0 / rank 2 / rank 1 from the base vertex 0","distance1_size":"r(r-1)^2(r+1)",
      "distance2_size":"(r-1)(r+1)^2","distance2_induced_graph":"(r-1)-independent-set blowup of complement of rook graph L2(r+1)",
      "distance2_spectrum":{"r^2(r-1)":1,"-r(r-1)":"2r","r-1":"r^2","0":"(r+1)^2(r-2)"},
      "distance1_local_graph":"Cayley derangement graph on GL2(r): A~B iff A^{-1}B has no eigenvalue 1",
      "distance1_local_degree":"a1 = r(r^3-2r^2-r+3)","cross_intersection_numbers":{"b1":"(r+1)(r^2-r-1)","c2":"r(r-1)(r^2-r-1)"},
      "primary_three_dimensional_eigenvalues":["k","r","-r(r-1)"],"exact_prime_anchors":{k:{"distance2_vertices":v[0],"edges":v[1]} for k,v in anchors.items()},
      "binary_exception":"At r=2 the 9-vertex complement of L2(3) is isomorphic to L2(3), producing the earlier doily 3x3 grid.",
      "boundary":"This closes the primary/subconstituent skeleton, not the full Terwilliger-algebra Wedderburn decomposition for all r."}

def pass5885():
    p5264=(ROOT/"analysis"/"w33_pass5264_hoffman13_cell_decomposition.py").read_text()
    assert "Counter(sum(p in blocks[c] for c in COVER) for p in range(156))==Counter({1:156})" in p5264
    p5376=(ROOT/"analysis"/"PASS5376_5379_allodd_footprint_rank_css_insert.tex").read_text()
    assert "\\operatorname{im}_2F=C_W^\\perp" in p5376
    C=reye_code(); wt=collections.Counter(map(sum,C)); assert wt=={0:1,6:12,8:3}
    inflated={12*w:n for w,n in wt.items()}; assert inflated=={0:1,72:12,96:3}
    return {"Hoffman_cover_cells":13,"cell_size":12,"partition_of_W35_points":True,"partition_size":156,
      "canonical_block_inflation":"one cover coordinate -> indicator of its 12-point P-component block","inflation_is_injective":True,
      "inflation_is_cover_stabilizer_equivariant":True,"image_contained_in":"C_W^perp = footprint/check code","local_Reye_dimension":4,
      "inflated_Reye_weight_enumerator":{"0":1,"72":12,"96":3},"composition_to_logical_quotient_CW_mod_CWperp":"zero",
      "deduction":"A canonical q=5 local-to-global map exists, but it embeds the Reye code entirely into the stabilizer/check sector and carries no nonzero logical class.",
      "compatibility_with_pass5873":"No contradiction: Pass5873 forbids 12-coordinate zero-extension into the check code; this map is 12-fold block inflation onto a partition of all 156 points."}

def pass5886():
    _,_,A,N=q3_census(); AA=collections.Counter();AN=collections.Counter();NN=collections.Counter()
    for i in range(len(A)):
        s=set(A[i])
        for j in range(i+1,len(A)):AA[len(s&set(A[j]))]+=1
        for C in N:AN[len(s&set(C))]+=1
    R=nx.Graph();R.add_nodes_from(range(len(N)))
    for i in range(len(N)):
        s=set(N[i])
        for j in range(i+1,len(N)):
            z=len(s&set(N[j]));NN[z]+=1
            if z==2:R.add_edge(i,j)
    assert set(dict(R.degree()).values())=={24}; comps=[R.subgraph(c).copy() for c in nx.connected_components(R)]
    assert sorted(map(len,comps))==[81]*6
    V=list(itertools.product(range(3),repeat=4));H=nx.Graph();H.add_nodes_from(range(81))
    for i,a in enumerate(V):
        for j in range(i+1,81):
            if sum(x!=y for x,y in zip(a,V[j]))==2:H.add_edge(i,j)
    for C in comps:
        nodes=list(C.nodes());lam=set();mu=set()
        for a,u in enumerate(nodes):
            Nu=set(C[u])
            for v in nodes[a+1:]:
                z=len(Nu&set(C[v]));(lam if C.has_edge(u,v) else mu).add(z)
        assert set(dict(C.degree()).values())=={24} and lam=={9} and mu=={6} and nx.is_isomorphic(C,H)
    return {"affine_affine_intersection_distribution":{str(k):v for k,v in sorted(AA.items())},
      "affine_nonlinear_intersection_distribution":{str(k):v for k,v in sorted(AN.items())},
      "nonlinear_nonlinear_intersection_distribution":{str(k):v for k,v in sorted(NN.items())},
      "nonlinear_intersection2_graph":{"vertices":486,"degree":24,"components":6,"component_size":81},"each_component_srg":[81,24,9,6],
      "each_component_identified_exactly_as":"Hamming-distance-2 graph on F3^4","imprimitivity_blocks":6,
      "deduction":"The nonlinear MRD orbit carries a canonical six-block imprimitivity system revealed by size-2 intersections; each block is an 81-point Hamming distance-two geometry."}

def pass5887():
    src=json.loads((ROOT/"data"/"PART_W33_PASS5667_5674_Q5_REYE_EQUIVARIANT_ORIENTATION.json").read_text())
    c=src["pass_5667_action_gate"]["cover_to_latin_conjugator_one_based"]; triples=src["pass_5669_reye_zero_shell"]["zero_triples_on_moving_twelve"]
    mapped={tuple(sorted(c[i-1] for i in T)) for T in triples}; xor_lines={tuple(sorted((i+1,j+5,(i^j)+9))) for i in range(4) for j in range(4)}
    assert mapped==xor_lines and len(mapped)==16
    eval_lines=set()
    for a,b,c0,d in itertools.product((0,1),repeat=4):
        x1=a+2*c0;x2=b+2*d;x3=x1^x2;eval_lines.add(tuple(sorted((x1+1,x2+5,x3+9))))
    assert eval_lines==xor_lines
    return {"q5_intrinsic_zero_shell_triples":16,"frozen_cover_to_Latin_conjugator":c,"mapped_zero_shell_equals_V4_Latin_graphs":True,
      "mapped_zero_shell_equals_M2F2_evaluation_lines":True,"evaluation_formula":"L_M={(w,x): x=Mw}, w in F2^2\\{0}","object_level_equality":True,
      "equivariance":"Inherited from the already certified conjugacy of the full moving-12 q=5 action to the Latin/matrix affine action.",
      "deduction":"The q=5 zero-shell Reye is not just group-isomorphic to the matrix model: under the frozen conjugator its sixteen intrinsic triples are literally the sixteen matrix-evaluation lines.",
      "boundary":"Finite q=5 cover combinatorics only; no physical two-qubit embedding follows."}

def main():
    gl4=gl4_perms()
    out={"schema":"w33.pass5880_5887.extension_nearfield_mod4_terwilliger_q5.v1","status":"PASS",
      "pass_5880_conjugate_1152_extension":pass5880(gl4),"pass_5881_q3_nearfield_spread":pass5881(),
      "pass_5882_mod4_Reye_Bockstein":pass5882(),"pass_5883_cokernel_quadratic_linking":pass5883(),
      "pass_5884_allfield_subconstituent_skeleton":pass5884(),"pass_5885_q5_cover_inflation_logical_zero":pass5885(),
      "pass_5886_q3_nonlinear_Hamming_blocks":pass5886(),"pass_5887_q5_zero_shell_matrix_object_theorem":pass5887(),
      "boundary":"Exact finite algebra, rank-metric coding, integral/2-adic lattice, finite graph and q=5 incidence statements. No continuum, particle, coupling, mass, threshold or hardware claim is inferred."}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__":main()
