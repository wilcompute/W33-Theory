#!/usr/bin/env python3
"""Five interconnected conditional TOE gates, 2026-11-19.

Five themes: causal torus -> flux index, dynamical fermion gauge center,
SSR two-copy Bell activation, symmetry-reduced causal history entropy,
and flavor graph constraints on anomaly-free charge shifts.
Not a derivation of quantum gravity, Born rule or the Standard Model.
"""
from __future__ import annotations
import itertools, json, math, sys
from collections import defaultdict, deque
from pathlib import Path
from scipy.integrate import quad
from scipy.special import iv
from scipy.optimize import linear_sum_assignment
import numpy as np
import sympy as sp

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'data/toe_20261119_five_linked_center_torus_bell_histories_flavor.json'

def gf2rank(columns):
    pivots={}
    for c in columns:
        while c:
            p=c.bit_length()-1
            if p not in pivots: pivots[p]=c;break
            c ^= pivots[p]
    return len(pivots)

def torus_causal(L,radius=1):
    N=L**2
    def label(x,y):return (x%L)*L+(y%L)
    A=np.zeros((N,N),dtype=np.uint8)
    for x in range(L):
        for y in range(L):
            w=label(x,y)
            for dx in range(-radius,radius+1):
                for dy in range(-radius,radius+1):
                    A[label(x+dx,y+dy),w]=1
    return A

def nerve_betti_2(A):
    n=A.shape[0]
    shadows=[tuple(np.flatnonzero(A[a])) for a in range(n)]
    faces=[sorted({face for sh in shadows for face in itertools.combinations(sh,k)}) for k in (1,2,3,4)]
    ranks=[]
    for k in (1,2,3):
        fidx={f:i for i,f in enumerate(faces[k-1])}
        columns=[sum(1<<fidx[sm] for sm in itertools.combinations(f,k)) for f in faces[k]]
        ranks.append(gf2rank(columns))
    betti=[len(faces[k])-(ranks[k-1] if k else 0)-(ranks[k] if k<3 else 0) for k in (0,1,2)]
    return {'betti':betti,'simplex_counts_0_to_3':[len(f) for f in faces], 'boundary_ranks_1_to_3':ranks}

def graph_from_overlap(A,L):
    n=L*L;C=A.astype(int).T@A.astype(int)
    x=C.copy();np.fill_diagonal(x,0)
    high=int(x.max())
    edges=[(a,b) for a in range(n) for b in range(a+1,n) if x[a,b]==high]
    adj=[set() for _ in range(n)]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    assert len(edges)==2*n and all(len(x)==4 for x in adj)
    # Only graph data, not original coordinates, is used to reconstruct a chart.
    def opp(v,a,b):
        return len(adj[a]&adj[b])==1
    def straight_cycle(origin,one):
        seq=[origin,one]
        while True:
            prev,cur=seq[-2:]
            candidates=[next_ for next_ in adj[cur] if next_!=prev and opp(cur,prev,next_)]
            assert len(candidates)==1,(cur,prev,candidates)
            nxt=candidates[0]
            if nxt==origin:break
            assert nxt not in seq
            seq.append(nxt)
        assert len(seq)==L
        return seq
    origin=0
    a=min(adj[origin]); b=min(v for v in adj[origin] if v!=a and not opp(origin,a,v))
    yaxis=straight_cycle(origin,b)
    chart={}
    xstart=a
    for y,base in enumerate(yaxis):
        xs=straight_cycle(base,xstart)
        for x,v in enumerate(xs):
            assert v not in chart.values()
            chart[(x,y)]=v
        nextbase=yaxis[(y+1)%L]
        corners=(adj[xstart]&adj[nextbase])-{base}
        assert len(corners)==1
        xstart=next(iter(corners))
    assert len(set(chart.values()))==n
    for y in range(L):
        for x in range(L):
            v=chart[x,y]
            assert {chart[(x+1)%L,y],chart[(x-1)%L,y],chart[x,(y+1)%L],chart[x,(y-1)%L]}==adj[v]
    return {'high_overlap':high,'edges':edges,'adj':adj,'chart':chart,'degrees':[len(a) for a in adj]}

