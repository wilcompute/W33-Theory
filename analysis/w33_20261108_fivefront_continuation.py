#!/usr/bin/env python3
"""Five independent W33 fronts: harmonic selector, E6/NB, higher-q, provenance, optics."""
from __future__ import annotations
import argparse, itertools, json, math, re, subprocess
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
OMEGA=np.exp(2j*np.pi/3)
V=list(itertools.product(range(3),repeat=3))
VID={x:i for i,x in enumerate(V)}
DIRS=[(1,0,0),(0,0,1),(1,1,1),(1,2,1)]
def n0(k):return sum(sum(a*b for a,b in zip(k,v))%3==0 for v in DIRS)
def q3(v):a,b,c=v;return (a*c-b*b)%3

def gauge():
    census=Counter()
    for k in V:
        h=4-(0 if k==(0,0,0) else 1)-n0(k)
        assert h>=0
        census[(n0(k),h)]+=1
    assert census==Counter({(4,0):1,(1,2):8,(2,1):12,(0,3):6})
    # GL2(3)/{+-I}=S4 on Sym2 and its dual characters.
    basis=[np.array([[1,0],[0,0]]),np.array([[0,1],[1,0]]),np.array([[0,0],[0,1]])]
    actions={}
    for t in itertools.product(range(3),repeat=4):
        G=np.array(t).reshape(2,2)
        if round(np.linalg.det(G))%3==0:continue
        key=min(t,tuple((-G%3).flatten()))
        M=np.array([[int((G@E@G.T)[i,j])%3 for E in basis] for i,j in [(0,0),(0,1),(1,1)]])
        actions[key]=np.array(s.Matrix(M.tolist()).inv_mod(3)).astype(int).T%3
    assert len(actions)==24
    todo=set(V);orbits=[]
    while todo:
        k=min(todo)
        orbit={tuple((M@np.array(k))%3) for M in actions.values()}
        assert orbit<=todo
        h=4-(0 if k==(0,0,0) else 1)-n0(k)
        orbits.append(dict(rep=list(k),size=len(orbit),harmonic_per_character=h,dim=len(orbit)*h))
        todo-=orbit
    assert sorted((o["size"],o["harmonic_per_character"]) for o in orbits)==[(1,0),(4,2),(4,2),(6,3),(12,1)]
    assert sum(o["dim"] for o in orbits)==46
    return dict(status="EXACT_FOURIER_CHARACTER_DECOMPOSITION",H1=46,
       translation_invariants=0,character_census={str(k):v for k,v in sorted(census.items())},
       S4_orbits=sorted(orbits,key=lambda x:(x["size"],x["rep"])),
       proof="For each momentum k, four edge directions; face rank n0(k), vertex rank 1 except k=0; at k=0 all four face directions are boundaries.",
       caveat="No translation-fixed harmonic mode; a photon identification needs additional physical selection and kinetic normalization.")

def flavor(root):
    p=root/"data/w33_20261001_dflat_cartan_mass_loop.json"
    native=None
    if p.is_file():
        c=json.loads(p.read_text(encoding="utf8"))
        native={"mass_rank":c["dimension_five_light_mass"]["rank_before_after"],
          "mass_kernel":c["mass_interface"]["kernel_dimension"],
          "source":"data/w33_20261001_dflat_cartan_mass_loop.json"}
        assert native["mass_rank"]==[78,79] and native["mass_kernel"]==3
    w=(-1+s.I*s.sqrt(3))/2
    Y=s.diag(1,2,4)+s.Matrix([[0,1,1],[1,0,1],[1,1,0]])/3
    B=s.Matrix([[1,w,-1]])
    M=Y.row_join(s.zeros(3,1)).col_join(B.row_join(s.Matrix([[5]])))
    delta=s.zeros(4,4);delta[0,3]=1
    eps=s.symbols("eps",real=True)
    d=s.factor((M+eps*delta).det())
    slope=s.simplify(s.im(s.trace(M.inv()*delta)))
    assert M.det()==s.Rational(985,27)
    assert slope==33*s.sqrt(3)/1970
    return dict(status="CONDITIONAL_FIRST_ORDER_STRONG_CP_SENSITIVITY",
      E6_original=native,rank_obstruction="81x81 E6 skew map has rank 78; the stated dim-5 update reaches 79 and still leaves two exact zeros. The full determinant vanishes, so its complex argument cannot be identified with the toy 4x4 determinant.",
      toy_det="985/27",toy_det_after_perturbation=str(d),
      perturbation="one REAL upper-right entry deltaM[0,3]=eps",
      derivative_im_trace_Minv_delta=str(slope),derivative=float(s.N(slope)),
      eps_bound_if_imposed_theta_lt_1e_minus10=float(1e-10/slope),
      caveat="Hypothetical insertion, not a derived one-loop diagram; symmetry and native E6 embedding still missing.")

