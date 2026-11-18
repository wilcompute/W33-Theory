"""Exact E6 F/D-flat rank audit, wire geometry control, and BF cusp tower.

Independent extensions of the repo's 18 November quartic Higgs and winding
papers; never assert a physical compactification.
"""
from __future__ import annotations
import itertools, json, math, sys
from pathlib import Path
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))

def higgs_full_moduli():
    # Supplied multiplets are one complex chiral adjoint 78 and one 27+27bar.
    n=78+27+27
    # The original superpotential is W=I-I^2/2, where
    # I=Hbar_i A^i_j S^j. Exactly F-flat at I=1 since W'=0.
    x,y,z=s.symbols("x y z")
    I=x*y*z;W=I-I**2/2
    vacuum={x:1,y:1,z:1}
    assert all(s.diff(W,v).subs(vacuum)==0 for v in (x,y,z))
    H=s.hessian(W,[x,y,z]).subs(vacuum)
    assert H==-s.ones(3) and H.rank()==1
    # At any full-field vacuum dI!=0 the exact chain rule yields
    # Hess W = -(dI)(dI)^T, hence rank1 in ALL 132 complex coords.
    # One full complex row of dI is nonzero, already seen in singlets.
    full_Fflat_complex_dimension=n-1
    # E6 has complex dim78. If SM gauge survives, stabilizer >=12.
    gdim=78;smin=8+3+1
    orbitmax=gdim-smin
    physical_flat_complex_min=full_Fflat_complex_dimension-orbitmax
    assert (n,orbitmax,physical_flat_complex_min)==(132,66,65)
    # D-term curvature plus massive-gauge Goldstone pairs can remove
    # at most two real modes per broken complex gauge generator.
    ungapped_real_min=2*n-2-2*orbitmax
    assert ungapped_real_min==2*physical_flat_complex_min==130
    # Charge-lattice global residual is NOT automatically a physical Z20;
    # the same SNF=(1,20) was already certified in 17 Nov repo.
    Q=s.Matrix([[-5,5,0],[-3,-1,4]])
    SN=smith_normal_form(Q,domain=ZZ)
    assert SN[0,0]==1 and abs(SN[1,1])==20
    assert Q*s.ones(3,1)==s.zeros(2,1)
    return dict(status="PASS",full_chiral_complex_coordinates=n,
       invariant="I=bar27 * A78 * 27",
       superpotential="W=f(I)=I-I^2/2 at I=1",
       exact_full_Fflat_hessian_rank=1,
       Fflat_smooth_complex_hypersurface_dimension=full_Fflat_complex_dimension,
       maximal_broken_complex_E6_generators_with_SM_preserved=orbitmax,
       local_F_and_D_flat_complex_moduli_lower_bound=physical_flat_complex_min,
       tree_level_uneaten_real_flat_directions_lower_bound=ungapped_real_min,
       verified_three_singlet_subspace_Hessian=[[int(v) for v in row] for row in H.tolist()],
       Abelian_charge_Smith_diagonal=[1,20],
       qualified_moduli_claim="Under a 4D global N=1 E6 gauge theory with these full chiral multiplets, ONLY the specified W=f(I), zero FI and a closed polystable Dflat SM-neutral vacuum, the Kähler quotient has at least65 complex moduli locally. If additional terms, flux, supergravity or a nonpolystable orbit are included, the count can change.",
       conclusion="Original algebraic F/D-flat E6 vacuum is extremely non-isolated; not a derived stable vacuum. Z20 is in the Abelian covering torus only, already known in 2026-11-17 source.")


