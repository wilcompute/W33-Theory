#!/usr/bin/env python3
"""Objectwise realization of the previously known BT1774 E8 Coxeter inversion.

Unlike the prior existence certificate, reports actual induced action on the
40 W33 fibers, sixfold phase intercepts and graph automorphism. Does not claim
a newly discovered Weyl conjugator.
"""
from pathlib import Path
import json,sys
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass7163_7170_e8_hexagonal_lift as E
import bt1774_e8_inversion_witness as W
OUT=ROOT/"data"/"2026_11_03_e8_base_permuting_global_inversion.json"
def apply_seq(v,seq):
    for i in seq:v=E.refl(v,E.SIMPLES[i])
    return v
def test_word(v,seq,reverse=False):
    return apply_seq(v,list(reversed(seq)) if reverse else seq)
def run():
    roots,fibs,phases,radj,base,zero,pairs,hist=E.e8_fibers()
    I={r:i for i,r in enumerate(roots)}
    words=[]
    for reverse in (False,True):
        for order in ("F_then_reverse_B","B_then_reverse_F"):
            def h(v):
                a=W.FSEQ if order.startswith("F") else W.BSEQ
                b=W.BSEQ if order.startswith("F") else W.FSEQ
                if reverse:
                    a=list(reversed(a));b=list(reversed(b))
                return apply_seq(apply_seq(v,a),list(reversed(b)))
            if not all(h(E.cox(r))==apply_seq(h(r),list(reversed(range(8)))) for r in roots):
                # E.cox uses Bourbaki order; its inverse applies 7..0.
                continue
            words.append((reverse,order,h))
    assert words,"Could not independently reconstruct BT1774 word: do not publish"
    reverse,order,h=words[0]
    perm=tuple(I[h(r)] for r in roots)
    assert len(set(perm))==240
    assert all(perm[I[E.cox(r)]]==I[apply_seq(h(r),list(reversed(range(8))))] for r in roots)
    fiber_map=[]
    alphas=[]
    phase_counts=[]
    for f,F in enumerate(fibs):
        images=[perm[i] for i in F]
        target=next(t for t,G in enumerate(fibs) if images[0] in G)
        assert set(images)==set(fibs[target])
        k_image=[fibs[target].index(a) for a in images]
        intercept=k_image[0]%6
        assert k_image==[(intercept-k)%6 for k in range(6)],(f,k_image)
        fiber_map.append(target);alphas.append(intercept);phase_counts.append(k_image)
    assert len(set(fiber_map))==40
    assert any(fiber_map[i]!=i for i in range(40))
    for a in range(40):
        for b in range(40):
            assert (b in base[a])==(fiber_map[b] in base[fiber_map[a]])
    assert all({perm[j] for j in radj[i]}==radj[perm[i]] for i in range(240))
    cycles=[];remaining=set(range(40))
    while remaining:
        u=min(remaining);cur=u;cc=[]
        while cur not in cc:
            cc.append(cur);remaining.remove(cur);cur=fiber_map[cur]
        assert cur==u
        cycles.append(cc)
    # h*h is a power of Coxeter, possibly identity; classify on phase.
    hhphase=[fibs[fiber_map[fiber_map[f]]].index(perm[perm[fibs[f][0]]]) for f in range(40)]
    roots_fixed=sum(i==perm[i] for i in range(240))
    ans={"status":"PASS_BT1774_OBJECTWISE_BASE_PERMUTING_REFLECTION",
      "prior_weyl_word":"BT1774 sequences FSEQ/BSEQ; reconstruction convention autodetected",
      "reconstruction":{"reverse_sequence_applied":reverse,"operation":order},
      "coxeter_conjugation_h_c_h_inverse":"c^-1 on each of 240 roots verified",
      "fiber_map":fiber_map,"fiber_map_fixed_count":sum(f==fiber_map[f] for f in range(40)),
      "fiber_map_cycle_sizes":dict(sorted(Counter(map(len,cycles)).items())),
      "fiber_map_cycle_witnesses":cycles,
      "affine_reflection_intercepts_mod6":alphas,
      "square_action_phase_on_k0":hhphase,
      "root_permutation_fixed_count":roots_fixed,
      "all_540_cross_fiber_edges_preserved":True,
      "base_collinearity_adjacency_preserved":True,
      "all_40_phases_obey_k_to_alpha_minus_k":True,
      "comparison":"Our earlier fixed-base no-go excludes maps (f,k)->(f,alpha_f-k). The known Coxeter inversion h acts (f,k)->(sigma(f),alpha_f-k), with sigma nontrivial; its base permutation resolves that obstruction. Existing BT1774 supplies the conjugator itself.",
      "not_physics":"No left-handed fermions, Lorentzian parity violation or Standard Model chirality derived."
    }
    OUT.write_text(json.dumps(ans,indent=2)+"\n",encoding="utf-8")
    print("INVERSION BRIDGE",ans["fiber_map_cycle_sizes"],"fixed",ans["fiber_map_fixed_count"],"word",order,reverse)
    return ans
if __name__=="__main__":run()
