"""Finite-native-path Wilson regulator, uniform gap and local heavy measure.

This deliberately CHANGES11991's nearest-edge kernel. The primitive deck is
native; a bounded cell tree and four closed period paths are supplied choices.
11519 owns the general relative-current/gap method; Luscher owns Abelian
measure reconstruction. The heavy onsite-reference construction is explicit.
"""
import json,itertools
from pathlib import Path
import numpy as np
import sympy as s
from scipy.linalg import eigh
from w33_pass12000_native_unitary_clock import native_paths
from w33_pass11991_native_four_period_cover import gamma4
ROOT=Path(__file__).resolve().parents[1]


def path_fields(phases,periods):
    edges,V,paths,tree,T,words=native_paths();vp=np.array(s.Matrix(V.tolist())*T.T.inv(),int)
    cells=list(itertools.product(*[range(n) for n in periods]));where={c:i for i,c in enumerate(cells)};n=len(cells)
    def walk(cell,a,word):
        c=np.array(cell);phase=0.
        for e,sign in word:
            u,v=edges[e]
            if sign>0:
                assert a==u;phase+=phases[where[tuple(c)],e];c=(c+vp[e])%periods;a=v
            else:
                assert a==v;c=(c-vp[e])%periods;phase-=phases[where[tuple(c)],e];a=u
        return tuple(c),a,np.exp(1j*phase)
    shifts=[np.zeros((27*n,27*n),complex) for _ in range(4)];coarse=[np.zeros((n,n),complex) for _ in range(4)];transport=np.zeros(27*n,complex)
    rev=lambda word:[(e,-sgn) for e,sgn in reversed(word)]
    maxrange=0
    for ic,c in enumerate(cells):
        for a,p in paths.items():
            _,dst,transport[27*ic+a]=walk(c,0,p);assert dst==a
            for mu,word in enumerate(words):
                full=rev(p)+word+p;end,b,phase=walk(c,a,full);assert b==a
                expect=tuple((np.array(c)+np.eye(4,dtype=int)[mu])%periods);assert end==expect
                shifts[mu][27*ic+a,27*where[end]+a]=phase;maxrange=max(maxrange,len(full))
        for mu,word in enumerate(words):
            end,a,phase=walk(c,0,word);assert a==0;coarse[mu][ic,where[end]]=phase
    lap=np.zeros((27*n,27*n),complex);L=np.zeros((27,27))
    for e in tree:
        a,b=edges[e];L[a,a]+=1;L[b,b]+=1;L[a,b]-=1;L[b,a]-=1
        for ic in range(n):
            aa,bb=27*ic+a,27*ic+b;p=np.exp(1j*phases[ic,e]);lap[aa,aa]+=1;lap[bb,bb]+=1;lap[aa,bb]-=p;lap[bb,aa]-=p.conjugate()
    U=np.diag(transport)
    assert max(np.max(abs(S-U.conj().T@np.kron(C,np.eye(27))@U)) for S,C in zip(shifts,coarse))<1e-12
    assert np.max(abs(lap-U.conj().T@np.kron(np.eye(n),L)@U))<1e-12
    return cells,shifts,coarse,lap,L,U,maxrange


def wilson(shifts):
    gamma,g5=gamma4();n=shifts[0].shape[0];D=3*np.eye(4*n,dtype=complex)
    for g,T in zip(gamma,shifts):D-=.5*(np.kron(np.eye(4)-g,T)+np.kron(np.eye(4)+g,T.conj().T))
    return D,np.kron(g5,np.eye(n))


def projector(Q):
    e,v=eigh(Q);return v[:,e>0]@v[:,e>0].conj().T,float(min(abs(e)))


