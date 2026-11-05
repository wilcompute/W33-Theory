"""Conditional DQQ determinant obstruction and a mixed-fermion quality check.

General determinant principle: Cheung, arXiv:1003.0941, sec.2.
Heavy-mediated breaking caveat: Bonnefoy, arXiv:2212.00102, secs.III-IV.
Model input: toe_20261105_five_fronts_model_completion.py, protected_variant.
No claim of a complete TOE, unknown gravitational Wilson coefficients, or
exhaustive UV protection. All numerical scales below are supplied inputs.
"""
import itertools,json,math,pathlib
import numpy as np
import sympy as sp
R=pathlib.Path(__file__).resolve().parents[1]
MP=2.435e18
MQ=27279937181.61975
CHI=.0756**4

def determinant_control():
    a,b,c,d,e=sp.symbols('a b c d e')
    M=sp.diag(e,sp.Matrix([[a,b],[c,d]]),sp.Matrix([[a,b],[c,d]]))
    F=sp.expand(M.det())
    assert sp.expand(F-e*(a*d-b*c)**2)==0
    assert sp.expand(sum(v*sp.diff(F,v) for v in [a,b,c,d,e])-5*F)==0
    rng=np.random.default_rng(20261105); residuals=[]
    for _ in range(30):
        Q=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
        U=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)))[0]
        V=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)))[0]
        # Magnitude invariant; determinant phase changes by constant det(UVdag).
        residuals.append(abs(abs(np.linalg.det(U@Q@V.conj().T))**2-abs(np.linalg.det(Q))**2))
    r=2*MQ**5/(MP*CHI)
    return dict(polynomial=str(F),max_scalar_degree=5,matrix_flavors=5,
        max_absolute_basis_magnitude_residual=max(residuals),
        mass_input_GeV=MQ,chi_input_GeV4=CHI,Planck_input_GeV=MP,
        potential_convention='-2 Re[c F/MP]; F=mD det(MQ)^2',
        amplitude_over_chi_for_c1=r,
        sufficient_c_for_uniform_theta_1e_10=1e-10/(r*(1+3e-10)),
        uniform_bound='For one QCD phase theta and same-harmonic determinant breaking, |theta_min|<=r/(1-3r) if r<1/3. This is sufficient, not necessary; aligned phases can evade generic tuning.',
        assumptions=['4D ordinary anomaly-free non-R protecting gauge symmetry; no GS/inflow',
          'only new colored fermions D+(two Q), no heavy-SM mixing; masses SM-singlet scalar polynomials',
          'renormalizable mass entries, possibly constants; all colored masses nonzero',
          'one-Higgs SM with full-rank renormalizable quark Yukawas, hence zero SM mixed color-protection anomaly',
          'global PQ respected by those masses and has nonzero QCD anomaly'],
        proof='Gauge covariance gives charge(det M) equal to minus total colored chiral charge. Weak multiplicity two duplicates MQ; the five color-fundamental flavors give F=mD det(MQ)^2. SM Yukawas cancel its own color anomaly: 2 sum Xq+sum Xu+sum Xd=0. Thus ordinary anomaly cancellation makes F invariant, while anomalous PQ makes F charged. Every entry has scalar degree at most one, so every monomial of F has degree at most five. Bare constants can only lower degree. Colorless additions cannot change this identity. For continuous nonabelian flavor symmetry use the determinant character, as in Cheung sec.2.',
        coefficient_scope='F includes Yukawa coefficients. c is the coefficient of this particular allowed polynomial, not a universal lower bound on individual monomial coefficients or a prediction of quantum gravity.',
        escapes=['new colored fermions','higher-dimensional/radiative mass generation with a specified UV completion','modified SM flavor sector','GS/inflow or higher-dimensional/nonlocal axion origin'])

