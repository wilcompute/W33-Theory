#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math, sys
from collections import Counter, deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_fixed9_chiral_null_fourplusfour.json"

from analysis.w33_20260924_history_bigcell_q43_compactification import (
    history_line, graph_adj, gl2_projective_reps, history_perm,
)
from analysis.w33_20260924_temporal_maslov_mu12 import weil_phase, root12_exponent

omega=np.exp(2j*np.pi/3)
hs=list(itertools.product(range(3),repeat=3))
idx={s:i for i,s in enumerate(hs)}

def pair(r,s):
    return sum(r[i]*s[i] for i in range(3))%3

def fourier(r):
    return np.array([omega**pair(r,s) for s in hs],dtype=complex)/math.sqrt(27)

def dual_matrix(r):
    # r.s = Tr(R S) with S=[[a,b],[b,c]], so R12=2*r_b.
    return np.array([[r[0],2*r[1]],[2*r[1],r[2]]],dtype=int)%3

def det3(M):
    return (int(M[0,0])*int(M[1,1])-int(M[0,1])*int(M[1,0]))%3
def linear_dual_perm(A,eps=1):
    # Recover dual action by brute character equality under s -> eps A s A^T.
    zero=(0,0,0)
    hp=history_perm(A,zero,eps)
    out={}
    for r in hs:
        v=fourier(r)
        # permutation representation e_s -> e_{hp(s)}, so transformed function coefficient.
        w=np.zeros(27,dtype=complex)
        for j,k in enumerate(hp): w[k]=v[j]
        dots=[abs(np.vdot(fourier(q),w)) for q in hs]
        q=hs[max(range(27),key=lambda i:dots[i])]
        assert max(dots)>1-1e-9
        out[r]=q
    return out

def orbits(points,maps):
    unseen=set(points); result=[]
    while unseen:
        s=min(unseen); orb={s}; todo=deque([s])
        while todo:
            x=todo.popleft()
            for mp in maps:
                y=mp[x]
                if y not in orb: orb.add(y); todo.append(y)
        result.append(sorted(orb)); unseen-=orb
    return sorted(result,key=lambda x:(len(x),x))
def main():
    A27=graph_adj([history_line(s) for s in hs]).astype(complex)
    rank1_diffs=[s for s in hs if s!=(0,0,0)
                 and (s[0]*s[2]-s[1]*s[1])%3==0]
    assert len(rank1_diffs)==8

    eig={}
    for r in hs:
        lam=sum(omega**pair(r,d) for d in rank1_diffs)
        val=int(round(lam.real))
        assert abs(lam.imag)<1e-8
        eig[r]=val
    assert Counter(eig.values())==Counter({2:12,-1:8,-4:6,8:1})
    fixed8=[r for r in hs if eig[r]==-1]
    assert len(fixed8)==8

    reps=gl2_projective_reps()
    psp_maps=[linear_dual_perm(M,1) for M in reps]
    pgsp_maps=psp_maps+[linear_dual_perm(M,2) for M in reps]
    op=orbits(fixed8,psp_maps)
    og=orbits(fixed8,pgsp_maps)
    assert sorted(map(len,op))==[4,4]
    assert sorted(map(len,og))==[8]
    rows=[]
    for r in fixed8:
        R=dual_matrix(r); det=det3(R)
        # The dual fixed-8 vectors themselves form two oriented rank-one classes.
        rank=0 if not np.any(R) else (1 if det==0 else 2)
        assert rank==1
        # Feed the symmetric-matrix coordinates of R to the same Weil phase.
        coords=(int(R[0,0]),int(2*R[0,1])%3,int(R[1,1]))
        ph,rr,_=weil_phase(coords)
        assert rr==1
        exp=root12_exponent(ph)
        rows.append({"dual":list(r),"dual_symmetric_matrix":R.astype(int).tolist(),
                     "weil_phase_exp_mu12":exp,
                     "phase":"i" if exp==3 else "-i"})
    phase_hist=Counter(x["phase"] for x in rows)
    assert phase_hist==Counter({"i":4,"-i":4})

    # Each PSp orbit is phase-uniform; PGSp merges them.
    phase_of={tuple(x["dual"]):x["phase"] for x in rows}
    orbit_phases=[sorted({phase_of[x] for x in o}) for o in op]
    assert sorted(orbit_phases)==[["-i"],["i"]]
    out={
      "schema":"w33.20260924.fixed9_chiral_null_fourplusfour.v1",
      "status":"PASS_FIXED9_IS_VACUUM_PLUS_TWO_ORIENTED_NULL_FOURS",
      "spectral_clock_fixed_sector":{
        "dimension":9,
        "decomposition":"1 + 4_+ + 4_- under PSp Bell-line stabilizer",
        "vacuum_dimension":1,
        "nontrivial_fixed_dimension":8,
        "fourier_condition":"null-history adjacency eigenvalue -1",
      },
      "PSp_order648":{
        "dual_null_orbits":[[list(x) for x in o] for o in op],
        "orbit_sizes":[len(o) for o in op],
        "orbit_weil_phases":orbit_phases,
        "interpretation":"the two 4-orbits are the +i and -i oriented rank-one cones",
      },
      "PGSp_order1296":{
        "dual_null_orbits":[[list(x) for x in o] for o in og],
        "orbit_sizes":[len(o) for o in og],
        "interpretation":"the outer nonsquare/temporal reversal extension fuses the two chiral fours",
      },
      "weil_phase_census":dict(phase_hist),
      "theorem":(
        "The order-three null-history clock has fixed sector 9=1+8. Fourier analysis "
        "shows its eight nonconstant modes are exactly rank-one dual quadratic forms. "
        "The PSp Bell-line stabilizer has two four-element orbits on them, distinguished "
        "by normalized Weil phase +i versus -i. The full PGSp extension fuses those "
        "orbits. Thus the fixed clock sector is vacuum plus a pair of temporally "
        "conjugate four-dimensional null-orientation sectors, not the qutrit operator module."
      ),
      "rows":rows,
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "PSp_orbits":out["PSp_order648"]["orbit_sizes"],
      "phases":out["PSp_order648"]["orbit_weil_phases"],
      "PGSp_orbits":out["PGSp_order1296"]["orbit_sizes"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
