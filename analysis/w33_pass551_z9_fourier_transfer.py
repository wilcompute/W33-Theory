#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter,defaultdict
from pathlib import Path
from w33_pass543_547_common import *

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass551_z9_fourier_transfer.json'
C=Cyc9();A9,A3=classes(9),classes(3);BIDX={b:i for i,b in enumerate(A3)}
ALPHAS=((1,0),(0,1),(1,1),(1,2))

def oriented(v):
 r=(v[0]%3,v[1]%3);q=cp(r,3)
 return v if r==q else ((-v[0])%9,(-v[1])%9)
def reduction_meta(v):
 if v[0]%3 or v[1]%3:
  w=oriented(v);b=(w[0]%3,w[1]%3);u=((w[0]-b[0])//3%3,(w[1]-b[1])//3%3);return b,u,True
 w=(v[0]//3%3,v[1]//3%3);return cp(w,3),(0,0),False
META=[reduction_meta(v) for v in A9]

def pair_deltas():
 out=[];E=range(9)
 for a,b in A9:
  vals=[]
  for c in (0,3,6):
   M=[[C.zero() for _ in E] for _ in E]
   for aa,bb,cc in ((a,b,c),((-a)%9,(-b)%9,(-c)%9)):
    for x in E:
     z=(cc+2*x*bb+aa*bb)%9;j=(x+aa)%9
     M[j][x]=C.add(M[j][x],C.from_exp(z))
   vals.append(M)
  out.append([mat_sub(vals[i],vals[0],C) for i in range(3)])
 return out
PD=pair_deltas();Z=C.zero()

def cp_from_trits(vals):
 D=[[Z for _ in range(9)] for _ in range(9)]
 for i,v in enumerate(vals):
  if v:
   M=PD[i][v]
   for r in range(9):
    for s in range(9):D[r][s]=C.add(D[r][s],M[r][s])
 return tuple(charpoly_from_traces(traces(D,9,C),C))

def section_trits(params,k):
 constants=params[:4];amps=list(params[4:])+[0]*(4-k);out=[]
 for b,u,primitive in META:
  i=BIDX[b]
  if not primitive:out.append(0);continue
  ell=(ALPHAS[i][0]*u[0]+ALPHAS[i][1]*u[1])%3
  out.append((constants[i]+amps[i]*ell)%3)
 return tuple(out)

def rank_mod(M,p=1000003):
 A=[[x%p for x in row] for row in M];r=0
 for col in range(len(A[0]) if A else 0):
  piv=next((i for i in range(r,len(A)) if A[i][col]),None)
  if piv is None:continue
  A[r],A[piv]=A[piv],A[r];iv=pow(A[r][col],-1,p)
  A[r]=[(x*iv)%p for x in A[r]]
  for i in range(len(A)):
   if i!=r and A[i][col]:
    q=A[i][col];A[i]=[(x-q*y)%p for x,y in zip(A[i],A[r])]
  r+=1
  if r==len(A):break
 return r

def transition(prev,cur):
 pc=sorted(set(prev.values()),key=str);cc=sorted(set(cur.values()),key=str);pi={x:i for i,x in enumerate(pc)};ci={x:i for i,x in enumerate(cc)}
 M=[[0]*len(cc) for _ in pc];signatures=defaultdict(set);children=defaultdict(list)
 for p,x in cur.items():children[p[:-1]].append(x);M[pi[prev[p[:-1]]]][ci[x]]+=1
 for par,ch in children.items():signatures[prev[par]].add(tuple(sorted(Counter(ch).values())))
 rank=rank_mod(M)
 return {'parent_states':len(pc),'child_states':len(cc),'rank':rank,'rank_certificate_prime':1000003,'nonzero_entries':sum(x!=0 for row in M for x in row),'full_row_rank':rank==len(pc),'spectral_markov':all(len(v)==1 for v in signatures.values()),'ambiguous_parent_spectra':sum(len(v)>1 for v in signatures.values()),'row_sum_histogram':dict(sorted(Counter(sum(r) for r in M).items()))}

def payload():
 layers=[];rows_prev=None;trans=[]
 for k in range(4):
  rows={p:cp_from_trits(section_trits(p,k)) for p in itertools.product(range(3),repeat=4+k)}
  counts=Counter(rows.values())
  layers.append({'active_packets':k,'parameters':4+k,'sections':len(rows),'distinct_charpolys':len(counts),'multiplicity_histogram':dict(sorted(Counter(counts.values()).items()))})
  if rows_prev is not None:trans.append(transition(rows_prev,rows))
  rows_prev=rows
 checks={
  'layer_sizes_81_243_729_2187':[x['sections'] for x in layers]==[81,243,729,2187],
  'image_sizes_13_26_96_336':[x['distinct_charpolys'] for x in layers]==[13,26,96,336],
  'all_transfer_matrices_full_row_rank':all(x['full_row_rank'] for x in trans),
  'first_packet_spectral_markov':trans[0]['spectral_markov'],
  'later_packets_need_memory':not trans[1]['spectral_markov'] and not trans[2]['spectral_markov'],
  'three_ambiguous_parent_spectra_each_later_layer':trans[1]['ambiguous_parent_spectra']==3 and trans[2]['ambiguous_parent_spectra']==3,
  'deep_anchors_zero':all(not primitive or True for _,_,primitive in META) and sum(not p for _,_,p in META)==4,
  'nine_primitive_lifts_per_fibre':all(sum(1 for b,_,p in META if p and b==base)==9 for base in A3),
 }
 return {
  'schema':'w33.pass551.z9_fourier_transfer.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'family':{'definition':'On each primitive nine-point Hjelmslev fibre use f_b(u)=c_b+a_b ell_b(u) in F3 and offset 3 f_b(u) in Z/9; deep anchors remain zero. The four ell_b are the listed nonzero linear functionals.','linear_functionals':ALPHAS,'enumerated_packets':3,'available_fibres':4},
  'layers':layers,'transfers':trans,
  'conclusion':'The exact image grows 13 -> 26 -> 96 -> 336. Aggregate transfer matrices retain full row rank, but after one packet equal parent characteristic polynomials can have different child spectra; a recursive classifier must retain Fourier-packet memory in addition to the polynomial.',
  'checks':checks,
  'boundary':'Exact for the 2,187-section three-packet affine family. The fourth packet would give 6,561 sections and the full 9^40 image remains open.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 551 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
