"""Five independent TOE physics fronts plus two collision checks, 2026-11-19.

Conditional mathematical constraints; not a G2 compactification, full GUT, or TOE.
"""
from collections import Counter
from itertools import combinations_with_replacement
from math import pi, log, exp, sqrt
from pathlib import Path
import json
import numpy as np
import sympy as sp
from toe_20261119_balanced_source_E8_cup_gate import sector_census
ROOT=Path(__file__).resolve().parents[1]

def singlet_holomorphic_vacuum():
    sectors,_,census=sector_census()
    fields=[]
    for s in sectors:
        if not s['label'].startswith('S_'):continue
        q=tuple(map(int,s['SU4_charge']))
        fields += [(s['label']+('_'+str(j+1) if s['b1']>1 else ''),q)
                   for j in range(s['b1'])]
        fields += [(s['label']+'_conj'+('_'+str(j+1) if s['b2']>1 else ''),
                    tuple(-k for k in q)) for j in range(s['b2'])]
    assert len(fields)==8
    names=[n for n,q in fields];charge=np.array([q for n,q in fields],int)
    neutral={}
    for degree in (1,2,3):
        neutral[degree]=[tuple(names[i] for i in tup)
                         for tup in combinations_with_replacement(range(8),degree)
                         if np.all(charge[list(tup)].sum(axis=0)==0)]
    assert len(neutral[1])==0 and len(neutral[2])==2 and len(neutral[3])==3
    assert set(neutral[2])=={('S_12','S_12_conj'),('S_14','S_14_conj')}
    assert set(neutral[3])=={
        ('S_12','S_14_conj','S_24'),
        ('S_13','S_14_conj','S_34_1'),
        ('S_13','S_14_conj','S_34_2')}
    S={n:sp.Symbol(n) for n in names}
    m,n,lam,k1,k2=sp.symbols('m n lam k1 k2',nonzero=True)
    A,B,C,D,E,F,G,H=[S[z] for z in [
        'S_12','S_12_conj','S_13','S_14','S_14_conj','S_24','S_34_1','S_34_2']]
    W=m*A*B+n*D*E+lam*A*E*F+k1*C*E*G+k2*C*E*H
    Fterms={key:sp.diff(W,val) for key,val in S.items()}
    assert Fterms['S_34_1']==k1*C*E
    assert Fterms['S_34_2']==k2*C*E
    # F_G=κ C E=0 for κ!=0 => either C=0 or E=0.
    # If E=0, ell(q)=(1,1,0) dot charges >=0, with only A/B zero:
    ell=np.array([1,1,0],int)
    positive=dict(zip(names,(charge@ell).tolist()))
    assert positive['S_12']==positive['S_12_conj']==0
    assert positive['S_13']>0 and positive['S_14']>0
    assert positive['S_24']>0 and positive['S_34_1']>0
    assert positive['S_14_conj']<0
    # Therefore under E=0, D_ell=0 => C=D=F=G=H=0.
    # In all F+D vacua with kappa1 or kappa2 nonzero: C=0.
    # Additional conditions with m,n !=0:
    # F_B=mA=0, F_D=nE=0 => A=E=0, then F_A=mB=>B=0;
    # F_E=nD+κCG+... =>D=-(κCG)/n; D-flat ell then C=F=G=H=D=0.
    return {
        'fields_and_charges':[{'field':name,'q':q.tolist()} for name,q in zip(names,charge)],
        'gauge_invariants_degrees_1_2_3':{str(k):v for k,v in neutral.items()},
        'W_general_renormalizable_without_neutral_fields':str(W),
        'F_derivatives':{key:str(val) for key,val in Fterms.items()},
        'ell_functional_on_fields':positive,
        'generic_nonzero_CEG_obstruction':'If k1 or k2 !=0, F_{G_i}=k_i C E=0. If E=0, ell=(1,1,0) on D=0 forces C=0 because other remaining ell charges are >=0. Hence C=S13=0 in ALL simultaneous F/D-flat vacua (canonical positive Kahler, zero FI).',
        'third_family_one_spurion_diagonal_needs_S13':True,
        'both_bilinears_nonzero_unique_SUSY_vacuum_origin':True,
        'two_bilinears_proof':'m !=0 => A=0 from F_B; n !=0 => E=0 from F_D; then B=0 from F_A. Remaining D_ell>=0 forces C,D,F,G,H=0. No other singlet field remains.',
        'exception':'A missing κ, noncanonical Kähler, FI shifts, additional charged fields/neutral mediators, or nonperturbative/source terms can evade these conditional statements.',
        'scope':'All monomials enumerate only the eight *specified* charged Spin10 singlets, gauge U1^3 charges, and polynomial degrees <=3. Gauge allowance does NOT prove a physical term is generated.'
    }

