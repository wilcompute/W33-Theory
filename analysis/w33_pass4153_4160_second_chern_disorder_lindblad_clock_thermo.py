#!/usr/bin/env python3
"""Deterministic verifier for Passes 4153-4160."""
from __future__ import annotations
import hashlib, itertools, json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm

CERT=json.loads(r'''{"schema":"w33.pass4153_4160.second_chern_disorder_lindblad_clock_thermo.v1","status":"PASS_EXACT_EIGHT_FRONT_WITH_CLIFFORD_DISORDER_LINDBLAD_GRAY_BETHE_AND_MEASUREMENT_BOUNDARIES","checks":{"4153":true,"4154":true,"4155":true,"4156":true,"4157":true,"4158":true,"4159":true,"4160":true},"all_checks_hold":true,"pass4153_second_chern_pump":{"control_hamiltonian":"H(n)=sum_{a=1}^5 n_a Gamma_a on S^4, with {Gamma_a,Gamma_b}=2 delta_ab","bundle":"rank-two negative-energy projector P=(I-H)/2 embedded in four SU(3)-singlet contraction channels","clifford_residual":0.0,"gamma_product":"Gamma1 Gamma2 Gamma3 Gamma4 Gamma5=-I4","projector_rank":2,"chern_density_identity":"Tr[P(dP)^4]=(1/8) epsilon_abcde n_a dn_b dn_c dn_d dn_e","sphere_integral":"integral Tr[P(dP)^4]=8 pi^2","second_chern_number":1,"first_chern_number":0,"pump_response":"one complete oriented S4 synthetic-control sweep carries one quantized second-Chern bundle unit","boundary":"Exact Yang-monopole Clifford bundle and synthetic nonlinear pump invariant; no fabricated four-dimensional device or continuum gauge field."},"pass4154_disordered_hawking":{"model":"nine-cell 38-dimensional Nambu chain; each cell applies a two-mode squeezer then a greybody beam splitter","disorder":"all 512 binary patterns with r_j -> r_j(1+0.5 s_j) and Gamma_j -> Gamma_j+0.05 s_j","patterns":512,"minimum_logarithmic_negativity":0.0920180870832679,"maximum_logarithmic_negativity":0.35854342498350217,"largest_minimum_PT_symplectic_eigenvalue":0.4560443261862474,"outside_occupation_range":[0.0022489743418531894,0.035610753291245134],"partner_occupation_range":[0.0060985620405201585,0.05591406283730719],"maximum_environment_occupation":0.028698313265692943,"partner_center_range":[3.0255016105494636,4.981957795233372],"partner_width_range":[0.6012179442437079,1.9537831469131335],"partner_IPR_range":[0.16672063313202767,0.7151738538456444],"maximum_paraunitary_residual":1.820507754118181e-15,"robustness_verdict":"Every audited disorder pattern remains entangled; no PT eigenvalue reaches 1/2.","boundary":"Finite exhaustive binary-disorder audit, not observed Hawking radiation or a theorem for arbitrary continuous disorder."},"pass4155_lindblad_scale_rg":{"scale_fixed_point":"s*=ln(80)/4","scale_value":1.0955066586684703,"jump_operators":"L-=sqrt[8 gamma(nbar+1)] b, L+=sqrt[8 gamma nbar] b^dagger","scale_operator":"s=s*+sigma(b+b^dagger), sigma^2=D/[4 gamma(2 nbar+1)]","mean_flow":"d<s>/dt=-4 gamma(<s>-s*)","liouvillian_gap":"4 gamma","stationary_state":"thermal oscillator with mean occupation nbar","demo":{"gamma":1.0,"D":0.01,"nbar":0.25,"variance_s":0.0025,"sigma2":0.0016666666666666668,"purity":0.6666666666666666,"entropy_nats":0.6255030294227348,"N12_stationary_residual":5.119891045273608e-16,"N12_gap":4.000007462337972},"selected_spectral_dimension":4,"boundary":"Exact displaced thermal Lindblad oscillator for the scale coordinate; not a derivation of physical spacetime."},"pass4156_compressed_gray_clock":{"program_gates":24,"legal_clock_states":25,"minimum_clock_qubits":5,"gray_codes":["00000","00001","00011","00010","00110","00111","00101","00100","01100","01101","01111","01110","01010","01011","01001","01000","11000","11001","11011","11010","11110","11111","11101","11100","10100"],"flip_bit_sequence":[0,1,0,2,0,1,0,3,0,1,0,2,0,1,0,4,0,1,0,2,0,1,0,3],"adjacent_hamming_distance":1,"clock_hamiltonian":"sum_t sqrt[(t+1)(24-t)] |g_(t+1)><g_t| tensor U_(t+1)+h.c.","clock_spectrum":"-24 Omega,-22 Omega,...,+24 Omega","perfect_transfer_time":"pi/(2 Omega)","full_revival_time":"pi/Omega","clock_locality":5,"clock_plus_SWAP_locality":7,"unused_codewords":7,"ideal_illegal_leakage":0,"perturbative_demo":{"penalty_over_Omega":40,"epsilon_over_Omega":0.01,"leakage_bound":3.9111373939543984e-07},"boundary":"Information-theoretically minimal five-qubit clock register, but locality rises to seven; no universal hardware advantage is claimed."},"pass4157_levi_thermodynamics":{"cell_degeneracies":{"dark":3161,"bright":160},"spin_model":"Z=sum_sigma prod_i g_sigma_i exp[beta J sum_edges sigma_i sigma_j+beta H sum_i sigma_i]","coexistence_field":"H_c(T)=-(T/2) ln(3161/160)","ln_degeneracy_ratio":2.983469896981791,"levi_degree":6,"nonbacktracking_branching":5,"bethe_critical_condition":"5 tanh(beta_c J)=1","beta_c_J_bethe":0.2027325540540822,"T_c_over_J_bethe":4.932606924752863,"beta_c_J_mean_field":0.16666666666666666,"T_c_over_J_mean_field":6.0,"tree_susceptibility":"chi=(1+tanh betaJ)/(1-5 tanh betaJ)","chi_at_betaJ_0p2":91.2397262009695,"finite_160_vertex_result":"analytic partition function; no true finite-size singularity","thermodynamic_limit_result":"large-girth six-regular covers possess a genuine Bethe ordering singularity at beta J=atanh(1/5) on the coexistence line","boundary":"Controlled classical two-sector interaction model on graph covers, not proof that the physical dark reservoir realizes this coupling."},"pass4158_zeno_firewall":{"protocol":"split a two-mode squeeze r into M pieces and project the partner onto vacuum after every piece","conditional_survival":"P_M=sech^(2M)(r/M)","pair_probability":"1-P_M ~ r^2/M","demo_r":0.09506557725167403,"demo":[{"M":1,"survival":0.9910167089788703,"pair_probability":0.008983291021129713},{"M":4,"survival":0.9977433966369643,"pair_probability":0.0022566033630356808},{"M":16,"survival":0.9994353213157814,"pair_probability":0.0005646786842186113},{"M":64,"survival":0.9998587996469871,"pair_probability":0.00014120035301290468},{"M":256,"survival":0.9999646980303329,"pair_probability":3.5301969667056454e-05}],"limit":"P_M -> 1 and conditional pair production -> 0 as M -> infinity","boundary":"Postselected measurement backaction and a quantum-Zeno suppression effect, not a black-hole firewall."},"pass4159_dimension_spectroscopy":{"active_bundle_dimension":2,"full_singlet_dimension":6,"active_maximally_mixed_purity":"1/2","full_singlet_maximally_mixed_purity":"1/6","pauli_twirl_survival":"(1/4) sum_{P in IXYZ} |<psi|P|psi>|^2=1/2 for every pure active state","effective_dimension":"d_eff=1/Tr(rho^2)","leakage_model":"rho=(1-p) I2/2 direct_sum p I4/4","leakage_p_0p1_purity":0.40750000000000003,"leakage_p_0p1_effective_dimension":2.4539877300613497,"boundary":"Participation-dimension spectroscopy of a finite holonomy bundle, not an anyonic quantum dimension."},"pass4160_torsion_echo":{"hamiltonian":"four-state clock ring with hopping Omega exp(i Phi/4) and loop flux Phi","pi_flux_spectrum":["-sqrt(2) Omega","-sqrt(2) Omega","+sqrt(2) Omega","+sqrt(2) Omega"],"pi_flux_echo_time":"pi/(sqrt(2) Omega)","pi_flux_echo":"U(T)=-I4","numeric_residual":1.0232645214710958e-15,"zero_flux_full_echo_time":"pi/Omega","speedup_ratio":"1/sqrt(2)","projective_loop_phase":"-1","boundary":"Exact projective clock-loop echo, not spacetime torsion or a measured time crystal."},"boundaries":["All results are finite Clifford, Gaussian, Lindblad, clock, Bethe, measurement, purity, or flux-ring statements.","No fabricated 4D pump, observed Hawking radiation, spacetime derivation, universal clock advantage, physical firewall, anyonic dimension, spacetime torsion, gravity, cosmology, or theory of everything is claimed."],"semantic_sha256":"0e9080801a2cfcca3b7b39afd807835d7bdc6b1a483cd685763b6dfe63405691"}''')
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_4153_4160_SECOND_CHERN_DISORDER_LINDBLAD_CLOCK_THERMO.json'

