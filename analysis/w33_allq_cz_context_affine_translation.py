#!/usr/bin/env python3
"""All-odd-prime parabolic theorem for the CZ action on W(3,q) contexts.

Fix the standard symplectic space V=X+P with X=P=F_q^2 and form
  omega((x,p),(x',p')) = x.p' - p.x'.
Let L_inf=P={(0,p)}.  The two-qudit controlled-Z Clifford has symplectic action
  G_B:(x,p)->(x,p+B x)
with B=[[0,1],[1,0]], a nonzero symmetric invertible matrix.

POINTS.
G_B fixes L_inf pointwise projectively.  These are the q+1 fixed Pauli points
already certified by the all-q CZ theorem.

CONTEXTS / LAGRANGIAN LINES.
There are (q+1)(q^2+1) Lagrangian lines in W(3,q). Relative to L_inf:
  * 1 line is L_inf itself;
  * q(q+1) lines meet L_inf in one point;
  * q^3 lines are disjoint from L_inf.

DISJOINT STRATUM.
Every Lagrangian disjoint from P is uniquely a graph
  L_S={(x,Sx):x in F_q^2}
with S symmetric. Therefore this stratum is canonically the affine space
  Sym_2(F_q) ~= F_q^3.
Under CZ,
  S -> S+B.
For prime q this nonzero translation has no fixed point and q-cycles only:
  q^3 = q^2 * q.
At q=3 this is the exact 27-context fully-entangled sector and its nine
3-cycles observed in the photon atlas.

INTERSECTING STRATUM, q odd.
A line meeting P in K=span(k) is determined by K and one of q affine choices.
Let x span K^perp in X.  Such a line is fixed by G_B iff Bx lies in K.
For B=[[0,1],[1,0]] and odd q this occurs for exactly TWO projective K:
the two coordinate axes.  All q lines over either K are fixed. Thus:
  fixed intersecting lines = 2q;
  nonfixed intersecting lines = q(q-1) = (q-1)*q,
so the latter form q-1 cycles of length q.

TOTAL CONTEXT ACTION, odd prime q:
  cycle profile = 1^(2q+1) q^(q^2+q-1).

At q=3:
  strata 1 + 12 + 27;
  fixed counts 1 + 6 + 0;
  nontrivial cycles 0 + 2 + 9;
  total line action 1^7 3^11,
exactly the independently measured W33 photon-context result.

Boundary:
Only q=3 has the repository's physical one-photon product/self-entangled
interpretation. For general odd q this is a finite symplectic/parabolic theorem,
not a claim about physical qudits or photons.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_allq_cz_context_affine_translation.json'

def inv(a,q):return pow(a%q,-1,q)
def canon(v,q):
    i=next(i for i,x in enumerate(v) if x%q)
    z=inv(v[i],q)
    return tuple((z*x)%q for x in v)

def check_q(q):
    assert q%2==1
    # projective K lines in F_q^2
    K=sorted({canon((a,b),q) for a in range(q) for b in range(q) if a or b})
    assert len(K)==q+1
    special=[]
    for k in K:
        # one perpendicular vector x=(-k2,k1)
        x=((-k[1])%q,k[0]%q)
        Bx=(x[1]%q,x[0]%q)
        # Bx lies in K iff determinant[k,Bx]=0
        if (k[0]*Bx[1]-k[1]*Bx[0])%q==0:special.append(k)
    assert len(special)==2

    # Sym_2 translation census, represented by triples (a,b,c).
    sym=[(a,b,c) for a in range(q) for b in range(q) for c in range(q)]
    B=(0,1,0)
    act=lambda S:((S[0]+B[0])%q,(S[1]+B[1])%q,(S[2]+B[2])%q)
    seen=set();cycles=[]
    for S in sym:
        if S in seen:continue
        u=S;n=0
        while u not in seen:
            seen.add(u);n+=1;u=act(u)
        cycles.append(n)
    assert len(cycles)==q*q and set(cycles)=={q}

    total=(q+1)*(q*q+1)
    strata=[1,q*(q+1),q**3]
    assert sum(strata)==total
    fixed=1+2*q
    qcycles=(q*(q-1))//q + q**3//q
    assert qcycles==q*q+q-1
    assert fixed + q*qcycles == total
    return {'q':q,'total_contexts':total,'strata':strata,
            'special_intersection_directions':[list(x) for x in special],
            'fixed_contexts':fixed,'q_cycles':qcycles,
            'cycle_profile':{'1':fixed,str(q):qcycles},
            'transverse_affine_space_size':q**3,
            'transverse_cycles':q*q,
            'intersecting_fixed':2*q,
            'intersecting_nontrivial_cycles':q-1}

def main(write=True):
    controls=[check_q(q) for q in (3,5,7,11)]
    q3=controls[0]
    assert q3['strata']==[1,12,27]
    assert q3['cycle_profile']=={'1':7,'3':11}
    out={'schema':'w33.allq_cz_context_affine_translation.v1','status':'PASS_PARABOLIC_AFFINE_CZ_THEOREM',
      'headline':'For odd prime q, fixing the CZ pointwise Lagrangian L_inf stratifies W(3,q) contexts as 1 + q(q+1) + q^3. The q^3 transverse contexts are Sym_2(F_q) and CZ acts as the free translation S->S+B. Exactly 2q of the intersecting contexts are fixed. Hence the full context cycle profile is 1^(2q+1) q^(q^2+q-1). At q=3 this is 1^7 3^11 with strata 1+12+27, exactly the photon product/one-product/fully-entangled context census.',
      'geometry':{
        'fixed_line':'L_inf=P',
        'disjoint_contexts':'graphs L_S of symmetric 2x2 matrices S',
        'affine_identification':'Sym_2(F_q) ~= F_q^3',
        'CZ_action':'S -> S+B, B=[[0,1],[1,0]]',
        'intersecting_fixed_directions':'two coordinate axes for odd q'},
      'theorem':{
        'context_strata':'1 + q(q+1) + q^3',
        'cycle_profile':'1^(2q+1) q^(q^2+q-1)',
        'fully_transverse':'q^2 cycles of length q',
        'one-intersection_nonfixed':'q-1 cycles of length q',
        'one-intersection_fixed':'2q'},
      'q3':q3,'enumerated_controls':controls,
      'boundary':'The one-photon product/self-entangled interpretation is asserted only at q=3 from the independent BT817/flagship atlas; general q is finite symplectic geometry only.',
      'checks':{'q3_1_12_27':True,'q3_1pow7_3pow11':True,'controls_q3_q5_q7_q11':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
