#!/usr/bin/env python3
"""An H4 gauge-covariant pi-flux on 120 inter-E8 four-cycles.

Double-E8 sheets are the two index-five glues of 25x60 packet
A4⊕A4 kernel. Each of 120 antipodal-root-line sectors is a C4
with two symmetric interlayer flip maps. For zero flux the
interlayer adjacency A satisfies A^3=4A and has 240 zero modes.

Put one negative hopping on each square: gauge-invariant Wilson
flux=-1, signed adjacency S satisfies EXACTLY S^2=2 I.
No zero modes; U= -i S/sqrt2 at time pi/(2sqrt2)
puts each root state into a coherent superposition of its two
opposite-sheet neighbors and squares to -I.

Raw coupler signs need not be H4 invariant, but all generators
are *gauge-covariant*: explicit vertexwise ±1 gauges conjugate
the transported sign pattern to original. On each C4 gauge
holonomy is complete invariant; uniform pi flux is full-H4
invariant as a GAUGE EQUIVALENCE CLASS.

The local graph is 120 disconnected plaquettes. It is not a
universal time-entangling photon experiment or dynamics on W33.
"""
from __future__ import annotations
import collections,itertools,json,math,sys
from pathlib import Path
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/"analysis") not in sys.path:sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261104_reye_kernel_a4a4_e8_glue import roots_scaled5
OUT=ROOT/"data"/"toe_20261104_two_e8_pi_flux_gauge_frame.json"
def flip1(v):return tuple(-x for x in v[:5])+v[5:]
def flip2(v):return v[:5]+tuple(-x for x in v[5:])
def swap(v):return v[5:]+v[:5]
def change(v,p,side):
    out=list(v)
    for i in range(5):out[5*side+p[i]]=v[5*side+i]
    return tuple(out)
