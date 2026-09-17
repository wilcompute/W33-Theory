#!/usr/bin/env python3
"""Close the 36-shell bridge objectwise and equivariantly.

Pass w33_suzuki_kernel_e6_quadratic_shell_bridge identified the 36 nonsingular
vectors of E/Z(E), E=2_-^(1+6), by exact orbit/stabilizer fingerprints but left
the explicit map to the repository's 36 W33 spreads / Schlaefli double-sixes
open.

The Pass4992 common reconstruction already builds the five PSp(4,3) generators
from orthogonal symmetries of the *same* Q^-(5,2) model.  We propagate those
identical generator words simultaneously on the 36 nonsingular vectors and on
the 36 double-sixes.  There is exactly one equivariant bijection.  It also
intertwines the extra orthogonal symmetry generating the full W(E6) action.
Composing with the pre-existing double-six <-> W33-spread isomorphism closes the
objectwise chain.
"""
from __future__ import annotations

from collections import deque
import json
from pathlib import Path

from w33_pass4992_4999_common import build_base, build_group, add2, polar, comp, closure

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_suzuki_kernel_e6_36_objectwise_intertwiner.json'
PHI36=(34,31,28,19,22,25,9,12,15,5,33,30,27,18,21,24,8,11,14,4,32,29,26,17,20,23,7,10,13,3,35,16,6,2,1,0)
NONS_TO_SPREAD=(7,12,32,2,21,29,8,9,22,3,6,13,20,26,14,28,27,33,23,15,5,18,35,10,24,17,25,11,30,34,1,31,16,19,4,0)


def solve_intertwiners(A,B):
    """All bijections phi with phi(A_g i)=B_g phi(i), seeded by phi(0)."""
    n=len(A[0]); out=[]
    for y0 in range(n):
        mp={0:y0}; q=deque([0]); ok=True
        while q and ok:
            x=q.popleft(); y=mp[x]
            for ga,gb in zip(A,B):
                xx=ga[x]; yy=gb[y]
                if xx in mp:
                    if mp[xx]!=yy: ok=False; break
                else:
                    mp[xx]=yy; q.append(xx)
        if ok and len(mp)==n and len(set(mp.values()))==n:
            out.append(tuple(mp[i] for i in range(n)))
    return out


def main(write=True):
    b=build_base(); g=build_group(b)
    sing=b['sing']; nons=b['nons']; DS=b['DS']; di=b['di']
    si={v:i for i,v in enumerate(sing)}; ni={v:i for i,v in enumerate(nons)}

    # Orthogonal symmetry r_v(x)=x+B(x,v)v on both quadratic shells.
    tS=[tuple(si[add2(x,v) if polar(x,v) else x] for x in sing) for v in nons]
    tN=[tuple(ni[add2(x,v) if polar(x,v) else x] for x in nons) for v in nons]
    cS=[comp(tS[0],t) for t in tS[1:]]
    cN=[comp(tN[0],t) for t in tN[1:]]

    # Reproduce the exact deterministic greedy generator selection of build_group.
    gp=[]; gn=[]; S0={tuple(range(27))}; chosen=[]
    for idx,(ps,pn) in enumerate(zip(cS,cN)):
        T=closure(gp+[ps],27)
        if len(T)>len(S0):
            gp.append(ps); gn.append(pn); chosen.append(idx); S0=T
        if len(S0)==25920: break
    assert tuple(chosen)==(0,2,5,9,19)
    assert gp==g['gp'] and len(closure(gn,36))==25920

    def dperm(p): return tuple(di[frozenset(p[x] for x in D)] for D in DS)
    DPp=[dperm(p) for p in gp]
    assert DPp==g['DPp'] and len(closure(DPp,36))==25920

    sols=solve_intertwiners(gn,DPp)
    assert len(sols)==1 and sols[0]==PHI36
    phi=sols[0]
    assert all(phi[gn[k][i]]==DPp[k][phi[i]] for k in range(len(gp)) for i in range(36))

    # The same map intertwines the missing outer orthogonal generator as well.
    outerN=tN[0]; outerD=dperm(tS[0])
    assert all(phi[outerN[i]]==outerD[phi[i]] for i in range(36))
    assert len(closure(gn+[outerN],36))==51840
    assert len(closure(DPp+[outerD],36))==51840

    # Compose with the independently constructed double-six -> W33 spread map.
    ds_to_spread=b['iso_ds_sp']
    ns_to_spread=tuple(ds_to_spread[phi[i]] for i in range(36))
    assert ns_to_spread==NONS_TO_SPREAD and sorted(ns_to_spread)==list(range(36))

    chain=json.loads((ROOT/'data'/'w33_psp36_spread_double_six_pfaffian_equivariance.json').read_text())
    assert chain['status']=='PASS' and chain['group']['degree']==36

    out={
      'schema':'w33.suzuki_kernel_e6_36_objectwise_intertwiner.v1','status':'PASS',
      'headline':'The 36 nonsingular vectors of the Suzuki kernel quotient E/Z(E)=F2^6_minus are uniquely and explicitly equivariantly identified with the 36 Schlaefli double-sixes under the exact five repository PSp(4,3) generators. The same bijection intertwines the outer orthogonal generator, so it is full W(E6)=O6^-(2)-equivariant. Composing with the certified double-six-to-W33-spread map gives an explicit nonsingular-vector <-> W33-spread bijection and closes the 27+36 kernel-shell bridge objectwise.',
      'generator_indices':chosen,
      'inner_group_order':25920,
      'full_group_order':51840,
      'unique_intertwiner_count':len(sols),
      'nonsingular_to_double_six':list(phi),
      'nonsingular_to_W33_spread':list(ns_to_spread),
      'outer_generator_intertwines':True,
      'composed_existing_chain':'nonsingular kernel vector <-> Schlaefli double-six <-> W33 spread <-> doily complement <-> signed Pfaffian section of the E6 Cartan cubic',
      'boundary':'This is an exact finite equivariant identification. It does not make the binary kernel shell a physical three-qubit subsystem or identify its quadratic value with an experimentally measured observable.'
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2)); return out

if __name__=='__main__': main(True)