def overlap_flux_index_on_graph(G,L,Q,m):
    # Standard, previously used Wilson/overlap regulator from repo's
    # toe_20261105_overlap_flux_chirality_index.py, now linked to a
    # chart CONSTRUCTED from the causal graph.
    N=L*L;ux=np.empty((L,L),complex);uy=np.ones((L,L),complex)
    for x in range(L):
        for y in range(L):
            ux[x,y]=np.exp(-2j*np.pi*Q*y/L**2)
            if y==L-1:uy[x,y]=np.exp(2j*np.pi*Q*x/L)
    Tx=np.zeros((N,N),complex);Ty=np.zeros((N,N),complex)
    for x in range(L):
        for y in range(L):
            site=G['chart'][x,y]
            Tx[site,G['chart'][(x+1)%L,y]]=ux[x,y]
            Ty[site,G['chart'][x,(y+1)%L]]=uy[x,y]
    sx=np.array([[0,1],[1,0]],complex)
    sy=np.array([[0,-1j],[1j,0]],complex)
    sz=np.diag([1.,-1.]);I2=np.eye(2)
    DW=(2-m)*np.eye(2*N,dtype=complex)
    for gamma,T in zip((sx,sy),(Tx,Ty)):
        DW-=.5*(np.kron(T,I2-gamma)+np.kron(T.conj().T,I2+gamma))
    ch=np.kron(np.eye(N),sz)
    H=ch@DW
    assert np.max(abs(H-H.conj().T))<1e-12
    eig,vec=np.linalg.eigh(H)
    gap=float(min(abs(eig)))
    assert gap>.1
    index=-round(np.sign(eig).sum()/2)
    # check reconstructed graph edges; the flux/axes are separately inserted
    for T in (Tx,Ty):
        nz=np.transpose(np.nonzero(abs(T)>1e-12))
        assert all((min(a,b),max(a,b)) in G['edges'] for a,b in nz)
    sgn=(vec*np.sign(eig))@vec.conj().T
    overlap=np.eye(2*N)+ch@sgn
    gw=ch@overlap+overlap@ch-overlap@ch@overlap
    gw_err=float(np.max(abs(gw)))
    assert gw_err<1e-12
    return {'flux_Q':Q,'m':m,'index':int(index),'gap':gap,'Ginsparg_Wilson_error':gw_err}

def gate_torus():
    checks=[]
    for L in (5,6,7,8):
        A=torus_causal(L)
        nerve=nerve_betti_2(A); assert nerve['betti']==[1,2,1]
        G=graph_from_overlap(A,L)
        checks.append({'L':L,'nerve':nerve,'max_overlap':G['high_overlap'], 'edges':len(G['edges']), 'degrees_unique':sorted(set(G['degrees']))})
    L=6;G=graph_from_overlap(torus_causal(L),L)
    index=[overlap_flux_index_on_graph(G,L,q,m) for q in (-1,0,1) for m in (1.,2.5)]
    assert all(x['index']==(-x['flux_Q'] if x['m']<2 else x['flux_Q']) for x in index)
    # Relabel antichain and witness events independently. Nerve unchanged,
    # graph is isomorphic, and index magnitude stays invariant in a chosen
    # (but arbitrary) orientation of the reconstructed chart.
    rng=np.random.default_rng(119);pa=rng.permutation(L*L);pw=rng.permutation(L*L)
    Apr=torus_causal(L)[np.ix_(pa,pw)]
    nerp=nerve_betti_2(Apr);Gp=graph_from_overlap(Apr,L)
    assert nerp['betti']==[1,2,1]
    checks2=[overlap_flux_index_on_graph(Gp,L,q,1.)['index'] for q in (-1,0,1)]
    assert checks2==[1,0,-1]
    return {'status':'PASS','torus_orders':checks,'L6_flux_index':index,
            'relabeling_invariant_index_sequence':checks2,
            'central_result':'Causal witness overlap recovers an unlabeled 2D torus graph; with a separately CHOSEN coordinate framing, U1 flux and Wilson regulator it supports the standard 2D overlap index.',
            'not_derived':'Spatial torus and 2+1 causal relation are synthetic; spin orientation, gauge field strength, gamma matrices, Wilson parameter, time metric and Standard Model chirality are all inputs.'}