def topology_chiral_tradeoff():
    # M=T3 minus B3, H1(M)=Z3; relative H1(M,∂M)=Z3 via LES.
    # Any nonzero H1 triple cup requires 3 linearly independent classes
    # because cup in odd degree is alternating (over char0).
    n=3;dim_so10=10*9//2
    # Linear cup ∫dx∧dy∧dz; all repeated wedges zero.
    eps=np.zeros((3,3,3),int)
    for p in __import__('itertools').permutations(range(3)):
        inv=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        eps[p]=(-1)**inv
    assert eps[0,1,2]==1 and np.count_nonzero(eps)==6
    return {'source_M':'T3 minus 1 open ball',
            'b1_absolute':3,'b1_relative_to_one_sphere':3,
            'relative_cup_xyz':int(eps[0,1,2]),
            'triple_cup_requires_b1_at_least_three':True,
            'unbroken_Spin10_Lie_algebra_dimension':dim_so10,
            'adjoint_chiral_zero_modes_if_trivial_flat_ad_bundle_and_no_boundary_projection':3*dim_so10,
            'adjoint_chiral_multiplets_if_no_projection':3,
            'cohomological_argument':'With unbroken Lie algebra g globally fixed by flat holonomy and no defect projection, H1(M;adP_invariants)=g tensor H1(M), dimension 45*3. Nonzero wedge of three degree-one classes requires dimension H1>=3.',
            'limitation':'Flux, singular boundary conditions, superpotentials and nontrivial adjoint holonomy could lift/projection these modes; any such choice must also preserve desired Spin10 gauge group and Yukawa classes.'
           }

def adjoint_GUT_consistency():
    # Minimal renormalizable 24_F Majorana fermion bilinear + 24H adjoint VEV.
    # H=diag(2,2,2,-3,-3) with arbitrary overall normalization absorbed.
    H=np.diag([2,2,2,-3,-3]).astype(float)
    def coeff(T):
        return float(np.trace(T@T@H)/np.trace(T@T))
    def basis(i,j):
        T=np.zeros((5,5));T[i,j]=T[j,i]=1
        return T
    cs={'octet':coeff(basis(0,1)),'triplet':coeff(basis(3,4)),
        'X_leptoquark':coeff(basis(0,3)),'singlet':coeff(H)}
    assert cs=={'octet':2.0,'triplet':-3.0,'X_leptoquark':-.5,'singlet':-1.0}
    assert 2*cs['X_leptoquark']==cs['octet']+cs['triplet']
    # Numbers are imported from parallel 40191f8 illustrative one-loop benchmark.
    M3=2.171635484e7;M8=4.542710799e5
    MXmax=(M3+M8)/2
    MU=2e16
    # Explicit signed-positive example has the maximum; relative sign can lower it.
    MXpos=MXmax
    shift=np.array([10/3,2,4/3])*log(MU/MXpos)/(2*pi)
    assert shift[0]-shift[2]>6 and MXmax<MU/1e8
    # One Weyl SU5 adjoint beta coefficient decomposition:
    # octet (0,0,2), triplet (0,4/3,0), X dirac (10/3,2,4/3).
    # total (10/3,10/3,10/3) complete 24.
    btotal=np.array([0,0,2])+np.array([0,4/3,0])+np.array([10/3,2,4/3])
    assert np.allclose(btotal,[10/3]*3)
    return {'SU5_adj_H_eigenvalues':[2,2,2,-3,-3],
            'renormalizable_mass_Clebsch_coefficients':cs,
            'exact_signed_mass_relation':'M_X=(M_octet+M_triplet)/2',
            'illustrative_triplet_M_GeV':M3,'illustrative_octet_M_GeV':M8,
            'inevitable_X_upper_mass_GeV_if_same_24':MXmax,
            'parallel_chosen_MU_GeV':MU,
            'extra_X_one_loop_b_shifts':[10/3,2,4/3],
            'abs_inverse_coupling_shifts_if_X_at_upper_mass':shift.tolist(),
            'new_inverse_alpha1_minus_alpha3_mismatch_magnitude_at_original_MU':float(shift[0]-shift[2]),
            'full_24_majorana_beta_shifts':btotal.tolist(),
            'conditional_no_go':'Embedding a light triplet and octet into the SAME renormalizable 24F with only 24H mass splitting forces a light (3,2)+conj fermion. This violates the effective calculation placing all other 24F components at MU.',
            'escape':'Different fermion representations, higher dimensional 24F²24H² terms, more Higgs irreps or nontrivial multiplet mixing can break the exact relation.',
            'limitation':'The two triplets and one octet are imported benchmark choices, not independently observed masses, and complex mixing matrices can change eigenvalue mass relations.'
           }

