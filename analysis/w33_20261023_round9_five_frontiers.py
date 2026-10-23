#!/usr/bin/env python3
"""Five further W33 frontiers: GF16, transverse chirality, budget search,
heralded-magic fault linear response, and native-metric gauge Ward.
"""
from __future__ import annotations
from pathlib import Path
from itertools import combinations
import json, math
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

try:
 from analysis.w33_20261023_gf16_first_order_obstruction import construct as gf2_case
 from analysis.w33_20261022_five_followups_round5 import A
 from analysis.w33_pass12189_12193_five_bridges import graph_inputs
except ImportError:
 from w33_20261023_gf16_first_order_obstruction import construct as gf2_case
 from w33_20261022_five_followups_round5 import A
 from w33_pass12189_12193_five_bridges import graph_inputs

ROOT=Path(__file__).resolve().parents[1]

def gf16_extension():
    old=json.loads((ROOT/"data/PART_20261023_GF16_FIRST_ORDER_OBSTRUCTION.json").read_text())
    cases=old["cases"]
    for t,r in enumerate(cases,2):
        q=2**t;n=(q+1)*(q*q+1)
        assert r["q"]==q and r["n"]==n
        assert r["dimC"]==q*q and r["rankDC"]==q*(q-1)//2
        assert r["rankDK"]==q**3//2-q*(q-1)//2
        assert r["rank_DK_intersection_C"]==r["rankDC"]
        assert r["rank_delta1"]==0
    return {"status":"GF2_GROWING_EXTENSION_CENSUS_Q4_Q8_Q16",
        "cases":cases,
        "splitting":"For modules over F2[T]/(T+1)^2, delta1=0 implies the exact module extension 0->C->K->Q->0 splits: the only nonprojective indecomposable is J1 and extensions of J1 by J1 are measured by delta1.",
        "general_q_proof":False,
        "scope":"GF16 4369-dimensional exact computation; splitting as cyclic transvection F2[C2]-modules, NOT splitting as full Sp4(q) modules."}


def induced_vertices(n):
    visited=[0]; i=0
    while len(visited)<n:
        node=visited[i];i+=1
        for j in np.flatnonzero(A[node]):
            j=int(j)
            if j not in visited:visited.append(j)
            if len(visited)>=n:break
    return visited


def tfim_spectrum(n,h,bias=0.):
    vertices=induced_vertices(n)
    edges=[(i,j) for i,j in combinations(range(n),2) if A[vertices[i],vertices[j]]]
    aa=9/32; m=1<<n
    indexes=np.arange(m,dtype=np.int64)
    bits=((indexes[:,None]>>np.arange(n))&1)
    signs=1-2*bits
    diagonal=np.zeros(m,dtype=float)
    for i,j in edges:diagonal-=aa*signs[:,i]*signs[:,j]
    diagonal-=bias*signs.sum(axis=1)
    rows=np.tile(indexes,n); cols=np.concatenate([indexes^(1<<i) for i in range(n)])
    val=np.full(n*m,-h)
    H=sparse.diags(diagonal,format="csr")+sparse.csr_matrix((val,(rows,cols)),shape=(m,m))
    if h:
        levels=np.sort(eigsh(H,k=2,which="SA",tol=1e-11,maxiter=15000,return_eigenvectors=False))
    else:
        levels=np.sort(diagonal)[:2]
    return {"n":n,"edges":len(edges),"vertices":vertices,"h":h,"bias":bias,
        "energy0":float(levels[0]),"energy1":float(levels[1]),
        "gap":float(levels[1]-levels[0]),"graph_degree_max":int(max(sum(i in e for e in edges) for i in range(n)))}


