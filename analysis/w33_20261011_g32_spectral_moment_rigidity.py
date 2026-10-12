#!/usr/bin/env python3
"""G32 symmetric-power commutants and vector-mass moment rigidity.

On the normalized Vinberg Cartan of the SU(9)+84 model, the vector mass
power sums p_k=sum_i e_i^k are G32-invariant Hermitian forms of bidegree
(k,k).  The actual four-dimensional Cartan representation has commutant
dimension 1 on Sym^k for k=1,2,3 and dimension 2 on Sym^4.  Hence p1,p2,p3
are radial while p4 is the first possible angular spectral invariant.

The commutant dimensions are certified numerically with a large singular-value
gap using the committed G32 generators; the moment constants are calibrated
from the exact Witting spectrum 0^24,(1/3)^54,1^2 and replayed numerically.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261011_g32_spectral_moment_rigidity.json"
sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass11879_11883_e8_higgs_siegel_modulus as P
import w33_pass11884_11886_one_loop_trinification as CW

def sha(rel):
    return hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()

def generators():
    W=P.W
    F=np.array([[W**(a*b) for b in range(3)] for a in range(3)])/np.sqrt(3)
    D=np.diag([1,1,W]); I3=np.eye(3)
    raw=(np.kron(F,I3),np.kron(I3,F),np.kron(D,I3),np.kron(I3,D),
         np.diag([W**(a*b) for a,b in P.C2]))
    return [P.cartan_action(g) for g in raw]

def sym_basis(k):
    words=list(itertools.product(range(4),repeat=k))
    groups={}
    for i,w in enumerate(words):
        occ=tuple(w.count(j) for j in range(4))
        groups.setdefault(occ,[]).append(i)
    B=np.zeros((4**k,len(groups)),complex)
    for j,(_,inds) in enumerate(sorted(groups.items())):
        B[inds,j]=1/np.sqrt(len(inds))
    return B

def kronpow(g,k):
    A=np.array([[1]],complex)
    for _ in range(k): A=np.kron(A,g)
    return A

def commutant_census():
    gs=generators(); out={}
    for k in range(1,5):
        B=sym_basis(k)
        Rs=[B.conj().T@kronpow(g,k)@B for g in gs]
        n=B.shape[1]
        A=np.vstack([np.kron(np.eye(n),R)-np.kron(R.T,np.eye(n)) for R in Rs])
        s=np.linalg.svd(A,compute_uv=False)
        tol=1e-8*s[0]
        nullity=n*n-int(np.sum(s>tol))
        nz=s[s>tol]
        out[str(k)]={
          "sym_dimension":int(n),
          "commutant_dimension":int(nullity),
          "smallest_nonzero_singular":float(nz[-1]),
          "largest_null_singular":float(s[-1]),
          "singular_gap_ratio":float(nz[-1]/max(s[-1],np.finfo(float).tiny)),
        }
    return out
def spectrum(c):
    c=np.asarray(c,complex); c=c/np.linalg.norm(c)
    return CW.vec_spectrum(c@P.H)

def moments(e,n=6):
    return [float(np.sum(e**k)) for k in range(1,n+1)]

def random_moment_replay():
    rng=np.random.default_rng(12011)
    rows=[]
    for _ in range(128):
        c=rng.normal(size=4)+1j*rng.normal(size=4)
        rows.append(moments(spectrum(c),6))
    A=np.array(rows)
    return {
      "trials":len(rows),
      "p1_range":[float(A[:,0].min()),float(A[:,0].max())],
      "p2_range":[float(A[:,1].min()),float(A[:,1].max())],
      "p3_range":[float(A[:,2].min()),float(A[:,2].max())],
      "p4_range":[float(A[:,3].min()),float(A[:,3].max())],
      "p5_range":[float(A[:,4].min()),float(A[:,4].max())],
      "p6_range":[float(A[:,5].min()),float(A[:,5].max())],
      "max_rigid_residual":float(max(np.max(abs(A[:,0]-20)),
                                      np.max(abs(A[:,1]-8)),
                                      np.max(abs(A[:,2]-4)))),
    }

def witting_calibration():
    e=spectrum([1,0,0,0])
    vals=np.round(e,12)
    uniq=[]
    for x in vals:
        if not uniq or abs(x-uniq[-1][0])>1e-10: uniq.append([float(x),1])
        else: uniq[-1][1]+=1
    m=moments(e,6)
    return {"spectrum":uniq,"moments":m,
            "exact_first_three":["20","8","4"],
            "exact_p4":"8/3"}

def large_soft_replay():
    # h_s(e)=(s+e)^2 log(s+e)-e^2 log e.
    # Angular expansion after summing:
    # const(s,p1,p2) - F + p3/(3s)-p4/(12s^2)
    # +p5/(30s^3)-p6/(60s^4)+...
    rng=np.random.default_rng(12012)
    c=rng.normal(size=4)+1j*rng.normal(size=4); e=spectrum(c)
    p=moments(e,8); F=CW.F_of(e)
    def exact(s):
        a=e+s
        base=np.zeros_like(e); mask=e>1e-14
        base[mask]=e[mask]**2*np.log(e[mask])
        return float(np.sum(a*a*np.log(a)-base))
    # Strip terms depending only on p1,p2 and s.
    def angularized(s):
        total=exact(s)
        radial=80*s*s*np.log(s)+s*(2*np.log(s)+1)*p[0]+(np.log(s)+1.5)*p[1]
        return total-radial
    rows=[]
    for s in (10.,30.,100.):
        approx=-F+p[2]/(3*s)-p[3]/(12*s*s)+p[4]/(30*s**3)-p[5]/(60*s**4)
        rows.append({"s":s,"exact_angularized":angularized(s),"series_through_s^-4":float(approx),
                     "error":float(angularized(s)-approx)})
    return {
      "formula":"H_s = radial(s,p1,p2) - F + p3/(3s) - p4/(12s^2) + p5/(30s^3) - p6/(60s^4)+...",
      "first_nonradial_correction_after_minus_F":"-p4/(12 s^2), because p3=4 is radial",
      "rows":rows,
    }
def payload():
    comm=commutant_census()
    replay=random_moment_replay()
    wit=witting_calibration()
    large=large_soft_replay()
    assert [comm[str(k)]["commutant_dimension"] for k in range(1,5)]==[1,1,1,2]
    assert min(comm[str(k)]["smallest_nonzero_singular"] for k in range(1,5))>0.8
    assert replay["max_rigid_residual"]<1e-10
    assert replay["p4_range"][1]-replay["p4_range"][0]>0.1
    assert [x[1] for x in wit["spectrum"]]==[24,54,2]
    assert max(abs(wit["spectrum"][i][0]-v) for i,v in enumerate((0.0,1/3,1.0)))<1e-10
    assert max(abs(x) for x in [wit["moments"][0]-20,wit["moments"][1]-8,wit["moments"][2]-4])<1e-10
    assert max(abs(r["error"]) for r in large["rows"])<1e-5
    return {
      "schema":"w33.20261011.g32-spectral-moment-rigidity.v1",
      "status":"PASS_G32_SYMMETRIC_POWER_COMMUTANTS_FORCE_P1_P2_P3_RADIAL_P4_FIRST_ANGULAR",
      "commutants":comm,
      "moment_replay":replay,
      "witting_calibration":wit,
      "large_soft_expansion":large,
      "theorem":(
        "For the committed G32 Cartan representation, End_G(Sym^k C^4) has "
        "dimension 1 for k=1,2,3 and 2 for k=4. Therefore every invariant "
        "Hermitian form of bidegree (k,k) is radial through k=3, while one "
        "new angular invariant appears at k=4. The vector mass moments obey "
        "p1=20, p2=8, p3=4 on the unit Cartan sphere; p4 is the first varying "
        "power sum."
      ),
      "scope":(
        "The commutant dimensions use double-precision matrices for the exact "
        "committed finite-group generators but have a >0.8 singular gap. "
        "This is a numerical representation certificate, not an exact CHEVIE "
        "character-table proof."
      ),
      "external_context":(
        "The rigidity is consistent with the classical spherical-7-design "
        "property of the E8 minimal shell; the present certificate concerns "
        "the repository's actual four-dimensional G32 Cartan representation."
      ),
      "sources":{p:sha(p) for p in [
        "analysis/w33_pass11879_11883_e8_higgs_siegel_modulus.py",
        "analysis/w33_pass11884_11886_one_loop_trinification.py",
      ]},
      "checks":{
        "commutants_1_1_1_2":True,
        "large_singular_gap":True,
        "p1_20":True,"p2_8":True,"p3_4":True,
        "p4_varies":True,
        "large_soft_series_replays":True,
      }
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true")
    a=ap.parse_args();p=payload();txt=json.dumps(p,indent=2,sort_keys=True)+"\n"
    if a.check:
        if not OUT.exists() or OUT.read_text()!=txt: raise SystemExit("certificate drift")
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(txt)
    print(json.dumps({"status":p["status"],"commutants":[p["commutants"][str(k)]["commutant_dimension"] for k in range(1,5)],
                      "max_rigid_residual":p["moment_replay"]["max_rigid_residual"]}))
if __name__=="__main__":raise SystemExit(main())
