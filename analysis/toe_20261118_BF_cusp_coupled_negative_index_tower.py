"""Coupled BF tower: an extensive negative-index theorem in a conditional
winding branch, robust against uniformly norm-bounded arbitrarily mixed
Hermitian masses and positive kinetic deformations.

No physical corrections are computed; all conclusions inherit the
conditional M-theory mass model in the existing repo.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[1]
def mass(l):return l-2-math.sqrt(4+16*l)
def deficit(l):return -4-mass(l)
def bounds(b):
    assert 0<=b<2.25
    t=math.sqrt(36-16*b)
    return 6-b-t,6-b+t
def count(r,y,b):
    lower,upper=bounds(b)
    a=3*math.pi*r/y
    lo=int(math.floor(math.sqrt(lower/a)))+1
    hi=int(math.ceil(math.sqrt(upper/a)))-1
    assert lo>=1
    cand=[u for u in range(lo,hi+1) if lower<a*u*u<upper]
    assert all(deficit(a*u*u)>b-1e-12 for u in cand)
    return 2*len(cand),cand,[lower,upper]

def run():
    table=[]
    for budget in (0.,0.5,1.,2.,2.2,2.24):
        for y in (1000.,10000.,100000.):
            r=1.
            n,_,(low,high)=count(r,y,budget)
            asym=2*(math.sqrt(high)-math.sqrt(low))/math.sqrt(3*math.pi*r)
            table.append(dict(correction_budget=budget,height=y,
                              robust_oriented_winding_count=n,
                              BF_lambda_open_interval=[low,high],
                              predicted_count_div_sqrt_height=asym,
                              actual_count_div_sqrt_height=n/math.sqrt(y)))
        assert table[-1]["robust_oriented_winding_count"]>table[-3]["robust_oriented_winding_count"]
    # Stress the min-max theorem on finite coupled matrices. Random
    # perturbation is just a diagnostic; proof is Rayleigh subspace.
    rng=np.random.default_rng(186825)
    y=1000.;r=1.
    mode_ids=[u for u in range(-40,41) if u!=0]
    lam=[3*math.pi*r*u*u/y for u in mode_ids]
    base=np.diag([mass(x) for x in lam]+[10.]*20)
    n=base.shape[0];ident=np.eye(n)
    delta=1.2;eps=.2;budget=delta+4*eps
    predicted,good,interval=count(r,y,budget)
    good_set=set(good)
    candidates=[i for i,u in enumerate(mode_ids) if abs(u) in good_set]
    assert len(candidates)==predicted and predicted>0
    gap=min(deficit(lam[i])-budget for i in candidates)
    assert gap>0
    trials=[]
    for k in range(12):
        A=rng.normal(size=(n,n));A=(A+A.T)/2;A=A/np.linalg.norm(A,2)*delta
        B=rng.normal(size=(n,n));B=(B+B.T)/2;B=B/np.linalg.norm(B,2)*eps
        K=ident+B
        assert np.linalg.eigvalsh(K).min()>0
        computed=eigh(base+A,K,eigvals_only=True,check_finite=False)
        n_bad=int(np.count_nonzero(computed<-4+1e-10))
        assert n_bad>=predicted
        sub=(base+A+4*K)[np.ix_(candidates,candidates)]
        assert np.linalg.eigvalsh(sub).max()<=-gap+1e-9
        trials.append(dict(n_below_BF=n_bad,negative_trial_subspace_dim=predicted,
                           max_negative_subspace_eigenvalue=float(np.linalg.eigvalsh(sub).max())))
    out=dict(status="PASS",analytic=dict(
      baseline_BF_window="0<lambda<12",
      BF_deficit="sqrt(4+16lambda)-lambda-2",
      max_deficit="9/4 at lambda=15/4",
      correction_budget_c="delta+4*epsilon with norm(Delta)<=delta, norm(E)<=epsilon<1, K=I+E>0",
      robust_open_window="lambda_-(c)<lambda<lambda_+(c), lambda_pm=6-c +/- sqrt(36-16c), c<9/4",
      asymptotic_robust_modes="N_c(y,r)=[2*(sqrt(lambda_+)-sqrt(lambda_-))/sqrt(3*pi*r)] sqrt(y)+O(1), y->infinity; oriented v=0 windings",
      negative_index_theorem="The BF matrix M0+Delta+4K is negative definite on the span of all horizontal modes with unperturbed deficit>c. Courant-Fischer/Sylvester inertia yields at least that many generalized BF-unsafe eigenvalues in the full Hermitian mass/positive-kinetic system, irrespective of off-diagonal coupling. Real-field conjugation may pair +/- vectors.",
      physical_limit="Requires a UNIFORM Hilbert-space operator-norm correction bound over the growing tower, true positive K and unchanged flux/winding spectrum. These hypotheses are not established for M-theory/string corrections; the result is conditional."
      ),rows=table,finite_mixing_stress=dict(
       r=r,height=y,matrix_dimension=n,delta=delta,epsilon=eps,
       guaranteed_robust_oriented_mode_count=predicted,
       guaranteed_quadratic_form_margin=gap,
       trials=trials))
    path=ROOT/"data/toe_20261118_BF_cusp_coupled_negative_index_tower.json"
    path.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS BF robust lambda window, sqrt(y) min-max negative-index bound, 12 random globally norm-bounded coupled tests")
    for z in table:
        if z["correction_budget"] in (1.,2.2) and z["height"] in (1000.,100000.):
            print("BUDGET",z["correction_budget"],"y",z["height"],"N",z["robust_oriented_winding_count"])
    return out
if __name__=="__main__":run()
