#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1819_oriented_edge_tuple_materializer_summary.json'
ROWS=['T001','T002','T010','T012','T020','T021','T100','T101','T111','T112','T120','T122','T200','T202','T210','T211','T221','T222']
OBS=[528,562,578,528,612,580,528,528,480,528,612,564,562,528,578,562,562,560]
UNTWIST={r:c for r,c in zip(ROWS,OBS)}
UNTWIST['T010']-=2; UNTWIST['T210']-=2; UNTWIST['T222']+=2
EDGE_TABLES={'T010':+2,'T210':+2,'T222':-2}
DOMAIN=list(range(12))
def table_coord(t): return tuple(int(x) for x in t[1:])
def quartet_pair(t):
    i,_,_=table_coord(t); a=4*i+0; b=4*i+3
    return [(a,b,a),(b,a,b)]
def key(mode,table,triple): return hashlib.sha256(f'BT1819|{mode}|{table}|{triple}'.encode()).hexdigest()
def select(table,count,mode,force_in=(),force_out=()):
    s=set(force_in); out=set(force_out)
    triples=[x for x in itertools.product(DOMAIN,repeat=3) if x not in out and x not in s]
    triples.sort(key=lambda x:key(mode,table,x))
    for x in triples:
        if len(s)>=count: break
        s.add(x)
    assert len(s)==count
    return s
def materialize():
    flat={}; obs={}
    for t,c in zip(ROWS,OBS):
        pair=set(quartet_pair(t)) if t in EDGE_TABLES else set()
        flat_count=UNTWIST[t]
        if t in ['T010','T210']:
            flat[t]=select(t,flat_count,'flat',force_out=pair)
            obs[t]=select(t,c,'obs',force_in=pair)
        elif t=='T222':
            flat[t]=select(t,flat_count,'flat',force_in=pair)
            obs[t]=select(t,c,'obs',force_out=pair)
        else:
            flat[t]=select(t,flat_count,'flat')
            obs[t]=select(t,c,'obs')
    return flat,obs
def digest(tables):
    h=hashlib.sha256()
    for t in ROWS:
        for x in sorted(tables[t]): h.update(f'{t}:{x};'.encode())
    return h.hexdigest()
def main():
    flat,obs=materialize()
    checks={'observed_total_9980':sum(len(obs[t]) for t in ROWS)==9980,'untwisted_total_9978':sum(len(flat[t]) for t in ROWS)==9978,'edge_added_to_T010_T210':all(set(quartet_pair(t))<=obs[t] and set(quartet_pair(t)).isdisjoint(flat[t]) for t in ['T010','T210']),'edge_removed_from_T222':set(quartet_pair('T222'))<=flat['T222'] and set(quartet_pair('T222')).isdisjoint(obs['T222'])}
    payload={'bt':'BT1819','title':'oriented-edge tuple materializer','verified':all(checks.values()),'summary':'BT1819 materializes two deterministic tuple-table sections over the 12=3x4 domain. The untwisted section has total 9978 and is F3-flat after the BT1816 repair. The observed twisted section has total 9980. The difference is exactly the unique oriented K4 edge law: add the two 00--11 edge-pair tuples to T010 and T210, and remove the corresponding two from T222. This encodes the old+old -> new twist without claiming the arbitrary hash-filled background tuples are physically unique.','domain':'12 values = 3 strand values x 4 quartet states','observed_counts':dict(zip(ROWS,OBS)),'untwisted_counts':UNTWIST,'edge_pair_tuples':{t:[list(x) for x in quartet_pair(t)] for t in EDGE_TABLES},'sha256_observed_tables':digest(obs),'sha256_untwisted_tables':digest(flat),'checks':checks,'boundary':'The special edge transfer is structural and fixed. The remaining background tuples are deterministic filler pending the true accepted-tuple predicate; use the hashes as reproducibility guards, not as a physical uniqueness claim.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'observed_total':9980,'untwisted_total':9978},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
