"""TOE68: 3^4 periodic U(1) Landau-flux overlap index POSITIVE CONTROL.

Uses the standard 4D Wilson-Dirac Hermitian kernel; this is deliberately
NOT a W33-derived four-dimensional lattice or constructed physical family.
"""
from pathlib import Path
import sys,json,itertools,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
P1=np.array([[0,1],[1,0]],complex)
P2=np.array([[0,-1j],[1j,0]],complex)
P3=np.diag([1.,-1.]).astype(complex)
I=np.eye(2,dtype=complex)
Z=np.zeros((2,2),complex)
GAMMA=[np.block([[Z,1j*s],[-1j*s,Z]]) for s in (P1,P2,P3)]
GAMMA.append(np.block([[Z,I],[I,Z]]))
G5=np.diag([1.,1.,-1.,-1.])
assert all(np.allclose(GAMMA[u]@GAMMA[v]+GAMMA[v]@GAMMA[u],
             (2 if u==v else 0)*np.eye(4)) for u in range(4) for v in range(4))
assert all(np.allclose(G5@g+g@G5,np.zeros((4,4))) for g in GAMMA)

def index(m,n,L=(3,3,3,3),wilson_mass=1.):
    sites=list(itertools.product(*map(range,L)))
    sid={x:j for j,x in enumerate(sites)}
    links=np.ones((len(sites),4),complex)
    for k,x in enumerate(sites):
        for a,b,charge in ((0,1,m),(2,3,n)):
            links[k,a]=np.exp(-2j*np.pi*charge*x[b]/(L[a]*L[b]))
            if x[b]==L[b]-1:
                links[k,b]=np.exp(2j*np.pi*charge*x[a]/L[a])
    H=np.zeros((len(sites)*4,len(sites)*4),complex)
    maxplaquetteerror=0.
    for k,x in enumerate(sites):
        H[4*k:4*k+4,4*k:4*k+4]=(4-wilson_mass)*G5
        for u in range(4):
            y=list(x);y[u]=(y[u]+1)%L[u];j=sid[tuple(y)]
            H[4*k:4*k+4,4*j:4*j+4]+=-.5*G5@(np.eye(4)-GAMMA[u])*links[k,u]
            H[4*j:4*j+4,4*k:4*k+4]+=-.5*G5@(np.eye(4)+GAMMA[u])*links[k,u].conjugate()
        for a in range(4):
            for b in range(a+1,4):
                xa=list(x);xb=list(x)
                xa[a]=(xa[a]+1)%L[a];xb[b]=(xb[b]+1)%L[b]
                pl=links[k,a]*links[sid[tuple(xa)],b]*np.conj(links[sid[tuple(xb)],a])*np.conj(links[k,b])
                angle=2*np.pi*m/9 if (a,b)==(0,1) else 2*np.pi*n/9 if (a,b)==(2,3) else 0.
                maxplaquetteerror=max(maxplaquetteerror,abs(pl-np.exp(1j*angle)))
    assert maxplaquetteerror<1e-12
    assert np.max(abs(H-H.conj().T))<1e-12
    ev=np.linalg.eigvalsh(H)
    plus=int(sum(ev>0));minus=int(sum(ev<0))
    assert min(abs(ev))>.1
    return {"m":m,"n":n,"overlap_index":(minus-plus)//2,
            "minimum_hermitian_kernel_gap":float(min(abs(ev))),
            "positive_kernel_eigenvalues":plus,"negative_kernel_eigenvalues":minus,
            "max_exact_flux_plaquette_deviation":float(maxplaquetteerror),
            "topological_charge_mn":m*n}

def certificate():
    runs=[index(m,n) for m,n in ((0,0),(1,0),(0,1),(1,1),(1,-1))]
    assert [r["overlap_index"] for r in runs]==[0,0,0,1,-1]
    charge=[1,5,-7,-8,9]
    assert sum(charge)==0 and sum(q**3 for q in charge)==0
    assert all(-q not in charge for q in charge)
    return {
       "status":"PASS_TOE68_NONNATIVE_4D_OVERLAP_POSITIVE_CONTROL",
       "lattice_lengths":[3,3,3,3],"matrix_dimension":324,
       "Wilson_mass":1.0,"two_independent_flux_plaquette_magnitudes":"2*pi/9",
       "overlap_runs":runs,
       "known_anomaly_free_U1_Weyl_charges":charge,
       "mixed_U1_gravity_anomaly":sum(charge),
       "cubic_U1_anomaly":sum(q**3 for q in charge),
       "sum_twisted_continuum_indices_for_mn1":sum(q*q for q in charge),
       "theorem":"The U(1) flux backgrounds have exactly the displayed quantized Wilson plaquettes and geometric topological product charge m*n.",
       "numerical":"The real Hermitian Wilson spectral signatures yield integer overlap indices matching (0,0,0,+1,-1), separated by nonzero spectral gaps; these are numerical sign-count certificates not interval-certified eigenspectra.",
       "scope":"Conventional non-W33 T4 overlap positive control only. The standard five-charge chiral anomaly-free example is known prior art and not derived from W33. No native 4D W33 chiral index, local Weyl measure, or physical Standard Model."}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe68_overlap_control.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],[q["overlap_index"] for q in c["overlap_runs"]])
