"""A declared W33 link-scalar EFT, relative boundary mode and UV stress test.

Prior mathematics: BT545--547, BT742/744, Pass5089 and5396--5401.
Resistance7/10: Pass4040/4044. Deconstruction/boundary breaking:2606.02728.
The graph is an internal gauge quiver on supplied4D spacetime, not spacetime.
"""
import pathlib,sys,json,math,importlib.util
from fractions import Fraction as Q
import numpy as np
import networkx as nx
import sympy as sp
R=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('native_prior',R/'analysis/w33_levi_kirchhoff_cycle_projector.py')
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
MP=2.435e18;CHI=.0756**4

def geometry():
    W,pts=prior.build_w33();G,lines=prior.build_levi(W,pts)
    edges=sorted(tuple(sorted(e))for e in G.edges());ei={e:i for i,e in enumerate(edges)}
    B=np.zeros((80,160),dtype=np.int64)
    for i,(u,v)in enumerate(edges):B[u,i]=-1;B[v,i]=1
    cycles=prior.simple_cycles_fixed_length(G,8)
    C=np.zeros((160,len(cycles)),dtype=np.int64)
    for j,c in enumerate(cycles):
        for u,v in zip(c,c[1:]+c[:1]):C[ei[tuple(sorted((u,v)))],j]=1 if u<v else -1
    assert len(cycles)==1620 and np.all(B@C==0)
    K=C@C.T;assert np.array_equal(K@K,160*K)
    return G,edges,B,C,K

def boundary_data(G,edges,B,C,K):
    u=0;dist=nx.single_source_shortest_path_length(G,u)
    v=min(x for x,d in dist.items()if d==4)
    j=np.zeros(80,dtype=np.int64);j[u]=-1;j[v]=1
    L=B@B.T
    # Exact Laplacian inverse on sum-zero vectors using known nonzero spectrum.
    x=sp.symbols('x');poly=sp.invert(x,(x-4)*(x-8)*(x*x-8*x+10))
    phi=[Q(0)for _ in range(80)];w=j.copy()
    for k in range(4):
        a=poly.expand().coeff(x,k);coef=Q(int(sp.numer(a)),int(sp.denom(a)))
        phi=[a+coef*int(b)for a,b in zip(phi,w)];w=L@w
    assert [sum(Q(int(L[i,k]))*phi[k]for k in range(80))for i in range(80)]==list(j)
    h=[phi[b]-phi[a]for a,b in edges];res=phi[v]-phi[u]
    assert res==Q(7,10)and sum(t*t for t in h)==res
    paths=list(nx.all_shortest_paths(G,u,v));assert len(paths)==4
    path_vectors=[]
    for path in paths:
        z=np.zeros(160,dtype=np.int64)
        for a,b in zip(path,path[1:]):z[edges.index(tuple(sorted((a,b))))]=1 if a<b else -1
        assert np.array_equal(B@z,j)and sum(Q(int(a))*b for a,b in zip(z,h))==res
        path_vectors.append(z)
    I=[i for i in range(80)if i not in [u,v]]
    hf=np.array([float(t)for t in h]);P=K/160
    Prel=P+np.outer(hf,hf)/float(res)
    assert np.max(abs(B[I]@Prel))<1e-12 and np.max(abs(Prel@Prel-Prel))<1e-12
    return dict(boundary_vertices=[u,v],distance=4,shortest_paths=paths,
        shortest_path_count=4,resistance=str(res),unit_current_edge_flow=[str(t)for t in h],
        full_gauge_rank=79,interior_gauge_rank=78,full_gauge_phase_modes=81,relative_phase_modes=82,
        cycle_potential_lifted_modes=81,remaining_boundary_modes=1,
        exact_inverse_polynomial=str(poly),relative_projector_error=float(np.max(abs(Prel@Prel-Prel))),
        phase_normalization='Cycle constraints set theta=B^T phi. Unit boundary phase psi=phi[v]-phi[u] has minimum-norm representative h/R, h=B^T Lplus(e_v-e_u). ||h||²=R and ||h/R||²=1/R. Thus fa=F/sqrt(R) when the supplied QCD anomaly is one.',
        integral_scope='Every u-v path has phase psi modulo integer closed-cycle phases; primitive boundary winding has period2pi. Prior5089 owns integral apartment generation. Anomaly-one and NDW1 are EFT inputs until a UV anomaly sector is supplied.')

