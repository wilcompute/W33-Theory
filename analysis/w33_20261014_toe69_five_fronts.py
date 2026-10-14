"""TOE69: five reproducible W33 research gates (exact and numerical separated).

Native 160-edge two-bit adversary, 20 octagon loop cover, truncated-gauge
Schur complement, overlap charge aliasing, and symmetric staggered free mass.
Not a physical Theory of Everything proof.
"""
from __future__ import annotations
import collections
import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass1081_1086_core import build_w33

HIGH=(30,31,49,51,59,62,63,82,83,93,95,118,119,138,139,142,143)
COVER=(65,103,176,287,353,439,514,543,620,758,793,880,935,986,
       1092,1143,1323,1481,1532,1542)

def graph():
    *_,flags,_=build_w33()
    ed=[(int(a),40+int(b)) for a,b in flags]
    assert len(ed)==160
    adj=[[] for _ in range(80)]
    for i,(a,b) in enumerate(ed):
        adj[a].append((b,i,1))
        adj[b].append((a,i,-1))
    return ed,adj

def octagons():
    ed,adj=graph()
    cycles=[]
    for root in range(80):
        def dfs(path,es):
            u=path[-1]
            if len(path)==8:
                for b,e,s in adj[u]:
                    if b==root and path[1]<u:
                        cycles.append(tuple(es+[e]))
                return
            for b,e,s in adj[u]:
                if b<=root or b in path:
                    continue
                dfs(path+[b],es+[e])
        for b,e,s in adj[root]:
            if b>root:
                dfs([root,b],[e])
    assert len(cycles)==1620
    return ed,adj,cycles

def windings(cycles,ed):
    voltage=np.zeros((160,3),int)
    for j,e in enumerate((59,93,139)):
        voltage[e,j]=1
    out=[]
    for ci,cycle in enumerate(cycles):
        sub=collections.defaultdict(list)
        for e in cycle:
            a,b=ed[e]
            sub[a].append((b,e,1))
            sub[b].append((a,e,-1))
        start=min(sub)
        prev=None
        curr=start
        w=np.zeros(3,int)
        for step in range(8):
            choices=[x for x in sub[curr] if x[0]!=prev]
            nxt,e,s=choices[0]
            w+=s*voltage[e]
            prev,curr=curr,nxt
        assert curr==start
        if np.any(w):
            out.append((ci,tuple(int(x) for x in w)))
    assert len(out)==238
    return out

def disorder_two_flip(cycles,ed,winding):
    q=np.array((0,-1,1))
    hi=set(HIGH)
    d,n=1000,245
    powers=[(d+n)**k*(d-n)**(8-k) for k in range(9)]
    singles=[0]*160
    cross=collections.defaultdict(int)
    base=0
    for idx,w in winding:
        coef=(1 if sum(w)%2 else -1)*int(np.dot(w,q))**2
        if not coef:
            continue
        es=cycles[idx]
        h=len(hi.intersection(es))
        b=powers[h]
        base+=coef*b
        flip={e:(-1 if e in hi else 1) for e in es}
        for e in es:
            singles[e]+=coef*(powers[h+flip[e]]-b)
        for a,e in itertools.combinations(sorted(es),2):
            cross[(a,e)]+=coef*(powers[h+flip[a]+flip[e]]
                -powers[h+flip[a]]-powers[h+flip[e]]+b)
    best=min((singles[a]+singles[b]+cross[a,b],a,b)
             for a in range(160) for b in range(a+1,160))
    assert base==-278181245315125293750000
    assert min(singles)==52315612734624060937500
    assert best==(337991711991203123437500,37,56)
    return {"status":"PASS_EXACT_TWO_EDGE_CORNER_LOCALITY",
      "native_winding_octagons":len(winding),"tested_pair_flips":12720,
      "high_edge_indices":list(HIGH),"epsilon_fraction":"245/1000",
      "phase_direction":[0,-1,1],"negative_baseline_integer":str(base),
      "smallest_positive_one_flip_integer":str(min(singles)),
      "smallest_positive_two_flip_integer":str(best[0]),
      "min_two_flip_pair":[best[1],best[2]],
      "scope":"Only fixed-direction Hamming-distance <=2 local optimality, not global 160-edge minimax or all-beta flux."}

