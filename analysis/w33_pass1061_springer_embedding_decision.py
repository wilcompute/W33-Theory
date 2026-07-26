from __future__ import annotations
import json, time
from pathlib import Path
from w33_pass1060_1064_core import *
from sympy.combinatorics import Permutation,PermutationGroup

def arbitrary_actions(w,q,a,g):
    qim=[q.canon_to_coord[reduce_basis(perm_word(q.rep[c],g),q.C)] for c in range(256)]
    qg=Permutation(qim)
    li={L:i for i,L in enumerate(w.lines)};ai={x:i for i,x in enumerate(a.axes)}
    def ml(l):return li[tuple(sorted(g(p) for p in w.lines[l]))]
    aim=[]
    for p,m in a.axes:
        mm=tuple(sorted(tuple(sorted((ml(x),ml(y)))) for x,y in m));aim.append(ai[(g(p),mm)])
    return qg,Permutation(aim)

def rank_bits(vs):return len(row_basis(vs))

def main():
    w=build_w33();q=build_quot(w);a=build_axes(w,q);e=build_e8();F=isometry(q,e)
    sim=matrix_perm(w,[[1,0,0,0],[0,2,0,0],[0,0,1,0],[0,0,0,2]])
    qsim,asim=arbitrary_actions(w,q,a,sim)
    PG=PermutationGroup(q.gens+[qsim]); AG=PermutationGroup(a.axis_gens+[asim]); P40=PermutationGroup(w.gens+[sim])
    equiv_fail=0
    for gg,aa in zip(q.gens+[qsim],a.axis_gens+[asim]):
        for i,c in enumerate(a.coords):
            if a.coords[aa(i)]!=gg(c):equiv_fail+=1
    orbits=sorted(len(o) for o in PG.orbits())
    def subset_orbits(domain):
        unseen=set(domain); sizes=[]; gens=q.gens+[qsim]
        while unseen:
            seed=next(iter(unseen)); orb={seed}; stack=[seed]; unseen.remove(seed)
            while stack:
                x=stack.pop()
                for gg in gens:
                    y=gg(x)
                    if y not in orb:
                        orb.add(y); unseen.discard(y); stack.append(y)
            sizes.append(len(orb))
        return sorted(sizes)
    ani_orbits=subset_orbits(q.ani); iso_orbits=subset_orbits(q.iso)
    span_rank=rank_bits(q.ani)
    checks={
      'similitude_doubles_PSp_to_PGSp':P40.order()==51840 and PG.order()==51840,
      'full_axis_action_order_51840':AG.order()==51840,
      'axis_to_code_map_equivariant_for_all_generators_including_outer':equiv_fail==0,
      'rootline_transport_has_order_51840':AG.order()==51840,
      'whole_256_orbits_are_code_fingerprint':orbits==[1,120,135],
      'anisotropic_orbit_is_120':ani_orbits==[120],
      'isotropic_orbit_is_135':iso_orbits==[135],
      'anisotropic_set_spans_F2_8':span_rank==8,
      'ordered_pair_fingerprint_is_excluded':[27,36,36,36]!=iso_orbits,
    }
    assert all(checks.values()),checks
    return {
      'schema':'w33.pass1061.springer_embedding_decision.v1','status':'PASS',
      'headline':'The Springer normalizer realizes the W33 code embedding, not the ordered-anisotropic-pair embedding. Its certified point action on the 40 Eisenstein fibres extends functorially to the binary adjacency code; the full PGSp(4,3) action is equivariant on all 120 local axes/root lines and has whole-group quotient orbits 1+120+135.',
      'decision':'CODE EMBEDDING',
      'logic_chain':[
        'Pass1021 identifies the Springer normalizer base action, by explicit S40 conjugacy, with the W33 POINT action and its full image with Aut(W33)=PGSp(4,3).',
        'C, Cperp, Cperp/C and the 120 local-axis supports are functorial constructions of that 40-point incidence action.',
        'This witness adds the multiplier-2 outer generator and verifies the axis-to-anisotropic-class map generator-by-generator for the full order-51840 group.',
        'The 120 anisotropic classes span F2^8, so the linear orthogonal action on them determines the entire 256-class action.',
        'The resulting matched whole-group orbits are 1+120+135, excluding the ordered-pair fingerprint 27+36+36+36 on the isotropic stratum.'
      ],
      'orders':{'base_point_action':int(P40.order()),'code_quotient_action':int(PG.order()),'axis_rootline_action':int(AG.order())},
      'whole_group_orbits':{'all_256':orbits,'anisotropic':ani_orbits,'nonzero_isotropic':iso_orbits},
      'anisotropic_span_rank':span_rank,
      'check_count':len(checks),'checks':checks,
      'supersession':'Pass1043 is now decided in the opposite direction from its original interpretation. Pass1057 correctly reopened it; the matched full-group action selects Pass125 code embedding.',
      'scope':'The decision uses the exact Pass1021 point-action conjugacy plus an independent full-PGSp functorial equivariance computation. It does not identify the ordered-pair subgroup by generators because its incompatible orbit fingerprint already excludes it.'
    }
if __name__ == "__main__":
    started = time.time(); result = main()
    output = Path(__file__).resolve().parents[1] / "data" / "w33_pass1061_springer_embedding_decision.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "headline": result["headline"], "check_count": result["check_count"], "output": str(output), "seconds": round(time.time()-started, 3)}, indent=2))
