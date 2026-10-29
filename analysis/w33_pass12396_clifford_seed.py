"""Compile one Hamming CSS frame to actual H/CNOT gates, not full27-state encoder."""
from pathlib import Path
import sys,json
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from w33_20261029_klein_e8_hamming_twistor_transform import generators,hamming_code

def run():
 code=hamming_code(generators()[0]);A=np.array([[(w>>i)&1 for i in range(8)] for w in sorted(code)],int);rank=0;piv=[]
 for col in range(8):
  hits=np.flatnonzero(A[rank:,col])
  if not len(hits):continue
  j=rank+hits[0];A[[rank,j]]=A[[j,rank]]
  for i in range(len(A)):
   if i!=rank and A[i,col]:A[i]^=A[rank]
  piv.append(col);rank+=1
 assert rank==4;G=A[:4];gates=[['H',i] for i in piv]
 for row,control in zip(G,piv):
  for target in range(8):
   if target not in piv and row[target]:gates.append(['CX',control,target])
 state=np.zeros(256);state[0]=1
 for gate in gates:
  if gate[0]=='H':
   q=gate[1]
   for word in range(256):
    if word>>q&1:continue
    other=word^(1<<q);a,b=state[word],state[other];state[word]=(a+b)/np.sqrt(2);state[other]=(a-b)/np.sqrt(2)
  else:
   _,c,t=gate;new=state.copy()
   for word in range(256):new[word^((1<<t) if word>>c&1 else 0)]=state[word]
   state=new
 target=np.zeros(256);target[list(code)]=.25;assert np.max(abs(state-target))<1e-14
 return {'gates':gates,'generator':G.tolist(),'amplitude_error':float(np.max(abs(state-target))),'scope':'Exact Clifford preparation of one Hamming CSS seed. Full coherent Fourier-frame encoder, auxiliary qutrit controls and E6 extension remain separate.'}
if __name__=='__main__':
 r=run();Path(__file__).resolve().parents[1].joinpath('data/w33_pass12396_clifford_seed.json').write_text(json.dumps(r,indent=2)+'\n');print(len(r['gates']),r['amplitude_error'])