def higher_q():
    rows=[]
    for q in [3,5,7,11]:
        x=np.indices((q,q,q))
        form=(x[0]*x[2]-x[1]**2)%q
        kernel=(form==0).astype(float);kernel[0,0,0]=0
        spectrum=np.rint(np.fft.fftn(kernel).real).astype(int)
        val={int(a):int(b) for a,b in zip(*np.unique(spectrum,return_counts=True))}
        assert set(val)=={q*q-1,-1,q-1,-q-1}
        projectors={eig:np.rint(np.fft.ifftn((spectrum==eig).astype(float)).real*q**3).astype(int)
                    for eig in val}
        good=[]
        for d in range(1,q):
            coeff=[sorted(set(int(z) for z in projectors[eig][form==d]))
                   for eig in [q*q-1,-1,q-1,-q-1]]
            if coeff==[[1],[q-1],[-q],[0]]:good.append(d)
        assert len(good)==(q-1)//2
        rows.append(dict(q=q,vertices=q**3,spectrum=val,anisotropic_good_values=good,
              certified_character_coefficients=[1,q-1,-q,0],
              uniform_amplitude_required=q**(-1.5),
              all_time_amplitude_bound=2/q**2,strictly_excluded=q>=5))
    return dict(status="ALL_TIME_NO_GO_ODD_PRIME_POWER_Q_GE_5_UNWEIGHTED",
      theorem="For an anisotropic difference in one class, U_t(0,d)=q^-3[1+(q-1)e^(-iq^2 t)-q e^(-i(q^2-q)t)]. Thus |U|<=2/q^2<q^-3/2 for q>4, ruling out exact instantaneous uniform mixing at every time.",
      field_character_lemma="Finite quadratic Gauss sums give the spectral values q^2-1,-1,q-1,-q-1 and a non-null shell with Fourier coefficient q-1 on the dual null sector. Orthogonality and A(d)=0 yield remaining projector coefficients -q,0.",
      checked_primes=rows,
      boundary="Unweighted affine null graph only; weighted Hamiltonians and different towers remain open.")

def provenance(root):
    patterns=[r"137\s*\+\s*1\s*/\s*28",r"137\s*\+\s*880\s*/\s*24445",
              r"3\s*/\s*13\s*\+\s*1\s*/\s*2200",r"1\s*/\s*600",r"Weber",r"Nelson.?Barr"]
    paths=["analysis/2026-11-07_natural_constants_derivation_catalog.md",
           "papers/standalone/toe_constants_companion.tex","docs/index.html",
           "papers/forty_points/sec09_physics.tex"]
    evidence=[]
    for path in paths:
        f=root/path
        if not f.is_file():continue
        for i,line in enumerate(f.read_text(encoding="utf8",errors="replace").splitlines(),1):
            hits=[p for p in patterns if re.search(p,line,re.I)]
            if hits:evidence.append(dict(path=path,line=i,matches=hits,text=line.strip()[:230]))
    # A frozen source location is NOT the earliest derivation. Current line attribution
    # can be requested with git blame as a separate optional, bounded process.
    return dict(status="SCOPED_SOURCE_LINE_EVIDENCE_NO_FALSE_HISTORICAL_PRIORITY",
       selected_sources=paths,source_line_hits=evidence[:90],
       matching_line_count=len(evidence),formulas=patterns,
       caveat="No claim that current line or first current source is the earliest commit or an independent physical proof. Full historical rename-aware git log and semantic scheme matching remain outstanding.")

