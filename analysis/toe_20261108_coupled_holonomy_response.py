"""Four native holonomies: static Hessian and a declared one-loop response kernel.

Continuous-time free complex scalar, temporal gauge, harmonic link profiles.
Tree electric inertia plus exact scalar Gaussian bubble, not complete gauge QFT.
Prior scalar action/full27bands: toe_20261108_native_scalar_wilson.py.
"""
from __future__ import annotations
import argparse
import hashlib
from itertools import combinations_with_replacement,product
import json
import math
from pathlib import Path
import sys
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261108_native_scalar_wilson as prior
PAIRS=list(combinations_with_replacement(range(4),2))


def momenta(sizes,theta=None):
    sizes=np.array(sizes)
    return (2*np.pi*np.array(list(product(*(range(int(n)) for n in sizes))),float)
            +(np.zeros(4) if theta is None else np.array(theta)))/sizes


def energy(sizes,mass,theta):
    points=momenta(sizes,theta);total=0.
    for start in range(0,len(points),256):
        H=prior.matrices(points[start:start+256])[0]
        total+=float(np.sqrt(np.maximum(np.linalg.eigvalsh(H),0)+mass**2).sum())
    return total/np.prod(sizes[:3])


def electric_metric(sizes,g=1.):
    d=np.diag(1/np.array(sizes,float))
    return float(sizes[3])/g**2*d@prior.geometry()[-1]@d


def expanded(packed):
    out=np.zeros((4,4))
    for (i,j),v in zip(PAIRS,packed):out[i,j]=out[j,i]=v
    return out


