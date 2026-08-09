#!/usr/bin/env python3
"""Pass 4546 -- resumable orbit-native engine for the full W33 apartment enumerator.

The complete [1620,39,162] numerical weight enumerator remains open until every
PGSp(4,3)+complement orbit has been accumulated. Pass 4512 reduced the task to
10,789,604 codeword orbits; Pass 4520 supplied the exact support-orbit schedule.
This script is the missing executable engine rather than another raw-subset scan.

Aut(C)=PGSp(4,3)=Aut(W33). To encode a coefficient subset S without any ambiguity
about exchanging S with its complement, adjoin a 41st marker vertex to the fixed
40-vertex dual-W33 graph. The marker is placed in its own colour cell and joined
exactly to the vertices of S. Two such 41-vertex coloured graphs are isomorphic
iff their neighbor sets S are in the same Aut(W33) orbit. Thus a pynauty
canonical certificate is an exact subset-orbit key, including at support 20.
Complement reduction is deliberately postponed until the final codeword assembly.

Orbit generation is inductive. From every representative at support m, add one
unselected vertex, canonicalize the marked graph, and retain one representative
per certificate. The exact expected shell counts from Pass 4520 are asserted.
For each representative the marked-graph automorphism group is its stabilizer
inside Aut(W33), so orbit_size=51840/|Aut(W33,S)|. The four-statistic theorem
then evaluates

  wt = 162m - 12*C(m,2) - 42e + 12p3 - 8c4.

The engine writes one JSONL checkpoint per support. A completed run is accepted
only if every shell count matches Burnside, orbit sizes sum to C(40,m), and the
support-20 complement involution reduces the grand total to 10,789,604 codeword
orbits. This file does not claim that final run has already completed.
"""
from __future__ import annotations

import argparse,itertools,json,math
from collections import Counter
from pathlib import Path

from w33_pass4495_4502_distance_prism_reconstruction import geometry

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_DIR=ROOT/'evidence'/'pass4546_orbit_enumerator'
EXPECTED=[1,1,2,5,16,48,165,571,1961,6252,18226,47911,113314,240735,460273,793280,1234880,1739041,2218732,2566830,2694464]
AUT_ORDER=51840


def load_nauty():
    try:import pynauty
    except ImportError as e:
        raise SystemExit('Pass 4546 requires pynauty: python -m pip install pynauty') from e
    return pynauty


def marked_graph(pynauty,A,mask):
    # Vertices 0..39 are W33 line vertices. Vertex 40 is a distinguished marker
    # whose neighborhood is exactly S. The singleton color fixes it absolutely.
    adj={i:set(int(j) for j in range(40) if A[i,j]) for i in range(40)}
    S={i for i in range(40) if (mask>>i)&1}
    adj[40]=set(S)
    for i in S:adj[i].add(40)
    coloring=[set(range(40)),{40}]
    return pynauty.Graph(number_of_vertices=41,directed=False,adjacency_dict=adj,vertex_coloring=coloring)


def certificate(pynauty,A,mask):
    return pynauty.certificate(marked_graph(pynauty,A,mask))


def stabilizer_order(pynauty,A,mask):
    # pynauty.autgrp returns generators, mantissa, exponent, vertex orbits, n_orbits.
    ans=pynauty.autgrp(marked_graph(pynauty,A,mask))
    mant,exp=ans[1],ans[2]
    order=int(round(float(mant)*(10**int(exp))))
    assert AUT_ORDER%order==0,(mask,order)
    return order


def weight_stats(mask,A,apset):
    S=[i for i in range(40) if (mask>>i)&1];m=len(S)
    e=sum(int(A[i,j]) for i,j in itertools.combinations(S,2))
    p3=sum(1 for t in itertools.combinations(S,3)
           if sum(int(A[i,j]) for i,j in itertools.combinations(t,2))==2)
    c4=sum(1 for q in itertools.combinations(S,4) if sum(1<<i for i in q) in apset)
    w=162*m-12*math.comb(m,2)-42*e+12*p3-8*c4
    return {'m':m,'e':e,'p3':p3,'c4':c4,'weight':w}


def read_shell(path):
    if not path.exists():return None
    rows=[]
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip():rows.append(json.loads(line))
    return rows


def write_shell(path,rows):
    tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w',encoding='utf-8') as f:
        for r in rows:f.write(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
    tmp.replace(path)


def generate_shell(pynauty,A,apset,prev,m):
    bycert={}
    for row in prev:
        base=int(row['mask'])
        for v in range(40):
            if (base>>v)&1:continue
            x=base|(1<<v);c=certificate(pynauty,A,x)
            if c not in bycert:bycert[c]=x
    assert len(bycert)==EXPECTED[m],(m,len(bycert),EXPECTED[m])
    rows=[];orbit_sum=0
    for x in bycert.values():
        stab=stabilizer_order(pynauty,A,x);orb=AUT_ORDER//stab;orbit_sum+=orb
        rows.append({'mask':x,'stabilizer_order':stab,'orbit_size':orb,**weight_stats(x,A,apset)})
    assert orbit_sum==math.comb(40,m),(m,orbit_sum,math.comb(40,m))
    rows.sort(key=lambda r:(r['weight'],r['mask']))
    return rows


def assemble(directory,max_support):
    spectra={};orbit_total=0
    for m in range(max_support+1):
        rows=read_shell(directory/f'support_{m:02d}.jsonl')
        if rows is None:break
        assert len(rows)==EXPECTED[m]
        c=Counter()
        for r in rows:c[int(r['weight'])]+=int(r['orbit_size'])
        spectra[str(m)]={str(k):v for k,v in sorted(c.items())}
        orbit_total+=len(rows)
    return spectra,orbit_total


def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--directory',type=Path,default=DEFAULT_DIR)
    ap.add_argument('--through',type=int,default=7,choices=range(0,21));args=ap.parse_args()
    pynauty=load_nauty();args.directory.mkdir(parents=True,exist_ok=True)
    pts,pidx,lines,A,apartments,apmasks,H=geometry();apset=set(apmasks)
    p0=args.directory/'support_00.jsonl'
    if not p0.exists():
        stab=stabilizer_order(pynauty,A,0);assert stab==AUT_ORDER
        write_shell(p0,[{'mask':0,'stabilizer_order':stab,'orbit_size':1,**weight_stats(0,A,apset)}])
    for m in range(1,args.through+1):
        path=args.directory/f'support_{m:02d}.jsonl'
        if path.exists():
            rows=read_shell(path);assert rows is not None and len(rows)==EXPECTED[m];continue
        prev=read_shell(args.directory/f'support_{m-1:02d}.jsonl');assert prev is not None
        rows=generate_shell(pynauty,A,apset,prev,m);write_shell(path,rows)
        print(f'support {m}: {len(rows)} orbits, labelled sum {sum(r["orbit_size"] for r in rows)}')
    spectra,norb=assemble(args.directory,args.through)
    summary={'pass':4546,'through_support':args.through,'expected_orbits_through_support':sum(EXPECTED[:args.through+1]),
             'observed_orbits_through_support':norb,'spectra_by_support':spectra,
             'full_target_codeword_orbits_mod_group_and_complement':10789604,
             'status':'SHELLS_0_TO_20_READY_FOR_COMPLEMENT_ASSEMBLY' if args.through==20 else 'RESUMABLE_FRONTIER',
             'acceptance':'At through=20, apply complement only to support-20 representatives and require grand total 10,789,604; no COMPLETE enumerator claim is valid before that checksum and coefficient accumulation.'}
    (args.directory/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='spectra_by_support'},indent=2));return 0

if __name__=='__main__':raise SystemExit(main())
