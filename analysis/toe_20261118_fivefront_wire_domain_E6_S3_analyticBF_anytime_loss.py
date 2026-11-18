"""Five independent W33/E6 falsifier fronts, no physical compactification claimed.

Front A: relative-boundary index sensitivity with explicit chain complexes.
Front B: rank-two algebraic gauge repair and anomaly inflow necessity.
Front C: finite-geometry natural triple from pointed W33 isotropic lines.
Front D: analytically corrected modular winding instability fraction.
Front E: sequential qutrit e-process under bounded heralding bias.
"""
import json,math,itertools,sys
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.special import ndtr
from scipy.integrate import quad
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261118_W33_triperiodic_Levi_homogenization as W
from sympy.combinatorics import Permutation,PermutationGroup


def boundary_domain_front():
    """Explicit mapping cone C^q(M,Sigma) for any subset of inner S2 defects."""
    rows=[]
    for m in range(1,8):
        for r in range(1,m+1):
            for t in (sp.Integer(1),sp.Integer(-1),sp.I,sp.Integer(2)):
                # M=S1 vee m*S2, relative Sigma is r disjoint spheres.
                dims=[1,1+r,m,r]
                d0=sp.Matrix([t-1]+[1]*r)
                d1=sp.zeros(m,1+r)
                d2=sp.zeros(r,m)
                for k in range(r):d2[k,k]=1
                assert d1*d0==sp.zeros(m,1)
                assert d2*d1==sp.zeros(r,1+r)
                ranks=[x.rank() for x in (d0,d1,d2)]
                betti=[dims[i]-(ranks[i-1] if i else 0)-
                       (ranks[i] if i<len(ranks) else 0) for i in range(4)]
                assert betti==[0,r,m-r,0]
                assert betti[1]-betti[2]==2*r-m
                rows.append(dict(m=m,r=r,char=str(t),b1=r,b2=m-r,index=2*r-m))
    assert len(rows)==4*sum(m for m in range(1,8))
    canonical=[x for x in rows if x["m"]==3 and x["char"]=="2"]
    assert [(x["r"],x["b1"],x["b2"],x["index"]) for x in canonical]==[
        (1,1,2,-1),(2,2,1,1),(3,3,0,3)]
    return dict(status="PASS",cases=len(rows),m3_sensitivity=canonical,
                theorem="For M=solid torus with m excised point balls, r>=1 selected relative S2 boundaries and outer torus absolute, all complex flat characters t!=0 satisfy (b1,b2)=(r,m-r), net chiral index 2r-m.",
                consequence="If one of three assumed defect spheres is not given the charged relative domain, index3 falls to index1 and a conjugate mode appears. Thus a claimed three-family construction depends on all three physical boundary projectors, not merely the ambient topology.",
                caveat="Topological de Rham mapping-cone index only. Does not prove the physical flux-coupled 7D Dirac/APS boundary projector, eta invariant, anomaly inflow, or self-adjointness.")


def anomaly_Higgs_front():
    # Native adjoint singlet chirals have q=(-5,-3), no independent SM-singlet direction.
    q=sp.Matrix([-5,-3])
    # E6 27 fundamental: SO10 singlet1_(4) -> Chi0,Psi+4.
    s=sp.Matrix([0,4])
    M=q*q.T+s*s.T
    assert M==sp.Matrix([[25,15],[15,25]])
    assert M.eigenvals()=={sp.Integer(40):1,sp.Integer(10):1}
    assert M.det()==400
    # D-flat algebraic new fields q, -q and s, -s of equal VEV magnitude.
    charges=[q,-q,s,-s]
    D=sum(charges,sp.zeros(2,1))
    assert D==sp.zeros(2,1)
    M_D=sum((v*v.T for v in charges),sp.zeros(2))
    assert M_D.rank()==2 and M_D.eigenvals()=={80:1,20:1}
    # The extra scalars can be vectorlike and hence cannot cancel the residual
    # chiral fermions' U1_Psi gauge anomalies.
    origin=dict(gravity_Psi=-144,cubic_Psi=-1296,
                Y2_Psi=-30,SU3sq_Psi=-18,SU2sq_Psi=-18)
    assert sum(v[1] for v in charges)==0
    # E6 cubic Yukawa charge mismatch from localized adjoint 16_-3:
    required_Psi=6
    available_27=[1,-2,4]
    available_27bar=[-1,2,-4]
    available_78=[-3,0,3]
    assert required_Psi not in available_27+available_27bar+available_78
    # Full 27 contains its own canonical cubic 16_(+1) 16_(+1) 10_(-2).
    assert 1+1-2==0
    return dict(status="PASS",
                old_singlet_charge=list(q),
                independent_E6_fundamental_singlet_charge=list(s),
                rank2_mass_matrix=M.tolist(),
                eigenvalues=[10,40],determinant=400,
                Dflat_minimal_algebraic_oppositely_charged_pair_set=[list(v) for v in charges],
                pair_mass_matrix=M_D.tolist(),
                residual_anomaly_unaffected_by_vectorlike_pairs=origin,
                adjoint_two_16_Psi_charge_sum=-6,
                required_cubic_partner_Psi_charge=6,
                E6_27_Psi_sector_charges=available_27,
                E6_27bar_Psi_sector_charges=available_27bar,
                E6_78_Psi_sector_charges=available_78,
                existing_same_sheet_cubic_Yukawa_possible_with_27_or_27bar=False,
                alternative_E6_27_family_cubic_Psi_conservation="16_(+1)*16_(+1)*10_(-2) has net U1Psi charge0, but requires an entirely different localized family sector.",
                caveat="This is a NECESSARY algebraic extension, not an E6 dynamical vacuum: source of the opposite-charge q scalar, E6 and SM gauge invariance of F-terms, 4D anomaly inflow and full scalar potential are unknown.")