class ScalarResponse:
    def __init__(self,sizes=(3,3,3,2),mass=.8,profile_mode="harmonic"):
        self.sizes=tuple(sizes);self.mass=mass
        _,V,a,b,h,_=prior.geometry()
        # Time-dependent spatial connection is h*theta/sizes in temporal gauge.
        # Replacing h by V dynamically without transformed A0 changes the model.
        assert profile_mode in ("harmonic","tree_without_induced_A0")
        profiles=(h if profile_mode=="harmonic" else V)/np.array(sizes)
        volume=np.prod(sizes[:3]);points=momenta(sizes)
        contact=np.zeros(10);frequencies=[];grams=[]
        for start in range(0,len(points),128):
            k=points[start:start+128];z=np.exp(1j*k@V.T)
            H=prior.matrices(k)[0];vals,U=np.linalg.eigh(H)
            w=np.sqrt(np.maximum(vals,0)+mass**2);Uh=U.conj().transpose(0,2,1)
            R=(U/(2*w[:,None,:]))@Uh
            edge_density=(z*R[:,b,a]).real
            for t,(i,j) in enumerate(PAIRS):
                contact[t]+=2*np.sum(edge_density*profiles[:,i]*profiles[:,j])
            X=[]
            for i in range(4):
                J=np.zeros_like(H)
                J[:,a,b]=-1j*z*profiles[:,i];J[:,b,a]=1j*z.conj()*profiles[:,i]
                X.append(Uh@J@U)
            p=w[:,:,None]+w[:,None,:]
            norm=2*w[:,:,None]*w[:,None,:]
            grams.append(np.array([((X[i]*X[j].conj()).real/norm).ravel()
                                   for i,j in PAIRS])/volume)
            frequencies.append(p.ravel())
        self.contact=expanded(contact/volume)
        self.p=np.concatenate(frequencies)
        self.gram=np.concatenate(grams,axis=1)
        self.K=self.contact-self.bubble(0.)
        self.K=(self.K+self.K.T)/2
        assert np.linalg.eigvalsh(self.K).min()>0
        self.moments=[expanded(self.gram@(self.p**(-3-2*r))) for r in range(3)]

    def bubble(self,nu):
        return expanded(self.gram@(self.p/(self.p**2+nu**2)))

    def pi(self,nu):
        return self.contact-self.bubble(nu)

    def Z(self,s=0.):
        assert s<(2*self.mass)**2
        return expanded(self.gram@(1/(self.p*(self.p**2-s))))

    def F(self,s,g):
        return self.K-s*(electric_metric(self.sizes,g)+self.Z(s))

    def Fmoment(self,s,g):
        Z=sum(s**r*z for r,z in enumerate(self.moments))
        return self.K-s*(electric_metric(self.sizes,g)+Z)

    def kinetic_at_root(self,s,g):
        return electric_metric(self.sizes,g)+expanded(self.gram@(self.p/(self.p**2-s)**2))

    def modes(self,g=.1):
        G=electric_metric(self.sizes,g)
        static,vec=eigh(self.K,G)
        inverse44=np.linalg.inv(G)[3,3]
        weights=vec[3]**2/inverse44
        upper=.5*(2*self.mass)**2
        assert np.linalg.eigvalsh(self.F(upper,g)).max()<0
        roots=sorted(brentq(lambda s,i=i:np.linalg.eigvalsh(self.Fmoment(s,g))[i],
                           0.,upper,xtol=1e-16,rtol=1e-12) for i in range(4))
        groups=[]
        for s in roots:
            if groups and abs(s-groups[-1]["s"])<max(1e-12,1e-7*s):
                groups[-1]["multiplicity"]+=1;continue
            groups.append(dict(s=float(s),multiplicity=1))
        for row in groups:
            s=row["s"];ev,U=eigh(self.F(s,g))
            chosen=np.argsort(abs(ev))[:row["multiplicity"]];W=U[:,chosen]
            C=W.T@self.kinetic_at_root(s,g)@W
            residue=W@np.linalg.solve(C,W.T)
            row["theta4_residue"]=float(residue[3,3])
            row["theta4_residue_over_tree_sum_rule"]=float(residue[3,3]/inverse44)
            row["null_residual"]=float(np.linalg.norm(self.F(s,g)@W))
            ratio=s/(2*self.mass)**2
            row["resolvent_remainder_operator_bound"]=float(s*ratio**3/(1-ratio)*np.linalg.norm(self.moments[0],2))
            row["exact_kernel_residual_mass_squared_error_bound"]=float(row["null_residual"]/np.linalg.eigvalsh(G).min())
            assert row["null_residual"]<1e-10
        return dict(g=g,static_tree_inertia_squared_frequencies=static.tolist(),
            static_theta4_weights=weights.tolist(),
            static_theta4_weights_scope="Individual weights depend on basis inside a degenerate eigenspace; summed degenerate weights are invariant.",
            static_theta4_weighted_squared_frequency=float(weights@static),
            old_single_coordinate_curvature_diagnostic=float(self.K[3,3]*inverse44),
            dynamic_subthreshold_groups=groups,
            subthreshold_mode_count=sum(x["multiplicity"] for x in groups),
            theta4_subthreshold_residue_fraction=sum(x["theta4_residue_over_tree_sum_rule"] for x in groups),
            pair_threshold_squared_conservative=(2*self.mass)**2,
            fractional_dynamic_shift_vs_static=[float(x/y-1) for x,y in zip(roots,static)],
            model_scope="Poles of the explicitly retained tree-electric plus scalar-one-loop homogeneous quadratic kernel. Not complete gauge-QFT poles: higher gauge loops, local A0/inhomogeneous gauge response, radius and charged inventories remain unbuilt. Finite lattice units.")


def primitive_paths():
    from w33_20261027_native_bloch_face_module import deck_loops
    _,V,a,b,_,_=prior.geometry()
    loops,W,_=deck_loops(list(zip(a,b)),V)
    coeff=sp.Matrix(W).T.inv()
    out=[]
    for axis in range(4):
        walk=[]
        for c,segment in zip(coeff[:,axis],loops):
            assert c.q==1
            segment=segment if c>=0 else [(e,-s) for e,s in segment[::-1]]
            walk+=segment*abs(int(c))
        vertex=0;position=np.zeros(4,int)
        for e,s in walk:
            assert vertex==(a[e] if s==1 else b[e])
            vertex=b[e] if s==1 else a[e];position+=s*V[e]
        assert vertex==0 and position.tolist()==np.eye(4,dtype=int)[axis].tolist()
        out.append(dict(axis=axis,steps=len(walk),period=position.tolist(),
                        signed_edges=[[int(e),int(s)] for e,s in walk]))
    return out