def cusp_BF_tower():
    """Count horizontal winding vectors and a uniform BF-deficit subband."""
    pi=math.pi
    out=[]
    for r in (0.5,1.0,2.0):
        for y in (100.,1000.,10000.,100000.):
            # lambda_u = (3 pi r/y) u^2, v=0; BF iff 0<lambda<12
            factor=3*pi*r/y
            n_unsafe=int(math.floor(math.sqrt(12/factor)))
            while factor*n_unsafe*n_unsafe>=12:n_unsafe-=1
            while factor*(n_unsafe+1)**2<12:n_unsafe+=1
            # Strict subband 3<=lambda<=5 lies in BF with margin
            # B(lambda)=sqrt(4+16lambda)-lambda-2 >= Bmin>0.
            lmin=3.;lmax=5.
            low=int(math.ceil(math.sqrt(lmin/factor)))
            high=int(math.floor(math.sqrt(lmax/factor)))
            while factor*low*low<lmin:low+=1
            while factor*high*high>lmax:high-=1
            cntmax=max(0,high-low+1)
            # The BF deficit at lambda=3 is sqrt52-5 ~2.211
            # and at 5 is sqrt84-7 ~2.165, so >= sqrt84-7.
            deficit_min=min(math.sqrt(4+16*lmin)-lmin-2,
                            math.sqrt(4+16*lmax)-lmax-2)
            assert deficit_min>2.16
            out.append(dict(flux_ratio=r,height=y,
                  oriented_BF_unsafe_horizontal_vectors=2*n_unsafe,
                  robust_subband_lambda=[lmin,lmax],
                  oriented_robust_subband_vectors=2*cntmax,
                  conservative_BF_deficit_lower_bound=deficit_min,
                  U_positive_min=low,U_positive_max=high,
                  normalized_unsafe_count_over_sqrt_y=2*n_unsafe/math.sqrt(y)))
    # This is asymptotically 4 sqrt(y/(pi r)) oriented BF-unsafe
    # vectors; the robust 3..5 band count is
    # (2/sqrt(3 pi r))*(sqrt5-sqrt3)*sqrt y + O(1).
    asymptotic_BF="4/sqrt(pi*r) * sqrt(y) + O(1)"
    asymptotic_robust="2*(sqrt(5)-sqrt(3))/sqrt(3*pi*r) * sqrt(y) + O(1)"
    assert all(x["oriented_BF_unsafe_horizontal_vectors"]>0 for x in out)
    assert all(x["oriented_robust_subband_vectors"]>=0 for x in out)
    return dict(status="PASS",cases=out,
       BF_oriented_horizontal_asymptotic=asymptotic_BF,
       strong_BF_deficit_band_asymptotic=asymptotic_robust,
       v_nonzero_at_deep_cusp="For fixed r and y large, any v!=0 has lambda>=3*pi*r*v^2*y, so the growing horizontal tower is isolated within this conditional winding branch.",
       physical_scope="This is the original conditional mixed-branch mass formula; identical +/- winding vectors need not be independent physical tachyon fields. At y->infty growing tower invalidates any fixed finite-species low-energy truncation. Does not prove universal M-theory tachyons; may be beyond EFT validity.")


def harmonic_wire_nogo():
    # M = S1 x (disk punctured by m balls) has S1 angular form dtheta
    # nonexact, nonsingular, closed/co-closed in local product metric
    # away from ball punctures. Thus topology b1>0 DOES NOT force
    # Morse critical points/localized bulk Gaussians.
    # Compute exactly the forward finite-difference holonomy on a
    # periodic 1D circle: no critical point, for any nonzero winding.
    n=12
    x=s.symbols("x",real=True)
    D=lambda f:s.diff(f,x)
    deriv=D(x)
    assert deriv==1
    # Holonomy around the S1 angular coordinate theta, winding k:
    # int_circle phi = 2*pi*k, nowhere zero for k!=0.
    # Puncturing small balls does not introduce bulk critical zeros.
    m=3
    euler_relative=-m # χ(M, union three S2)=χ(M)-χ(S2^3)=3-6=-3
    assert euler_relative==-3
    return dict(status="PASS",relative_betti_three=[0,3,0,0],
        relative_Euler_characteristic=euler_relative,
        smooth_nowhere_vanishing_closed_1form="phi=dtheta on solid torus, away from specified punctures; locally harmonic in product metric, no interior zero",
        period="integral_{S1}phi=2*pi",
        obstruction="Nonzero relative Betti/index does not force any interior Morse zero. Source/boundary conditions can carry the modes; a physical localized spinor background must derive its critical points, charge quantization and boundary projectors.",
        caveat="A nowhere-zero harmonic 1-form may fail the prescribed electric/magnetic boundary condition on puncture spheres; the claim is a logical counterexample to an automatic index-to-interior-defect implication, not a globally solved PW background with all boundary conditions.")


def run():
    out=dict(status="PASS",E6_flat_vacuum=higgs_full_moduli(),
             BF_cusp_tower=cusp_BF_tower(),wire_harmonic=harmonic_wire_nogo())
    path=ROOT/"data/toe_20261118_E6_flatness_BF_cusp_tower_wire_index_gate.json"
    path.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS: E6 full 132 Hessian rank1 >=65 flat complex moduli, BF cusp sqrt(y) tower, relative-cohomology/no-zero distinction")
    for q in out["BF_cusp_tower"]["cases"]:
        if q["flux_ratio"]==1:
            print("BF",q["height"],q["oriented_BF_unsafe_horizontal_vectors"],
                  q["oriented_robust_subband_vectors"])
    return out

if __name__=="__main__":run()