def ed(u,v):return tuple(sorted((u,v)))
def main():
    plus=sorted(set(roots_scaled5(2)))
    minus=sorted(set(roots_scaled5(3)))
    assert len(plus)==len(minus)==240
    ixplus={v:i for i,v in enumerate(plus)}
    ixminus={v:240+i for i,v in enumerate(minus)}
    G=nx.Graph()
    G.add_nodes_from(range(480))
    for i,v in enumerate(plus):
        G.add_edge(i,ixminus[flip1(v)])
        G.add_edge(i,ixminus[flip2(v)])
    assert G.number_of_edges()==480
    comps=sorted((sorted(c) for c in nx.connected_components(G)))
    assert len(comps)==120 and all(len(c)==4 for c in comps)
    all_edges={ed(u,v) for u,v in G.edges()}
    assert len(all_edges)==480
    # Unoriented Z2 Wilson loop each C4.
    sign={e:1 for e in all_edges}
    one_negative=[]
    for c in comps:
        links=sorted(ed(u,v) for u,v in itertools.combinations(c,2) if G.has_edge(u,v))
        assert len(links)==4
        sign[links[0]]=-1
        one_negative.append(links[0])
        assert math.prod(sign[e] for e in links)==-1
    A=np.zeros((480,480),dtype=np.int16)
    A0=nx.to_numpy_array(G,nodelist=range(480),dtype=np.int16)
    for (u,v),sgn in sign.items():
        A[u,v]=A[v,u]=sgn
    assert np.array_equal(A@A,2*np.eye(480,dtype=np.int16))
    assert not np.any(A0@A0@A0-4*A0)
    assert min(abs(np.linalg.eigvalsh(A.astype(float))))>1.0
    # Fourier data follows from quadratic polynomial and trace0:
    # ±sqrt2 each multiplicity240, and determinant (+/-) follows.
    assert np.trace(A)==0
    # One-tick U=-i A/sqrt(2), exact up to floating-point norm.
    basis=np.eye(480,dtype=complex)[:,0]
    evolved=(-1j/math.sqrt(2))*A@basis
    assert np.count_nonzero(abs(evolved)>1e-12)==2
    assert np.max(abs(np.abs(evolved)[abs(evolved)>1e-12]-1/math.sqrt(2)))<1e-12
    assert np.linalg.norm(evolved[:240])<1e-12
    assert abs(np.linalg.norm(evolved)-1)<1e-12
    assert np.linalg.norm(((-1j/math.sqrt(2))*A)@evolved + basis)<1e-12

    # Full effective H4 packet symmetry: (A5xA5)⋊C2.
    c5=(1,2,3,4,0);c3=(1,2,0,3,4)
    generators=[]
    for side in (0,1):
        for p in (c5,c3):
            img=tuple((ixplus if s==0 else ixminus)[change(v,p,side)]
              for s,rset in enumerate((plus,minus)) for v in rset)
            generators.append(img)
    generators.append(tuple((ixminus if s==0 else ixplus)[swap(v)]
       for s,rset in enumerate((plus,minus)) for v in rset))
    assert len(generators)==5
    for perm in generators:
        assert {ed(perm[u],perm[v]) for u,v in all_edges}==all_edges
    def gauge_for_generator(perm):
        # For original sign s_e and permutation g, define eta on
        # destination endpoints: eta[g(u)]*eta[g(v)]=s_e*s_{g(e)}.
        # Consistency on each 4-cycle follows from fixed Wilson flux.
        adj=[[] for _ in range(480)]
        for u,v in all_edges:
            x,y=perm[u],perm[v]
            bit=(sign[ed(u,v)]!=sign[ed(x,y)])
            adj[x].append((y,bit))
            adj[y].append((x,bit))
        bits=[None]*480
        for root in range(480):
            if bits[root] is not None:continue
            bits[root]=0
            stack=[root]
            while stack:
                u=stack.pop()
                for v,b in adj[u]:
                    want=bits[u]^int(b)
                    if bits[v] is None:bits[v]=want;stack.append(v)
                    else:assert bits[v]==want
        assert all(x in (0,1) for x in bits)
        for u,v in all_edges:
            x,y=perm[u],perm[v]
            assert sign[ed(x,y)]==sign[ed(u,v)]*(-1)**(bits[x]+bits[y])
        return bits
    gauges=[gauge_for_generator(perm) for perm in generators]
    change_counts=[sum(x) for x in gauges]
    # Reconstruct signed A after each generator's permutation and
    # vertexwise gauge twist, verifying the projective symmetry lift.
    for perm,bits in zip(generators,gauges):
        for u,v in all_edges:
            assert A[perm[u],perm[v]]*((-1)**bits[perm[u]])*((-1)**bits[perm[v]])==A[u,v]
    # Strict edge-orbit ± assignments cannot produce pi flux if
    # every C4 meets each edge orbit evenly. Construct edge orbits.
    unseen=set(all_edges);orbits=[]
    while unseen:
        seed=min(unseen);orbit={seed};todo=[seed]
        while todo:
            u,v=todo.pop()
            for p in generators:
                e=ed(p[u],p[v])
                if e not in orbit:orbit.add(e);todo.append(e)
        assert orbit<=unseen
        unseen-=orbit;orbits.append(orbit)
    assert sum(map(len,orbits))==480
    parity_hist=collections.Counter()
    all_parity_zero=True
    for c in comps:
        edges={ed(u,v) for u,v in itertools.combinations(c,2) if G.has_edge(u,v)}
        n=tuple(len(edges&o)%2 for o in orbits)
        parity_hist[str(n)]+=1
        if any(n):all_parity_zero=False
    # The edge orbits yield a sharper selection: the 20 C4 squares
    # whose roots are in the common A4+A4 shell each meet every
    # strict-H4 edge orbit EVENLY, and therefore CANNOT acquire
    # pi-flux under a literally invariant signed-edge assignment.
    # The other 100 squares can acquire pi under a single negative
    # size-100 orbit. This leaves 40 dark states (2 per trivial C4).
    assert sorted(map(len,orbits))==[40,40,100,100,100,100]
    parity_records=[]
    for c in comps:
        links={ed(u,v) for u,v in itertools.combinations(c,2) if G.has_edge(u,v)}
        par=tuple(len(links&o)%2 for o in orbits)
        parity_records.append((c,par,links))
    assert collections.Counter(str(pr) for _,pr,_ in parity_records)=={
      str((0,0,0,0,0,0)):20,str((0,0,1,1,1,1)):100}
    common_root_set=(set(plus)&set(minus))
    assert len(common_root_set)==40
    for c,par,_ in parity_records:
        is_common=plus[next(v for v in c if v<240)] in common_root_set
        assert is_common==(not any(par))
    orbit100=next(o for o in orbits if len(o)==100)
    strict_sign={e:(-1 if e in orbit100 else 1) for e in all_edges}
    assert all(all(strict_sign[ed(g[u],g[v])]==strict_sign[ed(u,v)]
                   for u,v in all_edges) for g in generators)
    strict_flux=collections.Counter()
    As=np.zeros((480,480),dtype=np.int16)
    for (u,v),sgn in strict_sign.items():As[u,v]=As[v,u]=sgn
    for c,par,links in parity_records:
        fl=math.prod(strict_sign[e] for e in links)
        strict_flux[fl]+=1
        assert (fl==1)==(not any(par))
    assert strict_flux=={1:20,-1:100}
    # Each +1 C4 contributes +/-2 eigen and TWO exact zero modes;
    # each pi C4 contributes +-sqrt2 twice, no zeros.
    for c,par,_ in parity_records:
        B=As[np.ix_(c,c)].astype(np.int64)
        if any(par):
            assert np.array_equal(B@B,2*np.eye(4,dtype=np.int64))
        else:
            assert np.array_equal(B@B@B,4*B)
    strict_dark_dimension=2*strict_flux[1]
    assert strict_dark_dimension==40
    result=dict(status="PASS_120_C4_PI_FLUX_H4_GAUGE_COVARIANT_EXACT_INVOLUTION",
        interlayer_root_modes=480,components=120,vertices_per_component=4,
        interlayer_signed_edges=480,one_negative_edge_per_C4=120,
        all_wilson_fluxes_minus_one=True,
        ordinary_zero_flux_graph_exact_poly="A0^3=4A0",
        ordinary_zero_flux_spectrum={"-2":120,"0":240,"2":120},
        pi_flux_graph_exact_poly="A_pi^2=2I480",
        pi_flux_spectrum={"-sqrt2":240,"sqrt2":240},
        pi_flux_has_no_zero_eigenmodes=True,
        pi_flux_one_tick_U="-i A_pi/sqrt2 (evolution time pi/(2sqrt2) at unit signed hopping)",
        one_tick_single_root_to_two_opposite_sheet_neighbor_equal_probabilities=[.5,.5],
        two_ticks_minus_identity=True,
        full_H4_packet_generators_count=5,
        all_generators_gauge_covariant=True,
        gauge_minus_sign_counts_per_generator=change_counts,
        H4_interlayer_edge_orbit_sizes=sorted(map(len,orbits)),
        per_C4_orbit_edge_intersection_parity_patterns=dict(parity_hist),
        strict_edge_orbit_signs_force_zero_flux=all_parity_zero,
        strict_full_H4_signed_edge_pi_flux_possible_on_all_120_C4=False,
        strict_full_H4_edge_orbits_count=len(orbits),
        strict_full_H4_20_common_A4_C4_forced_trivial_flux=True,
        strict_full_H4_100_noncommon_E8_glue_C4_allow_pi_flux=True,
        strict_full_H4_partial_pi_flux_squares=100,
        strict_full_H4_partial_zero_flux_squares=20,
        strict_full_H4_partial_flux_residual_zero_modes=strict_dark_dimension,
        strict_full_H4_partial_flux_exact_spectrum={
          "-2":20,"0":40,"2":20,"-sqrt2":200,"sqrt2":200},
        strict_full_H4_partial_pi_flux_verified_by_edge_orbit_signs=True,
        unexpected_40_mode_sector_warning="20 common A4 root-line C4 each have 2 dark vectors => 40D interlayer-only kernel. It is NOT a canonical W33 40-ray representation: full H4->W33 graph action is obstructed by the independent 5-adic group-order theorem.",
        distinction="Gauge-invariant pi Wilson flux may preserve H4 UP TO LOCAL Z2 GAUGE even if no literal edge-sign assignment is strictly H4 invariant. The actual local gauge lifts have been constructed for all 5 symmetry generators.",
        full_graph_warning="120 disconnected squares, no root-shell mixing across distinct C4 components; 480 optical modes are far more than the proposed 40-mode Witting readout. Combining an all-positive 56-regular intra-sheet E8 root graph with this fixed gauge choice may invalidate these same gauge lifts and must be audited separately.",
        physical_limit="Ideal signed 480-mode tight-binding graph, not realized photons, physical single-time/temporal entanglement, measured flux, natural W33 map or Lorentzian TOE. Z2 gauge equivalence here is combinatorial; no local gauge dynamical field has been built.",
        novelty_boundary="Flux pi signed C4 spectra are standard. This is a concrete full-H4 gauge-covariant construction on the NEW two-glue interlayer geometry, whose 120 squares derive from the packet incidence kernel."
    )
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(result["status"],"edge orbit sizes",result["H4_interlayer_edge_orbit_sizes"],
         "strict noflux",all_parity_zero,"gauge",change_counts,flush=True)
    return result
if __name__=="__main__":main()