def su2_haar_average(beta,lam,b):
    def s(phi):
        x=1-np.cos(phi);return x-lam*x*x/2
    def w(phi):return (2/np.pi)*np.sin(phi)**2*np.exp(-beta*s(phi))
    z=quad(w,0,np.pi,epsabs=1e-12)[0]
    ew=quad(lambda p:w(p)*np.cos(p),0,np.pi,epsabs=1e-12)[0]/z
    e2=quad(lambda p:w(p)*np.cos(p)**2,0,np.pi,epsabs=1e-12)[0]/z
    # determinant(b I_2 - U)=(b^2+1)-2b cos phi, positive for b>1.
    den=b*b+1-2*b*ew
    matter_ew=((b*b+1)*ew-2*b*e2)/den
    return {'lambda':lam,'beta':beta,'b':b,'pure_W':ew,'pure_W2':e2,'with_fundamental_W':matter_ew,
            'positive_normalized_fermion_determinant_weight':den>0}

def gate_matter_center():
    rows=[su2_haar_average(2.,lam,b) for lam in (0.,.5,1.) for b in (1.01,2.,10.,1000.)]
    ad=[x for x in rows if x['lambda']==1.]
    assert all(abs(x['pure_W'])<1e-12 for x in ad)
    assert all(x['with_fundamental_W']<0 for x in ad)
    assert abs(ad[-1]['with_fundamental_W'])<abs(ad[1]['with_fundamental_W'])
    return {'status':'PASS','Haar_quadrature':rows,
      'adjoint_exact_formula':'<cos(phi)>_with_fund = -[2 b/(b²+1)] <cos²(phi)>_pure_adj at all b>1; pure adjoint Wilson = 0',
      'physical_mechanism':'Dynamical fundamental matter explicitly breaks the pure-adjoint center selection rule without changing its bare pure-glue action. Large b decouples this loop effect.',
      'limitations':'One-site SU2 Haar toy with an inserted finite Wilson loop determinant, not 4D nonabelian gauge/fermion coupled action, RG running or vacuum unification.'}

# local basis |00>,|01>,|10>,|11> in each lab, each has 2 modes

def twocopy_state():
    s=np.zeros(16,dtype=complex)
    for a,b in ((0,3),(1,2),(2,1),(3,0)):
        s[4*a+b]=.5
    return s

def projectors_local():
    p0=np.diag([1,0,0,0]);p1=np.diag([0,1,1,0]);p2=np.diag([0,0,0,1]);
    Z=np.zeros((4,4),complex);Z[1,1]=1;Z[2,2]=-1
    X=np.zeros((4,4),complex);X[1,2]=X[2,1]=1
    return p0,p1,p2,X,Z

def bell_CHSH(rho):
    p0,p1,p2,X,Z=projectors_local()
    E=p0+p2
    A0=E+Z;A1=E+X
    B0=E+(-Z+X)/np.sqrt(2)
    B1=E+(-Z-X)/np.sqrt(2)
    for O in (A0,A1,B0,B1):
        assert np.linalg.norm(O@O-np.eye(4))<1e-12
        number=np.diag([0,1,1,2]);assert np.linalg.norm(O@number-number@O)<1e-12
    e=lambda A,B:float(np.trace(rho@np.kron(A,B)).real)
    return e(A0,B0)+e(A0,B1)+e(A1,B0)-e(A1,B1)

