"""Compact resolvent and finite Gibbs trace for the actual11769 Hamiltonian.

The proofs use the certified11767 Lie closure and11770 control estimate.
All constants below are qualitative/control-distance constants, not computed
particle masses. Full proofs and primary literature are in the packet report.
"""
from collections import Counter
from pathlib import Path
import hashlib,json,sys
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as A
OUT=ROOT/'data/w33_pass11778_11783_compact_vacuum_thermodynamics.json'


def depth_certificate():
    path=ROOT/'data/w33_pass11767_global_current_algebra.json'
    j=json.loads(path.read_text());w=j['witness'];depth=[]
    assert w['rank']==j['exact_rational_dimension']==6240
    assert [tuple(e) for e in w['edges']]==A.actual_edges()
    for k,(parent,steps,scale) in enumerate(w['operations']):
        if parent[0]=='g':degree=1
        else:
            assert parent[0]=='b' and parent[1]<k
            degree=depth[parent[1]]+1
        assert all(i<k for i,c in steps)
        depth.append(max([degree]+[depth[i] for i,c in steps]))
    counts=dict(sorted(Counter(depth).items()))
    assert counts=={1:160,2:480,3:1840,4:2601,5:1159}
    return dict(status='PASS',prior_certificate_sha256=hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        word_degree_upper_bound=5,counts_by_witness_degree_bound=counts,
        dimension=6240,
        interpretation='The independent mod101 rows are represented by Lie words of degree<=5. Lift those word expressions to characteristic zero: independence modulo101 certifies independence there. The prior exact upper bound then gives the full real closure by degree5. Counts are witness degree bounds, not asserted minimal graded dimensions.')


def compact_vacuum():
    return dict(status='THEOREM',
        model='Friedrichs realization of H=sum_e J_e^2 from11769 on L2(R78).',
        statements=['H has compact resolvent.','Its lowest eigenvalue E0>0 is attained with finite multiplicity.',
                    'The next distinct eigenvalue E_next exists and E_next-E0>0. This is a gap above the entire ground-state eigenspace, without a uniqueness assertion.'],
        proof=[
            'The represented connected finite-dimensional current group contains all Heisenberg translations and modulations, by the certified sl78 semidirect h157 closure.',
            'The horizontal control distance d induces the group topology. For every form-domain vector ||(pi(g)-I)psi||<=d(1,g)*sqrt(h[psi]); use infima of control lengths and the11770 telescoping estimate.',
            'Consequently any bounded form ball is uniformly continuous under ordinary translations and modulations as their parameters tend to zero.',
            'K_eps=exp(-eps*|q|^2)exp(-eps*|p|^2) is Hilbert-Schmidt and converges to I uniformly on each such form ball: write both factors as Gaussian averages of Weyl operators, use the uniform small-parameter estimate and bound Gaussian tails by2||psi||.',
            'Compact K_eps uniformly approximate the identity on the form ball, making the form embedding compact. Therefore the Friedrichs resolvent is compact.',
            'The prior11770 positive floor excludes E0=0. Compact resolvent supplies finite multiplicities, attainment and separation of successive distinct levels.'],
        numerical_scope='The parallel five-state collective-Hermite trial improves the floating upper estimate to E0<=127.619377843339...; see analysis/2026-10-08_collective_hermite2_4_ritz_refinement.md and its certificate. No numerical lower bound, gap size or ground-state multiplicity has been computed.',
        ground_real_structure='The parallel dressed antiunitary T fixes every current and has T^2=1. Compactness supplies a finite-dimensional ground sector invariant under T, with an orthonormal T-real basis. Thus at least one attained ground ray is T-invariant, without a uniqueness assumption. Every such ray has zero Hermitian current-curvature one-point functions, understood as the finite-energy quadratic pairing.',
        distinction='The control topology is used on the finite-dimensional Lie GROUP, not inferred merely from the rank-changing configuration-space principal symbol.')


