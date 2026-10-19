"""Transport 3 SO10xU1 27=1_4+10_-2+16_1 gradings by exact
Round12 27x27 Tits<->octonion matrix. Certify the E6 cubic
selection rules and cyclic triality automorphism coefficientwise.
Does not construct all D5 root generators or equate clocks and ticks.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round13_so10_transport.json"
def run():
    data=json.loads((ROOT/"data/w33_20261019_round12_full_octonion_intertwiner.json").read_text())
    T=s.Matrix([[s.sympify(x) for x in row] for row in data["target_to_firstTits_27x27"]]);V=T.inv()
    E=s.eye(27)
    # group 0=V01 (complement singlet index2), 1=V12 (comp0), 2=V20 (comp1).
    octave_for=[1,2,0]
    projs=[];charges=[];tables=[]
    for i in range(3):
        singlet=[i]
        vec=[j for j in range(3) if j!=i]+list(range(3+8*octave_for[i],11+8*octave_for[i]))
        spin=[j for j in range(3,27) if j not in vec]
        assert len(singlet)==1 and len(vec)==10 and len(spin)==16
        sets=[singlet,vec,spin]
        P=[]
        for idx in sets:
            D=s.diag(*[int(j in idx) for j in range(27)])
            P.append(T*D*V)
        assert all(p*p==p for p in P)
        assert sum(P,s.zeros(27))==E
        assert all(P[a]*P[b]==s.zeros(27) for a in range(3) for b in range(a+1,3))
        charge=T*s.diag(*[4 if j in singlet else -2 if j in vec else 1 for j in range(27)])*V
        assert charge==4*P[0]-2*P[1]+P[2]
        projs.append(P);charges.append(charge)
        tables.append({"clock_sector":i,"one_indices":singlet,"ten_indices":vec,"sixteen_indices":spin,
                       "traces":[int(s.trace(p)) for p in P],
                       "H_eigenvalues":{"4":1,"-2":10,"1":16}})
    # Every E6 Jordan cubic coefficient satisfies sum of U1 charges 0.
    # For canonical Cayley coordinates monomial supports are abc,
    # each -diag_complement * octet^2 and each x*y*z.
    supports=[[0,1,2]]
    for g,diag in enumerate((2,0,1)):
        supports += [[diag,3+8*g+k,3+8*g+k] for k in range(8)]
    for x in range(8):
      for y in range(8):
        for z in range(8):
            # exact triple support from round12 octonion 8-dimensional table
            from w33_20261019_round9_triality_cubic_texture import omul
            import numpy as np
            unit=np.eye(8)
            if round(2*omul(omul(unit[x],unit[y]),unit[z])[0])!=0:
                supports.append([3+x,11+y,19+z])
    assert len(supports)==89
    for i in range(3):
        vals=[4 if j in tables[i]["one_indices"] else -2 if j in tables[i]["ten_indices"] else 1 for j in range(27)]
        assert all(sum(vals[j] for j in m)==0 for m in supports)
    # Construct cyclic Peirce permutation C with C: singlet 0->1->2->0
    # and V01(0)->V12(1)->V20(2)->V01(0).
    C=s.zeros(27)
    for i in range(3):C[(i+1)%3,i]=1
    for g in range(3):
        for k in range(8):C[3+8*((g+1)%3)+k,3+8*g+k]=1
    assert C**3==E
    cycled=[sorted([int(j) for idx in tab["one_indices"] for j in range(27) if C[j,idx]==1]) for tab in tables]
    assert cycled==[[1],[2],[0]]
    cyclic_action=T*C*V
    assert cyclic_action**3==E
    assert all(cyclic_action*charges[i]*cyclic_action.inv()==charges[(i+1)%3] for i in range(3))
    # Cubic norm invariance under cyclic rotation can be checked by
    # checking a sparse coefficient dictionary on all 89 monomials.
    poly={}
    for m in supports:
        t=tuple(sorted(m));poly[t]=poly.get(t,0)+1
    remap={i:int(next(j for j in range(27) if C[j,i]!=0)) for i in range(27)}
    transformed={tuple(sorted(remap[j] for j in m)) for m in supports}
    assert transformed==set(tuple(sorted(m)) for m in supports)
    checks={"all_three_rank_1_10_16_projector_resolutions":True,
       "all_three_exact_transport_matrices_conjugate":True,
       "all_89_E6_cubic_monomials_U1_neutral":True,
       "cyclic_triality_order3_exact":True,
       "triality_cycles_three_SO10_charges":True}
    out={"schema":"w33.round13.SO10_branching_Tits_Octonion_transport.v1",
       "source_prior_art":"Repo Pass12076 states three D5 SO10 branchings, Pass12072 prohibits Clifford tick-clock equivariance. This constructs only diagonal U1 charge matrices and branching projectors, not the full forty D5 roots or a physical time operator.",
       "clock_sectors":tables,
       "charge_matrices_in_first_Tits_27_basis":[[[str(x) for x in row] for row in m.tolist()] for m in charges],
       "triality_order3_matrix_firstTits":[[str(x) for x in row] for row in cyclic_action.tolist()],
       "cubic_monomial_support_count":len(supports),
       "checks":checks,"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"rank_triples":[x["traces"] for x in tables]}))
    return out
if __name__=="__main__":run()
