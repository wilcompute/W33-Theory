#!/usr/bin/env python3
"""Reproducible nine-matching-layer photonic Trotter compilation and loss control."""
import json, math, sys
from pathlib import Path
import numpy as np
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_dual_27_electrical_transport import build_graphs
from w33_20261008_five_plus_one_deep import physical_photonic

OUT=ROOT/"data"/"w33_20261008_photonic_trotter_depth_loss.json"


def compile_depths(schedules=None):
    if schedules is None:
        schedules=physical_photonic()
    t=.78
    layers=(1,2,4,8,16,32,64)
    d={}
    for name,a in build_graphs().items():
        schedule=schedules[name]["nine_layer_schedule"]
        assert len(schedule)==9
        target=expm(-1j*t*a)
        out=[]
        for n in layers:
            step=np.eye(27,dtype=complex)
            theta=t/n
            co=np.cos(theta);si=np.sin(theta)
            for matching in schedule:
                e=np.eye(27,dtype=complex)
                for i,j in matching:
                    e[i,i]=co;e[j,j]=co
                    e[i,j]=-1j*si;e[j,i]=-1j*si
                step=e@step
            u=np.linalg.matrix_power(step,n)
            err=float(np.linalg.norm(u-target,ord=2))
            unit=float(np.max(np.abs(u.conj().T@u-np.eye(27))))
            mx=float(max(abs(u[i,j])**2 for i in range(27) for j in range(27) if i!=j))
            out.append({"repetitions":n,"physical_two_port_stages":9*n,
                        "full_unitary_operator_norm_error":err,
                        "unitarity_max_entry_residual":unit,
                        "max_offdiagonal_transfer":mx,
                        "uniform_survival_if_each_layer_has_1pct_loss":0.99**(9*n)})
            assert unit<1e-11
        assert out[-1]["full_unitary_operator_norm_error"]<out[0]["full_unitary_operator_norm_error"]
        d[name]=out
    cross=[]
    for i in range(len(layers)):
        p=d["point_far_H27"][i]
        l=d["line_transverse_null"][i]
        cross.append({"repetitions":p["repetitions"],
                      "discriminator_probability_gap":p["max_offdiagonal_transfer"]-l["max_offdiagonal_transfer"],
                      "circuit_depth":p["physical_two_port_stages"],
                      "survival_1pct_each":p["uniform_survival_if_each_layer_has_1pct_loss"]})
    result={"dimensionless_evolution_time":t,
            "assumptions":"Each matching is a simultaneous set of disjoint ideal two-port couplers, identical uniform per-layer survival 0.99; no port crosstalk or calibration error",
            "graphs":d,"discriminator_vs_depth":cross,
            "scope":"Trotter compilation feasibility and supplied loss toy; not a calibrated integrated photonic circuit"}
    return result


if __name__=="__main__":
    result=compile_depths()
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    for a in result["discriminator_vs_depth"]:
        print(a)
    print("TROTTER_DEPTH_CERT_PASS")