def summary(sizes,mass):
    x=ScalarResponse(sizes,mass)
    G=electric_metric(sizes);v,e=eigh(x.K,G)
    lower=[]
    for p,n in zip(primitive_paths(),sizes):
        r=p["steps"]*n
        lower.append((math.log(sizes[3])-.5*math.log(math.pi)+math.lgamma(r-.5)
                      -math.lgamma(r+1)-(r-.5)*math.log(10+mass**2))/math.log(10))
    return dict(sizes=list(sizes),mass=mass,static_Hessian=x.K.tolist(),
        tree_electric_metric_g1=G.tolist(),loop_kinetic_Z0=x.Z().tolist(),
        loop_kinetic_min_eigenvalue=float(np.linalg.eigvalsh(x.Z()).min()),
        static_squared_frequencies_over_g2=v.tolist(),
        theta4_static_weights=(e[3]**2/np.linalg.inv(G)[3,3]).tolist(),
        exact_positive_Hessian_bound="K >= diag(c_i)>0, c_i = L Gamma(r_i-1/2)/(sqrt(pi) r_i! (10+m²)^(r_i-1/2)), r_i=sizes_i*primitive_path_steps_i. Omitted winding outer products are PSD.",
        numeric_log10_diagonal_lower_bound=lower,
        modes=[x.modes(g) for g in (.1,.5)],
        contact_minus_bubble_static_cancellation=float(np.linalg.norm(x.K)/np.linalg.norm(x.contact)))


def produce():
    rows=[summary((n,n,n,2),.8) for n in (2,3,4,6,8)]
    paths=["analysis/toe_20261108_native_scalar_wilson.py",
           "data/w33_pass11991_native_four_period_cover.json",
           "analysis/w33_pass12189_12193_five_bridges.py",
           str(Path(__file__).relative_to(ROOT))]
    return dict(status="DECLARED_NATIVE_FOUR_HOLONOMY_SCALAR_ONELOOP_DYNAMIC_KERNEL_NOT_TOE",
        primitive_winding_paths=primitive_paths(),rows=rows,
        kernel="Pi(nu)=D-sum_ab C_ab*(omega_a+omega_b)/[(omega_a+omega_b)^2+nu^2], C_ijab=Re(X_iab conj(X_jab))/(2omega_a omega_b), X_i=Udag H_i U.",
        analytic_continuation="F(s)=K-s[Gtree+Z(s)], Z(s)=sum C/[p(p²-s)], p=omega_a+omega_b. For s<4m² each matrix coefficient is a positive Gram matrix. F'(s)=-Gtree-sum C*p/(p²-s)^2 <0.",
        root_algorithm="Root search uses Z0+sZ1+s²Z2 with Zr=sum C/p^(3+2r). For r=s/(4m²)<1 the omitted PSD matrix is bounded above by r³/(1-r)*Z0. Each candidate null vector/residue is checked against the unexpanded kernel. Formula bounds analytic truncation, not floating roundoff.",
        bath="Equivalent Schur kernel of a positive oscillator bath with squared frequencies p², coupling WW^T=C*p and contact D. K=D-sum C/p>0 plus Gtree>0 gives positive full quadratic Hamiltonian. This is an algebraic spectral representation of the retained one-loop kernel, not new microscopic matter.",
        strict_stability="Full winding potential is sum c_w(1-cos(w.Theta)), c_w>=0. Four literal primitive-axis paths make its global minimum unique modulo2pi in every coordinate and give positive diagonal lower bound on K.",
        dynamic_gauge="Time-dependent backgrounds use rational harmonic profiles h, temporal A0=0. Integer-tree-gauge profiles V have the same static Hessian but different frequency response unless the induced temporal vertex is included.",
        fermion_audit="Pass11991 owns a108D Euclidean GW/overlap kernel. Its finite Euclidean eigenvalues are not assigned physical continuous-time energies here. A compatible Hamiltonian/transfer construction, full charged spectrum and parity/anomaly treatment are needed before using a fermion vacuum loop. Older TOE57 spinless thermal fermions are also a distinct model.",
        scope="External torus sizes, mass, gauge coupling and continuous time. Exact free-scalar Gaussian contribution at fixed background plus tree electric term, restricted homogeneous harmonic sector. Not full dynamical gauge theory, stabilized compactification, physical particle mass, complete perturbative pole order, SM/gravity or TOE.",
        input_raw_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",default="data/toe_20261108_coupled_holonomy_response.json")
    a=p.parse_args();d=produce()
    (ROOT/a.out).write_text(json.dumps(d,indent=2)+"\n",encoding="utf-8")
    print(json.dumps([dict(sizes=r["sizes"],static=r["static_squared_frequencies_over_g2"],theta4weights=r["theta4_static_weights"],dynamic=r["modes"][1]["fractional_dynamic_shift_vs_static"]) for r in d["rows"]]))