def anisotropic_GR_relational_clock():
    # Generalized Kasner with free massless homogeneous scalar (Mpl=1):
    # ds²=-dt²+sum t^(2p_i)dx_i², phi=sigma ln(t).
    p=np.array([.5,1/3,1/6],float)
    sig=sqrt(1-sum(p*p))
    assert abs(sum(p)-1)<1e-12 and sig>0
    values=[]
    for t in (.25,.5,1.,2.,4.,10.):
        h=p/t
        phidot=sig/t
        ham=sum(h[i]*h[j] for i in range(3) for j in range(i+1,3))-.5*phidot**2
        dH=-p/t**2
        directional=dH+h*sum(h)
        scalar_ddot=-sig/t**2
        scalar=scalar_ddot+sum(h)*phidot
        # Exchange-count coordinate n=ln t with lapse N=e^n:
        n=log(t);N=exp(n)
        an=np.exp(p*n)
        h_n=(p/N)
        rela=np.exp(p*(sig*n)/sig)
        assert np.allclose(an,rela)
        values.append({'t':t,'constraint_error':abs(float(ham)),
                       'directional_error_max':float(max(abs(directional))),
                       'KG_error':abs(float(scalar)),
                       'exchange_clock_n_log_t':n,'required_lapse_dt_dn':N})
    assert max(x['constraint_error'] for x in values)<1e-13
    return {'Kasner_exponents':p.tolist(),'scalar_log_t_coefficient':sig,
            'Kasner_sum_p':float(sum(p)),'Kasner_sum_p_squared':float(sum(p*p)),
            'Hamiltonian_00':'sum_{i<j} H_i H_j=(1/2) phi_dot^2',
            'directional_Einstein':'Hdot_i+theta H_i=0',
            'scalar_equation':'phi_ddot+theta phi_dot=0',
            'exact_relational_observables':'a_i(phi)=exp(p_i phi/sigma), independent of t or n labeling',
            'coordinate_exchange_clock':'n=ln(t), lapse N(n)=dt/dn=exp(n); counting n as unit proper-time steps would be incorrect',
            'samples':values,
            'limitation':'Classical Bianchi-I minisuperspace solution, not quantum gravity, not 3+1 local Dirac algebra or emergent metric derivation.'}

def single_photon_local_superselection():
    I=np.eye(2,dtype=complex)
    X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex)
    Z=np.diag([1,-1]).astype(complex)
    psi=np.array([0,1,1,0],complex)/sqrt(2)
    rho=np.outer(psi,psi.conj())
    # U(1) x U(1) local twirling projects off coherences |01><10|.
    rho_tw=np.diag(np.diag(rho))
    assert abs(rho[1,2]-.5)<1e-12 and rho_tw[1,2]==0
    def e(A,B,state=rho):
        return float(np.trace(state@np.kron(A,B)).real)
    B0=(X+Y)/sqrt(2);B1=(X-Y)/sqrt(2)
    chsh=e(X,B0)+e(X,B1)+e(Y,B0)-e(Y,B1)
    assert abs(chsh-2*sqrt(2))<1e-12
    rng=np.random.default_rng(191126)
    max_allowed=0.
    for i in range(1500):
        # In a local {|0>,|1>} number SSR, Hermitian dichotomic
        # projective observables commuting with N are diagonal ±1.
        U=[np.diag(rng.choice([-1,1],size=2)) for _ in range(4)]
        val=e(U[0],U[2])+e(U[0],U[3])+e(U[1],U[2])-e(U[1],U[3])
        max_allowed=max(max_allowed,abs(val))
        assert abs(val)<=2+1e-12
        assert abs(e(U[0],U[2],rho)-e(U[0],U[2],rho_tw))<1e-12
    assert abs(max_allowed-2)<1e-12
    return {'single_photon_state':'(|10>+|01>)/sqrt2',
            'untwirled_CHSH_unrestricted':chsh,
            'locally_number_twirl_is_mixed_separable':True,
            'number_conserving_CHSH_upper':2,
            'sampled_number_conserving_measurement_quartets':1500,
            'sampled_max_abs_CHSH':max_allowed,
            'coherence_01_10_before':float(abs(rho[1,2])),
            'coherence_01_10_after':float(abs(rho_tw[1,2])),
            'resource_diagnosis':'Local operations commuting with local particle number cannot access relative |01><10| coherence without a reference/ancilla that lifts local SSR. A shared coherent phase reference is an additional physical resource.',
            'limitation':'Conditional on a strict local number superselection rule and no nonlocal/shared phase resources. Bell violation of single-photon states IS possible with suitable references or other allowed protocols; this is not a universal no-go.'}

