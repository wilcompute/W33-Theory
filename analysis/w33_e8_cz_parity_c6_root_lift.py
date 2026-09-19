#!/usr/bin/env python3
"""Lift the ORIENTED-PAULI LABEL action CZ*P through the 240-root E8 Coxeter fibration.

Parents:
  data/PART_W33_PASS7163_7170_E8_HEXAGONAL_LIFT.json
  data/w33_e8_z12_to_pauli_symplectic_sign.json
  data/w33_cz_parity_oriented_c6.json

This certificate is deliberately about the finite LABEL action.

Let d=c_Coxeter^5 be the internal order-six rotation of the forty E8 root
fibers. Quotienting by <d^2>=C3 gives the 80-state signed-Pauli carrier.
Through the frozen signed-Pauli isomorphism, the label permutation
G=CZ_3*(-I) acts on those 80 labels.

Seek a root permutation
  L:(x,k)->(Qx,k+delta_x) mod 6
lifting that LABEL permutation. Pass 7164 reduces Gram preservation to
  delta_y-delta_x = s_Qx,Qy-s_xy mod6
on every non-W33 base pair.

The orientation-preserving equations have a solution and the reversing branch
does not. The resulting L preserves the complete 240-root E8 Gram matrix,
commutes with d, has order six, and induces the same permutation of the
80 signed-Pauli labels as CZ_3*(-I).

Moreover L^3=d^3=-I on the E8 roots. Defining C=L d^{-1}, C has order three,
commutes with d, and induces the pure CZ LABEL action. Hence the exact
root-system automorphism envelope is
  <d,C> ~= C6 x C3.

PHYSICAL PARITY FIREWALL.
This does NOT identify d^3 with the physical flagship theta^3 holonomy.
Holotrade commit e2390ded proves:
  * physical theta^3 / qutrit parity is INNER on su(9), with fundamental
    spectrum 5+4 and fixed algebra su(5)+su(4)+u(1), dimension 40;
  * the Coxeter half-turn d^3 is global root negation, OUTER on su(9), with
    fixed algebra so(9), dimension 36.
Since 40 != 36, no Chevalley/lattice identification can send d^3 to the
physical parity gate.

Therefore the exact dictionary proved here is only
  d  -> signed-label negation on the 80 Pauli labels,
  C  -> the CZ label permutation,
  L  -> their product label permutation.
The physical SU(9) holonomies require a different inner Chevalley lift.

The coordinate witness depends on the frozen Coxeter fiber/base/switching gauge.
Existence and group relations are exact; physical identification and coordinate
canonicity are not claimed.
"""
from __future__ import annotations
import itertools, json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_e8_cz_parity_c6_root_lift.json'

SIMPLES=[
(1,-1,-1,-1,-1,-1,-1,1),(2,2,0,0,0,0,0,0),
(-2,2,0,0,0,0,0,0),(0,-2,2,0,0,0,0,0),
(0,0,-2,2,0,0,0,0),(0,0,0,-2,2,0,0,0),
(0,0,0,0,-2,2,0,0),(0,0,0,0,0,-2,2,0)]

ISO=[0,1,39,32,34,30,23,27,22,28,26,33,38,31,35,37,36,24,29,25,
     3,16,4,12,15,8,20,9,14,19,5,18,10,21,11,7,17,6,13,2]
ETA=[1,-1,1,-1,-1,1,-1,-1,1,-1,1,1,-1,-1,1,1,-1,1,-1,1,
     -1,-1,1,1,-1,1,-1,-1,1,1,-1,1,-1,-1,1,1,-1,1,-1,-1]

CZ=((1,0,0,0),(0,1,0,0),(0,1,1,0),(1,0,0,1))
PARITY=((2,0,0,0),(0,2,0,0),(0,0,2,0),(0,0,0,2))

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def roots_e8():
    R=[]
    for i,j in itertools.combinations(range(8),2):
        for si in (1,-1):
            for sj in (1,-1):
                x=[0]*8;x[i]=2*si;x[j]=2*sj;R.append(tuple(x))
    for bits in itertools.product((1,-1),repeat=8):
        if sum(x==-1 for x in bits)%2==0:R.append(tuple(bits))
    assert len(R)==len(set(R))==240
    return R