def assignments():
    rows=[]
    for p in itertools.product(range(4),repeat=3):
        A=B=0
        for w,k in zip([1,2,2],p):
            if k<2:A+=w*(1 if k==0 else -1)
            else:B+=w*(1 if k==2 else -1)
        g=math.gcd(abs(A),abs(B))
        row=dict(mass_choices=[['S','Sdag','T','Tdag'][i]for i in p],A=A,B=B,
                 primitive_scalar_X=[B//g,-A//g],primitive_invariant_degree=(abs(A)+abs(B))//g,
                 determinant_phase_winding=g)
        rows.append(row)
    return dict(rows=rows,count=len(rows),max_primitive_degree=max(x['primitive_invariant_degree']for x in rows),
        two_charged_scalar_rows=sum(x['A']!=0 and x['B']!=0 for x in rows),
        scope='64 diagonal single-monomial renormalizable assignments. General mixing is covered by determinant proof, not by this enumeration. Primitive X charges alone do not certify other gauge anomalies.')

def mixed_minimum(n=13):
    # Relax all SM and spinor contractions except even fermion number. This
    # superset proves a lower bound; the NNprime witness attains it for n13.
    # a,b signed S,T powers; l,h signed low/high Weyl field counts.
    bound=2*(n+1);best=bound;witness=[]
    for a in range(-n-1,n+2):
      for b in range(-n-1,n+2):
       for h in range(-bound//3,bound//3+1):
        l=-2*a-2*n*b-n*h
        cost=2*(abs(a)+abs(b))+3*(abs(l)+abs(h))
        if cost>best or (abs(l)+abs(h))%2 or 2*a+l==0:continue
        if cost<best:best=cost;witness=[]
        witness.append(dict(S=a,T=b,low_Weyl=l,high_Weyl=h,dimension=cost/2,PQ_charge=(2*a+l)/2))
    assert best==n+5 # n13: doubled dimension18.
    k=(n-1)//2
    return dict(n=n,minimum_relaxed_Lorentz_scalar_dimension=best/2,minimizers=witness,
        explicit_operator=f'S^{k} N Nprime / MP^{k-1}',operator_dimension=k+3,
        charges=dict(S_X=2,T_X=2*n,N_X=1,Nprime_X=-n,S_PQ=1,T_PQ=0,N_PQ=.5,Nprime_PQ=0),
        explicit_total_X=2*k+1-n,explicit_PQ=k+.5,
        explanation='N and Nprime are SM singlet left-handed Weyl fields present in the previous variant. Their antisymmetric spinor contraction is nonzero for distinct fields. Conjugates included. X-neutral SM fields and derivatives add dimension and cannot lower this charge-counting bound. This does not classify all operators or compute their complete mixing.')

def loop_control():
    # Two left-handed Weyl fields, not two Dirac pairs. Majorana matrix symmetric.
    a,b,z=sp.symbols('a b z',complex=True)
    M=sp.Matrix([[a,z],[z,b]]);H=sp.conjugate(M.T)*M
    tr=sp.expand(sp.trace(H*H))
    phase=2*(sp.conjugate(a)*sp.conjugate(b)*z*z+a*b*sp.conjugate(z)**2)
    remainder=sp.expand(tr-phase)
    n=13;F=1e11*math.sqrt(n*n+1);log=math.log(MP/F)
    dc=log/(8*math.pi**2)
    # n=13 gives 3n Dirac singlets and three heavy Dirac singlets:
    # 78 light Weyl and six heavy Weyl. Pairwise Dirac mass matrices J
    # are symmetric permutation matrices; J times an all-ones K is K.
    K=np.ones((6*n,6));JL=np.fliplr(np.eye(6*n));JH=np.fliplr(np.eye(6))
    flavor_trace=float(np.trace(JL.T@K@JH.T@K.T))
    assert flavor_trace==36*n
    return dict(trace_H_squared=str(tr),phase_sensitive_trace=str(phase),remainder=str(remainder),
        substitutions='a=y Sdag, b=yprime T, z=kappa S^6/MP^5',
        generated_scalar_operator='S^13 Tdag / MP^10 + h.c.',
        scalar_dimension=14,Planck_power=10,
        Coleman_Weinberg='V1=-Tr[H^2(log(H/mu^2)-3/2)]/(32pi^2) for two Weyl fermions, H=Mdag M.',
        coefficient_convention='Vtree=2 Re[c S^13 Tdag/MP^10]; dc/dlnmu=-conj(y yprime)*kappa^2/(8pi^2) at this order.',
        induced_c_magnitude_for_unit_y_kappa_and_zero_UV_c=dc,
        log_input=log,scale_input_GeV=F,
        full_singlet_flavor_control=dict(light_Weyl=6*n,heavy_Weyl=6,
            basis_invariant='Tr[YLdag kappa YHdag kappa^T]; beta_c=-trace/(8pi^2). Symmetric Weyl mass blocks.',
            coherent_unit_entry_trace=flavor_trace,
            coherent_fixed_coupling_leading_log_c=dc*flavor_trace,
            unit_entry_kappa_Frobenius_norm=float(np.linalg.norm(K)),
            norm_bound='|Tr(YLdag kappa YHdag kappa^T)| <= ||YL||op ||YH||op ||kappa||F^2. A unit bound on the entire Frobenius norm gives the single-block bound, unlike unit bounds on each entry.',
            scope='Fixed-coupling leading logarithm only. The coefficient85.59 is not a controlled UV model or a predicted theta: full Yukawa/operator running, finite matching and UV boundary values are needed. Coherent phases are an allowed stress test, not a statistical typicality claim.'),
        conclusion='Mixed dimension-nine breaking exists, so pure scalar degree14 is not an all-operator selection rule. Its two-insertion logarithmic potential needs the same MP^-10 as the scalar operator in this isolated subblock. No lower Planck power established here. Complete flavor multiplicities, arbitrary Wilson coefficients, finite thresholds and extra UV fields are uncomputed.',
        prior='Heavy-mediated effects established by Bonnefoy 2212.00102; this subblock tests the specific previous mirror-singlet variant.')

def build():
    return dict(status='PASS_CONDITIONAL_DETERMINANT_AND_EXPLICIT_MIXED_FERMION_CONTROLS',
        determinant=determinant_control(),two_scalar_assignments=assignments(),
        mixed_operators=mixed_minimum(),loop=loop_control(),
        sources=['https://arxiv.org/abs/1003.0941','https://arxiv.org/abs/2212.00102'],
        parent='analysis/toe_20261105_five_fronts_model_completion.py',
        boundary='Neither original DQQ axion protection nor replacement model UV completion is solved. This is a credited application and explicit operator calculation, not a new general determinant theorem.')
if __name__=='__main__':
    out=build();(R/'data/toe_20261105_determinant_and_fermion_quality.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(out['status'],out['determinant']['sufficient_c_for_uniform_theta_1e_10'],out['mixed_operators']['operator_dimension'])
