#!/usr/bin/env python3
"""One-photon generic n-qubit register dimension and mesh complexity firewall."""
from __future__ import annotations
import json
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]/"data/toe_20261122_single_photon_scaling_gate.json"

def verify():
    rows=[]
    for n in (1,2,3,4,6,8,10):
        d=2**n
        rows.append(dict(logical_qubits=n,required_orthogonal_modes=d,
                         generic_SU_d_real_parameters=d*d-1,
                         standard_Clements_two_mode_cells=d*(d-1)//2))
    assert rows[1]["required_orthogonal_modes"]==4
    assert rows[-1]["required_orthogonal_modes"]==1024
    assert rows[-1]["standard_Clements_two_mode_cells"]==523776
    assert rows[-1]["generic_SU_d_real_parameters"]==1048575
    return dict(status="PASS_SINGLE_PHOTON_GENERIC_REGISTER_SCALING_FIREWALL",
        date="2026-11-22",census=rows,
        theorem="One photon in d mutually orthogonal single-particle modes spans C^d. An unconstrained n-qubit state needs d>=2^n. General SU(d) has d^2-1 parameters and the conventional universal d-mode Clements decomposition has d(d-1)/2 two-mode cells.",
        conclusion="At n=10, 1024 mutually orthogonal modes and 523776 two-mode cells in a standard fully universal mesh; dense fixed-gate controllability at d=4 alone does not solve scalable BQP.",
        caveat="Not a lower bound on specialized compressed algorithms, alternative DOF/multiphoton processors, error-corrected architectures, or energy; no claimed universal quantum advantage.")

def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS one photon general state dimension resource census")
if __name__=="__main__":main()
