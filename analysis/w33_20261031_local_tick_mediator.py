"""A declared local Gaussian mediator gives exact event-aligning tick dynamics.

This supplies a microscopic interaction; it does not derive its existence,
spatial graph or physical scale from W33. The larger S3 wr S40 symmetry is
exposed explicitly: Hilbert-Schmidt overlap cannot see collinearity.
"""
import json,pathlib,sys,math,itertools
import numpy as np
from scipy.special import logsumexp
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261031_tick_rate_entropy import PI

def energy_matrix():
    overlaps=np.einsum('aij,bji->ab',PI,PI).real
    assert np.max(abs(overlaps-np.rint(overlaps)))<1e-12
    E=3-np.rint(overlaps).astype(int)
    assert set(E.flat)=={0,2,3}and np.array_equal(E,E.T)
    assert np.array_equal(E==0,np.eye(120,dtype=bool))
    return E

def heatbath(E,neighbors,betaJ):
    logits=-betaJ*E[:,neighbors].sum(axis=1)
    return np.exp(logits-logsumexp(logits))

def build():
    E=energy_matrix();rng=np.random.default_rng(331031)
    # Complete the square of the actual 9D Hermitian mediator action.
    identities=[]
    g=.7;mu2=1.3
    for a,b in ((0,0),(0,1),(0,3),(0,17)):
        raw=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9));F=(raw+raw.conj().T)/2;P=PI[a]+PI[b]
        direct=mu2*np.trace(F@F).real/2-g*np.trace(F@P).real
        shifted=F-g*P/mu2
        square=mu2*np.trace(shifted@shifted).real/2-g*g*np.trace(P@P).real/(2*mu2)
        assert abs(direct-square)<1e-12
        identities.append(dict(ticks=[a,b],pair_energy=int(E[a,b]),square_completion_error=abs(direct-square)))
    spectra=[]
    for betaJ in (.05,.3,1.,3.):
        x=math.exp(-betaJ);a=x**3;b=x**2;K=np.exp(-betaJ*E)
        expected=sorted([1+2*a+117*b]+[1+2*a-3*b]*39+[1-a]*80)
        assert np.max(abs(np.linalg.eigvalsh(K)-expected))<1e-12
        assert abs(1+2*a-3*b-(1-x)**2*(1+2*x))<1e-14
        spectra.append(dict(betaJ=betaJ,uniform_eigenvalue=expected[-1],
            direction_eigenvalue=1+2*a-3*b,outcome_eigenvalue=1-a,
            chain_correlation_length=1/math.log((1+2*a+117*b)/max(1-a,1+2*a-3*b))))
    # Detailed balance is checked against the full local conditional energy,
    # independently of drawing a trajectory. Also check the generator spectrum
    # on a two-site chain without allocating a 14400-square dense matrix.
    residual=0.
    for _ in range(400):
        neighbors=rng.integers(0,120,4);a,b=rng.integers(0,120,2);beta=.3
        p=heatbath(E,neighbors,beta);ea=E[a,neighbors].sum();eb=E[b,neighbors].sum()
        residual=max(residual,abs(math.exp(-beta*ea)*p[b]-math.exp(-beta*eb)*p[a]))
    assert residual<1e-14
    # A geometric finite perturbation of a constant ground state pays at
    # least 2J for each disagreeing edge, the Peierls energy condition.
    assert np.min(E[~np.eye(120,dtype=bool)])==2
    # The exact enlarged symmetry: arbitrary permutations of 40 directions,
    # and independent permutations of each direction's three outcomes.
    classes=[];unused=set(range(120))
    while unused:
        a=min(unused);C=sorted([a]+np.flatnonzero(E[a]==3).tolist());assert len(C)==3;classes.append(C);unused-=set(C)
    assert len(classes)==40
    direction={a:i for i,C in enumerate(classes)for a in C}
    assert all(E[a,b]==(0 if a==b else 3 if direction[a]==direction[b]else 2)for a,b in itertools.product(range(120),repeat=2))
    return dict(status='PASS_LOCAL_GAUSSIAN_MEDIATOR_AND_DETAILED_BALANCE',
        mediator_action='S=sum_edges [mu^2/2 Tr(Phi_e^2)-g Tr(Phi_e(Pi_a+Pi_b))], Phi_e Hermitian9x9, mu^2>0',
        exact_integrated_label_energy='J sum_edges(3-Tr(Pi_a Pi_b)), J=g^2/mu^2; label-independent Gaussian determinants and constants omitted',
        pair_energies={'same_tick':0,'same_direction_other_outcome':3,'different_directions_commuting_or_not':2},
        ground_states_on_connected_graph='Exactly120 constant event-label configurations. Optional onsite h_a quantum copies contribute the same factor3+6exp(-beta) for every label, so they do not change label selection.',
        square_completion_controls=identities,
        local_dynamics='At each vertex replace its label with probability proportional to exp[-beta J sum_neighbor E(a,b)]. This continuous-time heat-bath generator is local and reversible for the exact integrated Gibbs measure. The mediator itself can use local Ornstein-Uhlenbeck dynamics conditioned on endpoints.',
        detailed_balance_max_error=residual,finite_positive_T='Irreducible finite-volume heat-bath chain, unique stationary Gibbs measure; no finite-volume spontaneous symmetry breaking.',
        high_T_uniqueness='On a graph of maximum degree z, Dobrushin gives uniqueness if z*tanh(3 beta J/2)<1. The range of the change in a one-neighbor conditional energy is at most6J.',
        square_lattice_high_T_betaJ_bound=2*math.atanh(.25)/3,
        low_T_statement='On a supplied Z^d lattice, d>=2, the finite-range120-state model has120 symmetry-related constant periodic ground states and Peierls cost>=2J per disagreeing edge. Standard Pirogov-Sinai theory therefore gives120 ordered low-temperature phases. No explicit critical temperature or complete phase diagram is computed.',
        transfer_matrix_spectrum='1+2x^3+117x^2 (1), 1+2x^3-3x^2=(1-x)^2(1+2x) (39), 1-x^3 (80), x=exp(-beta J)',
        transfer_samples=spectra,accidental_symmetry='S3 wr S40: the interaction forgets W33 collinearity between distinct directions. This is a limitation, not an E8 vacuum-selection mechanism.',
        prior='The October19 variance audit already owns overlap blindness to W33 collinearity. Round13 auxiliary_mediator.py owns positive Gaussian matrix elimination for rank-two vacua, and Round14 pair_current_mediator.py owns a different engineered current interaction. Here this mechanism is placed on local edges for the actual rank-three120 ticks, with exact transfer spectrum and reversible kinetics. October9 q40 Potts and October21 local bond-chain constructions are different declared models. No novelty claimed for Gaussian integration, heat baths or Pirogov-Sinai theory.',
        literature=['https://doi.org/10.1007/BF01212295','https://www.math.ucla.edu/~biskup/290k.1.24w/PDFs/Zahradnik.pdf'],
        boundary='The positive mediator, coupling, spatial graph and temperature are supplied. This constructs conditional local event ordering and kinetics, not a unique physical clock, E8 real form, Lorentzian dynamics or a TOE.')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261031_local_tick_mediator.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['square_lattice_high_T_betaJ_bound'])
