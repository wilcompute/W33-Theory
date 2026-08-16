#!/usr/bin/env python3
"""Pass5682 bonkers: graph-cover refinement does not determine the physical speed of light.

A graph covering is a local isomorphism: every vertex in every connected Levi voltage
cover has the same four-neighbour local star as its image downstairs.  Therefore a
nearest-neighbour discrete-time propagator has the same microscopic causal statement
at every level,

    graph distance travelled per tick <= 1 edge.

Assign physical edge length ell_n and physical tick duration tau_n.  The causal speed
calibration is then

    c_n = ell_n / tau_n.

The cover construction fixes neither ell_n nor tau_n.  It adds sheets/global states;
it does not subdivide an abstract edge.  Consequently node count alone cannot fix an
SI propagation speed.

If one *chooses* to reinterpret a cover tower as a fixed-volume d-dimensional spatial
refinement, N_n=2^n N_0 implies ell_n/ell_0=2^{-n/d}.  Keeping a finite nonzero causal
speed then requires tau_n/tau_0 to scale by the same factor.  Both d and the absolute
ratio ell_0/tau_0 remain additional physical input unless independently derived.

This turns the "speed of light as processor speed" intuition into a precise boundary:
the finite geometry can supply a one-edge-per-tick causal cone, but total internal node
count controls state-space size, not the conversion from graph units to metres/seconds.
"""
from __future__ import annotations

import json
from pathlib import Path
import w33_pass5677_connected_levi_voltage_tower as tower

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5682_COVER_TOWER_CAUSAL_SPEED_SCALING.json'


def main():
    g=tower.levi_graph(); levels=[]
    for n in range(7):
        assert {len(a) for a in g}=={4}
        levels.append({'depth':n,'vertices':len(g),'local_degree':4,
                       'max_nearest_neighbor_graph_speed_edges_per_tick':1})
        if n<6:g,_=tower.fresh_connected_two_lift(g)

    fixed_volume_examples={}
    for d in (1,2,3,4):
        fixed_volume_examples[str(d)]={
            'ell_n_over_ell_0':f'2^(-n/{d})',
            'tau_n_over_tau_0_for_constant_c':f'2^(-n/{d})',
            'c_n_over_c_0_if_tau_fixed':f'2^(-n/{d})'
        }

    out={
      'pass':5682,
      'status':'COVER_TOWER_PRESERVES_GRAPH_CAUSAL_CONE_BUT_LEAVES_PHYSICAL_SPEED_CALIBRATION_FREE',
      'local_cover_fact':'every level is 4-regular and locally maps bijectively to the previous level',
      'nearest_neighbor_causal_bound':'Delta graph_distance <= 1 per discrete tick at every level',
      'physical_conversion':'c_n = ell_n/tau_n',
      'what_cover_fixes':['connectivity','sheet count','vertex and edge counts','local degree','graph-distance causal bound'],
      'what_cover_does_not_fix':['physical edge length ell_n','physical tick duration tau_n','spatial dimension d','SI value ell_0/tau_0'],
      'verified_levels':levels,
      'fixed_volume_refinement_if_assumed':fixed_volume_examples,
      'processor_speed_reading':'more cover sheets enlarge the internal state/history space but do not by themselves increase the one-edge-per-tick local information speed',
      'physics_conclusion':'A physical c can emerge only after an additional metric/time renormalization law fixes ell_n/tau_n. The graph topology alone supplies a dimensionless causal cone, not 299792458 m/s.',
      'physics_boundary':'This is a nearest-neighbour graph-causality statement. It is not a Lorentz-invariance proof or a derivation of the continuum metric.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