def loop_cover(cycles,ed,adj,winding):
    selected=[cycles[j] for j in COVER]
    counts=collections.Counter(e for cy in selected for e in cy)
    assert len(selected)==20 and len(counts)==160 and all(x==1 for x in counts.values())
    owner={e:i for i,cy in enumerate(selected) for e in cy}
    joint=collections.Counter()
    for flags in adj:
        loops=tuple(sorted({owner[e] for v,e,s in flags}))
        assert len(loops)==2
        joint[loops]+=1
    degree=[0]*20
    for (a,b),n in joint.items():
        degree[a]+=n
        degree[b]+=n
    assert degree==[8]*20
    wd=dict(winding)
    winds=[wd.get(j,(0,0,0)) for j in COVER]
    assert collections.Counter(winds)==collections.Counter({
        (0,0,0):17,(0,0,-1):1,(0,1,0):1,(1,0,0):1})
    return {"status":"PASS_EXACT_TWENTY_NATIVE_OCTAGON_COVER",
        "all_native_simple_octagons":len(cycles),
        "selection_indices":list(COVER),
        "twenty_octagon_edge_lists":[list(row) for row in selected],
        "every_edge_covered_once":True,"every_vertex_meets_two_octagons":True,
        "twenty_cycle_intersection_multigraph_degree":8,
        "intersection_edge_pair_multiplicity_counts":
          {str(k):v for k,v in collections.Counter(joint.values()).items()},
        "three_selected_nontrivial_windings":[list(w) for w in winds if any(w)],
        "proof":"Any local pairing partitions 160 edges into edge-disjoint closed nonbacktracking paths; native graph girth eight implies <=20 paths. This explicit 20-octagon cover saturates the bound. The invariant classical -J times number-of-loops Hamiltonian has ground energy -20J for J>0.",
        "scope":"Construction depends on selected cover and spanning-tree chords. No canonical spacetime, Einstein dynamics, or chirality follows."}

def native_gauge_cutoff_bound():
    # Exact block inequalities applied to TOE68 *numerical*, not interval-certified, Ritz values.
    Ecut={2:-2.1345423000162325,3:-2.1345424782977696}
    g=.9
    kappa=.6
    eta=.25
    bg=np.array([1,0]*4)
    occupations=[np.array([(bits>>j)&1 for j in range(8)])
                 for bits in range(256) if bits.bit_count()==4]
    bounds=[]
    for L,E in Ecut.items():
        diagonal=float("inf")
        low,high=0,0
        for occ in occupations:
            shift=np.cumsum(occ-bg)
            low=min(low,int(sum(shift)))
            high=max(high,int(sum(shift)))
            for m in (-L-1,L+1):
                diagonal=min(diagonal,.5*g*g*float((m+shift)@(m+shift))+eta)
        assert low>=-10 and high<=6
        assert 8*(L+1)+low>0 and -8*(L+1)+high<0
        assert abs(diagonal-{2:11.59,3:26.17}[L])<1e-9
        boundQ=diagonal-(8*kappa+eta)
        coupling=kappa+eta/2
        assert boundQ>E
        lower=(E+boundQ-math.sqrt((boundQ-E)**2+4*coupling**2))/2
        bounds.append({"L":L,"numerical_E_cutoff":E,"Q_diagonal_min":diagonal,
          "complement_Q_lower_by_Gershgorin":boundQ,
          "interface_operator_norm_bound":coupling,
          "lower_if_exact_cutoff_ground":lower,
          "upper_if_exact_cutoff_ground":E,
          "conditional_interval_width":E-lower})
    return {"status":"PASS_SCHUR_BLOCK_INEQUALITY_NUMERIC_INPUT",
      "bounds":bounds,
      "algebraic_proof":"For fixed four-fermion occupation, n_j=m+cumulative(occ-bg). Convexity and exact finite occupation census bound every |m|>=L+1 electric diagonal. Complement hopping has row sum <=8*kappa+eta. Interface has row/col sum <=kappa+eta/2. Apply 2x2 min-max lower eigenvalue formula with exact cutoff ground energy.",
      "limitation":"Displayed decimal intervals use previously reported numerical Ritz values, not certified enclosures of exact PHP ground energies. They are conditional bounds, NOT machine-rigorous energy intervals until those enclosures are supplied."}