def singlecopy_density(copy):
    # single photon only in the indicated copy (index 0 or1)
    s=np.zeros(16,complex)
    if copy==0:
        s[4*2+0]=1/np.sqrt(2) # Alice first mode on, Bob vacuum
        s[4*0+2]=1/np.sqrt(2)
    else:
        s[4*1+0]=1/np.sqrt(2)
        s[4*0+1]=1/np.sqrt(2)
    return np.outer(s,s.conj())

def local_twirl(rho):
    na=np.array([0,1,1,2]);nB=na.copy()
    charges=np.array([na[a] for a in range(4) for b in range(4)])
    mask=charges[:,None]==charges[None,:]
    return rho*mask

def gate_ssr_Bell():
    s=twocopy_state();assert np.linalg.norm(s)**2==1
    pure=np.outer(s,s.conj());rho=local_twirl(pure)
    s2=bell_CHSH(rho)
    assert abs(s2-(1+np.sqrt(2)))<1e-12
    # Three sectors weights p(n_A)=1/4,1/2,1/4.
    psector={k:float(np.trace(rho[np.ix_([4*a+b for a in range(4) if int(a).bit_count()==k for b in range(4)],
                              [4*a+b for a in range(4) if int(a).bit_count()==k for b in range(4)])]).real) for k in (0,1,2)}
    assert all(abs(psector[k]-([.25,.5,.25][k]))<1e-12 for k in range(3))
    vac=np.zeros((16,16),complex);vac[0,0]=1
    S=[]
    for eta in (0.,.2,.4,.6,.8,.9,1.):
        r=eta**2*pure+eta*(1-eta)*(singlecopy_density(0)+singlecopy_density(1))+(1-eta)**2*vac
        r=local_twirl(r)
        assert abs(np.trace(r)-1)<1e-12
        S.append({'survival_probability_per_photon_eta':eta,'SSR_valid_unconditional_CHSH':bell_CHSH(r)})
    # Explicit detector survival law at these supplied measurement settings.
    # Derive by expanding the vacuum, one-photon, and two-photon sectors.
    for row in S:
        eta=row['survival_probability_per_photon_eta']
        assert abs(row['SSR_valid_unconditional_CHSH']-(2-4*eta+(3+np.sqrt(2))*eta**2))<1e-12
    critical=4/(3+np.sqrt(2))
    assert 0.9<critical<1.
    # For two-copy state, operational SSR-Bell >2 without postselection,
    # yet a fixed measurement can be ineffective under loss; no claim all
    # eta values violate Bell or this is a loophole-free experimental test.
    return {'status':'PASS','two_copy_local_charge_sector_probabilities':psector,
      'CHSH_exact':s2,'formula':'S=1+sqrt(2): p=1/2 sector has Bell 2sqrt2 and p=1/2 product sectors yield 2',
      'loss_with_all_runs_included':S,
      'fixed_measurements_exact_survival_law':'S(eta)=2-4 eta+(3+sqrt(2)) eta²; violation only for eta>4/(3+sqrt(2))',
      'fixed_measurements_symmetric_photon_survival_threshold':float(critical),
      'limitations':'Known two-copy activation of mode entanglement under U1 SSR; two ideal identical single-photon copies, no independent phase ref, supplied ideal measurements; realistic loss, SSR alignment and detector efficiency require lab modeling.'}

def hist_group_action(l0,l1,l2):
    # group G=S_l0 x S_l1 x S_l2 acts on the M=l0*l1 + l1*l2 possible links.
    perms=[list(itertools.permutations(range(n))) for n in (l0,l1,l2)]
    M=l0*l1+l1*l2
    lengths_by_g=[]
    all_orbits_poly=np.zeros(M+1,dtype=int)
    group_order=0
    for a,b,c in itertools.product(*perms):
        image=[]
        for x in range(l0):
            for y in range(l1):image.append(a[x]*l1+b[y])
        for y in range(l1):
            for z in range(l2):image.append(l0*l1+b[y]*l2+c[z])
        seen=set();cyc=[]
        for i in range(M):
            if i in seen:continue
            j=i;L=0
            while j not in seen:
                seen.add(j);j=image[j];L+=1
            cyc.append(L)
        arr=np.zeros(M+1,dtype=int);arr[0]=1
        for cycle_size in cyc:
            arr[cycle_size:]+=arr[:-cycle_size].copy()
        all_orbits_poly+=arr
        lengths_by_g.append(cyc)
        group_order+=1
    assert group_order==math.factorial(l0)*math.factorial(l1)*math.factorial(l2)
    assert np.all(all_orbits_poly%group_order==0)
    orbit_poly=all_orbits_poly//group_order
    return orbit_poly,lengths_by_g,group_order

