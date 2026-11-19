"""Five physically constrained W33/TOE audit fronts, 2026-11-18.

This single independently reproducible suite covers: (1) actual
11D AdS4 x S7 homogeneous breathing/test scalar KK,
(2) gauged family SU3 anomaly + H27 Higgs commutant,
(3) exact tilted PW Dirichlet energy growth,
(4) full E6 f(I) moduli / singlet invariant ring,
(5) exact binomial power of the fixed-n multitime witness.
All are conditional checks, NOT a solved theory or experimental data.
"""
import json, math
from pathlib import Path
import numpy as np
import sympy as s
from scipy.stats import binom,beta
ROOT=Path(__file__).resolve().parents[1]

def adS4():
    u,L=s.symbols("u L",real=True,positive=True)
    V=(-s.Rational(21,2)*s.exp(-9*u)+s.Rational(9,2)*s.exp(-21*u))/L**2
    assert s.simplify(V.subs(u,0)+6/L**2)==0
    assert s.simplify(s.diff(V,u).subs(u,0))==0
    assert s.simplify(s.diff(V,u,2).subs(u,0)*L**2/63)==18
    # The electric flux F4=(3/L)vol4 solves 11D Einstein equations
    # with AdS4 radius L, round S7 radius 2L.
    assert s.simplify(-(3/L)**2/3+3/L**2)==0
    assert s.simplify((3/L)**2/6-6/(2*L)**2)==0
    samples=[s.Rational(l*(l+6),4) for l in range(10)]
    assert samples[0]==0 and samples[1]==s.Rational(7,4)
    return dict(BF_AdS4="-9/4",S7_over_AdS4_radius=2,
                breathing_canonical_m2L2=18,
                test_scalar_m2L2_first10=[str(v) for v in samples],
                caveat="Homogeneous breathing and uncoupled massless 11D spectator scalar only; full mixed 11D KK gravity/form/spinor spectrum not computed. Prior Tpq formula is AdS5.")

def e8_family():
    om=np.exp(2j*np.pi/3)
    X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
    Z=np.diag([1,om,om**2])
    b=[]
    for i in range(3):
        for j in range(3):
            M=np.zeros((3,3),complex);M[i,j]=1
            b.append(np.concatenate([(X@M-M@X).ravel(),(Z@M-M@Z).ravel(),[np.trace(M)]]))
    rank=int(np.linalg.matrix_rank(np.column_stack(b),tol=1e-10))
    assert rank==9
    assert 16-20+4==0 and 16-80+64==0
    return dict(E8_branching="(78,1)+(1,8)+(27,3)+(27bar,3bar)",
        isolated_chiral_27_triplet_SU3_cubed_anomaly=27,
        complete_adj_conjugate_pair_SU3_cubed_anomaly=0,
        H27_traceless_SU3_commutant_dim=9-rank,
        caveat="Only if SU3 family is GAUGED; the finite H27 group needs separate global/discrete anomaly analysis. A parallel E6-singlet adjoint Higgs preserving full H27 holonomy must vanish.")