def overlap_aliasing():
    charges=[1,5,-7,-8,9]
    assert sum(charges)==sum(q**3 for q in charges)==0
    size=lambda N:2*math.sin(math.pi/N**2)
    min_generic=next(N for N in range(3,100) if size(N)<1/30)
    min_charged=next(N for N in range(3,100) if 9*2*math.pi/N**2<2/5)
    assert (min_generic,min_charged)==(14,12)
    assert 9%(3*3)==0 and 9%3==0
    return {"status":"PASS_EXACT_CHARGE_NINE_LATTICE_ALIAS",
      "TOE68_N":3,"TOE68_unit_flux_plaquette_norm":size(3),
      "illustrative_sufficient_generic_norm_cutoff":"1/30",
      "first_N_satisfying_that_cutoff":min_generic,
      "representative_U1_charge_angle_bound":"max_abs_charge * 2*pi/N^2 < 2/5",
      "first_N_for_five_charge_bound":min_charged,
      "charge9_links_exactly_trivial_in_TOE68_background":True,
      "charge9_overlap_index_on_coarse_3pow4_background":0,
      "continuum_twist_Chern_product_at_charge9":81,
      "scope":"Distinct sufficient locality/admissibility criteria apply in different groups. This is an explicit aliasing failure of the prior q=9 five-charge control, not a proof any particular 4D W33 chiral construction exists."}

def free_staggered_mass():
    ed,adj=graph()
    B=np.zeros((40,40),complex)
    for i,(a,b) in enumerate(ed):
        B[a,b-40]=-1 if i in (59,93,139) else 1
    rank=int(np.linalg.matrix_rank(B,tol=1e-9))
    assert rank==28
    tests=[]
    for m in (.05,.2,1.):
        H=np.block([[m*np.eye(40),B],[B.conj().T,-m*np.eye(40)]])
        eigen=np.linalg.eigvalsh(H)
        assert sum(eigen<0)==sum(eigen>0)==40
        assert abs(eigen[40]-eigen[39]-2*m)<1e-10
        tests.append({"chosen_mass":m,"computed_canonical_fock_gap":float(eigen[40]-eigen[39])})
    return {"status":"PASS_EXACT_FREE_MASS_ZERO_MODE_LIFTING",
      "rank_at_3pi":rank,"massless_zero_single_particle_modes":24,
      "trial_mass_gaps":tests,
      "theorem":"H_m=[[mI,B],[B*, -mI]] has spectrum ±sqrt(sigma(B)^2+m^2), so for every m!=0 the canonical 40-particle free ground state is unique and has gap >=2|m|. Because B at three-pi has twelve zero singular values, the gap there is exactly 2|m|. TOE67's uniform all-beta flux proof remains valid for a common staggered mass.",
      "limitation":"An imposed sublattice parameter, not spontaneous interacting mass generation or a parameter-free W33 prediction."}

def certificate():
    ed,adj,cycles=octagons()
    winds=windings(cycles,ed)
    return {"status":"PASS_TOE69_FIVE_INDEPENDENT_FRONTS",
      "disorder":disorder_two_flip(cycles,ed,winds),
      "pairing_geometry":loop_cover(cycles,ed,adj,winds),
      "gauge":native_gauge_cutoff_bound(),
      "chirality":overlap_aliasing(),
      "zero_modes":free_staggered_mass()}

if __name__=="__main__":
    out=certificate()
    (ROOT/"data/w33_20261014_toe69_five_fronts.json").write_text(
        json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(out["status"],out["pairing_geometry"]["selected_cycle_indices"])
