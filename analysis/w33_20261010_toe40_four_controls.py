"""TOE40: four independent W33/modular/quantum/phenomenology gates.
Fifth (native Maxwell 2-complex) has a separate repository-dependent producer.
No result below establishes a physical theory of everything.
"""
import itertools,json,sys,math
from fractions import Fraction
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261010_toe40_four_controls.json"
w=np.exp(2j*np.pi/3)
def theta(t1,t2,e):
    n=np.arange(-12,13,dtype=float)
    x=[n+a/3 for a in range(3)]
    return np.array([[np.exp(3j*np.pi*(t1*x[a][:,None]**2+2*e*x[a][:,None]*x[b][None,:]+t2*x[b][None,:]**2)).sum()
                     for b in range(3)] for a in range(3)])
def purity(A):
    rho=A@A.conj().T;rho/=np.trace(rho)
    return float(np.trace(rho@rho).real)
def orbit_purity(A):
    phases=w**np.outer(range(3),range(3))
    return sum(purity(A*phases**j) for j in range(3))/3
def modular():
    t1=.173+1.07j;t2=.286+1.29j
    A=theta(t1,t2,0);C=w**np.outer(range(3),range(3))
    err=float(np.max(abs(theta(t1,t2,1)-C*A)))
    assert err<1e-10
    p0,p1=purity(A),purity(C*A)
    assert p0>1-1e-12 and p1<p0-.05
    F=np.array([[w**(a*b) for b in range(3)] for a in range(3)])/np.sqrt(3)
    q=orbit_purity(A)
    assert abs(q-orbit_purity(C*A))<1e-12
    assert abs(q-orbit_purity(A.conj()))<1e-12
    S=float(abs(q-orbit_purity(F@A@F.T)))
    assert S>.01
    return dict(status="OBSTRUCTION",initial_purity=p0,sheared_purity=p1,
                CZ_orbit_purity=q,S_modular_generator_defect=S,
                shear_series_residual=err,CP_invariance_verified=True,
                boundary="Not a full Siegel modular invariant; no stabilised vacuum.")
def proj(x):
    t=tuple(v%3 for v in x)
    return min(t,tuple(-v%3 for v in t))
def omega(x,y):
    return (x[0]*y[2]+x[1]*y[3]-x[2]*y[0]-x[3]*y[1])%3
def chirality():
    points=sorted({proj(x) for x in itertools.product(range(3),repeat=4) if any(x)})
    assert len(points)==40
    pos={p:i for i,p in enumerate(points)}
    lines=set()
    for i,x in enumerate(points):
        for y in points[i+1:]:
            if omega(x,y):continue
            l={pos[proj([a*x[t]+b*y[t] for t in range(4)])]
                for a,b in itertools.product(range(3),repeat=2) if a or b}
            lines.add(tuple(sorted(l)))
    lines=sorted(lines);assert len(lines)==40 and all(len(l)==4 for l in lines)
    M=np.zeros((40,40),dtype=int)
    for j,line in enumerate(lines):M[list(line),j]=1
    A=np.array([[int(i!=j and omega(x,y)==0) for j,y in enumerate(points)]
                 for i,x in enumerate(points)])
    assert np.array_equal(M@M.T,4*np.eye(40,dtype=int)+A)
    vals=np.linalg.eigvalsh(M@M.T)
    assert [int(np.sum(abs(vals-a)<1e-7)) for a in (16,6,0)]==[1,24,15]
    D=np.block([[np.zeros((40,40)),M],[M.T,np.zeros((40,40))]])
    G=np.diag([1]*40+[-1]*40)
    assert np.max(abs(G@D+D@G))==0
    assert np.linalg.matrix_rank(M)==25
    return dict(status="EXACT_ZERO_INDEX",spectrum={"16":1,"6":24,"0":15},
                point_kernel=15,line_kernel=15,Dirac_index=0,
                boundary="Balanced untwisted Levi Dirac has no unpaired physical Weyl fermion.")
def ccz():
    grid=list(itertools.product(range(3),repeat=3))
    f=lambda a,b,c:a*b*c%3
    step=lambda g,i:(lambda *v:(g(*((list(v)[:i]+[(v[i]+1)%3]+list(v)[i+1:])))-g(*v))%3)
    mixed=step(step(step(f,0),1),2)
    assert {mixed(*p) for p in grid}=={1}
    for g in (lambda a,b,c:a*b,lambda a,b,c:a*a,lambda a,b,c:c,lambda a,b,c:1):
        assert {step(step(step(g,0),1),2)(*p) for p in grid}=={0}
    assert all((f((a+1)%3,b,c)-f(a,b,c))%3==b*c%3 for a,b,c in grid)
    phase=np.exp(2j*np.pi*np.array([f(*p) for p in grid])/3)
    assert np.allclose(abs(phase),1.)
    return dict(status="EXACT_NONCLIFFORD_SURROGATE",dimension=27,
                nonzero_third_mixed_difference=1,unitarity_verified=True,
                X_conjugation="qutrit CZ phase omega^(b*c)",
                depolarizing_p=.01,global_depolarizing_state_fidelity=1-26/27*.01,
                boundary="CCZ_3 is not itself the 27-variable 45-triad E6 cubic.")
def locked():
    predicted=137+Fraction(40,1111)
    codata=137.035999177;sig=2.1e-8
    sigma=abs(float(predicted)-codata)/sig
    assert sigma>200
    R={'up':.569,'down':2.77,'charged_lepton':.081}
    q={'up':.0036,'down':.019,'charged_lepton':.059}
    bound=math.sqrt(max(R.values())/min(R.values()))
    assert bound>5
    return dict(status="REJECTS_TWO_STRICT_INTERPRETATIONS",
       archived_alpha_inverse=float(predicted),CODATA2022_inverse=codata,
       uncertainty=sig,conditional_sigma_discrepancy=sigma,
       shape_ratios_from_Pass11876_rounded=R,
       minimax_multiplicative_mismatch=bound,extreme_shape_ratio=max(R.values())/min(R.values()),
       second_ratio_spread=max(q.values())/min(q.values()),
       boundary="Not a theory-derived prediction. Existing archive has competing alpha recipes; fermion values are rounded and scheme dependent.")
def run():
    v=dict(schema="w33.toe40.four_controls.v1",modular=modular(),
      chirality=chirality(),ccz=ccz(),falsifiers=locked(),
      boundary="Mathematics and negative controls only; Maxwell is separately verified from actual W33 local complex.")
    OUT.write_text(json.dumps(v,indent=2)+"\n")
    print(json.dumps(v))
    return v
if __name__=="__main__":run()
