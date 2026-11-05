#!/usr/bin/env python3
"""Independent non-prime q=9 audit of the odd-field affine-null spectral clock.

F9 = F3[a]/(a^2+1), with elements a+b*alpha, alpha^2=2.
The six base-3 coordinates represent three F9-valued symmetric matrix entries.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import json
import numpy as np

def sq(a,b):
    return (a*a+2*b*b)%3, (2*a*b)%3

def verify():
    t0,t1,x0,x1,y0,y1=np.indices((3,)*6,dtype=np.int64)
    a0,a1=sq(t0,t1)
    b0,b1=sq(x0,x1)
    c0,c1=sq(y0,y1)
    mask=(((a0-b0-c0)%3==0)&((a1-b1-c1)%3==0)&
          ((t0!=0)|(t1!=0)|(x0!=0)|(x1!=0)|(y0!=0)|(y1!=0)))
    cone=mask.astype(np.int64)
    assert cone.shape==(3,)*6
    assert int(cone.sum())==80
    eig=np.fft.fftn(cone)
    assert np.max(np.abs(eig.imag))<1e-9
    rounded=np.rint(eig.real)
    assert np.max(np.abs(eig.real-rounded))<1e-9
    counts=Counter(int(v) for v in rounded.flat)
    assert counts=={80:1,8:360,-1:80,-10:288},counts
    assert sum(m*e for e,m in counts.items())==0
    assert sum(m*e*e for e,m in counts.items())==729*80
    phases=Counter()
    for e,m in counts.items():
        phases[((80-e)//9)%9]+=m
    assert phases=={0:81,8:360,1:288}
    report={
      "field":"F9=F3[alpha]/(alpha^2+1), alpha^2=2",
      "graph":"VO(3,9), Cayley null cone on Sym2(F9)",
      "vertex_count":729, "degree":80,
      "eigenvalues":{str(k):v for k,v in sorted(counts.items())},
      "laplacian_eigenvalues":{str(80-k):v for k,v in sorted(counts.items())},
      "clock_order":9, "fixed_modes":81,
      "nontrivial_normalized_adjacency_radius":1/8,
      "validation":"6D additive FFT over F3^6; Fourier eigenvalues certified to 1e-9, theoretical exact values from odd-field Gauss sums",
      "scope":"finite algebra only; no measured physical clock, no gravity or continuum derivation"
    }
    dest=Path(__file__).resolve().parents[1]/"data"/"w33_20261105_f9_null_clock_extension.json"
    dest.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("PASS Q9",report["eigenvalues"],"fixed_modes",report["fixed_modes"],"CERTIFICATE",dest)
    return report

if __name__=="__main__":
    verify()
