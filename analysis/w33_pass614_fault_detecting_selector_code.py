#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json,math
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass614_fault_detecting_selector_code.json'
WILSON={(0,1):56,(0,2):-84,(0,3):-168,(1,2):112,(1,3):-84,(2,3):56}
def onehot(n,i):return tuple(1 if j==i else 0 for j in range(n))
def hamming(a,b):return sum(x!=y for x,y in zip(a,b))
def edge_index():return {e:i for i,e in enumerate(itertools.combinations(range(4),2))}
def codeword(i,j):
 oid=[e for e in itertools.permutations(range(4),2)].index((i,j));return onehot(4,i)+onehot(4,j)+onehot(12,oid)
def flip(word,S):
 w=list(word)
 for i in S:w[i]^=1
 return tuple(w)
def permute_endpoint_blocks(word,p):
 out=[0]*20
 for i in range(4):out[p[i]]=word[i];out[4+p[i]]=word[4+i]
 out[8:]=word[8:]
 return tuple(out)
def payload():
 oriented=[(i,j) for i in range(4) for j in range(4) if i!=j];C={e:codeword(*e) for e in oriented};valid=set(C.values())
 distances=Counter(hamming(C[a],C[b]) for a,b in itertools.combinations(oriented,2));dmin=min(distances)
 corruptions=0;undetected=[]
 for e,w in C.items():
  for r in (1,2,3):
   for S in itertools.combinations(range(20),r):
    corruptions+=1
    if flip(w,S) in valid:undetected.append((e,S))
 correction_unique=True
 for e,w in C.items():
  ball={w}|{flip(w,(i,)) for i in range(20)}
  for f,v in C.items():
   if e<f:
    other={v}|{flip(v,(i,)) for i in range(20)}
    correction_unique &= ball.isdisjoint(other)
 perms=list(itertools.permutations(range(4)));perm_records=[];meaningful_detected=True
 for e,w in C.items():
  silent=[];detected=[]
  for p in perms:
   v=permute_endpoint_blocks(w,p)
   if v==w:silent.append(p)
   elif v not in valid:detected.append(p)
   else:meaningful_detected=False
  perm_records.append({'oriented_edge':list(e),'silent_endpoint_permutations':len(silent),'detected_endpoint_permutations':len(detected)})
 records=[]
 for i,j in oriented:
  pair=tuple(sorted((i,j)));records.append({'oriented_edge':[i,j],'codeword':list(C[(i,j)]),'source_onehot':list(C[(i,j)][:4]),'target_onehot':list(C[(i,j)][4:8]),'oriented_checksum_onehot':list(C[(i,j)][8:]),'Wilson_sum':WILSON[pair]})
 checks={'twelve_oriented_connection_codewords':len(C)==12 and len(valid)==12,'length20_constant_weight3':all(len(w)==20 and sum(w)==3 for w in valid),'minimum_distance4':dmin==4,'all_16200_weight1_2_3_faults_detected':corruptions==16200 and undetected==[],'single_bit_correction_balls_disjoint':correction_unique,'single_rail_loss_false_switch_detector_inversion_correctable':dmin>=3,'endpoint_permutation_checksum_detects_every_meaningful_move':meaningful_detected and all(r['silent_endpoint_permutations']==2 and r['detected_endpoint_permutations']==22 for r in perm_records),'Wilson_multiset_doubled_by_orientation':sorted(r['Wilson_sum'] for r in records)==sorted(2*list(WILSON.values())),'improves_original_weight2_distance2_to4':min(hamming(tuple(1 if k in e else 0 for k in range(4)),tuple(1 if k in f else 0 for k in range(4))) for e,f in itertools.combinations(WILSON,2))==2}
 return {'schema':'w33.pass614.fault_detecting_selector_code.v1','status':'PASS' if all(checks.values()) else 'FAIL','code':{'name':'oriented tetrahedral edge checksum code','length':20,'size':12,'constant_weight':3,'minimum_Hamming_distance':dmin,'distance_histogram':dict(sorted(distances.items())),'layout':'4 source one-hot rails + 4 target one-hot rails + 12 oriented-edge checksum rails','records':records},'fault_contract':{'detected':'every corruption of Hamming weight 1, 2, or 3','corrected':'every single-bit rail loss, false activation, or detector inversion','exhaustive_faults_checked':corruptions,'endpoint_permutation_test':perm_records,'silent_permutations':'identity and exchange of the two inactive endpoint labels; both leave the selected oriented edge physically unchanged'},'theorem':'The four-rail selector admits a 20-channel constant-weight-three upgrade with 12 oriented codewords and minimum distance four. It detects every one-, two-, and three-bit corruption, corrects every single-bit fault, and uses an independent twelve-way oriented checksum to detect every endpoint-rail permutation that changes the selected oriented transporter.','checks':checks,'boundary':'A fully correlated relabeling that permutes source, target, and checksum banks consistently maps one valid codeword to another and cannot be detected without an external absolute rail reference. This is an information-theoretic gauge ambiguity, not a coding defect.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 614 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'code':'[20,12,4]_constant_weight3'}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
