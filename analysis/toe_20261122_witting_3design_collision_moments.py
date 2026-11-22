"""Verify known 40-ray Witting projective 3-design and extract 2nd/3rd
spectral moments from two- and three-copy same-POVM-label collisions.

This is a computational application of PRIOR ART (e.g. Hoggar's 40-point
CP3 3-design), NOT the discovery of the 3-design. Contrasts against 20
five-MUB ququart rays: MUB is a 2-design but not a 3-design.
"""
from __future__ import annotations
import itertools,json,sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_relational_reference_pareto as base
OUT=ROOT/"data/toe_20261122_witting_3design_collision_moments.json"

def get_MUB():
    I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
    pauli=[np.kron(a,b) for a,b in itertools.product((I,X,Y,Z),repeat=2)][1:]
    lines=[pair for pair in itertools.combinations(range(15),3)
           if all(np.max(abs(pauli[i]@pauli[j]-pauli[j]@pauli[i]))<1e-12
                  for i,j in itertools.combinations(pair,2))]
    cover=next(comb for comb in itertools.combinations(lines,5)
               if len(set(itertools.chain.from_iterable(comb)))==15)
    rays=[]
    for a,b,_ in cover:
        _,U=eigh(pauli[a]+2*pauli[b])
        rays.extend(U.T)
    return np.asarray(rays)

def symmetric3():
    S=np.zeros((64,64))
    for perm in itertools.permutations(range(3)):
        for i,j,k in itertools.product(range(4),repeat=3):
            z=(i,j,k);w=tuple(z[h] for h in perm)
            S[16*w[0]+4*w[1]+w[2],16*i+4*j+k]+=1/6
    assert abs(np.trace(S)-20)<1e-12
    assert np.max(abs(S@S-S))<1e-12
    return S

def frame(rays):
    P=np.einsum("ai,aj->aij",rays,rays.conj())
    overlap=abs(rays.conj()@rays.T)**2
    moment=sum(np.kron(np.kron(p,p),p)for p in P)
    gap=np.max(abs(moment-len(rays)/20*symmetric3()))
    return P,float(gap),{str(k):float(np.mean(overlap**k))for k in (2,3,4)}

def main():
    rays,_,_,_=base.geometry()
    mubs=get_MUB()
    W,werr,wfp=frame(rays)
    M,merr,mfp=frame(mubs)
    assert len(W)==40 and len(M)==20
    assert werr<1e-11 and merr>.1
    assert abs(wfp["2"]-.1)<1e-12 and abs(wfp["3"]-.05)<1e-12
    assert wfp["4"]>1/35+1e-3
    assert abs(mfp["2"]-.1)<1e-12 and abs(mfp["3"]-.0625)<1e-12
    rng=np.random.default_rng(20261122)
    z=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
    rho=z@z.conj().T;rho/=np.trace(rho)
    prob=np.einsum("aij,ji->a",W,rho).real/10
    s2=float((prob**2).sum());s3=float((prob**3).sum())
    m2=float(np.trace(rho@rho).real);m3=float(np.trace(rho@rho@rho).real)
    assert abs(s2-(1+m2)/50)<1e-11
    assert abs(s3-(1+3*m2+2*m3)/3000)<1e-11
    # Check independent pure input states, including one five-MUB ray.
    trials=[]
    for key,x in (("Witting_basis_ray",rays[5]),("MUB_basis_ray",mubs[0])):
        for name,P in (("Witting40",W),("fiveMUB20",M)):
            p=np.einsum("aij,i,j->a",P,x.conj(),x).real*(4/len(P))
            a=float((p*p).sum());b=float((p*p*p).sum())
            if name=="Witting40":
                assert abs(a-.04)<1e-11 and abs(b-.002)<1e-11
            trials.append({"input":key,"POVM":name,"pair_collision":a,"triple_collision":b})
    result={"status":"PASS","date":"2026-11-22",
       "Witting40_3design_max_matrix_error":werr,
       "fiveMUB20_not_3design_max_matrix_error":merr,
       "Witting_frame_potentials":wfp,"fiveMUB_frame_potentials":mfp,
       "known_prior_art":"40-point CP3 3-design known in design theory; e.g. Hoggar, cited by Designs Related Through Projective and Hopf Maps (2025)",
       "exact_third_moment":"sum_{40} P_i^tensor3 = 2 Pi_symmetric3 (rank20)",
       "not_4design":True,
       "independent_input_collision_tests":trials,
       "random_mixed_rho_Tr_rho2":m2,"random_mixed_rho_Tr_rho3":m3,
       "random_mixed_rho_C2":s2,"random_mixed_rho_C3":s3,
       "purity_reconstruction_identity":"C2=(1+Tr(rho^2))/50; C3=(1+3Tr(rho^2)+2Tr(rho^3))/3000",
       "limits":"Requires 2 or 3 independent identical preparations and stable calibrated 40-outcome POVM; no uniqueness of Witting among projective 3-designs; no physical measurement or TOE."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PASS known Witting 3-design: unbiased spectral moments from collisions")
    return result
if __name__=="__main__":main()
