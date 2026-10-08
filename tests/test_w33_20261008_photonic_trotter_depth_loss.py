"""Regression of constructed nine-stage photonic Trotter circuit and loss tradeoff."""
import json, sys
from pathlib import Path
import numpy as np
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_photonic_trotter_depth_loss as m
from w33_20261008_dual_27_electrical_transport import build_graphs


def test_compiled_trotter_approaches_exact_walk_and_loss_grows():
    design=json.loads((ROOT/"data/w33_20261008_five_physics_deepening.json").read_text())
    out=m.compile_depths(design["physical_photonic"])
    stages=[9,18,36,72,144,288,576]
    assert [r["circuit_depth"] for r in out["discriminator_vs_depth"]]==stages
    for name,a in build_graphs().items():
        rows=out["graphs"][name]
        assert len(rows)==7
        errors=[r["full_unitary_operator_norm_error"] for r in rows]
        assert all(x>y for x,y in zip(errors,errors[1:]))
        assert errors[-1]<errors[0]/15
        assert all(r["unitarity_max_entry_residual"]<1e-11 for r in rows)
        assert abs(rows[0]["uniform_survival_if_each_layer_has_1pct_loss"]-0.99**9)<1e-12
    gaps=[r["discriminator_probability_gap"] for r in out["discriminator_vs_depth"]]
    assert all(x>0 for x in gaps)
    assert gaps[3]>.25
    assert out["discriminator_vs_depth"][3]["survival_1pct_each"]<.5
    assert out["discriminator_vs_depth"][-1]["survival_1pct_each"]<.004


def test_deterministic_matrix_schedule_is_unitary():
    design=json.loads((ROOT/"data/w33_20261008_five_physics_deepening.json").read_text())
    for name,a in build_graphs().items():
        layers=design["physical_photonic"][name]["nine_layer_schedule"]
        assert len(layers)==9
        x=np.eye(27,dtype=complex)
        for matching in layers:
            y=np.eye(27,dtype=complex)
            for i,j in matching:
                y[i,i]=y[j,j]=np.cos(.78)
                y[i,j]=y[j,i]=-1j*np.sin(.78)
            assert np.max(abs(y.conj().T@y-np.eye(27)))<1e-12
            x=y@x
        assert np.max(abs(x.conj().T@x-np.eye(27)))<1e-11
        # One step differs because the adjacency-layer blocks do not commute.
        assert np.linalg.norm(x-expm(-1j*.78*a),ord=2)>.01