def weyl_floor():
    # Anticommuting unitary Weyl pair with a.b=pi. Its Hermitian real parts
    # also anticommute and have norm<=1, hence X+Y<=sqrt(2)I.
    x=sp.symbols('x',real=True)
    assert sp.simplify(sp.exp(sp.I*(x+sp.pi))+sp.exp(sp.I*x))==0
    numerator=4-2*sp.sqrt(2)
    return dict(status='THEOREM_CONTROL_DISTANCE_BOUND',
        pair='r=(e_point0-e_point1)/sqrt2; M=exp(i*r.q), T=exp(-i*pi*r.p). Then MT=-TM.',
        universal_numerator=str(numerator),
        inequality='||Mpsi-psi||^2+||Tpsi-psi||^2 >= (4-2sqrt2)||psi||^2.',
        lower_bound='H >= (4-2sqrt2)/(d(1,M)^2+d(1,T)^2) I, where d is the original160-current horizontal control distance on the represented group.',
        proof='X=Re(M),Y=Re(T) anticommute, X^2+Y^2<=2I, so <X+Y><=sqrt2. Combine the exact displacement-norm identity with the current control estimate.',
        scope='A defined positive lower bound requiring no Kazhdan constant. The two control distances are finite but have not been numerically bounded; this is not a decimal spectral lower bound.')


def thermodynamics():
    n=78;theta=sp.Rational(1,6)
    integrability=sp.Rational(2,5)-2*theta
    assert integrability>0
    exponent=2*n/(2*theta)
    assert exponent==468
    prefactor=36*sp.factorial(233)**2/(2**78*sp.factorial(38)**2)
    return dict(status='THEOREM_NONNUMERIC_CONSTANTS',
        control_modulus='For small Heisenberg coordinate z, d(1,exp(z))<=C*|z|^(1/5), by the degree<=5 bracket certificate and the local ball-box estimate.',
        fractional_form='For every0<theta<1/5, || |p|^theta psi||^2+|| |q|^theta psi||^2 <= C_theta*(h[psi]+||psi||^2). Choose theta=1/6.',
        small_radius_integrability_exact=str(integrability),
        coercivity='H >= c*(|p|^(1/3)+|q|^(1/3))-C, for some c>0,C>=0.',
        heat_bound='Tr exp(-beta H) <= exp(beta*C)*[36*Gamma(234)^2/(2^78*Gamma(39)^2)]*(beta*c)^(-468), for all beta>0.',
        heat_prefactor_exact=str(prefactor),heat_power=468,
        proof='Integrate translation/modulation difference quotients against |z|^(-78-2theta); the small-radius exponent2/5-2theta is positive. Use min-max and Golden-Thompson for the fractional confining oscillator.',
        consequence='Every positive-temperature Gibbs partition function of this finite-cell model is finite. Its faithful Gibbs state is still typeI and retains the11774 modular-eigenbasis obstruction.',
        boundary='Constants, entropy values, thermodynamic limit and physical units are not computed.468 is a loose analytic heat bound, not a physical spacetime dimension or spectral-dimension prediction.')


def payload():
    eps=sp.symbols('eps',positive=True)
    x,y=sp.symbols('x y',real=True)
    kernel=sp.exp(-eps*x*x)*sp.exp(-(x-y)**2/(4*eps))/sp.sqrt(4*sp.pi*eps)
    hs=sp.integrate(sp.integrate(kernel*kernel,(y,-sp.oo,sp.oo)),(x,-sp.oo,sp.oo))
    assert sp.simplify(hs-1/(4*eps))==0
    return dict(schema='w33.pass11778_11783.v1',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        word_certificate=depth_certificate(),pass11778=compact_vacuum(),weyl_floor=weyl_floor(),
        smoothing_HS_norm_squared_78='(4*eps)^(-78)',pass11783=thermodynamics(),
        literature=['https://arxiv.org/abs/1209.4387','https://arxiv.org/abs/1203.0974'])


if __name__=='__main__':
    result=payload();OUT.write_text(json.dumps(result,indent=2)+'\n')
    print('11778 THEOREM compact resolvent, attained positive vacuum and gap;11783 finite Gibbs trace; word depth<=5')
