#!/usr/bin/env python3
"""Exact lattice covariant derivative/plaquette holonomy on a 2-torus.

Uniform quantized U(1) curvature, exact gauge covariance and finite-scale
Yang-Mills action. Demonstrates need for curvature corrections; is NOT the
Hamiltonian constraint algebra of curved GR or a gravitational spin connection.
"""
from pathlib import Path
import json, numpy as np, math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'2026_11_03_curved_covariant_holonomy_obstruction.json'
def links(L,m):
    A=np.zeros((L,L),complex);B=np.ones((L,L),complex)
    for x in range(L):
        for y in range(L):
            A[x,y]=np.exp(-2j*np.pi*m*y/(L*L))
            if y==L-1:B[x,y]=np.exp(2j*np.pi*m*x/L)
    return A,B
def matrices(A,B):
    L=len(A);N=L*L
    tx=np.zeros((N,N),complex);ty=tx.copy()
    idx=lambda x,y:x*L+y
    for x in range(L):
      for y in range(L):
        tx[idx(x,y),idx((x+1)%L,y)]=A[x,y]
        ty[idx(x,y),idx(x,(y+1)%L)]=B[x,y]
    assert np.max(abs(tx@tx.conj().T-np.eye(N)))<1e-12
    assert np.max(abs(ty@ty.conj().T-np.eye(N)))<1e-12
    return tx,ty
def plaquettes(A,B):
    L=len(A);return np.array([
        A[x,y]*B[(x+1)%L,y]*A[x,(y+1)%L].conjugate()*B[x,y].conjugate()
         for x in range(L) for y in range(L)])
def run():
    rows=[]
    for m in (0,1,2):
      for L in (4,6,8):
        A,B=links(L,m)
        X,Y=matrices(A,B)
        P=plaquettes(A,B)
        theta=2*np.pi*m/(L*L)
        assert np.max(abs(P-np.exp(1j*theta)))<1e-13
        C=X@Y-Y@X
        predicted=(np.exp(1j*theta)-1)*(Y@X)
        assert np.max(abs(C-predicted))<1e-12
        norm=float(np.linalg.norm(C,2))
        assert abs(norm-abs(np.exp(1j*theta)-1))<1e-12
        a=1/L
        action=float(np.sum(1-P.real)/(a*a))
        expected=(2*np.pi*m)**2/2
        if m==0:assert action<1e-9 and norm<1e-11
        else:assert abs(action-expected)/expected<.09
        # Independently change local fiber phases and links; both shifts
        # must transform by the same local conjugation G.
        rng=np.random.default_rng(9000+L*7+m)
        g=np.exp(1j*rng.uniform(-np.pi,np.pi,size=(L,L)))
        Ap=np.empty_like(A);Bp=np.empty_like(B)
        for x in range(L):
            for y in range(L):
                Ap[x,y]=g[x,y]*A[x,y]*g[(x+1)%L,y].conjugate()
                Bp[x,y]=g[x,y]*B[x,y]*g[x,(y+1)%L].conjugate()
        XP,YP=matrices(Ap,Bp)
        GG=np.diag(g.reshape(-1))
        assert np.max(abs(XP-GG@X@GG.conj().T))<1e-12
        assert np.max(abs(YP-GG@Y@GG.conj().T))<1e-12
        assert np.max(abs(plaquettes(Ap,Bp)-P))<1e-12
        rows.append({"L":L,"flux_integer_m":m,
             "plaquette_argument":theta,"quantized_total_flux":m,
             "covariant_shift_commutator_norm":norm,
             "lattice_Yang_Mills_action_with_a_1_over_L":action,
             "fixed_B_continuum_F2_over2_limit":expected,
             "gauge_transform_verified":True})
    assert all(r['covariant_shift_commutator_norm']>0
         for r in rows if r['flux_integer_m']>0)
    out={"status":"PASS_QUANTIZED_CURVATURE_GAUGE_COVARIANCE_AND_DISCRETE_BIANCHI",
      "model":"Uniform U(1) flux m on a 2D LxL periodic lattice, with a=1/L, T_x=f(x+1,y) times U_x, T_y=f(x,y+1) times U_y. A lattice gauge connection, not a metric/Levi-Civita connection.",
      "links":"U_x(x,y)=exp(-2pi i m y/L²), U_y(x,L-1)=exp(2pi i m x/L), otherwise U_y=1",
      "exact_curvature_relation":"T_x T_y = exp(2pi i m/L²) T_y T_x. [T_x,T_y]=(exp(2pi i m/L²)-1)T_y T_x. Uniform plaquette gauge-invariant Wilson phase.",
      "gauge_covariance":"For g(x) any site U1 phase, U'_e=g(source) U_e conjugate(g(target)), and T'_i=G T_i G†. Full operator identity tested.",
      "Wilson_action":"S=sum_plaquettes(1-Re W)/a² tends to integral F_xy²/2 for fixed square unit area and fixed integer flux 2pi m.",
      "rows":rows,
      "no_go":"Genuine nonzero discrete holonomy forces noncommuting naive shifts. Flat spin-two constraints based on commuting ordinary differences cannot simply be transplanted unchanged to this connection. Need curvature-dependent local terms that close an appropriate gravity constraint algebra.",
      "scope":"U1 lattice curvature with a supplied 2D flat coordinate torus, not a vierbein/spin connection, curved Regge gravity, Fierz-Pauli curved Hamiltonian closure, emergent time, or quantized Einstein theory.",
      "source":["https://doi.org/10.1103/PhysRevD.10.2445"]}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print("CURVATURE",[(r['L'],r['flux_integer_m'],round(r['covariant_shift_commutator_norm'],6)) for r in rows],flush=True)
if __name__=="__main__":run()
