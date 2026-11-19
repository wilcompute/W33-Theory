#!/usr/bin/env python3
"""Five TOE challenges + two independent cross-sector gates, 2026-11-19.
CONDITIONAL physics checks on supplied flat lattice/metric/gauge data.
No fundamental TOE, chiral SM derivation, quantum gravity or Born rule.
"""
from __future__ import annotations
import copy, json, math, sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261119_causal_spinc_overlap_anomaly_quantum_gravity.json"
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261105_causal_growth_without_background import sample as causal_sample
I2=np.eye(2,dtype=complex)
SX=np.array([[0,1],[1,0]],complex)
SY=np.array([[0,-1j],[1j,0]],complex)
SZ=np.diag([1,-1]).astype(complex)
GAM=(SX,SY)
PI=np.pi


def rank2(B):
    a=(np.asarray(B,dtype=np.uint8)%2).copy()
    r=0
    for c in range(a.shape[1]):
        inds=np.flatnonzero(a[r:,c])
        if not len(inds):continue
        k=r+int(inds[0])
        if k!=r:a[[r,k]]=a[[k,r]]
        for j in range(r+1,len(a)):
            if a[j,c]:a[j]^=a[r]
        r+=1
        if r==len(a):break
    return r


def torus_cell_spin_gate(L=3):
    """Cubical cell homology, NOT a spin structure on a bare causal poset."""
    V=L*L;E=2*V;F=V
    vid=lambda x,y:(x%L)*L+(y%L)
    hor=lambda x,y:vid(x,y)
    ver=lambda x,y:V+vid(x,y)
    D1=np.zeros((V,E),dtype=np.uint8)
    D2=np.zeros((E,F),dtype=np.uint8)
    for x in range(L):
        for y in range(L):
            D1[vid(x,y),hor(x,y)]=1
            D1[vid(x+1,y),hor(x,y)]=1
            D1[vid(x,y),ver(x,y)]=1
            D1[vid(x,y+1),ver(x,y)]=1
            f=vid(x,y)
            for e in [hor(x,y),ver(x+1,y),hor(x,y+1),ver(x,y)]:
                D2[e,f]^=1
    exact=(D1@D2)%2
    r1=rank2(D1);r2=rank2(D2)
    betti=[V-r1,E-r1-r2,F-r2]
    assert betti==[1,2,1] and not np.any(exact)
    return {"status":"PASS","cubical_torus_L":L,
        "cell_counts":{"V":V,"E":E,"F":F,"Euler_characteristic":V-E+F},
        "GF2_boundary_ranks":[r1,r2],"GF2_betti_numbers":betti,
        "number_of_H1_Z2_spin_torsor_classes":2**betti[1],
        "boundary_of_boundary_nonzero_entries":int(np.count_nonzero(exact)),
        "caution":"Four spin structures are classified by a Z2 H1 torsor after the oriented smooth torus and base spin structure are given. Bare directed events do not supply a spin lift or orientability."}


def links(L,flux,twist_x=0.,local_phase=None):
    ux=np.empty((L,L),complex);uy=np.ones((L,L),complex)
    for x in range(L):
        for y in range(L):
            ux[x,y]=np.exp(-2j*PI*flux*y/(L*L))
            if y==L-1:uy[x,y]=np.exp(2j*PI*flux*x/L)
            if x==L-1:ux[x,y]*=np.exp(1j*twist_x)
    if local_phase is not None:
        phase=np.exp(1j*np.asarray(local_phase))
        ux=phase*ux*np.conj(np.roll(phase,-1,axis=0))
        uy=phase*uy*np.conj(np.roll(phase,-1,axis=1))
    return ux,uy


def plaquette_phases(ux,uy):
    L=len(ux)
    P=np.empty((L,L),complex)
    for x in range(L):
        for y in range(L):
            P[x,y]=ux[x,y]*uy[(x+1)%L,y]*np.conj(ux[x,(y+1)%L])*np.conj(uy[x,y])
    return P


def wilson_operator(ux,uy):
    L=len(ux);n=2*L*L
    D=np.zeros((n,n),complex)
    for x in range(L):
        for y in range(L):
            j=2*(x*L+y)
            D[j:j+2,j:j+2]+=2*I2
            for dx,dy,gamma,ulink in [(1,0,SX,ux),(0,1,SY,uy)]:
                xp=(x+dx)%L;yp=(y+dy)%L
                xm=(x-dx)%L;ym=(y-dy)%L
                p=2*(xp*L+yp);m=2*(xm*L+ym)
                D[j:j+2,p:p+2] -= .5*(I2-gamma)*ulink[x,y]
                D[j:j+2,m:m+2] -= .5*(I2+gamma)*np.conj(ulink[xm,ym])
    return D


