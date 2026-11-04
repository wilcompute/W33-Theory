#!/usr/bin/env python3
"""Fuse three C3-equivariant 81-apartment bases to improve conditioning.

Exact: DB=0, C3 invariance, integer interaction census, independent
GF(2) basis witnesses from each constituent.
Numerical: 81D positive spectrum and condition-number estimates.
"""
from pathlib import Path
import importlib.util,json,math
from itertools import product
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("c3",ROOT/"analysis"/"toe_20261103_c3_symmetry_selector.py")
c3=importlib.util.module_from_spec(spec);spec.loader.exec_module(c3)
OUT=ROOT/"data"/"toe_20261103_c3_tightframe_fusion.json"

def run():
    D,C,flags=c3.mod.build()
    signed={tuple(np.flatnonzero(C[:,j]).tolist()):C[:,j] for j in range(C.shape[1])}
    pointset=sorted({c3.mod.canon(v) for v in product(range(3),repeat=4) if any(v)})
    pidx={x:i for i,x in enumerate(pointset)}
    lines=[[] for _ in range(40)]
    for p,l in flags:lines[l].append(p)
    lines=[tuple(sorted(line)) for line in lines]
    lidx={line:i for i,line in enumerate(lines)}
    fidx={fl:i for i,fl in enumerate(flags)}
    anchor=pointset[0]
    pp=[pidx[c3.mod.canon(tuple((p[k]+c3.mod.symp(p,anchor)*anchor[k])%3 for k in range(4)))] for p in pointset]
    lp=[lidx[tuple(sorted(pp[x] for x in line))] for line in lines]
    perm=np.array([fidx[(pp[p],lp[l])] for p,l in flags])
    def condition(M,Q):
        e=np.linalg.eigvalsh(Q.T@M@Q)
        return dict(min_positive=float(e[0]),max_positive=float(e[-1]),
                    condition=float(e[-1]/e[0]))
    prev_indices,_=c3.mod.choose(C,seed=33)
    prev_B=C[:,prev_indices]
    Q,_=np.linalg.qr(prev_B.astype(float))
    prev_H=prev_B@prev_B.T
    selected=[]
    Hs=[]
    for seed in [5,9,18]:
        row=c3.certificate(seed=seed,save=False)
        assert row["max_flag_load"]==6 and row["cycle_GF2_rank"]==81
        supports=row["selected_apartment_flag_supports"]
        B=np.stack([signed[tuple(s)] for s in supports],axis=1)
        H=B@B.T
        assert not np.any(D@B)
        conjugate=np.zeros_like(H);conjugate[np.ix_(perm,perm)]=H
        assert np.array_equal(H,conjugate)
        selected.append(dict(seed=seed,cycle_supports=supports,condition=condition(H,Q)["condition"]))
        Hs.append(H)
    total=sum(Hs)
    assert not np.any(D@total)
    conjugate=np.zeros_like(total);conjugate[np.ix_(perm,perm)]=total
    assert np.array_equal(total,conjugate)
    S=np.sign(total).astype(np.int64);np.fill_diagonal(S,0)
    absS=np.abs(S)
    triangles=int(np.trace(absS@absS@absS)//6)
    signed_sum=int(np.trace(S@S@S)//6)
    negative=(triangles-signed_sum)//2
    nlinks=int(np.count_nonzero(np.triu(total,1)))
    assert nlinks==4320 and negative==13066
    loads=np.diag(total).astype(int)
    assert int(loads.sum())==3*81*8
    cond=condition(total,Q)
    assert cond["condition"]<7.01
    assert max(loads)<=18
    pairs=[(5,13)]
    pairdata=[]
    for s,t in pairs:
        if s==13 or t==13:
            extra=c3.certificate(seed=13,save=False)
            eb=np.stack([signed[tuple(x)] for x in extra["selected_apartment_flag_supports"]],axis=1)
            EH=eb@eb.T
            pair=Hs[0]+EH
            pcond=condition(pair,Q)
            pairdata.append(dict(seeds=[5,13],condition=pcond["condition"],
                                 nonzero_hoppings=int(np.count_nonzero(np.triu(pair,1)))))
    out=dict(status="PASS_EXACT_C3_THREE_FRAME_FUSION_AND_SPECTRAL_EQUALIZATION",
        constituent_seeds=[5,9,18],constituent_witnesses=selected,
        C3_symmetry_verified_exact=True,cycle_cut_leakage_zero_exact=True,
        three_frames_cycle_count=243,max_individual_frame_load=6,
        fused_flag_load_min=int(min(loads)),fused_flag_load_max=int(max(loads)),
        fused_hopping_pairs=nlinks,max_offdiag_neighbors=int(np.max(np.count_nonzero(total,axis=1)-1)),
        signed_triangles=triangles,pi_flux_triangles=negative,
        original_seed33=condition(prev_H,Q),
        single_C3_seed5=condition(Hs[0],Q),
        two_C3_seed5_13=pairdata,
        three_C3_fused=cond,
        conditioning_gain_from_seed33=condition(prev_H,Q)["condition"]/cond["condition"],
        limitations="Three overlapping local frame operators increase maximum flag participation and network degree. C3 is selected, not derived; spectrum is numerical; not a physical continuum or hardware circuit.")
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(out["status"],"condition",cond["condition"],"hoppings",nlinks,flush=True)
    return out

if __name__=="__main__":run()