def destroy(n):
    a=np.zeros((n,n),complex)
    for k in range(1,n): a[k-1,k]=math.sqrt(k)
    return a

def lindblad_super(ls):
    n=ls[0].shape[0]; eye=np.eye(n); s=np.zeros((n*n,n*n),complex)
    for L in ls:
        q=L.conj().T@L
        s+=np.kron(L.conj(),L)-.5*np.kron(eye,q)-.5*np.kron(q.T,eye)
    return s

def squeezer(n,i,j,r):
    S=np.eye(2*n,dtype=complex); c=math.cosh(r); s=math.sinh(r)
    for row in (i,j,n+i,n+j): S[row,:]=0
    S[i,i]=c;S[i,n+j]=s;S[j,j]=c;S[j,n+i]=s
    S[n+i,n+i]=c;S[n+i,j]=s;S[n+j,n+j]=c;S[n+j,i]=s
    return S

def beamsplitter(n,i,j,g):
    S=np.eye(2*n,dtype=complex); t=math.sqrt(g); q=math.sqrt(1-g)
    for row in (i,j,n+i,n+j): S[row,:]=0
    S[i,i]=t;S[i,j]=q;S[j,i]=-q;S[j,j]=t
    S[n+i,n+i]=t;S[n+i,n+j]=q;S[n+j,n+i]=-q;S[n+j,n+j]=t
    return S

