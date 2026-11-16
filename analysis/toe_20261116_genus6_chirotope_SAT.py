#!/usr/bin/env python3
"""Genus-six 12-plane face simplicity: exact rank-4 signed determinant SAT.

All generic plane signs are encoded by a chirotope on 13 rank-4
vectors: 12 homogeneous planes plus the vertical point at infinity.
The 3x3 normal minors are simply determinants involving index 12.

First solve the 528 local no-cross clauses WITHOUT Grassmann-Pluecker
constraints; then add all 25740 uniform rank-4 three-term GP axioms.
A SAT assignment only gives an abstract uniform oriented matroid,
NOT necessarily a realizable 12-plane configuration in R3, nor
global nonintersecting faces. Unknown means solver timeout, not unsat.
"""
import ast,json,time,hashlib
from itertools import combinations
from pathlib import Path
from fractions import Fraction as F
import z3
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_genus6_full_chirotope_SAT.json"

def facets():
    tree=ast.parse((ROOT/"analysis"/"w33_genus_six_execution.py").read_text())
    raw=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign)
             and any(isinstance(t,ast.Name) and t.id=="FACETS_ONE" for t in n.targets))
    return set(tuple(sorted(int(x)-1 for x in f)) for f in raw)

def det3(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def det4(rows):
    a=rows[0]
    return sum((-1)**j*a[j]*det3(*[[rows[k][c] for c in range(4) if c!=j]
                                 for k in range(1,4)]) for j in range(4))
def inversion(t):
    return sum(t[i]>t[j] for i in range(len(t)) for j in range(i+1,len(t)))%2

def run():
    old=json.loads((ROOT/"data"/"toe_20261115_genus6_12plane_optimized_necessary.json").read_text())
    planes=[tuple((-F(str(a)),-F(str(b)),F(1),-F(str(c))))
            for a,b,c in old["parameters"]]
    planes.append((F(0),F(0),F(0),F(1)))
    Fs=facets()
    assert len(Fs)==44 and len(planes)==13
    minor={t:z3.Bool("neg_"+'_'.join(map(str,t))) for t in combinations(range(13),4)}
    assert len(minor)==715
    def neg(seq):
        return z3.Xor(minor[tuple(sorted(seq))],z3.BoolVal(bool(inversion(seq))))
    def eval_negative(f,k):
        return z3.Xor(neg((*f,k)),neg((*f,12)))
    S=z3.Solver()
    S.set(timeout=15000)
    constraints=[]
    for i in range(12):
        neighbors={}
        for f in Fs:
            if i in f:
                x,y=sorted(set(f)-{i})
                neighbors.setdefault(x,set()).add(y)
                neighbors.setdefault(y,set()).add(x)
        assert len(neighbors)==11 and all(len(v)==2 for v in neighbors.values())
        cyc=[min(neighbors),min(neighbors[min(neighbors)])]
        while len(cyc)<11:
            cyc.append(next(iter(neighbors[cyc[-1]]-{cyc[-2]})))
        assert cyc[0] in neighbors[cyc[-1]]
        edges=[(cyc[j],tuple(sorted((i,cyc[j],cyc[(j-1)%11]))),
                           tuple(sorted((i,cyc[j],cyc[(j+1)%11]))))
               for j in range(11)]
        for aa,bb in combinations(range(11),2):
            if bb==aa+1 or (aa==0 and bb==10):continue
            j,f0,f1=edges[aa];k,g0,g1=edges[bb]
            first=z3.Xor(eval_negative(f0,k),eval_negative(f1,k))
            second=z3.Xor(eval_negative(g0,j),eval_negative(g1,j))
            constraints.append(z3.Or(z3.Not(first),z3.Not(second)))
    assert len(constraints)==528
    S.add(constraints)
    initial={tuple(t):bool(det4([planes[x] for x in t])<0) for t in minor}
    assert all(det4([planes[x] for x in t])!=0 for t in minor)
    # Evaluate all constraints on the known nonembedded candidate independently.
    substitution=[(v,z3.BoolVal(initial[k])) for k,v in minor.items()]
    violated=sum(z3.is_false(z3.simplify(z3.substitute(c,*substitution))) for c in constraints)
    assert violated==8
    t0=time.monotonic()
    weak=str(S.check())
    weak_elapsed=time.monotonic()-t0
    assert weak=="sat"
    weak_model=S.model()
    weak_neg={k:z3.is_true(weak_model.eval(v,model_completion=True)) for k,v in minor.items()}
    assert weak_neg!=initial
    # All 3-term Grassmann-Pluecker chirotope sign axioms in rank 4:
    # terms det(abij)det(abkl), -det(abik)det(abjl),
    #       det(abil)det(abjk) cannot all have same sign.
    gp=0
    for a,b in combinations(range(13),2):
        remain=[x for x in range(13) if x not in (a,b)]
        for i,j,k,l in combinations(remain,4):
            p=z3.Xor(neg((a,b,i,j)),neg((a,b,k,l)))
            q=z3.Not(z3.Xor(neg((a,b,i,k)),neg((a,b,j,l))))
            r=z3.Xor(neg((a,b,i,l)),neg((a,b,j,k)))
            S.add(z3.Or(p!=q,q!=r))
            gp+=1
    assert gp==25740
    # Check the actual REAL candidate satisfies every GP axiom.
    # Construct the same GP clauses but check using exact rational signs directly.
    def parity(t):return bool(det4([planes[x] for x in t])<0)
    for a,b in combinations(range(13),2):
        rem=[i for i in range(13) if i not in (a,b)]
        for i,j,k,l in combinations(rem,4):
            P=parity((a,b,i,j))^parity((a,b,k,l))
            Q=not(parity((a,b,i,k))^parity((a,b,j,l)))
            R=parity((a,b,i,l))^parity((a,b,j,k))
            assert not (P==Q==R)
    S.set(timeout=35000)
    t1=time.monotonic()
    rigorous=str(S.check())
    elapsed=time.monotonic()-t1
    data={
      "status":"EXACT_GENUS6_13_VECTOR_UNIFORM_CHIROTOPE_SAT_NECESSARY_CONSTRAINTS",
      "abstract_map":"FACETS_ONE (one of 59 12-vertex neighborly genus-six maps)",
      "plane_vectors":12,"added_vertical_infinity_vector":1,
      "oriented_matroid_rank":4,
      "nonzero_chirotope_sign_variables":715,
      "face_simple_no_crossing_clauses":528,
      "Grassmann_Pluecker_uniform_rank4_axioms":gp,
      "saved_candidate_violated_face_simplicity_clauses":violated,
      "saved_candidate_satisfies_all_GP_axioms":True,
      "no_cross_only_SAT_status":weak,"no_cross_only_solve_seconds":weak_elapsed,
      "no_cross_and_GP_SAT_status":rigorous,"combined_solve_seconds":elapsed,
      "candidate_chirotope_sign_sha256":hashlib.sha256(bytes(int(initial[t]) for t in sorted(initial))).hexdigest(),
      "scope":"A SAT solution is ONLY an abstract uniform oriented matroid, not necessarily representable by 13 real rank4 vectors or a global nonselfintersecting polyhedron. UNSAT would exclude only uniform/generic plane arrangements of FACETS_ONE; nongeneric degeneracies and other 58 types remain. UNKNOWN means solver timed out; cannot infer SAT/UNSAT.",
      "no_global_polyhedron_claim":True}
    OUT.write_text(json.dumps(data,indent=2)+"\n")
    return data
if __name__=="__main__":
    x=run()
    print("RESULT",x["no_cross_only_SAT_status"],x["no_cross_and_GP_SAT_status"],
          x["Grassmann_Pluecker_uniform_rank4_axioms"],flush=True)