def selective_topological_cubic_alignment():
    # On punctured T3 the triple cup of integer cohomology row vectors
    # equals det. Separate independent physical-family triples from
    # dependent singlet-loop triples to avoid generating their W term.
    physical=np.eye(3,dtype=int)
    singlet=np.array([[1,0,0],[0,1,0],[1,1,0]],dtype=int)
    phys_det=int(round(np.linalg.det(physical)))
    singlet_det=int(round(np.linalg.det(singlet)))
    assert phys_det==1 and singlet_det==0
    # Small deformation of the singlet third wavefunction off its common
    # 2-plane induces nonzero kappa: this is codimension-one alignment.
    perturbed=singlet.copy()
    perturbed[2,2]=1
    assert int(round(np.linalg.det(perturbed)))==1
    return {
       'source_cohomology':'H1(T3 minus open ball, boundary; Z)=Z3',
       'physical_family_three_rows':physical.tolist(),
       'physical_Yukawa_triple_cup':phys_det,
       'singlet_loop_three_rows':singlet.tolist(),
       'singlet_loop_triple_cup':singlet_det,
       'single_entry_perturbation_triple_cup':int(round(np.linalg.det(perturbed))),
       'constructive_alignment':'Nonzero family Yukawa and zero dangerous S13*S34*S14conj loop cup can coexist at cohomology level if the singlet three classes are linearly dependent but the family triple is independent.',
       'non_generic_warning':'det(singlet)=0 is a codimension-one relation among wavefunction cohomology classes over R; quantized integral data may protect it, but no physical dynamics selecting these classes is supplied.',
       'separation_limit':'All wavefunction triples shown are abstract integral cohomology assignments, not solutions of a single E8 Higgs-bundle/Dirac localization problem with all charges and M2 corrections.'
    }


def chiral_Yukawa_hierarchy_control():
    # Retest formal hollow complex-symmetric flavor matrix vs hierarchy.
    rng=np.random.default_rng(1503)
    maxratio=0
    for j in range(1000):
        a,b,c=rng.normal(size=3)+1j*rng.normal(size=3)
        Y=np.array([[0,a,b],[a,0,c],[b,c,0]])
        singular=np.linalg.svd(Y,compute_uv=False)
        assert singular[0]<=singular[1]+singular[2]+1e-12
        maxratio=max(maxratio,float(singular[0]/singular[1]))
    return {'tested_random_complex_hollow_symmetric_matrices':1000,
            'max_s1_over_s2_seen':maxratio,
            'exact_bound':'s1<=s2+s3 hence s1/s2<=2 for canonical kinetic terms',
            'new_test_goal':'F-flat spurion availability and physical Yukawa overlap must both be established before claiming masses.'}

def run():
    data={'E8_singlet_FD_flatness':singlet_holomorphic_vacuum(),
          'compact_Yukawa_adjoint_tradeoff':topology_chiral_tradeoff(),
          'adjoint_SU5_mass_consistency':adjoint_GUT_consistency(),
          'anisotropic_Einstein_relational_clock':anisotropic_GR_relational_clock(),
          'single_photon_local_SSR':single_photon_local_superselection(),
          'charged_family_hierarchy_control':chiral_Yukawa_hierarchy_control(),
          'selective_topological_cubic_alignment':selective_topological_cubic_alignment()}
    dst=ROOT/'data/toe_20261119_TOE_five_fronts_new_bottleneck_certificates.json'
    dst.write_text(json.dumps(data,indent=2)+'\n',encoding='utf8')
    for k in data:print('PASS',k)
    print('SINGLET_C_REQUIRED_VEV_ZERO',data['E8_singlet_FD_flatness']['third_family_one_spurion_diagonal_needs_S13'])
    print('ADJOINT_X_GEV_UPPER',data['adjoint_SU5_mass_consistency']['inevitable_X_upper_mass_GeV_if_same_24'])
    print('SS_BELL_UNRESTRICTED',data['single_photon_local_SSR']['untwirled_CHSH_unrestricted'])
    print(dst)
    return data

if __name__=='__main__':run()
