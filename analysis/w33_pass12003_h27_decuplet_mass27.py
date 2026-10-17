"""A different spectator-mass channel: the27 kernel of Sym²(Sym³3)->Sym⁶3.

The anomaly spectator is priorOct1/11613; H27-preserving28 masses are prior
11271/11606. Here an explicit27-channel VEV gives rank10 and full continuous
SU3 breaking without an E6-charged mirror. Vacuum orientation is supplied.
"""
import json,itertools,math
from pathlib import Path
import sympy as s
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
EXP=[e for e in itertools.product(range(4),repeat=3) if sum(e)==3]
PAIRS=list(itertools.combinations_with_replacement(range(10),2))
EXP6=[e for e in itertools.product(range(7),repeat=3) if sum(e)==6]


def multiplication_matrix():
    return s.Matrix([[int(tuple(EXP[i][k]+EXP[j][k] for k in range(3))==e)*(1 if i==j else 2) for i,j in PAIRS] for e in EXP6])


def poly_generators():
    E={}
    for i,j in itertools.product(range(3),repeat=2):
        M=s.zeros(10)
        for a,e in enumerate(EXP):
            if e[j]:
                f=list(e);f[j]-=1;f[i]+=1;M[EXP.index(tuple(f)),a]=e[j]
        E[i,j]=M
    out=[]
    for i,j in itertools.combinations(range(3),2):out.extend([(E[i,j]+E[j,i])/2,(E[i,j]-E[j,i])/(2*s.I)])
    out.extend([(E[0,0]-E[1,1])/2,(E[0,0]+E[1,1]-2*E[2,2])/(2*s.sqrt(3))])
    return out


def payload():
    mult=[s.factorial(3)/s.prod(s.factorial(k) for k in e) for e in EXP]
    multiplication=multiplication_matrix();assert multiplication.rank()==28 and len(multiplication.nullspace())==27
    perm=[EXP.index((e[2],e[0],e[1])) for e in EXP];X=s.zeros(10)
    for i,j in enumerate(perm):X[j,i]=1
    # Z charges modulo3 impose invariance without numerical roots of unity.
    variables={pair:s.Symbol('n'+str(k)) for k,pair in enumerate(PAIRS) if sum(EXP[a][1]+2*EXP[a][2] for a in pair)%3==0}
    N=s.zeros(10)
    for (i,j),v in variables.items():N[i,j]=N[j,i]=v
    eq=list(X*N*X.T-N);eq+=list(multiplication*s.Matrix([N[i,j] for i,j in PAIRS]))
    A,_=s.linear_eq_to_matrix(eq,list(variables.values()));invariants=A.nullspace();assert len(invariants)==3
    vector=-6*sum(invariants,s.zeros(len(variables),1));N=N.subs(dict(zip(variables.values(),vector)))
    assert all(v.q==1 for v in N) and N.det()!=0 and X*N*X.T==N
    assert multiplication*s.Matrix([N[i,j] for i,j in PAIRS])==s.zeros(28,1)
    # SU3-invariance of the27-channel itself is checked using the actual
    # polynomial generators. Gauge breaking rank is exact over Q(i,sqrt3).
    generators=poly_generators();variations=[]
    for T in generators:
        delta=T*N+N*T.T
        assert multiplication*s.Matrix([delta[i,j] for i,j in PAIRS])==s.zeros(28,1)
        variations.append(s.Matrix(delta).reshape(100,1))
    assert s.Matrix.hstack(*variations).rank()==8
    root=s.diag(*[s.sqrt(v) for v in mult]);physical=root.inv()*N*root.inv()
    omega=-s.Rational(1,2)+s.I*s.sqrt(3)/2;Z=s.diag(*[omega**((e[1]+2*e[2])%3) for e in EXP])
    assert (Z.conjugate().T*physical*Z.conjugate()-physical).applyfunc(s.simplify)==s.zeros(10)
    assert X.T*physical*X==physical
    mass=np.array(physical,float);sv=np.linalg.svd(mass,compute_uv=False);assert sv[-1]>0
    Tphysical=[root.inv()*T*root for T in generators]
    assert all((T-T.conjugate().T).applyfunc(s.simplify)==s.zeros(10) for T in Tphysical)
    old=json.loads((ROOT/'data/w33_20261001_chiral_decuplet_and_condensate_bridge.json').read_text())['anomaly_repair'];assert old['A10']==27
    return dict(status='PASS',cubic_monomial_exponents=EXP,multinomial_normalizations=list(map(int,mult)),
        symmetric_square_dimension=55,sextic_image_rank=28,kernel_irrep='SU3(2,2), dimension27',
        H27_invariant_mass_space_in_kernel_dimension=3,explicit_integer_mass_N=N.tolist(),exact_determinant_N=str(N.det()),
        physical_mass_normalization='M=diag(mult)^-1/2 N diag(mult)^-1/2 in orthonormal Sym³3 coordinates',
        physical_mass_matrix=[[str(v) for v in row] for row in physical.tolist()],physical_mass_singular_values=sv.tolist(),
        exact_mass_rank=10,exact_continuous_SU3_breaking_rank=8,
        retained_finite_subgroup='Standard actual family X,Z Heisenberg image H27 is preserved, including its center. Full finite stabilizer not identified.',
        renormalizable_operator='y chi_bar10^T Phi_27 chi_bar10/2; Phi27 is the kernel component ofSym²10. It is an E6 singlet and center-trivial, hence legal for(E6xSU3)/Z3. No E6-charged mirror added.',
        anomaly='Prior(27,3)+(1,bar10) has27-27=0 continuousfamilySU3 cubic anomaly. The newscalar27 doesnotchange it; spectator massdoesnotpermitdroppingthresholdWessZumino terms.',
        nonsupersymmetric_running={'prior_no_mass_scalar':'-15/2','new_one_complex27':'-33/2','prior_one_complex28':'-57/2','T27':27,'real_scalar_components_new':54,'real_scalar_components_prior28':56},
        optional_SUSY_vacuum='Separate N=1 extension: independent Phi27 and dualPhiBar27, singlet X, W=X(PhiBar.Phi-v²)+y chi chi Phi/2. Set chi=0,X=0,Phi=M,PhiBar=M*,v²=||M||². AllF=0 and pairD=0 exactly. SU3Lie stabilizer0. This is a global zero-energy SUSY branch, not its selection or a soft/hidden/E6 completion.',
        optional_SUSY_mass_sector_flat_complex_moduli=45,
        U3_boundary='Only theSU3 subgroup is gauged. IdentifyingthecentralU1 oftheatlasU3 asgauged addsSU3²U1,U1³ andgravityU1 constraints notcancelledbythisinventory.',
        physics_boundary='A specified orientation and massYukawa, not a fullstableE6-toSM flavourvacuum. The optionalSUSYpair changesinventory/running and leaves45complexmass-sectorflatmoduli, excluding the original massless matter directions. No spectator massscale, observedYukawas, discrete/global anomalycompletion or RGUVsolution.',
        prior=['analysis/w33_20261001_chiral_decuplet_and_condensate_bridge.py anomalyowner','11613 anomaly spectator minimality','11271 Sym²bar10 symmetricmass rule and elementary28 channel','11276 sextetcomposite mass and WZ boundary','11602_11606 spectator_residual_symmetry H27-preserving28 andrunning cost','11998 actualU3 reduction andchargedfamilyinterpretation boundary'],
        primary=['https://doi.org/10.1103/PhysRevD.110.045026'])

if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass12003_h27_decuplet_mass27.json').write_text(json.dumps(d,indent=2,default=int)+'\n');print(d['status'],d['exact_determinant_N'])