def chiral_dynamics():
    # Physical local 9-dimensional Hilbert-space construction exists in round8;
    # the encoded 2-state sector yields the transverse field Ising Hamiltonian.
    # Designed h sum X is real and antiunitary-symmetric under K=X^tensor n K0.
    rows=[]
    for n in (2,4,6,8):
        for h in (0.,.1,.2):
            rows.append(tfim_spectrum(n,h))
    assert all(x["gap"]>=-1e-10 for x in rows)
    assert all(x["gap"]<1e-9 for x in rows if x["h"]==0)
    assert all(x["gap"]>0 for x in rows if x["h"]>0)
    # Two-spin chain exact levels -sqrt(J²+4h²) and -J,
    # hence tunnel gap sqrt(J²+4h²)-J.
    for h in (.1,.2):
        d=next(x for x in rows if x["n"]==2 and x["h"]==h)
        assert abs(d["gap"]-(math.sqrt((9/32)**2+4*h*h)-9/32))<1e-9
    checks=[]
    for n in (4,6,8):
        pos=tfim_spectrum(n,.1,.001)
        neg=tfim_spectrum(n,.1,-.001)
        assert abs(pos["energy0"]-neg["energy0"])<1e-9
        checks.append({"n":n,"h":.1,"bias_plus_energy":pos["energy0"],
                       "bias_minus_energy":neg["energy0"],
                       "even_energy_under_K":True})
    return {"status":"EXACT_SMALL_GRAPH_K_EVEN_CHIRAL_TUNNELING",
        "H":"H=-9/32 sum_W33edges ZiZj - h sum_i Xi - epsilon sum_i Zi in a selected parity-ground two-level onsite sector",
        "source_free_h":True,
        "K":"K=(tensor_i Xi) complex conjugation, at epsilon=0 KHK^-1=H",
        "finite_N_uniqueness":"At h>0 a real irreducible stoquastic transverse-Ising Hamiltonian has a unique strictly positive ground eigenvector; source-free chiral expectation vanishes.",
        "spectral_rows":rows,
        "bias_symmetry_checks":checks,
        "caveat":"The two-state sector is selected/engineered and the induced n<=8 W33 subgraphs are not a thermodynamic graph sequence. K need not be physical time reversal, and no time arrow follows."}


def heralded_fault_pipeline():
    native=json.loads((ROOT/"data/w33_pass12189_12193_five_bridges.json").read_text())["magic"]
    samples=native["single_Z_after_gate_controls"]; n=len(samples)
    S0=29/81
    assert n==40
    S=np.array([x["success"] for x in samples],float)
    F=np.array([x["fidelity_to_ideal"] if x["fidelity_to_ideal"] is not None else 1 for x in samples],float)
    assert np.all((S>=0)&(S<=1))
    dsuccess=float(np.sum(S)-40*S0)
    dcond=float(-np.sum(S*(1-F))/S0)
    assert dcond<0
    # For mutually exclusive single-site faults with probability epsilon
    # each, plus ideal no-fault event 1-40 epsilon, this is an exact
    # first-order single-Z error derivative at epsilon=0.
    rows=[]
    for p in (0.,1e-4,1e-3,1e-2):
        if p==0: yield_rate=S0;fidelity=1.
        else:
            denominator=(1-n*p)*S0+p*S.sum()
            numerator=(1-n*p)*S0+p*np.sum(S*F)
            yield_rate=float(denominator);fidelity=float(numerator/denominator)
        rows.append({"single_Z_per_site_fault_probability":p,
                     "single_fault_truncated_success_probability":yield_rate,
                     "single_fault_truncated_conditional_fidelity":fidelity})
    assert abs(rows[0]["single_fault_truncated_success_probability"]-S0)<1e-12
    accepted=[{"site":x["site"],"success":x["success"],
               "fidelity":x["fidelity_to_ideal"]} for x in samples if x["success"]>1e-10]
    return {"status":"W33_HERALDED_MAGIC_FIRST_ORDER_FAULT_SENSITIVITY",
        "input":"Pass12189 precomputed and independently frozen all-40 single-Z histograms",
        "ideal_postselection_success":S0,
        "number_accepted_fault_sites":len(accepted),
        "accepted_fault_sites":accepted,
        "dSuccess_dp_at_p0":dsuccess,
        "dConditionalFidelity_dp_at_p0":dcond,
        "noise_controls":rows,
        "scope":"A true single-fault *first-order* response model. p=0.01 truncation omits >=2 simultaneous faults and should not be treated as physical channel prediction. Does not distill, provide logical decoder or threshold."}


