"""Positive energy floor, central conversion and modular spectrum for11769.

The nonnumeric floor is a theorem using prior certified Lie generation and
SL78 property(T), not a numerical eigenvalue. See the companion proof report.
Prior modular15-spectator result: BT4253_BT4260, on a different harmonic kernel.
"""
from pathlib import Path
import hashlib,json,sys
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as A
OUT=ROOT/'data/w33_pass11770_11774_11776_vacuum_constraints_modular.json'


def positive_floor():
    prior=json.loads((ROOT/'data/w33_pass11767_global_current_algebra.json').read_text())
    assert prior['exact_rational_dimension']==6240
    assert prior['quotient_carrier_dimension']==78
    assert prior['rational_structure']=='sl(78,Q) semidirect Heisenberg_157(Q)'
    assert [tuple(e) for e in prior['witness']['edges']]==A.actual_edges()
    return dict(status='THEOREM_NONNUMERIC_CONSTANT',
        conclusion='There is delta>0 with H>=delta I for the nonzero-center Schrodinger representation of11769.',
        bound='delta=(epsilon/L_Q)^2, for a Kazhdan pair(Q,epsilon) of SL78(R) and the maximum current-control length L_Q on Q.',
        proof_steps=[
            'Each J_e has explicit strongly continuous unitary flow: exp(-it J_e)psi(q)=exp(-it*a*(V_e.q+a))*psi(q-t*(V_e.q+a)*U_e). U_e.V_e=0 gives Jacobian1 and preserves Schwartz space.',
            'The certified real Lie closure is sl78 semidirect h157; the generated connected group contains its SL78 Levi subgroup. The usual Schrodinger/linear-coordinate action integrates the representation.',
            'For a normalized form-domain vector, every current-control path of length L satisfies ||pi(g)psi-psi||<=L*sqrt(sum_e||J_e psi||^2). This follows by telescoping unitary products, then approximation by piecewise-constant controls.',
            'Bracket generation gives finite locally bounded control distance on the connected group; thus L_Q is finite on any compact Kazhdan set Q in the Levi subgroup.',
            'The restricted SL78 action on L2(R78) has no invariant vector: it is transitive on R78 minus0, so invariant measurable functions are constant almost everywhere and not square integrable unless zero.',
            'SL78(R) has property(T). Hence sup_Q||pi(g)psi-psi||>=epsilon||psi||. Combining gives the positive quadratic-form bound; extend from Schwartz by form closure.'],
        boundary='No numerical delta, ground-state attainment, compact resolvent or gap above an attained ground state is established.',
        literature='https://perso.univ-rennes1.fr/bachir.bekka/KazhdanTotal.pdf Theorem1.4.15')


def central_conversion():
    # Canonical coordinates (q1,q2,p1,p2), per oscillator. Original central
    # charge+1 plus auxiliary charge-1: Cq=q1+q2, Cp=p1-p2.
    omega=sp.Matrix([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])
    c=sp.Matrix([[1,1,0,0],[0,0,1,-1]])
    assert c*omega*c.T==sp.zeros(2)
    assert c.rank()==2
    return dict(status='PASS',one_mode_constraint_matrix=[list(c.row(i)) for i in range(2)],
        central_sum=0, independent_constraints=156, enlarged_phase_dimension=312,
        reduced_phase_dimension=0,
        algebra='C_A=hat(A,+1) tensor I+I tensor hat(A,-1); [C_A,C_B]=i C_[A,B], C_Z=0.',
        distribution='delta(q1+q2), constant in the relative coordinate, solves the Heisenberg constraints distributionally. It is not an L2 vector; the trace-zero SL78 action preserves it.',
        consequence='Full conversion removes all canonical degrees of freedom. A rigged-space reduction of the full Heisenberg constraints has one formal state, not a surviving matter sector.',
        boundary='Cancelling a central term alone does not construct physical gravitational constraints. Fewer constraints require a separately justified gauge principle.')


def helmert(n):
    q=np.zeros((n,n-1))
    for j in range(n-1):
        q[:j+1,j]=1/np.sqrt((j+1)*(j+2))
        q[j+1,j]=-(j+1)/np.sqrt((j+1)*(j+2))
    assert np.allclose(q.T@q,np.eye(n-1))
    return q


