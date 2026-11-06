"""Tests for the declared native-quiver EFT and attempted anomaly completion."""
import importlib.util,pathlib,math,json
from fractions import Fraction as Q
import numpy as np
import networkx as nx
import pytest
R=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('boundary_axion',R/'analysis/toe_20261105_native_boundary_axion.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
@pytest.fixture(scope='module')
def geo():return m.geometry()
@pytest.fixture(scope='module')
def boundary(geo):return m.boundary_data(*geo)

def test_reused_geometry_matches_actual_prior_certificates(geo):
    G,edges,B,C,K=geo
    prior=json.loads((R/'data/PART_BT547_W33_LEVI_KIRCHHOFF_CYCLE_PROJECTOR_results.json').read_text())
    assert prior['all_identities_hold']and len(G)==prior['objects']['levi_vertices']
    assert C.shape==(160,1620)and np.all(B@C==0)
    assert np.array_equal(K@K,160*K)and np.trace(K)//160==81

def test_relative_phase_count_and_one_boundary_mode(geo,boundary):
    G,edges,B,C,K=geo;u,v=boundary['boundary_vertices']
    I=[i for i in G if i not in [u,v]]
    assert np.linalg.matrix_rank(B[I])==78
    assert 160-78==82
    h=np.array([float(Q(x))for x in boundary['unit_current_edge_flow']])
    assert np.max(abs(C.T@h))<1e-13
    assert np.max(abs(B[I]@h))<1e-13
    assert np.linalg.matrix_rank(np.column_stack([K,h]))==82

def test_exact_current_resistance_and_four_path_phases(geo,boundary):
    G,edges,B,C,K=geo;h=[Q(x)for x in boundary['unit_current_edge_flow']]
    res=Q(boundary['resistance']);assert res==Q(7,10)and sum(t*t for t in h)==res
    assert len(boundary['shortest_paths'])==4
    for path in boundary['shortest_paths']:
        value=Q(0)
        for u,v in zip(path,path[1:]):value+=(1 if u<v else -1)*h[edges.index(tuple(sorted((u,v))))]/res
        assert value==1

@pytest.mark.parametrize('s',[2,3,4])
def test_actual_subdivision_and_lifted_current(geo,boundary,s):
    G,edges,B,C,K=geo;H=nx.Graph();H.add_nodes_from(G);lift=[]
    for u,v in edges:
        chain=[u]+list(range(len(H),len(H)+s-1))+[v]
        H.add_edges_from(zip(chain,chain[1:]));lift.extend(zip(chain,chain[1:]))
    assert len(H)==80+160*(s-1)and H.number_of_edges()==160*s
    u,v=boundary['boundary_vertices'];assert nx.shortest_path_length(H,u,v)==4*s
    assert sum(1 for _ in nx.all_shortest_paths(H,u,v))==4
    current=np.repeat([float(Q(x))for x in boundary['unit_current_edge_flow']],s)
    div=np.zeros(len(H))
    for (a,b),z in zip(lift,current):div[a]-=z;div[b]+=z
    assert np.allclose(div[[i for i in H if i not in [u,v]]],0)
    assert np.isclose(current@current,.7*s)
    # Lifting every cycle repeats each old edge s times.
    Cs=np.repeat(C,s,axis=0);weights=np.random.default_rng(s).integers(-3,4,C.shape[1])
    a=C@weights;b=Cs@weights
    assert np.array_equal(b,np.repeat(a,s))and b@b==s*(a@a)

def test_positive_cycle_locking_is_gauge_invariant_and_stationary(geo):
    G,edges,B,C,K=geo;c=C[:,0];rng=np.random.default_rng(15)
    phi=(.7+rng.random(160))*np.exp(1j*rng.normal(size=160))
    def potential(z):return abs(np.prod(z[c>0])-np.prod(z[c<0]))**2
    alpha=rng.normal(size=80);gauge=np.exp(1j*(B.T@alpha))
    assert np.isclose(potential(phi),potential(phi*gauge))
    assert potential(np.ones(160))==0
    eps=1e-5
    hess=(potential(np.exp(1j*eps*c))+potential(np.exp(-1j*eps*c)))/eps**2
    assert np.isclose(hess,128,rtol=1e-7)

def test_normalization_and_coherent_path_threshold(boundary):
    rows=m.quality_rows()['rows'];assert rows[2]['one_path_amplitude_over_chi']<1e-10
    assert rows[2]['coherent_four_path_amplitude_over_chi']>1e-10
    assert m.quality_rows()['first_coherent_shortest_path_pass']==4
    for row in rows:
        s=row['subdivision'];assert np.isclose(row['link_F_input_GeV']/math.sqrt(.7*s),1e11)
    assert rows[3]['edges']==640 and rows[3]['interior_gauge_factors']==558
    # Planck-only cycle locking is far below QCD on the quality-passing branch.
    assert rows[3]['Planck_cycle_mass_over_QCD_mass']<1e-70
    assert .13<rows[3]['EFT_cycle_gap_over_F_if_matching_scale_F']<.15

def test_chain_gauge_anomalies_and_accidental_QCD_charge():
    L=16;q=np.zeros((L,L-1),int);qb=q.copy()
    for i in range(L):
        if i<L-1:q[i,i]=-1
        if i>0:qb[i,i-1]=1
    assert np.all(np.sum(q+qb,axis=0)==0) # SU3²X,Y²X,gravity-X
    assert np.all(np.sum(q**3+qb**3,axis=0)==0)
    assert np.all(np.sum(q**2-qb**2,axis=0)==0) # YX²
    assert np.all(q[-1]+qb[0]==0) # Gauge allows closing mass.
    for i in range(L-1):assert np.all(q[i]+qb[i+1]==0)
    pq=[Q(-i,L)for i in range(1,L+1)];pqb=[Q(i-1,L)for i in range(1,L+1)]
    assert sum(pq)+sum(pqb)==-1 and pq[-1]+pqb[0]==-1
    for i in range(L):assert Q(1,L)+pq[i]+pqb[i]==0

@pytest.mark.parametrize('L',[4,12,16])
def test_chain_determinant_gauge_phase_and_no_closing_mass_control(L):
    psi=.41;r=1/math.sqrt(2)
    for mu in [0.,.37*np.exp(.2j),1.]:
        M=m.mass_matrix(L,psi,mu)
        assert np.allclose(np.linalg.det(M),r**L*np.exp(1j*psi)+(-1)**(L-1)*mu)
    a=m.mass_matrix(L,.2,0);b=m.mass_matrix(L,1.3,0)
    assert np.allclose(np.linalg.svd(a,compute_uv=False),np.linalg.svd(b,compute_uv=False))

def test_CW_winding_coefficient_by_independent_fourier_quadrature():
    # Integrate the one-particle scalar function directly, without a matrix.
    x=2*np.pi*np.arange(16384)/16384;r=1/math.sqrt(2)
    H=1+r*r+2*r*np.cos(x);f=H**2*np.log(H)
    for L in [4,12,16]:
        cn=np.mean(f*np.cos(L*x))
        assert np.isclose(cn,m.winding_coefficient(L,r),rtol=1e-7,atol=1e-15)
    # L>=3 removes the subtraction polynomial's Fourier contribution.
    assert abs(np.mean(H**2*np.cos(16*x)))<1e-14

def test_actual_server_PC_quality_agreement_including_smallest_amplitude():
    server=json.loads((R/'data/toe_20261105_native_boundary_axion_server.json').read_text())
    assert server['execution']=='functions.exec server V8'and server['cycleRank']==81
    for pc,js in zip(m.quality_rows()['rows'],server['quality']):
        assert js['coherentAmplitudeOverChi']>0
        assert np.isclose(pc['coherent_four_path_amplitude_over_chi']/js['coherentAmplitudeOverChi'],1,rtol=1e-12)

def test_closing_mass_has_an_independent_physical_CP_phase():
    L=16;psi=.31;delta=.79
    a=m.mass_matrix(L,psi,np.exp(1j*delta));b=m.mass_matrix(L,psi-delta,1)
    assert np.allclose(np.linalg.svd(a,compute_uv=False),np.linalg.svd(b,compute_uv=False))
    # Setting every Wilson coefficient real would have hidden this allowed phase.
    c=m.mass_matrix(L,psi,1)
    assert not np.allclose(np.linalg.svd(a,compute_uv=False),np.linalg.svd(c,compute_uv=False),atol=1e-6)

def test_added_Abelian_anomaly_cancellation_forces_closing_mass_neutral():
    rng=np.random.default_rng(123)
    for L in [4,12,16,24]:
        q=rng.integers(-100,101,L);qb=np.r_[-q[-1],-q[:-1]]
        assert sum(q+qb)==0 and q[-1]+qb[0]==0
        for i in range(L-1):assert q[i]+qb[i+1]==0
        qb[0]+=7
        assert sum(q+qb)==q[-1]+qb[0]==7

def test_scalar_factorizer_witness_and_parent_cycle_membership(geo,boundary):
    out=m.scalar_factorization(geo,boundary);G,edges,B,C,K=geo
    a,b=out['witness'];u,v=boundary['boundary_vertices'];I=[i for i in G if i not in [u,v]]
    assert a['native_edges']==[[0,41],[13,53]]and b['native_edges']==[[4,53],[13,41]]
    assert np.array_equal(np.array(a['full_vertex_charge'])[I],np.array(b['full_vertex_charge'])[I])
    assert abs(Q(out['mixing_PQ_charge']))==1
    for row in [a,b]:
        z=np.zeros(160,int)
        for e,sign in row['parent_cycle']:z[e]=sign
        assert np.all(B@z==0)and set(z[row['native_edge_indices']])=={1}

def test_scalar_factorizer_positive_mixing_and_tree_matching(geo,boundary):
    out=m.scalar_factorization(geo,boundary);row=out['benchmark'];s=row['s'];F=row['matching_M_input_GeV']
    # One8-link prefix at s4, with all link magnitudes F/sqrt2.
    A=(F/math.sqrt(2))**(2*s)/F**(2*s-1)
    assert np.isclose(A/F,1/16)
    epsilon=row['epsilon_input'];delta=.4
    def potential(psi):return epsilon*F**2*abs(A*np.exp(1j*psi)-A*np.exp(1j*delta))**2
    assert potential(delta)==0 and potential(delta+np.pi)>0
    assert np.isclose((potential(delta+np.pi)-potential(delta))/2,row['mixing_potential_amplitude_GeV4'])
    assert row['mixing_amplitude_over_chi']>1e40