def gate_history_quotient():
    poly,cycles,order=hist_group_action(2,4,2)
    M=16
    unlabeled=int(sum(poly))
    theta=2.5
    z=np.exp(1j*theta)
    unweighted_orbit_amplitude=sum(int(v)*z**k for k,v in enumerate(poly))
    groupoid_amplitude=(1+z)**M/order
    ordinary_labeled=(1+z)**M
    ratio=abs(unweighted_orbit_amplitude)/abs(groupoid_amplitude)
    large=[]
    for N in (8,16,32,64):
        a=N//4;b=N//2;c=N//4;bits=N*N//4
        lg=math.lgamma(a+1)+math.lgamma(b+1)+math.lgamma(c+1)
        lower_log=(bits*np.log(2)-lg)/np.log(10)
        large.append({'N':N,'bits':bits,'log10_labeled_histories':bits*np.log10(2),
                      'log10_orbit_count_lower_bound':lower_log,
                      'log10_group_size':lg/np.log(10)})
    assert unlabeled>0 and lower_log>200
    return {'status':'PASS','layer_counts':[2,4,2], 'G_order':order,
      'M':M,'unlabeled_history_edge_count_polynomial':list(map(int,poly)),
      'number_unlabeled_layered_histories':unlabeled,
      'Burnside_sum_relation':'sum_fixed_z / |G| counts orbits; quotient weights not equal to a groupoid 1/|Aut| weighting',
      'theta':theta,'unlabeled_complex_sum_real_imag':[unweighted_orbit_amplitude.real,unweighted_orbit_amplitude.imag],
      'groupoid_weighted_sum_real_imag':[groupoid_amplitude.real,groupoid_amplitude.imag],
      'magnitude_ratio_orbit_unweighted_over_groupoid':ratio,
      'large_N_entropy_bounds':large,
      'physical_message':'Removing layer-preserving label permutations costs exp(O(N log N)) but this family retains exp(O(N²)) distinct orbits; automorphism weighting changes quantum amplitudes and does not itself create a 4D phase.',
      'limit':'Layered incidence matrices with marked layer membership, not all unlabelled posets or a fundamental causal path measure. Orbit sum and groupoid weighting represent distinct model choices.'}

