#!/usr/bin/env python3
"""BT522: Projector Arithmetic Eigenvalue Derivation Theorem.

Executes branch 1 from the latest next-step list.

Goal: derive the BT512/BT514 lift eigenvalue multiplicities without using a
numeric eigensolver.  We rebuild the exact integer incidence matrices and use:
  * polynomial annihilators for the projective and odd Gram matrices;
  * integer trace moments and exact Vandermonde solves for multiplicities;
  * the exact BT519 projector identity for the coupling eigenvalue.

Matrices:
  M  = 320 x 1620 signed-Xmin/quadrangle lift.
  Q+ = 160 x 1620 antipodal pair-sum matrix.
  Q- = 160 x 1620 antipodal pair-difference matrix.
  C  = Q+ Q-^T.

Exact results recovered by arithmetic, not eigensolver:
  Spec(MM^T)     = 1296^1 + 464^24 + 144^30 + 112^24 + 80^81 + 0^160.
  Spec(Q+Q+^T)   = 2592^1 + 792^24 + 288^15 + 0^120.
  Spec(Q-Q-^T)   = 360^24 + 288^15 + 160^81 + 0^40.
  Spec(CC^T)     = 77760^24 + 0^136.
"""
from __future__ import annotations

import itertools, json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import sympy as sp

P = 3
Vec = tuple[int, int, int, int]


def canonical(v) -> Vec:
    vv = tuple(int(x) % P for x in v)
    if vv == (0, 0, 0, 0):
        raise ValueError("zero")
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % P for y in vv)  # type: ignore[return-value]
    raise AssertionError


def omega(u: Vec, v: Vec) -> int:
    return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1]) % P


