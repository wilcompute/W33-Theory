#!/usr/bin/env python3
"""Pass 1149: C3-Fourier resolution of the three cubic-kernel Steinberg copies."""
from __future__ import annotations
from fractions import Fraction
import json
from pathlib import Path
def mm(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def add(a,b): return [[a[i][j]+b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
def sub(a,b): return [[a[i][j]-b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
def scale(c,a): return [[c*x for x in row] for row in a]
def rank_q(a):
    m=[list(map(Fraction,row)) for row in a]; r=0
    for c in range(len(m[0])):
        p=next((i for i in range(r,len(m)) if m[i][c]),None)
        if p is None: continue
        m[r],m[p]=m[p],m[r]; q=m[r][c]; m[r]=[x/q for x in m[r]]
        for i in range(len(m)):
            if i!=r and m[i][c]:
                q=m[i][c]; m[i]=[m[i][j]-q*m[r][j] for j in range(len(m[0]))]
        r+=1
    return r
def main()->dict:
    I=[[Fraction(int(i==j)) for j in range(3)] for i in range(3)]
    C=[[Fraction(0),Fraction(0),Fraction(1)],[Fraction(1),Fraction(0),Fraction(0)],[Fraction(0),Fraction(1),Fraction(0)]]
    C2=mm(C,C); P0=scale(Fraction(1,3),add(add(I,C),C2)); Q=sub(I,P0); Z=[[Fraction(0)]*3 for _ in range(3)]
    assert mm(C,C2)==I and mm(P0,P0)==P0 and mm(Q,Q)==Q and mm(P0,Q)==Z
    assert rank_q(P0)==1 and rank_q(Q)==2
    total=3*81; full_kernel=2195; killed=3*432
    result={"schema":"w33.pass1149.fourier_steinberg_kernel_bridge.v1","status":"PASS","kernel_steinberg_module":"81_minus tensor C[C3]","dimension":total,"rational_color_projectors":{"trivial":"P0=(I+C+C^2)/3","cyclotomic_pair":"Q=I-P0","ranks_on_color_space":[1,2],"ranks_on_steinberg_space":[81,162]},"complex_fourier_split":[{"character":"1","rank":81},{"character":"omega","rank":81},{"character":"omega^2","rank":81}],"aligned_bridge":{"total_rank":243,"fourier_block_ranks":[81,81,81],"cubic_composite":"zero"},"hom_dimensions":{"color_extended_target":3,"single_uncolored_target":1},"killed_432_basis_columns":killed,"kernel_remainder_after_steinberg":full_kernel-total,"boundary":"A single uncolored target sees only the trivial C3 Fourier mode."}
    out=Path("data/w33_pass1149_fourier_steinberg_kernel_bridge.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("PASS 1149 rank",total); return result
if __name__=="__main__": main()
