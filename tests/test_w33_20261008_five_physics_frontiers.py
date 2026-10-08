"""Independent scoped regressions for five physics frontiers (not a TOE proof)."""
from __future__ import annotations
import sys
from fractions import Fraction
from pathlib import Path
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_five_physics_frontiers as m


def test_cptp_kraus_and_observable_two_step_support():
    d=m.cp_walk_frontier()
    gs=m.build_graphs()
    for name,a in gs.items():
        assert len(np.nonzero(a)[0])==216
        assert np.all(a.sum(axis=1)==8)
        # Explicit measure-prepare action on a general pure density matrix.
        v=np.arange(1,28,dtype=float)+1j*np.arange(27,dtype=float)
        v/=np.linalg.norm(v)
        rho=np.outer(v,v.conj())
        evolved=(a.T@np.real(np.diag(rho)))/8
        assert np.isclose(evolved.sum(),1)
        assert evolved.min()>=0
        assert all(np.linalg.eigvalsh(np.diag(evolved))>=-1e-12)
        assert np.array_equal((a@a).sum(axis=1),np.full(27,64))
        z=int(sum((a@a)[i,j]==0 for i in range(27) for j in range(27) if i!=j))
        assert z==d[name]["two_step_ordered_offdiagonal_zero_count"]
    assert d["point_far_H27"]["two_step_ordered_offdiagonal_zero_count"]==54
    assert d["line_transverse_null"]["two_step_ordered_offdiagonal_zero_count"]==0


def test_levi_gauss_is_not_dirac_and_edge_current_nonclosure():
    r=m.constraint_frontier()
    assert r["levi_edges"]==160 and r["induced_length_two_wedges"]==480
    q0,q1,q2,p0,p1,p2=sp.symbols("q0 q1 q2 p0 p1 p2")
    a=(p0+p1)*(q0-q1);b=(p1+p2)*(q1-q2)
    B=sp.expand(sum(sp.diff(a,q)*sp.diff(b,p)-sp.diff(a,p)*sp.diff(b,q)
                    for q,p in [(q0,p0),(q1,p1),(q2,p2)]))
    assert B.coeff(p0*q2)==1 and B.coeff(p2*q0)==-1


def test_chirality_character_orbits_no_unique_sign():
    pts,ls=m.projective_points_and_lines()
    assert len(pts)==40 and len(ls)==40
    incidence={p:sum(p in line for line in ls) for p in pts}
    assert set(incidence.values())=={4}
    assert sum(len(line) for line in ls)==160
    r=m.chirality_frontier()
    assert r["quartic_chiral_vacua"]==2*r["conjugate_sign_pairs"]==320
    assert r["unique_handedness_from_even_potential"] is False


def test_chiral_anomalies_need_neutrino_if_BL_gauged():
    r=m.chirality_frontier()["anomaly_checks"]
    assert all(v=="0" for k,v in r.items() if not k.endswith("without_Nc"))
    assert r["cubic_BL_without_Nc"]=="-1"
    assert r["gravitational_BL_without_Nc"]=="-1"


def test_heterotic_abelian_necessary_but_not_sufficient():
    r=m.vacuum_frontier()["operator_checks"]
    for k in ("UcDcDc","QLDc","LLEc"):
        assert r[k]["Y"]=="0" and r[k]["BL"]=="-1" and r[k]["matter_parity"]==-1
        assert r["Nc"+k]["BL"]=="0" and r["Nc"+k]["matter_parity"]==1
    for k in ("QQQL","UcUcDcEc"):
        assert r[k]["BL"]=="0" and r[k]["Y"]=="0" and r[k]["matter_parity"]==1


def test_normalization_requires_input_and_spectra_not_geometry():
    a,b,z=Fraction(3),Fraction(2),Fraction(5)
    original=[(a+b*l)/z for l in (0,6,9,12)]
    for t in (Fraction(1,2),Fraction(7),Fraction(19,3)):
        assert original==[(t*a+t*b*l)/(t*z) for l in (0,6,9,12)]
    assert (original[-1]-original[0])/(original[1]-original[0])==2
    assert (m.build_graphs()["point_far_H27"]**2).shape==(27,27)


def test_five_outputs_have_explicit_boundaries():
    r=m.build()
    assert set(("quantum_channel","gravity_constraint","chirality",
                "heterotic_operator_filter","normalization")).issubset(r)
    assert r["gravity_constraint"]["naive_nearest_edge_current_algebra_closes"] is False
    assert r["normalization"]["physical_absolute_scale_derived"] is False
    assert "NOT checked" in r["heterotic_operator_filter"]["boundary"]
