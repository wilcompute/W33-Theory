#!/usr/bin/env python3
"""Pass 5057: all-q local theta cut-space theorem and global distance reduction."""
from __future__ import annotations
import itertools,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from analysis.w33_pass5056_q4_theta_apartment_code import build_geometry,gf2_rank
OUT=ROOT/'data/PART_W33_PASS5057_LOCAL_THETA_CUTSPACE.json'

def local_certificate(q):
    n=q+1;edges=list(itertools.combinations(range(n),2));ei={e:i for i,e in enumerate(edges)};tri=[]
    for a,b,c in itertools.combinations(range(n),3):tri.append((1<<ei[(a,b)])^(1<<ei[(a,c)])^(1<<ei[(b,c)]))
    rr=gf2_rank(tri);m=len(edges);dim=m-rr;cuts=set();weights=Counter()
    for bits in range(1<<n):
        x=0
        for k,(i,j) in enumerate(edges):
            if ((bits>>i)^(bits>>j))&1:x|=1<<k
        cuts.add(x)
    assert len(cuts)==1<<(n-1)
    for x in cuts:
        weights[x.bit_count()]+=1;assert all((x&r).bit_count()%2==0 for r in tri)
    nz=[w for w in weights if w];expected=sorted({s*(n-s) for s in range(1,n)})
    assert rr==(n-1)*(n-2)//2 and dim==n-1==q and min(nz)==q and sorted(nz)==expected
    return {'q':q,'local_geodesics':n,'local_apartments':m,'theta_relations':len(tri),'theta_relation_rank':rr,'theta_kernel_dimension':dim,'nonzero_cut_weights':expected,'minimum_nonzero_local_weight':q}

def q4_chamber_star_witness():
    G=build_geometry();support={i for i,row in enumerate(G['apartment_cycle_rows']) if row&1};assert len(support)==256
    ph=Counter()
    for p,q,common in G['opposite_point_pairs']:
        w=sum(G['apt_index_by_points'][frozenset((p,q,common[i],common[j]))] in support for i,j in itertools.combinations(range(5),2))
        if w:ph[w]+=1
    lh=Counter()
    for l,m,common in G['opposite_line_pairs']:
        w=sum(G['apt_index_by_lines'][frozenset((l,m,common[i],common[j]))] in support for i,j in itertools.combinations(range(5),2))
        if w:lh[w]+=1
    ap=sum(ph.values());al=sum(lh.values());assert ph==Counter({4:128}) and lh==Counter({4:128}) and ap+al==256
    return {'support_weight':256,'active_opposite_point_charts':ap,'active_opposite_line_charts':al,'active_charts_total':ap+al,'active_cut_weight_histogram_points':dict(ph),'active_cut_weight_histogram_lines':dict(lh),'identity':'4*wt = q*A = 1024 for the q=4 chamber-star word'}

def main():
    local=[local_certificate(q) for q in range(2,11)];q4=q4_chamber_star_witness()
    result={'pass':5057,'status':'PASS','theorem':'Local theta relations are exactly the cut-space equations of K_{q+1}.','symbolic_proof':['Fix one of q+1 geodesics as vertex 0.','For every i<j, the theta triangle (0,i,j) imposes x_ij=x_0i+x_0j over F2.','Hence every solution is a cut x_ij=a_i+a_j, unique modulo adding 1 to all potentials.','Therefore the local solution dimension is q.','A cut with s versus q+1-s vertices has weight s(q+1-s), whose nonzero minimum is q.'],'local_formulae':{'geodesics':'q+1','apartments_edges':'C(q+1,2)','theta_triangles':'C(q+1,3)','theta_relation_rank':'q(q-1)/2','theta_kernel_dimension':'q','nonzero_cut_weight':'s(q+1-s), 1<=s<=q','minimum_local_weight':'q'},'global_double_count':{'identity':'4 wt(x) = sum_O wt(x|_O)','reason':'every apartment has exactly two opposite point pairs and two opposite line pairs','active_chart_bound':'if A(x) is the number of nonzero opposite-pair charts, wt(x) >= q A(x)/4','distance_reduction':'A(x)>=4q^3 for every nonzero theta-code word would imply d>=q^4','upper_bound':'the chamber-star word has q^4 apartments, so d<=q^4','remaining_wall':'prove A(x)>=4q^3 in general, or identify theta relations with a complete all-q Steinberg presentation'},'checked_local_q':local,'q4_chamber_star':q4,'external_bridge':'Recent symplectic Steinberg-module presentation/resolution work expresses the module through apartment/sharbly relations. The exact identification of this rank-2 finite-field theta subsystem with a complete presentation remains to be proved.','boundary':'This is an all-q local theorem and an all-q global reduction, not an all-q minimum-distance theorem. Pass5056 proves the missing global statement only at q=4.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
