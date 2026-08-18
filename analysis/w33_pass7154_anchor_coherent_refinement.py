#!/usr/bin/env python3
"""Pass7154 addendum: coherent-refinement diagnostics for all eight 512-state anchor conflict graphs.

This does not pretend that a low-order WL/coherent signature is a full maximum-independent-set
certificate. It freezes exact combinatorial data that can feed Delsarte/SDP work: stable equitable
vertex cells, quotient matrices, pair common-neighbor signatures, and numerical inertia anchors.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
import w33_pass7130_7137_structural_attack as p
import w33_pass7138_7145_c2_normalform_matrix_quotient as q

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7154_ANCHOR_COHERENT_REFINEMENT.json'
TYPES=[(1,1,2),(1,1,3),(1,1,4),(1,1,5),(1,2,3),(1,2,4),(1,3,4),(1,3,5)]
STATES=[(1,a,b,c) for a in range(1,9) for b in range(1,9) for c in range(1,9)]

def rank2(r): return 1 if r[3]==p.gm(r[1],r[2]) else 2

def graph(rep):
    Gi=p.invmat9(q.canonical_anchor_G(rep)); n=512
    nbr=[set() for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            if q.pair_value9(STATES[i],Gi,STATES[j])==0:
                nbr[i].add(j);nbr[j].add(i)
    return nbr

def stable_vertex_colors(nbr):
    n=len(nbr)
    # Start from exact matrix-rank + degree data.
    sig=[(rank2(STATES[i]),len(nbr[i])) for i in range(n)]
    while True:
        ids={s:k for k,s in enumerate(sorted(set(sig),key=repr))}
        col=[ids[s] for s in sig]; m=max(col)+1
        ns=[]
        for i in range(n):
            cnt=[0]*m
            for j in nbr[i]:cnt[col[j]]+=1
            ns.append((col[i],tuple(cnt)))
        ids2={s:k for k,s in enumerate(sorted(set(ns),key=repr))}; new=[ids2[s] for s in ns]
        if new==col:return col
        sig=ns

def quotient(nbr,col):
    cells=defaultdict(list)
    for i,c in enumerate(col):cells[c].append(i)
    keys=sorted(cells); Q=[]
    for a in keys:
        i=cells[a][0]; row=[]
        for b in keys:row.append(len(nbr[i]&set(cells[b])))
        # equitable check
        for ii in cells[a]:
            assert [len(nbr[ii]&set(cells[b])) for b in keys]==row
        Q.append(row)
    return [len(cells[k]) for k in keys],Q

def pair_signature_hist(nbr,col):
    hist=Counter(); n=len(nbr)
    for i in range(n):
        for j in range(i,n):
            adj=int(i!=j and j in nbr[i]); common=len(nbr[i]&nbr[j]) if i!=j else len(nbr[i])
            key=(col[i],col[j],adj,common)
            # unordered canonical endpoint colors
            if col[i]>col[j]: key=(col[j],col[i],adj,common)
            hist[key]+=1
    return hist

def main():
    rows={}
    for rep in TYPES:
        nbr=graph(rep); n=512
        col=stable_vertex_colors(nbr); sizes,Q=quotient(nbr,col)
        A=np.zeros((n,n),dtype=float)
        for i in range(n):
            for j in nbr[i]:A[i,j]=1.0
        ev=np.linalg.eigvalsh(A)
        pos=int((ev>1e-7).sum()); neg=int((ev<-1e-7).sum()); zero=n-pos-neg
        inertia_bound=n-max(pos,neg) # Cvetkovic upper bound on alpha
        ph=pair_signature_hist(nbr,col)
        rows[str(rep)]={
          'vertices':n,'edges':sum(map(len,nbr))//2,
          'degree_distribution':dict(sorted(Counter(map(len,nbr)).items())),
          'stable_vertex_cell_sizes':sorted(sizes),
          'stable_vertex_cell_count':len(sizes),
          'equitable_quotient_matrix':Q,
          'pair_signature_relation_count':len(ph),
          'pair_signature_class_sizes':sorted(ph.values()),
          'least_eigenvalue_numeric':round(float(ev[0]),10),
          'least_eigenvalue_multiplicity_numeric':int((abs(ev-ev[0])<1e-7).sum()),
          'inertia':{'positive':pos,'negative':neg,'zero':zero},
          'cvetkovic_alpha_upper_bound':inertia_bound,
        }
    out={
      'schema':'w33.pass7154.anchor_coherent_refinement.v1','status':'PASS',
      'boundary':'Exact graph construction, equitable refinement and common-neighbor signatures; eigenvalue/inertia fields are numerical anchors. No alpha=51 or residual-clique<=47 claim is inferred unless a separate exact certificate supplies it.',
      'cases':rows,
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