def overlap_operator(ux,uy,m0=1.):
    L=len(ux);DW=wilson_operator(ux,uy);N=2*L*L
    gamma5=np.kron(np.eye(L*L),SZ)
    H=gamma5@(DW-m0*np.eye(N))
    herm=float(np.linalg.norm(H-H.conj().T))
    eig,U=eigh(H,check_finite=True)
    assert herm<1e-12 and np.min(abs(eig))>1e-6
    S=(U*np.sign(eig))@U.conj().T
    D=np.eye(N)+gamma5@S
    GW=float(np.linalg.norm(gamma5@D+D@gamma5-D@gamma5@D))
    index=int(np.rint(-.5*np.sum(np.sign(eig))))
    index_tr=float(np.trace(gamma5@(np.eye(N)-D/2)).real)
    zero_count=int(np.sum(np.linalg.svd(D,compute_uv=False)<1e-8))
    return {"D":D,"GW_residual":GW,"index":index,
            "index_trace":index_tr,"kernel_gap":float(min(abs(eig))),
            "zero_spinor_modes":zero_count,"Hermitian_kernel_residual":herm}


def overlap_topology_gate():
    """2D Euclidean U1 flux sectors inserted manually; known overlap theorem."""
    rows=[]
    for L,q in [(6,0),(6,1),(6,-1),(6,2),(6,-2),(8,3),(8,5)]:
        ux,uy=links(L,q)
        p=plaquette_phases(ux,uy)
        qgeo=int(round(np.sum(np.angle(p))/(2*PI)))
        o=overlap_operator(ux,uy)
        assert qgeo==q and o["index"]==-q
        assert abs(o["index_trace"]-o["index"])<1e-9
        assert o["GW_residual"]<3e-11
        if q!=0:assert o["zero_spinor_modes"]>=abs(q)
        rows.append({"L":L,"inserted_U1_flux_Q":q,
                     "measured_plaquette_winding":qgeo,
                     "overlap_index_in_our_gamma_convention":o["index"],
                     "Ginsparg_Wilson_Frobenius_residual":o["GW_residual"],
                     "H_W_spectral_gap":o["kernel_gap"],
                     "overlap_zero_modes":o["zero_spinor_modes"]})
    L=6
    ux,uy=links(L,1)
    baseline=overlap_operator(ux,uy)
    rng=np.random.default_rng(20261119)
    phase=rng.uniform(-PI,PI,size=(L,L))
    xx,yy=links(L,1,local_phase=phase)
    shifted=overlap_operator(xx,yy)
    Pmat=np.kron(np.diag(np.exp(1j*phase.ravel())),I2)
    covariance=float(np.linalg.norm(shifted["D"]-Pmat@baseline["D"]@Pmat.conj().T))
    assert covariance<1e-10 and shifted["index"]==baseline["index"]
    # A flat global twist can lift zero modes without changing the topological
    # flux; the index still stays 0.
    trivial=overlap_operator(*links(6,0))
    flat_twisted=overlap_operator(*links(6,0,twist_x=PI))
    assert trivial["zero_spinor_modes"]==2 and flat_twisted["zero_spinor_modes"]==0
    return {"status":"PASS","sectors":rows,
        "local_U1_gauge_covariance_error":covariance,
        "flat_periodic_zero_modes":trivial["zero_spinor_modes"],
        "flat_antiperiodic_zero_modes":flat_twisted["zero_spinor_modes"],
        "index_direction":"index=-Q for chosen gamma conventions",
        "meaning":"Exact finite lattice modified chiral symmetry and topological flux-index relation for externally given 2D U1 links.",
        "limits":"Established Neuberger-overlap/GW mechanism on an inserted Euclidean torus and U1 bundle. Does not produce an intrinsic Lorentzian causal-set Dirac operator or SM chiral family."}