def heavy_frame(D,G5,shift,steps=12):
    _,g5=gamma4();e,v=eigh(g5);F=np.kron(v[:,e>.5],np.eye(len(D)//4));initial=F.copy();minimum=1e99
    for t in np.linspace(0,1,steps+1)[1:]:
        # D has Wilsonmass1; masszeroD=D+I. Opticalshift>=4.
        Q=G5@((shift-1)*np.eye(len(D))+t*(D+np.eye(len(D))))
        P,gap=projector(Q);minimum=min(minimum,gap)
        gram=F.conj().T@P@F;e,u=eigh(gram);assert min(e)>.5
        F=P@F@(u/np.sqrt(e))@u.conj().T
    return F,initial,minimum


def payload():
    rng=np.random.default_rng(12002);periods=np.array([2,2,1,1]);phases=rng.uniform(-1e-6,1e-6,(4,135))
    cells,S,C,L,L0,U,R=path_fields(phases,periods);n=len(cells);kappa=4*27**2
    DN,G5N=wilson(S);DN+=kappa*np.kron(np.eye(4),L)
    DC,G5=wilson(C);lifted=[np.kron(t,np.eye(27)) for t in C];DF,_=wilson(lifted);DF+=kappa*np.kron(np.eye(4*n),L0)
    UG=np.kron(np.eye(4),U);factor_error=float(np.max(abs(DN-UG.conj().T@DF@UG)));assert factor_error<1e-8
    deg=int(max(np.diag(L0)));M=7+2*kappa*deg;coefficient=8*R+2*kappa*deg;epsilon=1/(4*coefficient)
    # Exact polynomial identity behind all-volume/free/allmomentum gap1.
    r=s.symbols('r0:4',nonnegative=True);square=sum(2*q-q*q for q in r)+(sum(r)-1)**2
    assert s.expand(square-(1+2*sum(a*b for a,b in itertools.combinations(r,2))))==0
    lam=np.linalg.eigvalsh(L0);assert lam[1]>1/27**2 and kappa*lam[1]>4
    shift=float(kappa*lam[1]);F,E,gap=heavy_frame(DC,G5,shift);P,_=projector(G5@(DC+shift*np.eye(len(DC))))
    intertwine=float(np.max(abs(F@F.conj().T-P)));assert intertwine<1e-10
    gauge=np.diag(np.exp(1j*rng.uniform(-2,2,n)));G=np.kron(np.eye(4),gauge);Dg=G.conj().T@DC@G;Fg,_,_=heavy_frame(Dg,G5,shift)
    columns=E.conj().T@G@E;covariance=float(np.max(abs(Fg-G.conj().T@F@columns)));assert covariance<1e-10
    # Uniform locality bound uses native finite range, not an inverseLaplacian.
    return dict(status='PASS',native_cells_tested=n,native_vertices_tested=27*n,Dirac_dimension_tested=108*n,
        cell_tree_edge_count=26,primitive_period_words='12000 nativefourperiodloops in actualclockalignedunimodularbasis',maximum_native_hopping_range=R,
        optical_coefficient=kappa,tree_maximum_degree=deg,exact_tree_gap_lower='1/729',exact_optical_mass_gap_lower=3,
        exact_free_acoustic_Wilson_gap_lower=1,exact_free_Wilson_norm_upper=7,exact_free_identity='Q4(k)^2=[1+2 sum_(mu<nu) r_mu r_nu]I4, r_mu=1-cos(k_mu) in[0,2]. Valid for ALL momenta and ALL periodic volumes.',
        full_operator_norm_upper=M,native_link_phase_perturbation_coefficient=coefficient,uniform_native_weak_phase_radius_charge1=epsilon,uniform_native_weak_phase_radius_maxcharge6=epsilon/6,uniform_weak_field_gap_lower='.75',
        native_tensor_factorization_error=factor_error,heavy_endpoint_projector_error=intertwine,heavy_frame_gauge_covariance_error=covariance,numerical_heavy_homotopy_gap=gap,
        exact_native_operator='DW_path=DW4(T_mu_native_paths)+kappa L_zero_voltage_cell_tree. Treeparalleltransportwithin each27cell conjugates this EXACTLY to DW4(U_mu_rootloops) tensor I27 +kappa Ispin,cell tensor Ltree. Every term is boundedrange inoriginalnativecover.',
        heavy_measure='Everypositive Ltree eigenmode has ReDW>=kappalambda-1>=3 forallU1links. HomotopeDW(t)=(kappalambda-1)I+t DW_mass0. Its startprojector isONSITE gamma5, commutingwith everygaugeaction. Kato transport gives a globallysmooth gaugecovariant heavyframe; unlike a freehoppingreference, no spatiallynonlocalgaugefix is needed.',
        locality='NativehoprangeR, normM anduniformgap give sign-projector polynomialtails withr=1-g²/M²<1, hencevolumeindependent exponentialdecay. The heavyKato generator and finite-homotopy transport retain quasilocality. Bounds are conservative andmaygive averylonglocalitylength.',
        conditional_Abelian_measure='The soleacousticblock is exactly a standardcoarse4D Wilson/overlap operator. With suppliedanomalyfreeintegercharges and ALLrequiredadmissibility/locality/globalsector hypotheses ofLuscher, itsknownAbelianmeasure theorem plus explicittrivialheavyblocks pullsback throughboundednativepaths/celltree. This is an existence reduction, not an implementednumericalLuscher acousticcurrent. NonAbelianSMmeasure remainsopen.',
        regulator_change='Thisis a newpath/tree regulator, NOT a proof ofallmomentumgap/locality for11991 originalnearestedge currentkernel. It selects a tree andfourcycles, breaks canonicity anduseslargeopticalcoupling; the oldboundary ispreserved.',
        prior=['11991 selectednative4periodquotient','12000 explicitnativecyclecompiler','11519 standardWilsonuniformgap andrelativeprojectorcurrent/locality','11984 distinctsuppliedT4hybridopticaldecoupling','11997 nonlocalglobaltreeframe andfinitecellgap'],
        primary=['https://arxiv.org/abs/hep-lat/9808010','https://arxiv.org/abs/hep-lat/9811032'])

if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass12002_native_path_overlap.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['maximum_native_hopping_range'],d['heavy_frame_gauge_covariance_error'])
