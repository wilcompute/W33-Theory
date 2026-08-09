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

At support 20 the labelled subset spectrum is divided by two, because S and its
complement encode the same codeword and have equal weight. A separate canonical-
certificate pairing of support-20 representatives checks the stronger orbit
count: 9,442,244 lower-shell PGSp orbits plus 1,347,360 support-20 complement
classes = 10,789,604 codeword orbits. The numerical weight enumerator is accepted
only when its coefficients sum to 2^39. This file does not pre-claim that run.
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
FULL_CODEWORD_ORBITS=10789604
SUPPORT20_COMPLEMENT_ORBITS=1347360


def load_nauty():
    try:import pynauty
    except ImportError as e:
        raise SystemExit('Pass 4546 requires pynauty: python -m pip install pynauty') from e
    return pynauty


def marked_graph(pynauty,A,mask):
    adj={i:set(int(j) for j in range(40) if A[i,j]) for i in range(40)}
    S={i for i in range(40) if (mask>>i)&1};adj[40]=set(S)
    for i in S:adj[i].add(40)
    return pynauty.Graph(number_of_vertices=41,directed=False,adjacency_dict=adj,
                         vertex_coloring=[set(range(40)),{40}])


def certificate(pynauty,A,mask):return pynauty.certificate(marked_graph(pynauty,A,mask))


def stabilizer_order(pynauty,A,mask):
    ans=pynauty.autgrp(marked_graph(pynauty,A,mask));mant,exp=ans[1],ans[2]
    order=int(round(float(mant)*(10**int(exp))));assert AUT_ORDER%order==0,(mask,order);return order


def weight_stats(mask,A,apset):
    S=[i for i in range(40) if (mask>>i)&1];m=len(S)
    e=sum(int(A[i,j]) for i,j in itertools.combinations(S,2))
    p3=sum(1 for t in itertools.combinations(S,3)
           if sum(int(A[i,j]) for i,j in itertools.combinations(t,2))==2)
    c4=sum(1 for q in itertools.combinations(S,4) if sum(1<<i for i in q) in apset)
    return {'m':m,'e':e,'p3':p3,'c4':c4,
            'weight':162*m-12*math.comb(m,2)-42*e+12*p3-8*c4}


def read_shell(path):
    if not path.exists():return None
    return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]


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
    rows.sort(key=lambda r:(r['weight'],r['mask']));return rows


def shell_spectrum(rows):
    c=Counter()
    for r in rows:c[int(r['weight'])]+=int(r['orbit_size'])
    return c


def support20_complement_classes(pynauty,A,rows):
    cert_to_mask={certificate(pynauty,A,int(r['mask'])):int(r['mask']) for r in rows}
    assert len(cert_to_mask)==EXPECTED[20]
    seen=set();classes=0;full=(1<<40)-1
    for c,m in cert_to_mask.items():
        if c in seen:continue
        cc=certificate(pynauty,A,full^m);assert cc in cert_to_mask
        seen.add(c);seen.add(cc);classes+=1
    assert classes==SUPPORT20_COMPLEMENT_ORBITS,(classes,SUPPORT20_COMPLEMENT_ORBITS)
    return classes


def assemble_complete(pynauty,A,directory):
    full=Counter();support_spectra={};pgsp_orbits=0
    for m in range(21):
        rows=read_shell(directory/f'support_{m:02d}.jsonl');assert rows is not None and len(rows)==EXPECTED[m]
        c=shell_spectrum(rows);support_spectra[str(m)]={str(k):v for k,v in sorted(c.items())};pgsp_orbits+=len(rows)
        if m<20:full.update(c)
        else:
            assert all(v%2==0 for v in c.values())
            for w,v in c.items():full[w]+=v//2
    assert sum(full.values())==2**39
    rows20=read_shell(directory/'support_20.jsonl');assert rows20 is not None
    middle_classes=support20_complement_classes(pynauty,A,rows20)
    lower=sum(EXPECTED[:20]);assert lower+middle_classes==FULL_CODEWORD_ORBITS
    return full,support_spectra,pgsp_orbits,middle_classes


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

    if args.through==20:
        full,spectra,pgsp,middle=assemble_complete(pynauty,A,args.directory)
        summary={'pass':4546,'status':'COMPLETE_NUMERICAL_ENUMERATOR','through_support':20,
                 'PGSp_subset_orbits_support_0_to_20':pgsp,'support20_complement_orbits':middle,
                 'codeword_orbits_mod_PGSp_and_complement':FULL_CODEWORD_ORBITS,
                 'weight_enumerator':{str(k):v for k,v in sorted(full.items())},
                 'codeword_count_checksum':sum(full.values()),'support_spectra':spectra}
    else:
        observed=0;spectra={}
        for m in range(args.through+1):
            rows=read_shell(args.directory/f'support_{m:02d}.jsonl');assert rows is not None
            observed+=len(rows);spectra[str(m)]={str(k):v for k,v in sorted(shell_spectrum(rows).items())}
        summary={'pass':4546,'status':'RESUMABLE_FRONTIER','through_support':args.through,
                 'observed_orbits_through_support':observed,
                 'expected_orbits_through_support':sum(EXPECTED[:args.through+1]),
                 'full_target_codeword_orbits_mod_group_and_complement':FULL_CODEWORD_ORBITS,
                 'support_spectra':spectra,
                 'boundary':'The engine is exact and resumable; the complete numerical enumerator is not claimed until --through 20 emits the 2^39 checksum.'}
    (args.directory/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in {'support_spectra','weight_enumerator'}},indent=2));return 0

if __name__=='__main__':raise SystemExit(main())
