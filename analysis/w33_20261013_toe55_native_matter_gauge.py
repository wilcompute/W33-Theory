"""TOE55 native W33 160-link classical U(1) scalar-matter & metric action.

Finite graph, not QED: no fermionic/chiral matter, renormalized charge,
spin-two dynamics or physical units. The U(1) Ward identities are exact.
"""
from pathlib import Path
import sys,json
import numpy as np
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
rng=np.random.default_rng(55101)
ed,volts,lookup,zero,comm,*_=prep()
B=np.rint(gradient(ed,volts,np.zeros(3)).real).astype(float)
P=np.asarray([cycle_row(loop,ed,volts,lookup,np.zeros(3)) for loop in zero+comm]).real
n_links,n_sites=B.shape
assert (n_links,n_sites)==(160,80) and np.max(abs(P@B))<1e-10
ed=np.asarray(ed,dtype=int)
z=rng.normal(size=n_sites)+1j*rng.normal(size=n_sites)
p=rng.normal(size=n_sites)+1j*rng.normal(size=n_sites)
A=rng.normal(size=n_links)*.3
E=rng.normal(size=n_links)
w=.5+rng.random(n_links)
pw=rng.normal(size=n_links)
chi=rng.normal(size=n_sites)*.8
mass2,kappa,M,kw,w0=.6,1.1,2.,3.,1.
def energies(A,z,p,E,w,pw,g):
    phase=np.exp(1j*g*A)
    diff=z[ed[:,1]]-phase*z[ed[:,0]]
    electric=.5*np.sum(E*E/w)
    magnetic=.5*np.linalg.norm(P@A)**2
    scalar=.5*np.sum(abs(p)**2+mass2*abs(z)**2)
    hopping=.5*kappa*np.sum(abs(diff)**2)
    dynamic=.5*np.sum(pw*pw/M+kw*(w-w0)**2)
    return dict(electric=float(electric),magnetic=float(magnetic),
       scalar=float(scalar),hopping=float(hopping),metric_scalar=float(dynamic),
       total=float(electric+magnetic+scalar+hopping+dynamic))
def charge(z,p):
    # Canonical coordinates (Re z,Im z), momenta (Re p,Im p);
    # J_v = x_v p_yv - y_v p_xv generates z->exp(i chi) z.
    return np.imag(z.conj()*p)
# Matter charge neutrality is required by Gauss on a finite closed graph.
J=charge(z,p)
p=p-1j*(sum(J)/sum(abs(z)**2))*z
J=charge(z,p)
assert abs(sum(J))<1e-12
for g in (.1,.3,.7):
    # C_v=(B.T E)_v/g+J_v ; first-class Abelian gauge generators.
    # The graph has no boundary, hence sum_v C_v = sum_v J_v.
    E0=np.linalg.lstsq(B.T,-g*J,rcond=None)[0]
    G=B.T@E0/g+J
    assert max(abs(G))<1e-11
    before=energies(A,z,p,E0,w,pw,g)
    transformed_A=A+B@chi/g
    zp=np.exp(1j*chi)*z
    pp=np.exp(1j*chi)*p
    after=energies(transformed_A,zp,pp,E0,w,pw,g)
    terms={key:abs(before[key]-after[key]) for key in before}
    assert max(terms.values())<1e-8,terms
    gauss_after=B.T@E0/g+charge(zp,pp)
    assert max(abs(gauss_after))<1e-11
    if g==.1:
        sample={"max_energy_change_under_finite_gauge_transform":max(terms.values()),
                "max_gauss_residual":float(max(abs(G))),"initial_total_energy":before["total"],
                "hopping":before["hopping"]}
    # Finite gauge-orbit derivative is a Ward/Poisson-bracket check
    # {Qchi,H}=0 under the canonical gauge generator.
    eps=1e-5
    def orbit(t):
      zz=np.exp(1j*t*chi)*z
      pp0=np.exp(1j*t*chi)*p
      return energies(A+t*(B@chi)/g,zz,pp0,E0,w,pw,g)["total"]
    ward=(orbit(eps)-orbit(-eps))/(2*eps)
    assert abs(ward)<1e-8,(g,ward)
    sample[f"ward_derivative_g_{g}"]=float(ward)
# A matter coupling parameter cannot be inferred from the
# free acoustic W33 Maxwell spectrum. Show different finite hopping
# energies for different g at identical fields, while exact U1 survives.
vals={str(g):energies(A,z,p,E,w,pw,g)["hopping"] for g in (.1,.3,.7)}
assert max(vals.values())-min(vals.values())>1e-3
# First-class constraint algebra: C_v=(B.T E)/g + J_v,
# {C_v,C_w}=0 by canonical brackets, because {J_v,J_w}=0
# for distinct sites and {J_v,J_v}=0 antisymmetrically.
out={"status":"PASS_NATIVE_W33_CLASSICAL_U1_SCALAR_MATTER_METRIC_ACTION",
"w33_native_sites":n_sites,"w33_native_links":n_links,
"plaquette_rows":int(P.shape[0]),"max_plaquette_gradient_residual":float(np.max(abs(P@B))),
"action":"H=sum_e E_e²/(2w_e)+||P A||²/2+sum_v [|p_v|²+m²|z_v|²]/2 +κ sum_(a->b)|z_b-exp(ig A_e)z_a|²/2+sum_e[pw_e²/(2M)+kw(w_e-w0)²]/2",
"gauge":"A->A+B χ/g ; z,p->exp(iχ_v)*(z,p); E,w,pw invariant",
"gauss":"C_v=(B.T E)_v/g+Im(conj(z_v)*p_v). Canonical local U1 gauge generator, 80 Abelian first-class constraints for generic charged matter.",
"gauss_poisson_algebra":"{C_v,C_u}=0 identically, local charges J_v=x_v p_yv-y_v p_xv, commuting across sites; electric E commutes with J.",
"gauge_orbit_trials":[.1,.3,.7],"sample":sample,
"free_gauge_coupling_values_hopping_energy":vals,
"gauge_coupling_freedom":"The graph and magnetic/electric kinetic spectrum remain unchanged when varying free g. Coupled matter hopping varies. Quantized physical α requires additional dynamical normalization and matching; this finite model leaves g unspecified.",
"scope":"An explicit single finite classical Hamiltonian coupling scalar charge, W33 Maxwell and dynamical link-weight scalar variables. Gauge closure survives, but there is no Lorentzian continuum limit, spin-1/2 chiral fermion, nonabelian SM, Einstein constraints, quantization, renormalized coupling or prediction of nature."}
(R/"data/w33_20261013_toe55_native_matter_gauge.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"P_B":out["max_plaquette_gradient_residual"],"sample":sample,"couplings":vals}),flush=True)