def refl(x,r):
    q=dot(x,r); assert q%4==0; k=q//4
    return tuple(x[i]-k*r[i] for i in range(8))
def cox(x):
    y=x
    for r in SIMPLES:y=refl(y,r)
    return y
def mm(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(4))%3
                       for j in range(4)) for i in range(4))
def mv(A,v):
    return tuple(sum(A[i][j]*v[j] for j in range(4))%3 for i in range(4))
def canon(v):
    i=next(i for i,x in enumerate(v) if x); z=pow(v[i],-1,3)
    return tuple((z*x)%3 for x in v)
def scale(sign,v):
    z=1 if sign==1 else 2
    return tuple((z*x)%3 for x in v)
def compose(p,q): return [p[q[i]] for i in range(len(p))]
def pinv(p):
    q=[None]*len(p)
    for i,j in enumerate(p):q[j]=i
    return q
def ppow(p,n):
    q=list(range(len(p)))
    for _ in range(n):q=compose(p,q)
    return q
def porder(p,limit=60):
    I=list(range(len(p)));q=I
    for n in range(1,limit+1):
        q=compose(p,q)
        if q==I:return n
    raise AssertionError('order too large')
def cycle_profile(p):
    seen=set();C=Counter()
    for i in range(len(p)):
        if i in seen:continue
        u=i;n=0
        while u not in seen:
            seen.add(u);n+=1;u=p[u]
        C[n]+=1
    return dict(sorted(C.items()))

def build_parent_data():
    R=roots_e8();I={r:i for i,r in enumerate(R)}
    cp=[I[cox(r)] for r in R]
    d=list(range(240))
    for _ in range(5):d=[cp[i] for i in d]
    assert porder(d)==6
    seen=set();fib=[]
    for i in range(240):
        if i in seen:continue
        o=[];j=i
        while j not in o:
            o.append(j);seen.add(j);j=d[j]
        assert len(o)==6;fib.append(tuple(o))
    assert len(fib)==40
    phase=[{v:k for k,v in enumerate(F)} for F in fib]
    badj=[set() for _ in range(40)];soff={}
    for a,b in itertools.combinations(range(40),2):
        E=[(u,v) for u in fib[a] for v in fib[b] if dot(R[u],R[v])==4]
        if not E:
            badj[a].add(b);badj[b].add(a)
        else:
            assert len(E)==12
            D={(phase[b][v]-phase[a][u])%6 for u,v in E}
            ss=[s for s in D if (s+1)%6 in D]; assert len(ss)==1
            s=ss[0];soff[(a,b)]=s;soff[(b,a)]=(-s-1)%6
    assert all(len(x)==12 for x in badj)
    return R,d,fib,badj,soff

def signed_pauli_action():
    V=[v for v in itertools.product(range(3),repeat=4) if any(v)]
    PP=sorted({canon(v) for v in V}); assert len(PP)==40
    G=mm(CZ,PARITY)
    M={};Minv={}
    for a in range(40):
        for t in (0,1):
            v=scale(ETA[a]*((-1)**t),PP[ISO[a]])
            M[(a,t)]=v;Minv[v]=(a,t)
    assert len(Minv)==80
    Q=[None]*40;sheet=[None]*40
    for a in range(40):
        rec=[]
        for t in (0,1):
            b,u=Minv[mv(G,M[(a,t)])];rec.append((b,u^t))
        assert rec[0]==rec[1];Q[a],sheet[a]=rec[0]
    assert sorted(Q)==list(range(40))
    return Q,sheet

def solve_delta(Q,soff,orient):
    delta=[None]*40;delta[0]=0;stack=[0]
    while stack:
        a=stack.pop()
        for b in range(40):
            if (a,b) not in soff:continue
            s=soff[(a,b)];t=soff[(Q[a],Q[b])]
            rhs=(t-s)%6 if orient==1 else (t+s+1)%6
            want=(delta[a]+rhs)%6
            if delta[b] is None:delta[b]=want;stack.append(b)
            elif delta[b]!=want:return None
    return delta

