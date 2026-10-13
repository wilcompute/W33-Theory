"""TOE57: native two-plaquette compact U(1) quantum flux benchmark.

Explicit 2D independent integer-loop flux truncations, shared-link coupling,
Gauss sectors and truncation convergence; not the full 1385-plaquette theory.
"""
from pathlib import Path
import json,sys
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
ed,volts,lookup,octs,comm,*_=prep()
B=np.rint(gradient(ed,volts,np.zeros(3)).real).astype(int)
P=np.rint(np.asarray([cycle_row(w,ed,volts,lookup,np.zeros(3)) for w in octs+comm]).real).astype(int)
assert P.shape==(1385,160) and np.max(abs(P@B))==0
# Select two independent native plaquettes sharing edges, with nonzero
# overlap so the electric Hamiltonian has genuine mixed m1 m2 coupling.
c0=P[0]
choices=[(abs(int(c0@r)),j) for j,r in enumerate(P[1:len(octs)],1)
         if abs(int(c0@r))>0 and not np.array_equal(abs(c0),abs(r))]
overlap,j=max(choices);c1=P[j]
c=np.array([c0,c1])
assert abs(int(c0@c1))>0 and np.linalg.matrix_rank(c)==2
assert np.max(abs(c@B))==0
gram=c@c.T
assert gram[0,1]!=0
q=np.zeros(160,dtype=int);q[int(np.argmax(abs(c0)))] = 1
def sector(g,N,endpoint=False):
    ms=list(range(-N,N+1)); states=[(a,b) for a in ms for b in ms]
    pos={st:i for i,st in enumerate(states)}
    ref=q if endpoint else np.zeros(160,dtype=int)
    flux=np.asarray([ref+a*c0+b*c1 for a,b in states],dtype=int)
    ends=flux@B
    assert np.max(abs(ends-ends[0]))==0
    assert np.count_nonzero(ends[0]) == (2 if endpoint else 0)
    H=np.diag(g*g*np.sum(flux**2,axis=1)/2+2/(g*g))
    # Each single native Wilson cosine changes one loop-flux number
    # at fixed Gauss charge. Hard truncation at the edge of each axis.
    for idx,(a,b) in enumerate(states):
        for axis in (0,1):
            other=(a+1,b) if axis==0 else (a,b+1)
            if other in pos:
                H[idx,pos[other]]=H[pos[other],idx]=-1/(2*g*g)
    vals,vecs=np.linalg.eigh(H)
    v=vecs[:,0]; probs=v*v
    m1=np.array([a for a,b in states]);m2=np.array([b for a,b in states])
    boundary_probability=float(sum(probs[t] for t,(a,b) in enumerate(states)
                                   if abs(a)==N or abs(b)==N))
    return {"ground_energy":float(vals[0]),"gap":float(vals[1]-vals[0]),
       "ground_flux_mean":[float(np.dot(probs,m1)),float(np.dot(probs,m2))],
       "ground_flux_cross_cov":float(np.dot(probs,m1*m2)-np.dot(probs,m1)*np.dot(probs,m2)),
       "boundary_probability":boundary_probability,
       "gauss_charges":ends[0].tolist(),
       "level_count":len(states),
       "matrix_hermitian_residual":float(np.max(abs(H-H.T)))}
outs={}
for g in (0.4,0.8,1.2):
 for end in (False,True):
    records=[sector(g,N,end) for N in (2,3,4,5)]
    outs[f"{g}_{'open' if end else 'vacuum'}"]=records
    assert abs(records[-1]["ground_energy"]-records[-2]["ground_energy"])<.09
    assert records[-1]["boundary_probability"] < .02
# Shared edges generate c0.c1 m1 m2 term unlike disconnected rotors.
# Direct prove neutral flux energy mixed finite difference = g²(c0.c1).
g=.8
def e(a,b):return .5*g*g*np.linalg.norm(a*c0+b*c1)**2
cross=e(1,1)-e(1,0)-e(0,1)+e(0,0)
assert abs(cross-g*g*int(c0@c1))<1e-13
# Dynamic coupling cannot be determined by Gauss alone: all g have exact charge sectors.
out={"status":"PASS_TOE57_TWO_INTERACTING_NATIVE_COMPACT_PLAQUETTES",
"native_dimensions":{"vertices":80,"links":160,"plaquettes":1385},
"selected_native_plaquette_rows":[0,j],
"two_loop_signed_gram":gram.tolist(),"electric_cross_coupling_at_g_0p8":cross,
"electric_cross_coupling_exact_theorem":"For n=m0 c0 +m1 c1+q, electric g²||n||²/2 contains g² (c0.c1) m0 m1; because selected native plaquettes overlap, the two flux rotors are not independent.",
"basis":"Two integer loop coefficients m0,m1 in [-N,N] and fixed flux q=0 or a single oriented open edge; each finite block preserves B.T n charge exactly.",
"truncated_sectors":outs,
"limits":"Only two of 1385 native plaquettes and at most 121 flux states/sector. Remaining plaquette shifts break closure of this Hilbert truncation. No full native gauge+matter quantum dynamics, continuum EFT, measured confinement/string tension or universal coupling.",
"prior_art":"Kogut-Susskind Hamiltonian compact electric flux basis is established 1975; contribution is exact W33 shared-plaquette coupled block and numerical truncation check."}
(R/"data/w33_20261013_toe57_two_plaquette_quantum.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"chosen":j,"gram":gram.tolist(),"energies":{k:v[-1]["ground_energy"] for k,v in outs.items()}}))