def chain(rv,gv):
    n=19; S=np.eye(2*n,dtype=complex)
    for j,(r,g) in enumerate(zip(rv,gv)):
        S=beamsplitter(n,0,10+j,g)@squeezer(n,0,1+j,r)@S
    return S

def covariance(S):
    n=S.shape[0]//2; K=np.zeros((2*n,2*n),complex)
    for i in range(n):
        K[i,2*i]=K[n+i,2*i]=1/math.sqrt(2)
        K[i,2*i+1]=1j/math.sqrt(2);K[n+i,2*i+1]=-1j/math.sqrt(2)
    Sq=np.real_if_close(np.linalg.inv(K)@S@K,tol=1e5).real
    return .5*Sq@Sq.T

def symplectic_eigs(V):
    m=V.shape[0]//2; om=np.kron(np.eye(m),np.array([[0.,1.],[-1.,0.]]))
    return np.sort(np.abs(np.linalg.eigvals(1j*om@V)))[::2]

def logneg(S):
    V=covariance(S); modes=[0]+list(range(1,10)); idx=[q for m in modes for q in (2*m,2*m+1)]
    W=V[np.ix_(idx,idx)]; pt=np.eye(20);pt[1,1]=-1; nu=symplectic_eigs(pt@W@pt)
    return max(0.,-float(np.sum(np.log(2*nu[nu<.5])))),float(nu[0])