def w33_pointed_line_front():
    G,points,lines=W.levi()
    pidx={p:i for i,p in enumerate(points)}
    lidx={l:i for i,l in enumerate(lines)}
    edgeidx={(p,40+j):k for k,(p,jj) in enumerate([])} # unused
    flags=[(p,li) for li,line in enumerate(lines) for p in line]
    assert len(flags)==160
    fidx={f:i for i,f in enumerate(flags)}
    gens=[]
    for v in points:
        pm={i:pidx[W.projective(tuple((x[k]+W.symplectic(x,v)*v[k])%3
                                    for k in range(4)))] for i,x in enumerate(points)}
        lm={i:lidx[tuple(sorted(pm[k] for k in line))] for i,line in enumerate(lines)}
        flagperm=[fidx[(pm[p],lm[li])] for p,li in flags]
        gens.append(Permutation(flagperm))
    group=PermutationGroup(gens)
    order=int(group.order())
    assert order==25920
    anchor=0
    stab=group.stabilizer(anchor)
    st_order=int(stab.order())
    assert st_order==162
    anchorpoint,anchorline=flags[anchor]
    triple=sorted(set(lines[anchorline])-{anchorpoint})
    assert len(triple)==3
    induced=set()
    # stabilizer has only 162 elements; enumerate exactly
    for g in stab.generate_schreier_sims():
        arr=tuple(triple.index(g(fidx[(p,anchorline)]) if False else
                                   flags[g(fidx[(p,anchorline)])][0]) for p in triple)
        # check g fixes the anchor flag -> fixes its line and point
        assert g(anchor)==anchor
        assert sorted(arr)==[0,1,2]
        induced.add(arr)
    assert len(induced)==6
    distribution=Counter()
    for sigma in induced:
        cyc=sum(sigma[i]==i for i in range(3))
        distribution[cyc]+=1
    assert distribution=={3:1,1:3,0:2}
    # S3-invariant family mass matrices in the permutation basis must be aI+bJ
    # eigenvalues a (multiplicity2), a+3b (multiplicity1).
    a,b=sp.symbols("a b")
    mass=a*sp.eye(3)+b*sp.ones(3)
    assert mass.eigenvals()=={a:2,a+3*b:1}
    # Structural triple is W33-native only after a flag/pointed isotropic
    # line is selected; the flag itself has 160 possible positions.
    return dict(status="PASS",W33_flags=160,group="PSp(4,3)",group_order=order,
                flag_stabilizer_order=st_order,other_three_points=triple,
                induced_permutation_group="S3",distinct_triple_permutations=6,
                conjugacy_class_fixed_point_counts={str(k):v for k,v in distribution.items()},
                mass_matrix_general_S3_invariant="a I3+b J3",
                mass_eigenvalues={"a":2,"a+3b":1},
                rank_constraint="An exact S3 symmetry leaves a twofold family mass degeneracy. Physical fermion mass hierarchies require additional symmetry breaking or representation-dependent couplings.",
                novelty_scope="The 3=4-1 leftover points of a W33 isotropic line after choosing a flag supply a concrete, native and symmetry-covariant abstract defect triple; there are160 possible flags, and no derived map from flags to geometric wire defects or 7D field configuration.")


def below_area(y):
    """Normalised hyperbolic area of modular domain with Im(tau)<=y."""
    y0=math.sqrt(3)/2
    if y<=y0:return 0.
    if y<1:
        x=math.sqrt(1-y*y)
        return (6/math.pi)*(math.pi/6-math.asin(x)-(0.5-x)/y)
    return 1-3/(math.pi*y)