def quality_rows(fa=1e11):
    rows=[]
    for s in range(1,7):
        # Uniform subdivision has s unit resistors per old edge; the full
        # 81-cycle space persists and the boundary resistance is s*7/10.
        resistance=Q(7*s,10);F=fa*math.sqrt(float(resistance));degree=4*s
        logA=math.log(2)+degree*math.log(F/math.sqrt(2))-(degree-4)*math.log(MP)
        ratio=math.exp(logA)/CHI
        # Four shortest open paths all have the same phase after cycle locking.
        coherent=4*ratio;theta=coherent/(1-3*coherent)if coherent<1/3 else None
        cyc_degree=8*s
        logcycle=math.log(2)+cyc_degree*math.log(F/math.sqrt(2))-(cyc_degree-4)*math.log(MP)
        # C_s C_s^T has81 positive eigenvalues160*s (a prior tight frame lifted).
        logm2=math.log(160*s)+logcycle-2*math.log(F)
        logm2EFT=math.log(160*s)+math.log(2)+cyc_degree*math.log(F/math.sqrt(2))-(cyc_degree-4)*math.log(F)-2*math.log(F)
        rows.append(dict(subdivision=s,vertices=80+160*(s-1),edges=160*s,interior_gauge_factors=78+160*(s-1),
            closed_cycle_rank=81,relative_phase_modes=82,shortest_cycle_length=8*s,shortest_boundary_path_degree=degree,
            resistance=str(resistance),fa_input_GeV=fa,link_F_input_GeV=F,shortest_path_count=4,
            one_path_amplitude_over_chi=ratio,coherent_four_path_amplitude_over_chi=coherent,
            sufficient_uniform_theta_bound=theta,shortest_path_quality_pass=theta is not None and theta<1e-10,
            Planck_cycle_mass_over_QCD_mass=math.exp(.5*logm2)/(math.sqrt(CHI)/fa),
            EFT_cycle_gap_over_F_if_matching_scale_F=math.exp(.5*logm2EFT)/F))
    return dict(rows=rows,first_coherent_shortest_path_pass=next(r['subdivision']for r in rows if r['shortest_path_quality_pass']),
        input='fa1e11GeV, unit coefficients per shortest path, MP2.435e18GeV, chi(.0756GeV)^4. Potential includes2Re(c product links/MP^(d-4)).',
        scope='Only four leading shortest-path operators and coherent phases screened. Not a bound on all Wilson coefficients, all higher operators, UV mediator effects, threshold running or cosmology. The single-phase bound assumes81 cycle modes are locked above QCD; Planck-only cycle masses explicitly test that assumption.',
        refinement='Uniform subdivision adds new link scalars and gauge sites; it is not a graph cover or the forbidden all-odd signed2lift of4173. Its primitive cycles have length8s, all lifted apartments span the same81-dimensional integral cycle lattice.',
        action='Kinetic sum_edges |D Phi|², gauge U1 at all interior vertices and none at the two boundaries. Nonnegative potential sum_edges lambda_e(|Phi|²-F²/2)² + sum_apartments |Pplus-Pminus|²/Lambda_c^(8s-4), where Pplus and Pminus multiply the4s link fields of each sign. B C=0 makes Pplus and Pminus transform identically, so their difference norm is gauge invariant. Equal link vevs and a flat cycle phase are exactly stationary with zero potential; unlike a negative high-degree cosine term alone the polynomial potential is bounded below. Its phase cross term has amplitude2(F/sqrt2)^(8s)/Lambda_c^(8s-4). Supplied QCD term -chi cos(psi+theta0). Radials/vevs, cycle matching scale and anomaly coefficient supplied. Lambda_c=F for large cycle operators needs its own UV completion.')

