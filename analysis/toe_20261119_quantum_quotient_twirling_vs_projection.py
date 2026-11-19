#!/usr/bin/env python3
"""Z2 history symmetry: twirling a density != projecting to invariant vectors.

Exact finite counterexample useful for SSR/causal history/gauge quotient audits.
Not a cosmological quantum measure nor a theorem on continuum gravity.
"""
import json
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'data/toe_20261119_quantum_symmetry_orbit_coherence_extra.json'

def gate():
    I=np.eye(2,dtype=complex);U=np.array([[0,1],[1,0]],dtype=complex)
    pinv=(I+U)/2
    plus=np.array([1,1],dtype=complex)/np.sqrt(2)
    minus=np.array([1,-1],dtype=complex)/np.sqrt(2)
    states={"symmetric":np.outer(plus,plus.conj()),
            "antisymmetric":np.outer(minus,minus.conj()),
            "classical_incoherent":I/2}
    rows=[]
    for name,rho in states.items():
        twirled=(rho+U@rho@U.conj().T)/2
        projected=pinv@rho@pinv
        rows.append({"state":name,
          "same_labeled_diagonal_distribution":[float(rho[0,0].real),float(rho[1,1].real)],
          "Z2_twirl_trace":float(np.trace(twirled).real),
          "Z2_twirl_purity":float(np.trace(twirled@twirled).real),
          "invariant_projection_trace":float(np.trace(projected).real),
          "unnormalized_coherent_sum_weight":float((np.ones(2)@rho@np.ones(2)).real),
          "unitary_action_on_density_preserves_state":bool(np.allclose(U@rho@U.conj().T,rho))})
        assert np.allclose(twirled,rho)
        assert np.allclose(np.diag(rho),[.5,.5])
    x={a['state']:a for a in rows}
    assert np.allclose([x[k]['invariant_projection_trace'] for k in ('symmetric','antisymmetric','classical_incoherent')],[1.,0.,.5],atol=1e-12)
    assert np.allclose([x[k]['unnormalized_coherent_sum_weight'] for k in ('symmetric','antisymmetric','classical_incoherent')],[2.,0.,1.],atol=1e-12)
    assert all(abs(y['Z2_twirl_trace']-1)<1e-12 for y in rows)
    # Pure anti-invariant vector is an invariant RAY but not a gauge-invariant
    # VECTOR. If this Z2 is a gauge redundancy, the latter is the relevant
    # physical-state condition absent an additional charged boundary sector.
    a=np.array([1,-1],complex)
    assert np.allclose(U@a,-a)
    assert abs(np.sum(a))<1e-12
    return {"date":"2026-11-19","status":"PASS exact Z2 symmetry-versus-quantum-coherence gate",
      "TOE_solved":False,
      "histories_acted_on_by_Z2":2,
      "rows":rows,
      "trivial_rep_projection_P":"(I+U_swap)/2",
      "twirl_of_density_T":"(rho+U_swap rho U_swap_dagger)/2",
      "critical_difference":"The antisymmetric density is invariant under conjugation, and is a physical RAY under the exchange, but its vector is not invariant; physical gauge Hilbert selection needs an explicit representation/boundary-sector rule beyond density twirling.",
      "unlabeled_amplitude_obstruction":"Relative orbit labels carrying amplitudes (1,-1) are not a single-valued complex amplitude on the quotient orbit. Naively choosing a representative gives a sign ambiguity; projecting to trivial representation cancels the orbit amplitude.",
      "SSR_connection":"A U1 particle-number SSR constrains local accessible observables and charge-sector coherence; this is not the same as quotienting classical histories by permutations or projecting vectors onto gauge-invariant states.",
      "quantum_measure_limitation":"The unnormalized coherent-sum weights 2,0,1 cannot all be interpreted as normalized probabilities for one exhaustive event; no dynamics, physical decoherence functional or Lorentzian gravity derived."}

def main():
    r=gate();OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(r,indent=2)+'\n');print('PASS symmetry quantum quotient',[(x['state'],x['invariant_projection_trace']) for x in r['rows']])
if __name__=='__main__':main()