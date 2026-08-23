#!/usr/bin/env python3
"""Pass9253-9260 outside-box: Q-(5,3) glue selector versus Q+(5,3) Suzuki selector.

The transverse Golay/E6 glue pair constructs K and R (Pass9237-9244).  On the
Golay Lagrangian, C_-(a,b)=K(a,Rb) is a symmetric nondegenerate minus-type
6D form.  Its 2-space selector has the SAME number of nondegenerate candidates
as the Suzuki plus-type form.  A symbolic orthogonal-group calculation proves
this equality for every odd q and proves the hyperbolic/anisotropic shift q^6.
"""
from __future__ import annotations
import itertools,json,sys
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'analysis'))
import w33_rank24_root_shadow_core as rs
from w33_pass9093_9100_suzuki_qplus53_w33_selector import two_spaces_6
OUT=ROOT/'data/PART_W33_PASS9253_9260_ORTHOGONAL_SIGN_TWIN_SELECTOR.json';P=3

def type2(space,C):
 B=np.array(space,dtype=np.int64).T%P;G=B.T@C@B%P;r=rs.rank_modp(G,P)
 if r<2:return 'degenerate'
 iso=any(z!=(0,0) and int(np.array(z,dtype=np.int64)@G@np.array(z,dtype=np.int64))%P==0 for z in itertools.product(range(P),repeat=2))
 return 'hyperbolic' if iso else 'anisotropic'

def canon(v):
 v=tuple(int(x)%P for x in v)
 for x in v:
  if x:
   u=pow(x,-1,P);return tuple(u*y%P for y in v)
 raise ValueError

def main():
 G=np.array(rs.GOLAY12,dtype=np.int64)%P
 glue=json.loads((ROOT/'data/PART_W33_PASS9185_9196_GOLAY_TETRACODE_GLUE_BIFURCATION.json').read_text())
 E=np.array(glue['N(E6^4)_relative_glue']['generator_rref'],dtype=np.int64)%P
 pairing=G@E.T%P;H=rs.inv_mod(pairing,P).T@E%P;C=np.vstack([G,H])%P;Ci=rs.inv_mod(C,P)
 I6=np.eye(6,dtype=np.int64);Z=np.zeros((6,6),dtype=np.int64);D=np.block([[I6,Z],[Z,-I6]])%P;Swap=np.block([[Z,I6],[I6,Z]])%P
 K=Ci@D@C%P;S=Ci@Swap@C%P;R=K@S%P
 Cminus=G@K@(G@R%P).T%P
 assert np.array_equal(Cminus,Cminus.T) and rs.rank_modp(Cminus,P)==6 and np.array_equal(Cminus,I6%P)
 pts=sorted({canon(v) for v in itertools.product(range(P),repeat=6) if any(v)})
 singular=sum(int(np.array(v,dtype=np.int64)@Cminus@np.array(v,dtype=np.int64))%P==0 for v in pts);assert singular==112
 cnt=Counter(type2(z,Cminus) for z in two_spaces_6());assert cnt==Counter({'hyperbolic':4536,'degenerate':3640,'anisotropic':2835})
 plus=json.loads((ROOT/'data/PART_W33_PASS9093_9100_SUZUKI_QPLUS53_W33_SELECTOR.json').read_text())
 pc=plus['two_space_census'];assert (pc['degenerate'],pc['hyperbolic'],pc['anisotropic'])==(3640,5265,2106)
 assert cnt['hyperbolic']+cnt['anisotropic']==pc['hyperbolic']+pc['anisotropic']==7371
 assert pc['hyperbolic']-cnt['hyperbolic']==cnt['anisotropic']-pc['anisotropic']==729
 # General odd-q identity from orthogonal-group orbit-stabilizer formulas.
 q=sp.symbols('q', positive=True, integer=True)
 O2p=2*(q-1);O2m=2*(q+1)
 O4p=2*q**2*(q**2-1)**2;O4m=2*q**2*(q**2+1)*(q**2-1)
 O6p=2*q**6*(q**3-1)*(q**2-1)*(q**4-1);O6m=2*q**6*(q**3+1)*(q**2-1)*(q**4-1)
 Hp=sp.factor(O6p/(O2p*O4p));Ap=sp.factor(O6p/(O2m*O4m));Hm=sp.factor(O6m/(O2p*O4m));Am=sp.factor(O6m/(O2m*O4p))
 assert sp.simplify((Hp+Ap)-(Hm+Am))==0
 assert sp.factor(Hp-Hm)==q**6 and sp.factor(Am-Ap)==q**6
 total_formula=sp.factor(Hp+Ap);assert total_formula==q**4*(q**2-q+1)*(q**2+q+1)
 out={'schema':'w33.pass9253_9260.orthogonal_sign_twin_selector.v2','status':'PASS','passes':'9253-9260',
      'Niemeier_glue_selector':{'orthogonal_type':'Q-(5,3)','singular_projective_points':112,'two_space_census':dict(cnt),'nondegenerate_W33_candidates':7371},
      'Suzuki_selector':{'orthogonal_type':'Q+(5,3)','singular_projective_points':130,'two_space_census':{'degenerate':3640,'hyperbolic':5265,'anisotropic':2106},'nondegenerate_W33_candidates':7371},
      'general_odd_q_identity':{'nondegenerate_2space_total':'q^4 (q^2-q+1)(q^2+q+1), independent of orthogonal sign','hyperbolic_shift_plus_minus_minus':'q^6','anisotropic_shift_minus_minus_plus':'q^6'},
      'q3_shift':{'value':729,'equals':'3^6 = size of either ternary [12,6] glue code'},
      'theorem':'The Golay/E6 transverse-glue polarization produces a minus-type Q-(5,3) selector that is an exact orthogonal-sign twin of the Suzuki Q+(5,3) selector. Both select 7,371 nondegenerate 2-spaces/W33 candidates. More generally for every odd q, O+(6,q) and O-(6,q) have the same q^4(q^2-q+1)(q^2+q+1) nondegenerate 2-spaces, while changing sign transfers exactly q^6 cases between hyperbolic and anisotropic type.',
      'boundary':'The general count follows from standard orthogonal-group orders and orbit-stabilizer. At q=3 the q^6 shift equals the 729-word glue-code cardinality; that numerical equality is forced by the common dimension six, not claimed as an independent moonshine or physical law.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','minus':[4536,2835],'plus':[5265,2106],'total':7371,'shift':729,'general_total':str(total_formula)}))
 return 0
if __name__=='__main__':raise SystemExit(main())