def mass_matrix(length,phase,closing=1.,r=1/math.sqrt(2)):
    M=np.eye(length,dtype=complex)*r*np.exp(1j*phase/length)
    for i in range(length-1):M[i,i+1]=1
    M[-1,0]=closing
    return M

def winding_coefficient(n,r=1/math.sqrt(2)):
    assert n>=3 and 0<r<1
    return (-1)**(n+1)*r**n*(2/(n*(n-1)*(n-2))-4*r*r/(n*(n-1)*(n+1))+2*r**4/(n*(n+1)*(n+2)))

def uv_chain():
    out=[]
    for length in [4,8,12,16,20,24]:
        r=1/math.sqrt(2);c=winding_coefficient(length,r)
        amplitude=3*length*abs(c)/(8*math.pi**2)
        # Dimensionless matrix eigenvalues independently determine CW Fourier.
        grid=256;phases=2*math.pi*np.arange(grid)/grid;values=[];openvalues=[];minmass=10.
        for psi in phases:
            for close,target in [(1.,values),(0.,openvalues)]:
                M=mass_matrix(length,psi,close);ev=np.linalg.eigvalsh(M.conj().T@M)
                minmass=min(minmass,float(np.sqrt(ev.min())))
                target.append(float(-3/(16*math.pi**2)*np.sum(ev**2*(np.log(ev)-1.5))))
        numeric=float(2*np.mean(np.array(values)*np.cos(phases)))
        assert abs(numeric+3*length*c/(8*math.pi**2))<1e-13
        assert np.ptp(openvalues)<1e-12
        F=1e11*math.sqrt(.7*(length/4))
        out.append(dict(length=length,first_harmonic_CW_amplitude_over_F4=amplitude,
            numeric_cosine_coefficient=numeric,analytic_cosine_coefficient=-3*length*c/(8*math.pi**2),
            open_chain_phase_variation_over_F4=float(np.ptp(openvalues)),min_sampled_fermion_mass_over_F=minmass,
            F_input_GeV=F,first_harmonic_amplitude_over_chi=amplitude*F**4/CHI))
    L=16;qs=sp.symbols('q0:'+str(L));qb0=sp.symbols('qb0')
    qbs=[qb0]+[-t for t in qs[:-1]]
    anomaly=sp.expand(sum(qs)+sum(qbs));assert anomaly==qs[-1]+qb0
    return dict(rows=out,
        field_assignment='For path v0=u,...,vL=v, Phi_i has X(head)+1,X(tail)-1. LH Qi=(3,1,-1/3) has X(v_i)=-1, Qbari=(bar3,1,+1/3) has X(v_(i-1))=+1; endpoint gauges absent. Every interior site has one Qi and one Qbar_(i+1) with opposite X, color-conjugate, oppositeY. All gauge, cubic and mixed gravitational anomalies cancel site by site.',
        renormalizable_terms='y_i Phi_i Qi Qbari + M_i Qi Qbar_(i+1) for i<L. The bare closing mass mu Q_L Qbar_1 is ALSO gauge invariant: both endpoint fields are neutral under every interiorU1. It explicitly breaks the candidate boundary PQ and cannot be forbidden by this gauge group alone.',
        conditional_QCD_anomaly='If mu=0, choose PQ(Phi_i)=1/L, PQ(Qi)=-i/L, PQ(Qbari)=(i-1)/L for i=1..L. Every diagonal Yukawa and interior mass is invariant; sum_i[PQ(Qi)+PQ(Qbari)]=-1 gives QCD anomaly magnitude one in the color-fundamental convention. The closing mass has PQ charge-1 and is gauge allowed. Thus the attempted chain supplies anomaly one only under an additional protected-zero/locality assumption for mu.',
        additional_Abelian_protection_obstruction=dict(symbolic_color_anomaly=str(anomaly),closing_bilinear_charge=str(qs[-1]+qb0),
            statement='For any added ordinary U1 protection, unchanged chain inventory, gauge-neutral nonzero interior masses Mi, and zero mixed color anomaly from other sectors, Xi(Qbari+1)=-Xi(Qi). Hence sum_i Xi(Qi+Qbari)=Xi(QL)+Xi(Qbar1). Color anomaly cancellation forces the closing bilinear invariant. Adding only colorless fields cannot change this. This is a telescoping special case of the credited determinant obstruction.',
            escapes='Extra colored anomaly sectors, gauge-charged mass spurions, nonlocal/higher-dimensional locality or inflow change hypotheses. No nonabelian or all-model no-go asserted.'),
        determinant='det M = product_i(y_i Phi_i) + (-1)^(L-1) mu product_(i<L) M_i. With mu=0 all singular values are independent of the boundary phase; with nonzero mu the relative phase enters CW. Eliminating mu requires extra UV input such as a justified boundary-locality rule or further protection, not an assumed zero.',
        Fourier_derivation='For mu=M_i=F and yPhi/F=r exp(i psi/L), eigen mass²/F²=1+r²+2r cos((psi+2pi k)/L). Fourier of log(1+r exp(ix))+conj has l_n=(-1)^(n+1)r^n/n. Multiplication by(1+r²+2r cosx)^2 gives c_n=(-1)^(n+1)r^n[2/(n(n-1)(n-2))-4r²/(n(n-1)(n+1))+2r4/(n(n+1)(n+2))]. CW Dirac color3 first harmonic=-3L c_L F4/(8pi²).',
        scope='An explicit unsuccessful renormalizable anomaly-sector completion, not a general no-go for deconstruction. Constant fermion masses and couplings are supplied. Coherent real coefficients illustrate an allowed non-Planck-suppressed potential; a relative complex closing mass supplies an unconstrained CP phase. No all-harmonic theta minimum or full RG claimed.',
        prior='General heavy-mediation caveat2212.00102; deconstructed boundary breaking2606.02728; determinant principle1003.0941. The cyclic mass matrix and its Fourier analysis are standard methods applied to this explicit attempted completion.')