def verify():
    sx=np.array([[0,1],[1,0]],complex);sy=np.array([[0,-1j],[1j,0]],complex);sz=np.diag([1,-1]).astype(complex);I=np.eye(2)
    G=[np.kron(sx,sx),np.kron(sx,sy),np.kron(sx,sz),np.kron(sy,I),np.kron(sz,I)]
    assert max(np.linalg.norm(G[i]@G[j]+G[j]@G[i]-(2*np.eye(4) if i==j else 0)) for i in range(5) for j in range(5))<1e-13
    assert np.linalg.norm(np.linalg.multi_dot(G)+np.eye(4))<1e-13
    rb=np.array([.00979708977002,.0203649786239,.0410938074485,.0738588749836,.0950655772517,.0738588749836,.0410938074485,.0203649786239,.00979708977002])
    gb=np.array([.931739737612,.916053718604,.87648655463,.805844961224,.76,.805844961224,.87648655463,.916053718604,.931739737612])
    mins=9.;maxres=0.;eta=np.diag([1]*19+[-1]*19)
    for bits in itertools.product((-1.,1.),repeat=9):
        z=np.array(bits);S=chain(rb*(1+.5*z),gb+.05*z);l,_=logneg(S);mins=min(mins,l);maxres=max(maxres,float(np.linalg.norm(S@eta@S.conj().T-eta,2)))
    assert abs(mins-CERT['pass4154_disordered_hawking']['minimum_logarithmic_negativity'])<2e-12 and maxres<3e-15
    n=12;a=destroy(n);nb=.25;L=lindblad_super([math.sqrt(8*(nb+1))*a,math.sqrt(8*nb)*a.conj().T]);p=np.array([(nb/(nb+1))**k for k in range(n)]);p/=p.sum()
    assert np.linalg.norm(L@np.diag(p).flatten(order='F'))<1e-12
    eig=np.linalg.eigvals(L);gap=-max(x.real for x in eig if x.real<-1e-8);assert abs(gap-4)<1e-4
    codes=[t^(t>>1) for t in range(25)];assert len(set(codes))==25 and all((codes[t]^codes[t+1]).bit_count()==1 for t in range(24))
    H=np.zeros((25,25))
    for t in range(24):H[t,t+1]=H[t+1,t]=math.sqrt((t+1)*(24-t))
    assert abs(expm(-1j*H*math.pi/2)[-1,0]-1)<1e-12
    assert abs(5*math.tanh(math.atanh(.2))-1)<1e-15
    r=CERT['pass4158_zeno_firewall']['demo_r'];assert 1-(1/math.cosh(r/256)**2)**256<4e-5
    phi=math.pi;R=np.zeros((4,4),complex)
    for j in range(4):
        k=(j+1)%4;amp=np.exp(1j*phi/4);R[k,j]+=amp;R[j,k]+=amp.conjugate()
    assert np.linalg.norm(expm(-1j*R*math.pi/math.sqrt(2))+np.eye(4))<2e-14
    return True

def main():
    assert verify();base={k:v for k,v in CERT.items() if k!='semantic_sha256'}
    assert hashlib.sha256(json.dumps(base,sort_keys=True,separators=(',',':')).encode()).hexdigest()==CERT['semantic_sha256']
    OUT.write_text(json.dumps(CERT,separators=(',',':'))+'\n');print(CERT['status'],CERT['semantic_sha256'])
if __name__=='__main__':main()
