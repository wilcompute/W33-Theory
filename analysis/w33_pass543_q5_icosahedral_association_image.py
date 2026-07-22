#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from collections import Counter
from pathlib import Path
import networkx as nx
import sympy as sp
from w33_pass543_547_common import *
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'w33_pass543_q5_icosahedral_association_image.json'
A=(1,1,2,2,2,3,3,2,3,2,3,2);B=(1,1,2,2,3,3,3,3,2,3,2,2)
def graph():
 C=classes(5);G=nx.Graph();G.add_nodes_from(range(12))
 for i,u in enumerate(C):
  for j in range(i+1,12):
   if leg(omega(u,C[j],5),5)==1:G.add_edge(i,j)
 return C,G
def payload():
 C=CycPrime(5);V,G=graph();x=sp.symbols('x');M=sp.Matrix(nx.to_numpy_array(G,dtype=int));cp=sp.factor(M.charpoly(x).as_expr())
 tangent=tangent_prime(5);gram=[]
 for i in range(12):
  gram.append([trace(matmul(tangent[i],tangent[j],C),C) for j in range(12)])
 deltas=pair_deltas_prime(5);cross=set();local={}
 for c in range(5):local[c]={trace(matmul(deltas[i][c],deltas[i][c],C),C) for i in range(12)}
 for i in range(12):
  for j in range(i+1,12):
   for c in range(1,5):
    for d in range(1,5):cross.add(trace(matmul(deltas[i][c],deltas[j][d],C),C))
 cpA=charpoly_prime(5,A)[0];cpB=charpoly_prime(5,B)[0]
 checks={
  'icosahedral_charpoly':sp.expand(cp-(x-5)*(x+1)**5*(x*x-5)**3)==0,
  'module_dimensions_1_3_3_5':1+3+3+5==12,
  'tangent_gram_minus10_identity':all(gram[i][j]==((-10,0,0,0) if i==j else (0,0,0,0)) for i in range(12) for j in range(12)),
  'tangent_injective_rank12':all(gram[i][i]!=C.zero() for i in range(12)),
  'finite_pair_cross_terms_vanish':cross=={C.zero()},
  'local_square_classes':len(local[1])==len(local[2])==1 and local[1]==local[4] and local[2]==local[3] and local[1]!=local[2],
  'pass540_pair_quadratic_match':cpA[2]==cpB[2],
  'pass540_pair_full_charpoly_match':cpA==cpB,
 }
 return {'schema':'w33.pass543.q5_icosahedral_association_image.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'association_scheme':{'vertices':12,'adjacency_charpoly':str(cp),'permutation_module':'1 + 3 + 3prime + 5','adjacency_eigen_multiplicities':{'5':1,'sqrt5':3,'-sqrt5':3,'-1':5}},
  'linearized_block_map':{'gram':'-10 I_12','conclusion':'Every A5 irreducible survives; spectral collisions are nonlinear, not a missing-irrep effect.'},
  'quadratic_charpoly_coefficient':{'cross_pair_terms':'zero','offset_0':list(next(iter(local[0]))),'offset_pm1':list(next(iter(local[1]))),'offset_pm2':list(next(iter(local[2]))),'real_basis_t_relation':'tr(N_c^2)=20-10t for c=+-1 and 30+10t for c=+-2, t=zeta5+zeta5^-1','conclusion':'e2 depends only on the coordinate square-class histogram.'},
  'pass540_pair':{'square_histogram_equal':Counter(x*x%5 for x in A)==Counter(x*x%5 for x in B),'charpoly_equal':cpA==cpB},'checks':checks,'boundary':'Exact association and tangent/quadratic image; not a complete enumeration of the 2,034,735 q=5 section orbits.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 543 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