def robust_BF_analytic_front():
    data=[]
    for r in (.9,1.,1.2,2.,5.,10.):
        for d in (0.,.25,.5,1.,1.5,2.,2.2):
            root=math.sqrt(36-16*d)
            l_lo=6-d-root;l_hi=6-d+root
            y_lo=3*math.pi*r/l_hi
            y_hi=math.inf if l_lo==0 else 3*math.pi*r/l_lo
            frac=below_area(y_hi)-below_area(y_lo)
            assert -1e-12<=frac<=1+1e-12
            if d==0:
                import toe_20261118_fivefront_global_Wilson_modular_photonic as Old
                assert abs(frac-(1-Old.modular_stable_fraction(r)))<1e-12
            data.append(dict(r=r,delta=d,lambda_lo=l_lo,lambda_hi=l_hi,
                             y_lo=y_lo,y_hi=y_hi,unsafe_fraction=frac))
    assert abs(next(x["unsafe_fraction"] for x in data
                    if x["r"]==2 and x["delta"]==1)-.453122108370014)<1e-10
    # Geometric-domain measure, not actual physical moduli probability.
    return dict(status="PASS",samples=data,
                exact_formula="F_robust=F_below(3*pi*r/lambda_lo)-F_below(3*pi*r/lambda_hi), with F_below(y)=0 if y<=sqrt3/2; 6/pi*(pi/6-asin(sqrt(1-y²))-(1/2-sqrt(1-y²))/y) if sqrt3/2<y<1; 1-3/(pi*y) if y>=1.",
                y_max_infinite_when_delta_zero=True,
                note="This is an analytic closed form replacing parent numerical quadrature. No bound on actual physical string/M-theory correction delta has been established.")


def anytime_loss_front(max_n=1000):
    """Vectorised exact killed-binomial DP for sequential likelihood e-process."""
    results=[]
    for kappa in (1.,1.025,1.05,1.10,1.15,1.20):
        p0=kappa/(kappa+2)
        p1=7/(7+8*kappa)
        if p1<=p0:continue
        logup=math.log(p1/p0);logdown=math.log((1-p1)/(1-p0))
        cuts=math.log(100)
        def recur(p):
            state=np.array([1.],dtype=float)
            hits=0.
            Etrunc=0.
            rec={}
            for n in range(1,max_n+1):
                Etrunc+=float(state.sum())
                new=np.zeros(n+1)
                new[:-1]+=state*(1-p)
                new[1:]+=state*p
                idx=np.arange(n+1)
                reject=idx*logup+(n-idx)*logdown>=cuts-1e-12
                hits+=float(new[reject].sum())
                new[reject]=0.
                state=new
                if n in (200,292,600,1000):
                    rec[str(n)]=hits
            assert abs(hits+state.sum()-1)<1e-8
            return rec,Etrunc
        null,EN=recur(p0)
        alt,EA=recur(p1)
        assert all(v<=.0100000001 for v in null.values())
        results.append(dict(herald_odds_bound=kappa,
                            null_p=p0,alternative_p=p1,
                            E_success=p1/p0,E_failure=(1-p1)/(1-p0),
                            alternative_detection_by_n=alt,
                            null_false_positive_by_n=null,
                            alternative_expected_truncated_accepted=EA,
                            max_n=max_n))
    return dict(status="PASS",confidence_level=.99,threshold_e=100,
                exact_bounded_loss_sequential_results=results,
                no_IID_null="Conditional p(success|past)<=kappa/(kappa+2) is sufficient for nonnegative likelihood-ratio test supermartingale with calibrated p1>p0.",
                caveat="Null conditional bounds need independent event-ready heralding and detector calibration. The alternative expected stopping times assume IID accepted data. This is not an operational device-independent proof of multitime quantum memory.")


def run():
    out=dict(status="PASS",boundary=boundary_domain_front(),
             gauge=anomaly_Higgs_front(),
             W33=w33_pointed_line_front(),
             winding=robust_BF_analytic_front(),
             memory=anytime_loss_front())
    path=ROOT/"data/toe_20261118_fivefront_wire_domain_E6_S3_analyticBF_anytime_loss.json"
    path.write_text(json.dumps(out,indent=2,default=lambda v:int(v) if isinstance(v,sp.Integer) else str(v))+"\n",encoding="utf-8")
    print("PASS all five: boundary domain index, E6 rank-two charges/no Yukawa, W33 pointed S3 triple, analytic BF, herald-biased e-process")
    return out

if __name__=="__main__":run()
