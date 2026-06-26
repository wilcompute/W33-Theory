#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1825_d5_coxeter_defect_involution.json'
STRANDS=[0,1,2]
def tau(s): return {0:2,2:0,1:1}[s]
def A(state):
    p,s=state; return ((p+5)%10,tau(s))
def R(state):
    p,s=state; return ((p+2)%10,s) # Coxeter bus phase rotation on decagon phases
def I(state):
    p,s=state; return ((-p)%10,tau(s)) # inversion gauge paired with strand reflection
def compose(f,g,state): return f(g(state))
def orbit(start,gen,limit=100):
    out=[]; x=start
    while x not in out and len(out)<limit:
        out.append(x); x=gen(x)
    return out
def main():
    states=[(p,s) for p in range(10) for s in STRANDS]
    checks={'A_involution':all(A(A(x))==x for x in states),'R_order_5':all(orbit(x,R)[0]==x and len(orbit(x,R))==5 for x in states),'I_involution':all(I(I(x))==x for x in states),'D5_relation_IRI_equals_Rinv':all(compose(I,compose(R,I),x)==((x[0]-2)%10,x[1]) for x in states),'A_commutes_R':all(compose(A,R,x)==compose(R,A,x) for x in states),'A_commutes_I':all(compose(A,I,x)==compose(I,A,x) for x in states)}
    start=(3,0); Aorb=orbit(start,A); D5orb=sorted(set(orbit(x,R)[k] for x in Aorb for k in range(5)))
    payload={'bt':'BT1825','title':'D5/Coxeter test for defect involution','verified':all(checks.values()),'summary':'BT1825 tests the BT1822 antipodal defect inside the D5/Coxeter bus gauge. On decagon phase/strand states, the defect A is p->p+5 with strand toggle 0<->2. The Coxeter bus rotation is R:p->p+2 (order 5), and inversion is I:p->-p plus the same strand reflection. The checks show A is an involution, R and I generate D5, and A commutes with both R and I. Thus the defect is a central D5-invariant antipodal involution inside the 30-cell clock.', 'maps':{'A_defect':'(p,s)->(p+5,tau(s)); tau swaps 0 and 2, fixes 1','R_bus':'(p,s)->(p+2,s), order 5','I_inversion':'(p,s)->(-p,tau(s)), order 2'},'observed_start':{'phase':3,'strand':0},'A_orbit':[{'phase':p,'strand':s} for p,s in Aorb],'D5_orbit_of_A_pair':[{'phase':p,'strand':s} for p,s in D5orb],'D5_orbit_size_of_pair':len(D5orb),'checks':checks,'interpretation':'The local defect is not broken by the D5 gauge. It is the central antipodal layer: a period-2 involution commuting with the order-5 Coxeter bus rotation and with inversion.','boundary':'This is the D5 action on the C10 x K3 ring quotient. It does not enumerate the full W(E8) Coxeter normalizer.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'D5_pair_orbit_size':len(D5orb)},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