def modular_spectrum(t=None,f=None):
    g=A.geometry();trial=A.exact_trial()
    t=trial['t'] if t is None else t;f=trial['f'] if f is None else f
    c,ci=A.spectral_covariance(g);c=t*c;ci=ci/t
    phase=f*np.diag(g['s']);basis=helmert(40)
    qq=basis.T@c[:40,:40]@basis/2
    qp=basis.T@(c@phase)[:40,:40]@basis/2
    pp=basis.T@(ci+phase@c@phase)[:40,:40]@basis/2
    sigma=np.block([[qq,qp],[qp.T,pp]])
    omega=np.block([[np.zeros((39,39)),np.eye(39)],[-np.eye(39),np.zeros((39,39))]])
    ev=np.linalg.eigvals(1j*omega@sigma)
    assert abs(ev.imag).max()<1e-12
    nus=np.sort(ev.real[ev.real>0])
    assert np.allclose(nus,np.r_[np.full(15,.5),np.full(24,2/np.sqrt(10))],atol=3e-13)
    nu=2/np.sqrt(10);epsilon=np.log((nu+.5)/(nu-.5))
    theta,mass=sp.symbols('theta mass',real=True,positive=True)
    test=sp.Function('test')(theta)
    plus,minus=sp.exp(theta),mass**2*sp.exp(-theta)
    h,px=(plus+minus)/2,(plus-minus)/2
    def boost(x):return -sp.I*sp.diff(x,theta)
    assert sp.simplify(boost(plus*test)-plus*boost(test)+sp.I*plus*test)==0
    assert sp.simplify(boost(minus*test)-minus*boost(test)-sp.I*minus*test)==0
    assert sp.simplify(h*h-px*px-mass**2)==0
    return dict(status='PASS',point_subsystem_modes=39,
        pure_modes=15,thermal_modes=24,thermal_nu_exact='2/sqrt(10)',
        thermal_modular_energy_exact='log((4+sqrt(10))/(4-sqrt(10)))',
        thermal_modular_energy=float(epsilon),symplectic_eigenvalues=nus.tolist(),
        faithful_on_full_point_algebra=False,
        prior='BT4253_BT4260 pass4259 already owns fifteen spectators for harmonic kernel5I-A; this is the actual11769 variational state, not that kernel.',
        ritz_boundary='The11769 Hermite correction leaves the line-side15 kernel pure. The11775 point-plus-line correction has Schmidt rank at most2 on the kernel factors. Neither trial is separating for the full line algebra.',
        pure_point_obstruction=[
            'Let K have a complete eigenbasis and let positive selfadjoint P obey exp(itK)Pexp(-itK)=exp(-ct)P, c nonzero.',
            'For every K eigenvector, its P spectral probability measure is invariant under all positive dilations. Disjoint logarithmic annuli force zero measure on(0,infinity); the probability is concentrated at0.',
            'Thus P annihilates every vector of the complete K eigenbasis, hence P=0. This uses spectral covariance, not finite P moments or a domain-sensitive commutator.',
            'On the faithful thermal24-mode support, the standard modular generator epsilon*(N_left-N_right) has a complete occupation eigenbasis. It therefore cannot be a nontrivial Borchers dilation generator. Infinite Fock dimension alone does not bypass the obstruction.'],
        typeI_extension='For any faithful normal state on a typeI factor B(K), its trace-class density operator has an eigenbasis. The standard modular generator log(rho)_left-log(rho)_right therefore has a complete eigenbasis; the same obstruction applies beyond Gaussian states. This is a standard modular-theory boundary, consistent with the cited half-sided-inclusion literature, not a new general theorem.',
        constructive_escape='On L2(R,dtheta), B=-i*d/dtheta, Pplus=exp(theta), Pminus=m^2*exp(-theta) obey exact dilation relations with positive Pplus/Pminus. H=(Pplus+Pminus)/2, Pspatial=(Pplus-Pminus)/2 give H^2-Pspatial^2=m^2. This supplied1+1 kinematics has continuous boost spectrum; it is not the11769 Hamiltonian or a reconstructed local net.',
        rapidity_checks='Symbolic differential-operator commutators and the mass-shell identity were checked exactly, with supplied positive mass.',
        boundary='A geometric modular reconstruction needs a state/algebra pair with suitable continuous modular spectrum plus standard inclusions/intersections. No spacetime or Einstein equation is derived.',
        literature=['https://arxiv.org/abs/math/0412061','https://arxiv.org/abs/2111.03172'])


def principal_symbol():
    g=A.geometry();a=1/np.sqrt(20)
    q=np.r_[np.array([39]+[-1]*39)*a,np.zeros(40)]
    fields=(g['v']@q+a)[:,None]*g['u']
    assert np.linalg.matrix_rank(fields,tol=1e-9)==4
    assert np.linalg.matrix_rank(a*g['u'],tol=1e-9)==78
    active=np.flatnonzero(np.linalg.norm(fields,axis=1)>1e-9)
    gram=g['u'][active]@g['u'][active].T
    assert np.allclose(np.linalg.eigvalsh(gram),[1,1,1,24/5])
    return dict(status='PASS',principal_rank_at_origin=78,principal_rank_at_star=4,
        star_gram_eigenvalues=['1','1','1','24/5'],
        vector_field='X_e(q)=(V_e.q+a)U_e; J_e=-i X_e.partial+a(V_e.q+a)',
        affine_closure_dimension=6161,
        bracket_generation='Forget multiplication blocks r,z in the certified sl78 semidirect h157 closure: the vector fields generate sl78 semidirect R78. Its translations span every tangent space. Thus the principal fields are bracket-generating everywhere, including at rank4 star points.',
        boundary='Local bracket generation does not prove compact resolvent, localization at infinity or an excitation gap. No uniformly elliptic approximation may silently replace this rank-changing operator.')


def payload():
    return dict(schema='w33.pass11770_11774_11776.v1',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        pass11770=positive_floor(),pass11772=central_conversion(),
        pass11774=modular_spectrum(),pass11776=principal_symbol())


if __name__=='__main__':
    result=payload();OUT.write_text(json.dumps(result,indent=2,default=int)+'\n')
    print('11770 theorem: H>=delta I, delta>0; 11772/11774/11776 PASS')
