#!/usr/bin/env python3
"""Cross-identify the older {-4,0,+4} Steinberg frame with P,Q,R,S.

The full M3(Q) certificate reveals by coordinates that the geometric K3,3
projector Q is exactly the zero-eigenspace projector of the older deterministic
symmetric orbital 11+25, while the new K3,3-dark projector S is exactly its
+4-eigenspace projector.  This script proves those identities directly in the
59-orbital algebra and records the remaining -4 projector T.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp
from w33_20260901_steinberg_frame_common import build
from w33_20260831_c5_wedderburn_kernel import mulvec

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_STEINBERG_OLD_NEW_CROSSID.json'

def main():
    F=build();Talg,E=F['T'],F['E'];P,Q,R,S=F['Pvec'],F['Qvec'],F['Rvec'],F['Svec']
    rel,reps=F['rel'],F['reps'];zero=sp.zeros(59,1)
    tr=[]
    for seed in reps:
        a,b=divmod(seed,1080);tr.append(int(rel[b,a]))
    assert tr[11]==25
    B=sp.zeros(59,1);B[11]=1;B[25]=1;B=mulvec(E,B,Talg)
    proj={}
    for lam in (-4,0,4):
        v=E;den=sp.Rational(1)
        for mu in (-4,0,4):
            if mu==lam:continue
            v=mulvec(v,B-mu*E,Talg);den*=lam-mu
        v/=den
        assert mulvec(v,v,Talg)==v and 1080*v[F['diag']]==81
        proj[lam]=v
    assert proj[0]==Q
    assert proj[4]==S
    U=proj[-4]
    assert U==E-Q-S
    assert U==P+R-Q
    assert mulvec(U,Q,Talg)==zero==mulvec(Q,U,Talg)
    assert mulvec(U,S,Talg)==zero==mulvec(S,U,Talg)
    # Q and U are the two orthogonal primitive lines spanning P+R.
    assert Q+U==P+R
    out={'schema':'w33.20260901.steinberg-old-new-crossid.v1','status':'PASS',
      'orbitalOperator':'symmetric orbital 11+25 restricted to St^3',
      'spectralIdentification':{'eigenvalue_-4':'U = P+R-Q','eigenvalue_0':'Q_K33','eigenvalue_+4':'S_K33_dark'},
      'planeIdentity':'P+R = Q+U','allFourProjectorsActualRank':81,
      'theorem':'The older deterministic {-4,0,+4} primitive Steinberg frame and the new geometric K3,3 frame are not independent discoveries: its zero eigenspace is exactly the K3,3-selected projector Q, its +4 eigenspace is exactly the K3,3-dark projector S, and its -4 eigenspace is the unique orthogonal complement U to Q in the intrinsic P+R plane.',
      'boundary':'This exact cross-identification is in finite representation multiplicity space; the eigenvalues -4,0,+4 are not particle charges, masses, or energies.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','old0isQ':True,'oldPlus4isS':True,'oldMinus4':'P+R-Q'},sort_keys=True))

if __name__=='__main__':main()
