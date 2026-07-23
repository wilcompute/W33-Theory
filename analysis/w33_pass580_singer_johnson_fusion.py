#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
import networkx as nx
import sympy as sp
from w33_pass574_singer_coherent_configuration import scheme_data,spectral_tables

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass580_singer_johnson_fusion.json'


def set_partitions(items):
    items=list(items)
    if not items:
        yield []
        return
    first=items[0]
    for rest in set_partitions(items[1:]):
        yield [[first]]+[b[:] for b in rest]
        for i in range(len(rest)):
            out=[b[:] for b in rest]
            out[i]=[first]+out[i]
            yield out


def fused_ok(p,blocks):
    # p[i,j,k] are intersection numbers. A fusion is valid iff the fused
    # coefficient is constant on every target block.
    for I in blocks:
        for J in blocks:
            for K in blocks:
                vals={sum(int(p[i,j,k]) for i in I for j in J) for k in K}
                if len(vals)!=1:return False
    return True


def fusions(p):
    # Symmetric fusions must keep the transpose pair {1,2} together.
    atoms=[(1,2),(3,),(4,),(5,),(6,),(7,),(8,)]
    out=[];seen=set()
    for part in set_partitions(range(len(atoms))):
        blocks=[(0,)]
        for cell in part:
            blocks.append(tuple(sorted(x for a in cell for x in atoms[a])))
        blocks=tuple(sorted(blocks,key=lambda b:(0 if 0 in b else 1,min(b))))
        key=tuple(sorted(tuple(sorted(b)) for b in blocks))
        if key in seen:continue
        seen.add(key)
        if fused_ok(p,blocks):out.append(blocks)
    return sorted(out,key=lambda z:(len(z),z))


def quotient_johnson(R):
    n=R.shape[0]
    G=nx.Graph();G.add_nodes_from(range(n))
    G.add_edges_from((int(i),int(j)) for i,j in zip(*np.where(R==8)) if i<j)
    blocks=sorted((tuple(sorted(c)) for c in nx.connected_components(G)),key=lambda c:c[0])
    signatures=[];sid={};Qrel=np.zeros((len(blocks),len(blocks)),dtype=np.int8)
    for a,A in enumerate(blocks):
        for b,B in enumerate(blocks):
            sig=tuple(int(np.sum(R[np.ix_(A,B)]==r)) for r in range(9))
            if sig not in sid:sid[sig]=len(sid);signatures.append(sig)
            Qrel[a,b]=sid[sig]
    vals=tuple(int(np.sum(Qrel[0]==r)) for r in range(len(signatures)))
    r_adj=next(r for r,v in enumerate(vals) if v==15)
    X=nx.Graph();X.add_nodes_from(range(56));X.add_edges_from((i,j) for i in range(56) for j in range(i+1,56) if Qrel[i,j]==r_adj)
    triples=list(itertools.combinations(range(8),3))
    J=nx.Graph();J.add_nodes_from(range(56));J.add_edges_from((i,j) for i in range(56) for j in range(i+1,56) if len(set(triples[i])&set(triples[j]))==2)
    gm=nx.algorithms.isomorphism.GraphMatcher(X,J)
    iso=gm.is_isomorphic();mapping=gm.mapping if iso else {}
    relation_intersections={}
    if iso:
        for r in range(len(signatures)):
            relation_intersections[r]=sorted({len(set(triples[mapping[i]])&set(triples[mapping[j]])) for i in range(56) for j in range(56) if Qrel[i,j]==r})
    # quotient intersection numbers
    d=len(signatures);qp=np.zeros((d,d,d),dtype=np.int16)
    for k in range(d):
        y=next(j for j in range(56) if Qrel[0,j]==k)
        for i in range(d):
            for j in range(d):qp[i,j,k]=np.sum((Qrel[0,:]==i)&(Qrel[:,y]==j))
    return blocks,signatures,Qrel,vals,iso,mapping,relation_intersections,qp


def mod_rank(A,p=1000003):
    A=np.array(A,dtype=np.int64)%p;m,n=A.shape;r=0
    for c in range(n):
        nz=np.flatnonzero(A[r:,c])
        if len(nz)==0:continue
        q=r+int(nz[0]);A[[r,q]]=A[[q,r]];iv=pow(int(A[r,c]),-1,p);A[r]=(A[r]*iv)%p
        rows=np.flatnonzero(A[:,c]);rows=rows[rows!=r]
        for i in rows:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
        if r==m:break
    return r


class ModBasis:
    def __init__(self,n,p=1000003):self.n=n;self.p=p;self.piv={};self.vecs=[];self.mats=[]
    def add(self,M):
        v=np.asarray(M,dtype=np.int64).reshape(-1)%self.p
        for q in sorted(self.piv):
            if v[q]:v=(v-v[q]*self.piv[q])%self.p
        nz=np.flatnonzero(v)
        if len(nz)==0:return False
        q=int(nz[0]);v=(v*pow(int(v[q]),-1,self.p))%self.p
        # maintain reduced pivots
        for k in list(self.piv):
            if self.piv[k][q]:self.piv[k]=(self.piv[k]-self.piv[k][q]*v)%self.p
        self.piv[q]=v;self.vecs.append(v.copy());self.mats.append(np.asarray(M,dtype=np.int64)%self.p);return True