def spin_c_anomaly_gate():
    """Representation parity in Spin^c and a 2D chiral anomaly congruence."""
    rows=[]
    for is_spinor in (True,False):
        spin_center=-1 if is_spinor else +1
        for q in range(-4,5):
            descends=(spin_center*((-1)**q)==1)
            rows.append({"spinor":is_spinor,"integer_U1_character_weight":q,
                         "SpinC_quotient_representation_well_defined":descends})
            assert descends==(q%2==(1 if is_spinor else 0))
    # In 1+1 dimensions U1 gauge anomaly cancellation requires
    # sum_L q²=sum_R q². q odd => q² ≡1 mod 8.
    for odd in range(-15,16,2):
        assert odd*odd%8==1
    L=[1,7];R=[5,5]
    anomaly=sum(q*q for q in L)-sum(q*q for q in R)
    assert anomaly==0 and L!=R and (len(L)-len(R))%8==0
    invalid=[1,3,5]
    assert sum(q*q for q in invalid)%8==len(invalid)%8
    return {"status":"PASS","SpinC_quotient":"[Spin(n) x U(1)] / <(-1,-1)>",
        "representation_center_constraints":rows,
        "necessary_2D_anomaly_congruence":
          "For only odd-charged Weyl spinors, sum_L q² - sum_R q²=0 implies N_L-N_R divisible by 8.",
        "odd_square_mod_8":1,"sample_nonvectorlike_2D_chiral_anomaly_free_charges":
           {"left":[1,7],"right":[5,5],"anomaly":anomaly,
            "left_number_minus_right":0},
        "caveats":[
           "These are two-dimensional U1 chiral gauge anomalies, NOT four-dimensional Standard Model anomaly conditions.",
           "The parity restriction applies only when this U1 is the actual Spin^c quotient factor with integral characters and no independent spin/gauge structure.",
           "The sample charges are freely selected to cancel the anomaly; neither their magnitudes nor any family is derived.",
           "Neutral fundamental fermions or fractional SM hypercharges require a different global structure or normalization."]}


def squeezed_quantum_gate():
    """Even purity plus a fixed canonical commutator cannot select a vacuum."""
    J=np.array([[0.,1.],[-1.,0.]])
    out=[]
    for r in (0.,.5,1.):
        V=np.diag([np.exp(2*r),np.exp(-2*r)])/2
        W=V+.5j*J
        ev=np.linalg.eigvalsh(W)
        assert abs(np.linalg.det(V)-.25)<1e-13
        assert min(ev)>-1e-12
        assert np.linalg.norm(W-W.T-1j*J)<1e-13
        out.append({"squeezing_r":r,"min_W_eigenvalue":float(min(ev)),
                    "symplectic_purity_det_V":float(np.linalg.det(V)),
                    "fixed_commutator_error":float(np.linalg.norm(W-W.T-1j*J)),
                    "H_oscillator_frequency_1_energy":float(np.trace(V)/2),
                    "q_variance":float(V[0,0]),"p_variance":float(V[1,1])})
    assert out[0]["H_oscillator_frequency_1_energy"] < out[-1]["H_oscillator_frequency_1_energy"]
    # The ground state changes when one changes the Hamiltonian's frequency.
    omega=4.
    Vw=np.diag([1/(2*omega),omega/2])
    Ww=Vw+.5j*J
    EwithH=lambda V,frequency:(frequency**2*V[0,0]+V[1,1])/2
    E0=EwithH(np.eye(2)/2,omega)
    Ew=EwithH(Vw,omega)
    assert abs(Ew-omega/2)<1e-12 and E0>Ew
    return {"status":"PASS","fixed_commutator":"[q,p]=i, J=[[0,1],[-1,0]]",
         "pure_Gaussian_two_point_options":out,
         "same_commutator_and_purity":True,
         "frequency_4_ground_covariance":Vw.tolist(),
         "frequency_4_ground_energy":float(Ew),
         "frequency_4_energy_in_frequency_1_vacuum":float(E0),
         "conclusion":"Even positivity, purity and the canonical commutator do not single out the vacuum. Supplying the Hamiltonian/time generator can select a ground state; it is an independent input.",
         "limits":"Only one-mode canonical Gaussian quantum mechanics; no causal-set Born-rule derivation, interacting scattering or Hadamard uniqueness theorem."}


def su2(theta,axis=0):
    g=(SX,SY,SZ)[axis]
    return np.cos(theta/2)*I2+1j*np.sin(theta/2)*g


def su2_plaquettes(ux,uy):
    L=len(ux)
    out=[]
    for x in range(L):
        for y in range(L):
            P=ux[x,y]@uy[(x+1)%L,y]@ux[x,(y+1)%L].conj().T@uy[x,y].conj().T
            out.append(P)
    return out


