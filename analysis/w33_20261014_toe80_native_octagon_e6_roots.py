"""TOE80 exact E6 root-system reconstruction FROM native W33 octagons.

Inputs are the independently group-certified 27 W33 primitive octagons,
their stabilizer-invariant 45 tritangent triples, and regular H27 center.
No E6 roots or simple Cartan matrix are imported.

The cubic-surface GQ(2,4) SRG(27,10,1,5) adjacency A gives the
EXACT rational rank-six spectral projector
       P6=(3 I-3 A+J)/18.
The 27 scaled column vectors w_i=sqrt(6)*P6 e_i have Gram 6P6.
For nonadjacent i,j the 216 ordered-as-unordered pairs generate
36 root lines, each with multiplicity six; with both signs this is
72 norm²=2 vectors closed under integral Weyl reflections.
An explicit positive-root system has 6 Cartan generators of type E6.

The 27 address weights span the six-dimensional REAL reflection module,
not the 27D trinification matter representation. Its central C3 acts on
that 6D real module as 3 omega +3 conjugate omega characters, demanding
antiunitary/conjugate-sector handling if used as a qutrit operator model.
"""
from __future__ import annotations
from collections import Counter,defaultdict,deque
from itertools import combinations,permutations
from pathlib import Path
import json,sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe77_H27_shared_octagon_group import certificate as native

def determinant_integer(a):
    """Exact Leibniz determinant for a 6-by-6 integer Cartan matrix."""
    n=len(a);total=0
    for p in permutations(range(n)):
        inversions=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        z=1
        for i,j in enumerate(p):
            z*=int(a[i][j])
        total+=(-1 if inversions%2 else 1)*z
    return total

