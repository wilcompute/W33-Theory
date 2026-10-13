"""Coupled compact rotor and fermions, solved in Gauss' physical Hilbert space.

Native8-link octagon subsystem plus a separate standard1D refinement control.
Not the full1385-plaquette W33 Hamiltonian or a4D chiral continuum theory.
"""
from pathlib import Path
import itertools
import json
import sys
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
from scipy.optimize import minimize_scalar

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))


def physical_basis(N,cutoff,static=None):
    assert N%2==0 and N>=4
    static=np.zeros(N,dtype=int) if static is None else np.asarray(static,dtype=int)
    assert sum(static)==0
    background=np.arange(N)%2
    patterns=[]
    for filled in itertools.combinations(range(N),N//2):
        occ=np.zeros(N,dtype=int);occ[list(filled)]=1
        patterns.append(occ)
    basis=[];flux=[];occupation=[]
    for occ in patterns:
        bits=sum(int(x)<<i for i,x in enumerate(occ))
        charge=occ-background+static
        for winding in range(-cutoff,cutoff+1):
            n=winding+np.cumsum(charge)
            assert np.array_equal(np.roll(n,1)-n+charge,np.zeros(N,dtype=int))
            basis.append((bits,winding));flux.append(n);occupation.append(occ)
    return basis,np.array(flux),np.array(occupation)


def matrix(N,cutoff,electric=.64,hopping=.7,mass=.3,magnetic=.625,static=None,electric_offset=0.):
    # electric coefficient is g²*a, magnetic coefficient beta/g².
    basis,flux,occ=physical_basis(N,cutoff,static)
    positions={s:i for i,s in enumerate(basis)}
    diagonal=electric*np.sum((flux+electric_offset)**2,axis=1)/2+mass*(occ@((-1.)**np.arange(N)))+magnetic
    rows=list(range(len(basis)));cols=rows.copy();values=diagonal.tolist()
    transitions=[]
    for i,(bits,winding) in enumerate(basis):
        for a in range(N):
            b=(a+1)%N
            if occ[i,a]==occ[i,b]:continue
            direction=1 if occ[i,a] else -1  # + means a->b; flux_a lowers.
            target=(bits^(1<<a)^(1<<b),winding-direction if a==N-1 else winding)
            if target not in positions:continue
            j=positions[target]
            # Jordan-Wigner fermion sign, including the periodic boundary.
            sign=(-1)**int(np.sum(occ[i,min(a,b)+1:max(a,b)]))
            rows.append(i);cols.append(j);values.append(-hopping*sign)
            expected=np.zeros(N,dtype=int);expected[a]=-direction
            assert np.array_equal(flux[j]-flux[i],expected)
            if len(transitions)<20:transitions.append((i,j,a,direction))
        if magnetic:
            for step in (-1,1):
                target=(bits,winding+step)
                if target in positions:
                    rows.append(i);cols.append(positions[target]);values.append(-magnetic/2)
    H=coo_matrix((values,(rows,cols)),shape=(len(basis),len(basis))).tocsr()
    assert (H-H.T).nnz==0
    return H,basis,flux,occ,transitions


def solve(N,cutoff,**parameters):
    H,basis,flux,occ,transitions=matrix(N,cutoff,**parameters)
    v0=np.random.default_rng(11969+N).normal(size=H.shape[0])
    ev,U=eigsh(H,k=3,which='SA',tol=1e-11,v0=v0)
    order=np.argsort(ev);ev=ev[order];U=U[:,order]
    p=abs(U[:,0])**2
    boundary=np.array([abs(w)==cutoff for _,w in basis])
    residual=float(np.linalg.norm(H@U[:,0]-ev[0]*U[:,0]))
    assert residual<1e-8
    return dict(dimension=len(basis),ground_energy=float(ev[0]),gap=float(ev[1]-ev[0]),
                second_gap=float(ev[2]-ev[0]),boundary_probability=float(p@boundary),
                mean_occupations=(p@occ).tolist(),electric_flux_second_moment=float(p@np.sum(flux*flux,axis=1)),
                eigenpair_residual=residual)


def native_octagon():
    from w33_20261010_toe38_local_maxwell_2complex import prep
    edges,volts,lookup,octs,*_=prep();walk=octs[0]
    vertices=walk[:-1];assert len(vertices)==len(set(vertices))==8
    B=np.zeros((160,80),dtype=int)
    for i,(a,b) in enumerate(edges):B[i,a]=-1;B[i,b]=1
    _,flux,occ=physical_basis(8,2)
    embedded=np.zeros((len(flux),160),dtype=int)
    charge=np.zeros((len(flux),80),dtype=int)
    charge[:,vertices]=occ-np.arange(8)%2
    for k,(a,b) in enumerate(zip(walk,walk[1:])):
        edge=lookup[tuple(sorted((a,b)))];sign=1 if edges[edge][0]==a else -1
        embedded[:,edge]=sign*flux[:,k]
    assert np.max(abs(embedded@B+charge))==0
    # Bare fermion hopping at unchanged flux violates two Gauss generators.
    bad=np.zeros(80,dtype=int);bad[vertices[0]]=-1;bad[vertices[1]]=1
    assert np.count_nonzero(bad)==2
    sweep=[dict(cutoff=L,**solve(8,L)) for L in (1,2,3,4)]
    assert abs(sweep[-1]['ground_energy']-sweep[-2]['ground_energy'])<1e-6
    return dict(native_vertices=list(map(int,vertices)),native_Gauss_max_residual=0,
                physically_coupled_site_fermions=8,background_occupations=(np.arange(8)%2).tolist(),
                full_fermion_pattern_count=70,flux_cutoff_sweep=sweep,
                bare_fermion_hop_negative_control_nonzero_Gauss_generators=2,
                operator_rule='For oriented a->b hopping psi_b† psi_a, rotor lowers n_ab by1. Fermion charge change and electric divergence change cancel at both vertices; a bare fermion hop without rotor does not commute with Gauss.',
                scope='All8 site fermions and the global rotor integer are quantum and interact. This is the chosen native octagon subsystem with boundary exterior links frozen; full native hopping and all other plaquette shifts do not preserve this subsystem.')


def screened_circle(distance,e,length):
    photon_mass=e/np.sqrt(np.pi)
    return e*e*(np.cosh(photon_mass*length/2)-np.cosh(photon_mass*(length/2-distance)))/(2*photon_mass*np.sinh(photon_mass*length/2))


def shifted_mass_symmetry():
    from fractions import Fraction as F
    N=8;cutoff=3;electric=F(49,100);mass=-electric/8
    basis,flux,occ=physical_basis(N,cutoff);index={s:i for i,s in enumerate(basis)}
    rows=[];cols=[];values=[];energies=[]
    for i,(bits,winding) in enumerate(basis):
        shifted=np.roll(occ[i],-1)
        target=(sum(int(x)<<j for j,x in enumerate(shifted)),winding+int(occ[i,0]))
        nt=np.roll(flux[i],-1)+(1+(-1)**np.arange(N))//2
        # Exact untruncated identity: theta -> theta-pi, n' +alpha'
        # = roll(n+alpha) + (-1)^i/2. Background is crucial.
        e0=electric*sum(int(x)**2 for x in flux[i])/2+mass*sum(int((-1)**j*x) for j,x in enumerate(occ[i]))
        e1=electric*sum((F(int(x))-F(1,2))**2 for x in nt)/2+mass*sum(int((-1)**j*x) for j,x in enumerate(shifted))
        assert e0==e1;energies.append(e0-e1)
        if target in index:
            j=index[target]
            assert np.array_equal(flux[j],nt)
            rows.append(j);cols.append(i);values.append((-1)**((N//2-1)*int(occ[i,0])))
    T=coo_matrix((values,(rows,cols)),shape=(len(basis),len(basis))).tocsr()
    parameters=dict(electric=float(electric),mass=float(mass),magnetic=0.)
    H0,*_=matrix(N,cutoff,**parameters)
    H1,*_=matrix(N,cutoff,electric_offset=-.5,**parameters)
    defect=H1@T-T@H0
    interior=[i for i,(_,l) in enumerate(basis) if abs(l)<cutoff-1]
    bulk=defect[:,interior]
    residual=float(max(abs(bulk.data),default=0))
    assert residual<1e-12
    return dict(lattice_mass_shift='m_lat=m_physical-e²*a/8',
                exact_integer_map='occ_i -> occ_(i+1); n_i -> n_(i+1)+(1+(-1)^i)/2; theta -> theta-pi. Fermion translation sign=(-1)^[(N/2-1)*occ_0].',
                exact_diagonal_energy_cases=len(energies),exact_energy_difference='0',
                projected_kinetic_intertwiner_bulk_residual=residual,
                projection_boundary='Finite winding cutoff is not invariant under the integer map; exact statement is untruncated, bulk test excludes boundary columns.',
                theta_interpretation='For unit-charge fermions the one-site map relates distinct theta theories; it is parameter covariance, not an internal symmetry at fixed theta.',
                prior_art='Dempsey,Klebanov,Pufu,Zan2022; not a newly discovered mass-shift theorem.',
                primary='https://arxiv.org/abs/2206.05308')


def improved_mass_refinement():
    length=8.;e=.7;records=[]
    for N in (4,6,8,10,12):
        a=length/N
        d=solve(N,3,electric=e*e*a,hopping=1/(2*a),mass=-e*e*a/8,magnetic=0.)
        records.append(dict(sites=N,spacing=a,mass_counterterm=-e*e*a/8,**d,
                            fractional_gap_error=d['gap']/(e/np.sqrt(np.pi))-1))
    return dict(samples=records,benchmark=e/np.sqrt(np.pi),
                scope='Known1D regulator mass matching, explicitly verified on our Hamiltonian. Standard Schwinger continuum control, not W33-derived charge or4D running.')


def matched_static_screening():
    length=8.;e=.7;rows=[]
    for N in (8,10,12):
        a=length/N
        parameters=dict(electric=e*e*a,hopping=1/(2*a),mass=-e*e*a/8,magnetic=0.)
        vacuum=solve(N,3,**parameters)['ground_energy']
        potentials=[]
        for r in range(1,N//2+1):
            values=[]
            for sign in (1,-1):
                q=np.zeros(N,dtype=int);q[0]=sign;q[r]=-sign
                values.append(solve(N,3,static=q,**parameters)['ground_energy']-vacuum)
            potentials.append(dict(distance=r*a,source_plus_minus_energy=values,source_sign_mean=float(np.mean(values))))
        distances=np.array([v['distance'] for v in potentials]);values=np.array([v['source_sign_mean'] for v in potentials])
        # Last separation is held out, not included in charge extraction.
        fit=minimize_scalar(lambda z:np.sum((screened_circle(distances[:-1],z,length)-values[:-1])**2),bounds=(.05,2.),method='bounded')
        prediction=float(screened_circle(distances[-1],fit.x,length))
        rows.append(dict(sites=N,spacing=a,potentials=potentials,
                         extracted_screening_charge=float(fit.x),
                         held_out_separation=float(distances[-1]),held_out_prediction=prediction,
                         held_out_actual=float(values[-1]),held_out_error=abs(prediction-values[-1])))
    return dict(samples=rows,known_dimensionful_charge_input=e,
                scope='Effective charge matching in a standard1D regulator, after known mass counterterm and explicit source-sign averaging. This is a finite-spacing extraction against a known continuum kernel, with one held-out separation. It does not predict the supplied charge, establish a4D beta function, or construct a native W33 refinement tower.')


def refinement():
    # Separate1+1D regulator, with standard staggered hopping and physical
    # dimensional charge e held fixed. This is not a W33 refinement tower.
    length=8.;e=.7;records=[]
    for N in (4,6,8,10):
        a=length/N;parameters=dict(electric=e*e*a,hopping=1/(2*a),mass=0.,magnetic=0.)
        cut=[dict(cutoff=L,**solve(N,L,**parameters)) for L in (2,3)]
        vacuum=cut[-1]['ground_energy']
        potentials=[]
        for r in range(1,N//2+1):
            static=np.zeros(N,dtype=int);static[0]=1;static[r]=-1
            charged=solve(N,3,static=static,**parameters)
            potentials.append(dict(distance=r*a,energy_shift=charged['ground_energy']-vacuum))
        distances=np.array([v['distance'] for v in potentials]);values=np.array([v['energy_shift'] for v in potentials])
        fit=minimize_scalar(lambda q:np.sum((screened_circle(distances,q,length)-values)**2),bounds=(.05,2.),method='bounded')
        predictions=screened_circle(distances,fit.x,length)
        records.append(dict(sites=N,spacing=a,bare_dimensionless_charge=e*a,
                            cutoff_sweep=cut,static_potentials=potentials,
                            effective_charge_from_continuum_kernel=float(fit.x),
                            fit_max_energy_residual=float(np.max(abs(predictions-values))),
                            benchmark_massless_continuum_gap=e/np.sqrt(np.pi)))
    return dict(length=length,dimensionful_charge_input=e,samples=records,
                scope='Separate finite-ring staggered Schwinger benchmark with supplied physical length/charge and standard1D continuum screening kernel. Finite-size and flux-cutoff comparisons do not determine4D W33 running, chiral SM charges or physical units; the engineering e*a trajectory is specified, not a derived beta function.',
                primary='https://arxiv.org/abs/2104.00025')


def payload():
    return dict(status='PASS',native=native_octagon(),one_dimensional_refinement=refinement(),
                exact_mass_matching=shifted_mass_symmetry(),mass_matched_refinement=improved_mass_refinement(),
                matched_static_screening=matched_static_screening())


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11969_quantum_gauge_fermion.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS native',[(r['cutoff'],r['dimension'],r['gap']) for r in d['native']['flux_cutoff_sweep']],flush=True)
    print('REFINEMENT',[(r['sites'],r['cutoff_sweep'][-1]['gap'],r['effective_charge_from_continuum_kernel']) for r in d['one_dimensional_refinement']['samples']],flush=True)