def su2_wilson_action(ux,uy):
    return float(sum(1-.5*np.trace(P).real for P in su2_plaquettes(ux,uy)))


def small_yang_mills_gate():
    """Gauge-invariant positive plaquette action and discrete link force.
    The Wilson action, gauge group and lattice are INPUTS, not derivations.
    """
    L=3;rng=np.random.default_rng(202611191)
    ux=np.empty((L,L,2,2),complex);uy=np.empty_like(ux)
    site=np.empty_like(ux)
    for x in range(L):
        for y in range(L):
            for obj in (ux,uy,site):
                axis=rng.normal(size=3);axis/=np.linalg.norm(axis)
                angle=rng.uniform(-1.,1.)
                obj[x,y]=np.cos(angle/2)*I2+1j*np.sin(angle/2)*sum(axis[i]*g for i,g in enumerate((SX,SY,SZ)))
    initial=su2_wilson_action(ux,uy)
    xcopy=np.empty_like(ux);ycopy=np.empty_like(uy)
    for x in range(L):
        for y in range(L):
            xcopy[x,y]=site[x,y]@ux[x,y]@site[(x+1)%L,y].conj().T
            ycopy[x,y]=site[x,y]@uy[x,y]@site[x,(y+1)%L].conj().T
    gauge_error=abs(su2_wilson_action(xcopy,ycopy)-initial)
    assert gauge_error<1e-12
    # The directional derivatives of the *actual action* are dynamical
    # forces; geometry and gauge transport alone do not assign S.
    def shift(angle,axis):
        trial=ux.copy()
        trial[0,0]=su2(angle,axis)@ux[0,0]
        return su2_wilson_action(trial,uy)
    h=1e-5
    grad=np.array([(shift(h,j)-shift(-h,j))/(2*h) for j in range(3)])
    gradient_norm=float(np.linalg.norm(grad))
    assert gradient_norm>1e-3
    unit=grad/gradient_norm
    step=-.14*gradient_norm
    gen=sum(unit[j]*[SX,SY,SZ][j] for j in range(3))
    rotated=np.cos(step/2)*I2+1j*np.sin(step/2)*gen
    newx=ux.copy()
    newx[0,0]=rotated@ux[0,0]
    final=su2_wilson_action(newx,uy)
    assert final<initial
    assert np.linalg.norm(newx[0,0]@newx[0,0].conj().T-I2)<1e-12
    return {"status":"PASS","group":"SU(2) imposed","lattice":[L,L],
         "initial_wilson_action":initial,"after_one_negative_gradient_step":final,
         "energy_decrease":initial-final,"local_frame_gauge_action_error":gauge_error,
         "one_link_gauge_force_vector":grad.tolist(),"force_norm":gradient_norm,
         "conclusion":"Chosen local gauge-invariant action has nonzero Euler-Lagrange force and a downhill step, unlike Wilson transport alone.",
         "limits":"No derivation of SU2, Wilson/Yang-Mills action, quantum measure, charged-current matter, or Standard Model beta function."}


def angle(a,b,c):
    # Angle opposite c when adjacent lengths a and b.
    x=np.clip((a*a+b*b-c*c)/(2*a*b),-1.,1.)
    return float(np.arccos(x))