def optics():
    def h(t):return np.array([[OMEGA**(t*(i-j)**2%3)/np.sqrt(3) for j in range(3)] for i in range(3)])
    P=np.zeros((27,27),complex)
    for a,b,c in V:
        d=(c+2*a)%3
        e=(a+2*d)%3
        P[VID[(e,b,d)],VID[(a,b,c)]]=1
    H=np.kron(np.kron(h(1),h(-1)),h(-1))
    U=OMEGA*np.exp(-1j*np.pi/6)*P.T@H@P
    target=np.array([[np.exp(-1j*np.pi/6)*OMEGA**((1+q3(tuple((a[i]-b[i])%3 for i in range(3))))%3)/np.sqrt(27)
                     for b in V] for a in V])
    residual=float(np.max(abs(U-target)))
    assert residual<1e-12
    r=np.eye(3);theta=.08
    r[0,0]=r[1,1]=np.cos(theta);r[0,1]=np.sin(theta);r[1,0]=-np.sin(theta)
    bad=OMEGA*np.exp(-1j*np.pi/6)*P.T@np.kron(np.kron(r@h(1),h(-1)),h(-1))@P
    wrong_t=np.indices((3,3,3));q=(wrong_t[0]*wrong_t[2]-wrong_t[1]**2)%3
    null=(q==0).astype(float);null[0,0,0]=0
    drift=np.fft.ifftn(np.exp(-1j*(2*np.pi/9+.03)*(8-np.fft.fftn(null).real)))
    return dict(status="EXACT_27_MODE_CLIFFORD_COMPILATION_WITH_SYNTHETIC_FALSIFIERS",
      circuit="c<-c+2a; a<-a+2c; H+ on a, H- on b,c; undo two SUMs; global phase",
      forward_SUM=2,inverse_SUM=2,tritters_3x3=27,
      two_mode_MZI_upper_bound=81,generic_27_mode_bound=351,
      nonClifford_count=0,full_matrix_residual=residual,
      tritter_error_rad=theta,bad_tritter_max_probability_deviation=float(np.max(abs(abs(bad)**2-1/27))),
      tick_drift_rad=.03,tick_drift_max_probability_deviation=float(np.max(abs(abs(drift)**2-1/27))),
      caveat="27 rails represent 3 qutrit degrees of freedom; no calibrated optical chip, loss/error budget, or measurement exists. A Clifford circuit within ordinary quantum mechanics makes identical predictions.")

def produce(root):
    return dict(schema="w33.20261108.fivefront_continuation.v1",date="2026-11-08",
       gauge=gauge(),flavor=flavor(root),higher_q=higher_q(),provenance=provenance(root),optics=optics(),
       scope="Exact mathematical claims and conditional modeling only; not a demonstrated TOE.")
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--root",type=Path,default=ROOT)
    ap.add_argument("--out",type=Path,default=Path("data/w33_20261108_fivefront_continuation.json"))
    args=ap.parse_args();obj=produce(args.root)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({"H1":obj["gauge"]["H1"],"q_excluded":[v["q"] for v in obj["higher_q"]["checked_primes"] if v["strictly_excluded"]],"NB_slope":obj["flavor"]["derivative_im_trace_Minv_delta"],"optics_residual":obj["optics"]["full_matrix_residual"],"provenance_lines":obj["provenance"]["matching_line_count"]}))
if __name__=="__main__":main()
