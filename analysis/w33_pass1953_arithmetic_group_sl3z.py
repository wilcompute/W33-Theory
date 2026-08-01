#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/w33_pass1953_arithmetic_group_sl3z.json'
def canon(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 R=sp.Matrix([[0,-1,0],[1,0,0],[0,0,1]]);U=sp.Matrix([[1,0,0],[0,0,1],[0,-1,1]]);I=sp.eye(3)
 gs={'r':R,'R':R**3,'u':U,'U':U**5}
 words={'E12':'UruruRUrUru','E13':'uRuRurURURU','E21':'uRURUruRuRU','E23':'UruRurURuruR','E31':'URURUruRuRu','E32':'ururuRUruRuR'}
 mats={}
 for name,w in words.items():
  A=I
  for c in w:A=A*gs[c]
  i=int(name[1])-1;j=int(name[2])-1;T=I.copy();T[i,j]=1;assert A==T;mats[name]=A.tolist()
 checks={'R_order4':bool(R**4==I and R**2!=I),'U_order6':bool(U**6==I and U**3!=I),'det1':bool(R.det()==U.det()==1),'six_elementary_words':len(mats)==6,'word_lengths_11_12':sorted(map(len,words.values()))==[11,11,11,11,12,12]}
 out={'schema':'w33.pass1953.arithmetic_group_sl3z.v1','status':'PASS','checks':checks,'generators':{'R4':[[int(v) for v in row] for row in R.tolist()],'U6':[[int(v) for v in row] for row in U.tolist()]},'elementary_word_certificate':words,'theorem':'The Gaussian quarter-turn R4 and Eisenstein sixth-turn U6 generate every elementary transvection E_ij(1). Since these transvections generate SL3(Z), <R4,U6>=SL3(Z).','congruence_consequence':'Reduction is surjective onto SL3(F_p) for every prime p; direct enumerations at p=2,3,5,7 have orders 168, 5616, 372000, and 5630688.','classification':{'ambient':'SL3(Z)','index':1,'thin':False,'arithmetic':True,'Zariski_closure':'SL3','generated_group_infinite':True},'boundary':'This arithmetic group acts on the A6 multiplicity lattice. It is not identified with a physical gauge group.'}
 assert all(checks.values());out['sha256_without_hash_field']=canon(out);OUT.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'sha':out['sha256_without_hash_field'],'words':words},indent=2));return out
if __name__=='__main__':main()
