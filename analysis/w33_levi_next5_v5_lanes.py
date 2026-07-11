#!/usr/bin/env python3
"""Compile 240 E8 roots into explicit 72+6+6x27 equivariant typed lanes."""
from __future__ import annotations
from functools import lru_cache
from collections import Counter
from itertools import combinations
import json, random
import networkx as nx
from pathlib import Path

from w33_levi_next5_v5_common import (
    compose_perm, e8_roots, find_e6_simple_roots, ip, orbit,
    reflection_perm, sha256_json,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_2026_07_11_LEVI_NEXT5_V5_lanes.json"


def classical_lines():
    labels=[f'E{i}' for i in range(6)]
    labels += [f'L{i}{j}' for i,j in combinations(range(6),2)]
    labels += [f'Q{i}' for i in range(6)]
    def intersects(a,b):
        if a==b:return False
        ka,kb=a[0],b[0]
        if ka==kb and ka in {'E','Q'}: return False
        if ka=='E' and kb=='L': return int(a[1]) in {int(b[1]),int(b[2])}
        if ka=='L' and kb=='E': return intersects(b,a)
        if ka=='E' and kb=='Q': return int(a[1])!=int(b[1])
        if ka=='Q' and kb=='E': return intersects(b,a)
        if ka=='L' and kb=='L': return not ({int(a[1]),int(a[2])}&{int(b[1]),int(b[2])})
        if ka=='L' and kb=='Q': return int(b[1]) in {int(a[1]),int(a[2])}
        if ka=='Q' and kb=='L': return intersects(b,a)
        raise AssertionError((a,b))
    G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in combinations(range(27),2):
        if intersects(labels[i],labels[j]):G.add_edge(i,j)
    assert set(dict(G.degree()).values())=={10}
    return labels,G


def graph_for_orbit(roots,orb):
    candidates=[]
    for val in (-1,0,1):
        G=nx.Graph();G.add_nodes_from(range(27))
        for i,j in combinations(range(27),2):
            if ip(roots[orb[i]],roots[orb[j]])==val:G.add_edge(i,j)
        candidates.append((val,G))
    return next((v,G) for v,G in candidates if set(dict(G.degree()).values())=={10})


def induced_perm_on_positions(gen,orb):
    idx={r:i for i,r in enumerate(orb)}
    return tuple(idx[gen[r]] for r in orb)


def set_digest(xs): return sha256_json([sorted(x) for x in xs])

@lru_cache(maxsize=1)
def analyze(seed=20260711):
    roots=e8_roots(); a2a=roots[0]; a2b=next(r for r in roots if ip(a2a,r)==-1)
    e6roots=[r for r in roots if ip(r,a2a)==0 and ip(r,a2b)==0]
    simple=find_e6_simple_roots(e6roots)
    gens=[reflection_perm(roots,a) for a in simple]
    unseen=set(range(240));orbits=[]
    while unseen:
        o=orbit(next(iter(unseen)),gens);orbits.append(o);unseen-=set(o)
    orbits=sorted(orbits,key=lambda o:(len(o),o[0]))
    fixed=[o[0] for o in orbits if len(o)==1]
    payload=[o for o in orbits if len(o)==27]
    control=next(o for o in orbits if len(o)==72)
    assert len(fixed)==6 and len(payload)==6 and len(control)==72
    labels,schlafli=classical_lines()

    lane_maps=[]; lane_graph_values=[]; lane_perms=[]
    for lane,orb in enumerate(payload):
        value,G=graph_for_orbit(roots,orb);lane_graph_values.append(value)
        mapping=next(nx.algorithms.isomorphism.GraphMatcher(G,schlafli).isomorphisms_iter())
        # mapping local orbit position -> classical line position
        inv={native:local for local,native in mapping.items()}
        slot_to_root=[orb[inv[s]] for s in range(27)]
        lane_maps.append(slot_to_root)
        perms=[]
        for g in gens:
            root_to_slot={r:s for s,r in enumerate(slot_to_root)}
            perms.append(tuple(root_to_slot[g[r]] for r in slot_to_root))
        lane_perms.append(perms)

    cpos={r:i for i,r in enumerate(control)}
    routes={}
    for lane,slot_roots in enumerate(lane_maps):
        for slot,ridx in enumerate(slot_roots):
            plus=[cpos[a] for a in control if ip(roots[ridx],roots[a])==1]
            minus=[cpos[a] for a in control if ip(roots[ridx],roots[a])==-1]
            zero=[cpos[a] for a in control if ip(roots[ridx],roots[a])==0]
            routes[(lane,slot)]={'root':ridx,'control_plus':sorted(plus),'control_minus':sorted(minus),'control_zero':sorted(zero)}
    route_counts=Counter((len(x['control_plus']),len(x['control_minus']),len(x['control_zero'])) for x in routes.values())

    fixed_ip=[[ip(roots[i],roots[j]) for j in fixed] for i in fixed]
    fixed_graph=nx.Graph();fixed_graph.add_nodes_from(range(6))
    for i,j in combinations(range(6),2):
        if fixed_ip[i][j]==1:fixed_graph.add_edge(i,j)
    fixed_degrees=sorted(dict(fixed_graph.degree()).values())

    # Generator-by-generator route equivariance.
    route_equiv=True; graph_equiv=True; lane_preservation=True
    control_perms=[induced_perm_on_positions(g,control) for g in gens]
    for gi,g in enumerate(gens):
        if any(g[r]!=r for r in fixed): lane_preservation=False
        for lane in range(6):
            p=lane_perms[lane][gi]
            for s in range(27):
                a=routes[(lane,s)]; b=routes[(lane,p[s])]
                if g[a['root']]!=b['root']: route_equiv=False
                if sorted(control_perms[gi][x] for x in a['control_plus'])!=b['control_plus']: route_equiv=False
                if sorted(control_perms[gi][x] for x in a['control_minus'])!=b['control_minus']: route_equiv=False
            for u,v in schlafli.edges():
                if not schlafli.has_edge(p[u],p[v]):graph_equiv=False

    # Each classical cubic line now has six parallel minuscule payload addresses.
    bundles=[]
    for slot in range(27):
        roots6=[lane_maps[l][slot] for l in range(6)]
        bundles.append({'slot':slot,'label':labels[slot],'roots':roots6})

    # State table for every E8 root.
    state=[None]*240
    for i,r in enumerate(control):state[r]={'kind':'E6_CONTROL','lane':0,'slot':i}
    for i,r in enumerate(fixed):state[r]={'kind':'A2_REFERENCE','lane':i,'slot':0}
    for lane,orbmap in enumerate(lane_maps):
        for slot,r in enumerate(orbmap):state[r]={'kind':'MINUSCULE_PAYLOAD','lane':lane,'slot':slot}
    assert all(x is not None for x in state)

    # Seeded replay smoke.  The exhaustive generator/object loops above are
    # the proof; this random walk is retained only as an integration regression.
    rng=random.Random(seed); current=rng.randrange(240); replay_ok=True; trace=[]
    for step in range(50000):
        gi=rng.randrange(6); nxt=gens[gi][current]
        a,b=state[current],state[nxt]
        if a['kind']!=b['kind'] or a['lane']!=b['lane']: replay_ok=False;break
        if step<32:trace.append((current,gi,nxt,a['kind'],a['lane']))
        current=nxt

    checks={
        'decomposition_72_6_6x27':sorted(map(len,orbits))==[1]*6+[27]*6+[72],
        'six_schlafli_complement_payload_lanes':all(v in (-1,0,1) for v in lane_graph_values) and all(len(m)==27 for m in lane_maps),
        'a2_reference_hexagon':fixed_degrees==[2]*6 and nx.is_connected(fixed_graph),
        'route_signature_16_16_40':route_counts==Counter({(16,16,40):162}),
        'generator_lane_preservation':lane_preservation,
        'generator_route_equivariance':route_equiv,
        'generator_schlafli_complement_equivariance':graph_equiv,
        'all_240_states_typed':len(state)==240 and all(x is not None for x in state),
        'seeded_replay_smoke_50k':replay_ok,
        'bundle_six_roots_per_line':all(len(set(b['roots']))==6 for b in bundles),
    }
    return {
        'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
        'lane_semantics':{
            'E6_CONTROL':{'count':72,'meaning':'reflection, syndrome-control, and double-six incidence lane'},
            'A2_REFERENCE':{'count':6,'meaning':'pointwise-fixed phase/clock/reference hexagon'},
            'MINUSCULE_PAYLOAD':{'lanes':6,'slots_per_lane':27,'meaning':'six parallel degree-10 complement-Schlaefli payload lanes'},
        },
        'decomposition':{'orbit_sizes':sorted(map(len,orbits)),'fixed_root_indices':fixed,'control_root_indices':control,'payload_root_indices':payload},
        'routing':{
            'payload_addresses':162,'control_fanout_per_payload':{'plus':16,'minus':16,'orthogonal':40},
            'classical_line_bundles':bundles,
            'route_digest':sha256_json({f'{l}:{s}':x for (l,s),x in routes.items()}),
            'state_digest':sha256_json(state),'generator_digest':sha256_json(gens),
            'lane_permutation_digest':sha256_json(lane_perms),
        },
        'a2_reference':{'inner_product_matrix':fixed_ip,'cycle_edges':sorted(tuple(sorted(x)) for x in fixed_graph.edges())},
        'seeded_replay_smoke':{
            'steps':50000,'passed':replay_ok,'trace_digest':sha256_json(trace),
            'proof_strength':'none beyond the exhaustive generator/object equivariance checks',
        },
        'theorem':(
            'The complete E8 carrier is compiled into 72 typed E6 control states, a pointwise-fixed six-state A2 '
            'reference hexagon, and six 27-state payload lanes carrying SRG(27,10,1,5), the complement '
            'of the conventional Schlaefli graph SRG(27,16,10,8). Every W(E6) simple reflection preserves '
            'lane identity, complement-Schlaefli adjacency, and the exact 16+/16-/40-orthogonal routing relation.'
        ),
        'scope_boundary':(
            'The six payload lanes are canonically typed and individually identified with the '
            'degree-10 intersection graph, i.e. the complement of the conventional Schlaefli graph. '
            'Choosing one physical naming alignment across all six remains a calibration convention. '
            'The seeded 50k replay is a smoke test; exhaustive generator equivariance is the certificate.'
        )
    }

def main():
    out=analyze();text=json.dumps(out,indent=2,sort_keys=True)+"\n"
    OUT.write_text(text,encoding="utf-8");print(text,end="")
    return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
