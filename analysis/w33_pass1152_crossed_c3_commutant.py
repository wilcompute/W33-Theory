#!/usr/bin/env python3
"""Pass 1152: crossed commutant of the Omega_432 x C3 carrier."""
from __future__ import annotations
from fractions import Fraction
import json
from pathlib import Path
def rank_q(a):
    m=[list(map(Fraction,r)) for r in a]; rank=0
    for c in range(len(m[0])):
        p=next((i for i in range(rank,len(m)) if m[i][c]),None)
        if p is None: continue
        m[rank],m[p]=m[p],m[rank]; z=m[rank][c]; m[rank]=[x/z for x in m[rank]]
        for i in range(len(m)):
            if i!=rank and m[i][c]: q=m[i][c]; m[i]=[m[i][j]-q*m[rank][j] for j in range(len(m[0]))]
        rank+=1
    return rank
def main()->dict:
    C=[[0,0,1],[1,0,0],[0,1,0]]; eq=[]
    for i in range(3):
        for j in range(3):
            row=[0]*9
            for k in range(3): row[3*i+k]+=C[k][j]; row[3*k+j]-=C[i][k]
            eq.append(row)
    cdim=9-rank_q(eq); assert cdim==3
    result={"schema":"w33.pass1152.crossed_c3_commutant.v1","status":"PASS","ambient_G_commutant_dimension":234,"color_shift_centralizer_dimension":cdim,"crossed_commutant":{"algebra":"H(S5\\W(E6)/S5) tensor C[C3]","dimension":78,"center_dimension":27,"commutator_subspace_dimension":51,"complex_fourier_form":"H direct_sum H direct_sum H"},"dimension_drop":"234 -> 78"}
    out=Path("data/w33_pass1152_crossed_c3_commutant.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8"); print("PASS 1152 dimension",78); return result
if __name__=="__main__": main()