def certificate():
    g=native()
    assert g["induced_faithful_permutation_group_order"]==216
    assert g["pair_stabilizer_is_semidirect_H27_by_D8"]
    assert g["native_216_invariant_cubic_surface_intersection_srg_count"]==1
    trit=g["native_GQ24_tritangent_lines"]
    assert len(trit)==45 and all(len(x)==3 for x in trit)
    edges={tuple(sorted(pair)) for triple in trit for pair in combinations(triple,2)}
    assert len(edges)==135
    N=27
    I=np.eye(N,dtype=np.int64)
    J=np.ones((N,N),dtype=np.int64)
    A=np.zeros((N,N),dtype=np.int64)
    for a,b in edges:A[a,b]=A[b,a]=1
    assert np.all(A.sum(axis=1)==10)
    assert np.array_equal(A@A,5*I-4*A+5*J)
    Q=3*I-3*A+J
    # P=Q/18, P²=P EXACTLY: Q²=18Q, trace(P)=6,
    # so rank(P)=6 over Q, no floating numerical rank argument.
    assert np.array_equal(Q@Q,18*Q)
    assert np.trace(Q)==108
    assert np.array_equal(Q@J,np.zeros((N,N),dtype=np.int64))
    assert set(Q.diagonal())=={4}
    assert set(Q[a,b] for a,b in edges)=={-2}
    nonadj=[(a,b) for a,b in combinations(range(N),2) if A[a,b]==0]
    assert len(nonadj)==216
    assert all(Q[a,b]==1 for a,b in nonadj)
    # w_i=sqrt(6)*P e_i, so w_i·w_j=Q_ij/3.
    # Norm²(w_i)=4/3. Adjacent inner=-2/3; nonadj=1/3.
    # Diff Q_i-Q_j represents w_i-w_j scaled by 18/sqrt(6):
    # root dot <r,s>=(r_int·s_int)/54.
    lines=defaultdict(list)
    signed=set()
    witness={}
    for a,b in nonadj:
        d=tuple(int(x) for x in Q[:,a]-Q[:,b])
        assert sum(x*x for x in d)==108
        k=next(i for i,x in enumerate(d) if x)
        canonical=d if d[k]>0 else tuple(-x for x in d)
        lines[canonical].append([a,b])
        signed.add(d)
        signed.add(tuple(-x for x in d))
        witness.setdefault(d,[a,b])
        witness.setdefault(tuple(-x for x in d),[b,a])
    assert len(lines)==36
    assert set(len(v) for v in lines.values())=={6}
    assert len(signed)==72
    roots=sorted(signed)
    dot_counts=Counter()
    root_set=set(roots)
    for u in roots:
        for v in roots:
            dot=sum(x*y for x,y in zip(u,v))
            assert dot%54==0
            k=dot//54
            assert -2<=k<=2
            dot_counts[k]+=1
            # Actual reflection in norm-two root u:
            # s_u(v)=v-<v,u>u, computed EXACTLY in integer coords.
            assert tuple(y-k*x for x,y in zip(u,v)) in root_set
    assert dict(sorted(dot_counts.items()))=={
        -2:72,-1:1440,0:2160,1:1440,2:72}
    # Deterministic generic chamber: base-11 power sum never
    # vanishes on any root; 36 positive and 36 negative.
    base=[11**i for i in range(N)]
    orient=lambda r:sum(x*b for x,b in zip(r,base))
    assert all(orient(r)!=0 for r in roots)
    positives={r for r in roots if orient(r)>0}
    assert len(positives)==36
    simple=sorted(r for r in positives
                  if not any(tuple(r[i]-u[i] for i in range(N)) in positives
                             for u in positives))
    assert len(simple)==6
    C=[]
    for u in simple:
        row=[]
        for v in simple:
            prod=sum(x*y for x,y in zip(u,v))
            assert prod%54==0
            row.append(prod//54)
        C.append(row)
    assert all(C[i][i]==2 for i in range(6))
    assert all(C[i][j] in (0,-1) for i in range(6)
               for j in range(6) if i!=j)
    assert C==[list(x) for x in zip(*C)]
    assert determinant_integer(C)==3
    degrees=[sum(C[i][j]==-1 for j in range(6)) for i in range(6)]
    assert sorted(degrees)==[1,1,1,2,2,3]
    # E6 Dynkin tree has 6 vertices, 5 edges, unique 3-leg branch
    # with arm lengths 1,2,2 (unlike D6 arm lengths 1,1,3).
    adj_simple={i:{j for j in range(6) if C[i][j]==-1} for i in range(6)}
    middle=next(i for i in range(6) if len(adj_simple[i])==3)
    assert sum(degrees)==10
    lengths=[]
    for start in adj_simple[middle]:
        visited={middle,start};last=middle;here=start;length=1
        while len(adj_simple[here])>1:
            nxt=next(x for x in adj_simple[here] if x!=last)
            assert nxt not in visited
            visited.add(nxt);last,here=here,nxt;length+=1
        lengths.append(length)
    assert sorted(lengths)==[1,2,2]
    # Stronger theorem: EACH ROOT reflection permutes the original
    # 27 weights. Six simple reflections generate 51,840 distinct
    # permutations, giving the complete E6 Weyl action explicitly.
    # Reflection of w_k about u=w_i-w_j:
    #   w_k -> w_k - <w_k,u>u,
    # checked in 27-coordinate integer numerators Q.
    col_to_index={tuple(int(z) for z in Q[:,i]):i for i in range(27)}
    assert len(col_to_index)==27
    root_reflections=set()
    for u in roots:
        p=[]
        for k in range(27):
            prod=sum(int(x)*int(y) for x,y in zip(Q[:,k],u))
            assert prod%54==0
            m=prod//54
            assert m in (-1,0,1)
            dest=tuple(int(x)-m*int(y) for x,y in zip(Q[:,k],u))
            assert dest in col_to_index
            p.append(col_to_index[dest])
        assert sorted(p)==list(range(27))
        root_reflections.add(tuple(p))
    assert len(root_reflections)==36
    simple_gen=[]
    for u in simple:
        p=[]
        for k in range(27):
            prod=sum(int(x)*int(y) for x,y in zip(Q[:,k],u))
            assert prod%54==0
            dest=tuple(int(x)-(prod//54)*int(y)
                       for x,y in zip(Q[:,k],u))
            p.append(col_to_index[dest])
        simple_gen.append(tuple(p))
    ident=tuple(range(27))
    Weyl={ident}
    fringe=deque([ident])
    while fringe:
        state=fringe.popleft()
        for gen in simple_gen:
            nxt=tuple(gen[state[i]] for i in range(27))
            if nxt not in Weyl:
                Weyl.add(nxt)
                assert len(Weyl)<=51840
                fringe.append(nxt)
    assert len(Weyl)==51840
    assert {x[0] for x in Weyl}==set(range(27))
    assert sum(perm[0]==0 for perm in Weyl)==1920
    # The 216 native octagon stabilizer sits as a subgroup of this
    # abstract cubic-line automorphism action, but no canonical global
    # isomorphism of W(E6) and the original PGSp group is selected here.
    # Native regular H27 center is the 27-point order-3 permutation Z.
    # Its 6D E6 root module has trace -3 and no C3-invariant vectors,
    # hence complexifies as 3 omega ⊕ 3 conjugate omega.
    center=g["normal_H27_center_generator_27"]
    assert sorted(center)==list(range(27))
    Z=np.zeros((27,27),dtype=np.int64)
    for i,j in enumerate(center):Z[j,i]=1
    assert np.array_equal(Z@Z@Z,I)
    assert not np.array_equal(Z,I)
    assert np.array_equal(Q@Z,Z@Q)
    assert np.trace(Q@Z)==-54
    assert np.array_equal(Q@(I+Z+Z@Z),np.zeros((27,27),dtype=np.int64))
    # Exact E6 27-line tight-frame relation:
    # sum_i w_i = 0, sum_i |w_i><w_i| = 6 I on image(P).
    assert np.array_equal(Q@np.ones(27,dtype=np.int64),
                          np.zeros(27,dtype=np.int64))
    return {
      "status":"PASS_TOE80_NATIVE_W33_OCTAGON_EXACT_E6_72_ROOTS",
      "native_W33_primitive_octagon_address_count":27,
      "native_cubic_surface_tritangents":45,
      "cubic_graph_adjacency_edges":135,
      "cubic_graph_SRG_parameters":[27,10,1,5],
      "rank_six_projector_exact":"P6=(3I-3A+J)/18",
      "scaled_integer_projector_Q":"Q=3I-3A+J; Q²=18Q, trace Q=108, QJ=0",
      "rational_projection_rank":6,
      "line_weight_Gram":"w_i·w_j=(3 delta_ij -3 A_ij+1)/3; w_i=sqrt(6)P6 e_i",
      "weight_inner_product_by_relation":{
         "same":"4/3","adjacent":"-2/3","nonadjacent":"1/3"},
      "nonadjacent_line_pairs":216,
      "positive_and_negative_E6_root_vectors":72,
      "distinct_unoriented_E6_root_lines":36,
      "each_root_line_repeated_in_nonadjacent_pairs":6,
      "E6_root_integer_vectors_representation":
         "For nonadjacent i,j use r_ij=Q[:,i]-Q[:,j] in Z^27; physical normalized root squared length is r·r/54=2",
      "root_system_integral_inner_product_histogram":{str(k):v for k,v in sorted(dot_counts.items())},
      "closure_under_all_root_reflections_exact":True,
      "positive_root_count":len(positives),
      "six_simple_roots_as_directed_octagon_index_pairs":
          [witness[u] for u in simple],
      "E6_Cartan_matrix_from_native_octagons":C,
      "E6_Cartan_determinant":3,
      "E6_Dynkin_branch_arm_lengths":sorted(lengths),
      "root_system_rank":6,
      "number_of_distinct_root_reflections_on_27_weights":len(root_reflections),
      "Weyl_group_on_27_native_weights_order":len(Weyl),
      "Weyl_group_transitive_on_27_weights":True,
      "Weyl_minuscule_weight_stabilizer_order":1920,
      "Weyl_E6_to_native_216_subgroup_index":51840//216,
      "six_generating_simple_root_reflections_27_permutations":[list(z) for z in simple_gen],
      "native_H27_center_action_on_E6_root_module":{
         "C3_projector_fixed_dimension":0,
         "trace_Z_on_six_dimensional_real_module":-3,
         "complex_irrep_eigenspaces":{"omega":3,"omega_conjugate":3},
         "meaning":"Normal H27 center acts as a complex structure on the real six-dimensional E6 reflection module. An element inverting the center exchanges the two conjugate three-dimensional sectors; it cannot be realized by unitary conjugation on a single fixed nonreal central character."},
      "native_projector_integer_numerator_27x27":Q.tolist(),
      "simple_roots_integer_27_coordinate_vectors":[list(x) for x in simple],
      "scope":"This constructs the finite E6 root system as an exact rational projector on the 27 shared W33 octagons. The explicit W(E6) permutation action on 27 weights does not imply a four-dimensional E6 gauge field, a physical Grand Unified Theory or any particle mass or coupling prediction. The bridge to the independent 27-line carrier is graph-isomorphism-level and retains noncanonical gauge choices."
    }

if __name__=="__main__":
    result=certificate()
    (ROOT/"data/w33_20261014_toe80_native_octagon_e6_roots.json").write_text(
        json.dumps(result,indent=2)+"\n")
    print(result["status"],"72_RO",result["positive_and_negative_E6_root_vectors"],
          "CARTAN",result["E6_Cartan_matrix_from_native_octagons"],
          "CENTER",result["native_H27_center_action_on_E6_root_module"])
