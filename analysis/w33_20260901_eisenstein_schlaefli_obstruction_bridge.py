#!/usr/bin/env python3
"""Exact bridge between the 27x40 obstruction carrier and the old 1080
Schlaefli four-cycle carrier, plus a firewall on the E8 Eisenstein operator.

The 2026-09-01 obstruction carrier is the diagonal PSp(4,3)-set
    completion charts (27) x W33 isotropic lines (40).
Pass 4850 independently built the 1080 chordless four-cycles of the Schlaefli
27-line graph and found orbital rank 59 and three Q(sqrt(-3)) center factors.
This witness decides whether that agreement is objectwise.

It also compares the *specific* omega=C^10 used by the older E8/Witting weld
with the specific E6+A2 grading used by Pass 7081.  Equality of quadratic
fields is not promoted to equality of operators unless omega preserves the E6
carrier.
"""
from __future__ import annotations

import itertools
import json
from collections import deque
from pathlib import Path

import networkx as nx

import w33_20260901_obstruction_wedderburn_steinberg_projectors as obstruction
from w33_pass4992_4999_common import build_base
from w33_pass7081_7096_e8_z3_z4_z12_common_refinement import (
    e8_roots_doubled, simple_roots, coeff_map, dot,
)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_EISENSTEIN_SCHLAEFLI_OBSTRUCTION_BRIDGE.json'


def compose(p,q): return tuple(p[q[i]] for i in range(len(q)))


def paired_closure(A,B):
    n=len(A[0]);m=len(B[0]);I=(tuple(range(n)),tuple(range(m)))
    S={I};D=deque([I])
    while D:
        a,b=D.popleft()
        for ga,gb in zip(A,B):
            z=(compose(ga,a),compose(gb,b))
            if z not in S:S.add(z);D.append(z)
    return sorted(S)


def q4_cycles(G):
    q4=[]
    for S in itertools.combinations(range(27),4):
        H=G.subgraph(S)
        if H.number_of_edges()==4 and set(dict(H.degree()).values())=={2} and nx.is_connected(H):
            q4.append(frozenset(S))
    assert len(q4)==1080
    return q4


def e8_omega_audit():
    roots=e8_roots_doubled();R=set(roots)
    h=(1,3,9,27,81,243,729,2187)
    simp=simple_roots(roots,h);cm=coeff_map(roots,simp)
    assert len(simp)==8
    Z3_NODE=4
    neutral={r for r in roots if cm[r][Z3_NODE]%3==0}
    assert len(neutral)==78  # E6 + A2 roots = 72+6

    # Exact simple system used in w33_e8_eisenstein_witting_weld.py.
    def basis(i,s=2):
        v=[0]*8;v[i]=s;return tuple(v)
    def add(a,b):return tuple(x+y for x,y in zip(a,b))
    def sub(a,b):return tuple(x-y for x,y in zip(a,b))
    A=[
      (1,-1,-1,-1,-1,-1,-1,1),
      add(basis(0),basis(1)),
      sub(basis(1),basis(0)),
      sub(basis(2),basis(1)),
      sub(basis(3),basis(2)),
      sub(basis(4),basis(3)),
      sub(basis(5),basis(4)),
      sub(basis(6),basis(5)),
    ]
    def refl(v,a):
        # doubled roots have real inner product dot/4 and norm two.
        c=sum(x*y for x,y in zip(v,a))//4
        return tuple(v[i]-c*a[i] for i in range(8))
    def cox(v):
        for a in A:v=refl(v,a)
        return v
    def power(v,k):
        for _ in range(k):v=cox(v)
        return v
    omega={r:power(r,10) for r in roots}
    assert set(omega.values())==R and all(omega[omega[omega[r]]]==r for r in roots)
    # Fixed-point-free is the defining Eisenstein property of the old weld.
    assert all(omega[r]!=r for r in roots)

    escaped=[r for r in sorted(neutral) if omega[r] not in neutral]
    retained=len(neutral)-len(escaped)
    return {
      'oldWeldOperator':'omega=C^10, order 3, fixed-point-free on 240 E8 roots',
      'comparisonCarrier':'Pass7081 Z3-neutral E6+A2 root subsystem',
      'neutralRoots':len(neutral),'neutralRootsRetainedByOmega':retained,
      'neutralRootsEscapingUnderOmega':len(escaped),
      'preservesThisE6A2Carrier':len(escaped)==0,
      'firstEscape':{'from':list(escaped[0]),'to':list(omega[escaped[0]])} if escaped else None,
      'reading':(
        'For the exact coordinate choices already frozen in the repository, the '
        'Witting-weld omega is not silently identified with the Q(sqrt(-3)) '
        'endomorphism field of the PSp obstruction blocks unless it preserves '
        'the E6+A2 carrier.  A failure here is an operator-level firewall, not a '
        'claim that no conjugate E6 subsystem can ever be omega-stable.'),
    }


