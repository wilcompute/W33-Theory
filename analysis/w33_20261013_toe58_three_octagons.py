"""TOE58 front 1: three genuinely coupled octagons on the native W33 deck.

Full 1385 native plaquettes are NOT quantized; this is an exact
3-loop subspace with finite integer flux cutoff and Gauss-charge sectors.
"""
from pathlib import Path
from itertools import product
import numpy as np,json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
ed,volt,lk,octs,comm,*_=prep()
B=np.rint(gradient(ed,volt,np.zeros(3)).real).astype(int)
P=np.rint(np.asarray([cycle_row(x,ed,volt,lk,np.zeros(3)).real for x in octs+comm])).astype(int)
c0,c1=P[0],P[186]
assert np.array_equal((np.array([c0,c1])@B),np.zeros((2,80),int))
options=[]
for j,c in enumerate(P[:len(octs)]):
 if j in (0,186):continue
 if (c@c0!=0 and c@c1!=0 and np.linalg.matrix_rank([c0,c1,c])==3):
  options.append((-min(abs(int(c@c0)),abs(int(c@c1))),j))
assert options
_,j=min(options);C=np.vstack([c0,c1,P[j]])
G=C@C.T
assert np.linalg.matrix_rank(G)==3 and np.count_nonzero(G-np.diag(np.diag(G)))>=4
assert np.max(abs(C@B))==0
q=np.zeros(160,dtype=int);q[0]=1
def calc(g,N,charged):
 sites=list(product(range(-N,N+1),repeat=3));pos={s:i for i,s in enumerate(sites)}
 f=np.asarray(sites,dtype=int)@C+(q if charged else 0)
 charge=f@B;assert np.max(abs(charge-charge[0]))==0
 H=np.diag(g*g*np.sum(f*f,axis=1)/2+3/(g*g))
 for a,s in enumerate(sites):
  for k in range(3):
   t=list(s);t[k]+=1;t=tuple(t)
   if t in pos:H[a,pos[t]]=H[pos[t],a]=-1/(2*g*g)
 ev,V=np.linalg.eigh(H)
 boundary=np.array([max(abs(x) for x in s)==N for s in sites])
 return dict(N=N,dimension=len(sites),ground=float(ev[0]),gap=float(ev[1]-ev[0]),
             boundary_probability=float(boundary@(V[:,0]**2)),
             Gauss_endpoint_charges=charge[0].tolist())
samples={}
for g in (.7,1.1):
 for end in (False,True):
  key=f"{g}_{'open' if end else 'neutral'}"
  samples[key]=[calc(g,N,end) for N in (1,2,3)]
  assert samples[key][-1]["ground"]<=samples[key][-2]["ground"]+1e-10
  assert abs(samples[key][-1]["ground"]-samples[key][-2]["ground"])<.15
  assert samples[key][-1]["gap"]>0
  assert sorted(x for x in samples[key][-1]["Gauss_endpoint_charges"] if x)==([-1,1] if end else [])
out={"status":"PASS_TOE58_NATIVE_THREE_INTERACTING_OCTAGONS","native_rows":1385,"native_sites":80,"native_links":160,
"octagon_indices":[0,186,j],"signed_Gram":G.tolist(),"samples":samples,
"proof":"Each selected signed octagon c has B.T c=0; n=m1 c1+m2 c2+m3 c3+q has fixed B.T n for all integer coefficients. The non-diagonal rank3 Gram contains exact mixed electric flux interactions. Truncated Wilson shifts in each coefficient preserve Gauss, while increasing cutoff gives variational nonincreasing ground energies.",
"limitation":"The three-loop subspace omits the other 1382 plaquette shift operators, all dynamical charged matter and unbounded flux; finite truncation differences do not certify full W33 QED, continuum, confinement or an experimental energy scale."}
(R/"data/w33_20261013_toe58_three_octagons.json").write_text(json.dumps(out,indent=2)+"\n")
print("TOE58 three-octagon",j,G.tolist(),[(k,[round(x["ground"],6) for x in v]) for k,v in samples.items()])