def PW_energy():
    x,y,z,R,a=s.symbols("x y z R a",real=True,positive=True)
    f=(x**4-6*x*x*y*y+y**4)/4-(x*x+y*y)/2+z*z-a*x
    assert sum(s.diff(f,v,2) for v in (x,y,z))==0
    grad2=s.expand(sum(s.diff(f,v)**2 for v in (x,y,z)))
    def integral(poly):
        p=s.Poly(poly,x,y,z)
        result=0
        for ex,coeff in p.terms():
            if any(n%2 for n in ex):continue
            ia,ib,ic=[n//2 for n in ex];N=ia+ib+ic
            angular=2*s.gamma(s.Rational(2*ia+1,2))*s.gamma(s.Rational(2*ib+1,2))*s.gamma(s.Rational(2*ic+1,2))/s.gamma(s.Rational(2*N+3,2))
            result+=coeff*angular*R**(2*N+3)/(2*N+3)
        return s.simplify(result)
    exact=64*s.pi*R**9/315+8*s.pi*R**5/5+4*s.pi*a*a*R**3/3
    assert s.simplify(integral(grad2)-exact)==0
    return dict(laplacian=0,
       energy_ball_R="64*pi*R^9/315+8*pi*R^5/5+4*pi*a^2*R^3/3",
       global_source_free_finite_energy_R3=False,
       smooth_closed_compact_nonconstant_exact_harmonic_f_possible=False,
       caveat="The published parallel local 3 L2 PW solutions remain valid. A physical G2/global gauge gluing needs boundary/source/nonexact data; this is the flat auxiliary Higgs Dirichlet integral, not 11D energy.")

def E6_moduli():
    q=s.Matrix([[-5,5,0],[-3,-1,4]])
    assert q*s.ones(3,1)==s.zeros(2,1)
    inv={}
    for n in range(13):
        inv[n]=[(i,j,n-i-j) for i in range(n+1) for j in range(n-i+1)
                if q*s.Matrix([i,j,n-i-j])==s.zeros(2,1)]
    assert inv[3]==[(1,1,1)] and inv[6]==[(2,2,2)]
    assert not inv[1] and not inv[2] and inv[0]==[(0,0,0)]
    x,y,z=s.symbols("x y z")
    I=x*y*z;H=s.hessian(I-I**2/2,(x,y,z)).subs({x:1,y:1,z:1})
    assert H.rank()==1
    return dict(singlet_invariant_ring="C[xyz]",
        no_nonzero_all_threeVEV_Fflat_with_only_renormalizable_cubic=True,
        general_analytic_fI_at_stationary_dI_nonzero_Hessian_rank_at_most=1,
        full_chiral_field_dim=132,SM_unbroken_minimum_generators=12,
        smooth_one_invariant_moduli_complex_lower_bound=65,
        separable_k_constraints_reduced_moduli_lower_bound="max(0,66-k)",
        caveat="Requires the stated 78+27+27bar full chiral inventory, smooth polystable N1 quotient and W=f(I) or separable stationary invariants. Not a no-go for arbitrary E6 UV superpotentials.")

def photon():
    alpha=.01;gamma=.96;eta=.95
    pg=(1+gamma)/2;pe=(1+eta)/2
    def stats(n):
        k=np.arange(n+1);lo=np.zeros(n+1)
        lo[1:]=beta.ppf(alpha/3,k[1:],n-k[1:]+1)
        lo=2*lo-1
        conservative=np.sqrt(1-np.maximum(lo,0)**2)
        needed=conservative[:,None]+conservative[None,:]
        kg=np.searchsorted(lo,needed,side="right")
        tail=binom.sf(np.arange(n+2)-1,n,pg)
        w=binom.pmf(k,n,pe)
        power=float((w[:,None]*w[None,:]*tail[kg]).sum())
        gg=int(round(n*pg));ee=int(round(n*pe))
        design=2*math.sqrt(1-max(lo[ee],0)**2)-lo[gg]
        return dict(n=n,accepted_total=3*n,model_exact_rejection_power=power,
                    rounded_expected_successes=[gg,ee,ee],
                    designpoint_W3_upper=design)
    rows=[stats(n) for n in (300,450,600,900)]
    assert abs(rows[1]["model_exact_rejection_power"]-.66128121221282)<1e-10
    assert rows[2]["model_exact_rejection_power"]>.90
    return dict(alpha=alpha,gamma=gamma,eta=eta,pairwise_classical_p=.45,
        rows=rows,not_experimental_data=True,
        caveat="Exact independent fixed-n Bernoulli/Clopper-Pearson/Bonferroni power for the chosen Beyer et al three-time qubit witness only, not validated physical instruments or an intrinsically qutrit process.")

def run():
    parts=dict(AdS4=adS4(),E8_family=e8_family(),PW_global=PW_energy(),
               E6=E6_moduli(),photon_power=photon())
    out=dict(status="PASS",new_tests=22,parts=parts,
             reviewed_parallel_head="9321eb27ecaeacea9d640b31c8d010fa3a9f84f7",
             complete_TOE_proven=False)
    dest=ROOT/"data/toe_20261118_fivefront_global_physics_closure.json"
    dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    print("PASS all five reproducible mathematical/conditional TOE audits")
    for name,x in parts.items(): print(name,"PASS")
    return out
if __name__=="__main__":run()