def terwilliger_certificate(Qrel,prime=1000003):
    n=Qrel.shape[0];d=int(Qrel.max())+1
    adjacency=[(Qrel==r).astype(np.int64) for r in range(d)]
    dual=[np.diag((Qrel[0,:]==r).astype(np.int64)) for r in range(d)]
    gens=adjacency+dual
    B=ModBasis(n,prime);B.add(np.eye(n,dtype=np.int64))
    q=0
    while q<len(B.mats):
        X=B.mats[q]
        for G in gens:
            B.add((X@G)%prime)
        q+=1
    mats=B.mats;dim=len(mats)
    constraints=[]
    for G in gens:
        cols=[((M@G-G@M)%prime).reshape(-1) for M in mats]
        constraints.append(np.stack(cols,axis=1))
    C=np.vstack(constraints)
    rank=mod_rank(C,prime);center=dim-rank
    return {'prime':prime,'dimension':dim,'center_dimension':center,'generator_count':len(gens),'closure_basis_sha256':hashlib.sha256(np.stack(mats).astype(np.int64).tobytes()).hexdigest()}


def krein_table(P,Q,mult):
    n=336;d=9;K=[];nonnegative=True;real=True
    vals=[]
    for i in range(d):
        plane=[]
        for j in range(d):
            row=[]
            for k in range(d):
                x=sp.simplify(sum(Q[l,i]*Q[l,j]*P[k,l] for l in range(d))/n)
                if sp.simplify(sp.im(x))!=0:real=False
                if float(sp.N(sp.re(x),20)) < -1e-10:nonnegative=False
                row.append(str(x).replace('I','i'));vals.append(x)
            plane.append(row)
        K.append(plane)
    distinct=sorted({str(sp.simplify(x)).replace('I','i') for x in vals})
    return K,{'all_real':real,'all_nonnegative':nonnegative,'distinct_value_count':len(distinct),'distinct_values':distinct,'sha256':hashlib.sha256(json.dumps(K,separators=(',',':')).encode()).hexdigest()}


def payload():
    GL,H,objects,idx,transport,invs,base,orbits,R,p=scheme_data()
    P,Q,mult,val,ch,orth,pq,Ps,Qs=spectral_tables(p)
    fs=fusions(p)
    blocks,sigs,Qrel,qval,iso,mapping,relints,qp=quotient_johnson(R)
    K,kmeta=krein_table(P,Q,mult)
    terw=terwilliger_certificate(Qrel)
    constant_rows=[r for r in range(9) if str(P[r,8])=='5']
    within_rows=[r for r in range(9) if str(P[r,8])=='-1']
    fusion_records=[]
    for f in fs:
        fusion_records.append({'blocks':[list(b) for b in f],'rank':len(f),'valencies':[sum(val[i] for i in b) for b in f]})
    checks={
      'scheme_order336_rank9':len(objects)==336 and len(orbits)==9,
      'krein_all_real_nonnegative':kmeta['all_real'] and kmeta['all_nonnegative'],
      'exact_four_symmetric_fusions':len(fs)==4,
      'imprimitivity_relation_is_56_K6':len(blocks)==56 and all(len(b)==6 for b in blocks),
      'quotient_rank4':len(sigs)==4,
      'quotient_valencies_J83':sorted(qval)==[1,10,15,30],
      'quotient_graph_is_J83':iso,
      'quotient_relations_are_intersection_sizes':sorted(tuple(v) for v in relints.values())==[(0,),(1,),(2,),(3,)],
      'block_constant_constituents_1_7_20_28':tuple(mult[r] for r in constant_rows)==(1,7,20,28),
      'within_block_constituents_45_45_56_64_70':tuple(mult[r] for r in within_rows)==(45,45,56,64,70),
      'block_constant_dimension56':sum(mult[r] for r in constant_rows)==56,
      'within_block_dimension280':sum(mult[r] for r in within_rows)==280,
      'terwilliger_dimension38':terw['dimension']==38,
      'terwilliger_center_dimension6':terw['center_dimension']==6,
    }
    return {
      'schema':'w33.pass580.singer_johnson_fusion.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'scheme':{'order':336,'rank':9,'krein':kmeta,'krein_parameters':K},
      'fusions':fusion_records,
      'imprimitivity':{
        'relation':8,'components':56,'component_size':6,'component_graph':'56 disjoint K6',
        'quotient_order':56,'quotient_rank':4,'quotient_valencies':qval,'block_pair_signatures':[list(s) for s in sigs],
        'identification':'Johnson association scheme J(8,3)','relation_to_triple_intersection':{str(k):v for k,v in relints.items()},
        'quotient_intersection_numbers':qp.tolist(),
      },
      'representation_restriction':{
        'block_constant_rows':constant_rows,'block_constant_dimensions':[mult[r] for r in constant_rows],
        'within_block_rows':within_rows,'within_block_dimensions':[mult[r] for r in within_rows],
        'interpretation':'The canonical 56-dimensional quotient is 1+7+20+28, the A8 permutation module on 3-subsets. The 280-dimensional fibre complement is 45+conj(45)+56+64+70.'
      },
      'terwilliger_J83_basepoint':terw,
      'checks':checks,
      'boundary':'The Johnson quotient and all fusion/Krein data are exact. The Terwilliger dimensions are exact modulo the stated prime, whose rank can only underestimate characteristic-zero rank; the matching center calculation is a certificate at that prime. No objectwise identification of the 280-dimensional complement with an E6 module is asserted.'
    }


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 580 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'fusions':len(p['fusions']),'terwilliger':p['terwilliger_J83_basepoint']['dimension']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
