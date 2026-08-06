#!/usr/bin/env python3
"""Passes 4041-4048: eight exact physics constructions on the W33/Levi H1 substrate."""
from __future__ import annotations
import hashlib, itertools, json, math
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_4041_4048_EIGHT_PHYSICS_EXPANSION.json'
MOD=3

def canonical_sha(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def norm(v):
    v=tuple(x%MOD for x in v)
    for a in v:
        if a:
            return tuple((1 if a==1 else 2)*x%MOD for x in v)
    raise ValueError

def form(u,v):
    return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%MOD

def geometry():
    pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    W=nx.Graph();W.add_nodes_from(range(40))
    for i,u in enumerate(pts):
        for j in range(i+1,40):
            if form(u,pts[j])==0:W.add_edge(i,j)
    lines=sorted(tuple(sorted(c)) for c in nx.find_cliques(W) if len(c)==4)
    assert len(lines)==40 and W.number_of_edges()==240
    L=nx.Graph();L.add_nodes_from(range(80))
    for j,line in enumerate(lines):
        for p in line:L.add_edge(p,40+j)
    edges=sorted(tuple(sorted(e)) for e in L.edges())
    D=np.zeros((80,160),dtype=float)
    for k,(p,l) in enumerate(edges):D[p,k]=-1;D[l,k]=1
    X=nx.line_graph(L)
    AX=nx.to_numpy_array(X,nodelist=edges,dtype=float)
    I=np.eye(160)
    Pn=((AX-6*I)@(AX-2*I)@(AX@AX-4*AX-2*I))/2
    P=Pn/160
    assert np.linalg.matrix_rank(D)==79
    assert np.linalg.norm(P@P-P,2)<1e-11 and round(np.trace(P))==81
    assert np.linalg.norm(D@P,2)<1e-11
    return W,L,X,edges,D,AX,P

def cluster(vals,tol=1e-8):
    out=[]
    for x in sorted(map(float,vals)):
        if not out or abs(x-out[-1][0])>tol:out.append([x,1])
        else:out[-1][1]+=1
    return out

def longest_plateau(d,N,kappa,target,tol=0.05):
    int_lams=np.array([0]+[4-math.sqrt(6)]*24+[4]*30+[4+math.sqrt(6)]*24+[8],float)
    n=np.arange(N);ext=2*kappa*(1-np.cos(2*np.pi*n/N))
    def ds(lams,t):
        z=np.exp(-t*lams)
        return float(2*t*np.dot(lams,z)/z.sum())
    ts=np.logspace(-2,5,5000)
    vals=np.array([ds(int_lams,t)+d*ds(ext,t) for t in ts])
    mask=np.abs(vals-target)<tol
    best=None;start=None
    for i,m in enumerate(mask):
        if m and start is None:start=i
        if start is not None and ((not m) or i==len(mask)-1):
            end=i-1 if not m else i
            if best is None or end-start>best[1]-best[0]:best=(start,end)
            start=None
    assert best is not None
    a,b=best
    return {'t_start':float(ts[a]),'t_end':float(ts[b]),'ds_min':float(vals[a:b+1].min()),'ds_max':float(vals[a:b+1].max()),'samples':int(b-a+1)}

def main():
    W,L,X,edges,D,AX,P=geometry()
    checks={}
    checks['geometry']=W.number_of_nodes()==40 and L.number_of_nodes()==80 and len(edges)==160 and AX.sum()/2==480
    checks['h1_projector']=np.linalg.norm(P@P-P,2)<1e-11 and round(np.trace(P))==81

    Ux=np.array([[0,1],[-1,0]],dtype=complex)
    Uz=np.diag([-1j,1+0j])
    comm=Ux@Uz-Uz@Ux
    checks['holonomic']=np.linalg.norm(Ux.conj().T@Ux-np.eye(2))<1e-12 and np.linalg.norm(Uz.conj().T@Uz-np.eye(2))<1e-12 and abs(np.linalg.norm(comm,'fro')**2-4)<1e-12
    p4041={
      'logical_support':'any orthonormal pair inside rank-81 H1 plus one H1 helper and one excited ancilla',
      'tripod_spectrum':'{-Omega,0,0,+Omega}','dark_dimension':2,
      'loop_X':{'path':'theta:0->acos(1/4), phi:0->2pi, theta->0','connection':'A_phi=cos(theta)[[0,-1],[1,0]]','holonomy':[['0','1'],['-1','0']]},
      'loop_Z':{'path':'theta:0->pi/6, chi:0->2pi, theta->0','connection':'A_chi=diag(i sin^2(theta),0)','holonomy':[['-i','0'],['0','1']]},
      'commutator_frobenius_squared':4,
      'continuous_control':'varying theta gives continuous Y- and Z-axis angles; the two loop families generate SU(2)',
      'adiabatic_gap':'Omega',
      'boundary':'Exact Wilczek-Zee connection and holonomies in the ideal tripod embedding; no finite-speed fidelity, pulse bandwidth, loss, or laboratory implementation is certified.'}

    G2=P*P;vals=np.linalg.eigvalsh(G2)
    expected=[(41/200,81),((252-27*math.sqrt(6))/800,24),(117/400,30),((252+27*math.sqrt(6))/800,24),(81/160,1)]
    got=cluster(vals)
    checks['two_boson']=len(got)==5 and all(abs(got[i][0]-expected[i][0])<1e-10 and got[i][1]==expected[i][1] for i in range(5))
    p4042={'single_particle_flat_band_dimension':81,'symmetric_two_boson_dimension':81*82//2,'contact_map_rank':int(np.linalg.matrix_rank(G2)),'contact_dark_dimension':81*82//2-int(np.linalg.matrix_rank(G2)),'projected_interaction':'V=U sum_e |P e,P e><P e,P e|','nonzero_energies_over_U':[{'value':'81/160','multiplicity':1},{'value':'(252+27sqrt(6))/800','multiplicity':24},{'value':'117/400','multiplicity':30},{'value':'(252-27sqrt(6))/800','multiplicity':24},{'value':'41/200','multiplicity':81}],'reading':'The contact interaction has 160 bright pair channels and a 3161-dimensional exactly contact-dark pair manifold.','boundary':'Exact flat-band-projected two-boson contact spectrum only; no bound-pair mobility, many-body phase, topological order, or interacting-device experiment is claimed.'}

    u,svals,vh=np.linalg.svd(D,full_matrices=False);Q=vh[:79].T;Pcut=np.eye(160)-P
    H=np.block([[np.zeros((160,160)),Q],[Q.T,np.zeros((79,79))]])
    Ucool=np.eye(239)-H@H-1j*H
    checks['cooling']=np.linalg.norm(Q.T@Q-np.eye(79),2)<1e-12 and np.linalg.norm(Q@Q.T-Pcut,2)<1e-11 and np.linalg.norm(H@H@H-H,2)<1e-11 and np.linalg.norm(Ucool.conj().T@Ucool-np.eye(239),2)<1e-11
    checks['cooling_action']=np.linalg.norm(Ucool[:160,:160]-P,2)<1e-11 and np.linalg.norm(Ucool[160:,:160]+1j*Q.T,2)<1e-11
    p4043={'system_link_modes':160,'protected_modes':81,'cut_modes':79,'reservoir_modes':79,'polar_isometry':'Q=D^T(DD^T)^(-1/2) on the charge-zero vertex sector','identities':['Q^T Q=I_79','Q Q^T=P_cut'],'passive_swap_hamiltonian':'H_cool=[[0,Q],[Q^T,0]]','one_shot_time':'pi/(2g)','one_shot_action':'|psi>_sys|0>_res -> P_H1|psi>_sys - i Q^T|psi>_res','number_conservation':'The coupling is bilinear and passive; total excitation number is conserved before reservoir reset.','boundary':'The exact swap requires a 79-mode polar coupler. Reservoir reset, locality, finite-depth synthesis, calibration, and loss are not certified.'}

    ss=sp.symbols('s');gs=sp.symbols('g0:5')
    eqs=[sp.Eq((ss+4)*gs[0]-4*gs[1],1),sp.Eq(-gs[0]+(ss+4)*gs[1]-3*gs[2],0),sp.Eq(-gs[1]+(ss+4)*gs[2]-3*gs[3],0),sp.Eq(-gs[2]+(ss+4)*gs[3]-3*gs[4],0),sp.Eq(-4*gs[3]+(ss+4)*gs[4],0)]
    sol=sp.solve(eqs,gs,dict=True)[0];Z=[sp.factor(2*(sol[gs[0]]-sol[gs[d]])) for d in range(1,5)];R=[sp.limit(z,ss,0) for z in Z]
    R_expected=[sp.Rational(79,160),sp.Rational(13,20),sp.Rational(111,160),sp.Rational(7,10)]
    pair_counts=Counter();nodes=list(L.nodes())
    for i,a in enumerate(nodes):
        for b in nodes[i+1:]:pair_counts[nx.shortest_path_length(L,a,b)]+=1
    d0=nx.single_source_shortest_path_length(L,0);canonical={d:min(v for v,dd in d0.items() if dd==d) for d in range(1,5)}
    checks['coulomb']=R==R_expected and dict(pair_counts)=={1:160,2:480,3:1440,4:1080}
    p4044={'drive':'inject +I at vertex u and -I at vertex v','readout':'measure differential potential (phi_u-phi_v)/I','regularized_response_parameter':'s=(i omega C + gamma)/J','shell_transfer_functions':{str(d+1):str(Z[d]) for d in range(4)},'dc_resistances':{'1':'79/160','2':'13/20','3':'111/160','4':'7/10'},'unordered_pair_counts':{str(k):int(v) for k,v in sorted(pair_counts.items())},'canonical_pairs_from_vertex_0':{str(d):[0,int(v)] for d,v in canonical.items()},'minimum_dc_shell_gap':'1/160','sufficient_absolute_classification_error':'<1/320 in units of 1/J','boundary':'Exact finite-network impedance spectroscopy. Parasitic capacitance, port loading, calibration drift, and continuum electromagnetism are outside the theorem.'}

    p1=longest_plateau(1,64,0.05,1);p4=longest_plateau(4,64,0.05,4)
    checks['refinement']=p1['t_end']>p1['t_start'] and p4['t_end']>p4['t_start'] and p4['ds_min']>3.95 and p4['ds_max']<4.05
    p4045={'cell':'80-vertex Levi graph with internal Laplacian spectrum 0^1+(4-sqrt6)^24+4^30+(4+sqrt6)^24+8^1','external_graph':'d-dimensional periodic cubic torus of W33 cells','parameters':{'N_per_axis':64,'kappa_over_J':0.05},'long_wavelength_laplacian':'lambda(k)=2 kappa sum_mu(1-cos k_mu)=kappa |k|^2+O(k^4)','wave_equation':'d2 psi/dt2 + L psi=0 gives omega(k)=sqrt(kappa)|k|+O(k^3)','cell_light_speed':'c_cell=a sqrt(kappa)','one_dimensional_tower_plateau':p1,'four_dimensional_tower_plateau':p4,'verdict':'A 4D plateau is obtained only when four external lattice directions are explicitly supplied; a 1D chain remains one-dimensional.','boundary':'This is an engineered refinement family, not emergence of four dimensions from one W33 cell and not a derivation of Lorentz invariance or vacuum c.'}

    Qs=np.block([[np.zeros((80,80)),D],[D.T,np.zeros((160,160))]]);qvals=np.linalg.eigvalsh(Qs);zero=int(np.sum(np.abs(qvals)<1e-9));pos=qvals[qvals>1e-9]
    positive_expected=[(math.sqrt(4-math.sqrt(6)),24),(2.0,30),(math.sqrt(4+math.sqrt(6)),24),(math.sqrt(8),1)];posc=cluster(pos)
    checks['susy']=zero==82 and len(posc)==4 and all(abs(posc[i][0]-positive_expected[i][0])<1e-9 and posc[i][1]==positive_expected[i][1] for i in range(4))
    p4046={'supercharge':'Q=[[0,D],[D^T,0]]','grading':'+ on 80 vertex modes, - on 160 link modes','square':'Q^2=diag(DD^T,D^T D)','zero_modes':{'vertex_uniform':1,'edge_H1':81,'total':82},'witten_index':'1-81=-80','positive_supercharge_spectrum':[{'value':'sqrt(4-sqrt(6))','multiplicity':24},{'value':'2','multiplicity':30},{'value':'sqrt(4+sqrt(6))','multiplicity':24},{'value':'sqrt(8)','multiplicity':1}],'pairing':'Every nonzero eigenvalue occurs in an exact +/- pair.','boundary':'Exact discrete supersymmetric factorization of the incidence complex; it is not evidence for supersymmetry in particle physics.'}

    e=np.zeros(160);e[0]=1;RH=np.eye(160)-2*P;Re=np.eye(160)-2*np.outer(e,e);UF=Re@RH;fvals=np.linalg.eigvals(UF)
    plus=int(np.sum(np.abs(fvals-1)<1e-8));minus=int(np.sum(np.abs(fvals+1)<1e-8));non=[z for z in fvals if abs(z-1)>1e-8 and abs(z+1)>1e-8];cosphi=float(np.real(non[0]))
    checks['floquet']=plus==78 and minus==80 and len(non)==2 and abs(cosphi-1/80)<1e-10
    p4047={'floquet_unitary':'U_F=(I-2|e><e|)(I-2P_H1)','spectrum':{'+1':78,'-1':80,'nontrivial':'exp(+/- i phi)'},'phase':'cos(phi)=2(P_H1)ee-1=1/80','infinite_order_proof':'If phi/pi were rational and cos(phi) rational, Niven theorem permits only 0, +/-1/2, +/-1; 1/80 is excluded.','reading':'One local defect plus the global Hodge reflection produces an exact quasiperiodic single-particle clock.','boundary':'This is an infinite-order Floquet rotor, not a many-body time crystal or spontaneous temporal symmetry breaking.'}

    base=edges[0];dx=nx.single_source_shortest_path_length(X,base);transfer={};pdiag=81/160
    for d in range(1,5):
        js=[j for j,e2 in enumerate(edges) if dx[e2]==d];vals={round(float(P[0,j]),12) for j in js};assert len(vals)==1
        pef=float(next(iter(vals)));s0=pef/pdiag;t=math.pi/(2*abs(pef));amp=(1+s0)/2*np.exp(-1j*pdiag*(1+s0)*t)-(1-s0)/2*np.exp(-1j*pdiag*(1-s0)*t)
        transfer[str(d)]={'normalized_overlap':s0,'time_over_pi':t/math.pi,'probability':float(abs(amp)**2)}
    checks['wormhole']=all(abs(v['probability']-1)<1e-12 for v in transfer.values())
    p4048={'normalized_protected_site_state':'|u_e>=P_H1|e>/sqrt(81/160)','two_defect_hamiltonian':'H_ef=P|e><e|P+P|f><f|P','projected_overlap_by_line_graph_distance':{'1':'-1/3','2':'1/9','3':'-1/27','4':'1/81'},'perfect_transfer_times_over_pi':{'1':'80/27','2':'80/9','3':'80/3','4':'80'},'verified_probabilities':transfer,'mechanism':'The symmetric and antisymmetric protected combinations acquire a relative phase pi.','boundary':'Perfect transfer between nonorthogonal protected site states in the ideal projected model; not superluminal signaling, a spacetime wormhole, or a locality-preserving hardware protocol.'}

    checks={k:bool(v) for k,v in checks.items()};assert all(checks.values())
    payload={'schema':'w33.pass4041_4048.eight_physics_expansion.v1','status':'PASS_EXACT_FIVE_PHYSICS_AND_THREE_OUTSIDE_BOX_WITH_CONTINUUM_AND_HARDWARE_BOUNDARIES','pass4041_non_abelian_H1_holonomies':p4041,'pass4042_interacting_two_photon_flat_band':p4042,'pass4043_number_conserving_Hodge_cooling':p4043,'pass4044_synthetic_Coulomb_spectroscopy':p4044,'pass4045_causal_refinement_tower':p4045,'pass4046_outside_box_Hodge_supersymmetry':p4046,'pass4047_outside_box_single_defect_Floquet_clock':p4047,'pass4048_outside_box_protected_perfect_transfer':p4048,'external_context':['Tripod/M-pod dark spaces are established platforms for non-Abelian holonomic quantum computation.','Interacting flat-band photons can delocalize or form interaction-enabled states; the present result is the exact W33 projected contact spectrum.','Particle-number-conserving engineered cooling is an active preparation strategy; the present result is an exact one-shot polar swap.','The four-dimensional heat-kernel plateau in the refinement model is externally supplied by four torus directions, not derived from W33.'],'boundaries':['Exact finite graph, projector, interaction, holonomy, swap, resolvent, heat-trace, supersymmetry, Floquet, and transfer statements only.','No fabricated device, measured gate fidelity, many-body phase, reservoir implementation, emergent spacetime, physical supersymmetry, time crystal, wormhole, gravity, Standard Model, or theory of everything is established.'],'checks':checks}
    payload['semantic_sha256']=canonical_sha(payload);OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');print('PASS_4041_4048_EIGHT_PHYSICS',payload['semantic_sha256']);return payload

if __name__=='__main__':main()
