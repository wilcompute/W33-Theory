"""A locally isolated classical vacuum of an explicitly deformed native cubic.

This changes the superpotential and supplies a scale; it is not vacuum selection
by the original homogeneous cubic. Standard Sp SQCD is credited separately.
"""
import json,pathlib,sys
import sympy as s
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_clifford_native_cubic_repair import cubic_terms,DUADS,representation,transform_cubic

def model():
    x=s.symbols('x:29');mu=s.Matrix([[1,2],[3,5]])
    W=sum(c*s.prod(x[i] for i in t) for t,c in cubic_terms().items())
    for i in range(4):
        pq=[x[DUADS.index((i,j))]for j in [4,5]];uv=[x[15+i],x[21+i]]
        W+=sum(mu[a,b]*uv[a]*pq[b] for a in range(2) for b in range(2))
    W+=x[20]*x[25]+x[27]*(x[19]-1)+x[28]*(x[26]-1)
    v=[0]*29
    for ij in [(0,2),(1,3)]:v[DUADS.index(ij)]=1
    v[19]=v[26]=1
    return x,s.expand(W),v

def build():
    x,W,v=model();at=dict(zip(x,v));F=[s.diff(W,z) for z in x];H=s.hessian(W,x).subs(at)
    assert all(f.subs(at)==0 for f in F) and W.subs(at)==0
    assert H.rank()==24
    A=s.zeros(6)
    for k,(i,j) in enumerate(DUADS):A[i,j]=v[k];A[j,i]=-v[k]
    chi=A[:4,:4];assert chi*chi.conjugate().T==s.eye(4)
    # Complexified gauge tangents. Their span is exactly the Hessian kernel.
    tangents=[]
    for i in range(4):
        for j in range(4):
            if i==j:continue
            T=s.zeros(4);T[i,j]=1;tangents.append(T)
    for i in range(3):
        T=s.zeros(4);T[i,i]=1;T[3,3]=-1;tangents.append(T)
    vectors=[]
    for T in tangents:
        B=s.diag(T,s.zeros(2));dA=B*A+A*B.T
        z=[dA[i,j]for i,j in DUADS]+[0]*14;vectors.append(s.Matrix(z))
    G=s.Matrix.hstack(*vectors);assert G.rank()==5 and H*G==s.zeros(29,15)
    charged=[DUADS.index((i,j))for j in [4,5]for i in range(4)]+list(range(15,19))+list(range(21,25))
    HC=H.extract(charged,charged);assert HC.rank()==16 and HC.det()==256
    # New terms pair a dual and fundamental, or singlets: exact SU4 invariance.
    extra=s.expand(W-sum(c*s.prod(x[i]for i in t)for t,c in cubic_terms().items()))
    for T in tangents:
        B=s.diag(T,s.zeros(2));AA=s.zeros(6)
        for k,(i,j)in enumerate(DUADS):AA[i,j]=x[k];AA[j,i]=-x[k]
        dA=B*AA+AA*B.T;dz=[dA[i,j]for i,j in DUADS]+list(-B.T*s.Matrix(x[15:21]))+list(-B.T*s.Matrix(x[21:27]))+[0,0]
        assert s.expand(sum(s.diff(extra,z)*d for z,d in zip(x,dz)))==0
    # Effective mass-deformed Nf1 SQCD: W=2 sqrt(L8/M)+mM.
    # Eliminate the square root with Y^2 M=L8, F_M=m-Y/M=0.
    M,Y,L8,m=s.symbols('M Y L8 m',nonzero=True)
    assert s.expand((Y**2*M-L8).subs(Y,m*M))==m**2*M**3-L8
    return dict(status='PASS_NATIVE_29_FIELD_LOCAL_STABILIZATION',
        model='Original native27 in changed SU4 embedding plus two gauge singlet chiral multiplets S,T; no extra16-matter extension assumed.',
        superpotential=str(W),quadratic_mu_matrix=[[1,2],[3,5]],
        deformation='sum_i (u_i p_i+2 u_i q_i+3 v_i p_i+5 v_i q_i) +u5 v4+ S(u4-1)+T(v5-1), i=0..3; coefficients expressed in supplied common mass units.',
        dimensionful_restore='u5 v4 coefficient m0; entries of mu have mass dimension1; multipliers kappaS*S*(u4-vscale)+kappaT*T*(v5-vscale), kappas dimension1. Example uses vscale=m0=kappas=1 and mu=[[1,2],[3,5]].',
        VEV_model=v,all_F_zero=True,D_flat_witness='chi chi-dagger=I4; nonzero u4,v5 are SU4 singlets, so every traceless Hermitian SU4 moment vanishes.',
        exact_Hessian_rank=24,Hessian_kernel_dimension=5,complex_gauge_tangent_rank=5,
        Hessian_kernel_equals_complex_gauge_orbit=True,charged_Hessian_rank=16,charged_Hessian_determinant=256,
        unbroken_gauge_group='USp4',local_physical_chiral_flat_directions=0,
        invariance='All15 sl4 infinitesimal variations of every new term vanish identically; terms are SU4 invariant and hence invariant under the actual seven Clifford generators.',
        classical_scope='At F=D=0 the scalar potential is nonnegative and the quotient chiral Hessian is nonsingular. This is a locally isolated classical supersymmetric vacuum modulo gauge. Unbroken gauge multiplets remain; no classification of other vacua.',
        quantum_completion=dict(assumptions='All chiral masses and Higgs scale parametrically above the strong scale, standard4D N=1 Sp dynamics, nonsingular local gauge quotient.',
            low_energy='pure USp4 SYM with dual Coxeter number3',gaugino_branches=3,
            conclusion='Holomorphic nondegeneracy permits a small nonperturbative displacement of each local classical branch in the weak-coupling regime; a calculation of the full finite-coupling UV vacuum is not supplied.',
            mass_deformed_mesonic_benchmark='W=2 sqrt(Lambda_low^8/M)+m M +X(t-v); finite critical mesons obey M^3=Lambda_low^8/m^2. X balances the t derivative. Three solutions for nonzero parameters, with W_MM=3m/(2M) nonzero.',
            meson_critical_polynomial='m^2 M^3-Lambda_low^8',same_as_native_pure_cubic=False),
        ownership='Nov2 conditional vacuum and Nov3 exact F-flat chart own the undeformed branch and its ADS obstruction. Multiplier stabilization and Sp SQCD mass deformations are established methods; explicit native29 benchmark checked here.',
        reference='https://arxiv.org/abs/hep-th/9505006',
        boundary='The scale and mass matrix are added inputs. This does not derive the physical vacuum, measured constants, Standard Model, gravity or a TOE.')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261103_native_singlet_stabilization.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['exact_Hessian_rank'],flush=True)