def gate_flavor_connectivity():
    xs=sp.symbols('x_e x_mu x_tau')
    zero_sum=sp.Matrix([[1,1,1]])
    edges=[(0,1),(1,2),(0,2)]
    results=[]
    for mask in range(8):
        chosen=[edges[j] for j in range(3) if mask&(1<<j)]
        eq=[ [1 if k==a else -1 if k==b else 0 for k in range(3)] for a,b in chosen]
        A=zero_sum.col_join(sp.Matrix(eq)) if eq else zero_sum
        rank=A.rank()
        dim=3-rank
        results.append({'allowed_offdiagonal_Yukawa_edges':chosen,'rank_with_zero_sum':rank,'remaining_family_difference_dimension':dim})
    assert [r['remaining_family_difference_dimension'] for r in results]==[2,1,1,0,1,0,0,0]
    # For X=L_mu-L_tau, the Weinberg Majorana operator LiLjHH can be
    # neutral only for X_i+X_j=0: (e,e),(mu,tau) on unbroken U1.
    X=[0,1,-1]
    allowed=[(i,j) for i in range(3) for j in range(i,3) if X[i]+X[j]==0]
    assert allowed==[(0,0),(1,2)]
    # Check all perturbative anomaly equations directly for a 2-parameter
    # generation-dependent hypercharge deformation with 3 sterile nu^c.
    p,q=sp.symbols('p q'); family_charges=[p,q,-p-q]
    linear_gauge=sp.Integer(0); linear_grav=sp.Integer(0); cubic=sp.Integer(0)
    cubic_without_nu=sp.Integer(0)
    for x in family_charges:
        multiplets=[(6,1),(3,-4),(3,2),(2,-3+6*x),(1,6-6*x),(1,-6*x)]
        cubic+=sum(mult*y**3 for mult,y in multiplets)
        cubic_without_nu+=sum(mult*y**3 for mult,y in multiplets[:-1])
        linear_grav+=sum(mult*y for mult,y in multiplets)
        linear_gauge+=(3*1+(-3+6*x))
    assert sp.simplify(cubic)==sp.simplify(linear_grav)==sp.simplify(linear_gauge)==0
    cubic_without_nu=sp.factor(cubic_without_nu)
    assert cubic_without_nu==-648*p*q*(p+q)
    return {'status':'PASS','rank_table':results,'one_Higgs_three_generation_Yukawa_tree_minimum_edges':2,
      'unbroken_Lmu_minus_Ltau_allowed_Weinberg_operator_indices':allowed,
      'with_three_nu_c_two_parameter_cubic_anomaly':str(sp.factor(cubic)),
      'without_nu_c_generic_two_parameter_cubic_anomaly':str(cubic_without_nu),
      'linear_anomalies_zero':str(sp.factor(linear_gauge))+';'+str(sp.factor(linear_grav)),
      'Majorana_texture_for_X_0_plus1_minus1':'[[*,0,0],[0,0,*],[0,*,0]]',
      'core_implication':'Given one neutral Higgs and a connected graph of renormalizable offdiagonal charged-lepton Yukawa couplings, family-difference U1 charge shifts are forced to zero by linear constraints. But observed PMNS mixing can instead arise in the neutrino sector or broken symmetries.',
      'limitation':'The full charged-lepton Yukawa graph and global gauge group are assumed; flavor connectivity does not emerge from the causal torus and no Yukawa masses or oscillation probabilities are predicted.'}

def all_gates():
    gates={'causal_torus_overlap_chirality_flux':gate_torus(),
           'dynamical_fundamental_center':gate_matter_center(),
           'two_copy_particle_SSR_Bell':gate_ssr_Bell(),
           'unlabeled_history_group_action_entropy':gate_history_quotient(),
           'anomaly_free_flavor_graph':gate_flavor_connectivity()}
    assert all(x['status']=='PASS' for x in gates.values())
    return {'status':'PASS','TOE_solved':False,'4d_gravity_derived':False,'SM_chirality_derived':False,
            'Born_rule_derived':False,'five_gates':gates,
            'provenance':'Prior repo overlap index is standard; our new bridge reconstructs spatial 2D torus adjacency from order before using that known lattice regulator. All conclusions conditional.',
            'references':['https://arxiv.org/abs/2611.06102','https://www.nature.com/articles/s41598-018-20034-8',
                          'https://doi.org/10.1103/PhysRevA.82.042116','https://doi.org/10.1088/1361-6382/acc50c',
                          'https://doi.org/10.1103/PhysRevX.14.031033']}

def main():
    out=all_gates();OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'status':out['status'],'gates':list(out['five_gates']),
         'torus_betti':[v['nerve']['betti'] for v in out['five_gates']['causal_torus_overlap_chirality_flux']['torus_orders']],
         'CHSH_two_copies':out['five_gates']['two_copy_particle_SSR_Bell']['CHSH_exact'],
         'number_unlabeled_2_4_2':out['five_gates']['unlabeled_history_group_action_entropy']['number_unlabeled_layered_histories'],
         'file':str(OUT)}))
if __name__=='__main__':main()