def scalar_factorization(geo,boundary):
    G,edges,B,C,K=geo;u,v=boundary['boundary_vertices']
    I=[i for i in G if i not in [u,v]];seen={};pair=None
    for j in range(C.shape[1]):
        for sign in [1,-1]:
            cols=np.flatnonzero(C[:,j]==sign)
            for k in [2,3,4]:
                take=cols[:k];charge=np.sum(B[:,take],axis=1);key=tuple(int(t)for t in charge[I])
                row=dict(native_prefix_size=k,native_edge_indices=take.tolist(),
                    native_edges=[list(edges[e])for e in take],full_vertex_charge=charge.tolist(),
                    parent_cycle=[[int(e),int(C[e,j])]for e in np.flatnonzero(C[:,j])])
                old=seen.get(key)
                if old and old['full_vertex_charge']!=row['full_vertex_charge']:
                    pair=[old,row];break
                seen[key]=row
            if pair:break
        if pair:break
    assert pair is not None
    delta=np.array(pair[0]['full_vertex_charge'])-pair[1]['full_vertex_charge']
    assert all(delta[i]==0 for i in I)and delta[v]==-delta[u]and abs(delta[v])==1
    h=[Q(t)for t in boundary['unit_current_edge_flow']];res=Q(boundary['resistance'])
    pqs=[sum(h[e]for e in row['native_edge_indices'])/res for row in pair]
    assert abs(pqs[0]-pqs[1])==1
    s=4;F=1e11*math.sqrt(.7*s);epsilon=1e-3
    amplitude=2*epsilon*F**4/2**(2*s)
    return dict(witness=pair,relative_PQ_charges=[str(t)for t in pqs],mixing_PQ_charge=str(pqs[0]-pqs[1]),
        construction='Factor each chosen positive/negative cycle half-product by prefix scalars A_k, with positive renormalizable terms |M A2-Phi1 Phi2|² and |M Ak-A_(k-1) Phik|², then M²|A_(4s),plus-A_(4s),minus|². Prefix scalar charge is the sum of its link charges. At tree level Ak=product_(i<=k) Phii/M^(k-1), so cycle matching gives |Pplus-Pminus|²/M^(8s-4). Coefficients, radial sector and M supplied.',
        failure='The explicit two prefix fields A and B have identical interior gauge charges but differ by one unit of boundary PQ charge. Therefore epsilon M²|A-exp(i delta) B|² is gauge invariant, positive, renormalizable and PQ breaking. Canonical prefix factorization of the apartment potential admits it; another mediator architecture is not ruled out by this witness.',
        subdivision_lift='Each of the two native edges in a prefix expands to s links. These two fields represent2s links each, so their bilinear replaces a4s-link boundary operator by a canonical dimension2 mixing. New degree2 vertices cancel inside each complete native-edge chain, so their interior charge equality survives refinement.',
        benchmark=dict(s=s,old_link_EFT_F_input_GeV=F,matching_M_input_GeV=F,epsilon_input=epsilon,
            prefix_link_count_each=2*s,prefix_VEV_over_F=2**(-s),mixing_dimension=2,
            mixing_potential_amplitude_GeV4=amplitude,mixing_amplitude_over_chi=amplitude/CHI),
        normalization_caveat='Auxiliary scalar kinetic terms change the low-energy phase metric. The benchmark reuses F from the link-only EFT, not a newly matched physical fa. The mixing potential amplitude on the tree constraint sheet is computed; no complete scalar spectrum or revised axion decay constant claimed.',
        interpretation='This realizes the known heavy-mediation concern2212.00102 on explicit native charge vectors. Graph path length protects the restricted link inventory; it is not a selection rule on a larger mediator inventory.')