def build_geometry():
    pts=[]; seen=set()
    for raw in itertools.product(range(P), repeat=4):
        if raw == (0,0,0,0):
            continue
        c=canonical(raw)
        if c not in seen:
            seen.add(c); pts.append(c)
    pidx={p:i for i,p in enumerate(pts)}
    A=np.zeros((40,40), dtype=np.int64); edges=[]
    for i,j in itertools.combinations(range(40),2):
        if omega(pts[i], pts[j]) == 0:
            A[i,j]=A[j,i]=1; edges.append((i,j))
    lines=set()
    for i,j in edges:
        u,v=pts[i],pts[j]; line=set()
        for a,b in itertools.product(range(P), repeat=2):
            if a==0 and b==0:
                continue
            line.add(pidx[canonical((a*u[t]+b*v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    lines=sorted(lines)
    point_lines=defaultdict(list); edge_to_line={}
    for li,L in enumerate(lines):
        for p in L:
            point_lines[p].append(li)
        for e in itertools.combinations(L,2):
            edge_to_line[tuple(sorted(e))]=li
    return A, point_lines, edge_to_line


def ordinary_quadrangles(A):
    quads=[]; seen=set()
    for a,b in itertools.combinations(range(40),2):
        if A[a,b]:
            continue
        common=[x for x in range(40) if A[a,x] and A[b,x]]
        for c,d in itertools.combinations(common,2):
            cyc=tuple(sorted(tuple(sorted(e)) for e in ((a,c),(c,b),(b,d),(d,a))))
            if cyc not in seen:
                seen.add(cyc); quads.append(cyc)
    return quads


def local_signed(p:int, Ls:list[int]):
    Ls=sorted(Ls); faces=[]; v2f=defaultdict(list)
    for L in Ls:
        others=[x for x in Ls if x != L]
        star=[tuple(sorted((L,M))) for M in others]
        opp=[tuple(sorted(pair)) for pair in itertools.combinations(others,2)]
        fp=(p,L,1); fm=(p,L,-1); faces += [fp,fm]
        for v in star:
            v2f[(p,v)].append(fp)
        for v in opp:
            v2f[(p,v)].append(fm)
    return faces, v2f


def matrices():
    A, point_lines, edge_to_line = build_geometry()
    quads = ordinary_quadrangles(A)
    signed=[]; v2f={}
    for p in range(40):
        fs, loc = local_signed(p, point_lines[p])
        signed += fs; v2f.update(loc)
    signed=sorted(signed); pairs=sorted({(p,L) for p,L,s in signed})
    sf_idx={f:i for i,f in enumerate(signed)}; pair_idx={p:i for i,p in enumerate(pairs)}
    M=np.zeros((320,1620), dtype=np.int64)
    for qi,cyc in enumerate(quads):
        inc=defaultdict(list)
        for u,v in cyc:
            inc[u].append((u,v)); inc[v].append((u,v))
        for p,es in inc.items():
            lpair=tuple(sorted(edge_to_line[tuple(sorted(e))] for e in es))
            for f in v2f[(p,lpair)]:
                M[sf_idx[f], qi] = 1
    Qp=np.zeros((160,1620), dtype=np.int64); Qm=np.zeros((160,1620), dtype=np.int64)
    for p,L in pairs:
        i=pair_idx[(p,L)]
        Qp[i] = M[sf_idx[(p,L,1)]] + M[sf_idx[(p,L,-1)]]
        Qm[i] = M[sf_idx[(p,L,1)]] - M[sf_idx[(p,L,-1)]]
    return A, M, Qp, Qm


def trace_moments(G: np.ndarray, max_power: int) -> list[int]:
    out=[]
    Pwr=np.eye(G.shape[0], dtype=object)
    Gobj=G.astype(object)
    for k in range(max_power+1):
        out.append(int(sum(Pwr[i,i] for i in range(G.shape[0]))))
        Pwr=Pwr@Gobj
    return out


def multiplicities_from_moments(eigs: list[int], moments: list[int]) -> dict[str,int]:
    m=sp.symbols('m0:'+str(len(eigs)))
    eqs=[]
    for k in range(len(eigs)):
        eqs.append(sp.Eq(sum(m[i]*(eigs[i]**k) for i in range(len(eigs))), moments[k]))
    sol=sp.solve(eqs, m, dict=True)[0]
    return {str(eigs[i]): int(sol[m[i]]) for i in range(len(eigs))}


def annihilator_zero(G: np.ndarray, roots: list[int]) -> bool:
    X=np.eye(G.shape[0], dtype=object)
    Gobj=G.astype(object)
    for r in roots:
        X=X@(Gobj - r*np.eye(G.shape[0], dtype=object))
    return not np.any(X)


def main() -> dict:
    A, M, Qp, Qm = matrices()
    Gs=M@M.T; Ge=Qp@Qp.T; Go=Qm@Qm.T; C=Qp@Qm.T; Gc=C@C.T

    signed_eigs=[1296,464,144,112,80,0]
    even_eigs=[2592,792,288,0]
    odd_eigs=[360,288,160,0]
    coup_eigs=[77760,0]

    # Exact low-degree annihilators where practical.
    assert annihilator_zero(Ge, even_eigs)
    assert annihilator_zero(Go, odd_eigs)
    assert annihilator_zero(Gc, coup_eigs)

    signed_mult=multiplicities_from_moments(signed_eigs, trace_moments(Gs, len(signed_eigs)-1))
    even_mult=multiplicities_from_moments(even_eigs, trace_moments(Ge, len(even_eigs)-1))
    odd_mult=multiplicities_from_moments(odd_eigs, trace_moments(Go, len(odd_eigs)-1))
    coup_mult=multiplicities_from_moments(coup_eigs, trace_moments(Gc, len(coup_eigs)-1))

    assert signed_mult == {'1296':1,'464':24,'144':30,'112':24,'80':81,'0':160}
    assert even_mult == {'2592':1,'792':24,'288':15,'0':120}
    assert odd_mult == {'360':24,'288':15,'160':81,'0':40}
    assert coup_mult == {'77760':24,'0':136}

    # W33 projector arithmetic: P2 numerator has eigenvalue 60 on the +2 sector.
    I=np.eye(40, dtype=np.int64)
    P2num=(12*I-A)@(A+4*I)
    assert np.trace(P2num)//60 == 24
    assert P2num@P2num == 60*P2num

    results={
        'theorem':'BT522 Projector Arithmetic Eigenvalue Derivation Theorem',
        'method':'integer trace moments + annihilator polynomials; no numeric eigensolver used for multiplicities',
        'annihilators':{
            'even':'x(x-288)(x-792)(x-2592)=0',
            'odd':'x(x-160)(x-288)(x-360)=0',
            'coupling':'x(x-77760)=0'},
        'spectra_from_trace_moments':{
            'signed_MMt':signed_mult,
            'even_Qplus':even_mult,
            'odd_Qminus':odd_mult,
            'coupling_CCt':coup_mult},
        'projector_arithmetic':{'P2num':'(12I-A)(A+4I)','P2num_squared':'P2num^2=60 P2num','trace_P2num_over_60':24},
        'substrate_reading':{'1296':'16*81 signed top degree','2592':'16*162 projective top degree','77760':'324*60*4 coupling scale','81':'trace-derived odd/signed protected multiplicity','24':'W33 +2 projector rank and coupling multiplicity'}
    }
    out=Path('data/PART_BT522_PROJECTOR_ARITHMETIC_EIGENVALUE_DERIVATION_results.json')
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2)); return results

if __name__=='__main__': main()