def gauss_bonnet_dimensional_gate(L=3):
    """Piecewise-flat Regge Gauss-Bonnet, plus actual dimensionless growth scan."""
    rng=np.random.default_rng(202611192)
    H=1+.07*rng.normal(size=(L,L))
    V=1+.07*rng.normal(size=(L,L))
    D=np.sqrt(2)*(1+.05*rng.normal(size=(L,L)))
    deficit=np.full((L,L),2*PI)
    for x in range(L):
        for y in range(L):
            # Triangles A B C and A C D, with independent but shared edge lengths.
            ab=H[x,y];bc=V[(x+1)%L,y];ac=D[x,y]
            ad=V[x,y];cd=H[x,(y+1)%L]
            for a,b,c,places in [
                (ab,ac,bc,[(x,y),(x+1,y),(x+1,y+1)]),
                (ac,ad,cd,[(x,y),(x+1,y+1),(x,y+1)])]:
                if not abs(a-b)<c<a+b:raise ValueError("bad triangle inequalities")
                # At A, at B/D, and at C for the relevant ordering
                th0=angle(a,b,c)
                # angle at second vertex has adjacent sides a,c
                th1=angle(a,c,b)
                th2=angle(b,c,a)
                for (xx,yy),th in zip(places,(th0,th1,th2)):
                    deficit[xx%L,yy%L]-=th
    # Small local nonzero Regge curvature sums to zero on 2D torus.
    total=float(deficit.sum())
    assert abs(total)<1e-11 and np.linalg.norm(deficit)>1e-2
    # Tetrahedral triangulation of S², 3 equilateral triangles per vertex.
    sphere_deficit=4*(2*PI-3*PI/3)
    assert abs(sphere_deficit-4*PI)<1e-12
    # Existing project already tested this exact type of unembedded growth.
    samples=[causal_sample(220,p,20261119+int(1000*p)) for p in (.025,.065,.15)]
    dims=[r.get("local_dim_median") for r in samples]
    return {"status":"PASS",
       "torus_cell_complex":{"V":L*L,"E":3*L*L,"F":2*L*L,"chi":0},
       "torus_regge_total_deficit_radians":total,
       "local_regge_deficit_L2_norm":float(np.linalg.norm(deficit)),
       "local_deficit_min_max":[float(deficit.min()),float(deficit.max())],
       "sphere_tetrahedron_total_deficit_radians":float(sphere_deficit),
       "Gauss_Bonnet":"Sum_v deficit(v)=2pi*Euler, independent of the edge lengths on a 2D closed triangulation.",
       "unembedded_sequential_growth_controls":samples,
       "median_intrinsic_dimension_estimates":dims,
       "conclusion":"2D Einstein-Hilbert Regge curvature is topological and supplies no local graviton dynamics; the sampled 3-parameter causal growth has no demonstrated universal emergent 4D attractor.",
       "limits":"Spatial Euclidean 2D Regge models and finite stochastic posets, not a dynamical Lorentzian 3+1 quantum gravity path integral."}


def produce():
    fronts={
      "I_intrinsic_torus_cohomology_and_spin_torsor":torus_cell_spin_gate(),
      "II_overlap_Dirac_GW_flux_index_and_gauge_covariance":overlap_topology_gate(),
      "III_pure_quantum_state_selection_nonuniqueness":squeezed_quantum_gate(),
      "IV_dimension_gravity_topological_action_and_growth":gauss_bonnet_dimensional_gate(),
      "V_global_SpinC_charge_and_chiral_anomaly_constraints":spin_c_anomaly_gate(),
      "VI_extra_dynamic_SU2_Yang_Mills_variational_force":small_yang_mills_gate()
    }
    assert all(x["status"]=="PASS" for x in fronts.values())
    return {"status":"PASS 6 conditional physics gates; NO TOE",
      "date":"2026-11-19","TOE_solved":False,
      "quantum_gravity_derived":False,"SM_generation_or_constants_derived":False,
      "lattice_metric_spin_gauge_as_inputs":True,
      "source_urls":[
       "https://doi.org/10.1143/PTP.107.163",
       "https://doi.org/10.1103/PhysRevD.109.014502",
       "https://doi.org/10.1016/S0550-3213(99)00115-7",
       "https://andrea-cappelli.github.io/theses/villa.pdf",
       "https://doi.org/10.1007/s10714-024-03281-1",
       "https://doi.org/10.1007/s41114-019-0023-1"],
      "fronts":fronts}

def main():
    r=produce()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2),encoding="utf-8")
    f=r["fronts"]
    print(json.dumps({"status":"PASS","fronts":list(f.keys()),
      "torus_betti":f["I_intrinsic_torus_cohomology_and_spin_torsor"]["GF2_betti_numbers"],
      "overlap_Q_index":[(x["inserted_U1_flux_Q"],x["overlap_index_in_our_gamma_convention"]) for x in f["II_overlap_Dirac_GW_flux_index_and_gauge_covariance"]["sectors"]],
      "quantum_energy":f["III_pure_quantum_state_selection_nonuniqueness"]["pure_Gaussian_two_point_options"],
      "torus_total_Regge":f["IV_dimension_gravity_topological_action_and_growth"]["torus_regge_total_deficit_radians"],
      "odd_anomaly":f["V_global_SpinC_charge_and_chiral_anomaly_constraints"]["sample_nonvectorlike_2D_chiral_anomaly_free_charges"],
      "YM_deltaS":f["VI_extra_dynamic_SU2_Yang_Mills_variational_force"]["energy_decrease"],
      "output":str(OUT)}))
if __name__=="__main__":main()
