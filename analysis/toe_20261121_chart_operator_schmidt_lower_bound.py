"""Exact operator-Schmidt rank obstruction for Witting two-ququart chart gates.

At physical chart phase t=3*pi/8, U_z=I+(-1-i)*3 Q_z/4.
All 45 have operator Schmidt rank 8 and common singular values
sqrt(17/2), sqrt(9/2), and 6 times sqrt(1/2).

A local gate rank1 and a rank-one controlled two-ququart phase gate
I+(exp(i theta)-1)P tensor Q rank<=2. Thus k such entanglers have
OSR<=2**k. Rank8 Witting U needs k>=3, necessary not sufficient.
"""
from __future__ import annotations
import math,json
from pathlib import Path
import numpy as np
import toe_20261121_relational_reference_pareto as geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261121_chart_operator_schmidt_lower_bound.json"

def os_singular_values(U):
    return np.linalg.svd(U.reshape(4,4,4,4).transpose(0,2,1,3).reshape(16,16),
                         compute_uv=False)

def chart_unitaries(rays,H):
    rayP=np.asarray([np.outer(r,r.conj()) for r in rays])
    for row in H:
        ids=np.flatnonzero(row)
        Q=sum(np.kron(rayP[i],rayP[i]) for i in ids)
        Proj=.75*Q
        assert np.max(abs(Proj@Proj-Proj))<1e-11
        assert abs(np.trace(Proj).real-6)<1e-11
        U=np.eye(16)+(-1-1j)*Proj
        assert np.max(abs(U.conj().T@U-np.eye(16)))<1e-11
        yield U,Proj

def main():
    rays,H,A,P=geometry.geometry()
    target=np.array([math.sqrt(17/2),math.sqrt(9/2)]+[1/math.sqrt(2)]*6+[0]*8)
    ranks=[]
    deviations=[]
    for U,Proj in chart_unitaries(rays,H):
        s=os_singular_values(U)
        deviations.append(float(np.max(abs(s-target))))
        ranks.append(int(np.sum(s>1e-10)))
    assert len(ranks)==45
    assert set(ranks)=={8}
    assert max(deviations)<1e-10
    firstProj=next(chart_unitaries(rays,H))[1]
    phase_scan=[]
    for angle in (0,math.pi/6,math.pi/2,math.pi,2*math.pi):
        U=np.eye(16)+(np.exp(1j*angle)-1)*firstProj
        s=os_singular_values(U)
        phase_scan.append({"chart_phase":angle,"operator_schmidt_rank":int(np.sum(s>1e-10)),
                           "leading_singular_values":s[:8].tolist()})
    assert [v["operator_schmidt_rank"] for v in phase_scan]==[1,8,8,8,1]
    obj={
      "status":"PASS",
      "date":"2026-11-21",
      "charts_tested":45,
      "all_operator_schmidt_ranks":sorted(set(ranks)),
      "max_singular_value_error_against_exact_spectrum":max(deviations),
      "nonzero_singular_values_formula":["sqrt(17/2)","sqrt(9/2)"]+["1/sqrt(2)"]*6,
      "min_rank2_entangling_gate_count_lower_bound":3,
      "proof":"OSR(U*V)<=OSR(U)*OSR(V), local gates OSR1, primitive I+(exp(i t)-1)P tensor Q has OSR<=2. Since OSR(U_chart)=8, 2^k>=8.",
      "phase_dependence":phase_scan,
      "warning":"Only a necessary lower bound for rank2 controlled-phase primitives. Physical qudit CPF operations may have different Schmidt ranks and resources; three gates are not proven sufficient."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")
    print("PASS all 45 chart gates OSR8; at least three rank-two entanglers")
    return obj

if __name__=="__main__":main()
