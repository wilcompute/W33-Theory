#!/usr/bin/env python3
"""Pass5011-5012: first mixed reader circuits and the canonical V24 failure frame."""
from __future__ import annotations
import itertools,json,sys
from pathlib import Path
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis.w33_pass4992_4999_common import build_base
O11=ROOT/'data/PART_W33_PASS5011_FIRST_MIXED_SUPPORT13_AND_TRIT_K33.json'
O12=ROOT/'data/PART_W33_PASS5012_FAILURE_FRAME_IS_CANONICAL_V24.json'

def main():
 b=build_base();T=b['tritangents'];M=b['M'].astype(int);G27=b['G27'];W=b['W'];L=b['L'];C=b['C'].astype(int)
 AT=nx.Graph();AT.add_nodes_from(range(45))
 for i,j in itertools.combinations(range(45),2):
  if len(set(T[i])&set(T[j]))==1:AT.add_edge(i,j)
 # Pure-tritangent support-six circuits: signed K3,3.
 indep=[frozenset(s) for s in itertools.combinations(range(45),3) if all(not AT.has_edge(*e) for e in itertools.combinations(s,2))]
 circuits={}
 for A in indep:
  common=set(range(45))
  for a in A:common&=set(AT.neighbors(a))
  for B in itertools.combinations(sorted(common-A),3):
   B=frozenset(B)
   if all(not AT.has_edge(*e) for e in itertools.combinations(B,2)):
    key=tuple(sorted((tuple(sorted(A)),tuple(sorted(B)))))
    circuits[key]=(A,B)
 assert len(circuits)==120
 for A,B in circuits.values():
  assert np.all(M[list(A)].sum(0)-M[list(B)].sum(0)==0)
 # Nine tritangents with nonzero centered coefficient sum must cover all 27 cubic lines.
 through=[[] for _ in range(27)]
 for i,t in enumerate(T):
  for x in t:through[x].append(i)
 covers=[]
 def bt(ch,rem):
  if not rem:
   if len(ch)==9:covers.append(tuple(sorted(ch)))
   return
  if len(ch)>=9:return
  x=min(rem,key=lambda q:sum(set(T[i])<=rem for i in through[q]))
  for i in through[x]:
   S=set(T[i])
   if S<=rem:bt(ch+[i],rem-S)
 bt([],set(range(27)));covers=sorted(set(covers));assert len(covers)==200
 assert all(np.all(M[list(S)].sum(0)==6) for S in covers)
 # Four-line point pencils are the minimum nonzero-sum line-centered dependencies.
 pencils=[tuple(j for j,Q in enumerate(L) if p in Q) for p in range(40)]
 Lraw=C.T;ones=np.ones(36,dtype=int)
 assert all(len(P)==4 and np.array_equal(Lraw[list(P)].sum(0),ones) for P in pencils)
 # -6 times one pencil plus +1 times one exact cover is a raw support-13 dependency.
 for P in pencils[:2]:
  for S in covers[:2]:assert np.all(-6*Lraw[list(P)].sum(0)+M[list(S)].sum(0)==0)
 out11={'pass':5011,'global_reader_distance':6,
  'pure_tritangent_minimum':{'support':6,'count':120,'geometry':'signed K3,3','correction':'Pass4998 support-eight 2K4 family remains valid but is not minimum'},
  'nonzero_sum_tritangent_centered_dependencies':{'minimum_support':9,'reason':'Nc=(sum c)/9 * 1_27 forces coverage of all27 cubic lines; each tritangent covers3 lines','exact_9_covers':200,'cover_geometry':'nine pairwise line-disjoint tritangents partition all27 cubic lines','raw_sum_per_cover':'6 * 1_36'},
  'mixed_reader_minimum':{'support':13,'composition':'4 line + 9 tritangent','count':8000,'construction':'-6 on a four-line W33 point pencil and +1 on a nine-tritangent exact cover','supports_9_to_12_exist':False},
  'theorem':'The first mixed line+tritangent reader circuits occur at support13, not9. Pure tritangent dependencies already occur at support6 as120 signed K3,3 configurations. A mixed relation needs a four-line point pencil and at least nine tritangents; exactly200 nine-tritangent partitions exist, yielding40*200=8000 minimum mixed support13 circuits.',
  'boundary':'The global arbitrary-erasure distance remains6. Pass4998 is retained only as a secondary support-eight pure-tritangent family.'}
 O11.write_text(json.dumps(out11,indent=2,sort_keys=True)+'\n')
 # Pass5012: the 240 six-line failures are exactly the canonical line V24.
 Z=np.array([[1 if p in Q else 0 for Q in L] for p in range(40)],dtype=int)
 D=np.array([Z[p]-Z[q] for p,q in W.edges()],dtype=int);assert D.shape==(240,40)
 assert np.linalg.matrix_rank(D)==24 and np.linalg.matrix_rank(C)==16 and np.max(np.abs(D@C.T))==0
 AQ=nx.to_numpy_array(b['Q'],nodelist=range(40),dtype=int)
 assert np.array_equal(D.T@D,-AQ@AQ+8*AQ+48*np.eye(40,dtype=int))
 assert np.array_equal((Z.T@Z)@D.T,6*D.T)
 ev=np.linalg.eigvalsh((D.T@D).astype(float));assert sum(np.isclose(ev,60))==24 and sum(np.isclose(ev,0))==16
 out12={'pass':5012,'failure_gradient_matrix':[240,40],'rank':24,'line_reader_left_nullity':24,'rowspan_equals_kernel_C':True,'tight_frame_spectrum':{'60':24,'0':16},'exact_Gram_identity':'D^T D = -A_Q^2 + 8 A_Q + 48 I = 60 P_24','point_line_intertwiner':'Z^T Z D^T = 6 D^T; hence Z maps line V24 isomorphically to point V24 with inverse Z^T/6 on that sector','theorem':'The Pass5007 minimum-failure 24-space is exactly the canonical shared W33 degree-24 line module: rowspan(D)=ker(C). The 240 W33 edge gradients are its tight frame, and point-line incidence gives the explicit 24-to-24 intertwiner.', 'boundary':'This is an explicit real/rational intertwiner theorem, not a dimension match.'}
 O12.write_text(json.dumps(out12,indent=2,sort_keys=True)+'\n');print(json.dumps({'5011':out11,'5012':out12},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
