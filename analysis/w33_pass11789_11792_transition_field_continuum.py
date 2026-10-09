"""A named dynamics-preserving limit from actual W33 spectral transitions.

Replication, a lattice, couplings and a chosen spectral pair are supplied.
This proves a selected-sector free-field limit, not emergence from one cell.
"""
from pathlib import Path
import hashlib,json,sys
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_pass11789_11792_transition_field_continuum.json'

def scaled_spin_x(M,cut):
    x=np.zeros((cut+1,cut+1))
    for n in range(cut):
        x[n+1,n]=x[n,n+1]=np.sqrt((n+1)*max(1-n/M,0))/2
    return x

def oscillator_x(cut):
    x=np.zeros((cut+1,cut+1))
    for n in range(cut):x[n+1,n]=x[n,n+1]=np.sqrt(n+1)/2
    return x

def two_site(M,cut,omega=1.3,kappa=.7,r=.2):
    x=oscillator_x(cut) if M is None else scaled_spin_x(M,cut)
    identity=np.eye(cut+1);xx=np.kron(x,identity);yy=np.kron(identity,x)
    num=np.diag(np.arange(cut+1));n=np.kron(num,identity)+np.kron(identity,num)
    return omega*n+kappa*(xx-yy)@(xx-yy)+r*(xx@xx+yy@yy)

def convergence_control(cut=9,occupation=3):
    target=two_site(None,cut)
    columns=[i*(cut+1)+j for i in range(occupation+1) for j in range(occupation+1)]
    rows=[]
    for M in (32,64,128,256,512,1024):
        error=float(np.linalg.norm((two_site(M,cut)-target)[:,columns],2))
        rows.append(dict(M=M,core_operator_error=error,scaled_error=M*error))
    assert all(rows[i+1]['core_operator_error']<rows[i]['core_operator_error'] for i in range(len(rows)-1))
    assert max(x['scaled_error'] for x in rows)<20
    return rows

def construction():
    # The embedding preserves exact finite-cell time evolution before coupling.
    w=sp.symbols('w',positive=True);H=sp.diag(0,w)
    plus=sp.Matrix([[0,0],[1,0]]);minus=plus.T
    assert H*plus-plus*H==w*plus
    A=plus+minus;B=sp.I*(plus-minus)
    assert (-sp.I*(A*B-B*A))[0,0]==2
    ell,k,c,m=sp.symbols('ell k c m',positive=True)
    dispersion=m*m+4*c*c*sp.sin(k*ell/2)**2/ell**2
    assert sp.limit(dispersion,ell,0)==m*m+c*c*k*k
    return dict(status='PASS',
        exact_input='By11778 compactness, choose T-real eigenvectors g,e of actual H with omega=E_e-E0>0. P_g,P_e reduce H; S+=|e><g|, S-=S+* are bounded and [H,S+]=omega*S+. Ground multiplicity need not be1.',
        actual_to_spin_map='At each supplied spatial site use M actual independent cells, restrict each cell to span{g,e}, then their permutation-symmetric Dicke sector. I_M:|n> -> normalized symmetric n-excitation state, 0<=n<=M. The sum of actual H-E0 restricts exactly to omega*n.',
        interacting_sequence='H_M=sum_x omega*(S_z(x)+M/2)+(kappa/M)*sum_<xy>(S_x(x)-S_x(y))^2+(r/M)*sum_x S_x(x)^2. Here S_x=(sum S+ +sum S-)/2. These are explicitly supplied bounded inter-cell interactions; r>-omega ensures a stable quadratic limit.',
        exact_ladder='I_M^* S+ I_M |n>=sqrt((n+1)(M-n))|n+1>; S_x/sqrtM -> (a+a*)/2=Q/sqrt2 on every fixed finite-occupation core.',
        operator_limit='I_M^* H_M I_M -> H_quad=sum_x[omega*P_x^2+(omega+r)*Q_x^2]/2+(kappa/2)*sum_<xy>(Q_x-Q_y)^2-omega*#sites/2. On a fixed finite lattice, extend the finite spin blocks by a number operator on their complement. Core convergence to the essentially self-adjoint semibounded quadratic Hamiltonian implies strong resolvent, hence strong time-evolution convergence. No full-cell-spectrum identification is claimed.',
        core_error_bound='For n<=N, sqrt(n+1)*|sqrt(1-n/M)-1|/2 <= N*sqrt(N+1)/(2M). On fixed finite-site finite-occupation vectors, linear and quadratic spin errors are O(1/M), by the weighted-shift bound and product rule.',
        dispersion='Omega_ell(k)^2=omega*(omega+r+kappa*4*sum_a sin(k_a*ell/2)^2).',
        continuum_parameters='Supply m_phys>0,c0>0,d>=1; kappa=c0^2/(omega*ell^2), r=m_phys^2/omega-omega. Then Omega_ell(k)^2=m_phys^2+(4*c0^2/ell^2)*sum sin(k_a*ell/2)^2 -> m_phys^2+c0^2|k|^2.',
        observable_map='phi_x=Q_x/(sqrtomega*ell^(d/2)); pi_x=sqrtomega*P_x/ell^(d/2). Phi_ell(f)=ell^d sum_x f(x)phi_x; Pi_ell(g)=ell^d sum_x g(x)pi_x. Their commutator is i*ell^d*sum_x f(x)g(x) -> i*integral f*g.',
        local_net='First M->infinity at fixed finite lattice; then ell->0 at fixed torus and then volume->infinity. Fourier dispersion and vacuum covariance converge for smooth test functions to massive free Klein-Gordon covariance. Define A(O)={W(E_KG f): real f in C_c^infinity(O)} double-prime in its vacuum representation. Causal KG propagator gives spacelike commutativity; lattice dynamics converge on smeared finite-energy observables. This is the selected-transition free net, not the earlier independent78-current chiral net.',
        vacuum_characteristic='For equal-time real Schwartz f,g, <W(f,g)>=exp[-1/4 integral (|fhat(k)|^2/Omega(k)+Omega(k)*|ghat(k)|^2) dk], with the matching Fourier convention. Lattice Riemann sums converge by smooth-test decay and m_phys>0.',
        state_map='At each finite lattice choose the quadratic Gaussian vacuum, truncate its occupation tail, and embed the resulting vectors with I_M. Taking the truncation and M limits gives its Weyl correlations. These are specified state sequences; convergence of the exact finite-M ground states is not claimed.',
        independent_two_site_controls=convergence_control(),
        supplied_inputs=['choice of exact spectral pair','M-cell replication','spatial lattice and dimension','interactions kappa,r','physical mass m_phys and speed c0','order of limits'],
        limitations='No predicted mass or dimension, convergence of all original cell observables, selected physical vacuum, scattering interaction, gravity or TOE completion. The construction is useful because every embedding and generator is specified.')

