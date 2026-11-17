"""Complete 24-real-component SU5 Hermitian-adjoint Hessian.

At V=-m2 Tr(Phi^2)+lambda (TrPhi^2)^2+kappa TrPhi^4
with positive kappa and m2,lambda+7*kappa/30 positive, the
global 3+2 VEV has 12 gauge Goldstones and 12 radial/shape modes.
We compute the whole 24x24 Hessian in an orthonormal su(5) basis.

The Z2-even model supports sign-related inequivalent gauge orbits;
a straight-line kink is a restricted field configuration and gives
an upper bound on the true minimal wall tension, not a physical
cosmological domain-wall prediction.
"""
from pathlib import Path
import json,math
import numpy as np
import scipy.linalg as la
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261117_SU5_complete_Hessian_thermal_wall.json"

def basis5():
    n=5
    B=[]
    for i in range(n):
        for j in range(i+1,n):
            R=np.zeros((n,n),complex);R[i,j]=R[j,i]=1/math.sqrt(2)
            I=np.zeros((n,n),complex);I[i,j]=-1j/math.sqrt(2);I[j,i]=1j/math.sqrt(2)
            B.extend([R,I])
    for k in range(1,n):
        T=np.zeros((n,n),complex)
        T[np.arange(k),np.arange(k)]=1/math.sqrt(k*(k+1))
        T[k,k]=-k/math.sqrt(k*(k+1))
        B.append(T)
    assert len(B)==24
    Gram=np.array([[np.trace(A@B1).real for B1 in B] for A in B])
    assert np.allclose(Gram,np.eye(24),atol=1e-14)
    assert all(abs(np.trace(t))<1e-14 for t in B)
    return B

def full_hessian(m2=1.,lam=.35,kappa=.75):
    assert m2>0 and kappa>0 and lam+7*kappa/30>0
    g=lam+7*kappa/30
    r=math.sqrt(m2/(2*g))
    phi=np.diag([2,2,2,-3,-3])*r/math.sqrt(30)
    B=basis5()
    H=np.empty((24,24),float)
    for i,T in enumerate(B):
        for j,U in enumerate(B):
            delta=np.trace(T@U).real
            q1=np.trace(phi@T).real
            q2=np.trace(phi@U).real
            d4=(4*np.trace(phi@phi@(T@U+U@T)) +
                2*np.trace(phi@T@phi@U+phi@U@phi@T)).real
            H[i,j]=(-2*m2+4*lam*r*r)*delta +8*lam*q1*q2+kappa*d4
    assert np.allclose(H,H.T,atol=1e-10)
    evals=np.linalg.eigvalsh(H)
    expected=np.array([0.]*12+[2*kappa*r*r/3]*8+
                       [8*kappa*r*r/3]*3+[4*m2])
    assert np.allclose(evals,expected,atol=1e-10), (evals,expected)
    # Spot-check analytical Hessian against central finite differences
    rng=np.random.default_rng(20261117)
    def V(P):
        return (-m2*np.trace(P@P)+lam*np.trace(P@P)**2+
                kappa*np.trace(P@P@P@P)).real
    tests=[]
    for q in range(7):
        co=rng.normal(size=24)
        co/=np.linalg.norm(co)
        T=sum(c*b for c,b in zip(co,B))
        h=1e-3
        finite=(V(phi+h*T)-2*V(phi)+V(phi-h*T))/h**2
        exact=co@H@co
        assert abs(finite-exact)<1e-5
        tests.append(abs(finite-exact))
    return {"status":"PASS_SU5_FULL_24_REAL_SCALAR_HESSIAN",
       "normalization":"Hermitian adjoint Phi with 1/2 Tr(dPhi)^2 canonical kinetic; basis Tr(T_i T_j)=delta_ij",
       "VEV_norm_r":r,"squared_norm_r2":r*r,
       "full_24x24_eigenvalue_spectrum":[float(v) for v in evals],
       "eigenvalue_multiplicities":{
           "gauge_orbit_Goldstone_12":{"multiplicity":12,"m2":0},
           "SU3_colour_octet_8":{"multiplicity":8,"m2":2*kappa*r*r/3},
           "SU2_weak_triplet_3":{"multiplicity":3,"m2":8*kappa*r*r/3},
           "radial_singlet_1":{"multiplicity":1,"m2":4*m2}},
       "Goldstones":"12 zero eigenvalues are tangent to SU5/S(U3xU2); eaten by massive gauge bosons in gauged theory",
       "numeric_directional_Hessian_finite_difference_max_error":max(tests),
       "no_E6_completion":"Spectrum applies to bosonic SU5 adjoint potential, NOT soft E6 full scalar spectrum or quantum-corrected masses."}

def thermal_and_wall(m2=1.,lam=.35,kappa=.75,thermal_c=.4):
    g=lam+7*kappa/30
    r=math.sqrt(m2/(2*g))
    # Simplified high-T shape-blind c T^2 TrPhi² correction.
    Tc=math.sqrt(m2/thermal_c)
    sigma=(4/3)*math.sqrt(2*g)*r**3
    # The restricted 1D kink is phi(x)=r tanh(sqrt(2g) r x)D
    # with normalized D=diag(2,2,2,-3,-3)/sqrt30.
    def field(z):
        return r*math.tanh(math.sqrt(2*g)*r*z)
    for z in (-2.,0.,2.):
        f=field(z)
        first=r*math.sqrt(2*g)*r*(1-math.tanh(math.sqrt(2*g)*r*z)**2)
        assert first>0
        assert abs(field(-z)+field(z))<1e-12
    # The actual wall tension can be LOWER along multidimensional paths;
    # the ansatz tension is a variational upper bound if an exact Z2
    # is present and the barrier is finite.
    return {"status":"PASS_SU5_MEAN_FIELD_THERMAL_AND_RESTRICTED_SIGN_WALL",
      "mean_field_addition":"delta V = +c T² TrPhi²; c assumed positive and shape-independent",
      "thermal_coefficient_c":thermal_c,
      "mean_field_symmetry_restoration_temperature":Tc,
      "below_Tc_3plus2_shape_persists_if_kappa_positive":True,
      "do_not_infer_transition_order":"Gauge and bosonic loop cubic terms, daisy resummation and nonperturbative thermal effects can make the actual transition first order; mean-field threshold only.",
      "Z2_sign_orbits":"If Phi->-Phi is an exact GLOBAL Z2 and only this adjoint VEV selects the vacuum, the 3+2 and opposite 2+3 sign multisets are not SU5-conjugate.",
      "restricted_one_component_kink_profile":"f(z)=r tanh(sqrt(2g)*r*z) with g=lambda+7kappa/30; Phi=f(z) diag(2,2,2,-3,-3)/sqrt30",
      "restricted_wall_tension":sigma,
      "tension_is_upper_bound":"A nontrivial multidimensional wall path may have smaller tension; if Z2 is explicitly broken, stable walls need not exist.",
      "quantum_physics_not_computed":"This is a leading phenomenological thermal mass term, not the actual one-loop finite-T E6 action."}

def verify():
    return {"status":"PASS_SU5_24MODE_HESSIAN_THERMAL_RESTRICTED_KINK",
            "Hessian":full_hessian(),"thermal_wall":thermal_and_wall()}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"])
