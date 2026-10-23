"""GF16, chiral tunneling, bounded SWAP search, magic noise, native gauge controls."""
import json,math
from pathlib import Path
import numpy as np
from analysis.w33_20261023_gf16_first_order_obstruction import construct,rank_rows,kernel
from analysis.w33_20261023_round9_five_frontiers import (
    gf16_extension,chiral_dynamics,tfim_spectrum,
    heralded_fault_pipeline,native_gauge_wave)
from analysis.w33_20261022_five_followups_round5 import A,transvection,cycles

ROOT=Path(__file__).resolve().parents[1]


def test_GF16_bitset_exact_obstruction_and_char2_splitting():
    src=json.loads((ROOT/"data/PART_20261023_GF16_FIRST_ORDER_OBSTRUCTION.json").read_text())
    got=construct(16)
    assert got==src["cases"][-1]
    assert got["n"]==4369 and got["dimC"]==256
    assert got["rankDC"]==120 and got["rankDK"]==1928
    assert got["rank_DK_intersection_C"]==120
    assert got["rank_delta1"]==0
    assert [x["rank_delta1"] for x in gf16_extension()["cases"]]==[0,0,0]


def test_transverse_chirality_tunneling_and_antiunitary_evenness():
    d=chiral_dynamics()
    rows=d["spectral_rows"]
    for n in (2,4,6,8):
        values=[r for r in rows if r["n"]==n]
        assert len(values)==3
        assert values[0]["gap"]==0
        assert values[1]["gap"]>0 and values[2]["gap"]>0
        assert values[1]["energy0"]>values[2]["energy0"]
        assert values[1]["graph_degree_max"]<=12
    for n in (4,6,8):
        p=tfim_spectrum(n,.1,.001)
        m=tfim_spectrum(n,.1,-.001)
        assert abs(p["energy0"]-m["energy0"])<1e-9


def test_four_layer_budget28_still_unresolved_without_false_infeasibility():
    dat=json.loads((ROOT/"data/PART_20261023_SWAPCOUNT_28_SEARCH.json").read_text())
    assert dat["status"]=="UNKNOWN" and dat["swap_budget"]==28
    assert dat["proof_of_lower_bound_36"] is False
    assert len(cycles(transvection(0)))==9
    assert all(len(z)==3 for z in cycles(transvection(0)))
    assert 28<=36
    assert A.shape==(40,40)


def test_magic_heralding_exact_first_order_noise():
    result=heralded_fault_pipeline()
    assert result["number_accepted_fault_sites"]==4
    assert [x["site"] for x in result["accepted_fault_sites"]]==[0,1,2,3]
    assert math.isclose(result["dSuccess_dp_at_p0"],-128/9,abs_tol=1e-11)
    assert math.isclose(result["dConditionalFidelity_dp_at_p0"],-228/841,abs_tol=1e-12)
    for sample in result["accepted_fault_sites"]:
        assert math.isclose(sample["success"],2/81,abs_tol=1e-12)
        assert math.isclose(sample["fidelity"],1/58,abs_tol=1e-12)
    assert result["noise_controls"][0]["single_fault_truncated_conditional_fidelity"]==1


def test_four_dimensional_native_metric_and_exact_gauge_Ward():
    d=native_gauge_wave()
    G=np.asarray(d["native_G"])
    metric=np.asarray(d["metric_G_over_rho"])
    assert np.allclose(G/d["rho"],metric)
    assert math.isclose(d["rho"],2/27,abs_tol=1e-12)
    assert np.allclose(metric,[[5,2.5,-3,0],[2.5,5,0,-3],[-3,0,6,-3],[0,-3,-3,6]])
    assert np.all(np.linalg.eigvalsh(metric)>0)
    errors=[x["relative_acoustic_metric_error"] for x in d["rows"]]
    assert errors[0]>errors[1]>errors[2]>errors[3]>0
    assert errors[0]/errors[1]>3.5
    assert errors[1]/errors[2]>3.5
    assert errors[2]/errors[3]>3.5
    assert all(abs(x["discrete_gauge_eigenvalues"][0])<1e-10 for x in d["rows"])