def build():
    G,edges,B,C,K=geometry();boundary=boundary_data(G,edges,B,C,K)
    return dict(status='PASS_NATIVE_BOUNDARY_EFT_AND_TWO_FAILED_UV_REPAIRS',
        native=dict(vertices=80,edges=160,girth=8,apartments=1620,cycle_rank=81,cycle_frame_bound=160,
            no_invariant_single_axion='Prior BT742 establishes the cycle module is the irreducible81-dimensional Steinberg representation. A symmetry-preserving quadratic potential cannot single out one zero mode inside it. New boundaries explicitly break that symmetry.'),
        boundary=boundary,quality=quality_rows(),UV=uv_chain(),scalar_factorization=scalar_factorization((G,edges,B,C,K),boundary),
        prior_sources=['analysis/w33_levi_kirchhoff_cycle_projector.py','analysis/BT742_steinberg_identification_schur.md','analysis/w33_pass5089_integral_oriented_apartment_presentation.py','analysis/w33_pass5396_5401_allq_apartment_tight_frame.py','analysis/w33_pass4033_4040_physics_continuation.py','analysis/w33_pass4041_4048_eight_physics_expansion.py','analysis/2026-11-03_optimal_5load_apartment_hamiltonian.md'],
        external_sources=['https://arxiv.org/abs/2606.02728','https://arxiv.org/abs/2212.00102','https://arxiv.org/abs/1003.0941'],
        boundary_of_claim='A supplied4D link-scalar EFT with explicit native incidence, phase normalization, leading quality operators and a renormalizable completion stress test. The chain supplies anomaly one if its gauge-allowed closing mass is removed by extra input; protected removal of that mass, cycle-locking UV origin and a common gravity/matter action remain open. No complete TOE or observational prediction.')
if __name__=='__main__':
    d=build();(R/'data/toe_20261105_native_boundary_axion.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],'first_coherent_subdivision',d['quality']['first_coherent_shortest_path_pass'],flush=True)