def native_gauge_wave():
    data,b,V,G,aa,bb=graph_inputs()
    G=np.array(G,dtype=float)
    rho=math.sqrt(float(np.linalg.det(G)))
    metric=G/rho
    assert np.allclose(G,G.T) and np.min(np.linalg.eigvalsh(G))>0
    root=np.linalg.cholesky(metric).T
    rows=[]
    m=np.array([1,2,1,0],float)
    ideal=float(m@metric@m)
    for N in (8,16,32,64):
        k=2*np.pi*m/N
        p=np.exp(1j*k)-1
        d0=root@p
        d1=np.zeros((6,4),complex)
        for idx,(a,c) in enumerate(combinations(range(4),2)):
            d1[idx,a]=-d0[c];d1[idx,c]=d0[a]
        assert np.allclose(d1@d0,0,atol=1e-12)
        M=d1.conj().T@d1
        assert np.allclose(M@d0,0,atol=1e-11)
        eig=np.linalg.eigvalsh(M)
        s=float(np.vdot(d0,d0).real)
        assert np.allclose(eig,[0,s,s,s],rtol=1e-10,atol=1e-11)
        generic=np.array([.1+.8j,-.7+.4j,.5-.8j,.2+.3j])
        for alpha in (0.,.8+.6j):
            assert np.allclose(d1@(generic+alpha*d0),d1@generic,atol=1e-11)
        rows.append({"N":N,"discrete_gauge_eigenvalues":[float(x) for x in eig],
                     "scaled_transverse_dispersion":s/(2*np.pi/N)**2,
                     "relative_acoustic_metric_error":abs(s/(2*np.pi/N)**2-ideal)/ideal})
    assert all(rows[i+1]["relative_acoustic_metric_error"]<rows[i]["relative_acoustic_metric_error"] for i in range(3))
    return {"status":"NATIVE_METRIC_FOUR_DIMENSIONAL_GAUGE_WARD_TEMPLATE",
        "source":"Pass12192 native 27-site / 135-edge periodic voltage cover, actual acoustic metric G, not bare W33 40-point carrier",
        "native_G":G.tolist(),"rho":rho,"metric_G_over_rho":metric.tolist(),
        "d0":"sqrt(G/rho) (exp(ik)-1)",
        "d1":"antisymmetric discrete wedge with rows -d0_nu at mu, +d0_mu at nu",
        "exact_Ward":"d1 d0=0 and M=d1^dag d1 has M d0=0",
        "Maxwell_symbol":"eigenvalues [0,s,s,s], s=d0^dag d0",
        "continuum_symbol":"lim_{N->infinity} N² s/(2pi)² = m^T G/rho m for k=(2pi/N)m",
        "rows":rows,
        "scope":"A gauge-invariant FOUR-DIMENSIONAL EUCLIDEAN coarse-grained cochain template with native G; this is not a derived microscopic gauge field, not a Lorentzian action, and its 3 off-gauge modes are not yet two physical photon helicities. No gravity or dynamics of G established."}


def run():
    return {"schema":"w33.toe.round9.20261023.v1",
       "gf16":gf16_extension(),
       "chirality":chiral_dynamics(),
       "routing":json.loads((ROOT/"data/PART_20261023_SWAPCOUNT_28_SEARCH.json").read_text()),
       "magic":heralded_fault_pipeline(),
       "gauge":native_gauge_wave()}


if __name__=="__main__":
    import sys
    raw=json.dumps(run(),indent=2)+"\n"
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(raw,encoding="utf-8")
    else:print(raw)