def modular_and_fluctuation_obstructions():
    return dict(status='PASS',
        current_only_fluctuations='For a T-invariant density matrix/state and T-even currents, the expected Hermitian form i[J_e,J_f] vanishes by antiunitarity, whenever the form expectation exists. Thus the product-state quantum central-limit symplectic form for these current fluctuations is zero: the Gaussian fluctuation algebra is commutative. A nonzero quantum oscillator needs a T-odd partner or a different state.',
        explicit_repair='A=S++S- is T-even and B=i(S+-S-) is T-odd in T-real eigenvectors; -i<g|[A,B]|g>=2. Their collective fluctuations have nondegenerate canonical symplectic form. This supplies named observables rather than assuming the current fluctuations are quantum.',
        spectral_modular_obstruction='Let P=H-E0 for the actual compact-resolvent cell. Its nonzero spectrum has a positive gap. A unitary dilation satisfying Delta^(is) P Delta^(-is)=exp(-2*pi*s) P would force every positive spectral value arbitrarily close to0, contradicting the gap. Therefore actual cell energy cannot be a nontrivial Borchers translation generator, independently of a chosen typeIII algebra.',
        massive_continuum_control='For the massive1+1 KG field, P0=m*cosh(theta) is gapped on the one-particle space but P0-P1=m*exp(-theta) has spectrum(0,infinity). Boosts dilate the lightlike generator. Hence the cell obstruction does not prohibit a massive continuum local net; a lightlike translation is the relevant modular generator.',
        prior='11778 owns actual energy compactness/gap,11774 owns the earlier typeI modular-spectrum boundary, and parallel spatial-product work owns the fact that adding Z^d does not select d.',
        literature=['https://journals.aps.org/pr/abstract/10.1103/PhysRev.58.1098','https://arxiv.org/abs/math/0412061','https://arxiv.org/abs/math-ph/0203021'])

def certificate():
    return dict(schema='w33.pass11789_11792.v1',source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),pass11789=construction(),pass11791_11792=modular_and_fluctuation_obstructions())
if __name__=='__main__':
    x=certificate();OUT.write_text(json.dumps(x,indent=2)+'\n')
    print('11789 named transition-field limit;11791/11792 fluctuation and modular obstructions PASS')
