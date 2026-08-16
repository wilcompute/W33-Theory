#!/usr/bin/env python3
"""Pass5687: metric/clock renormalization on the cover tower and an expander obstruction.

Pass5624 gives the split-step Dirac conversion c=ell/tau and O(a) finite-step
anisotropy. Pass5683 gives an existential 4-regular Ramanujan 2-lift tower.

If N_n=N_0 2^n cells are interpreted as a refinement of a fixed d-dimensional
physical volume, uniform cell length must scale
    ell_n/ell_0 = 2^{-n/d}.
Keeping one physical causal speed requires the clock to scale identically,
    tau_n/tau_0 = 2^{-n/d},
so c_n=ell_n/tau_n is constant.  If the split-step parameter a follows the same
refinement scale, its first-order lattice artifact decays as 2^{-n/d}.

But the Ramanujan tower has a uniform normalized spectral gap and hence a uniform
conductance lower bound: it is an expander.  A graph metric with nonvanishing
macroscopic conductance is not a local finite-dimensional manifold refinement,
where boundary/volume ratios of large physical regions shrink with resolution.
Thus the balanced cover tower is excellent as an internal routing/state network,
but its graph adjacency cannot simply be declared physical space.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5687_METRIC_CLOCK_EXPANDER_NO_SPACETIME.json'

def main():
    dreg=4;ram=2*math.sqrt(3)
    comb_gap=dreg-ram
    norm_gap=1-ram/dreg
    cheeger_lower=norm_gap/2 # standard easy side for normalized Laplacian
    assert comb_gap>0 and norm_gap>0
    rows=[]
    for d in range(1,7):
        r=2**(-1/d)
        rows.append({'dimension':d,'ell_step_ratio':r,'tau_step_ratio_for_fixed_c':r,'first_order_split_step_error_ratio':r})
    r3=2**(-1/3)
    assert abs(rows[2]['ell_step_ratio']-r3)<1e-15
    out={
      'pass':5687,'status':'FIXED_VOLUME_METRIC_CLOCK_SCALING_IS_CONDITIONAL_AND_RAMANUJAN_GRAPH_METRIC_IS_NOT_MANIFOLDLIKE',
      'cover_counts':'N_n=N_0 2^n',
      'conditional_fixed_volume_law':'ell_n/ell_0 = 2^{-n/d}',
      'fixed_speed_clock_law':'tau_n/tau_0 = 2^{-n/d}, hence c_n=ell_n/tau_n=c_0',
      'split_step_compatibility':'If the Pass5624 lattice parameter a scales with ell and tau in natural units, its O(a) anisotropy/error decays by 2^{-1/d} per cover level.',
      'dimension_table':rows,
      'd3_example':{'per_level_scale':r3,'after_3_levels':0.5},
      'ramanujan_network':{'degree':4,'adjacency_bound':ram,'combinatorial_gap_lower':comb_gap,'normalized_gap_lower':norm_gap,'cheeger_conductance_lower':cheeger_lower},
      'obstruction':'A uniform-expansion graph metric does not have the shrinking macroscopic boundary/volume behavior of a local fixed-dimensional manifold refinement. The Ramanujan tower should not be identified with physical space by graph distance alone.',
      'physics_conclusion':'The repo can consistently keep c fixed under a chosen d-dimensional volume refinement only by co-scaling spatial length and clock time. Neither d nor the absolute calibration is fixed by the cover topology; the expander result instead favors interpreting the tower as internal routing/state refinement.',
      'boundary':'No Lorentz-invariant spacetime limit, physical value of c, or preferred dimension is derived. The manifold comparison uses standard spectral-expander/Cheeger facts and is a structural obstruction to the naive graph-distance reading.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
