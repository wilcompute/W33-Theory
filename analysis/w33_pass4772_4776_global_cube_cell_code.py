#!/usr/bin/env python3
"""Passes 4772 and 4776 — global coupling of the 135 router cells and cube identification.

Pass4776 first proves that the 135 Pass4748 fifteen-edge coding cells and the
135 Pass4758 dependency cubes are literally the same PSp G-set.  For each cube,
its six residues map to the six selected270 vertices incident with one selected135
vertex.  The cube cold graph is K6-3K2; the three missing pairs are exactly the
three Petersen-hot edges.  Completing them gives the physical K6 cell, while the
remaining twelve edges split into the three K2,2 cold blocks of Pass4748.

Pass4772 uses that intrinsic K6 description to globally couple the local
[15,3,7]_2 cells.  The three local logical generators are indexed equivariantly
by the three quotient GQ lines through the cell's packet.  Thus the 405 logical
coordinates partition into 27 groups of 15.  One even-parity constraint per
line gives [2025,378,14]_2 exactly.  The repetition choice on every 15-group gives
[2025,27,105]_2.  Both are PGSp-invariant constructions.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle

ROOT=Path(__file__).resolve().parents[1]
OUT2=ROOT/'data/PART_W33_PASS4772_GLOBAL_CROSSFIBER_CODE.json'
OUT6=ROOT/'data/PART_W33_PASS4776_CUBE_CELL_EQUIVARIANT_IDENTIFICATION.json'

def pmask(m,p):
    y=0
    for i in range(40):
        if (int(m)>>i)&1:y|=1<<p[i]
    return y

def gf2_rank(vals):
    piv={}
    for x in vals:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def main():
    D=build_all();B=build_bundle()
    rm=D['rmasks'];U=D['cube_unions'];cubeR=D['cube_residues'];G=D['G'];sel=D['selected270'];sing=D['selected135'];N=np.asarray(D['selected_incidence'])
    phiU=D['phiU'];phiR=D['phiR'];assert len(U)==135 and len(sel)==270 and N.shape==(135,270)
    hot={tuple(sorted(e)) for e in B['hot']};cold={tuple(sorted(e)) for e in B['cold']};router=hot|cold
    K5=B['K5'];projected=B['projected'];packets=B['packets']
    assert len(hot)==405 and len(cold)==1620 and len(router)==2025
    # Reassociate sorted cube unions with their six residue sets.
    union_to_R={}
    for R in cubeR:
        u=0
        for r in R:u|=rm[r]
        union_to_R[u]=tuple(R)
    assert set(union_to_R)==set(U)

    owner=[]
    for T in projected:
        hit=[i for i,S in enumerate(K5) if set(T)<=S];assert len(hit)==1;owner.append(hit[0])
    packet_of_s={s:p for p,T in enumerate(packets) for s in T}
    coord_of_s={(p,s):i for p,T in enumerate(packets) for i,s in enumerate(T)}
    assert len(packet_of_s)==135

    # Literal cube -> selected135 cell check.
    cells={};cold_missing_profiles=[]
    for ui,u in enumerate(U):
        s=phiU[ui];R=union_to_R[u];mapped={phiR[r] for r in R};inc=set(np.flatnonzero(N[s]).tolist())
        assert len(R)==len(mapped)==len(inc)==6 and mapped==inc
        allpairs={tuple(sorted(e)) for e in itertools.combinations(sorted(inc),2)}
        assert allpairs<=router and len(allpairs)==15
        H=allpairs&hot;C=allpairs&cold;assert (len(H),len(C))==(3,12)
        # The dependency cube itself is K6 minus exactly those three hot pairs.
        depcold=set()
        missing=set()
        for a,b in itertools.combinations(R,2):
            e=tuple(sorted((a,b)));me=tuple(sorted((phiR[a],phiR[b])))
            if (rm[a]&rm[b]).bit_count()==2:depcold.add(me)
            else:missing.add(me)
        assert depcold==C and missing==H and len(missing)==3
        p=packet_of_s[s];c=coord_of_s[(p,s)];incident=sorted(i for i,S in enumerate(K5) if p in S);assert len(incident)==3
        groups={f:sorted(v for v in inc if owner[v]==f) for f in incident};assert set(map(len,groups.values()))=={2}
        hot_expected={tuple(sorted(groups[f])) for f in incident};assert hot_expected==H
        blocks={}
        for a,b in itertools.combinations(incident,2):
            E={tuple(sorted((x,y))) for x in groups[a] for y in groups[b]};assert len(E)==4 and E<=C;blocks[(a,b)]=E
        cells[s]={'packet':p,'coord':c,'fibers':incident,'vertices':sorted(inc),'hot':H,'blocks':blocks,'physical':allpairs}
        cold_missing_profiles.append((len(depcold),len(missing)))
    assert Counter(cold_missing_profiles)==Counter({(12,3):135})
    edge_counts=Counter(e for C in cells.values() for e in C['physical'])
    assert set(edge_counts)==router and set(edge_counts.values())=={1}

    # Stabilizers agree literally for a representative cube/cell.
    all40=(1<<40)-1;rep=lambda x:min(int(x),int(x)^all40);sidx={x:i for i,x in enumerate(sing)}
    ui0=0;s0=phiU[ui0];u0=U[ui0]
    Hcube={g for g in G if pmask(u0,g)==u0}
    Hcell={g for g in G if sidx[rep(pmask(sing[s0],g))]==s0}
    assert Hcube==Hcell and len(Hcube)==192

    out6={'pass':4776,'G_set':{'cube_count':135,'cell_count':135,'PSp_transitive':True,'representative_stabilizer_order':192,
        'stabilizers_equal_as_subgroups':True,'equivariant_map':'cube union u -> phiU(u)=selected135 vertex -> its Pass4748 cell'},
      'local_geometry':{'cube_residues':6,'dependency_cold_edges':12,'dependency_graph':'K6 - 3K2','missing_pairs':3,
        'missing_pairs_equal_Petersen_hot_edges':True,'completed_physical_cell':'K6','physical_edges':15,
        'cold_partition':'three K2,2 blocks between the three matched residue pairs'},
      'global_partition':{'135_cells_partition_all_2025_router_edges':True},
      'theorem':'The 135 dependency cubes and 135 cross-fiber coding cells are the same PSp(4,3) G-set under an explicit equivariant bijection with identical order-192 stabilizers. Each cube is K6-3K2 in the cold residue graph; its three missing pairs become exactly the Petersen-hot matching, completing the fifteen-edge K6 coding cell.',
      'boundary':'Exact finite incidence/G-set identification. The K6 completion is a router combinatorial structure, not a six-particle interaction.'}
    OUT6.write_text(json.dumps(out6,indent=2,sort_keys=True)+'\n')

    # Build the physical weight-7 logical generator indexed by each incident quotient line.
    edges=sorted(router);eidx={e:i for i,e in enumerate(edges)}
    logical=[];groups_by_line=defaultdict(list);genmasks=[]
    for s in range(135):
        C=cells[s];F=C['fibers'];Hall=set(C['hot'])
        for L in F:
            others=sorted(set(F)-{L});block=C['blocks'][tuple(sorted(others))]
            supp=Hall|block;assert len(supp)==7
            m=sum(1<<eidx[e] for e in supp);j=len(logical)
            logical.append((s,L));groups_by_line[L].append(j);genmasks.append(m)
    assert len(logical)==405 and Counter(map(len,groups_by_line.values()))==Counter({15:27})
    assert gf2_rank(genmasks)==405
    # Local intersections certify the [15,3,7] weight law 0,7,8,15.
    for s in range(135):
        I=[j for j,(ss,L) in enumerate(logical) if ss==s];assert len(I)==3
        ws=sorted((genmasks[I[a]]^genmasks[I[b]]).bit_count() for a,b in itertools.combinations(range(3),2));assert ws==[8,8,8]
        assert (genmasks[I[0]]^genmasks[I[1]]^genmasks[I[2]]).bit_count()==15

    # Even-parity outer code: 27 disjoint checks on the logical coordinate groups.
    even_dim=405-27;even_d=14
    # Explicit d=14 witness: two weight-7 logical generators in the same quotient-line group, distinct cells.
    L0=min(groups_by_line);a,b=groups_by_line[L0][:2];assert logical[a][0]!=logical[b][0]
    witness=(genmasks[a]^genmasks[b]).bit_count();assert witness==14
    # Proof boundary: every line group has even logical weight, so total logical weight W is even.
    # If W=2 the two coordinates lie in one group and in distinct cells => 7+7=14.
    # If W>=4, local physical weight w(h) for h=1,2,3 active logical bits in a cell is 7,8,15 >=4h, hence physical weight >=16.

    # Repetition outer code: one bit per quotient line, repeated over its 15 logical coordinates.
    rep_rows=[]
    for L in range(27):
        m=0
        for j in groups_by_line[L]:m^=genmasks[j]
        assert m.bit_count()==105;rep_rows.append(m)
    assert gf2_rank(rep_rows)==27
    # At each cell, h selected incident lines gives local weight f(h)=0,7,8,15, a strictly increasing function.
    # Hence adding a selected quotient line strictly increases weight; minimum nonzero repetition word is one line, weight105.
    rep_d=105

    out2={'pass':4772,'logical_geometry':{'local_code':'[15,3,7]_2','cells':135,'logical_coordinates':405,
        'logical_index':'(selected135 cell, one of the three quotient GQ lines through its packet)','quotient_line_groups':27,'coordinates_per_group':15},
      'even_line_coupling':{'parameters':'[2025,378,14]_2','dimension':even_dim,'distance':even_d,'parity_checks':27,
        'explicit_weight14_witness':True,'K_times_d':even_dim*even_d},
      'repetition_line_coupling':{'parameters':'[2025,27,105]_2','dimension':27,'distance':rep_d,'K_times_d':27*rep_d},
      'comparisons':{'Pass4748_direct_sum':'[2025,405,7]_2','Pass4748_K_times_d':405*7,'Pass4748_uncoupled_baseline':'[2025,567,4]_2','baseline_K_times_d':567*4},
      'symmetry':'All constraints are indexed only by the intrinsic 27 GQ lines and the complementary-line labeling of the local S3 permutation module; PSp and the PGSp outer automorphism permute the 27 groups, so both coupled codes are PGSp-invariant.',
      'distance_proof':'For even coupling, total logical weight is even. Weight two forces two distinct cells in one quotient-line group and gives 7+7=14; logical weight >=4 gives physical weight >=4W>=16 because local weights are 7,8,15 for h=1,2,3. For repetition, the local weight f(h)=0,7,8,15 is strictly increasing as quotient lines are added, so a single selected quotient line is the unique minimum type and has 15*7=105.',
      'theorem':'The 135 local cross-fiber codes admit canonical global GQ-line coupling. One even check on each of 27 disjoint fifteen-coordinate logical groups yields an exact PGSp-invariant [2025,378,14]_2 code, doubling distance from 7 to 14 for only 27 lost dimensions. Repetition on each group yields [2025,27,105]_2.',
      'boundary':'Exact binary linear-code construction and distance proof. No universal coding optimum or hardware fault-tolerance threshold is claimed.'}
    OUT2.write_text(json.dumps(out2,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'4772':out2,'4776':out6},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
