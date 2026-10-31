"""Local positive-mass current mediation restores W33 relation sensitivity.

The mechanism is supplied, with its sign and enlarged residual symmetry
explicit. It extends Round14 current mediation and the preceding edge model.
"""
import pathlib,sys,json,math
import numpy as np
from scipy.special import logsumexp
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261031_tick_rate_entropy import PI
from w33_pass12055_microscopic_tick_model import ADJ
from w33_20261031_local_tick_mediator import energy_matrix

def current_cost():
    products=PI[:,None,:,:]@PI[None,:,:,:]
    comm=products-products.swapaxes(0,1)
    C=np.sum(abs(comm)**2,axis=(2,3))
    expected=(4/3)*np.kron(np.ones((40,40))-np.eye(40)-ADJ,np.ones((3,3)))
    assert np.max(abs(C-expected))<1e-12
    return expected

def spectrum(beta,J,K):
    o=math.exp(-3*beta*J);c=math.exp(-2*beta*J);n=math.exp(-beta*(2*J-4*K/3))
    return [(1+2*o+36*c+81*n,1),(1+2*o+6*c-9*n,24),(1+2*o-12*c+9*n,15),(1-o,80)]

def heatbath(E,neighbors,beta):
    logp=-beta*E[:,neighbors].sum(1);return np.exp(logp-logsumexp(logp))

def build():
    E0=energy_matrix();C=current_cost();rng=np.random.default_rng(20261031)
    # One edge mediator, not one field for every pair of possible labels.
    # j=i[Pi_a,Pi_b] is Hermitian and traceless.
    controls=[]
    for a,b in ((0,0),(0,1),(0,3),(0,15)):
        j=1j*(PI[a]@PI[b]-PI[b]@PI[a]);mu2=1.7;g=.9
        raw=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9));B=(raw+raw.conj().T)/2
        B-=np.trace(B)*np.eye(9)/9
        direct=mu2*np.trace(B@B).real/2-g*np.trace(B@j).real
        shifted=B-g*j/mu2
        square=mu2*np.trace(shifted@shifted).real/2-g*g*np.trace(j@j).real/(2*mu2)
        assert abs(direct-square)<1e-12
        controls.append(dict(ticks=[a,b],current_norm=float(C[a,b]),square_completion_error=abs(direct-square)))
    samples=[]
    for K in (0.,.5,1.5,2.):
        for beta in (.2,1.,3.):
            E=E0-K*C;W=np.exp(-beta*E)
            eig=np.linalg.eigvalsh(W);expected=sorted(v for value,mult in spectrum(beta,1.,K)for v in [value]*mult)
            assert np.max(abs(eig-expected))<1e-10
            p=heatbath(E,[0,3,14,28],beta);weights=np.exp(-beta*E[:,[0,3,14,28]].sum(1))
            assert np.max(abs(weights[:,None]*p[None,:]-weights[None,:]*p[:,None]))<1e-10
            samples.append(dict(J=1,K=K,beta=beta,spectrum=spectrum(beta,1.,K)))
    assert np.allclose(C[np.ix_([0,1,2],[0,1,2])],0)
    return dict(status='PASS_LOCAL_W33_SENSITIVE_MEDIATION',
        mediator='For each oriented spatial edge, add a traceless Hermitian9x9 B_e with mu_c^2/2 Tr B_e^2-g_c Tr(B_e i[Pi_a,Pi_b]), mu_c^2>0. Reversing the edge reverses B and current. Complete its square.',
        exact_effective_energy='E_ab=J(3-Tr Pi_a Pi_b)-K ||[Pi_a,Pi_b]||_F^2, J>=0, K=g_c^2/(2 mu_c^2)>=0.',
        pair_costs=['same tick:0','same direction, other outcome:3J','distinct commuting directions:2J','noncommuting directions:2J-4K/3'],
        square_completion_controls=controls,transfer_samples=samples,
        exact_zero_T_threshold='K=3J/2. For J>0 and0<=K<3J/2 every unlike tick costs at least min(2J,2J-4K/3)>0, so connected-graph label ground states are the120 constant events. On a supplied bipartite spatial graph, K>3J/2 allows a noncommuting two-sublattice pair to minimize every edge, so constant events cease to be ground states. At equality both types coexist among many possible ground patterns.',
        low_T_scope='Below the threshold, the finite120-state short-range model satisfies the Peierls condition and has transitive constant ground states, giving ordered low-T phases on supplied Z^d,d>=2 by standard Pirogov-Sinai theory. Above it, no complete ground-state or finite-T classification is claimed.',
        transfer_eigenvalues='1+2o+36c+81n (1),1+2o+6c-9n (24),1+2o-12c+9n (15),1-o (80); o=e^-3betaJ,c=e^-2betaJ,n=e^-beta(2J-4K/3).',
        restored_geometry='For J>0,K>0 the colored pair relation determines Pauli direction triples and W33 collinearity. The former S3 wr S40 symmetry reduces to S3^40 semidirect Aut(W33); independent outcome relabelings remain an enlarged symmetry beyond physical Clifford covariance.',
        stochastic_dynamics='Local conditional heat bath obeys detailed balance for this exact energy, including negative bond energies. It is thermal kinetics, not a fundamental time arrow.',
        prior='Round14 pair_current_mediator.py owns the stable current-elimination mechanism for rank-two vacuum mixtures. The preceding local_tick_mediator.py owns Gaussian edge alignment. Here one field per spatial edge couples the actual rank-three tick current, recovering the24+15 W33 sectors and exact coupling threshold.',
        boundary='Spatial graph, mediator content, couplings, temperature and quantum interpretation are supplied. No measured particle, unique E8 real form, causal metric, UV completion or physical vacuum selection derived.')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261031_geometry_sensitive_mediator.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'])
