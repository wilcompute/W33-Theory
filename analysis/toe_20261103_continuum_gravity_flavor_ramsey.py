#!/usr/bin/env python3
"""Four independent TOE falsifiers: metric-graph refinement, GR bracket,
E6 minimal flavor spurions, and phase-sensitive pi-flux triangle Ramsey.

All finite mathematical/control results. Not a derived continuum, observed
particle spectrum, nonlinear Einstein theory, or implemented hardware.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter
import json,math,importlib.util
import numpy as np
import sympy as sy
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261103_continuum_gravity_flavor_ramsey.json"
spec=importlib.util.spec_from_file_location("base",ROOT/"analysis"/"2026_11_03_optimal_5load_apartment_hamiltonian.py")
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)

def graph_subdivision(D,L):
    edges=[tuple(int(i) for i in np.flatnonzero(abs(D[:,e]))) for e in range(160)]
    n=80+160*(L-1);rows=[];cols=[];values=[]
    for e,(a,b) in enumerate(edges):
        chain=[a]+[80+e*(L-1)+t for t in range(L-1)]+[b]
        for u,v in zip(chain,chain[1:]):
            rows.extend([u,v,u,v]);cols.extend([u,v,v,u]);values.extend([1,1,-1,-1])
    A=coo_matrix((values,(rows,cols)),shape=(n,n)).tocsr()
    assert len(edges)*L==160*L and np.max(abs(A@np.ones(n)))==0
    return A

def continuum(D):
    results=[]
    for L in (1,2,3,4,6,8,16,32):
        lap=graph_subdivision(D,L)
        eig=np.sort(eigsh(lap,k=9,sigma=1e-6,which="LM",
                           return_eigenvectors=False,tol=1e-10))
        assert abs(eig[0])<1e-8 and eig[1]>0
        n=lap.shape[0];e=160*L;rank=e-n+1
        assert rank==81
        results.append(dict(subdivision_length=L,vertices=n,edges=e,betti1=rank,
             spectral_gap=float(eig[1]),rescaled_gap=float(eig[1]*L*L)))
    predicted=math.acos(math.sqrt(6)/4)**2
    assert abs(results[-1]["rescaled_gap"]-predicted)<0.07
    n=64;circ=2-2*np.cos(2*np.pi*np.arange(n)/n)
    fiber=np.array([0]+[10]*24+[16]*15)
    def dspec(eig,t):
        w=np.exp(-t*eig)
        return float(2*t*(eig@w)/sum(w))
    imported4=[dict(t=t,product_spectral_dimension=4*dspec(circ,t)+dspec(fiber,t),
                    one_factor=dspec(circ,t),w33_internal=dspec(fiber,t))
               for t in (4.,8.,16.,64.)]
    assert 4.<imported4[-1]["product_spectral_dimension"]<4.02
    return dict(base_betti=81,subdivision=results,
       metric_graph_predicted_first_eigenvalue=predicted,
       first_eigenvalue_formula="arccos(sqrt(6)/4)^2 for Kirchhoff metric graph with 160 unit edges",
       continuum_dimension="Weyl/spectral dimension one on finite compact metric graph, not four",
       imposed_4torus_times_W33_heat=imported4,
       boundary="Taking Cartesian fourth power inserts 4D by hand; subdivision alone preserves 81 topological cycles and gives a one-dimensional metric graph.")

def gravity(D,B):
    out=None
    for i in range(81):
        ci=B[:,i]
        for j in range(i+1,81):
            cj=B[:,j]
            r=int(np.count_nonzero((ci!=0)&(cj!=0)))
            s=int(ci@cj)
            if r==1 and s:
                x=ci;p=cj
                raw=int((ci@x)*(ci@(np.abs(cj)*p))-(cj@x)*(cj@(np.abs(ci)*p)))
                assert raw==s*(8-r) and raw in (-7,7)
                assert not np.any(D@p)
                out=dict(cycle_pair=[i,j],overlap=r,signed_intersection=s,
                    poisson_bracket_at_gauss_zero=raw,Gauss_zero=True,
                    analytic_general_identity="{hi,hj}|x=ci,p=cj = (ci.cj)*(8-|supp(ci) intersection supp(cj)|)",
                    boundary="Closure into Gauss alone fails for these toy local gauge-invariant constraints; GR hypersurface deformation algebra not modeled.")
                break
        if out:break
    assert out
    return out

def flavor():
    Yu=sy.diag(1,2,4)
    Yd=sy.Matrix([[1,1,sy.I],[1,2,1],[sy.I,1,3]])
    Hup=Yu*Yu.conjugate().T
    Hdown=Yd*Yd.conjugate().T
    comm=Hup*Hdown-Hdown*Hup
    cp=sy.im(sy.trace(comm*comm*comm))
    assert cp==-97200
    # Proportional matrices imply identical left eigenvectors and zero CKM mixing
    prop=(3*Yu)*(3*Yu).conjugate().T
    assert Hup*prop-prop*Hup==sy.zeros(3)
    assert sum(1 for i in range(3) for j in range(3) if (Hup*prop-prop*Hup)[i,j])==0
    assert Yd==Yd.T
    return dict(decomposition="27=16_1+10_-2+1_4, SU5: (10+5bar+1)+(5+5bar)+(1)",
        one_27_contains_one_SU5_chiral_generation_plus_vectorlike_5_5bar=True,
        single_flavor_spurion_proportional_Yu_Yd_CP_invariant=0,
        second_independent_symmetric_spurion_Yu=[[str(z) for z in row] for row in Yu.tolist()],
        second_independent_symmetric_spurion_Yd=[[str(z) for z in row] for row in Yd.tolist()],
        exact_two_spurion_CP_trace=str(cp),
        theorem="If Yu=aY and Yd=bY, [Hu,Hd]=0 and CKM=I modulo degeneracies/rephasings; a second independent spurion can produce nonzero CP-odd commutator.",
        boundary="Two arbitrary spurions show mathematical possibility, not natural Yukawa coefficients, measured masses, nor selection of chirality. Established E6 models already use two symmetric Yukawa matrices.")

def hardware():
    J=1.0
    hp=np.array([[0,1,1],[1,0,1],[1,1,0]],dtype=float)
    hm=hp.copy();hm[0,1]=-1;hm[1,0]=-1
    gauge=np.diag([1,1,-1])
    assert np.array_equal(hm,-gauge@hp@gauge)
    assert np.allclose(np.linalg.eigvalsh(hp),[-1,-1,2])
    assert np.allclose(np.linalg.eigvalsh(hm),[-2,1,1])
    times=(0.2,0.4,0.8)
    rows=[]
    for t in times:
        up=expm(-1j*t*hp);um=expm(-1j*t*hm)
        probability_gap=float(np.max(abs(abs(up)**2-abs(um)**2)))
        contrast=float((up[0,0]-um[0,0]).imag)
        assert probability_gap<1e-13 and contrast>0
        rows.append(dict(t=t,site_probability_max_gap=probability_gap,
                         coherent_reference_imaginary_contrast=contrast,
                         leading_2t3_over_3=2*t**3/3))
    eps=sy.symbols("eps0:3",real=True)
    ep=sy.diag(*eps)
    spp=sy.Matrix(hp.astype(int))+ep
    spm=sy.Matrix(hm.astype(int))+ep
    cubic=sy.expand((spp**3)[0,0]-(spm**3)[0,0])
    assert cubic==4
    rng=np.random.default_rng(53)
    samples=[]
    for _ in range(500):
        j=1+0.02*rng.normal(size=3)
        e=rng.normal(scale=0.05,size=3)
        h=np.array([[e[0],j[0],j[2]],[j[0],e[1],j[1]],[j[2],j[1],e[2]]])
        hpi=h.copy();hpi[0,1]*=-1;hpi[1,0]*=-1
        samples.append(float((expm(-0.4j*h)[0,0]-expm(-0.4j*hpi)[0,0]).imag))
    s=np.array(samples)
    return dict(plaquette_sites=3,onsite_flux_zero_eigenvalues=[-1,-1,2],
        onsite_flux_pi_eigenvalues=[-2,1,1],
        site_probabilities_cannot_discriminate_flux_for_equal_real_hoppings=True,
        Ramsey_reference_phase_contrast=rows,
        cubed_return_matrix_difference_exact=str(cubic),
        robust_perturbation_sample_size=500,onsite_disorder_sigma=0.05,
        hopping_disorder_sigma=0.02,matched_disorder_pair=True,
        contrast_mean=float(s.mean()),contrast_std=float(s.std()),
        contrast_minimum=float(s.min()),contrast_positive_fraction=float((s>0).mean()),
        uniform_amplitude_loss_factor_at_gamma_0_1_t_0_4=math.exp(-0.1*.4/2),
        experiment="Ramsey measure Im<0|exp(-i H t)|0> relative to idle phase reference for +/- triangle flux; compare at identical static disorder.",
        boundary="Simulated 3-site tight binding and non-Hermitian uniform loss factor; not a calibrated optical pulse sequence or physical demonstration.")

def main():
    D,C,_=base.build()
    pick,_=base.choose(C,seed=33)
    B=C[:,pick]
    out=dict(status="PASS_FOUR_INDEPENDENT_TOE_FALSIFIERS",
             continuum=continuum(D),gravity=gravity(D,B),flavor=flavor(),hardware=hardware(),
             physical_boundary="Finite mathematics and controlled toy simulations only; no completed TOE.")
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(out["status"],out["continuum"]["subdivision"][-1]["rescaled_gap"],
          out["gravity"]["poisson_bracket_at_gauss_zero"],
          out["flavor"]["exact_two_spurion_CP_trace"],out["hardware"]["contrast_minimum"],flush=True)
    return out

if __name__=="__main__":main()
