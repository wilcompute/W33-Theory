#!/usr/bin/env python3
"""Is the 30-mode W33 flat band distinguishable from graph regularity alone?

Compare 40x40 row/column-4 incidence to one connected circulant and
128 seeded connected simple random 4-regular bipartite graphs.
W33's 30 modes are NOT solely degree regularity; but neither are they
a unique physical/topological invariant or a TOE explanation.
"""
import json,sys,math
from pathlib import Path
import numpy as np
import networkx as nx
from w33_20261109_flux_dark_mode_fragility import build

def connected(M):
    G=nx.Graph()
    G.add_nodes_from(range(80))
    G.add_edges_from((i,40+j) for i,j in zip(*np.nonzero(M)))
    return nx.is_connected(G)

def sample(rng,max_retries=4000):
    # configuration of four perfect matchings with no repeated edge
    # creates simple 4-regular bipartite graph, not a uniform 4-regular
    # graph sampler. Distinguish sampling method from random graph law.
    for attempt in range(max_retries):
        M=np.zeros((40,40),int)
        for i in range(4):
            p=rng.permutation(40)
            M[np.arange(40),p]+=1
        if M.max()!=1:continue
        if connected(M):return M
    raise RuntimeError("Unable to sample simple connected graph")

def rank(M):return int(np.linalg.matrix_rank(M,tol=1e-9))
def main(path=None):
    W,edges,G=build()
    c=np.zeros((40,40),int)
    for i in range(40):
        for j in range(4):c[i,(i+j)%40]=1
    assert connected(c)
    assert rank(c)==37
    assert c.sum()==160 and np.all(c.sum(axis=1)==4) and np.all(c.sum(axis=0)==4)
    rng=np.random.default_rng(202611092111)
    sample_count=128
    ranks=[rank(sample(rng)) for _ in range(sample_count)]
    assert len(ranks)==sample_count
    assert rank(W)==25
    # W33 30 null modes cannot be explained by degree-4 alone.
    assert all(x>25 for x in ranks)
    out={"status":"PASS_W33_DARK_MODES_NOT_EXPLAINED_BY_DEGREE_REGULARITY",
     "native_W33":{"points":40,"lines":40,"incidences":160,"degree_each":4,
           "incidence_rank":25,"zero_modes_of_80_chiral_walk":30},
     "connected_four_consecutive_cyclic_hopping":{
           "incidences":160,"degree_each":4,"rank":rank(c),
           "zero_modes_of_80_chiral_walk":80-2*rank(c)},
     "random_configuration_sampler":{
           "type":"four independent random perfect matchings conditioned on no multiedges and connectedness; not uniform on all connected regular bipartite graphs",
           "seed":202611092111,"sampled_graphs":sample_count,
           "incidence_rank_min":int(min(ranks)),
           "incidence_rank_max":int(max(ranks)),
           "rank_histogram":{str(i):ranks.count(i) for i in sorted(set(ranks))},
           "equal_or_exceed_W33_flat_band_count":int(sum(r<=25 for r in ranks))},
     "scientific_interpretation":"W33's large 15+15 flat sector depends on its highly constrained geometry and not solely having 40+40 vertices with degree four. This does not prove W33 is uniquely identifiable by the 30-mode spectrum; many other nonisomorphic graphs can share spectral features. A useful lab falsifier must measure more than one bulk number, e.g. the 40-state Gram signature and gauge-flux robustness.",
     "scope":"Seeded graph controls, not systematic enumeration of nonisomorphic 4-regular graphs. No claim of uniqueness, phase continuum, gravity, SM masses, or experimental observation."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("REGULAR_CONTROL",json.dumps({"W33_rank":25,"cyclic_rank":37,
        "random_hist":out["random_configuration_sampler"]["rank_histogram"]}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
