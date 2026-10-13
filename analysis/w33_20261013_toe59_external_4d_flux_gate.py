"""TOE59 four-dimensional chirality prerequisite: explicit quantized U1 F wedge F.

External 4-torus witness, NOT a native W33 overlap index! A native
spatial 2-complex without a specified fourth direction/4-cells cannot
supply this witness without extra structure.
"""
from pathlib import Path
import itertools,json,numpy as np
R=Path(__file__).resolve().parents[1];L=3
sites=list(itertools.product(range(L),repeat=4));ids={x:i for i,x in enumerate(sites)}
n=len(sites)
def neighbour(x,d):
 y=list(x);y[d]=(y[d]+1)%L;return tuple(y)
def field(flux_pairs):
 U=np.ones((n,4),dtype=complex)
 for (a,b),flux in flux_pairs.items():
  phi=2*np.pi*flux/(L*L)
  for i,x in enumerate(sites):
   U[i,a]*=np.exp(-1j*phi*x[b])
   if x[b]==L-1:U[i,b]*=np.exp(1j*2*np.pi*flux*x[a]/L)
 return U
def curvature(U):
 F={}
 for a in range(4):
  for b in range(a+1,4):
   v=[]
   for i,x in enumerate(sites):
    xa=ids[neighbour(x,a)];xb=ids[neighbour(x,b)]
    z=U[i,a]*U[xa,b]*np.conj(U[xb,a])*np.conj(U[i,b])
    v.append(float(np.angle(z)))
   F[(a,b)]=np.array(v)
 return F
def top_charge(F):
 # Q=1/(4pi²) Σ(F01 F23 - F02 F13 + F03 F12).
 return float(np.dot(F[(0,1)],F[(2,3)])/ (4*np.pi**2)
              -np.dot(F[(0,2)],F[(1,3)])/(4*np.pi**2)
              +np.dot(F[(0,3)],F[(1,2)])/(4*np.pi**2))
records=[]
for flux in ({(0,1):1,(2,3):1},{(0,1):1},{(0,2):1,(1,3):1},
             {(0,3):1,(1,2):1}):
 U=field(flux);F=curvature(U);q=top_charge(F)
 expected=flux.get((0,1),0)*flux.get((2,3),0)-flux.get((0,2),0)*flux.get((1,3),0)+flux.get((0,3),0)*flux.get((1,2),0)
 assert abs(q-expected)<1e-12,(flux,q,expected)
 for k,values in F.items():
  target=2*np.pi*flux.get(k,0)/(L*L)
  assert np.max(abs(values-target))<1e-12,(k,target,values.max())
 rng=np.random.default_rng(59022);chi=rng.uniform(-np.pi,np.pi,size=n)
 W=U.copy()
 for i,x in enumerate(sites):
  for a in range(4):W[i,a]*=np.exp(1j*(chi[i]-chi[ids[neighbour(x,a)]]))
 cov=max(np.max(abs(F[k]-curvature(W)[k])) for k in F)
 assert cov<1e-12
 records.append(dict(flux_pairs={str(k):v for k,v in flux.items()},
    U1_second_Chern_character=round(q),actual_numeric_Q=q,
    gauge_curvature_residual=float(cov),max_abs_plaquette_angle=float(max(max(abs(x)) for x in F.values()))))
out={"status":"PASS_TOE59_EXTERNAL_4D_U1_TOPOLOGICAL_INDEX_PREREQUISITE",
"external_torus_length":L,"sites":n,"records":records,
"exact_theorem":"On a 4-torus with integer first Chern fluxes n_ij, the spin-Dirac U1 ch2 index integral is Q=n01*n23-n02*n13+n03*n12. A smooth 3D time-independent spatial connection with no mixed temporal flux n0i has Q=0. Nonzero Q requires both spatial and temporal first-Chern flux sectors. The periodic link fields here encode bundle transition functions at boundaries and have small admissible principal plaquette angles 2pi/9.",
"native_boundary":"W33 native 80-site spatial two-complex has only B:C0→C1 and P:C1→C2; no supplied temporal links, 4-cells or C4 cup product. The explicit 4D torus in this script is AN EXTERNAL CONTROL and has not been coupled to W33 320-band overlap. This shows what topological data the existing static index0 test lacks, not a W33 chiral discovery.",
"prior_art":"Abelian flux bundles/T4 Dirac index and overlap admissibility are standard; external4D overlap controls already exist in W33 passes11423–11427/11582. This is a transparent flux calculation only, not an executed nonzero overlap index."}
(R/"data/w33_20261013_toe59_external_4d_flux_gate.json").write_text(json.dumps(out,indent=2)+"\n")
print("TOE59 external 4D control",[(r["flux_pairs"],r["actual_numeric_Q"]) for r in records])
