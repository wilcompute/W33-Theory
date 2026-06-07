#!/usr/bin/env python3
"""BT514: Xmin Even/Odd Coupling Bridge Theorem.

This corrects/refines BT513.

BT513's intended antipodal signed-face split is right, but the naive claim that
the even and odd sectors are orthogonal is false.  The correction is stronger:
the even/projective and odd/chiral sectors are coupled by a pure rank-24 bridge.

Let M be the 320 x 1620 signed-Xmin/quadrangle lift from BT512.  Rows come in
antipodal pairs (p,L,+), (p,L,-).  Define:
    Q+ = plus + minus   (even/projective pair-sum)
    Q- = plus - minus   (odd/chiral pair-difference)

Then:
  Spec(Q+ Q+^T) = 2592^1 + 792^24 + 288^15 + 0^120
  Spec(Q- Q-^T) = 360^24 + 288^15 + 160^81 + 0^40
  C = Q+ Q-^T is not zero.  It has:
      entries in {-9,0,27}, row/column sums zero,
      rank(C)=24,
      Spec(C C^T)=77760^24 + 0^136,
      singular value = 72*sqrt(15) with multiplicity 24.

Thus the even and odd sectors communicate only through the W33 24-dimensional
sector.  The 81-dimensional homology/generation sector remains in the odd
chiral side and is not part of the even-odd coupling bridge.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

import numpy as np

P_FIELD = 3
Vec = tuple[int, int, int, int]


def canonical(v) -> Vec:
    vv = tuple(int(x) % P_FIELD for x in v)
    if vv == (0, 0, 0, 0):
        raise ValueError("zero vector")
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % P_FIELD for y in vv)  # type: ignore[return-value]
    raise AssertionError


def omega(u: Vec, v: Vec) -> int:
    return (u[0]*v[2] - u[2]*v[0] + u[1]*v[3] - u[3]*v[1]) % P_FIELD


def build_geometry():
    points=[]; seen=set()
    for raw in product(range(P_FIELD), repeat=4):
        if raw == (0,0,0,0):
            continue
        c=canonical(raw)
        if c not in seen:
            seen.add(c); points.append(c)
    pidx={p:i for i,p in enumerate(points)}
    edges=[(i,j) for i,j in combinations(range(len(points)),2) if omega(points[i],points[j])==0]
    adj=[[False]*len(points) for _ in points]
    for i,j in edges:
        adj[i][j]=adj[j][i]=True
    lines=set()
    for i,j in edges:
        u,v=points[i],points[j]
        line=set()
        for a,b in product(range(P_FIELD), repeat=2):
            if a==0 and b==0:
                continue
            line.add(pidx[canonical((a*u[t]+b*v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    lines=sorted(lines)
    point_lines=defaultdict(list); edge_to_line={}
    for li,L in enumerate(lines):
        for p in L:
            point_lines[p].append(li)
        for e in combinations(L,2):
            edge_to_line[tuple(sorted(e))]=li
    return points, edges, adj, lines, point_lines, edge_to_line


def ordinary_quadrangles(adj):
    quads=[]; seen=set()
    for a,b in combinations(range(len(adj)),2):
        if adj[a][b]:
            continue
        common=[x for x in range(len(adj)) if adj[a][x] and adj[b][x]]
        for c,d in combinations(common,2):
            cyc=tuple(sorted(tuple(sorted(e)) for e in ((a,c),(c,b),(b,d),(d,a))))
            if cyc not in seen:
                seen.add(cyc); quads.append(cyc)
    return quads


def local_signed_faces(p:int, Ls:list[int]):
    Ls=sorted(Ls)
    faces=[]; v2f=defaultdict(list)
    for L in Ls:
        others=[x for x in Ls if x!=L]
        star=tuple(sorted(tuple(sorted((L,M))) for M in others))
        opp=tuple(sorted(tuple(sorted(pair)) for pair in combinations(others,2)))
        f_star=(p,L,+1)
        f_opp=(p,L,-1)
        faces.extend([f_star,f_opp])
        for v in star:
            v2f[(p,v)].append(f_star)
        for v in opp:
            v2f[(p,v)].append(f_opp)
    return faces, v2f


def spectrum_counter(A: np.ndarray) -> dict[str, int]:
    return {str(k): int(v) for k, v in sorted(Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float))).items())}


def main() -> dict:
    points, edges, adj, lines, point_lines, edge_to_line = build_geometry()
    quads=ordinary_quadrangles(adj)
    assert len(points)==40 and len(lines)==40 and len(edges)==240 and len(quads)==1620

    signed_faces=[]; local_vertex_to_faces={}
    for p in range(len(points)):
        faces, v2f = local_signed_faces(p, point_lines[p])
        signed_faces.extend(faces)
        local_vertex_to_faces.update(v2f)
    signed_faces=sorted(signed_faces)
    pairs=sorted({(p,L) for p,L,s in signed_faces})
    sf_idx={f:i for i,f in enumerate(signed_faces)}
    pair_idx={pair:i for i,pair in enumerate(pairs)}
    assert len(signed_faces)==320 and len(pairs)==160

    M=np.zeros((320, len(quads)), dtype=np.int16)
    for qi,cyc in enumerate(quads):
        inc=defaultdict(list)
        for u,v in cyc:
            inc[u].append((u,v)); inc[v].append((u,v))
        for p,es in inc.items():
            lpair=tuple(sorted(edge_to_line[tuple(sorted(e))] for e in es))
            for f in local_vertex_to_faces[(p,lpair)]:
                M[sf_idx[f], qi] += 1

    Qp=np.zeros((160, len(quads)), dtype=np.int16)
    Qm=np.zeros((160, len(quads)), dtype=np.int16)
    for p,L in pairs:
        i=pair_idx[(p,L)]
        plus=M[sf_idx[(p,L,+1)]]
        minus=M[sf_idx[(p,L,-1)]]
        Qp[i]=plus+minus
        Qm[i]=plus-minus

    C=Qp@Qm.T
    CCt=C@C.T
    signed_spec=Counter(int(round(x)) for x in np.linalg.eigvalsh((M@M.T).astype(float)))
    even_spec=Counter(int(round(x)) for x in np.linalg.eigvalsh((Qp@Qp.T).astype(float)))
    odd_spec=Counter(int(round(x)) for x in np.linalg.eigvalsh((Qm@Qm.T).astype(float)))
    coupling_spec=Counter(int(round(x)) for x in np.linalg.eigvalsh(CCt.astype(float)))
    entry_dist=Counter(int(x) for x in C.flatten())

    checks={
        "signed_BT512_spectrum": signed_spec==Counter({0:160,80:81,112:24,144:30,464:24,1296:1}),
        "even_projective_spectrum": even_spec==Counter({0:120,288:15,792:24,2592:1}),
        "odd_chiral_spectrum": odd_spec==Counter({0:40,160:81,288:15,360:24}),
        "coupling_nonzero": np.max(np.abs(C))==27,
        "coupling_entry_values": set(entry_dist)=={-9,0,27},
        "coupling_rank_24": int(np.linalg.matrix_rank(C.astype(float)))==24,
        "coupling_spectrum": coupling_spec==Counter({0:136,77760:24}),
        "coupling_row_sums_zero": Counter(int(x) for x in C.sum(axis=1))==Counter({0:160}),
        "coupling_col_sums_zero": Counter(int(x) for x in C.sum(axis=0))==Counter({0:160}),
        "rank_signed": int(np.linalg.matrix_rank(M.astype(float)))==160,
        "rank_even": int(np.linalg.matrix_rank(Qp.astype(float)))==40,
        "rank_odd": int(np.linalg.matrix_rank(Qm.astype(float)))==120,
    }

    results={
        "theorem":"BT514 Xmin Even/Odd Coupling Bridge Theorem",
        "summary":{
            "signed_faces":320,
            "antipodal_pairs":160,
            "quadrangles":len(quads),
            "rank_signed":int(np.linalg.matrix_rank(M.astype(float))),
            "rank_even_projective":int(np.linalg.matrix_rank(Qp.astype(float))),
            "rank_odd_chiral":int(np.linalg.matrix_rank(Qm.astype(float))),
            "rank_even_odd_coupling":int(np.linalg.matrix_rank(C.astype(float))),
            "all_checks_passed":all(checks.values()),
        },
        "checks":checks,
        "spectra":{
            "signed_MMt":{str(k):int(v) for k,v in sorted(signed_spec.items())},
            "even_Qplus_QplusT":{str(k):int(v) for k,v in sorted(even_spec.items())},
            "odd_Qminus_QminusT":{str(k):int(v) for k,v in sorted(odd_spec.items())},
            "coupling_CCt":{str(k):int(v) for k,v in sorted(coupling_spec.items())},
        },
        "coupling_bridge":{
            "C":"Qplus Qminus^T",
            "entry_distribution":{str(k):int(v) for k,v in sorted(entry_dist.items())},
            "row_sums":"all zero",
            "column_sums":"all zero",
            "rank":24,
            "singular_value":"72*sqrt(15)",
            "multiplicity":24,
            "reading":"even/projective and odd/chiral sectors communicate only through a 24-dimensional W33 matter sector",
        },
        "correction_to_BT513":{
            "BT513_overstrong_claim":"even and odd sectors were asserted orthogonal",
            "correct_statement":"Qplus Qminus^T is nonzero of rank 24; the split is coupled, not orthogonal",
            "what_survives":"the 81-sector remains in the odd/chiral Qminus spectrum; projective Qplus still carries 1,24,15",
        },
        "substrate_reading":{
            "40":"even/projective rank = W33 point/line count",
            "120":"odd/chiral rank and projective nullity = E8 root-pair count",
            "81":"odd/chiral protected homology multiplicity",
            "24":"rank of even-odd coupling bridge and W33 matter multiplicity",
            "72sqrt15":"single nonzero coupling singular value scale",
            "77760":"72^2*15 coupling-square eigenvalue",
        },
    }

    out=Path("data/PART_BT514_XMIN_EVEN_ODD_COUPLING_BRIDGE_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results,indent=2),encoding="utf-8")
    print(json.dumps(results,indent=2))
    return results

if __name__=="__main__":
    main()
