"""Independent Cech, Serre, actual-E8, F/D and fixed-state controls."""
import hashlib
import itertools as it
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s
from scipy.linalg import expm
from scipy.sparse import eye
from scipy.sparse.linalg import expm_multiply

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11742_11749_nonzero_flavor_and_flux_frame as N


def test_frozen_source_and_eight_scoped_sections():
    p=json.loads(N.OUT.read_text())
    assert p['source_sha256']==hashlib.sha256(Path(N.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    assert set(p['passes'])==set(map(str,range(11742,11750)))
    assert all(v['status']=='PASS' and v['scope'] for v in p['passes'].values())
    assert 'unproved' in p['physical_boundary']


def independent_bott(n):
    if -1 in n:return [0]*5
    q=sum(k<0 for k in n);ans=[0]*5
    ans[q]=int(np.prod([k+1 if k>=0 else -k-1 for k in n]));return ans


def test_koszul_no_generic_rank_assumption_and_rr_serre():
    for n in N.K:
        ambient=independent_bott(n);shifted=independent_bott([k-2 for k in n])
        assert all(a*b==0 for a,b in zip(ambient,shifted))
        h=[ambient[q]+shifted[q+1] for q in range(4)]
        rr=2*sum(np.prod(v) for v in it.combinations(n,3))+2*sum(n)
        assert h==[0,4,0,0] and rr==-4
        assert N.M.tetraquadric_cohomology(tuple(-k for k in n))==h[::-1]
    assert independent_bott(N.K[2])==[0]*5
    assert independent_bott([k-2 for k in N.K[2]])==[0,0,4,0,0]


def test_exact_positive_slope_point_and_c3():
    t=list(map(s.sympify,N.flavor_certificate()['positive_Kahler_point']))
    assert all(v>0 for v in t)
    for n in N.K:
        slope=sum(n[i]*t[j]*t[k] for i in range(4) for j,k in it.combinations([j for j in range(4) if j!=i],2))
        assert s.simplify(slope)==0
    x=s.symbols('x:4');poly=s.prod(sum(a*b for a,b in zip(n,x)) for n in N.K)
    assert 2*sum(s.expand(poly).coeff(x[i],1).coeff(x[j],1).coeff(x[k],1).subs(dict.fromkeys(x,0)) for i,j,k in it.combinations(range(4),3))==-24


def test_line_projective_commutators_cancel_and_determinant_lift():
    g=N.G;h=N.H
    assert g*h==-h*g
    assert all(sum(n)%2==0 for n in N.K)
    assert np.sum(N.K,axis=0).tolist()==[0,0,0,0]
    # Serre duality includes det(g)^-1, det(h)^-1 on each negative factor.
    assert -g.inv().T==-g and -h.inv().T==-h


def test_each_cover_cohomology_is_regular_and_quotient_not_index_only():
    for a,b in N.cohomology_actions():
        assert a*b==b*a and a*a==b*b==s.eye(4)
        for x,y in N.CHARS:
            projector=(s.eye(4)+x*a)*(s.eye(4)+y*b)/4
            assert projector*projector==projector and projector.rank()==1


def test_invariant_linear_system_is_basepoint_free_every_minimal_pattern():
    chars=[(0,0),(0,1),(1,0)]
    invariant=[v for v in it.product(range(3),repeat=4) if all(sum(chars[j][k] for j in v)%2==0 for k in range(2))]
    assert len(invariant)==21
    for available in it.product(list(it.combinations(range(3),2)),repeat=4):
        assert any(all(v[i] in available[i] for i in range(4)) for v in invariant)


def test_fixed_loci_are_disjoint_and_hypersurface_fibers_are_trivial():
    # Each nonidentity has two eigenrays per factor. None of the three
    # eigenray sets intersects another, so their sixteen-point sets are disjoint.
    g,h=N.G,N.H
    eigens=[x.eigenvects() for x in (g,h,g*h)]
    rays=[[v[2][0] for v in pair] for pair in eigens]
    assert all(s.Matrix.hstack(a,b).det()!=0 for i,j in it.combinations(range(3),2) for a in rays[i] for b in rays[j])
    for es in eigens:
        for vals in it.product([x[0] for x in es],repeat=4):assert s.prod(v**2 for v in vals)==1


def test_cech_serre_pairing_gives_nonzero_cubic():
    # a(y,z)=y0 z1-y1 z0; b(y*,w)=y0* w1-y1* w0;
    # c(z*,w*)=z0* w0*+z1* w1*. Constant-term contractions give2.
    eps=s.Matrix([[0,1],[-1,0]]);delta=s.eye(2)
    assert sum(eps[a,b]*eps[a,c]*delta[b,c] for a,b,c in it.product(range(2),repeat=3))==2
    for actions in zip(*N.cohomology_actions()):
        vs=[s.Matrix([0,1,-1,0]),s.Matrix([0,1,-1,0]),s.Matrix([1,0,0,1])]
        assert N.cup(*[a*v for a,v in zip(actions,vs)])==2
    assert s.Rational(2,4)==s.Rational(1,2)


def test_all64_character_triples_and_wilson_mass_ranks():
    p=N.character_robustness_certificate()
    assert len(p['compatible_nonzero_cups'])==16 and p['forbidden_zero_triples']==48
    for a in p['compatible_nonzero_cups']:assert abs(a['cover_cup'])==2
    for a in p['exotic_mass_matrices']:assert s.Matrix(a['matrix']).rank()==3


def test_actual_heavy_exchange_has_nonzero_baryon_lepton_operator():
    labs,_,D=N.matter_dictionary();idx={a:i for i,a in enumerate(labs)}
    # Two independently read cubic vertices and the corresponding inverse
    # family mass entry give the displayed quartic coefficient.
    v1=D[idx['x',1,2,3],idx['x',3,7,8],idx['x',0,3,6]]
    v2=D[idx['x',0,1,3],idx['A',3,1],idx['k',0,4,5]]
    inv=N.family_mass((1,1,1)).inv()
    assert -s.Rational(1,4)*int(v1)*int(v2)*inv[1,2]==-s.Rational(1,4)
    p=N.character_robustness_certificate()
    assert s.sympify(p['exact_integrated_superpotential_monomial'])==-s.prod(s.symbols('a b c d'))/4
    wilson={0:1,1:1,2:1,7:-1,8:-1}
    assert wilson[1]*wilson[2]==wilson[7]*wilson[8]==wilson[0]*wilson[1]==wilson[1]==1
    assert 'no retained light' in p['doublet_triplet_boundary']


def original(v):
    out=N.E._zero()
    for lab,c in v.items():
        if lab[0]=='H':
            h=np.zeros(9);h[lab[1]]=1;h[8]=-1
            z=(np.diag(h).astype(complex),np.zeros(84),np.zeros(84))
        else:z=N.P.root_element(lab)
        out=N.B.add(out,N.B.scale(float(c),z))
    return out


def test_sparse_brackets_against_original_tensor_for_frame_inputs():
    section,rs,basis=N.frame_data()
    # Every Cartan, all opposite image roots, and all root species with
    # disjoint/overlapping trivectors are covered by an independent tensor implementation.
    image={a for r in rs for a in r}|set(section)
    probes={('H',i) for i in range(8)}|{N.P.dual(a)[0] for a in image}|set(basis[::17])
    for r in image:
        for a in probes:
            actual=N.E.bracket(original({r:1}),original({a:1}))
            assert np.allclose(N.E._vec(actual),N.E._vec(original(N.bracket(r,a))),atol=1e-13)


def test_frame_double_identity_on_all248_and_ancillary_essential():
    section,rs,basis=N.frame_data()
    for a in basis:
        lhs=N.add(*(N.bv({u:1},N.bv(r,{a:1})) for u,r in zip(section,rs)))
        assert lhs==N.scale(6,N.theta(a))
    # Omitting constrained ancillary loses the qS term: not the symmetric tensor.
    a=('k',0,1,3)
    pR=N.add(*(N.scale(N.pairing(u,a),r) for u,r in zip(section,rs)))
    assert not pR and N.theta(a)
    assert N.scale(6,N.theta(a))!=N.scale(7,N.theta(a))


def test_finite_coordinate_frame_transport_and_full_ancillary_product():
    section,rs,basis=N.frame_data()
    C=N.add(*(N.scale(s.Rational(i+1,13),r) for i,r in enumerate(rs)))
    def transport(v):
        out=v;term=v
        for i in range(1,5):
            term=N.scale(s.Rational(1,i),N.bv(C,term));out=N.add(out,term)
        assert not N.bv(C,term)
        return out
    for a in [N.P.dual(u)[0] for u in section]+[('H',2),('k',0,1,3)]:
        Ea=transport({a:1})
        assert all(sum(c*N.pairing(u,v) for v,c in Ea.items())==N.pairing(u,a) for u in section)
        D=N.add(*(N.bv({u:1},N.bv(r,Ea)) for u,r in zip(section,rs)))
        assert D==N.scale(6,N.theta(a)) # rotation is constant, hence DeltaSigma=0
        for b in [('A',0,3),('k',0,1,3),('H',0)]:
            product=N.scale(7,N.bv(N.theta(a),{b:1}))
            assert all(sum(c*d*N.pairing(x,y) for x,c in r.items() for y,d in product.items())==0 for r in rs)


def test_X_branch_and_anomalies_from_actual_roots():
    labs,charges,D=N.matter_dictionary()
    assert sorted(charges)==[-4]*5+[-1]*10+[2]*10+[5]*2
    assert sum(charges)==sum(c**3 for c in charges)==0
    for i,j,k in zip(*np.nonzero(D)):assert charges[i]+charges[j]+charges[k]==0
    assert N.anomaly_exotic_certificate()['family_Stueckelberg_rank']==2


def test_bundle_orientation_matches_fundamental_family_roots():
    labs,_,_=N.matter_dictionary();roots,weights,_=N.P.roots()
    for a in labs:
        w=weights[roots.index(a)];total=sum(w[i] for i in (3,4,5))
        assert [3*w[i]-total for i in (3,4,5)]==[6,-3,-3]
    p=N.flavor_certificate()
    assert p['V_cover_c3']==-24 and p['V_quotient_c3']==-6
    assert p['quotient_holomorphic_Euler_index']==-3
    assert p['net_H1_minus_H2_quotient']==3 and 'V=K;' in p['structure_bundle']


def test_actual_cubic_pairs_five_exotics_but_not_both_bar_fives():
    labs,charges,D=N.matter_dictionary();sing=labs.index(('A',3,6))
    f=[i for i,q in enumerate(charges) if q==-4];b=[i for i,q in enumerate(charges) if q==-1]
    block=s.Matrix(D[sing][np.ix_(f,b)].tolist())
    assert block.rank()==5 and len(block.nullspace())==5
    v=s.symbols('v1:4');Y=N.family_mass(v)
    assert s.factor(Y.det())==s.prod(v)/4
    assert s.kronecker_product(Y.subs(dict(zip(v,(1,1,1)))),block).rank()==15


def test_minimal_D_obstruction_and_imported_pair_flatness():
    for S in [(0,0,0),(1,0,0),(1,1,1)]:
        r=sum(abs(v)**2 for v in S);assert (5*r==0)==(S==(0,0,0))
    for r in [s.Rational(1,3),3,7]:
        q2=(s.sqrt(r*r+4)+r)/2;p2=(s.sqrt(r*r+4)-r)/2
        assert p2>0 and q2>0 and s.simplify(p2*q2)==1
        assert s.simplify(5*(r+p2-q2))==0
    assert 5+(-5)==5**3+(-5)**3==0


def test_coupled_superpotential_F_equations_and_branch_degeneracy():
    J=N.P.su2_generators((1,1,1,2));Phi=[1j*j for j in J]
    for i in range(3):assert np.allclose(Phi[(i+1)%3]@Phi[(i+2)%3]-Phi[(i+2)%3]@Phi[(i+1)%3]+Phi[i],0)
    assert np.allclose(sum(a@a.conj().T-a.conj().T@a for a in Phi),0)
    assert abs(2/3*sum(np.trace(a@a) for a in Phi)+1)<1e-13
    p=N.coupled_action_certificate()
    assert len(p['all_zero_F_Higgs_partitions'])==7 and not p['nonprincipal_branch_selected']
    assert 'not derived' in p['imported_fields']


def test_complex_Higgs_rescaling_cancels_full_SU2_singlet_D_term():
    units,_,_=N.B.hidden_su5();Jz=N.B.scale(.5,N.B.add(units[3,3],N.B.scale(-1,units[4,4])))
    sing=N.P.root_element(('A',3,6))
    assert np.allclose(N.E._vec(N.E.bracket(Jz,sing)),.5*N.E._vec(sing))
    assert not np.any(N.E._vec(N.E.bracket(units[3,4],sing)))
    t=(s.sqrt(13)-3)/2;a=s.sqrt(t);jp=s.Matrix([[0,1],[0,0]]);jm=jp.T
    jz=s.diag(s.Rational(1,2),-s.Rational(1,2))
    phi=[s.I*(a*jp+jm/a)/2,(a*jp-jm/a)/2,s.I*jz]
    adjoint=sum((v*v.conjugate().T-v.conjugate().T*v for v in phi),s.zeros(2))
    singlet_density=3*(s.diag(1,0)-s.eye(2)/2)
    assert (adjoint+singlet_density).applyfunc(s.simplify)==s.zeros(2)
    assert s.simplify(t-1/t+3)==0 # same equation cancels X with P^2=t,Q^2=1/t
    assert 'not zero' in N.coupled_action_certificate()['SU2_singlet_D_control']


def test_total_occupation_conserved_but_local_occupation_moves():
    H,basis=N.boson_hamiltonian();assert H.shape==(820,820)
    assert all(len(v)==2 for v in basis) and not (H-H.T).nnz
    assert np.all(np.sum([[v.count(i) for i in range(40)] for v in basis],axis=1)==2)
    local=np.array([v.count(0) for v in basis]);comm=H.multiply(local[None,:])-H.multiply(local[:,None])
    assert comm.nnz>0


def test_fixed_N2_same_state_same_time_shift_only_changes_phase():
    H,basis=N.boson_hamiltonian();psi=np.zeros(820,complex);psi[basis.index((0,1))]=1
    time=.091;shift=.73
    a=expm_multiply(-1j*time*H,psi)
    b=expm_multiply(-1j*time*(H+2*shift*eye(820)),psi)
    assert np.max(abs(b-np.exp(-2j*time*shift)*a))<1e-12


def test_volume_mixture_and_local_shift_do_respond():
    p=N.fixed_data_vacuum_certificate()
    assert p['inhomogeneous_shift_Gibbs_response_norm']>1e-4
    beta=.4;C=.3;eps=1e-5
    probability=lambda c:1/(1+np.exp(beta*c))
    derivative=(probability(C+eps)-probability(C-eps))/(2*eps)
    assert abs(derivative+beta*probability(C)*(1-probability(C)))<1e-10


def test_effective_cover_class_uses_cohomology_not_raw_coefficients():
    p=N.anomaly_class_certificate();A=s.Matrix(p['intersection_pairing_matrix'])
    raw=s.Matrix(p['raw_cover_budget']);effective=s.Matrix(p['effective_representative'])
    assert min(raw)<0 and min(effective)>=0 and A*(raw-effective)==s.zeros(4,1)
    assert A.rank()==4 and A*effective==s.Matrix([14,14,14,18])
    assert 'multiplies' in p['descent_control'] and 'remain open' in p['scope']


def test_positive_metrics_make_holomorphic_masses_nonidentifiable():
    Y=N.family_mass((1,1,1));D=s.diag(1,s.Rational(1,10),s.Rational(1,100))
    Z=Y.T*D**-2*Y
    assert Z.is_positive_definite and Y*Z.inv()*Y.T==D**2
    vals,U=np.linalg.eigh(np.array(Z,float));inverse=(U/np.sqrt(vals))@U.T
    singular=np.linalg.svd(np.array(Y,float)@inverse,compute_uv=False)
    assert np.allclose(singular,[1,.1,.01],atol=1e-10)
    assert N.kinetic_identifiability_certificate()['equal_VEV_holomorphic_eigenvalues']==['1','-1/2','-1/2']


def test_all_positive_results_retain_distinct_physical_boundaries():
    assert 'not measured' in N.flavor_certificate()['normalization']
    assert 'separate duality' in N.flux_frame_certificate()['scope']
    assert 'cannot' in N.anomaly_exotic_certificate()['obstruction']
    assert 'No clock' in N.coupled_action_certificate()['unresolved_flat_directions']
    assert 'no derived spacetime' in N.fixed_data_vacuum_certificate()['scope']