def main(write=True):
    R,d,fib,badj,soff=build_parent_data();Q,sheet=signed_pauli_action()
    delta=solve_delta(Q,soff,+1);reverse=solve_delta(Q,soff,-1)
    assert delta is not None and reverse is None
    if sum((delta[a]%2)==sheet[a] for a in range(40))==0:
        delta=[(x+1)%6 for x in delta]
    assert all((delta[a]%2)==sheet[a] for a in range(40))

    L=[None]*240
    for a in range(40):
        for k in range(6):L[fib[a][k]]=fib[Q[a]][(k+delta[a])%6]
    assert sorted(L)==list(range(240))
    assert all(dot(R[i],R[j])==dot(R[L[i]],R[L[j]])
               for i in range(240) for j in range(240))
    assert all(L[d[i]]==d[L[i]] for i in range(240))
    assert porder(L)==6

    antip=ppow(d,3)
    assert ppow(L,3)==antip
    assert all(R[antip[i]]==tuple(-x for x in R[i]) for i in range(240))

    C=compose(L,pinv(d))
    assert porder(C)==3 and compose(C,d)==compose(d,C)
    assert compose(C,d)==L

    dprof=cycle_profile(d);Lprof=cycle_profile(L);Cprof=cycle_profile(C)
    assert dprof=={6:40} and Lprof=={2:3,6:39} and Cprof=={1:12,3:76}
    group={tuple(compose(ppow(d,a),ppow(C,b))) for a in range(6) for b in range(3)}
    assert len(group)==18

    parents=[json.loads((ROOT/'data/w33_e8_z12_to_pauli_symplectic_sign.json').read_text()),
             json.loads((ROOT/'data/w33_cz_parity_oriented_c6.json').read_text())]
    assert all(p['status']=='PASS' for p in parents)

    out={
      'schema':'w33.e8_cz_parity_c6_root_lift.v2',
      'status':'PASS_LABEL_LIFT__PHYSICAL_PARITY_FIREWALL',
      'headline':'The oriented-Pauli LABEL permutation CZ*(-I) admits an exact 240-root E8 lift through the Coxeter fibration. The lift preserves the full Gram matrix and yields a commuting C6 x C3 root-automorphism envelope. This is NOT a physical lift of the flagship theta^3 parity: the Coxeter half-turn is outer on su9 with fixed dimension 36, while physical parity is inner with fixed dimension 40.',
      'lift':{
        'base_action':'Q induced by the CZ*label-negation permutation through the frozen signed-Pauli map',
        'phase_solution_delta':delta,
        'phase_histogram':{str(k):delta.count(k) for k in range(6)},
        'orientation_preserving_solution':True,'orientation_reversing_solution':False,
        'sheet_parity_matches_signed_label_negation':True,
        'full_240_root_Gram_preserved':True,'commutes_with_internal_fiber_C6':True},
      'root_actions':{
        'internal_d':{'order':6,'cycles':dprof,'quotient_label_action':'v -> -v'},
        'lift_L':{'order':6,'cycles':Lprof,'quotient_label_action':'CZ followed by v -> -v'},
        'pure_CZ_label_lift_C=L*d^-1':{'order':3,'cycles':Cprof,'quotient_label_action':'CZ'}},
      'shared_center':{'identity':'L^3=d^3=global E8 root negation'},
      'generated_group':{'generators':'d (order6), C (order3)','commute':True,'order':18,'isomorphism':'C6 x C3'},
      'physical_parity_firewall':{
        'source':'wilcompute/Holotrade commit e2390ded61d93030eea0cc3f21bd5863e3b0d49f',
        'physical_theta3':'inner on su9; fixed algebra su5+su4+u1; dimension 40',
        'qutrit_parity_gate':'inner on su9; fundamental spectrum 5+4; centralizer dimension 40',
        'coxeter_half_turn_d3':'global root negation; outer on su9; fixed algebra so9; dimension 36',
        'conclusion':'40 != 36, so d^3 cannot be identified with physical parity in any Chevalley lift.'},
      'closure':{
        'proved':'exact E8 root lift of the signed-Pauli LABEL action and its C6 x C3 automorphism envelope',
        'not_proved':'a physical heterotic SU9 holonomy lift',
        'next_target':'construct or rule out an E8/Chevalley realization of the INNER 5+4 parity and commuting 5+2+2 order-three holonomy.'},
      'parents':['data/PART_W33_PASS7163_7170_E8_HEXAGONAL_LIFT.json',
                 'data/w33_e8_z12_to_pauli_symplectic_sign.json',
                 'data/w33_cz_parity_oriented_c6.json']}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
