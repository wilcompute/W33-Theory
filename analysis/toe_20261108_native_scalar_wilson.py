"""Declared charged complex scalar on the actual native four-period cover.

All27 Bloch bands retained. Continuous time and unit hopping/lattice units.
An external L-cell compactification, scalar mass and gauge coupling are inputs.
Prior native graph/metric: Pass11991,12189 and Oct27 propagation/response.
Standard graph heat-kernel/holonomy methods: Kan-Shiraishi2212.07049 sectionII.
No physical photon, selected compactification, CC or TOE follows.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import sys
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass12189_12193_five_bridges import graph_inputs


@lru_cache(None)
def geometry():
    _,B,V,G,a,b=graph_inputs()
    V=np.rint(V).astype(int)
    h=V-B[:,1:]@np.linalg.solve(B[:,1:].T@B[:,1:],B[:,1:].T@V)
    M=np.rint(h.T@h).astype(int)
    assert np.max(abs(h.T@h-M))<1e-12
    assert np.max(abs(M/27-G))<1e-13
    assert np.all(np.bincount(np.r_[a,b],minlength=27)==10)
    return B,V,a,b,h,M


def exact_normalization():
    M=sp.Matrix(geometry()[-1].tolist())
    A=M[:3,:3];b=M[:3,3];s=sp.factor(M[3,3]-(b.T*A.inv()*b)[0])
    assert s==sp.Rational(27,5) and A.inv()*b==sp.Matrix([0,-sp.Rational(3,5),-sp.Rational(1,2)])
    return dict(native_M=[[int(x) for x in row] for row in M.tolist()],noncompact_block_det=int(A.det()),
        Schur_scalar_kinetic=str(s),inverse_M44=str(M.inv()[3,3]),
        field_redefinition="A_noncompact'=A_noncompact+(0,-3/5,-1/2)*A4",
        compact_kinetic="f_theta^2=27/(5*g^2*L), theta=L*A4; sum electric energy over L cells, unit microscopic link kinetic 1/g^2.",
        reduced_quadratic_symbol="k^T M k/27 = (k3+A^-1*b*k4)^T A (k3+A^-1*b*k4)/27 + k4^2/5",
        continuum_radius="For this supplied leading common metric, R_effective=sqrt(5)*L/(2*pi) in lattice units. It is not a measured radius or a full-band dispersion identity.",
        caveat="Metric and engineered leading common cone are prior inputs. Scalar potential below uses actual full native covariant vertex Laplacian, not the engineered gauge magnetic matrix.")


def matrices(k,compact_cells=1,charge=1,voltages=None):
    """H, d_theta H, d_theta^2 H for H=D^dag D; batch last axes27x27."""
    _,V,a,b,_,_=geometry()
    if voltages is not None:V=np.asarray(voltages)
    k=np.atleast_2d(k)
    z=np.exp(1j*(k@V.T))
    H=np.zeros((len(k),27,27),complex)
    H[:,np.arange(27),np.arange(27)]=10
    Hp=np.zeros_like(H);Hpp=np.zeros_like(H)
    w=charge*V[:,3]/compact_cells
    for e,(i,j) in enumerate(zip(a,b)):
        H[:,i,j]-=z[:,e];H[:,j,i]-=z[:,e].conj()
        Hp[:,i,j]-=1j*w[e]*z[:,e];Hp[:,j,i]+=1j*w[e]*z[:,e].conj()
        Hpp[:,i,j]+=w[e]**2*z[:,e];Hpp[:,j,i]+=w[e]**2*z[:,e].conj()
    return H,Hp,Hpp


def grid(grid_size,compact_cells,theta,charge=1):
    """Unshifted periodic BZ trapezoid = actual finite noncompact torus."""
    base=np.asarray(list(product(range(grid_size),repeat=3)),float)*2*np.pi/grid_size
    return np.vstack([np.column_stack((base,np.full(len(base),(2*np.pi*n+charge*theta)/compact_cells)))
                      for n in range(compact_cells)])


def trace_sqrt_curvature(H,Hp,Hpp,mass):
    vals,U=np.linalg.eigh(H)
    assert np.min(vals)>-1e-10 and mass>0
    w=np.sqrt(np.maximum(vals,0)+mass**2)
    X=U.conj().transpose(0,2,1)@Hp@U
    Y=U.conj().transpose(0,2,1)@Hpp@U
    positive=np.sum(Y.diagonal(axis1=1,axis2=2).real/(2*w),axis=1)
    denominator=2*w[:,:,None]*w[:,None,:]*(w[:,:,None]+w[:,None,:])
    negative=np.sum(abs(X)**2/denominator,axis=(1,2))
    return w.sum(1),positive-negative


def energy(grid_size,compact_cells,mass,theta,charge=1,curvature=False,lowest_only=False):
    points=grid(grid_size,compact_cells,theta,charge);total=curv=0.
    for start in range(0,len(points),512):
        H,Hp,Hpp=matrices(points[start:start+512],compact_cells,charge)
        if curvature:
            E,C=trace_sqrt_curvature(H,Hp,Hpp,mass);total+=float(E.sum());curv+=float(C.sum())
        else:
            vals=np.linalg.eigvalsh(H)
            if lowest_only:vals=vals[:,:1]
            total+=float(np.sqrt(np.maximum(vals,0)+mass**2).sum())
    return (total/grid_size**3,curv/grid_size**3) if curvature else total/grid_size**3


def full_cover_spectrum(sizes,theta):
    """Independent real-space lifted graph, boundary twist on winding edges."""
    _,V,a,b,_,_=geometry()
    cells=list(product(*(range(s) for s in sizes)));idx={c:i for i,c in enumerate(cells)}
    N=27*len(cells);H=np.zeros((N,N),complex)
    for x in cells:
        for e,(i,j) in enumerate(zip(a,b)):
            end=np.array(x)+V[e];wrap=end//np.array(sizes);end=tuple(end%np.array(sizes))
            u=27*idx[x]+i;v=27*idx[end]+j;z=np.exp(1j*theta*wrap[3])
            H[u,u]+=1;H[v,v]+=1;H[u,v]-=z;H[v,u]-=z.conjugate()
    return np.linalg.eigvalsh(H)


def literal_winding_path():
    from w33_20261027_native_bloch_face_module import deck_loops
    _,V,a,b,_,_=geometry()
    loops,W,_=deck_loops(list(zip(a,b)),V)
    coeff=sp.Matrix(W).T.inv()*sp.Matrix([0,0,0,1])
    path=[]
    for c,walk in zip(coeff,loops):
        assert c.q==1
        segment=walk if c>=0 else [(e,-s) for e,s in walk[::-1]]
        path+=segment*abs(int(c))
    position=np.zeros(4,int);vertex=0
    for e,sign in path:
        assert vertex==(a[e] if sign==1 else b[e])
        vertex=b[e] if sign==1 else a[e];position+=sign*V[e]
    assert vertex==0 and position.tolist()==[0,0,0,1]
    return dict(start_end_vertex=0,primitive_period=position.tolist(),steps=len(path),
        signed_edges=[[int(e),int(s)] for e,s in path],
        winding_one_on_L_compact_cover="Repeat this literal based path L times; it has zero noncompact period and one compact winding. This proves a positive nonzero heat-walk coefficient, not minimal loop length.")


def winding_curvature_lower_bound(L,mass):
    r=literal_winding_path()["steps"]*L
    logbound=math.log(L)-.5*math.log(math.pi)+math.lgamma(r-.5)-math.lgamma(r+1)-(r-.5)*math.log(10+mass**2)
    return dict(walk_length=r,log10_numeric_lower_bound=logbound/math.log(10),
        exact_formula="V_theta_second(0)>=L*Gamma(r-1/2)/[sqrt(pi)*r!*(10+m^2)^(r-1/2)]>0; r=L times the literal based primitive winding-walk length.",
        proof="Keep only the forward/reverse winding-one walks based at vertex0 in each of L compact cells in exp(tA). All remaining walk coefficients are nonnegative after BZ3 projection. Integrate that one term in the trace-sqrt proper-time representation. Formula exact; printed log uses ordinary floating arithmetic.")


def produce(extended=False):
    rows=[]
    for L in (2,3,4,6):
        for mass in (.3,.8):
            samples=[]
            for n in (4,6,8,12):
                E0,C=energy(n,L,mass,0,curvature=True)
                Epi=energy(n,L,mass,np.pi)
                samples.append(dict(noncompact_grid=n,full_bands=27,compact_cells=L,mass=mass,
                    E0=E0,delta_V_pi=Epi-E0,V_theta_second_at_zero=C,
                    single_holonomy_normalized_curvature_at_g1=C*5*L/27))
            rows.append(dict(L=L,mass=mass,samples=samples,
                analytic_curvature_lower_bound=winding_curvature_lower_bound(L,mass),
                last_two_curvature_relative_change=abs(samples[-1]['V_theta_second_at_zero']/samples[-2]['V_theta_second_at_zero']-1),
                numerical_scope="Deterministic finite-torus samples; last-grid difference is a convergence diagnostic, not a rigorous infinite-volume error bound."))
    shape=[]
    for theta in (0,.3,1.,2.,np.pi):
        shape.append(dict(theta=theta,delta_V=energy(10,3,.3,theta)-energy(10,3,.3,0)))
    d=dict(status="NATIVE_27_BAND_CHARGED_COMPLEX_SCALAR_WILSON_POTENTIAL_NOT_TOE",
        action="S_matter=sum_sites |D_t chi|^2-m^2|chi|^2-sum_actual_edges |exp(i a_e)chi_head-chi_tail|^2. One complex charge1 scalar, continuous time, unit hopping; canonical time kinetic. Free scalar integrated exactly at fixed gauge background.",
        normalization=exact_normalization(),literal_winding_witness=literal_winding_path(),rows=rows,shape_control=shape,
        potential="V(theta)-V(0)=int_BZ3 dk/(2pi)^3 sum_n=0..L-1 sum_j=1..27 [sqrt(m^2+lambda_j(k,(2pi*n+theta)/L))-sqrt(m^2+lambda_j(k,2pi*n/L))]. Complex scalar has two real oscillators, hence coefficient1, not1/2.",
        analytic_curvature="For X=U^dag H' U,Y=U^dag H'' U,omega=sqrt(m^2+lambda): E''=sum_a Yaa/(2omega_a)-sum_ab |Xab|^2/[2omega_a omega_b(omega_a+omega_b)]. Stable at eigenvalue degeneracy.",
        positivity_proof="Regular native graph H=10I-A(theta). Exp(tA) expands into positive-weight walks. BZ3 integration projects zero noncompact period; sum compact momenta selects period multiple L. Paired winding walks give nonnegative coefficients times cos(w theta). In sqrt(X)=-1/(2sqrt(pi))*integral dt t^-3/2[exp(-tX)-I], this yields V(theta)-V(0)=sum_w>=1 c_w(1-cos(w theta)), c_w>=0. At positive mass all derivatives converge. Literal primitive e4 walk repeated L gives c_1>0, so theta=0 mod2pi is the unique global minimum and V''(0)>0 for this scalar inventory.",
        finite_grid_scope="Unshifted trapezoid is an actual periodic finite torus. Extra noncompact winding walks can alias at finite grid; this preserves positivity there but changes coefficients. Infinite-volume numerical limit needs controlled extrapolation.",
        finite_volume_upper_bound="Coefficientwise c_w(infinite BZ3)<=c_w(Nperiodic torus), since the latter adds nonnegative walks whose noncompact periods are multiples of N. Thus 0<Vtheta_second_infinite(0)<=Vtheta_second_N(0), and DeltaV_infinite(theta)<=DeltaV_N(theta). If N2 is a multiple of N1, the N2 winding set is a subset, so both upper bounds decrease. Analytic comparison of exact finite-volume quantities; floating results are not interval-certified roundoff bounds.",
        mass_normalization_boundary="At finite noncompact torus size N, all four holonomies are physical and the potential can mix them. The quantity C*5*g^2*L/27 is a single-holonomy normalized curvature diagnostic, NOT automatically a finite-torus pole eigenmass. The Schur single-scalar mass formula requires infinite noncompact volume, where constant noncompact connections shift the BZ integral and the potential is independent of them. A full finite-volume pole calculation needs the four-variable potential Hessian.",
        boundary="Scalar-only contribution, external L compactification, mass and unit microscopic scale. No native charged Dirac construction, SM charge identification, gauge quantum corrections, radion potential, selected lattice spacing, observed scalar mass, CC value, relic populations, Lorentzian quantum continuum or TOE completion. A stable scalar holonomy is not radius stabilization. Fermionic/boundary twists or extra fields can change the minimum.",
        prior_owners=["data/w33_pass11991_native_four_period_cover.json","analysis/w33_pass12189_12193_five_bridges.py","analysis/w33_20261027_native_bloch_face_module.py","analysis/2026-10-27_acoustic_vacuum_density.md","analysis/w33_20261108_five_boundary_bridges.py"],
        primary_context=["https://arxiv.org/html/2212.07049v2#S2","https://arxiv.org/abs/hep-ph/0105021"])
    if extended:
        d["extended_finite_volume_controls"]=[]
        for L,mass in ((3,.3),(6,.3),(6,.8)):
            for n in (20,28):
                E,C=energy(n,L,mass,0,curvature=True)
                d["extended_finite_volume_controls"].append(dict(L=L,mass=mass,noncompact_grid=n,E0=E,V_theta_second_at_zero=C,single_holonomy_normalized_curvature_at_g1=C*5*L/27))
    paths=d["prior_owners"]+[str(Path(__file__).relative_to(ROOT))]
    d["input_raw_sha256"]={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    return d


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",default="data/toe_20261108_native_scalar_wilson.json");p.add_argument("--extended",action="store_true")
    args=p.parse_args();d=produce(args.extended)
    (ROOT/args.out).write_text(json.dumps(d,indent=2)+"\n",encoding="utf-8")
    print(json.dumps([dict(L=x["L"],mass=x["mass"],curvature=x["samples"][-1]["V_theta_second_at_zero"],relative_change=x["last_two_curvature_relative_change"]) for x in d["rows"]]))