def main():
    acts,charts,wlines=obstruction.build_action()
    assert len(acts)==4 and len(charts)==27 and len(wlines)==40
    chart_act=[tuple(g[c*40]//40 for c in range(27)) for g in acts]
    line_act=[tuple(g[l]%40 for l in range(40)) for g in acts]

    CG=nx.Graph();CG.add_nodes_from(range(27))
    for a,b in itertools.combinations(range(27),2):
        if set(charts[a])&set(charts[b]):CG.add_edge(a,b)
    assert set(dict(CG.degree()).values())=={10}

    cubic=build_base();G27=cubic['G27']
    assert set(dict(G27.degree()).values())=={10}
    gm=nx.algorithms.isomorphism.GraphMatcher(CG,G27)
    mp=next(gm.isomorphisms_iter());assert len(mp)==27
    invmp={v:k for k,v in mp.items()}

    q4=q4_cycles(G27);qi={S:i for i,S in enumerate(q4)}
    qacts=[]
    for pc in chart_act:
        pv=tuple(mp[pc[invmp[v]]] for v in range(27))
        assert all(G27.has_edge(a,b)==G27.has_edge(pv[a],pv[b])
                   for a,b in itertools.combinations(range(27),2))
        qacts.append(tuple(qi[frozenset(pv[x] for x in C)] for C in q4))

    G=paired_closure(acts,qacts);assert len(G)==25920
    H=[(a,b) for a,b in G if a[0]==0];assert len(H)==24
    fixed=[i for i in range(1080) if all(b[i]==i for _a,b in H)]
    assert len(fixed)==1
    q0=fixed[0]
    phi=[None]*1080
    for a,b in G:
        x=a[0];y=b[q0]
        if phi[x] is None:phi[x]=y
        else:assert phi[x]==y
    assert len(set(phi))==1080 and all(x is not None for x in phi)
    for ga,gq in zip(acts,qacts):
        assert all(phi[ga[x]]==gq[phi[x]] for x in range(1080))

    # Fiber theorem: for each completion chart c, its 40 W33 coordinates map
    # to all forty chordless C4s carried by the sixteen cubic lines skew to c.
    fiber_checks=[]
    for c in range(27):
        cubic_line=mp[c]
        skew=set(range(27))-{cubic_line}-set(G27.neighbors(cubic_line))
        assert len(skew)==16
        mapped={q4[phi[c*40+l]] for l in range(40)}
        intrinsic={C for C in q4 if C<=skew}
        assert len(mapped)==len(intrinsic)==40 and mapped==intrinsic
        fiber_checks.append({'chart':c,'cubicLine':cubic_line,'skewLines':16,'fourCycles':40})

    e8=e8_omega_audit()
    out={
      'schema':'w33.20260901.eisenstein-schlaefli-obstruction-bridge.v1','status':'PASS',
      'gSetBridge':{
        'left':'27 completion charts x 40 W33 isotropic lines',
        'right':'1080 chordless four-cycles of the Schlaefli 27-line graph',
        'degree':1080,'ambient':'PSp(4,3)','groupOrder':25920,
        'pointStabilizerOrder':24,'baseFixedFourCycles':1,
        'equivariantBijection':True,
        'chartToCubicLine':{str(k):int(v) for k,v in sorted(mp.items())},
        'obstructionToFourCycle':phi,
        'fiberTheorem':'For each cubic line c, the 40 W33 coordinates over c are exactly the 40 chordless C4s among the 16 cubic lines skew to c.',
        'fiberChecks':fiber_checks},
      'e8EisensteinOperatorAudit':e8,
      'theorem':(
        'The depth-three obstruction carrier and the old Pass4850 Schlaefli-C4 '
        'carrier are literally the same transitive PSp(4,3)-set.  Thus the '
        'rank-59/center-15/Q(sqrt(-3)) Wedderburn theorem is prior art on the '
        'same module; what is new is the explicit obstruction<->C4 dictionary. '
        'The separate E8 omega audit keeps the common quadratic field from '
        'being promoted to a common operator without an explicit invariant carrier.'),
      'boundary':'Finite G-set and root-system statements only; no physical channel identification.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','bijection':len(set(phi)),'fiberC4':40,
      'omegaPreservesE6A2':e8['preservesThisE6A2Carrier'],
      'omegaEscapes':e8['neutralRootsEscapingUnderOmega']},sort_keys=True))

if __name__=='__main__':main()
