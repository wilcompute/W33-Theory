"""TOE67 regressions: exact Fourier all-temperature flux and ribbon symmetry."""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe67_continuous_all_beta_determinant import (
    certificate as determinant_certificate,native_three_chords,
    quarter_sample_coefficients)
from w33_20261014_toe67_ribbon_symmetry_obstruction import (
    certificate as symmetry_certificate)

def test_all_64_exact_gaussian_integer_charpolys_and_strict_margins():
    q=determinant_certificate()
    assert q["status"]=="PASS_TOE67_EXACT_CONTINUOUS_ALL_BETA_FLUX_THEOREM"
    assert q["exact_quarter_phase_samples"]==64
    assert q["phase_chord_indices"]==[59,93,139]
    assert [min(t["strict_coordinate_margin"]) for t in q["margin_table"]]==[
        138,3344,29664,121056,221568,89088,13728]
    assert len(q["fourier_coefficients"])==27
    assert q["coefficients_e0_through_e10_at_pi"]==[
        1,52,1116,12960,89492,380192,994976,1561792,1386816,627456,109824]

def test_independent_integer_zero_and_pi_bipartite_spectra():
    edges,sel=native_three_chords()
    base=quarter_sample_coefficients(edges,sel,(0,0,0))
    pi=quarter_sample_coefficients(edges,sel,(2,2,2))
    assert base==[1,52,1116,12960,88560,357696,793152,746496,0,0,0]
    assert pi==[1,52,1116,12960,89492,380192,994976,1561792,1386816,627456,109824]
    assert all(a>=b for a,b in zip(pi,base))

def native_singular_squares(theta):
    edges,sel=native_three_chords()
    B=np.zeros((40,40),complex)
    for e,(a,b) in enumerate(edges):
        B[a,b-40]=np.exp(1j*theta[sel.index(e)]) if e in sel else 1.
    return np.linalg.svd(B,compute_uv=False)**2

def test_offgrid_fourier_against_full_matrix_and_det_order():
    import ast
    q=json.loads((ROOT/"data/w33_20261014_toe67_continuous_all_beta_determinant.json").read_text())
    modes={ast.literal_eval(n):np.asarray(arr) for n,arr in q["fourier_coefficients"].items()}
    ref=native_singular_squares(np.pi*np.ones(3))
    for angles in ([.2,.5,1.1],[1.7,2.8,5.9],[2.91,3.04,3.01]):
        th=np.asarray(angles)
        spec=native_singular_squares(th)
        assert sum(spec<1e-9)==12
        assert sum(abs(spec-6.)<1e-8)==18
        active=spec[(spec>1e-9)&(abs(spec-6.)>1e-8)]
        assert len(active)==10
        direct=np.zeros(11);direct[0]=1.
        for eig in active:
            for k in range(10,0,-1):direct[k]+=eig*direct[k-1]
        reconstruction=sum((np.exp(1j*np.dot(n,th))*c for n,c in modes.items()),np.zeros(11,complex))
        assert np.allclose(reconstruction.real,direct,atol=.00003,rtol=1e-9)
        assert max(abs(reconstruction.imag))<1e-7
        for t in (.03,.5,3.):
            assert sum(np.log1p(t*ref))>sum(np.log1p(t*spec))

def test_common_staggered_mass_thermal_dominance():
    sqpi=native_singular_squares(np.pi*np.ones(3))
    sqother=native_singular_squares(np.array([.23,1.91,4.04]))
    for m in (0.,.7,3.):
        for beta in (.2,1.,9.):
            def free(sq):
                e=beta*np.sqrt(sq+m*m)/2
                return -2/beta*sum(np.logaddexp(e,-e))
            assert free(sqpi)<free(sqother)

def test_explicit_order_three_symplectic_ribbon_obstruction():
    c=symmetry_certificate()
    assert c["status"]=="PASS_TOE67_FULL_SYMMETRY_RIBBON_NO_GO"
    assert c["line_action_on_four_incident_lines"]==[0,2,3,1]
    assert c["full_PSp_invariant_ribbon_rotation_exists"] is False
    assert c["rotation_independent_doubled_genus"]==81
    assert all(q["doubled_genus"]==81 for q in c["illustrative_consistent_boundary_counts"])

def test_exact_fermionic_zero_shell_canonical_degeneracy():
    from math import comb
    q=determinant_certificate()
    f=q["flatband_entropy_obstruction"]
    assert f["minimum_zero_one_particle_states_for_any_flat_phase"]==24
    assert f["canonical_N40_many_body_zero_shell_degeneracy_lower"]==comb(24,12)==2704156
    assert f["canonical_N40_many_body_zero_shell_degeneracy_at_zero_phase"]==comb(30,15)==155117520
    assert "not" in q["scope"].lower()
